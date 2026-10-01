from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from kb_pipeline.pilot import run_pilot
from kb_pipeline.schemas import RunManifest, StageStatus
from kb_pipeline.stage_cache import StageCache


def _source(
    source_id: str,
    text: str,
    *,
    reply_to_id: str | None = None,
    url: str | None = None,
) -> dict:
    return {
        "source_id": source_id,
        "author": "pilot-test",
        "url": url or f"https://x.com/pilot-test/status/{source_id[2:]}",
        "text": text,
        "published_at": None,
        "fetched_at": datetime(2026, 9, 23, tzinfo=timezone.utc).isoformat(),
        "language": "en",
        "reply_to_id": reply_to_id,
        "conversation_id": None,
        "quoted_source_id": None,
        "raw_ref": f"fixture:{source_id}",
        "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "context_status": "unavailable",
    }


def _claim(
    claim_id: str,
    source_id: str,
    quote: str,
    *,
    text: str = "Keep a concise checkpoint for the next turn.",
) -> dict:
    return {
        "claim_id": claim_id,
        "source_ids": [source_id],
        "text": text,
        "kind": "recommendation",
        "evidence": [{"source_id": source_id, "quote": quote}],
        "scope": "Long-running assistant conversations",
        "conditions": ["Preserve decisions and active constraints"],
        "limitations": ["The summary can omit details"],
    }


def _write_fixture(path: Path, value: dict) -> Path:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    return path


def _hash_tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    notes = vault / "Pojęcia"
    notes.mkdir(parents=True)
    (notes / "Manual note.md").write_text(
        "# Memory compaction\n\nMemory compaction keeps active context available.\n",
        encoding="utf-8",
    )
    obsidian = vault / ".obsidian"
    obsidian.mkdir()
    (obsidian / "workspace.json").write_text('{"layout": "manual"}\n', encoding="utf-8")
    return vault


def test_context_and_candidates_are_recorded(tmp_path):
    vault = _vault(tmp_path)
    workspace = tmp_path / "workspace"
    parent_text = "A checkpoint preserves active context during memory compaction."
    focus_text = "Keep a concise checkpoint for the next turn."
    fixture = _write_fixture(
        tmp_path / "fixture.json",
        {
            "sources": [
                _source("x:100", parent_text),
                _source("x:101", focus_text, reply_to_id="x:100"),
            ],
            "claims": [_claim("claim-1", "x:101", focus_text)],
            "mock_semantic_relations": {"claim-1": "supports"},
            "query": "memory compaction",
        },
    )
    vault_before = _hash_tree(vault)

    result = run_pilot(vault, workspace, fixture)

    assert result["status"] == "completed"
    assert result["proposed_claim_ids"] == ["claim-1"]
    run_dir = Path(result["run_dir"])
    context = json.loads((run_dir / "artifacts" / "context_bundles.json").read_text(encoding="utf-8"))
    assert context[1]["related"][0]["source"]["source_id"] == "x:100"
    assert context[1]["related"][0]["source"]["text"] == parent_text
    assert context[1]["context_status"] == "complete"
    summary = json.loads(
        (run_dir / "artifacts" / "validated_input_summary.json").read_text(encoding="utf-8")
    )
    assert "raw_ref" not in json.dumps(summary)
    assert focus_text not in json.dumps(summary)

    proposal = (run_dir / "proposal.md").read_bytes()
    proposal_text = proposal.decode("utf-8")
    assert "OFFLINE MOCK — DO NOT PUBLISH" in proposal_text
    assert focus_text in proposal_text
    assert "source_id: `x:101`" in proposal_text
    assert "https://x.com/pilot-test/status/101" in proposal_text
    assert "Long-running assistant conversations" in proposal_text
    assert "Preserve decisions and active constraints" in proposal_text
    assert "Candidate note paths (suggestions only)" in proposal_text
    assert "Pojęcia/Manual note.md" in proposal_text

    verification = json.loads(
        (run_dir / "artifacts" / "verification_results.json").read_text(encoding="utf-8")
    )[0]
    assert verification["status"] == "completed"
    assert verification["assessment_mode"] == "fixture_mock"
    assert verification["fake"] is True
    assert verification["result"]["independently_validated"] is False

    with StageCache(run_dir) as cache:
        manifest = cache.load_manifest(result["run_id"])
    assert isinstance(manifest, RunManifest)
    assert manifest.stages["fixture_validation"].status is StageStatus.completed
    assert manifest.stages["semantic_assessment"].status is StageStatus.deferred
    assert manifest.stages["publication"].status is StageStatus.deferred

    repeated = run_pilot(vault, workspace, fixture)
    assert repeated["run_id"] == result["run_id"]
    assert (Path(repeated["run_dir"]) / "proposal.md").read_bytes() == proposal
    assert [path.name for path in workspace.iterdir() if path.is_dir()] == [result["run_id"]]
    assert _hash_tree(vault) == vault_before


