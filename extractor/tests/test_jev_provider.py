import io
import json
import urllib.error
from datetime import datetime, timezone

import pytest

import kb_pipeline.jev_provider as jev_provider
from kb_pipeline.jev_provider import (
    JevConfigurationError,
    JevRequestError,
    JevResponseError,
    JevTransportError,
    evaluate_jev,
)
from kb_pipeline.schemas import ContextBundle, ContextItem, ContextStatus, SourceRecord

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def make_source(
    source_id: str,
    *,
    author: str,
    text: str,
    reply_to_id: str | None = None,
    quoted_source_id: str | None = None,
) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        author=author,
        text=text,
        url=f"https://x.com/{author}/status/{source_id[2:]}",
        reply_to_id=reply_to_id,
        quoted_source_id=quoted_source_id,
        conversation_id="x:100",
        fetched_at=NOW,
        language="en",
        raw_ref=f"cache:test:{source_id}",
        content_hash="a" * 64,
    )


def make_bundle() -> ContextBundle:
    focus = make_source(
        "x:100",
        author="alice",
        text="Prune stale tool output before it consumes the context budget.",
        reply_to_id="x:101",
        quoted_source_id="x:102",
    )
    parent = make_source(
        "x:101",
        author="bob",
        text="The parent post reports a long benchmark run.",
    )
    quote = make_source(
        "x:102",
        author="chen",
        text="The quoted post proposes retaining tool errors.",
    )
    return ContextBundle(
        focus=focus,
        related=[
            ContextItem(source=parent, role="parent", provenance="cache:parent"),
            ContextItem(source=quote, role="quote", provenance="cache:quote"),
        ],
        context_status=ContextStatus.complete,
    )


def make_response(topic: str = "compaction") -> dict:
    probabilities = {option: 0.0 for option in ("compaction", "evals", "harness", "other")}
    probabilities[topic] = 1.0
    return {
        "model": "jev-1.13.0",
        "answers": {
            "engineering_value": {"type": "noul", "noul": 0.91},
            "context_sufficient": {"type": "noul", "noul": 0.84},
            "topic": {
                "type": "choice",
                "choice": topic,
                "probabilities": probabilities,
                "confidence": 1.0,
            },
        },
        "usage": {"input_tokens": 320, "output_tokens": 42},
    }


def encode(payload) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def http_error(status: int, *, headers=None, body: bytes = b"") -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "https://api.typesafe.ai/v1/systemone",
        status,
        "request failed",
        headers or {},
        io.BytesIO(body),
    )


def test_evaluate_posts_structured_request_and_returns_complete_response(monkeypatch):
    bundle = make_bundle()
    response = make_response()
    captured = {}

    monkeypatch.setenv("TYPESAFE_API_KEY", "environment-key")

    def transport(request, timeout):
        captured["request"] = request
        captured["timeout"] = timeout
        return encode(response)

    result = evaluate_jev(bundle, timeout=2.5, transport=transport)

    request = captured["request"]
    assert request.full_url == "https://api.typesafe.ai/v1/systemone"
    assert request.method == "POST"
    assert request.get_header("Authorization") == "Bearer environment-key"
    assert request.get_header("Content-type") == "application/json"
    assert captured["timeout"] == 2.5

    payload = json.loads(request.data.decode("utf-8"))
    assert set(payload) == {"state", "model", "questions"}
    assert payload["model"] == "jev-latest"
    assert payload["state"]["focus"]["source_id"] == "x:100"
    assert payload["state"]["focus"]["author"] == "alice"
    assert payload["state"]["focus"]["text"].startswith("Prune stale")
    assert payload["state"]["focus"]["provenance"] == "cache:test:x:100"
    assert payload["state"]["missing_ids"] == []
    assert [
        (item["source_id"], item["author"], item["role"], item["provenance"])
        for item in payload["state"]["related"]
    ] == [
        ("x:101", "bob", "parent", "cache:parent"),
        ("x:102", "chen", "quote", "cache:quote"),
    ]
    assert payload["state"]["related"][0]["text"] != payload["state"]["related"][1]["text"]

    questions = payload["questions"]
    assert questions["engineering_value"]["type"] == "noul"
    assert questions["context_sufficient"]["type"] == "noul"
    assert questions["topic"]["type"] == "choice"
    assert set(questions["topic"]["criteria"]) == {"compaction", "evals", "harness", "other"}
    assert "does not imply rejection" in questions["topic"]["criteria"]["other"]
    assert result == response


