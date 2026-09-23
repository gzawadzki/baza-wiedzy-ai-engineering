from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

import pytest

from kb_pipeline.jev_provider import (
    JevConfigurationError,
    JevRequestError,
    JevResponseError,
    JevTransportError,
)
from kb_pipeline.live_jev import compute_context_hash, evaluate_live_source
from kb_pipeline.schemas import ContextBundle, ContextItem, ContextStatus, SourceRecord
from kb_pipeline.stage_cache import StageCache
from kb_pipeline.storage import SourceStore

EXTRACTOR = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _hash_tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    vault.mkdir(parents=True, exist_ok=True)
    (vault / ".obsidian").mkdir(exist_ok=True)
    (vault / "Pojęcia").mkdir(exist_ok=True)
    (vault / "Pojęcia" / "Note.md").write_text("# Note\nExisting content.\n", encoding="utf-8")
    return vault


def make_source(
    source_id: str,
    *,
    author: str = "alice",
    text: str = "Prune stale tool output before it consumes the context budget.",
    content_hash: str | None = None,
    reply_to_id: str | None = None,
    quoted_source_id: str | None = None,
) -> SourceRecord:
    chash = content_hash or hashlib.sha256(text.encode("utf-8")).hexdigest()
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
        content_hash=chash,
    )


def insert_source(store: SourceStore, record: SourceRecord) -> None:
    store.connection.execute(
        "INSERT INTO source_revisions VALUES (?, ?, ?, ?)",
        (record.source_id, record.content_hash, record.model_dump_json(), "{}"),
    )
    store.connection.commit()


def make_response(
    topic: str = "compaction",
    *,
    engineering_value: float = 0.91,
    context_sufficient: float = 0.84,
) -> dict:
    probabilities = {option: 0.0 for option in ("compaction", "evals", "harness", "other")}
    probabilities[topic] = 1.0
    return {
        "model": "jev-latest",
        "answers": {
            "engineering_value": {"type": "noul", "noul": engineering_value},
            "context_sufficient": {"type": "noul", "noul": context_sufficient},
            "topic": {
                "type": "choice",
                "choice": topic,
                "probabilities": probabilities,
                "confidence": 1.0,
            },
        },
        "usage": {"input_tokens": 320, "output_tokens": 42},
    }


class FakeTransport:
    def __init__(self, response: dict | None = None, error: Exception | None = None):
        self.response = response or make_response()
        self.error = error
        self.call_count = 0
        self.requests: list[object] = []

    def __call__(self, request: object, timeout: float) -> bytes:
        self.call_count += 1
        self.requests.append(request)
        if self.error:
            raise self.error
        return json.dumps(self.response).encode("utf-8")


def test_evaluate_live_source_success(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    before_vault = _hash_tree(vault)
    transport = FakeTransport()

    summary = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
    )

    assert transport.call_count == 1
    assert summary["status"] == "completed"
    assert summary["source_id"] == "x:100"
    assert summary["source_hash"] == source.content_hash
    assert summary["decision"] == "extract"
    assert summary["topic"] == "compaction"
    assert summary["engineering_score"] == 0.91
    assert summary["cached"] is False
    assert summary["usage"] == {"input_tokens": 320, "output_tokens": 42}
    assert _hash_tree(vault) == before_vault

    # Check StageCache
    cache_key = StageCache.key("filter", source.content_hash, summary["context_hash"], "jev-latest", "v1")
    with StageCache(workspace) as cache:
        cached = cache.get(cache_key)
        assert cached is not None
        assert cached["source_id"] == "x:100"
        assert cached["answers"]["topic"]["choice"] == "compaction"
        assert cached["usage"] == {"input_tokens": 320, "output_tokens": 42}

    # Check filesystem artifact
    artifact_path = workspace / summary["artifact_ref"]
    assert artifact_path.is_file()
    artifact_data = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert artifact_data["source_id"] == "x:100"
    assert artifact_data["model"] == "jev-latest"


