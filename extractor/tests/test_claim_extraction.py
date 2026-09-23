from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from kb_pipeline.claim_extraction import (
    _classify_candidate,
    _segment_text_candidates,
    _verify_exact_quote_and_offsets,
    extract_claim_proposals,
    extract_live_claims,
)
from kb_pipeline.context import build_context
from kb_pipeline.live_jev import (
    compute_context_hash,
    compute_input_hash,
    compute_policy_version_key,
)
from kb_pipeline.schemas import (
    Claim,
    ClaimType,
    ContextBundle,
    ContextStatus,
    Evidence,
    SourceRecord,
)
from kb_pipeline.stage_cache import StageCache
from kb_pipeline.storage import SourceStore

EXTRACTOR_DIR = Path(__file__).resolve().parents[1]
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
    (vault / "Pojęcia" / "Architektura.md").write_text(
        "# Architektura\nNiezmienna treść bazy wiedzy.\n", encoding="utf-8"
    )
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


def seed_filter_assessment(
    workspace: Path,
    record: SourceRecord,
    bundle: ContextBundle,
    *,
    decision: str = "extract",
    bypass: bool = False,
    model: str = "jev-latest",
    question_version: str = "v1",
    policy_version: str = "v1",
    usefulness_threshold: float = 0.7,
    context_threshold: float = 0.6,
    reason_code: str = "sufficient_value_and_context",
    engineering_score: float = 0.92,
) -> str:
    source_hash = record.content_hash
    context_hash = compute_context_hash(bundle)
    input_hash = compute_input_hash(record.source_id, source_hash)
    policy_key = compute_policy_version_key(
        question_version, policy_version, usefulness_threshold, context_threshold
    )
    cache_key = StageCache.key("filter", input_hash, context_hash, model, policy_key, schema_version=1)

    artifact_data = {
        "source_id": record.source_id,
        "source_hash": source_hash,
        "context_hash": context_hash,
        "model": model,
        "question_version": question_version,
        "policy_version": policy_version,
        "usefulness_threshold": usefulness_threshold,
        "context_threshold": context_threshold,
        "answers": {
            "engineering_value": {"noul": engineering_score, "type": "noul"},
            "context_sufficient": {"noul": 0.85, "type": "noul"},
            "topic": {"choice": "compaction", "confidence": 1.0, "type": "choice"},
        },
        "assessment": {
            "source_id": record.source_id,
            "decision": decision,
            "reason_code": reason_code,
            "engineering_score": engineering_score,
            "topic": "compaction",
            "probabilities": {"engineering_value": engineering_score, "context_sufficient": 0.85},
            "model": model,
            "question_version": question_version,
            "policy_version": policy_version,
            "raw_response_ref": "artifacts/filter_test.json",
            "bypass": bypass,
            "schema_version": 1,
        },
        "usage": {"input_tokens": 100, "output_tokens": 20},
        "raw_response_ref": "artifacts/filter_test.json",
    }

    with StageCache(workspace) as cache:
        cache.put(cache_key, artifact_data)

    return cache_key


