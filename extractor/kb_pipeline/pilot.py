from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .context import build_context
from .retrieval import reindex, search
from .schemas import (
    Claim,
    ContextBundle,
    RunManifest,
    SourceRecord,
    StageRecord,
    StageStatus,
    VerificationRelation,
)
from .stage_cache import StageCache
from .verification import verify_claim

_FIXTURE_FIELDS = {"sources", "claims", "mock_semantic_relations", "query"}
_REQUIRED_FIELDS = {"sources", "claims", "query"}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate fixture field: {key}")
        result[key] = value
    return result


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _safe_paths(vault: Path, workspace: Path) -> tuple[Path, Path]:
    vault_entry = Path(os.path.abspath(vault))
    vault_path = vault.resolve(strict=True)
    if not vault_path.is_dir():
        raise ValueError("Vault must be a directory")

    workspace_entry = Path(os.path.abspath(workspace))
    workspace_path = workspace.resolve(strict=False)
    if (
        _is_within(workspace_entry, vault_entry)
        or _is_within(workspace_path, vault_path)
    ):
        raise ValueError("Workspace must be outside the vault")
    return vault_path, workspace_path


def _validate_fixture(
    payload: bytes,
) -> tuple[list[SourceRecord], list[Claim], dict[str, VerificationRelation], str]:
    try:
        fixture = json.loads(payload.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Fixture must be valid UTF-8 JSON") from exc

    if not isinstance(fixture, dict):
        raise ValueError("Fixture must be a JSON object")
    unknown_fields = set(fixture) - _FIXTURE_FIELDS
    missing_fields = _REQUIRED_FIELDS - set(fixture)
    if unknown_fields:
        raise ValueError(f"Unexpected fixture fields: {', '.join(sorted(unknown_fields))}")
    if missing_fields:
        raise ValueError(f"Missing fixture fields: {', '.join(sorted(missing_fields))}")
    if not isinstance(fixture["sources"], list) or not isinstance(fixture["claims"], list):
        raise ValueError("Fixture sources and claims must be lists")
    if not isinstance(fixture["query"], str):
        raise ValueError("Fixture query must be a string")

    sources = [SourceRecord.model_validate(item) for item in fixture["sources"]]
    claims = [Claim.model_validate(item) for item in fixture["claims"]]

    source_ids = [source.source_id for source in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Fixture contains duplicate source IDs")
    claim_ids = [claim.claim_id for claim in claims]
    if len(claim_ids) != len(set(claim_ids)):
        raise ValueError("Fixture contains duplicate claim IDs")

    source_id_set = set(source_ids)
    for claim in claims:
        missing = (set(claim.source_ids) | {item.source_id for item in claim.evidence}) - source_id_set
        if missing:
            raise ValueError(
                f"Claim '{claim.claim_id}' references missing sources: {', '.join(sorted(missing))}"
            )

    raw_relations = fixture.get("mock_semantic_relations", {})
    if not isinstance(raw_relations, dict):
        raise ValueError("mock_semantic_relations must be an object")
    claim_id_set = set(claim_ids)
    unknown_claims = set(raw_relations) - claim_id_set
    if unknown_claims:
        raise ValueError(
            "Mock relations reference unknown claims: " + ", ".join(sorted(unknown_claims))
        )
    relations: dict[str, VerificationRelation] = {}
    for claim_id, relation in raw_relations.items():
        try:
            relations[claim_id] = VerificationRelation(relation)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid mock relation for claim '{claim_id}'") from exc

    return sources, claims, relations, fixture["query"]


def _source_summary(source: SourceRecord) -> dict[str, Any]:
    return {
        "source_id": source.source_id,
        "author": source.author,
        "url": source.url,
        "published_at": source.published_at.isoformat() if source.published_at else None,
        "language": source.language,
        "reply_to_id": source.reply_to_id,
        "conversation_id": source.conversation_id,
        "quoted_source_id": source.quoted_source_id,
        "context_status": source.context_status.value,
    }


def _context_json(bundle: ContextBundle) -> dict[str, Any]:
    def with_text(source: SourceRecord) -> dict[str, Any]:
        return {**_source_summary(source), "text": source.text}

    return {
        "focus": with_text(bundle.focus),
        "related": [
            {
                "source": with_text(item.source),
                "role": item.role,
                "provenance": item.provenance,
            }
            for item in bundle.related
        ],
        "missing_ids": bundle.missing_ids,
        "context_status": bundle.context_status.value,
    }


def _write_json(path: Path, value: Any) -> None:
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((payload + "\n").encode("utf-8"))


def _stage_record(status: StageStatus, *refs: str, error: str | None = None) -> StageRecord:
    return StageRecord(status=status, artifact_refs=list(refs), error=error)


def _proposal(
    claims: list[Claim],
    results: dict[str, dict[str, Any]],
    sources: dict[str, SourceRecord],
    candidates: list[dict[str, Any]],
) -> str:
    eligible = [claim for claim in claims if results[claim.claim_id]["status"] == "completed"]
    lines = [
        "# Offline staging proposal",
        "",
        "> **OFFLINE MOCK — DO NOT PUBLISH**",
        "",
    ]
    for claim in eligible:
        lines.extend([f"## {claim.claim_id}", "", claim.text, "", "### Evidence", ""])
        for evidence in claim.evidence:
            source = sources[evidence.source_id]
            lines.extend(
                [
                    f'- Quote: “{evidence.quote}”',
                    f"  - source_id: `{source.source_id}`",
                    f"  - url: {source.url or 'URL not provided'}",
                ]
            )
        lines.extend(["", f"Scope: {claim.scope or 'Not specified.'}", ""])
        if claim.conditions:
            lines.extend(["Conditions:", *[f"- {item}" for item in claim.conditions], ""])
        else:
            lines.extend(["Conditions: None specified.", ""])
        if claim.limitations:
            lines.extend(["Limitations:", *[f"- {item}" for item in claim.limitations], ""])
        lines.extend(["Candidate note paths (suggestions only):", ""])
        if candidates:
            lines.extend(f"- `{candidate['path']}`" for candidate in candidates)
        else:
            lines.append("- No matching note candidates.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def run_pilot(vault: Path, workspace: Path, fixture: Path) -> dict[str, Any]:
    vault_path, workspace_path = _safe_paths(Path(vault), Path(workspace))
    fixture_payload = Path(fixture).read_bytes()
    fixture_hash = hashlib.sha256(fixture_payload).hexdigest()
    run_id = f"offline-{fixture_hash}"
    sources, claims, mock_relations, query = _validate_fixture(fixture_payload)
    source_by_id = {source.source_id: source for source in sources}

    run_dir = workspace_path / run_id
    if _is_within(run_dir.resolve(strict=False), vault_path):
        raise ValueError("Run directory must be outside the vault")
    run_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir = run_dir / "artifacts"

    summary = {
        "run_id": run_id,
        "fixture_hash": fixture_hash,
        "source_count": len(sources),
        "claim_count": len(claims),
        "evidence_count": sum(len(claim.evidence) for claim in claims),
        "source_ids": [source.source_id for source in sources],
        "claim_ids": [claim.claim_id for claim in claims],
        "mock_relation_claim_ids": sorted(mock_relations),
        "query_present": bool(query.strip()),
    }
    summary_ref = "artifacts/validated_input_summary.json"
    _write_json(artifact_dir / "validated_input_summary.json", summary)

    stage_statuses: dict[str, StageRecord] = {
        "fixture_validation": _stage_record(StageStatus.completed, summary_ref),
        "context_assembly": _stage_record(StageStatus.pending),
        "quote_verification": _stage_record(StageStatus.pending),
        "semantic_assessment": _stage_record(
            StageStatus.deferred, error="No real semantic evaluator is used by this run."
        ),
        "vault_search": _stage_record(StageStatus.pending),
        "proposal": _stage_record(StageStatus.pending),
        "publication": _stage_record(
            StageStatus.deferred, error="Staged proposals are not published."
        ),
    }

    with StageCache(run_dir) as cache:
        previous = cache.load_manifest(run_id)
        created_at = previous.created_at if previous else datetime.now(timezone.utc)
        cache.put(
            cache.key("fixture_validation", fixture_hash, "", "offline", "v1"),
            {"mode": "offline", "bypass": True, "summary": summary},
        )

        context_bundles: list[dict[str, Any]] = []
        context_ref = "artifacts/context_bundles.json"
        try:
            context_bundles = [
                _context_json(build_context(source, source_by_id.get)) for source in sources
            ]
            _write_json(artifact_dir / "context_bundles.json", context_bundles)
            cache.put(
                cache.key("context", fixture_hash, "", "offline", "v1"),
                {"mode": "offline", "bypass": True, "bundles": context_bundles},
            )
            stage_statuses["context_assembly"] = _stage_record(
                StageStatus.completed, context_ref
            )
        except Exception as exc:
            stage_statuses["context_assembly"] = _stage_record(
                StageStatus.error, error=str(exc)
            )

        verification_artifact: list[dict[str, Any]] = []
        proposed_claim_ids: list[str] = []
        deferred_claim_ids: list[str] = []
        verification_ref = "artifacts/verification_results.json"
        try:
            for claim in claims:
                mock_relation = mock_relations.get(claim.claim_id)
                semantic_check = None
                if mock_relation is not None:
                    semantic_check = lambda _claim, _sources, relation=mock_relation: (
                        relation,
                        "Fixture-supplied mock semantic relation.",
                    )
                result = verify_claim(claim, source_by_id, semantic_check)
                eligible = (
                    result.quote_matches
                    and result.source_supported
                    and result.relation is VerificationRelation.supports
                )
                status = "completed" if eligible else "deferred"
                if eligible:
                    proposed_claim_ids.append(claim.claim_id)
                else:
                    deferred_claim_ids.append(claim.claim_id)
                verification_artifact.append(
                    {
                        "claim_id": claim.claim_id,
                        "status": status,
                        "assessment_mode": (
                            "fixture_mock" if mock_relation is not None else "bypassed"
                        ),
                        "bypass": True,
                        "fake": mock_relation is not None,
                        "mock_relation_applied": mock_relation is not None and result.quote_matches,
                        "result": result.model_dump(mode="json"),
                    }
                )
            _write_json(artifact_dir / "verification_results.json", verification_artifact)
            cache.put(
                cache.key("verification", fixture_hash, "", "fixture-mock", "v1"),
                {
                    "mode": "offline_mock",
                    "bypass": True,
                    "fake": bool(mock_relations),
                    "results": verification_artifact,
                },
            )
            stage_statuses["quote_verification"] = _stage_record(
                StageStatus.completed, verification_ref
            )
        except Exception as exc:
            stage_statuses["quote_verification"] = _stage_record(
                StageStatus.error, error=str(exc)
            )
            deferred_claim_ids = [claim.claim_id for claim in claims]

        search_results: list[dict[str, Any]] = []
        search_ref = "artifacts/search_candidates.json"
        try:
            index_path = run_dir / "index.sqlite3"
            indexed_sections = reindex(vault_path, index_path)
            if query.strip():
                search_results = search(index_path, query)
            _write_json(
                artifact_dir / "search_candidates.json",
                {
                    "mode": "offline",
                    "bypass": True,
                    "indexed_sections": indexed_sections,
                    "candidates": search_results,
                },
            )
            cache.put(
                cache.key("search", fixture_hash, "", "fts5", "v1"),
                {
                    "mode": "offline",
                    "bypass": True,
                    "indexed_sections": indexed_sections,
                    "candidates": search_results,
                },
            )
            stage_statuses["vault_search"] = _stage_record(
                StageStatus.completed if query.strip() else StageStatus.deferred,
                search_ref,
            )
        except Exception as exc:
            stage_statuses["vault_search"] = _stage_record(StageStatus.error, error=str(exc))

        proposal_path: Path | None = None
        if stage_statuses["quote_verification"].status is StageStatus.error:
            proposal_status = StageStatus.deferred
            deferred_claim_ids = [claim.claim_id for claim in claims]
        elif proposed_claim_ids:
            proposal_path = run_dir / "proposal.md"
            proposal_path.write_bytes(
                _proposal(
                    claims,
                    {item["claim_id"]: item for item in verification_artifact},
                    source_by_id,
                    search_results,
                ).encode("utf-8")
            )
            proposal_status = StageStatus.completed
        else:
            proposal_status = StageStatus.deferred

        proposal_decisions = {
            "mode": "offline_mock",
            "bypass": True,
            "fake": bool(mock_relations),
            "proposed_claim_ids": proposed_claim_ids,
            "deferred_claim_ids": deferred_claim_ids,
            "proposal_ref": "proposal.md" if proposal_path else None,
            "candidate_paths_are_suggestions": True,
        }
        proposal_ref = "artifacts/proposal_decisions.json"
        _write_json(artifact_dir / "proposal_decisions.json", proposal_decisions)
        cache.put(
            cache.key("proposal", fixture_hash, "", "offline", "v1"),
            proposal_decisions,
        )
        proposal_refs = [proposal_ref]
        if proposal_path:
            proposal_refs.append("proposal.md")
        stage_statuses["proposal"] = _stage_record(proposal_status, *proposal_refs)

        manifest = RunManifest(
            run_id=run_id,
            created_at=created_at,
            code_version="offline-pilot-v1",
            model_versions={"semantic_assessment": "fixture-mock-only"},
            policy_version="offline-pilot-v1",
            input_hashes={"fixture": fixture_hash},
            stages=stage_statuses,
            publication_plan_ref=None,
        )
        cache.persist_manifest(manifest)

    statuses = {name: record.status.value for name, record in stage_statuses.items()}
    overall_status = (
        "error"
        if StageStatus.error in (record.status for record in stage_statuses.values())
        else "completed"
    )
    return {
        "run_id": run_id,
        "run_dir": str(run_dir),
        "status": overall_status,
        "stages": statuses,
        "proposed_claim_ids": proposed_claim_ids,
        "deferred_claim_ids": deferred_claim_ids,
        "search_candidates": search_results,
        "proposal_path": str(proposal_path) if proposal_path else None,
    }
