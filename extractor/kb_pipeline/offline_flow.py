"""One offline vertical run: cache -> sources -> context -> gates -> claims ->
verification -> integration -> NotePatch -> read-only publication plan.

This module orchestrates stages that already exist; it does not reimplement them.
Code owns order, thresholds, routing, validation and the decision to stop.
Providers are injected explicitly: nothing here silently substitutes a fake for a
live provider, and every artifact records which provider mode produced it.

Nothing in this module writes into the vault. The vault is read (retrieval index
built in the workspace, ``plan_publication`` diff) and never patched.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import yaml

from . import local_gate
from .assemble import AssembledPost
from .claim_extraction import extract_claim_proposals
from .context import build_context
from .filtering import assess_filter
from .integration import (
    ALLOWED_CREATE_DIRS,
    IntegrationAdvice,
    NoteView,
    SectionCandidate,
    integrate_claims,
)
from .live_jev import compute_context_hash, compute_input_hash
from .local_gate import category_from_clm, decide_clm, screen_focus
from .publication import plan_publication
from .retrieval import reindex, search
from .schemas import (
    SCHEMA_VERSION,
    Claim,
    ContextBundle,
    FilterDecision,
    RunManifest,
    SourceRecord,
    StageRecord,
    StageStatus,
    VerificationRelation,
)
from .stage_cache import StageCache
from .thresholds import resolve_thresholds, thresholds_manifest

CODE_VERSION = "offline-flow-v1"
POLICY_VERSION = "offline-flow-v1"
PROMPT_VERSION = "v1"

STAGES = (
    "input",
    "context",
    "local_gate",
    "clm_gate",
    "jev_evaluate",
    "category",
    "claim_extraction",
    "verification",
    "integration",
    "publication_plan",
)

_SEMANTIC_CALLABLE = "provider"
_TOPIC_OPTIONS = ("compaction", "evals", "harness", "other")


def _topic_probabilities(topic: str, *, confidence: float = 0.9) -> dict[str, float]:
    """Routing-only topic distribution the existing checker accepts (sums to one)."""
    labels = set(_TOPIC_OPTIONS)
    if topic not in labels:
        raise ValueError(f"fake topic {topic!r} is not one of {sorted(labels)}")
    others = sorted(labels - {topic})
    share = (1.0 - confidence) / len(others) if others else 0.0
    values = {label: share for label in others}
    values[topic] = confidence
    return {label: round(values[label], 6) for label in sorted(labels)}


class _StageFailure(RuntimeError):
    """A provider stage failed. Recorded as ``error``, never as ``defer``."""


def _claim_context_hash(claim: Claim, context_hash: str) -> str:
    """Context hash extended with the claim text, so each claim keys separately."""
    payload = json.dumps(
        {"context": context_hash, "claim": claim.claim_id, "text": claim.text},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Providers
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class FlowProviders:
    """Explicitly injected providers. ``mode`` is recorded in every artifact.

    ``mode`` is ``"fake-offline"`` for fixture/fake providers and ``"live"`` for
    real network providers. There is no default value: a caller must say which
    one it is passing.
    """

    mode: str
    local_filter: Callable[[str], dict]
    categorize: Callable[[str], dict]
    jev_evaluate: Callable[[ContextBundle], dict]
    extract_claims: Callable[[ContextBundle, str], Sequence[Claim]]
    advisor: Callable[..., Any]
    semantic_check: Callable[..., tuple[VerificationRelation, str]] | None = None
    model_versions: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.mode not in ("fake-offline", "live"):
            raise ValueError(
                "FlowProviders.mode must be an explicit 'fake-offline' or 'live', "
                f"got {self.mode!r}"
            )


def fake_providers(
    *,
    clm_answers: Mapping[str, float] | None = None,
    promo_answers: Mapping[str, float] | None = None,
    category: str | None = None,
    category_confidence: float = 0.9,
    jev_answers: Mapping[str, float] | None = None,
    topic: str = "other",
    claim_mode: str = "heuristic",
    relations: Mapping[str, str] | None = None,
) -> FlowProviders:
    """Deterministic offline providers. Everything they return is a fixture value.

    They reproduce *behaviour* on fixtures only. No claim about real model
    quality, real thresholds or real relations follows from them.
    """
    answers = {
        "focus_claim": 0.85,
        "promotion": 0.05,
        **dict(clm_answers or {}),
        **dict(promo_answers or {}),
    }

    def local_filter(text: str) -> dict:
        return {
            "model": "fake-clm",
            "answers": {
                "focus_claim": {"type": "noul", "noul": float(answers["focus_claim"])},
                "promotion": {"type": "noul", "noul": float(answers["promotion"])},
            },
        }

    def categorize(text: str) -> dict:
        chosen = category or "Pojęcia"
        return {
            "model": "fake-clm",
            "answers": {
                "category": {
                    "type": "choice",
                    "choice": chosen,
                    "confidence": float(category_confidence),
                }
            },
        }

    jev = {"engineering_value": 0.85, "context_sufficient": 0.9, **dict(jev_answers or {})}

    def jev_evaluate(bundle: ContextBundle) -> dict:
        return {
            "model": "fake-jev",
            "answers": {
                "engineering_value": {"type": "noul", "noul": float(jev["engineering_value"])},
                "context_sufficient": {"type": "noul", "noul": float(jev["context_sufficient"])},
                "topic": {
                    "type": "choice",
                    "choice": topic,
                    "confidence": 0.9,
                    "probabilities": _topic_probabilities(topic),
                },
            },
        }

    def extract_claims(bundle: ContextBundle, kind_hint: str | None = None) -> Sequence[Claim]:
        if claim_mode != "heuristic":
            raise ValueError(
                "fake_providers only implements claim_mode='heuristic'; "
                f"got {claim_mode!r}"
            )
        return extract_claim_proposals(bundle.focus, bundle)

    relation_map = dict(relations or {})

    def semantic_check(
        claim: Claim, sources: Mapping[str, SourceRecord]
    ) -> tuple[VerificationRelation, str]:
        relation = VerificationRelation(relation_map.get(claim.claim_id, "supports"))
        return relation, "Fake offline semantic relation; not a real assessment."

    def advisor(claim: Claim, candidates: Sequence[SectionCandidate], notes: Mapping[str, NoteView]):
        body_lines = [claim.text.strip(), ""]
        for evidence in claim.evidence:
            body_lines.append(f"> {evidence.quote}")
        if claim.conditions:
            body_lines.extend(["", "Warunki:"] + [f"- {item}" for item in claim.conditions])
        if claim.limitations:
            body_lines.extend(["", "Ograniczenia:"] + [f"- {item}" for item in claim.limitations])
        body_lines.extend(
            [
                "",
                "Status: the claim is source-supported and not independently validated "
                "(fake offline provider).",
            ]
        )
        if candidates:
            target = candidates[0]
            return IntegrationAdvice(
                operation="enrich",
                target_note_id=target.note_id,
                relative_path=target.relative_path,
                section=target.heading,
                rationale=f"Fake advisor: enrich managed note {target.note_id}",
                proposed_body="\n".join(body_lines),
            )
        return IntegrationAdvice(
            operation="create",
            relative_path=None,
            rationale="Fake advisor: no candidate note, propose a new managed note",
            proposed_body="\n".join(body_lines),
        )

    return FlowProviders(
        mode="fake-offline",
        local_filter=local_filter,
        categorize=categorize,
        jev_evaluate=jev_evaluate,
        extract_claims=extract_claims,
        advisor=advisor,
        semantic_check=semantic_check,
        model_versions={
            "clm": "fake-clm",
            "jev": "fake-jev",
            "extraction": "heuristic-offline",
            "semantic": "fake-relation",
            "advisor": "fake-advisor",
        },
    )


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _write_json(path: Path, value: Any) -> None:
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((payload + "\n").encode("utf-8"))


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _focus_gate(record: SourceRecord) -> tuple[str, str] | None:
    """Reuse the existing local gate with author text only."""
    return screen_focus(
        AssembledPost(
            source_id=record.source_id,
            author=record.author,
            url=record.url or "",
            published_at=record.published_at.isoformat() if record.published_at else None,
            is_reply=record.reply_to_id is not None,
            document=record.text,
            focus_evidence=record.text,
        )
    )


def _frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    try:
        data = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return {}, text
    return (data if isinstance(data, dict) else {}), text[end + 4 :]


def load_managed_notes(vault: Path) -> dict[str, NoteView]:
    """Read-only view of kb-managed notes inside the publisher allowlist.

    Manual notes are never treated as integration targets: only notes whose
    frontmatter explicitly declares ``kb_managed: true`` are returned.
    """
    vault_path = Path(vault).resolve()
    notes: dict[str, NoteView] = {}
    for directory in sorted(ALLOWED_CREATE_DIRS):
        base = vault_path / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.is_symlink():
                continue
            raw = path.read_bytes()
            data, _ = _frontmatter(raw.decode("utf-8", errors="replace"))
            if not data.get("kb_managed"):
                continue
            note_id = str(data.get("note_id") or path.stem)
            notes[note_id] = NoteView(
                note_id=note_id,
                relative_path=path.relative_to(vault_path).as_posix(),
                content=raw.decode("utf-8"),
                content_hash=hashlib.sha256(raw).hexdigest(),
                managed=True,
            )
    return notes


def _to_candidates(rows: Sequence[Mapping[str, Any]]) -> list[SectionCandidate]:
    return [
        SectionCandidate(
            note_id=str(row["note_id"]),
            relative_path=str(row["path"]),
            heading=str(row["heading"]),
            anchor=str(row["anchor"]),
            snippet=str(row["snippet"]),
            score=float(row["score"]),
        )
        for row in rows
    ]


# --------------------------------------------------------------------------- #
# Cached provider calls
# --------------------------------------------------------------------------- #
class _CallLedger:
    """Counts real provider calls and records replays (cache hits)."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.replays: list[str] = []

    def record(self, stage: str, replayed: bool) -> None:
        (self.replays if replayed else self.calls).append(stage)

    @property
    def provider_calls(self) -> int:
        return len(self.calls)

    def breakdown(self) -> dict[str, Any]:
        return {
            "calls": sorted(self.calls),
            "replays": sorted(self.replays),
            "per_stage": {
                stage: {
                    "calls": self.calls.count(stage),
                    "replays": self.replays.count(stage),
                }
                for stage in sorted(set(self.calls) | set(self.replays))
            },
        }