def test_extract_accepted_filter_success(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    vault_before = _hash_tree(vault)

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:100", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    result = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        content_hash=focus.content_hash,
    )

    assert result["status"] == "completed"
    assert result["cached"] is False
    assert result["claim_count"] == 1
    assert result["source_id"] == "x:100"
    assert result["content_hash"] == focus.content_hash
    assert result["verified"] is False
    assert result["published"] is False

    # Check proposal files exist outside vault
    json_path = workspace / result["proposal_json_ref"]
    md_path = workspace / result["proposal_md_ref"]
    assert json_path.is_file()
    assert md_path.is_file()
    assert not json_path.resolve().is_relative_to(vault.resolve())
    assert not md_path.resolve().is_relative_to(vault.resolve())

    # Verify machine-readable proposal structure
    machine_proposal = json.loads(json_path.read_text(encoding="utf-8"))
    assert machine_proposal["schema_version"] == 1
    assert machine_proposal["source_id"] == "x:100"
    assert machine_proposal["content_hash"] == focus.content_hash
    assert machine_proposal["verified"] is False
    assert machine_proposal["published"] is False
    assert machine_proposal["staging"] is True
    assert machine_proposal["claim_count"] == 1

    claim_data = machine_proposal["claims"][0]
    assert claim_data["text"] == text
    assert claim_data["kind"] == "recommendation"
    assert len(claim_data["evidence"]) == 1
    ev = claim_data["evidence"][0]
    assert ev["source_id"] == "x:100"
    assert ev["content_hash"] == focus.content_hash
    assert ev["quote"] == text
    assert ev["start"] == 0
    assert ev["end"] == len(text)
    assert text[ev["start"] : ev["end"]] == ev["quote"]

    # Verify human-readable markdown staging proposal
    md_content = md_path.read_text(encoding="utf-8")
    assert "UNVERIFIED / UNPUBLISHED — STAGING ONLY" in md_content
    assert "Source ID: `x:100`" in md_content
    assert focus.content_hash in md_content
    assert text in md_content
    assert f"[{ev['start']}:{ev['end']}]" in md_content

    # Assert vault immutability
    vault_after = _hash_tree(vault)
    assert vault_before == vault_after


def test_extract_rejected_filter_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(
        workspace, focus, bundle, decision="reject", reason_code="low_engineering_value"
    )

    with pytest.raises(ValueError, match="is 'reject' \\(expected 'extract'\\)"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
        )


def test_extract_deferred_filter_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(
        workspace, focus, bundle, decision="defer", reason_code="borderline_engineering_value"
    )

    with pytest.raises(ValueError, match="is 'defer' \\(expected 'extract'\\)"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
        )


def test_extract_bypass_filter_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract", bypass=True)

    with pytest.raises(ValueError, match="bypass=True"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
        )


def test_missing_filter_cache_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, focus)

    with pytest.raises(ValueError, match="No matching Jev filter assessment found"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
        )


def test_mismatching_source_revision_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100", content_hash="a" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, focus)

    # Providing a different hash not present in the store fails
    with pytest.raises(ValueError, match="not found in store"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash="b" * 64,
        )


