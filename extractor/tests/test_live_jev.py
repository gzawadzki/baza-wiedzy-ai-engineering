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
from kb_pipeline.live_jev import (
    compute_context_hash,
    compute_input_hash,
    compute_policy_version_key,
    evaluate_live_source,
)
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

    # Check StageCache. The raw assessment key carries stage, input, context,
    # model, question version and schema version - never a threshold.
    input_hash = compute_input_hash("x:100", source.content_hash)
    cache_key = StageCache.key("filter", input_hash, summary["context_hash"], "jev-latest", "v1", schema_version=1)
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


def test_cache_collision_different_sources_same_content(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    # Same content, different authors and source IDs
    shared_text = "Prune stale tool output before it consumes the context budget."
    s1 = make_source("x:100", author="alice", text=shared_text)
    s2 = make_source("x:200", author="bob", text=shared_text)
    assert s1.content_hash == s2.content_hash

    with SourceStore(workspace) as store:
        insert_source(store, s1)
        insert_source(store, s2)

    # First call for x:100 with extract response
    transport1 = FakeTransport(response=make_response(topic="compaction", engineering_value=0.95))
    summary1 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport1,
    )
    assert transport1.call_count == 1
    assert summary1["source_id"] == "x:100"
    assert summary1["decision"] == "extract"

    # Second call for x:200 must NOT reuse x:100's cached assessment
    transport2 = FakeTransport(response=make_response(topic="other", engineering_value=0.10))
    summary2 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:200",
        api_key="test-key",
        transport=transport2,
    )
    assert transport2.call_count == 1
    assert summary2["source_id"] == "x:200"
    assert summary2["decision"] == "reject"
    assert summary2["cached"] is False

    # Now verify both are independently cached
    replay1 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=FakeTransport(),
    )
    assert replay1["cached"] is True
    assert replay1["source_id"] == "x:100"
    assert replay1["decision"] == "extract"

    replay2 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:200",
        api_key="test-key",
        transport=FakeTransport(),
    )
    assert replay2["cached"] is True
    assert replay2["source_id"] == "x:200"
    assert replay2["decision"] == "reject"


def test_threshold_and_policy_change_recompute_without_a_new_call(tmp_path):
    """Plan §1.7: a bar change recomputes the decision, it does not re-ask the model.

    This is the behaviour the previous contract got wrong: thresholds and the
    policy version used to sit in the raw-assessment cache key, so moving a bar
    threw the answer away and paid for it again.
    """
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    # Response with engineering_value = 0.75
    transport = FakeTransport(response=make_response(engineering_value=0.75, context_sufficient=0.85))

    # Initial evaluation with default threshold 0.7 -> extract
    s1 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        policy_version="v1",
        usefulness_threshold=0.7,
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 1
    assert s1["decision"] == "extract"
    fingerprint_1 = compute_policy_version_key("v1", "v1", 0.7, 0.6)

    # Changed threshold to 0.85 -> 0.75 is below 0.85, decision should be defer
    # (borderline) - recomputed from the cached raw answer, no new call.
    s2 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        policy_version="v1",
        usefulness_threshold=0.85,
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 1
    assert s2["cached"] is True
    assert s2["decision"] == "defer"
    assert s2["decision_recomputed_from_cache"] is True
    assert s2["decision_fingerprint"] == compute_policy_version_key("v1", "v1", 0.85, 0.6)
    assert fingerprint_1 != s2["decision_fingerprint"]

    # Changed policy_version -> still a decision change, still no new call
    s3 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        policy_version="v2",
        usefulness_threshold=0.7,
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 1
    assert s3["cached"] is True
    assert s3["decision"] == "extract"
    assert s3["policy_version"] == "v2"
    assert s3["decision_fingerprint"] == compute_policy_version_key("v1", "v2", 0.7, 0.6)

    # Back to the original bars -> the original decision, still no new call
    s4 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        policy_version="v1",
        usefulness_threshold=0.7,
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 1
    assert s4["decision"] == "extract"
    assert s4["decision_fingerprint"] == fingerprint_1