def test_missing_api_key_fails_before_transport(monkeypatch):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    calls = 0

    def transport(request, timeout):
        nonlocal calls
        calls += 1
        raise AssertionError("transport should not be called")

    with pytest.raises(JevConfigurationError, match="TYPESAFE_API_KEY"):
        evaluate_jev(make_bundle(), transport=transport)

    assert calls == 0


def test_authentication_error_is_clear_and_sanitized():
    key = "private-test-key"
    calls = 0

    def transport(request, timeout):
        nonlocal calls
        calls += 1
        raise http_error(401, body=encode({"debug_authorization": key}))

    with pytest.raises(JevConfigurationError) as caught:
        evaluate_jev(make_bundle(), api_key=key, transport=transport)

    assert calls == 1
    assert "HTTP 401" in str(caught.value)
    assert "TYPESAFE_API_KEY" in str(caught.value)
    assert key not in str(caught.value)


def test_schema_error_is_not_retried():
    calls = 0

    def transport(request, timeout):
        nonlocal calls
        calls += 1
        raise http_error(422, body=b'{"field":"state"}')

    with pytest.raises(JevRequestError, match="HTTP 422"):
        evaluate_jev(make_bundle(), api_key="test-key", max_attempts=3, transport=transport)

    assert calls == 1


@pytest.mark.parametrize("status", [429, 529])
def test_transient_status_is_retried(monkeypatch, status):
    attempts = 0
    delays = []
    monkeypatch.setattr(jev_provider.time, "sleep", delays.append)

    def transport(request, timeout):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise http_error(status, headers={"Retry-After": "0"})
        return encode(make_response("other"))

    result = evaluate_jev(
        make_bundle(),
        api_key="test-key",
        max_attempts=2,
        transport=transport,
    )

    assert result["answers"]["topic"]["choice"] == "other"
    assert attempts == 2
    assert delays == [0.0]


def test_temporary_network_failure_is_retried(monkeypatch):
    attempts = 0
    delays = []
    monkeypatch.setattr(jev_provider.time, "sleep", delays.append)

    def transport(request, timeout):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise urllib.error.URLError("temporary connection failure")
        return encode(make_response())

    evaluate_jev(
        make_bundle(),
        api_key="test-key",
        max_attempts=2,
        transport=transport,
    )

    assert attempts == 2
    assert delays == [jev_provider._INITIAL_RETRY_DELAY_SECONDS]


def test_retry_after_at_limit_is_honored(monkeypatch):
    attempts = 0
    delays = []
    monkeypatch.setattr(jev_provider.time, "sleep", delays.append)

    def transport(request, timeout):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise http_error(
                429,
                headers={"Retry-After": str(int(jev_provider._MAX_RETRY_DELAY_SECONDS))},
            )
        return encode(make_response())

    evaluate_jev(
        make_bundle(),
        api_key="test-key",
        max_attempts=2,
        transport=transport,
    )

    assert attempts == 2
    assert delays == [jev_provider._MAX_RETRY_DELAY_SECONDS]