def test_stale_context_hash_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    focus = make_source("x:100", reply_to_id="x:101")
    parent_v1 = make_source("x:101", text="Parent context version 1", content_hash="a" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        insert_source(store, parent_v1)
        bundle_v1 = build_context(focus, store.get_deterministic)

    # Seed filter assessment with parent v1 context
    seed_filter_assessment(workspace, focus, bundle_v1, decision="extract")

    # Now update parent in store to v2
    with SourceStore(workspace) as store:
        store.connection.execute("DELETE FROM source_revisions WHERE source_id='x:101'")
        parent_v2 = make_source("x:101", text="Parent context version 2", content_hash="b" * 64)
        insert_source(store, parent_v2)

    # Extraction must fail closed because current context hash does not match seeded filter cache
    with pytest.raises(ValueError, match="No matching Jev filter assessment found"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
        )


def test_ambiguous_related_context_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    focus = make_source("x:100", reply_to_id="x:101")
    parent_rev1 = make_source("x:101", text="Parent rev 1", content_hash="1" * 64)
    parent_rev2 = make_source("x:101", text="Parent rev 2", content_hash="2" * 64)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        insert_source(store, parent_rev1)
        insert_source(store, parent_rev2)

    with pytest.raises(ValueError, match="Multiple revisions found for source 'x:101'"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
        )


def test_context_gaps_preserved_in_proposals(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    # Focus replies to missing parent x:999
    text = "Always pin dependency versions in container builds to avoid drift."
    focus = make_source("x:100", text=text, reply_to_id="x:999")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    assert bundle.context_status == ContextStatus.partial or bundle.context_status == ContextStatus.unavailable
    assert "x:999" in bundle.missing_ids

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    result = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        content_hash=focus.content_hash,
    )

    assert result["status"] == "completed"
    assert result["missing_ids"] == ["x:999"]
    assert result["context_status"] in ("partial", "unavailable")

    machine_proposal = json.loads((workspace / result["proposal_json_ref"]).read_text(encoding="utf-8"))
    assert machine_proposal["missing_ids"] == ["x:999"]
    assert machine_proposal["context_status"] in ("partial", "unavailable")

    claim_item = machine_proposal["claims"][0]
    limitations_text = " ".join(claim_item["limitations"])
    assert "x:999" in limitations_text


def test_exact_substring_and_offset_verification_rules():
    source_text = "Always validate all tool arguments against strict Pydantic models."
    chash = hashlib.sha256(source_text.encode("utf-8")).hexdigest()

    # Valid claim
    valid_claim = Claim(
        claim_id="claim_valid_0",
        source_ids=["x:100"],
        text=source_text,
        kind=ClaimType.recommendation,
        evidence=[
            Evidence(
                source_id="x:100",
                content_hash=chash,
                quote=source_text,
                start=0,
                end=len(source_text),
            )
        ],
    )
    _verify_exact_quote_and_offsets("x:100", source_text, chash, valid_claim)

    # Source ID mismatch on evidence
    source_id_mismatch_claim = Claim(
        claim_id="claim_source_id_mismatch",
        source_ids=["x:999"],
        text=source_text,
        kind=ClaimType.recommendation,
        evidence=[
            Evidence(
                source_id="x:999",
                content_hash=chash,
                quote=source_text,
                start=0,
                end=len(source_text),
            )
        ],
    )
    with pytest.raises(ValueError, match="Evidence source_id 'x:999' does not match pinned source 'x:100'"):
        _verify_exact_quote_and_offsets("x:100", source_text, chash, source_id_mismatch_claim)

    # Offset out of range
    bad_offsets_claim = Claim(
        claim_id="claim_bad_offsets",
        source_ids=["x:100"],
        text="Always",
        kind=ClaimType.recommendation,
        evidence=[
            Evidence(
                source_id="x:100",
                content_hash=chash,
                quote="Always",
                start=0,
                end=len(source_text) + 10,
            )
        ],
    )
    with pytest.raises(ValueError, match="out of range"):
        _verify_exact_quote_and_offsets("x:100", source_text, chash, bad_offsets_claim)

    # Slice mismatch (normalized or modified quote)
    slice_mismatch_claim = Claim(
        claim_id="claim_slice_mismatch",
        source_ids=["x:100"],
        text="Always validate",
        kind=ClaimType.recommendation,
        evidence=[
            Evidence(
                source_id="x:100",
                content_hash=chash,
                quote="Always  validate",  # extra space, not exact slice
                start=0,
                end=15,
            )
        ],
    )
    with pytest.raises(ValueError, match="Exact quote mismatch"):
        _verify_exact_quote_and_offsets("x:100", source_text, chash, slice_mismatch_claim)

    # Content hash mismatch on evidence
    hash_mismatch_claim = Claim(
        claim_id="claim_hash_mismatch",
        source_ids=["x:100"],
        text=source_text,
        kind=ClaimType.recommendation,
        evidence=[
            Evidence(
                source_id="x:100",
                content_hash="f" * 64,
                quote=source_text,
                start=0,
                end=len(source_text),
            )
        ],
    )
    with pytest.raises(ValueError, match="does not match pinned revision"):
        _verify_exact_quote_and_offsets("x:100", source_text, chash, hash_mismatch_claim)


def test_no_reliable_claims_emits_empty_proposals(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    # Non-actionable text
    banter_text = "Thanks for the great conversation @alice! Have a nice weekend."
    focus = make_source("x:200", text=banter_text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    result = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:200",
        content_hash=focus.content_hash,
    )

    assert result["status"] == "completed"
    assert result["claim_count"] == 0
    assert result["claims"] == []

    json_path = workspace / result["proposal_json_ref"]
    md_path = workspace / result["proposal_md_ref"]
    assert json_path.is_file()
    assert md_path.is_file()

    machine_proposal = json.loads(json_path.read_text(encoding="utf-8"))
    assert machine_proposal["claim_count"] == 0
    assert machine_proposal["claims"] == []

    md_content = md_path.read_text(encoding="utf-8")
    assert "No reliable actionable claims extracted from this source revision." in md_content


def test_replay_idempotency(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Ensure all agent tool inputs are validated before execution."
    focus = make_source("x:100", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    # First run: writes proposal and caches
    res1 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        content_hash=focus.content_hash,
    )
    assert res1["cached"] is False
    assert res1["claim_count"] == 1

    json_bytes1 = (workspace / res1["proposal_json_ref"]).read_bytes()
    md_bytes1 = (workspace / res1["proposal_md_ref"]).read_bytes()

    # Second run: replays from cache
    res2 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        content_hash=focus.content_hash,
    )
    assert res2["cached"] is True
    assert res2["claim_count"] == 1
    assert res2["proposal_json_ref"] == res1["proposal_json_ref"]
    assert res2["proposal_md_ref"] == res1["proposal_md_ref"]

    # Proposals on disk are identical
    json_bytes2 = (workspace / res2["proposal_json_ref"]).read_bytes()
    md_bytes2 = (workspace / res2["proposal_md_ref"]).read_bytes()
    assert json_bytes1 == json_bytes2
    assert md_bytes1 == md_bytes2


def test_multiple_distinct_claims_in_single_source(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    multiline_text = (
        "Tips for robust agent harnesses:\n"
        "- Prune stale tool output before it consumes the context budget.\n"
        "- Never write unverified assertions to persistent storage.\n"
        "- Long conversations suffer from context drift in multi-turn dialogues."
    )
    focus = make_source("x:300", text=multiline_text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    result = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:300",
        content_hash=focus.content_hash,
    )

    assert result["status"] == "completed"
    assert result["claim_count"] == 3

    kinds = [c["kind"] for c in result["claims"]]
    assert kinds[0] == "recommendation"
    assert kinds[1] == "recommendation"
    assert kinds[2] == "observation"

    # Verify each claim is an exact substring of the original text
    for claim in result["claims"]:
        ev = claim["evidence"][0]
        assert ev["content_hash"] == focus.content_hash
        assert multiline_text[ev["start"] : ev["end"]] == ev["quote"]


def test_safe_paths_guard_workspace_and_symlinks(tmp_path):
    vault = make_vault(tmp_path)
    inside_vault_workspace = vault / "nested_workspace"

    with pytest.raises(ValueError, match="Workspace must be outside the vault"):
        extract_live_claims(
            vault=vault,
            workspace=inside_vault_workspace,
            source_id="x:100",
            content_hash="a" * 64,
        )


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


def test_proposals_symlink_inside_vault_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    proposals_link = workspace / "proposals"
    workspace.mkdir(parents=True, exist_ok=True)
    _make_symlink_or_junction(proposals_link, vault / "Pojęcia")

    before_vault = _hash_tree(vault)
    with pytest.raises(ValueError, match="inside the vault"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
        )

    after_vault = _hash_tree(vault)
    assert before_vault == after_vault


def test_policy_identity_mismatch_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract", policy_version="v2")

    # Invocation with default policy_version="v1" must fail closed
    with pytest.raises(ValueError, match="No matching Jev filter assessment found"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
            policy_version="v1",
        )


def test_model_identity_mismatch_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    focus = make_source("x:100")

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    # Seed assessment with model 'custom-jev-v2'
    seed_filter_assessment(workspace, focus, bundle, decision="extract", model="custom-jev-v2")

    # Query with default model 'jev-latest' -> fails closed
    with pytest.raises(ValueError, match="No matching Jev filter assessment found"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:100",
            content_hash=focus.content_hash,
            model="jev-latest",
        )

    # Query with matching model 'custom-jev-v2' -> succeeds
    res = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:100",
        content_hash=focus.content_hash,
        model="custom-jev-v2",
    )
    assert res["status"] == "completed"


def test_cli_claim_extract_success(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Always validate all tool arguments against strict Pydantic models."
    focus = make_source("x:500", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "kb_pipeline",
            "claim-extract",
            "--vault",
            str(vault),
            "--workspace",
            str(workspace),
            "--source-id",
            "x:500",
            "--content-hash",
            focus.content_hash,
        ],
        cwd=EXTRACTOR_DIR,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0
    output = json.loads(proc.stdout)
    assert output["status"] == "completed"
    assert output["source_id"] == "x:500"
    assert output["claim_count"] >= 1
    assert output["cached"] is False


def test_cli_claim_extract_failure_exits_code_one(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "kb_pipeline",
            "claim-extract",
            "--vault",
            str(vault),
            "--workspace",
            str(workspace),
            "--source-id",
            "x:999",
            "--content-hash",
            "0" * 64,
        ],
        cwd=EXTRACTOR_DIR,
        capture_output=True,
        text=True,
    )

    assert proc.returncode != 0
    output = json.loads(proc.stdout)
    assert output["status"] == "error"
    assert "not found in store" in output["error"]


def test_tampered_cached_quote_rejected_on_replay(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:601", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    res = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:601",
        content_hash=focus.content_hash,
    )
    assert res["status"] == "completed"

    # Tamper with the cached payload in StageCache (alter quote text)
    with StageCache(workspace) as cache:
        rows = cache.connection.execute(
            "SELECT key, value_json FROM artifacts"
        ).fetchall()
        for k, v in rows:
            data = json.loads(v)
            if data.get("claims"):
                data["claims"][0]["evidence"][0]["quote"] = "Tampered quote not in source text."
                cache.connection.execute(
                    "UPDATE artifacts SET value_json=? WHERE key=?",
                    (json.dumps(data), k),
                )
        cache.connection.commit()

    with pytest.raises(ValueError, match="(Exact quote mismatch|Quote '.*' is not an exact substring)"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:601",
            content_hash=focus.content_hash,
        )


def test_tampered_proposal_json_artifact_rejected_on_replay(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:602", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    res = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:602",
        content_hash=focus.content_hash,
    )
    assert res["status"] == "completed"

    # Tamper with the JSON artifact on disk
    json_path = workspace / res["proposal_json_ref"]
    data = json.loads(json_path.read_text(encoding="utf-8"))
    data["claims"][0]["evidence"][0]["quote"] = "Tampered on disk quote."
    json_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="(Divergent claims payload|Exact quote mismatch|Quote '.*' is not an exact substring)"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:602",
            content_hash=focus.content_hash,
        )


def test_missing_proposal_json_artifact_rejected_on_replay(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:603", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    res = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:603",
        content_hash=focus.content_hash,
    )
    assert res["status"] == "completed"

    # Delete JSON artifact
    json_path = workspace / res["proposal_json_ref"]
    json_path.unlink()

    with pytest.raises(ValueError, match="Cached proposal JSON artifact missing"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:603",
            content_hash=focus.content_hash,
        )


def test_missing_proposal_md_artifact_rejected_on_replay(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:604", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    res = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:604",
        content_hash=focus.content_hash,
    )
    assert res["status"] == "completed"

    # Delete Markdown artifact
    md_path = workspace / res["proposal_md_ref"]
    md_path.unlink()

    with pytest.raises(ValueError, match="Cached proposal Markdown artifact missing"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:604",
            content_hash=focus.content_hash,
        )


def test_differing_model_and_policy_outputs_keyed_separately(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:605", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    # Seed 3 different evaluations: default, custom model, custom policy
    seed_filter_assessment(workspace, focus, bundle, decision="extract", model="jev-latest", policy_version="v1")
    seed_filter_assessment(workspace, focus, bundle, decision="extract", model="custom-model", policy_version="v1")
    seed_filter_assessment(workspace, focus, bundle, decision="extract", model="jev-latest", policy_version="v2")

    res1 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:605",
        content_hash=focus.content_hash,
        model="jev-latest",
        policy_version="v1",
    )
    res2 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:605",
        content_hash=focus.content_hash,
        model="custom-model",
        policy_version="v1",
    )
    res3 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:605",
        content_hash=focus.content_hash,
        model="jev-latest",
        policy_version="v2",
    )

    # Distinct artifact references
    refs = {res1["proposal_json_ref"], res2["proposal_json_ref"], res3["proposal_json_ref"]}
    assert len(refs) == 3

    md_refs = {res1["proposal_md_ref"], res2["proposal_md_ref"], res3["proposal_md_ref"]}
    assert len(md_refs) == 3

    # All artifacts exist simultaneously on disk without overwriting each other
    for r in refs:
        assert (workspace / r).is_file()
    for mr in md_refs:
        assert (workspace / mr).is_file()

    # Verify content of each proposal corresponds to its specific evaluation
    p1 = json.loads((workspace / res1["proposal_json_ref"]).read_text(encoding="utf-8"))
    p2 = json.loads((workspace / res2["proposal_json_ref"]).read_text(encoding="utf-8"))
    p3 = json.loads((workspace / res3["proposal_json_ref"]).read_text(encoding="utf-8"))

    assert p1["model"] == "jev-latest" and p1["policy_version"] == "v1"
    assert p2["model"] == "custom-model" and p2["policy_version"] == "v1"
    assert p3["model"] == "jev-latest" and p3["policy_version"] == "v2"

    # Capture mtimes of res1 files
    res1_json_stat_before = (workspace / res1["proposal_json_ref"]).stat()
    res1_md_stat_before = (workspace / res1["proposal_md_ref"]).stat()

    # Replay res1
    replay1 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:605",
        content_hash=focus.content_hash,
        model="jev-latest",
        policy_version="v1",
    )
    assert replay1["cached"] is True
    assert replay1["proposal_json_ref"] == res1["proposal_json_ref"]

    # Ensure files were not overwritten on rerun
    res1_json_stat_after = (workspace / res1["proposal_json_ref"]).stat()
    res1_md_stat_after = (workspace / res1["proposal_md_ref"]).stat()
    assert res1_json_stat_before.st_mtime_ns == res1_json_stat_after.st_mtime_ns
    assert res1_md_stat_before.st_mtime_ns == res1_md_stat_after.st_mtime_ns

    # Other evaluation proposals remain intact
    assert (workspace / res2["proposal_json_ref"]).is_file()
    assert (workspace / res3["proposal_json_ref"]).is_file()