def test_context_change_and_immutable_artifacts(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    focus = make_source("x:100", reply_to_id="x:101")
    parent_v1 = make_source("x:101", text="Parent context version 1", content_hash="a" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        insert_source(store, parent_v1)

    transport = FakeTransport()
    s1 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 1
    ref1 = s1["artifact_ref"]
    artifact_path1 = workspace / ref1
    assert artifact_path1.is_file()

    # Update parent to version 2 (simulating updated single revision in store)
    with SourceStore(workspace) as store:
        store.connection.execute("DELETE FROM source_revisions WHERE source_id='x:101'")
        parent_v2 = make_source("x:101", text="Parent context version 2", content_hash="b" * 64)
        insert_source(store, parent_v2)

    # Evaluate again: context_hash changes, so provider is invoked and distinct artifact is written
    s2 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
    )
    assert transport.call_count == 2
    ref2 = s2["artifact_ref"]
    artifact_path2 = workspace / ref2
    assert artifact_path2.is_file()

    assert ref1 != ref2
    assert artifact_path1.is_file()
    assert artifact_path2.is_file()


def test_refresh_preserves_immutable_artifact_refs(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    transport = FakeTransport()
    s1 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
    )
    ref1 = s1["artifact_ref"]
    path1 = workspace / ref1
    assert path1.is_file()

    # Refresh
    s2 = evaluate_live_source(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        api_key="test-key",
        transport=transport,
        refresh=True,
    )
    ref2 = s2["artifact_ref"]
    path2 = workspace / ref2
    assert path2.is_file()

    assert ref1 != ref2
    assert path1.is_file()
    assert path2.is_file()


def _make_symlink_or_junction(link_path: Path, target_path: Path) -> None:
    try:
        link_path.symlink_to(target_path, target_is_directory=True)
    except (OSError, NotImplementedError):
        if sys.platform == "win32" and target_path.is_dir():
            res = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link_path), str(target_path)],
                capture_output=True,
                check=False,
            )
            if res.returncode != 0:
                pytest.skip("Symlinks/junctions are unavailable in this environment")
        else:
            pytest.skip("Symlinks are unavailable in this environment")


def test_artifacts_symlink_inside_vault_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    artifacts_link = workspace / "artifacts"
    _make_symlink_or_junction(artifacts_link, vault / "Pojęcia")

    before_vault = _hash_tree(vault)
    with pytest.raises(ValueError, match="inside the vault"):
        evaluate_live_source(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            api_key="test-key",
            transport=FakeTransport(),
        )

    assert _hash_tree(vault) == before_vault


def test_validate_safe_artifact_target_mock_symlink(tmp_path, monkeypatch):
    """Directly test symlink traversal check even when OS symlink creation is restricted."""
    from kb_pipeline.live_jev import _validate_safe_artifact_target

    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    target_dir = workspace / "artifacts"

    # Simulate target_dir being a symlink whose resolved path is inside vault
    monkeypatch.setattr(Path, "is_symlink", lambda self: self == target_dir)
    monkeypatch.setattr(Path, "resolve", lambda self, strict=False: vault / "Pojęcia" if self == target_dir else self)

    with pytest.raises(ValueError, match="inside the vault"):
        _validate_safe_artifact_target(target_dir, vault)


def test_cli_subprocess_artifacts_symlink_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    source = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, source)

    artifacts_link = workspace / "artifacts"
    _make_symlink_or_junction(artifacts_link, vault / "Pojęcia")

    before_vault = _hash_tree(vault)
    proc = _run_cli(
        "--vault", str(vault),
        "--workspace", str(workspace),
        "--source-id", "x:100",
    )
    assert proc.returncode == 1
    result = json.loads(proc.stdout)
    assert result["status"] == "error"
    assert "inside the vault" in result["error"]
    assert _hash_tree(vault) == before_vault

