"""Durable claim identity, separate from claim revisions and source revisions.

Plan §1.8: a claim's identity must survive a revision of its source. A hash of
the normalised claim text does not achieve that — a model paraphrases on every
run, so the same meaning gets a new identifier. This module therefore keeps:

* a **registry** of durable claim ids, granted once at the first write;
* **claim revisions** (what the claim says), stored per revision;
* **source revisions** (which pinned revision of which source it was read from),
  stored beside but not inside the claim identity;
* **unresolved candidates** for anything that matches ambiguously.

Matching uses the source id and the *normalised quote text*, never the offsets:
a shifted fragment still matches, so a move inside the text cannot mint a new
identity. When the same evidence yields a claim whose meaning fields differ
(text, kind, technology), the two records are **kept as candidates** and neither
is merged automatically. Semantic deduplication is not guaranteed here and the
registry says so in every report it writes.

Storage is one atomically rewritten JSON registry in the workspace. It is
operational state: nothing here is written into the vault.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from .schemas import Claim

# Claim fields that decide *what the claim is*. A difference here is not a
# revision of the same claim, it is a different reading of the same evidence.
IDENTITY_FIELDS = ("text", "kind", "technology")
# Fields that decide the *revision* of a claim: same meaning, different wording
# of the conditions, limitations, scope or version.
REVISION_FIELDS = ("text", "kind", "technology", "scope", "conditions", "limitations")

_WHITESPACE = re.compile(r"\s+")

SEMANTIC_DEDUP_GUARANTEE = (
    "not guaranteed: an unmatched paraphrase is only a merge candidate, and an "
    "ambiguous match keeps both records unresolved"
)


def normalise_text(text: str) -> str:
    """NFKC, casefolded, whitespace-collapsed. Used for matching, not for display."""
    return _WHITESPACE.sub(" ", unicodedata.normalize("NFKC", text).casefold()).strip()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def evidence_key(source_id: str, quote: str) -> str:
    """Matching key for one evidence item: source identity plus quote content.

    Offsets are deliberately excluded, so moving a quote inside the source text
    does not create a new identity.
    """
    return f"{source_id}|{_sha256(normalise_text(quote))}"


def quote_key(quote: str) -> str:
    """Cross-source matching key, used to surface merge candidates only."""
    return _sha256(normalise_text(quote))


def _field(claim: Claim, name: str) -> Any:
    value = getattr(claim, name)
    if name == "text":
        return normalise_text(value)
    if name in ("conditions", "limitations"):
        return sorted(normalise_text(item) for item in value)
    if value is None:
        return None
    # Enums compare by their serialised value, so a stored revision and a live
    # claim body always agree.
    return normalise_text(str(getattr(value, "value", value)))


def identity_body(claim: Claim) -> dict[str, Any]:
    return {name: _field(claim, name) for name in IDENTITY_FIELDS}


def revision_body(claim: Claim) -> dict[str, Any]:
    return {name: _field(claim, name) for name in REVISION_FIELDS}


def _digest(payload: Any) -> str:
    return _sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class IdentityAssignment:
    """What happened to one extracted claim when it met the registry."""

    claim: Claim
    provider_claim_id: str
    status: str  # new | unchanged | revision | ambiguous
    reason: str
    matched_claim_id: str | None = None
    revision: int = 1
    candidates: tuple[str, ...] = ()
    merge_candidates: tuple[str, ...] = ()

    def to_dict(self, *, transitions: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "provider_claim_id": self.provider_claim_id,
            "claim_id": self.claim.claim_id,
            "revision": self.revision,
            "unresolved_candidates": list(self.candidates),
            "merge_candidates": list(self.merge_candidates),
        }
        if transitions:
            # What this invocation did. It differs between the first write and a
            # replay of the same claim, so it belongs in the run summary and the
            # checkpoints, not in the byte-stable artifact.
            payload.update(
                {
                    "status": self.status,
                    "reason": self.reason,
                    "matched_claim_id": self.matched_claim_id,
                }
            )
        return payload


class ClaimIdentityRegistry:
    """Durable claim ids with revisions, kept in the workspace."""

    def __init__(self, workspace: Path) -> None:
        self.path = Path(workspace).resolve() / "identity" / "registry.json"
        self._data: dict[str, Any] = {
            "claims": {},
            "notes": {},
            "claims_by_key": {},
            "claims_by_quote": {},
            "sequence": 0,
        }
        if self.path.is_file():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                loaded = None
            if isinstance(loaded, dict) and "claims" in loaded:
                for name in ("claims", "notes", "claims_by_key", "claims_by_quote"):
                    value = loaded.get(name)
                    if isinstance(value, dict):
                        self._data[name] = value
                self._data["sequence"] = int(loaded.get("sequence", 0))

    # ------------------------------------------------------------------ io --
    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            self._data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False
        )
        temporary = self.path.with_suffix(".json.tmp")
        temporary.write_bytes((payload + "\n").encode("utf-8"))
        os.replace(temporary, self.path)

    def close(self) -> None:
        self._write()

    def __enter__(self) -> "ClaimIdentityRegistry":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    # ------------------------------------------------------------- queries --
    def claims(self) -> dict[str, Any]:
        return self._data["claims"]

    def notes(self) -> dict[str, Any]:
        return self._data["notes"]

    def _next_claim_id(self) -> str:
        self._data["sequence"] = int(self._data["sequence"]) + 1
        return f"clm-{self._data['sequence']:08d}"

    def _candidates_for(self, claim: Claim) -> set[str]:
        """Claim ids registered under **every** evidence key of the claim."""
        keys = {evidence_key(item.source_id, item.quote) for item in claim.evidence}
        if not keys:
            return set()
        per_key = [set(self._data["claims_by_key"].get(key, [])) for key in sorted(keys)]
        return set.intersection(*per_key)

    def _cross_source_candidates(self, claim: Claim) -> set[str]:
        """Same quote, different source: a merge candidate, never a merge."""
        found: set[str] = set()
        for item in claim.evidence:
            found.update(self._data["claims_by_quote"].get(quote_key(item.quote), []))
        found.difference_update(self._candidates_for(claim))
        return found

    # ------------------------------------------------------------ mutation --
    def _record_revision(
        self,
        claim_id: str,
        claim: Claim,
        source_revisions: dict[str, str],
        *,
        run_id: str,
        body: dict[str, Any],
    ) -> int:
        record = self._data["claims"].setdefault(
            claim_id,
            {
                "claim_id": claim_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "created_in_run": run_id,
                "current_revision": 0,
                "revisions": [],
            },
        )
        body_hash = _digest(body)
        for existing in record["revisions"]:
            if existing["body_hash"] == body_hash:
                # Same claim, same wording: the recorded revision is replayed
                # instead of being duplicated. Which runs touched it is kept in
                # the run checkpoints, so the registry itself stays byte-stable.
                return int(existing["revision"])
        revision = int(record["current_revision"]) + 1
        record["revisions"].append(
            {
                "revision": revision,
                "body_hash": body_hash,
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                "run_id": run_id,
                "claim": json.loads(claim.model_dump_json()),
                # The source revision is recorded beside the claim revision and
                # never forms part of the claim identity.
                "source_revisions": dict(source_revisions),
            }
        )
        record["current_revision"] = revision
        for item in claim.evidence:
            key = evidence_key(item.source_id, item.quote)
            holders = self._data["claims_by_key"].setdefault(key, [])
            if claim_id not in holders:
                holders.append(claim_id)
            quote_holders = self._data["claims_by_quote"].setdefault(quote_key(item.quote), [])
            if claim_id not in quote_holders:
                quote_holders.append(claim_id)
        return revision

    def assign(
        self,
        claims: Sequence[Claim],
        *,
        source_id: str,
        content_hash: str,
        run_id: str,
    ) -> list[IdentityAssignment]:
        """Give every extracted claim a durable id and record its revision."""
        assignments: list[IdentityAssignment] = []
        for provider_claim in claims:
            assignments.append(
                self._assign_one(
                    provider_claim,
                    source_id=source_id,
                    content_hash=content_hash,
                    run_id=run_id,
                )
            )
        self._write()
        return assignments

    def _assign_one(
        self, provider_claim: Claim, *, source_id: str, content_hash: str, run_id: str
    ) -> IdentityAssignment:
        source_revisions = {source_id: content_hash}
        body = identity_body(provider_claim)
        matched = sorted(self._candidates_for(provider_claim))

        if len(matched) == 1:
            existing = self._data["claims"][matched[0]]
            stored = self._stored_identity(existing)
            if stored is not None and _digest(stored) == _digest(body):
                previous = int(existing["current_revision"])
                revision = self._record_revision(
                    matched[0],
                    provider_claim,
                    source_revisions,
                    run_id=run_id,
                    body=revision_body(provider_claim),
                )
                return IdentityAssignment(
                    claim=provider_claim.model_copy(update={"claim_id": matched[0]}),
                    provider_claim_id=provider_claim.claim_id,
                    status="unchanged" if revision == previous else "revision",
                    reason=(
                        "same claim, same wording: the recorded revision is replayed"
                        if revision == previous
                        else "same claim, material conditions/limitations changed: "
                        "new revision of the same claim id"
                    ),
                    matched_claim_id=matched[0],
                    revision=revision,
                )
            # Same evidence, different meaning fields: unresolved on purpose.
            return self._new_unresolved(
                provider_claim,
                source_revisions=source_revisions,
                run_id=run_id,
                candidates=matched,
                reason="same_evidence_different_claim: a paraphrase or a second "
                "reading of the same quote; a relation check decides, not a hash",
            )

        if len(matched) > 1:
            return self._new_unresolved(
                provider_claim,
                source_revisions=source_revisions,
                run_id=run_id,
                candidates=matched,
                reason="ambiguous_evidence_key: the same evidence maps to several claims",
            )

        merge = sorted(self._cross_source_candidates(provider_claim))
        claim_id = self._next_claim_id()
        revision = self._record_revision(
            claim_id,
            provider_claim,
            source_revisions,
            run_id=run_id,
            body=revision_body(provider_claim),
        )
        return IdentityAssignment(
            claim=provider_claim.model_copy(update={"claim_id": claim_id}),
            provider_claim_id=provider_claim.claim_id,
            status="new",
            reason="no registry record matched this evidence",
            revision=revision,
            merge_candidates=tuple(merge),
        )

    def _new_unresolved(
        self,
        provider_claim: Claim,
        *,
        source_revisions: dict[str, str],
        run_id: str,
        candidates: Iterable[str],
        reason: str,
    ) -> IdentityAssignment:
        """Keep both records; never merge automatically."""
        claim_id = self._next_claim_id()
        revision = self._record_revision(
            claim_id,
            provider_claim,
            source_revisions,
            run_id=run_id,
            body=revision_body(provider_claim),
        )
        self._data["claims"][claim_id].setdefault("unresolved", []).append(
            {
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                "run_id": run_id,
                "reason": reason,
                "candidates": sorted(candidates),
                "status": "awaiting_reconciliation",
            }
        )
        return IdentityAssignment(
            claim=provider_claim.model_copy(update={"claim_id": claim_id}),
            provider_claim_id=provider_claim.claim_id,
            status="ambiguous",
            reason=reason,
            candidates=tuple(sorted(candidates)),
            revision=revision,
        )

    @staticmethod
    def _stored_identity(record: dict[str, Any]) -> dict[str, Any] | None:
        revisions = record.get("revisions") or []
        if not revisions:
            return None
        current = max(revisions, key=lambda item: int(item["revision"]))
        claim = current.get("claim") or {}
        return {
            "text": normalise_text(str(claim.get("text", ""))),
            "kind": normalise_text(str(claim.get("kind", ""))),
            "technology": (
                normalise_text(str(claim["technology"])) if claim.get("technology") else None
            ),
        }

    # --------------------------------------------------------------- notes --
    def register_note(
        self,
        *,
        note_id: str,
        relative_path: str,
        section: str | None,
        claim_ids: Sequence[str],
        run_id: str | None = None,
    ) -> dict[str, Any]:
        """Record a note identity, independent of the note's title.

        The first ``relative_path`` a note id was granted with stays its identity
        anchor; a later different path is recorded as a move, not as a new note.
        """
        record = self._data["notes"].get(note_id)
        if record is None:
            record = {
                "note_id": note_id,
                "relative_path": relative_path,
                "section": section,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "claim_ids": sorted(set(claim_ids)),
                "path_history": [{"relative_path": relative_path, "first_seen_run": run_id}],
                "path_changed": False,
            }
            self._data["notes"][note_id] = record
        else:
            changed = False
            merged = sorted(set(record.get("claim_ids", [])) | set(claim_ids))
            changed = changed or merged != record.get("claim_ids")
            record["claim_ids"] = merged
            if record["relative_path"] != relative_path:
                record["path_changed"] = True
                record["path_history"].append(
                    {"relative_path": relative_path, "first_seen_run": run_id}
                )
                changed = True
            if section and not record.get("section"):
                record["section"] = section
                changed = True
            if changed:
                record["updated_at"] = _utcnow()
        return record

    def note_ids(self) -> list[str]:
        return sorted(self._data["notes"])


def identity_report(assignments: Sequence[IdentityAssignment], *, transitions: bool = True) -> dict[str, Any]:
    """Machine-readable record of the identity decisions of one run.

    With ``transitions=False`` the report is the identity *result* only, which is
    byte-stable across an identical replay; the per-invocation transition belongs
    in the run summary and the stage checkpoints.
    """
    counts = {"new": 0, "unchanged": 0, "revision": 0, "ambiguous": 0}
    for assignment in assignments:
        counts[assignment.status] = counts.get(assignment.status, 0) + 1
    report: dict[str, Any] = {
        "claims": [assignment.to_dict(transitions=transitions) for assignment in assignments],
        "unresolved": [
            assignment.to_dict(transitions=transitions)
            for assignment in assignments
            if assignment.candidates
        ],
        "merge_candidates": [
            assignment.to_dict(transitions=transitions)
            for assignment in assignments
            if assignment.merge_candidates
        ],
        "transition_counts": counts if transitions else None,
        "identity_rule": (
            "identity is granted once and matched on source id plus normalised quote "
            "text, never on offsets; a shifted fragment keeps the same claim id"
        ),
        "revision_rule": (
            "changed conditions, limitations, scope, kind or technology are a new "
            "revision of the same claim; the source revision is stored beside it"
        ),
        "semantic_dedup": SEMANTIC_DEDUP_GUARANTEE,
    }
    return report