def test_evaluate_live_source_idempotent_replay_and_refresh(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    transport = FakeTransport()

    first = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 1
    assert first["cached"] is False

    # Second call without refresh should use StageCache and not call transport
    second = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
        refresh=False,
    )
    assert transport.call_count == 1
    assert second["cached"] is True
    assert second["decision"] == first["decision"]
    assert second["context_hash"] == first["context_hash"]

    # Third call with refresh=True should call transport again
    third = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
        refresh=True,
    )
    assert transport.call_count == 2
    assert third["cached"] is False


def test_evaluate_live_source_topic_other(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    transport = FakeTransport(response=make_response(topic="other"))
    summary = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
    )
    assert summary["topic"] == "other"
    assert summary["decision"] == "extract"


def test_evaluate_live_source_context_building_and_hashes(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    focus = make_source("x:100", reply_to_id="x:101", quoted_source_id="x:102")
    parent = make_source("x:101", text="Parent context")
    quote = make_source("x:102", text="Quote context")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        insert_source(store, parent)
        insert_source(store, quote)

    transport = FakeTransport()
    summary = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
    )
    assert summary["context_status"] == ContextStatus.complete.value
    assert summary["context_hash"] is not None

    bundle = ContextBundle(
        focus=focus,
        related=[
            ContextItem(source=parent, role="parent", provenance="cache:lookup"),
            ContextItem(source=quote, role="quote", provenance="cache:lookup"),
        ],
        context_status=ContextStatus.complete,
    )
    assert summary["context_hash"] == compute_context_hash(bundle)