def test_retry_after_over_limit_stops_retrying(monkeypatch):
    attempts = 0
    delays = []
    monkeypatch.setattr(jev_provider.time, "sleep", delays.append)

    def transport(request, timeout):
        nonlocal attempts
        attempts += 1
        raise http_error(429, headers={"Retry-After": "120"})

    with pytest.raises(JevRequestError, match="retry later"):
        evaluate_jev(
            make_bundle(),
            api_key="test-key",
            max_attempts=2,
            transport=transport,
        )

    assert attempts == 1
    assert delays == []


def test_network_retry_count_is_bounded(monkeypatch):
    attempts = 0
    delays = []
    monkeypatch.setattr(jev_provider.time, "sleep", delays.append)

    def transport(request, timeout):
        nonlocal attempts
        attempts += 1
        raise urllib.error.URLError("still unavailable")

    with pytest.raises(JevTransportError, match="after 2 attempts"):
        evaluate_jev(
            make_bundle(),
            api_key="test-key",
            max_attempts=2,
            transport=transport,
        )

    assert attempts == 2
    assert delays == [jev_provider._INITIAL_RETRY_DELAY_SECONDS]


@pytest.mark.parametrize(
    "raw_response",
    [
        pytest.param(b"not-json", id="invalid-json"),
        pytest.param(
            encode(
                {
                    "model": "jev-1.13.0",
                    "answers": {
                        "engineering_value": {"type": "noul", "noul": 0.9},
                        "topic": {
                            "type": "choice",
                            "choice": "harness",
                            "probabilities": {
                                "compaction": 0.0,
                                "evals": 0.0,
                                "harness": 1.0,
                                "other": 0.0,
                            },
                            "confidence": 1.0,
                        },
                    },
                    "usage": {"input_tokens": 10, "output_tokens": 3},
                }
            ),
            id="missing-answer",
        ),
        pytest.param(
            encode(
                {
                    "model": "jev-1.13.0",
                    "answers": {
                        "engineering_value": {"type": "noul", "noul": 0.9},
                        "context_sufficient": {"type": "noul", "noul": 0.8},
                        "topic": {"type": "noul", "noul": 0.7},
                    },
                    "usage": {"input_tokens": 10, "output_tokens": 3},
                }
            ),
            id="wrong-answer-type",
        ),
    ],
)
def test_malformed_response_raises_response_error(raw_response):
    def transport(request, timeout):
        return raw_response

    with pytest.raises(JevResponseError):
        evaluate_jev(make_bundle(), api_key="test-key", transport=transport)


def test_unicode_source_text_reaches_transport_unchanged():
    text = "将旧工具输出压缩，并为代理保留可恢复的检查点。"
    focus = make_source("x:200", author="作者", text=text, reply_to_id="x:201")
    bundle = ContextBundle(
        focus=focus,
        missing_ids=["x:201"],
        context_status=ContextStatus.unavailable,
    )
    captured = {}

    def transport(request, timeout):
        captured["raw"] = request.data
        return encode(make_response("other"))

    evaluate_jev(bundle, api_key="test-key", transport=transport)

    assert text.encode("utf-8") in captured["raw"]
    payload = json.loads(captured["raw"].decode("utf-8"))
    assert payload["state"]["focus"]["text"] == text
    assert payload["state"]["focus"]["author"] == "作者"


def test_missing_parent_remains_explicit_in_state():
    focus = make_source("x:300", author="alice", text="Yes", reply_to_id="x:301")
    bundle = ContextBundle(
        focus=focus,
        missing_ids=["x:301"],
        context_status=ContextStatus.unavailable,
    )
    captured = {}

    def transport(request, timeout):
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        response = make_response("other")
        response["answers"]["context_sufficient"] = {"type": "noul", "noul": 0.1}
        return encode(response)

    result = evaluate_jev(bundle, api_key="test-key", transport=transport)

    state = captured["payload"]["state"]
    assert state["focus"]["source_id"] == "x:300"
    assert state["related"] == []
    assert state["missing_ids"] == ["x:301"]
    assert state["context_status"] == "unavailable"
    assert result["answers"]["context_sufficient"]["noul"] == 0.1