def test_untrusted_cached_proposal_ref_rejected(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:701", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    res = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:701",
        content_hash=focus.content_hash,
    )
    assert res["status"] == "completed"

    # Tamper with proposal_json_ref to point to relative traversal path
    with StageCache(workspace) as cache:
        rows = cache.connection.execute("SELECT key, value_json FROM artifacts").fetchall()
        for k, v in rows:
            data = json.loads(v)
            if data.get("proposal_json_ref"):
                data["proposal_json_ref"] = "../../evil.json"
                cache.connection.execute(
                    "UPDATE artifacts SET value_json=? WHERE key=?",
                    (json.dumps(data), k),
                )
        cache.connection.commit()

    with pytest.raises(ValueError, match="Untrusted proposal JSON ref in cache"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:701",
            content_hash=focus.content_hash,
        )

    # Tamper with proposal_md_ref to point to absolute path
    with StageCache(workspace) as cache:
        rows = cache.connection.execute("SELECT key, value_json FROM artifacts").fetchall()
        for k, v in rows:
            data = json.loads(v)
            if data.get("proposal_md_ref"):
                data["proposal_json_ref"] = res["proposal_json_ref"]
                data["proposal_md_ref"] = "/etc/passwd"
                cache.connection.execute(
                    "UPDATE artifacts SET value_json=? WHERE key=?",
                    (json.dumps(data), k),
                )
        cache.connection.commit()

    with pytest.raises(ValueError, match="Untrusted proposal Markdown ref in cache"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:701",
            content_hash=focus.content_hash,
        )