def test_quote_evidence_needs_semantic_assessment(tmp_path):
    vault = _vault(tmp_path)
    fixture = _write_fixture(
        tmp_path / "fixture.json",
        {
            "sources": [
                _source(
                    "x:200",
                    "A verified quote without a semantic verdict.",
                    reply_to_id="x:201",
                )
            ],
            "claims": [_claim("claim-no-verdict", "x:200", "A verified quote")],
            "query": "memory compaction",
        },
    )

    result = run_pilot(vault, tmp_path / "workspace", fixture)

    assert result["proposed_claim_ids"] == []
    assert result["deferred_claim_ids"] == ["claim-no-verdict"]
    assert result["proposal_path"] is None
    verification = json.loads(
        (Path(result["run_dir"]) / "artifacts" / "verification_results.json").read_text(encoding="utf-8")
    )[0]
    assert verification["result"]["quote_matches"] is True
    assert verification["result"]["relation"] == "uncertain"
    assert verification["assessment_mode"] == "bypassed"
    assert verification["fake"] is False
    assert verification["status"] == "deferred"
    context = json.loads(
        (Path(result["run_dir"]) / "artifacts" / "context_bundles.json").read_text(encoding="utf-8")
    )[0]
    assert context["context_status"] == "unavailable"
    assert context["missing_ids"] == ["x:201"]


def test_relation_without_matching_evidence_does_not_qualify(tmp_path):
    vault = _vault(tmp_path)
    fixture = _write_fixture(
        tmp_path / "fixture.json",
        {
            "sources": [_source("x:300", "The original source has different wording.")],
            "claims": [_claim("claim-bad-quote", "x:300", "quote from another source")],
            "mock_semantic_relations": {"claim-bad-quote": "supports"},
            "query": "memory compaction",
        },
    )

    result = run_pilot(vault, tmp_path / "workspace", fixture)

    assert result["proposed_claim_ids"] == []
    assert result["deferred_claim_ids"] == ["claim-bad-quote"]
    assert result["proposal_path"] is None
    verification = json.loads(
        (Path(result["run_dir"]) / "artifacts" / "verification_results.json").read_text(encoding="utf-8")
    )[0]
    assert verification["result"]["quote_matches"] is False
    assert verification["result"]["source_supported"] is False


def test_source_references_must_resolve(tmp_path):
    vault = _vault(tmp_path)
    fixture = _write_fixture(
        tmp_path / "fixture.json",
        {
            "sources": [_source("x:400", "A source with no matching claim evidence.")],
            "claims": [_claim("claim-missing", "x:401", "No quote")],
            "query": "memory compaction",
        },
    )

    with pytest.raises(ValueError, match="references missing sources"):
        run_pilot(vault, tmp_path / "workspace", fixture)


def test_duplicate_record_ids_are_refused(tmp_path):
    vault = _vault(tmp_path)
    source = _source("x:500", "Repeated source id.")
    fixture = _write_fixture(
        tmp_path / "fixture.json",
        {
            "sources": [source, source],
            "claims": [],
            "query": "memory compaction",
        },
    )

    with pytest.raises(ValueError, match="duplicate source IDs"):
        run_pilot(vault, tmp_path / "workspace", fixture)


def test_workspace_alias_is_refused(tmp_path):
    vault = _vault(tmp_path)
    fixture = _write_fixture(
        tmp_path / "fixture.json",
        {"sources": [], "claims": [], "query": "memory compaction"},
    )
    workspace_link = tmp_path / "workspace-link"
    try:
        workspace_link.symlink_to(vault, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are unavailable")

    with pytest.raises(ValueError, match="outside the vault"):
        run_pilot(vault, workspace_link, fixture)


def test_workspace_inside_vault_is_refused(tmp_path):
    vault = _vault(tmp_path)
    fixture = _write_fixture(
        tmp_path / "fixture.json",
        {"sources": [], "claims": [], "query": "memory compaction"},
    )

    with pytest.raises(ValueError, match="outside the vault"):
        run_pilot(vault, vault / "staging", fixture)
