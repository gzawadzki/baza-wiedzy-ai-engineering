"""Tests for knowledge base claim integration and artifact generation."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml
from pydantic import ValidationError

from kb_pipeline.audit import _frontmatter
from kb_pipeline.integration import (
    IntegrationAdvice,
    NoteView,
    SectionCandidate,
    integrate_claims,
    write_integration_artifacts,
)
from kb_pipeline.schemas import (
    Claim,
    ClaimType,
    Evidence,
    IntegrationDecision,
    IntegrationOperation,
    VerificationRelation,
    VerificationResult,
)


def make_claim(
    claim_id: str = "x:100:0",
    text: str = "Retrieval improves grounding in language models",
    quote: str = "Retrieval improves grounding",
    source_id: str = "x:100",
    conditions: list[str] | None = None,
    limitations: list[str] | None = None,
) -> Claim:
    return Claim(
        claim_id=claim_id,
        source_ids=[source_id],
        text=text,
        kind=ClaimType.observation,
        evidence=[Evidence(source_id=source_id, quote=quote)],
        conditions=conditions or [],
        limitations=limitations or [],
    )


def make_verification(
    claim_id: str = "x:100:0",
    quote_matches: bool = True,
    relation: VerificationRelation = VerificationRelation.supports,
    source_supported: bool = True,
) -> VerificationResult:
    return VerificationResult(
        claim_id=claim_id,
        quote_matches=quote_matches,
        relation=relation,
        source_supported=source_supported,
        reason="Verification check passed",
    )


def make_note(
    note_id: str = "retrieval-grounding",
    relative_path: str = "Pojęcia/retrieval-grounding.md",
    content: str = "# Retrieval Grounding\n\nOverview of retrieval techniques.\n",
    content_hash: str = "a" * 64,
    managed: bool = True,
) -> NoteView:
    return NoteView(
        note_id=note_id,
        relative_path=relative_path,
        content=content,
        content_hash=content_hash,
        managed=managed,
    )


def make_candidate(
    note_id: str = "retrieval-grounding",
    relative_path: str = "Pojęcia/retrieval-grounding.md",
    heading: str = "Retrieval Grounding",
    anchor: str = "retrieval-grounding",
    snippet: str = "Overview of retrieval techniques.",
    score: float = 0.95,
) -> SectionCandidate:
    return SectionCandidate(
        note_id=note_id,
        relative_path=relative_path,
        heading=heading,
        anchor=anchor,
        snippet=snippet,
        score=score,
    )


def test_public_types_extra_fields_forbidden():
    with pytest.raises(ValidationError):
        NoteView(
            note_id="n1",
            relative_path="p",
            content="c",
            content_hash="a" * 64,
            managed=True,
            unexpected_field="bad",
        )

    with pytest.raises(ValidationError):
        SectionCandidate(
            note_id="n1",
            relative_path="p",
            heading="h",
            anchor="a",
            snippet="s",
            score=1.0,
            unexpected_field="bad",
        )

    with pytest.raises(ValidationError):
        IntegrationAdvice(
            operation=IntegrationOperation.create,
            rationale="rationale",
            unexpected_field="bad",
        )


def test_note_view_content_hash_pattern():
    with pytest.raises(ValidationError):
        NoteView(
            note_id="n1",
            relative_path="p",
            content="c",
            content_hash="invalid_hash",
            managed=True,
        )

    with pytest.raises(ValidationError):
        NoteView(
            note_id="n1",
            relative_path="p",
            content="c",
            content_hash="A" * 64,
            managed=True,
        )

    valid = NoteView(
        note_id="n1",
        relative_path="p",
        content="c",
        content_hash="f" * 64,
        managed=True,
    )
    assert valid.content_hash == "f" * 64


def test_missing_verification_defers_without_advisor():
    claim = make_claim(claim_id="c1")
    advisor = Mock()

    decisions = integrate_claims([claim], {}, {}, {}, advisor)

    advisor.assert_not_called()
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None
    assert decision.claim_ids == ["c1"]


def test_quote_match_failure_defers_without_advisor():
    claim = make_claim(claim_id="c1")
    verif = make_verification(claim_id="c1", quote_matches=False)
    advisor = Mock()

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    advisor.assert_not_called()
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None
    assert decision.claim_ids == ["c1"]


def test_unsupported_relation_defers_without_advisor():
    claim = make_claim(claim_id="c1")
    verif = make_verification(
        claim_id="c1",
        relation=VerificationRelation.uncertain,
    )
    advisor = Mock()

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    advisor.assert_not_called()
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None


def test_exact_quote_duplicate_defers_without_advisor():
    claim = make_claim(claim_id="c1", quote="Exact quote already present in vault")
    verif = make_verification(claim_id="c1", relation=VerificationRelation.supports)
    existing_note = make_note(
        note_id="existing-note",
        content="Header\n\nExact quote already present in vault\nFooter",
    )
    advisor = Mock()

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {existing_note.note_id: existing_note},
        advisor,
    )

    advisor.assert_not_called()
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.duplicate
    assert decision.patch is None
    assert decision.claim_ids == ["c1"]


def test_contradiction_with_conflicts_records_conflict():
    claim = make_claim(claim_id="c1")
    verif = make_verification(
        claim_id="c1",
        relation=VerificationRelation.contradicts,
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.defer,
        rationale="Conflict observed",
        conflicting_claim_ids=["prior:claim:1"],
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    advisor.assert_called_once()
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.record_conflict
    assert decision.patch is None
    assert decision.conflicting_claim_ids == ["prior:claim:1"]


def test_contradiction_without_conflicts_defers():
    claim = make_claim(claim_id="c1")
    verif = make_verification(
        claim_id="c1",
        relation=VerificationRelation.contradicts,
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        rationale="Contradiction without matching claims",
        conflicting_claim_ids=[],
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    advisor.assert_called_once()
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None
    assert decision.conflicting_claim_ids == []


def test_supports_with_unsupported_source_defers_without_advisor():
    claim = make_claim(claim_id="c1")
    verif = make_verification(
        claim_id="c1",
        relation=VerificationRelation.supports,
        source_supported=False,
    )
    advisor = Mock()

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    advisor.assert_not_called()
    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None


def test_enrich_managed_note_success():
    quote_text = "Verified evidence quote for enrichment"
    claim = make_claim(
        claim_id="claim-101",
        quote=quote_text,
        conditions=["Context window >= 8k"],
        limitations=["English only"],
    )
    verif = make_verification(claim_id="claim-101")
    note = make_note(
        note_id="target-note",
        relative_path="Pojęcia/target-note.md",
        content="# Initial Content\n",
        content_hash="1" * 64,
        managed=True,
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="target-note",
        relative_path="Pojęcia/target-note.md",
        rationale="Enriching existing concept",
        proposed_body=f"Summary of findings with quote: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {note.note_id: note},
        advisor,
    )

    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.enrich
    assert decision.patch is not None
    patch = decision.patch
    assert patch.note_id == "target-note"
    assert patch.relative_path == "Pojęcia/target-note.md"
    assert patch.claim_ids == ["claim-101"]
    assert patch.base_hash == "1" * 64
    assert patch.proposed_content.startswith("# Initial Content\n")
    assert "## Teza claim-101" in patch.proposed_content
    assert "claim-101" in patch.proposed_content
    assert quote_text in patch.proposed_content
    assert "Context window >= 8k" in patch.proposed_content
    assert "English only" in patch.proposed_content
    assert "source-supported and not independently validated" in patch.proposed_content


def test_add_evidence_managed_note_success():
    quote_text = "Secondary evidence supporting established theory"
    claim = make_claim(claim_id="claim-202", quote=quote_text)
    verif = make_verification(claim_id="claim-202")
    note = make_note(
        note_id="evidence-note",
        relative_path="Pojęcia/evidence-note.md",
        content="# Established Theory\n",
        content_hash="2" * 64,
        managed=True,
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.add_evidence,
        target_note_id="evidence-note",
        relative_path="Pojęcia/evidence-note.md",
        rationale="Adding new evidence",
        proposed_body=f"Additional confirmation: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {note.note_id: note},
        advisor,
    )

    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.add_evidence
    assert decision.patch is not None
    assert "## Dowód claim-202" in decision.patch.proposed_content
    assert quote_text in decision.patch.proposed_content
    assert decision.patch.base_hash == "2" * 64


def test_unmanaged_note_defers():
    quote_text = "Evidence targeting an unmanaged note"
    claim = make_claim(claim_id="claim-303", quote=quote_text)
    verif = make_verification(claim_id="claim-303")
    note = make_note(
        note_id="raw-note",
        relative_path="Pojęcia/raw-note.md",
        content="# Raw Note\n",
        content_hash="3" * 64,
        managed=False,
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="raw-note",
        relative_path="Pojęcia/raw-note.md",
        rationale="Enrich unmanaged file",
        proposed_body=f"Summary with {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {note.note_id: note},
        advisor,
    )

    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None
    assert "not managed" in decision.rationale.lower()


def test_supplied_content_hash_preserved():
    quote_text = "Content hash integrity verification quote"
    claim = make_claim(claim_id="c-hash", quote=quote_text)
    verif = make_verification(claim_id="c-hash")
    supplied_hash = "deadbeef" * 8
    actual_content = "# Raw content with BOM or LF differences\n"
    recomputed_hash = hashlib.sha256(actual_content.encode("utf-8")).hexdigest()
    assert supplied_hash != recomputed_hash

    note = make_note(
        note_id="target-hash",
        relative_path="Pojęcia/target-hash.md",
        content=actual_content,
        content_hash=supplied_hash,
        managed=True,
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="target-hash",
        relative_path="Pojęcia/target-hash.md",
        rationale="Enrich note",
        proposed_body=f"Body containing quote: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {note.note_id: note},
        advisor,
    )

    assert len(decisions) == 1
    patch = decisions[0].patch
    assert patch is not None
    assert patch.base_hash == supplied_hash
    assert patch.base_hash != recomputed_hash


def test_create_new_note_success():
    quote_text = "Autonomous agent feedback loop dynamics"
    claim = make_claim(claim_id="x:404:1", quote=quote_text)
    verif = make_verification(claim_id="x:404:1")
    advice = IntegrationAdvice(
        operation=IntegrationOperation.create,
        rationale="New concept synthesis",
        proposed_body=f"# Agent Loops\n\nAnalysis quoting: {quote_text}\n",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.create
    assert decision.patch is not None
    patch = decision.patch
    assert patch.note_id == "kb-x-404-1"
    assert patch.relative_path == "Pojęcia/kb-x-404-1.md"
    assert patch.base_hash is None
    assert patch.claim_ids == ["x:404:1"]

    fm, err = _frontmatter(patch.proposed_content)
    assert err is None
    assert fm is not None
    assert fm["note_id"] == "kb-x-404-1"
    assert fm["kb_managed"] is True
    assert fm["claim_ids"] == ["x:404:1"]
    assert quote_text in patch.proposed_content


def test_create_with_advisor_relative_path():
    quote_text = "Custom destination quote text"
    claim = make_claim(claim_id="custom-1", quote=quote_text)
    verif = make_verification(claim_id="custom-1")
    advice = IntegrationAdvice(
        operation=IntegrationOperation.create,
        relative_path="Narzędzia/custom-tool.md",
        rationale="Custom folder creation",
        proposed_body=f"Content with quote: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    assert len(decisions) == 1
    patch = decisions[0].patch
    assert patch is not None
    assert patch.relative_path == "Narzędzia/custom-tool.md"
    assert patch.note_id == "kb-custom-1"


def test_create_rejected_when_candidates_exist():
    quote_text = "Candidate presence prevents note creation"
    claim = make_claim(claim_id="c-cand", quote=quote_text)
    verif = make_verification(claim_id="c-cand")
    cand = make_candidate()
    advice = IntegrationAdvice(
        operation=IntegrationOperation.create,
        rationale="Create despite candidate",
        proposed_body=f"Body: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {"c-cand": [cand]},
        {},
        advisor,
    )

    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None


def test_create_rejected_when_path_already_exists():
    quote_text = "Collision with pre-existing note relative path"
    claim = make_claim(claim_id="col-1", quote=quote_text)
    verif = make_verification(claim_id="col-1")
    existing_note = make_note(
        note_id="existing-tool",
        relative_path="Narzędzia/existing.md",
        content="Other note",
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.create,
        relative_path="Narzędzia/existing.md",
        rationale="Collision test",
        proposed_body=f"Body: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {existing_note.note_id: existing_note},
        advisor,
    )

    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.defer
    assert decisions[0].patch is None


def test_unsafe_relative_paths_defer():
    quote_text = "Checking path traversal safety"
    claim = make_claim(claim_id="unsafe-1", quote=quote_text)
    verif = make_verification(claim_id="unsafe-1")

    for unsafe_path in ["../escaped.md", "/etc/passwd.md", "C:\\temp\\file.md"]:
        advice = IntegrationAdvice(
            operation=IntegrationOperation.create,
            relative_path=unsafe_path,
            rationale="Unsafe path injection",
            proposed_body=f"Body: {quote_text}",
        )
        advisor = Mock(return_value=advice)
        decisions = integrate_claims([claim], [verif], {}, {}, advisor)
        assert len(decisions) == 1
        assert decisions[0].operation == IntegrationOperation.defer
        assert decisions[0].patch is None


def test_empty_proposed_body_defers():
    claim = make_claim(claim_id="empty-b")
    verif = make_verification(claim_id="empty-b")
    advice = IntegrationAdvice(
        operation=IntegrationOperation.create,
        rationale="Missing body",
        proposed_body="   \n  ",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.defer
    assert decisions[0].patch is None


def test_quote_missing_from_new_text_defers():
    claim = make_claim(claim_id="missing-q", quote="Must be present verbatim")
    verif = make_verification(claim_id="missing-q")
    advice = IntegrationAdvice(
        operation=IntegrationOperation.create,
        rationale="Body without verbatim quote",
        proposed_body="This text does not have the original snippet.",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.defer
    assert decisions[0].patch is None


def test_harness_guard_unrelated_claim():
    claim = make_claim(
        claim_id="unrelated-harness",
        text="Vector database indexing and clustering efficiency",
        quote="clustering efficiency",
    )
    verif = make_verification(claim_id="unrelated-harness")
    note = make_note(
        note_id="Harness",
        relative_path="Pojęcia/Harness.md",
        content="# Harness\nGeneral agent test harness.\n",
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="Harness",
        relative_path="Pojęcia/Harness.md",
        rationale="Mapping unknown concept to harness",
        proposed_body="clustering efficiency discussion",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {note.note_id: note},
        advisor,
    )

    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.operation == IntegrationOperation.defer
    assert decision.patch is None


def test_harness_allowed_for_matching_claim():
    quote_text = "Harness design for multi-turn evaluations"
    claim = make_claim(
        claim_id="related-harness",
        text="A test harness is essential for multi-turn evaluations",
        quote=quote_text,
    )
    verif = make_verification(claim_id="related-harness")
    note = make_note(
        note_id="Harness",
        relative_path="Pojęcia/Harness.md",
        content="# Harness\nGeneral agent test harness.\n",
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="Harness",
        relative_path="Pojęcia/Harness.md",
        rationale="Valid harness concept",
        proposed_body=f"Adding insight: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {note.note_id: note},
        advisor,
    )

    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.enrich
    assert decisions[0].patch is not None


def test_yaml_frontmatter_handles_colon_and_quotes():
    quote_text = "Quote with \"nested\" and 'mixed' quotes"
    claim = make_claim(
        claim_id='test:id:with:colons:and"quotes"',
        quote=quote_text,
    )
    verif = make_verification(claim_id='test:id:with:colons:and"quotes"')
    advice = IntegrationAdvice(
        operation=IntegrationOperation.create,
        rationale="Complex character validation",
        proposed_body=f"Body containing: {quote_text}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    assert len(decisions) == 1
    patch = decisions[0].patch
    assert patch is not None

    parsed_fm, err = _frontmatter(patch.proposed_content)
    assert err is None
    assert parsed_fm is not None
    assert parsed_fm["claim_ids"] == ['test:id:with:colons:and"quotes"']
    assert parsed_fm["kb_managed"] is True


def test_decisions_ordered_by_claim_id():
    claims = [
        make_claim(claim_id="z:300"),
        make_claim(claim_id="a:100"),
        make_claim(claim_id="m:200"),
    ]
    advisor = Mock()

    decisions = integrate_claims(claims, {}, {}, {}, advisor)

    assert [d.claim_ids[0] for d in decisions] == ["a:100", "m:200", "z:300"]


def test_write_artifacts_workspace_inside_vault_raises(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    inside_workspace = vault / "workspace"
    inside_workspace.mkdir()

    decisions = [
        IntegrationDecision(
            operation=IntegrationOperation.defer,
            claim_ids=["c1"],
            rationale="Test defer",
        )
    ]

    with pytest.raises(ValueError, match="outside the vault"):
        write_integration_artifacts(inside_workspace, vault, decisions)


def test_write_artifacts_canonical_json_and_deterministic(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    decisions = [
        IntegrationDecision(
            operation=IntegrationOperation.defer,
            claim_ids=["c1"],
            rationale="Deterministic output test",
        )
    ]

    path1 = write_integration_artifacts(workspace, vault, decisions)
    bytes1 = path1.read_bytes()

    path2 = write_integration_artifacts(workspace, vault, decisions)
    bytes2 = path2.read_bytes()

    assert path1 == path2
    assert bytes1 == bytes2

    expected_hash = hashlib.sha256(bytes1).hexdigest()
    assert path1.parent.name == expected_hash
    assert path1.name == "decisions.json"
    assert bytes1.endswith(b"\n")

    decoded = json.loads(bytes1.decode("utf-8"))
    assert isinstance(decoded, list)
    assert decoded[0]["claim_ids"] == ["c1"]


def test_write_artifacts_symlink_inside_vault_raises(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    decisions = [
        IntegrationDecision(
            operation=IntegrationOperation.defer,
            claim_ids=["c1"],
            rationale="Symlink traversal test",
        )
    ]

    target_dir = workspace / "integration"

    monkeypatch.setattr(Path, "is_symlink", lambda self: self == target_dir)
    monkeypatch.setattr(
        Path,
        "resolve",
        lambda self, strict=False: vault / "subdir" if self == target_dir else self,
    )

    with pytest.raises(ValueError, match="inside the vault"):
        write_integration_artifacts(workspace, vault, decisions)


def test_write_artifacts_rejects_sensitive_keys(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    forbidden_keys = [
        "headers",
        "authorization",
        "cookie",
        "api_key",
        "password",
        "token",
        "access_token",
        "refresh_token",
        "user_credentials",
        "app_secret",
    ]

    for key in forbidden_keys:
        bad_payload = [
            {
                "operation": "defer",
                "claim_ids": ["c1"],
                "rationale": "test",
                key: "sensitive_val",
            }
        ]
        with pytest.raises(ValueError, match="Prohibited sensitive dictionary key"):
            write_integration_artifacts(workspace, vault, bad_payload)


def test_write_artifacts_allows_sensitive_words_in_values(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    decisions = [
        IntegrationDecision(
            operation=IntegrationOperation.defer,
            claim_ids=["c1"],
            rationale="Contains headers, authorization, cookie, api_key, password, token, credential, secret.",
        )
    ]

    path = write_integration_artifacts(workspace, vault, decisions)
    assert path.is_file()


def test_positional_constructors():
    n = NoteView("note-1", "Pojęcia/note-1.md", "Content", "c" * 64, True)
    assert n.note_id == "note-1"
    assert n.relative_path == "Pojęcia/note-1.md"
    assert n.content == "Content"
    assert n.content_hash == "c" * 64
    assert n.managed is True

    s = SectionCandidate("note-1", "Pojęcia/note-1.md", "Heading", "anchor", "snippet", 0.8)
    assert s.note_id == "note-1"
    assert s.heading == "Heading"
    assert s.score == 0.8

    a = IntegrationAdvice(IntegrationOperation.create, None, None, None, "Rationale text")
    assert a.operation == IntegrationOperation.create
    assert a.rationale == "Rationale text"


def test_target_note_not_found_defers():
    claim = make_claim(claim_id="c-missing-target")
    verif = make_verification(claim_id="c-missing-target")
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="nonexistent-note",
        relative_path="Pojęcia/nonexistent.md",
        rationale="Missing target",
        proposed_body=f"Summary with {claim.evidence[0].quote}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.defer
    assert decisions[0].patch is None


def test_relative_path_mismatch_defers():
    claim = make_claim(claim_id="c-path-mismatch")
    verif = make_verification(claim_id="c-path-mismatch")
    note = make_note(
        note_id="real-note",
        relative_path="Pojęcia/real-note.md",
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="real-note",
        relative_path="Procesy/wrong-path.md",
        rationale="Wrong path provided",
        proposed_body=f"Summary with {claim.evidence[0].quote}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims(
        [claim],
        [verif],
        {},
        {note.note_id: note},
        advisor,
    )

    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.defer
    assert decisions[0].patch is None


def test_contradiction_never_produces_patch():
    claim = make_claim(claim_id="c-contra-patch")
    verif = make_verification(
        claim_id="c-contra-patch",
        relation=VerificationRelation.contradicts,
    )
    advice = IntegrationAdvice(
        operation=IntegrationOperation.enrich,
        target_note_id="note-1",
        relative_path="Pojęcia/note-1.md",
        rationale="Contradiction should not write patch",
        conflicting_claim_ids=["prior:claim:99"],
        proposed_body=f"Proposed text: {claim.evidence[0].quote}",
    )
    advisor = Mock(return_value=advice)

    decisions = integrate_claims([claim], [verif], {}, {}, advisor)

    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.record_conflict
    assert decisions[0].patch is None


def test_advisor_signature_variants():
    quote = "Quote for signature test"
    claim = make_claim(claim_id="c-sig", quote=quote)
    verif = make_verification(claim_id="c-sig")

    def adv_one_arg(c):
        return IntegrationAdvice(
            operation=IntegrationOperation.create,
            rationale="One argument advisor",
            proposed_body=f"Body: {quote}",
        )

    def adv_two_args(c, cands):
        return IntegrationAdvice(
            operation=IntegrationOperation.create,
            rationale="Two arguments advisor",
            proposed_body=f"Body: {quote}",
        )

    def adv_three_args(c, cands, n):
        return IntegrationAdvice(
            operation=IntegrationOperation.create,
            rationale="Three arguments advisor",
            proposed_body=f"Body: {quote}",
        )

    d1 = integrate_claims([claim], [verif], {}, {}, adv_one_arg)
    assert d1[0].operation == IntegrationOperation.create

    d2 = integrate_claims([claim], [verif], {}, {}, adv_two_args)
    assert d2[0].operation == IntegrationOperation.create

    d3 = integrate_claims([claim], [verif], {}, {}, adv_three_args)
    assert d3[0].operation == IntegrationOperation.create


def test_advisor_returning_dict():
    quote = "Quote for dict advisor"
    claim = make_claim(claim_id="c-dict", quote=quote)
    verif = make_verification(claim_id="c-dict")

    def adv_dict(c, cands):
        return {
            "operation": "create",
            "rationale": "Dict advisor result",
            "proposed_body": f"Body: {quote}",
        }

    decisions = integrate_claims([claim], [verif], {}, {}, adv_dict)
    assert len(decisions) == 1
    assert decisions[0].operation == IntegrationOperation.create


def test_write_artifacts_workspace_symlink_alias_inside_vault(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    workspace = tmp_path / "workspace_link"

    monkeypatch.setattr(
        Path,
        "resolve",
        lambda self, strict=False: vault / "aliased_ws" if self == workspace else self,
    )

    decisions = [
        IntegrationDecision(
            operation=IntegrationOperation.defer,
            claim_ids=["c1"],
            rationale="Alias test",
        )
    ]

    with pytest.raises(ValueError, match="outside the vault"):
        write_integration_artifacts(workspace, vault, decisions)