def test_evaluate_live_source_ambiguous_source_fails_without_content_hash(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    rev1 = make_source("x:100", text="Revision 1", content_hash="1" * 64)
    rev2 = make_source("x:100", text="Revision 2", content_hash="2" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, rev1)
        insert_source(store, rev2)

    transport = FakeTransport()
    with pytest.raises(ValueError, match="multiple revisions"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key="test-key",
            transport=transport,
        )
    assert transport.call_count == 0


def test_evaluate_live_source_ambiguous_source_succeeds_with_content_hash(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    rev1 = make_source("x:100", text="Revision 1", content_hash="1" * 64)
    rev2 = make_source("x:100", text="Revision 2", content_hash="2" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, rev1)
        insert_source(store, rev2)

    transport = FakeTransport()
    summary = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        content_hash="2" * 64,
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 1
    assert summary["source_hash"] == "2" * 64


def test_evaluate_live_source_ambiguous_related_source_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    focus = make_source("x:100", reply_to_id="x:101")
    parent1 = make_source("x:101", text="Parent revision 1", content_hash="1" * 64)
    parent2 = make_source("x:101", text="Parent revision 2", content_hash="2" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        insert_source(store, parent1)
        insert_source(store, parent2)

    transport = FakeTransport()
    with pytest.raises(ValueError, match="Multiple revisions found for source 'x:101'"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key="test-key",
            transport=transport,
        )
    assert transport.call_count == 0


def test_evaluate_live_source_missing_source_fails(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    transport = FakeTransport()
    with pytest.raises(ValueError, match="not found in store"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:999",
            api_key="test-key",
            transport=transport,
        )


def test_evaluate_live_source_missing_api_key_fails_closed(tmp_path, monkeypatch):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    with pytest.raises(JevConfigurationError, match="API key is missing"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key=None,
        )


def test_evaluate_live_source_transport_error_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    transport = FakeTransport(error=urllib.error.URLError("connection refused"))
    with pytest.raises(JevTransportError, match="network request failed"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key="test-key",
            transport=transport,
        )

    # Nothing should be in StageCache or artifacts
    with StageCache(workspace) as cache:
        cursor = cache.connection.execute("SELECT count(*) FROM artifacts")
        assert cursor.fetchone()[0] == 0
    assert not (workspace / "artifacts").exists()


def test_evaluate_live_source_http_error_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    error = urllib.error.HTTPError("https://api.typesafe.ai/v1/systemone", 422, "Unprocessable", {}, None)
    transport = FakeTransport(error=error)
    with pytest.raises(JevRequestError, match="rejected the request schema"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key="test-key",
            transport=transport,
        )


def test_evaluate_live_source_invalid_response_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    class MalformedTransport:
        def __call__(self, request: object, timeout: float) -> bytes:
            return b"not json"

    with pytest.raises(JevResponseError, match="malformed JSON"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key="test-key",
            transport=MalformedTransport(),
        )


def test_evaluate_live_source_safe_paths_rejects_workspace_in_vault(tmp_path):
    vault = make_vault(tmp_path)
    workspace = vault / "internal_workspace"

    with pytest.raises(ValueError, match="Workspace must be outside the vault"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key="test-key",
        )


# Subprocess CLI tests


def _run_cli(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env is not None:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, "-m", "kb_pipeline", "jev-evaluate", *args],
        cwd=EXTRACTOR,
        capture_output=True,
        text=True,
        env=merged_env,
        check=False,
    )


def test_cli_subprocess_missing_key(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    env = {"TYPESAFE_API_KEY": ""}
    proc = _run_cli(
        "--vault", str(vault),
        "--workspace", str(workspace),
        "--source-id", "x:100",
        env=env,
    )
    assert proc.returncode == 1
    result = json.loads(proc.stdout)
    assert result["status"] == "error"
    assert "API key is missing" in result["error"]


def test_cli_subprocess_safe_path(tmp_path):
    vault = make_vault(tmp_path)
    workspace = vault / "inside_workspace"

    proc = _run_cli(
        "--vault", str(vault),
        "--workspace", str(workspace),
        "--source-id", "x:100",
    )
    assert proc.returncode == 1
    result = json.loads(proc.stdout)
    assert result["status"] == "error"
    assert "Workspace must be outside the vault" in result["error"]


def test_cli_subprocess_ambiguity(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    rev1 = make_source("x:100", text="Rev 1", content_hash="1" * 64)
    rev2 = make_source("x:100", text="Rev 2", content_hash="2" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, rev1)
        insert_source(store, rev2)

    proc = _run_cli(
        "--vault", str(vault),
        "--workspace", str(workspace),
        "--source-id", "x:100",
    )
    assert proc.returncode == 1
    result = json.loads(proc.stdout)
    assert result["status"] == "error"
    assert "multiple revisions" in result["error"]


def test_cli_subprocess_cache_hit_offline(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    # Pre-populate StageCache using evaluate_live_source with fake transport
    evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=FakeTransport(),
    )

    before_vault = _hash_tree(vault)

    # Subprocess runs offline with NO api key set: cache hit!
    env = {"TYPESAFE_API_KEY": ""}
    proc = _run_cli(
        "--vault", str(vault),
        "--workspace", str(workspace),
        "--source-id", "x:100",
        env=env,
    )
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["status"] == "completed"
    assert result["cached"] is True
    assert result["source_id"] == "x:100"
    assert result["decision"] == "extract"
    assert _hash_tree(vault) == before_vault


def test_cli_subprocess_ambiguity_resolved_with_content_hash(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    rev1 = make_source("x:100", text="Rev 1", content_hash="1" * 64)
    rev2 = make_source("x:100", text="Rev 2", content_hash="2" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, rev1)
        insert_source(store, rev2)

    # Pre-populate cache for rev2
    evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        content_hash="2" * 64,
        api_key="test-key",
        transport=FakeTransport(),
    )

    env = {"TYPESAFE_API_KEY": ""}
    proc = _run_cli(
        "--vault", str(vault),
        "--workspace", str(workspace),
        "--source-id", "x:100",
        "--content-hash", "2" * 64,
        env=env,
    )
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    assert result["status"] == "completed"
    assert result["cached"] is True
    assert result["source_hash"] == "2" * 64