def test_divergent_disk_proposal_contents_vs_cache_rejected(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:702", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    res = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:702",
        content_hash=focus.content_hash,
    )
    assert res["status"] == "completed"

    # Modify scope/kind in disk JSON artifact without changing count or quote
    json_path = workspace / res["proposal_json_ref"]
    data = json.loads(json_path.read_text(encoding="utf-8"))
    data["claims"][0]["scope"] = "Divergent scope altered on disk."
    json_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Divergent claims payload between disk proposal and cache"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:702",
            content_hash=focus.content_hash,
        )


def test_destination_proposal_json_exists_with_divergent_content_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:703", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    input_hash = compute_input_hash(focus.source_id, focus.content_hash)
    context_hash = compute_context_hash(bundle)
    policy_key = compute_policy_version_key("v1", "v1", 0.7, 0.6)
    extract_cache_key = StageCache.key(
        "claim_extract", input_hash, context_hash, "jev-latest", policy_key, schema_version=1
    )

    dest_dir = workspace / "proposals"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_json = dest_dir / f"claim_proposals_{extract_cache_key}.json"
    dest_json.write_text(json.dumps({"divergent": "pre-existing content"}), encoding="utf-8")

    with pytest.raises(ValueError, match="Destination proposal JSON '.*' already exists with divergent content"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:703",
            content_hash=focus.content_hash,
        )