# --------------------------------------------------------------------------- #
# The flow
# --------------------------------------------------------------------------- #
def run_offline_flow(
    *,
    source: SourceRecord,
    lookup: Callable[[str], SourceRecord | None],
    vault: Path,
    workspace: Path,
    providers: FlowProviders,
    run_id: str,
    thresholds: Mapping[str, float] | None = None,
    index_path: Path | None = None,
) -> dict[str, Any]:
    """Run stages 1-10 for one source. Returns a JSON-serialisable report."""
    limits = resolve_thresholds(thresholds)
    vault_path = Path(vault).resolve(strict=True)
    workspace_path = Path(workspace).resolve()
    if _is_within(workspace_path, vault_path) or workspace_path == vault_path:
        raise ValueError("Workspace must live outside the vault")
    run_dir = workspace_path / "runs" / run_id
    if _is_within(run_dir.resolve(strict=False), vault_path):
        raise ValueError("Run directory must live outside the vault")
    artifact_dir = run_dir / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    index = Path(index_path) if index_path is not None else run_dir / "index.sqlite3"

    ledger = _CallLedger()
    stages: dict[str, StageRecord] = {}
    counters = {"extract": 0, "reject": 0, "defer": 0, "error": 0}
    provider_note = {"mode": providers.mode, "fake": providers.mode == "fake-offline"}
    cache_ref = StageCache(workspace_path)

    def cached(stage: str, input_hash: str, context_hash: str, model: str, produce):
        """One provider call, or a replay from cache.

        The key carries stage, input hash, context hash, model, prompt version and
        schema version only. Thresholds, decisions, budget, run id and wall-clock
        time are deliberately outside it, so changing a threshold recomputes the
        decision from the cached raw answer instead of paying for a new call.
        """
        key = cache_ref.key(stage, input_hash, context_hash, model, PROMPT_VERSION, SCHEMA_VERSION)
        payload = cache_ref.get(key)
        replayed = payload is not None
        if replayed:
            value = payload["value"]
        else:
            value = produce()
            cache_ref.put(key, {"provider": provider_note, "value": value})
        ledger.record(stage, replayed)
        return value, replayed, key

    def stage_error(name: str, message: str) -> None:
        stages[name] = StageRecord(status=StageStatus.error, error=message)

    def finish(status: str, reason: str, *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        counters[status] = counters.get(status, 0) + 1
        manifest = RunManifest(
            run_id=run_id,
            created_at=datetime.now(timezone.utc),
            code_version=CODE_VERSION,
            prompt_versions={"offline_flow": PROMPT_VERSION},
            model_versions=dict(providers.model_versions),
            policy_version=POLICY_VERSION,
            input_hashes={
                "source_id": source.source_id,
                "source_content_hash": source.content_hash,
                "vault": vault_path.name,
            },
            stages=stages,
            token_count=None,
            cost=None,
            publication_plan_ref=stages.get("publication_plan").artifact_refs[0]
            if stages.get("publication_plan")
            and stages["publication_plan"].artifact_refs
            else None,
        )
        summary = {
            "run_id": run_id,
            "run_dir": str(run_dir),
            "source_id": source.source_id,
            "status": status,
            "reason": reason,
            "stages": {name: record.status.value for name, record in stages.items()},
            "counters": dict(counters),
            "provider_mode": providers.mode,
            "provider_calls": ledger.provider_calls,
            "provider_replays": len(ledger.replays),
            "provider_stages": ledger.breakdown(),
            "replay": ledger.provider_calls == 0,
            "thresholds": thresholds_manifest(limits),
            "vault_written": False,
            "fake_providers": provider_note,
            **(extra or {}),
        }
        _write_json(run_dir / "summary.json", summary)
        _write_json(run_dir / "manifest.json", json.loads(manifest.model_dump_json()))
        cache_ref.persist_manifest(manifest)
        cache_ref.close()
        summary["manifest_ref"] = str(run_dir / "manifest.json")
        return summary

    def _flow(_lookup: Callable[[str], SourceRecord | None]):
        # ---------------- stage 1: input ----------------
        input_ref = "artifacts/source_record.json"
        _write_json(
            artifact_dir / "source_record.json",
            {"provider": provider_note, "record": json.loads(source.model_dump_json())},
        )
        stages["input"] = StageRecord(status=StageStatus.completed, artifact_refs=[input_ref])
        input_hash = compute_input_hash(source.source_id, source.content_hash)

        # ---------------- stage 2: context ----------------
        context_ref = "artifacts/context_bundle.json"
        try:
            bundle = build_context(source, _lookup)
        except Exception as exc:  # noqa: BLE001 - stage failure is an error, not a defer
            stage_error("context", str(exc))
            return finish("error", "context_failed")
        context_hash = compute_context_hash(bundle)
        _write_json(
            artifact_dir / "context_bundle.json",
            {
                "provider": provider_note,
                "focus": {
                    "source_id": bundle.focus.source_id,
                    "author": bundle.focus.author,
                    "text": bundle.focus.text,
                    "published_at": (
                        bundle.focus.published_at.isoformat() if bundle.focus.published_at else None
                    ),
                },
                "related": [
                    {
                        "role": item.role,
                        "provenance": item.provenance,
                        "source_id": item.source.source_id,
                        "author": item.source.author,
                        "text": item.source.text,
                    }
                    for item in bundle.related
                ],
                "missing_ids": bundle.missing_ids,
                "context_status": bundle.context_status.value,
                "context_hash": context_hash,
            },
        )
        stages["context"] = StageRecord(status=StageStatus.completed, artifact_refs=[context_ref])

        # ---------------- stage 3: local gate (code, no provider) ----------------
        screened = _focus_gate(bundle.focus)
        if screened is not None:
            status, reason = screened
            stages["local_gate"] = StageRecord(
                status=StageStatus.rejected if status == "reject" else StageStatus.deferred,
                error=None,
                artifact_refs=["artifacts/gate_decisions.json"],
            )
            _write_json(
                artifact_dir / "gate_decisions.json",
                {"local_gate": {"status": status, "reason": reason}, "provider": provider_note},
            )
            return finish(status, reason)
        stages["local_gate"] = StageRecord(
            status=StageStatus.completed, artifact_refs=["artifacts/gate_decisions.json"]
        )
        _write_json(
            artifact_dir / "gate_decisions.json",
            {"local_gate": {"status": "passed"}, "provider": provider_note},
        )

        # ---------------- stage 4: CLM on author text ----------------
        try:
            clm_response, replayed, clm_key = cached(
                "clm_gate",
                input_hash,
                "",
                providers.model_versions.get("clm", "clm"),
                lambda: providers.local_filter(bundle.focus.text),
            )
        except Exception as exc:  # noqa: BLE001 - provider failure is an error, never a defer
            stage_error("clm_gate", f"clm_failed: {exc}")
            return finish("error", f"clm_failed: {exc}")
        try:
            clm_status, clm_reason = decide_clm(
                clm_response,
                focus_claim_reject=limits["focus_claim_reject"],
                promotion_reject=limits["promotion_reject"],
            )
        except Exception as exc:  # noqa: BLE001
            stage_error("clm_gate", str(exc))
            return finish("error", f"clm_failed: {exc}")
        _write_json(
            artifact_dir / "gate_decisions.json",
            {
                "local_gate": {"status": "passed"},
                "clm_gate": {
                    "status": clm_status,
                    "reason": clm_reason,
                    "answers": clm_response.get("answers"),
                },
                "provider": provider_note,
                "thresholds": {"focus_claim_reject": limits["focus_claim_reject"],
                               "promotion_reject": limits["promotion_reject"]},
            },
        )
        if clm_status != "keep":
            stages["clm_gate"] = StageRecord(
                status=StageStatus.rejected if clm_status == "reject" else StageStatus.deferred
            )
            return finish(clm_status, clm_reason)
        stages["clm_gate"] = StageRecord(
            status=StageStatus.completed, artifact_refs=["artifacts/gate_decisions.json"]
        )

        # ---------------- stage 5: Jev ----------------
        def _produce_jev():
            try:
                return providers.jev_evaluate(bundle)
            except Exception as exc:  # noqa: BLE001 - provider failure is an error, never a defer
                raise _StageFailure(f"jev_failed: {exc}") from exc

        try:
            jev_response, replayed, jev_key = cached(
                "jev_evaluate",
                input_hash,
                context_hash,
                providers.model_versions.get("jev", "jev"),
                _produce_jev,
            )
        except _StageFailure as exc:
            stage_error("jev_evaluate", str(exc))
            return finish("error", str(exc))
        except Exception as exc:  # noqa: BLE001
            stage_error("jev_evaluate", str(exc))
            return finish("error", f"jev_failed: {exc}")
        try:
            assessment = assess_filter(
                bundle,
                jev_response,
                usefulness_threshold=limits["jev_usefulness"],
                context_threshold=limits["jev_context"],
                question_version=PROMPT_VERSION,
                policy_version=POLICY_VERSION,
                raw_response_ref=jev_key,
            )
        except Exception as exc:  # noqa: BLE001
            stage_error("jev_evaluate", str(exc))
            return finish("error", f"jev_invalid_response: {exc}")
        jev_ref = "artifacts/jev_assessment.json"
        _write_json(
            artifact_dir / "jev_assessment.json",
            {
                "provider": provider_note,
                "raw_response_ref": jev_key,
                "answers": jev_response.get("answers"),
                "assessment": assessment.model_dump(mode="json"),
                "thresholds": {
                    "jev_usefulness": limits["jev_usefulness"],
                    "jev_context": limits["jev_context"],
                },
            },
        )
        stages["jev_evaluate"] = StageRecord(
            status=StageStatus.completed, artifact_refs=[jev_ref]
        )
        if assessment.decision is not FilterDecision.extract:
            outcome = assessment.decision.value
            return finish(
                outcome,
                assessment.reason_code,
                extra={"assessment": assessment.model_dump(mode="json")},
            )

        # ---------------- stage 6: category ----------------
        category_response, _, _ = cached(
            "category",
            input_hash,
            "",
            providers.model_versions.get("clm", "clm"),
            lambda: providers.categorize(bundle.focus.text),
        )
        try:
            category = category_from_clm(
                category_response, category_confidence=limits["category_confidence"]
            )
        except ValueError as exc:
            stages["category"] = StageRecord(status=StageStatus.deferred, error=str(exc))
            return finish("defer", f"category: {exc}")
        stages["category"] = StageRecord(status=StageStatus.completed)

        # ---------------- stage 7: claim extraction ----------------
        claims_ref = "artifacts/claims.json"
        try:
            claim_payload, _, _ = cached(
                "claim_extraction",
                input_hash,
                context_hash,
                providers.model_versions.get("extraction", "extraction"),
                lambda: [
                    claim.model_dump(mode="json")
                    for claim in providers.extract_claims(bundle, category)
                ],
            )
            claims = [Claim.model_validate(item) for item in claim_payload]
        except _StageFailure as exc:
            stage_error("claim_extraction", str(exc))
            return finish("error", str(exc))
        except Exception as exc:  # noqa: BLE001
            stage_error("claim_extraction", str(exc))
            return finish("error", f"claim_extraction_failed: {exc}")
        foreign_quotes = [
            (claim.claim_id, evidence.quote)
            for claim in claims
            for evidence in claim.evidence
            if evidence.source_id != bundle.focus.source_id
            or not _quote_in_text(evidence.quote, bundle.focus.text)
        ]
        if foreign_quotes:
            stages["claim_extraction"] = StageRecord(
                status=StageStatus.rejected,
                error=f"quote_not_in_author_text: {foreign_quotes[0][0]}",
            )
            return finish("reject", "quote_not_in_author_text")
        _write_json(
            artifact_dir / "claims.json",
            {
                "provider": provider_note,
                "category": category,
                "claims": [claim.model_dump(mode="json") for claim in claims],
            },
        )
        stages["claim_extraction"] = StageRecord(
            status=StageStatus.completed if claims else StageStatus.deferred,
            artifact_refs=[claims_ref],
        )
        if not claims:
            return finish("defer", "no_claims_extracted")

        # ---------------- stage 8: verification ----------------
        verification_ref = "artifacts/verification_results.json"
        from .verification import verify_claim

        focus_only = {bundle.focus.source_id: bundle.focus}
        semantic_model = providers.model_versions.get("semantic", "semantic")

        def semantic_check_for(claim: Claim):
            """One semantic relation call per claim, or a replay from cache."""
            if providers.semantic_check is None:
                return None
            payload, _, _ = cached(
                "semantic_check",
                input_hash,
                _claim_context_hash(claim, context_hash),
                semantic_model,
                lambda: list(providers.semantic_check(claim, focus_only)),
            )
            relation, reason = VerificationRelation(payload[0]), payload[1]
            return lambda _claim, _sources: (relation, reason)

        try:
            results = [
                verify_claim(claim, focus_only, semantic_check_for(claim)) for claim in claims
            ]
        except Exception as exc:  # noqa: BLE001
            stage_error("verification", str(exc))
            return finish("error", f"verification_failed: {exc}")
        eligible = [
            claim
            for claim, result in zip(claims, results)
            if result.quote_matches
            and result.source_supported
            and result.relation is VerificationRelation.supports
        ]
        _write_json(
            artifact_dir / "verification_results.json",
            {
                "provider": provider_note,
                "semantic_checker": providers.semantic_check is not None,
                "results": [
                    {**result.model_dump(mode="json"), "status": (
                        "completed"
                        if claim in eligible
                        else ("deferred" if result.quote_matches else "rejected")
                    )}
                    for claim, result in zip(claims, results)
                ],
            },
        )
        stages["verification"] = StageRecord(
            status=StageStatus.completed if eligible else StageStatus.deferred,
            artifact_refs=[verification_ref],
        )
        if not eligible:
            return finish("defer", "no_source_supported_claims")

        # ---------------- stage 9: retrieval + integration -> NotePatch ----------
        integration_ref = "artifacts/integration_decisions.json"
        advisor_model = providers.model_versions.get("advisor", "advisor")
        advisor_calls: list[str] = []

        def cached_advisor(claim: Claim, claim_candidates, notes_map):
            key_context = hashlib.sha256(
                json.dumps(
                    {
                        "candidates": [
                            {"note_id": item.note_id, "relative_path": item.relative_path}
                            for item in claim_candidates
                        ],
                        "notes": {
                            note_id: view.content_hash for note_id, view in notes_map.items()
                        },
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest()

            def _produce():
                advice = providers.advisor(claim, claim_candidates, notes_map)
                return json.loads(advice.model_dump_json())

            payload, _, _ = cached(
                "advisor",
                _claim_context_hash(claim, context_hash),
                key_context,
                advisor_model,
                _produce,
            )
            advisor_calls.append(claim.claim_id)
            return IntegrationAdvice.model_validate(payload)

        try:
            indexed = reindex(vault_path, index)
            notes = load_managed_notes(vault_path)
            candidates_by_claim = {
                claim.claim_id: _to_candidates(search(index, claim.text))
                for claim in eligible
            }
            decisions = integrate_claims(
                eligible, results, candidates_by_claim, notes, cached_advisor
            )
        except Exception as exc:  # noqa: BLE001
            stage_error("integration", str(exc))
            return finish("error", f"integration_failed: {exc}")
        patches = [decision.patch for decision in decisions if decision.patch is not None]
        _write_json(
            artifact_dir / "integration_decisions.json",
            {
                "provider": provider_note,
                "indexed_sections": indexed,
                "advisor_claims": advisor_calls,
                "decisions": [decision.model_dump(mode="json") for decision in decisions],
            },
        )
        proposal_path = artifact_dir / "proposed_section.md"
        proposal_path.parent.mkdir(parents=True, exist_ok=True)
        proposal_path.write_bytes(_render_proposal(eligible, decisions, notes).encode("utf-8"))
        stages["integration"] = StageRecord(
            status=StageStatus.completed if patches else StageStatus.deferred,
            artifact_refs=[integration_ref, "artifacts/proposed_section.md"],
        )

        # ---------------- stage 10: read-only publication plan --------------
        plan_ref = "artifacts/publication_plan.json"
        try:
            plan = plan_publication([patch.model_dump(mode="json") for patch in patches], vault_path)
            _write_json(
                artifact_dir / "publication_plan.json",
                {
                    "provider": provider_note,
                    "mode": "plan_only",
                    "applied": False,
                    "plan": json.loads(plan.model_dump_json()),
                    "diff": _render_diff(plan, notes),
                },
            )
            stages["publication_plan"] = StageRecord(status=StageStatus.completed, artifact_refs=[plan_ref])
        except Exception as exc:  # noqa: BLE001
            stage_error("publication_plan", str(exc))
            return finish("error", f"publication_plan_failed: {exc}", extra={"patches": [p.model_dump(mode="json") for p in patches]})

        return finish(
            "extract",
            "offline_vertical_flow",
            extra={
                "category": category,
                "claim_ids": [claim.claim_id for claim in eligible],
                "patch_count": len(patches),
                "patches": [patch.model_dump(mode="json") for patch in patches],
                "publication_plan_ref": plan_ref,
            },
        )

    try:
        return _flow(lookup)
    finally:
        cache_ref.close()


def _quote_in_text(quote: str, text: str) -> bool:
    from .verification import _matches_quote  # reuse one matcher, not a second rule

    return _matches_quote(text, quote, is_slice=False)


def _render_proposal(
    claims: Sequence[Claim],
    decisions: Sequence[Any],
    notes: Mapping[str, NoteView],
) -> str:
    lines = [
        "# Proposed note section (offline staging, not published)",
        "",
        f"> OFFLINE {claims and ''}FAKE PROVIDERS — source-supported, not independently validated.",
        "",
    ]
    for decision in decisions:
        lines.append(f"## {decision.operation.value}: {', '.join(decision.claim_ids)}")
        lines.append("")
        lines.append(f"Rationale: {decision.rationale}")
        lines.append("")
        if decision.patch is None:
            lines.append("No NotePatch proposed.")
            lines.append("")
            continue
        patch = decision.patch
        lines.append(f"- note_id: `{patch.note_id}`")
        lines.append(f"- relative_path: `{patch.relative_path}`")
        lines.append(f"- section: `{patch.section}`")
        lines.append(f"- base_hash: `{patch.base_hash}`")
        lines.append("")
        lines.append(patch.proposed_content)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _render_diff(plan: Any, notes: Mapping[str, NoteView]) -> str:
    lines = ["# Read-only publication diff", "", "No file in the vault is written by this run.", ""]
    for write in plan.writes:
        known = write.note_id in notes
        lines.append(f"## {write.relative_path}")
        lines.append("")
        lines.append(f"- action: {write.action}")
        lines.append(f"- note_id: {write.note_id}")
        lines.append(f"- base_hash: {write.base_hash}")
        lines.append(f"- proposed_hash: {write.proposed_hash}")
        lines.append(f"- content_visible_in_run_view: {known}")
        lines.append("")
    if not plan.writes:
        lines.append("No writes planned.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
