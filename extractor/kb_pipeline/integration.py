"""Offline integration stage producing structured integration decisions and artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from .schemas import (
    Claim,
    IntegrationDecision,
    IntegrationOperation,
    NotePatch,
    VerificationRelation,
    VerificationResult,
)

__all__ = [
    "NoteView",
    "SectionCandidate",
    "IntegrationAdvice",
    "integrate_claims",
    "write_integration_artifacts",
]

EXACT_FORBIDDEN_KEYS = frozenset({
    "headers",
    "authorization",
    "cookie",
    "api_key",
    "password",
    "token",
})

ALLOWED_CREATE_DIRS = frozenset({"Pojęcia", "Procesy", "Narzędzia", "Zasady"})

WINDOWS_RESERVED_NAMES = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
})


class NoteView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note_id: str
    relative_path: str
    content: str
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    managed: bool

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if args:
            fields = ("note_id", "relative_path", "content", "content_hash", "managed")
            kwargs = dict(zip(fields, args)) | kwargs
        super().__init__(**kwargs)


class SectionCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    note_id: str
    relative_path: str
    heading: str
    anchor: str
    snippet: str
    score: float

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if args:
            fields = ("note_id", "relative_path", "heading", "anchor", "snippet", "score")
            kwargs = dict(zip(fields, args)) | kwargs
        super().__init__(**kwargs)


class IntegrationAdvice(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation: IntegrationOperation
    target_note_id: str | None = None
    relative_path: str | None = None
    section: str | None = None
    rationale: str
    conflicting_claim_ids: list[str] = Field(default_factory=list)
    proposed_body: str | None = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if args:
            fields = (
                "operation",
                "target_note_id",
                "relative_path",
                "section",
                "rationale",
                "conflicting_claim_ids",
                "proposed_body",
            )
            kwargs = dict(zip(fields, args)) | kwargs
        super().__init__(**kwargs)


def _is_safe_relative_path(path_str: str | None) -> bool:
    if not path_str or not isinstance(path_str, str):
        return False
    if "\x00" in path_str:
        return False
    if path_str.startswith("/") or path_str.startswith("\\"):
        return False
    if re.match(r"^[a-zA-Z]:", path_str):
        return False
    p = Path(path_str)
    if p.is_absolute():
        return False
    for part in p.parts:
        if part in ("..", ""):
            return False
    norm = os.path.normpath(path_str)
    if norm.startswith("..") or os.path.isabs(norm):
        return False
    return True


def _is_valid_create_path(path_str: str | None) -> bool:
    if not _is_safe_relative_path(path_str):
        return False
    if not path_str or not path_str.endswith(".md"):
        return False
    p = Path(path_str)
    parts = p.parts
    if len(parts) < 2:
        return False
    if parts[0] not in ALLOWED_CREATE_DIRS:
        return False
    for part in parts:
        stem = Path(part).stem.upper()
        base = part.split(".")[0].upper()
        if stem in WINDOWS_RESERVED_NAMES or base in WINDOWS_RESERVED_NAMES:
            return False
    return True


def _sanitize_note_id(claim_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "-", claim_id)
    return f"kb-{cleaned}"


def _is_harness_target(note_id: str, relative_path: str) -> bool:
    stem = Path(relative_path).stem.casefold()
    nid = note_id.casefold()
    return nid in ("harness", "kb-harness") or stem == "harness"


def _call_advisor(
    advisor: Any,
    claim: Claim,
    candidates: list[SectionCandidate],
    notes: Mapping[str, NoteView],
) -> IntegrationAdvice:
    try:
        import inspect

        sig = inspect.signature(advisor)
        params = list(sig.parameters.values())
        has_varargs = any(p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD) for p in params)
        if not has_varargs:
            pos_params = [
                p for p in params
                if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
            ]
            num_pos = len(pos_params)
            req_params = [p for p in pos_params if p.default is inspect.Parameter.empty]
            num_req = len(req_params)
            if num_req <= 1 and num_pos == 1:
                res = advisor(claim)
            elif num_req <= 2 and num_pos == 2:
                res = advisor(claim, candidates)
            elif num_pos >= 3:
                res = advisor(claim, candidates, notes)
            else:
                res = advisor(claim, candidates)
        else:
            res = advisor(claim, candidates)
    except (ValueError, TypeError):
        try:
            res = advisor(claim, candidates)
        except TypeError:
            try:
                res = advisor(claim)
            except TypeError:
                res = advisor(claim, candidates, notes)

    if isinstance(res, dict):
        return IntegrationAdvice.model_validate(res)
    return res


def _build_appended_section(
    claim: Claim,
    advice: IntegrationAdvice,
    target_content: str,
) -> tuple[str, str]:
    is_enrich = advice.operation == IntegrationOperation.enrich
    heading_title = f"Teza {claim.claim_id}" if is_enrich else f"Dowód {claim.claim_id}"
    heading = f"## {heading_title}"

    quotes_block = "\n".join(f"> {ev.quote}" for ev in claim.evidence)
    conditions_block = (
        "\n".join(f"- {c}" for c in claim.conditions)
        if claim.conditions
        else "Brak"
    )
    limitations_block = (
        "\n".join(f"- {l}" for l in claim.limitations)
        if claim.limitations
        else "Brak"
    )

    body_text = advice.proposed_body.strip() if advice.proposed_body else ""

    section_body = (
        f"{heading}\n\n"
        f"{body_text}\n\n"
        f"**Identyfikator tezy**: {claim.claim_id}\n\n"
        f"**Dowody**:\n{quotes_block}\n\n"
        f"**Warunki / Conditions**:\n{conditions_block}\n\n"
        f"**Ograniczenia / Limitations**:\n{limitations_block}\n\n"
        f"Status: the claim is source-supported and not independently validated.\n"
    )

    base = target_content
    if not base.endswith("\n"):
        base += "\n"
    if not base.endswith("\n\n"):
        base += "\n"
    proposed_content = base + section_body
    return heading_title, proposed_content


def _build_create_content(
    claim: Claim,
    new_note_id: str,
    proposed_body: str,
) -> str:
    fm_dict = {
        "note_id": new_note_id,
        "kb_managed": True,
        "claim_ids": [claim.claim_id],
    }
    fm_yaml = yaml.safe_dump(fm_dict, sort_keys=False, allow_unicode=True)
    body = proposed_body.strip()
    return f"---\n{fm_yaml}---\n\n{body}\n"


def integrate_claims(
    claims: Sequence[Claim] | Mapping[str, Claim],
    verifications: Sequence[VerificationResult] | Mapping[str, VerificationResult],
    candidates: Sequence[SectionCandidate] | Mapping[str, Sequence[SectionCandidate]],
    notes: Mapping[str, NoteView],
    advisor: Any,
) -> list[IntegrationDecision]:
    claim_list: list[Claim] = (
        list(claims.values()) if isinstance(claims, dict) else list(claims)
    )
    sorted_claims = sorted(claim_list, key=lambda c: c.claim_id)

    verif_map: Mapping[str, VerificationResult] = (
        verifications
        if isinstance(verifications, dict)
        else {v.claim_id: v for v in verifications}
    )

    decisions: list[IntegrationDecision] = []

    for claim in sorted_claims:
        if candidates is None:
            claim_candidates = []
        elif isinstance(candidates, dict):
            claim_candidates = list(candidates.get(claim.claim_id, []))
        elif isinstance(candidates, (list, tuple)):
            claim_candidates = list(candidates)
        else:
            claim_candidates = []

        candidate_note_ids = list(dict.fromkeys(c.note_id for c in claim_candidates))

        verif = verif_map.get(claim.claim_id)

        if verif is None:
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=f"Verification missing for claim '{claim.claim_id}'",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        if not verif.quote_matches:
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=f"Verification quote mismatch for claim '{claim.claim_id}'",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        if verif.relation not in (VerificationRelation.supports, VerificationRelation.contradicts):
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=f"Verification relation '{verif.relation.value}' is neither supports nor contradicts",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        duplicate_note: NoteView | None = None
        for ev in claim.evidence:
            if not ev.quote:
                continue
            for note in notes.values():
                if ev.quote in note.content:
                    duplicate_note = note
                    break
            if duplicate_note is not None:
                break

        if duplicate_note is not None:
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.duplicate,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=f"Exact evidence quote already present in note '{duplicate_note.note_id}'",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        if verif.relation == VerificationRelation.contradicts:
            advice = _call_advisor(advisor, claim, claim_candidates, notes)
            conflicts = (
                advice.conflicting_claim_ids
                if advice and advice.conflicting_claim_ids
                else []
            )
            if conflicts:
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.record_conflict,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=advice.rationale if advice else "Contradiction recorded",
                        patch=None,
                        conflicting_claim_ids=conflicts,
                    )
                )
            else:
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=advice.rationale if advice else "Contradiction without conflicting claims",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
            continue

        if not verif.source_supported:
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=f"Claim '{claim.claim_id}' is not source-supported",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        advice = _call_advisor(advisor, claim, claim_candidates, notes)
        if advice is None:
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale="Advisor returned no advice",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        if advice.operation in (
            IntegrationOperation.duplicate,
            IntegrationOperation.record_conflict,
            IntegrationOperation.defer,
        ):
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=advice.rationale,
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        if not advice.proposed_body or not advice.proposed_body.strip():
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale="Proposed body is empty",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        if any(ev.quote not in advice.proposed_body for ev in claim.evidence):
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale="Evidence quote missing from proposed body",
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )
            continue

        if advice.operation == IntegrationOperation.create:
            if len(claim_candidates) > 0:
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale="Cannot create note when candidate notes exist",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            new_note_id = _sanitize_note_id(claim.claim_id)
            if not advice.relative_path or not advice.relative_path.strip():
                rel_path = f"Pojęcia/{new_note_id}.md"
            else:
                rel_path = advice.relative_path.strip()

            if not _is_valid_create_path(rel_path):
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=f"Invalid or unsafe create relative path '{rel_path}'",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            if _is_harness_target(new_note_id, rel_path) and "harness" not in claim.text.casefold():
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale="Harness note rejected for unrelated claim",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            if any(n.relative_path == rel_path for n in notes.values()) or new_note_id in notes:
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=f"Note already exists at path '{rel_path}' or note_id '{new_note_id}'",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            proposed_content = _build_create_content(claim, new_note_id, advice.proposed_body)
            patch = NotePatch(
                note_id=new_note_id,
                relative_path=rel_path,
                section=advice.section,
                claim_ids=[claim.claim_id],
                base_hash=None,
                proposed_content=proposed_content,
            )
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.create,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=advice.rationale,
                    patch=patch,
                    conflicting_claim_ids=advice.conflicting_claim_ids,
                )
            )

        elif advice.operation in (IntegrationOperation.enrich, IntegrationOperation.add_evidence):
            if not advice.target_note_id or advice.target_note_id not in notes:
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=f"Target note '{advice.target_note_id}' not found",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            target = notes[advice.target_note_id]
            if not advice.relative_path or target.relative_path != advice.relative_path:
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=f"Relative path mismatch for target note '{target.note_id}'",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            if not _is_safe_relative_path(advice.relative_path):
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=f"Unsafe relative path '{advice.relative_path}'",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            if _is_harness_target(target.note_id, target.relative_path) and "harness" not in claim.text.casefold():
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale="Harness note rejected for unrelated claim",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            if not target.managed:
                decisions.append(
                    IntegrationDecision(
                        operation=IntegrationOperation.defer,
                        claim_ids=[claim.claim_id],
                        candidate_note_ids=candidate_note_ids,
                        rationale=f"Target note '{target.note_id}' is not managed",
                        patch=None,
                        conflicting_claim_ids=[],
                    )
                )
                continue

            section_name, proposed_content = _build_appended_section(
                claim, advice, target.content
            )
            patch = NotePatch(
                note_id=target.note_id,
                relative_path=target.relative_path,
                section=advice.section or section_name,
                claim_ids=[claim.claim_id],
                base_hash=target.content_hash,
                proposed_content=proposed_content,
            )
            decisions.append(
                IntegrationDecision(
                    operation=advice.operation,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=advice.rationale,
                    patch=patch,
                    conflicting_claim_ids=advice.conflicting_claim_ids,
                )
            )

        else:
            decisions.append(
                IntegrationDecision(
                    operation=IntegrationOperation.defer,
                    claim_ids=[claim.claim_id],
                    candidate_note_ids=candidate_note_ids,
                    rationale=advice.rationale,
                    patch=None,
                    conflicting_claim_ids=[],
                )
            )

    return decisions


def _normalize_key(key: str) -> str:
    return re.sub(r"[\s\-]+", "_", key.strip().lower())


def _is_forbidden_key(key: str) -> bool:
    norm = _normalize_key(key)
    if norm in EXACT_FORBIDDEN_KEYS:
        return True
    if norm.endswith("_token"):
        return True
    if "credential" in norm or "secret" in norm:
        return True
    return False


def _validate_dict_keys(data: Any) -> None:
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(k, str) and _is_forbidden_key(k):
                raise ValueError(f"Prohibited sensitive dictionary key: '{k}'")
            _validate_dict_keys(v)
    elif isinstance(data, list):
        for item in data:
            _validate_dict_keys(item)


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def write_integration_artifacts(
    workspace: Path | str,
    vault: Path | str,
    decisions: Sequence[IntegrationDecision | dict[str, Any]],
) -> Path:
    vault_entry = Path(os.path.abspath(vault))
    vault_path = Path(vault).resolve(strict=True)
    if not vault_path.is_dir():
        raise ValueError("Vault must be a directory")

    workspace_entry = Path(os.path.abspath(workspace))
    workspace_path = Path(workspace).resolve(strict=False)

    if _is_within(workspace_entry, vault_entry) or _is_within(workspace_path, vault_path):
        raise ValueError("Workspace must be outside the vault")

    payload = [
        d.model_dump(mode="json") if hasattr(d, "model_dump") else d
        for d in decisions
    ]

    _validate_dict_keys(payload)

    json_str = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    json_bytes = json_str.encode("utf-8")
    content_hash = hashlib.sha256(json_bytes).hexdigest()

    artifact_dir = Path(workspace) / "integration" / content_hash
    target_path = artifact_dir / "decisions.json"

    check_node: Path | None = target_path
    while check_node is not None and check_node != check_node.parent:
        if check_node.is_symlink():
            link_target = Path(os.path.abspath(check_node.resolve(strict=False)))
            if _is_within(link_target, vault_entry) or _is_within(link_target, vault_path):
                raise ValueError(
                    f"Artifact path '{target_path}' traverses a symlink pointing inside the vault: '{link_target}'"
                )
        check_node = check_node.parent

    resolved_target = target_path.resolve(strict=False)
    target_entry = Path(os.path.abspath(resolved_target))
    if _is_within(target_entry, vault_entry) or _is_within(resolved_target, vault_path):
        raise ValueError(
            f"Artifact destination '{target_path}' resolves inside the vault: '{resolved_target}'"
        )

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(json_bytes)
    return target_path