def test_destination_proposal_md_exists_with_divergent_content_fails_closed(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:704", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    input_hash = compute_input_hash(focus.source_id, focus.content_hash)
    context_hash = compute_context_hash(bundle)
    policy_key = compute_policy_version_key("v1", "v1", 0.7, 0.6)
    extract_cache_key = StageCache.key(
        "claim_extract", input_hash, context_hash, "jev-latest", policy_key, schema_version=1
    )

    dest_dir = workspace / "proposals"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_md = dest_dir / f"claim_proposals_{extract_cache_key}.md"
    dest_md.write_text("# Divergent markdown already present", encoding="utf-8")

    with pytest.raises(ValueError, match="Destination proposal markdown '.*' already exists with divergent content"):
        extract_live_claims(
            vault=vault,
            workspace=workspace,
            source_id="x:704",
            content_hash=focus.content_hash,
        )


def test_destination_files_exist_with_identical_content_accepted(tmp_path):
    vault = make_vault(tmp_path)
    workspace = tmp_path / "workspace"

    text = "Prune stale tool output before it consumes the context budget."
    focus = make_source("x:705", text=text)

    with SourceStore(workspace) as store:
        insert_source(store, focus)
        bundle = build_context(focus, store.get_deterministic)

    seed_filter_assessment(workspace, focus, bundle, decision="extract")

    # Initial extraction
    res1 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:705",
        content_hash=focus.content_hash,
    )
    assert res1["status"] == "completed"

    # Clear claim_extract entries from StageCache to simulate cache missing while files exist
    with StageCache(workspace) as cache:
        cache.connection.execute("DELETE FROM artifacts WHERE key LIKE 'claim_extract%'")
        # StageCache keys are hashed, so let's delete all extraction cache keys:
        input_hash = compute_input_hash(focus.source_id, focus.content_hash)
        context_hash = compute_context_hash(bundle)
        policy_key = compute_policy_version_key("v1", "v1", 0.7, 0.6)
        extract_cache_key = StageCache.key(
            "claim_extract", input_hash, context_hash, "jev-latest", policy_key, schema_version=1
        )
        cache.connection.execute("DELETE FROM artifacts WHERE key=?", (extract_cache_key,))
        cache.connection.commit()

    # Re-running with existing identical files succeeds and repopulates cache
    res2 = extract_live_claims(
        vault=vault,
        workspace=workspace,
        source_id="x:705",
        content_hash=focus.content_hash,
    )
    assert res2["status"] == "completed"
    assert res2["cached"] is False
    assert res2["proposal_json_ref"] == res1["proposal_json_ref"]


