from datetime import datetime, timezone

import pytest

from kb_pipeline.schemas import RunManifest, StageRecord, StageStatus
from kb_pipeline.stage_cache import StageCache
from kb_pipeline.storage import SourceStore


def test_keys_track_assessment_inputs(tmp_path):
    workspace = tmp_path / "workspace"
    base = ("filter", "input-a", "context-a", "jev", "question-v1")
    with StageCache(workspace) as cache:
        key = cache.key(*base)
        assert key == StageCache.key(*base, schema_version=1)
        assert cache.get(key) is None
        artifact = {"decision": "reject", "probabilities": {"engineering": 0.24},
                    "evidence": ["przykład", {"reason": None}], "schema_version": 1}
        cache.put(key, artifact)
        assert cache.get(key) == artifact
        for changed in [("extract", *base[1:]), (base[0], "input-b", *base[2:]),
                        (*base[:2], "context-b", *base[3:]), (*base[:3], "other-model", base[4]),
                        (*base[:4], "question-v2")]:
            assert cache.get(cache.key(*changed)) is None
        assert cache.get(cache.key(*base, schema_version=2)) is None

    with StageCache(workspace) as cache:
        assert cache.get(key) == artifact
        cache.put(key, {"decision": "defer", "reason": "missing context"})
        assert cache.get(key) == {"decision": "defer", "reason": "missing context"}


def test_artifacts_exclude_sensitive_fields(tmp_path):
    with StageCache(tmp_path) as cache:
        for value in ({"provider": {"headers": {"Authorization": "Bearer private"}}},
                      {"results": [{"api_key": "private"}]},
                      {"access_token": "private"}):
            with pytest.raises(ValueError, match="sensitive fields"):
                cache.put("key", value)
            assert cache.get("key") is None


@pytest.mark.parametrize("status", [StageStatus.rejected, StageStatus.deferred, StageStatus.error])
def test_manifest_status_survives_restart(tmp_path, status):
    workspace = tmp_path / "workspace"
    manifest = RunManifest(
        run_id=f"run-{status.value}", created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        code_version="v1", policy_version="threshold-0.5",
        prompt_versions={"filter": "question-v1"}, model_versions={"filter": "jev"},
        input_hashes={"x:123": "abc"},
        stages={"filter": StageRecord(status=status, artifact_refs=["cache:filter:abc"],
                                      error="provider timeout" if status is StageStatus.error else None,
                                      attempts=2)},
    )
    with StageCache(workspace) as cache:
        assert cache.load_manifest(manifest.run_id) is None
        cache.persist_manifest(manifest)
    with StageCache(workspace) as cache:
        restored = cache.load_manifest(manifest.run_id)
        assert restored == manifest
        assert restored.stages["filter"].status is status
        assert cache.load_manifest("other-run") is None


def test_policy_updates_reuse_artifact_without_changing_source_state(tmp_path):
    workspace = tmp_path / "workspace"
    with SourceStore(workspace) as store:
        store.connection.execute("INSERT INTO source_revisions VALUES (?, ?, ?, ?)",
                                 ("x:123", "hash-a", "record", "raw"))
        store.connection.commit()

    key = StageCache.key("filter", "hash-a", "context-a", "jev", "question-v1")
    with StageCache(workspace) as cache:
        cache.put(key, {"probabilities": {"engineering": 0.7}})
        original = RunManifest(run_id="run-1", created_at=datetime.now(timezone.utc),
                               code_version="v1", policy_version="threshold-0.5")
        cache.persist_manifest(original)
        updated = original.model_copy(update={"policy_version": "threshold-0.8"})
        cache.persist_manifest(updated)
        assert cache.load_manifest("run-1") == updated
        assert cache.get(key) == {"probabilities": {"engineering": 0.7}}

    with SourceStore(workspace) as store:
        assert store.connection.execute("SELECT source_id, content_hash, record_json, raw_json "
                                        "FROM source_revisions").fetchall() == [
                                            ("x:123", "hash-a", "record", "raw")]
    assert (workspace / "stage_cache.sqlite3").is_file()
    assert (workspace / "sources.sqlite3").is_file()
