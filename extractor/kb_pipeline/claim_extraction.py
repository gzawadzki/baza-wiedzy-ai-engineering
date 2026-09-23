"""Bounded offline claim extraction stage for Jev-filtered source revisions."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .context import build_context
from .live_jev import (
    _clean_token,
    _validate_safe_artifact_target,
    _write_json,
    compute_context_hash,
    compute_input_hash,
    compute_policy_version_key,
)
from .pilot import _safe_paths
from .schemas import Claim, ClaimType, ContextBundle, ContextStatus, Evidence, SourceRecord
from .stage_cache import StageCache
from .storage import SourceStore

_IMPERATIVE_VERBS = frozenset(
    {
        "prune",
        "keep",
        "avoid",
        "ensure",
        "use",
        "validate",
        "verify",
        "isolate",
        "store",
        "limit",
        "enforce",
        "clean",
        "cache",
        "measure",
        "test",
        "prefer",
        "separate",
        "monitor",
        "pin",
        "filter",
        "batch",
        "benchmark",
        "evaluate",
        "handle",
        "deploy",
        "scale",
        "check",
        "record",
        "guard",
        "restrict",
        "prevent",
        "reject",
        "sanitize",
        "implement",
        "configure",
        "maintain",
        "track",
        "checkpoint",
        "preserve",
        "split",
        "build",
        "run",
        "set",
    }
)

_MODAL_RECOMMENDATIONS = re.compile(
    r"\b(always|never|must|should|ought to|recommend|recommended|crucial to|essential to|"
    r"best to|better to|make sure|need to|important to|do not|don't)\b",
    re.IGNORECASE,
)

_LIMITATION_PATTERNS = re.compile(
    r"\b(fails when|fails if|limited to|limited by|bottleneck|limitation|drawback|"
    r"pitfall|anti-pattern|anti pattern|caveat|does not scale|cannot handle|"
    r"breaks when|breaks if|degrades when|degrades if|risk of|trade-off|tradeoff)\b",
    re.IGNORECASE,
)

_EXPERIMENT_PATTERNS = re.compile(
    r"\b(experimented with|tested with|in our benchmark|in benchmark|ablation showed|"
    r"trial of|we measured|evaluated on|evaluation shows)\b",
    re.IGNORECASE,
)

_OBSERVATION_PATTERNS = re.compile(
    r"\b(observed that|results show|results indicate|measured that|demonstrates that|"
    r"causes|leads to|suffer from|suffers from|context drift|in practice|found that|tends to|correlates with|"
    r"increases latency|reduces latency|reduces tail latency|improves throughput|"
    r"degrades throughput)\b",
    re.IGNORECASE,
)

_HYPOTHESIS_PATTERNS = re.compile(
    r"\b(hypothesize|suspect that|conjecture that|likely because|might be caused by)\b",
    re.IGNORECASE,
)

_LIST_PREFIX_RE = re.compile(r"^(\s*[-*•]\s+|\s*\d+[\.\)]\s+)")


def _segment_text_candidates(text: str) -> list[tuple[int, int, str]]:
    """Segment source text into candidate statements while strictly preserving exact offsets."""
    candidates: list[tuple[int, int, str]] = []
    lines: list[tuple[int, int, str]] = []

    pos = 0
    raw_lines = text.splitlines(keepends=True)
    for raw_line in raw_lines:
        line_start = pos
        line_end = line_start + len(raw_line)
        lines.append((line_start, line_end, raw_line))
        pos = line_end

    for line_start, line_end, raw_line in lines:
        prefix_match = _LIST_PREFIX_RE.match(raw_line)
        if prefix_match:
            marker_len = prefix_match.end()
            cand_start = line_start + marker_len
            cand_end = line_end
        else:
            cand_start = line_start
            cand_end = line_end

        cand_str = text[cand_start:cand_end]
        lstrip_len = len(cand_str) - len(cand_str.lstrip())
        cand_str_l = cand_str.lstrip()
        rstrip_len = len(cand_str_l) - len(cand_str_l.rstrip())

        clean_start = cand_start + lstrip_len
        clean_end = cand_end - rstrip_len

        if clean_end <= clean_start:
            continue

        clean_line = text[clean_start:clean_end]

        sentence_splits = list(re.finditer(r"(?<=[.!?])\s+(?=[A-Za-z0-9\"'“‘])", clean_line))
        if not sentence_splits:
            candidates.append((clean_start, clean_end, clean_line))
        else:
            s_pos = 0
            for sm in sentence_splits:
                s_end = sm.start()
                s_raw = clean_line[s_pos:s_end]
                s_lstrip = len(s_raw) - len(s_raw.lstrip())
                s_trimmed = s_raw.strip()
                if s_trimmed:
                    actual_start = clean_start + s_pos + s_lstrip
                    actual_end = actual_start + len(s_trimmed)
                    candidates.append((actual_start, actual_end, text[actual_start:actual_end]))
                s_pos = sm.end()

            rem_raw = clean_line[s_pos:]
            rem_lstrip = len(rem_raw) - len(rem_raw.lstrip())
            rem_trimmed = rem_raw.strip()
            if rem_trimmed:
                actual_start = clean_start + s_pos + rem_lstrip
                actual_end = actual_start + len(rem_trimmed)
                candidates.append((actual_start, actual_end, text[actual_start:actual_end]))

    return candidates


def _classify_candidate(statement: str) -> ClaimType | None:
    """Classify whether a candidate statement is an actionable engineering claim."""
    words = [w for w in re.split(r"\s+", statement) if w]
    if len(statement) < 15 or len(words) < 3:
        return None

    if all(w.startswith(("http://", "https://", "@", "#")) for w in words):
        return None

    first_word_cleaned = re.sub(r"^[^\w]+|[^\w]+$", "", words[0]).lower()

    if _LIMITATION_PATTERNS.search(statement):
        return ClaimType.limitation
    if _EXPERIMENT_PATTERNS.search(statement):
        return ClaimType.experiment
    if _OBSERVATION_PATTERNS.search(statement):
        return ClaimType.observation
    if _HYPOTHESIS_PATTERNS.search(statement):
        return ClaimType.hypothesis

    if first_word_cleaned in _IMPERATIVE_VERBS or _MODAL_RECOMMENDATIONS.search(statement):
        return ClaimType.recommendation

    return None


def extract_claim_proposals(record: SourceRecord, bundle: ContextBundle) -> list[Claim]:
    """Extract distinct actionable claim proposals from the focus source record offline."""
    candidates = _segment_text_candidates(record.text)
    claims: list[Claim] = []
    seen_quotes: set[str] = set()
    slot = 0

    source_id_clean = _clean_token(record.source_id)

    for start, end, statement in candidates:
        if statement in seen_quotes:
            continue

        kind = _classify_candidate(statement)
        if kind is None:
            continue

        seen_quotes.add(statement)

        # Exact quote and offset verification against focus source text
        exact_slice = record.text[start:end]
        if exact_slice != statement:
            raise ValueError(
                f"Candidate slice mismatch: source[{start}:{end}] is '{exact_slice}', expected '{statement}'"
            )

        evidence_item = Evidence(
            source_id=record.source_id,
            content_hash=record.content_hash,
            quote=exact_slice,
            start=start,
            end=end,
        )

        limitations = [
            f"Context status: {bundle.context_status.value}",
        ]
        if bundle.missing_ids:
            limitations.append(f"Missing context sources: {', '.join(sorted(bundle.missing_ids))}")
        limitations.append("Unverified live extraction (independent validation deferred)")

        claim_id = f"claim_{source_id_clean}_{record.content_hash[:12]}_{slot}"
        slot += 1

        claim = Claim(
            claim_id=claim_id,
            source_ids=[record.source_id],
            text=exact_slice,
            kind=kind,
            evidence=[evidence_item],
            scope="Extracted from source revision without independent semantic verification.",
            conditions=[
                f"Derived from focus source '{record.source_id}' revision '{record.content_hash[:10]}'."
            ],
            limitations=limitations,
        )
        claims.append(claim)

    return claims


def _verify_exact_quote_and_offsets(
    source_text: str,
    content_hash: str,
    claim: Claim,
) -> None:
    """Deterministic exact substring/offset check against the pinned revision text."""
    for ev in claim.evidence:
        if ev.content_hash != content_hash:
            raise ValueError(
                f"Evidence content_hash '{ev.content_hash}' does not match pinned revision '{content_hash}'"
            )
        if ev.start is None or ev.end is None:
            raise ValueError(f"Evidence for claim '{claim.claim_id}' is missing start/end offsets")
        if ev.start < 0 or ev.end > len(source_text) or ev.start >= ev.end:
            raise ValueError(
                f"Evidence offsets [{ev.start}:{ev.end}] are out of range for source text (len={len(source_text)})"
            )
        slice_text = source_text[ev.start:ev.end]
        if slice_text != ev.quote:
            raise ValueError(
                f"Exact quote mismatch for claim '{claim.claim_id}': source[{ev.start}:{ev.end}] is '{slice_text}', but evidence quote is '{ev.quote}'"
            )
        if ev.quote not in source_text:
            raise ValueError(
                f"Quote '{ev.quote}' is not an exact substring of source text"
            )


def _render_human_readable_proposal(
    record: SourceRecord,
    bundle: ContextBundle,
    claims: list[Claim],
) -> str:
    """Render a human-readable staging proposal markdown clearly marked unverified/unpublished."""
    lines = [
        "# Staging Claim Proposal",
        "",
        "> **UNVERIFIED / UNPUBLISHED — STAGING ONLY**",
        "> This proposal has NOT undergone independent semantic verification and is NOT published to the vault.",
        "",
        "## Source Revision Provenance",
        f"- **Source ID**: `{record.source_id}`",
        f"- **Content Hash**: `{record.content_hash}`",
        f"- **Author**: `{record.author}`",
        f"- **URL**: {record.url or 'URL not provided'}",
        f"- **Context Status**: `{bundle.context_status.value}`",
        f"- **Missing Context IDs**: `{', '.join(sorted(bundle.missing_ids)) if bundle.missing_ids else 'none'}`",
        f"- **Related Context Count**: {len(bundle.related)}",
        "",
    ]

    if not claims:
        lines.extend([
            "## Staged Claims",
            "",
            "No reliable actionable claims extracted from this source revision.",
            "",
        ])
    else:
        lines.extend([
            f"## Staged Claims ({len(claims)})",
            "",
        ])
        for claim in claims:
            lines.extend([
                f"### Claim: `{claim.claim_id}`",
                "",
                f"- **Kind**: `{claim.kind.value}`",
                f"- **Statement**: {claim.text}",
                "- **Evidence**:",
            ])
            for ev in claim.evidence:
                lines.extend([
                    f'  - Quote: “{ev.quote}”',
                    f"  - Source ID: `{ev.source_id}`",
                    f"  - Content Hash: `{ev.content_hash}`",
                    f"  - Offsets: `[{ev.start}:{ev.end}]`",
                ])
            lines.extend([
                f"- **Scope**: {claim.scope or 'Not specified.'}",
                "- **Conditions**:",
                *([f"  - {c}" for c in claim.conditions] if claim.conditions else ["  - None specified."]),
                "- **Limitations**:",
                *([f"  - {lim}" for lim in claim.limitations] if claim.limitations else ["  - None specified."]),
                "",
            ])

    return "\n".join(lines).rstrip() + "\n"


def extract_live_claims(
    vault: Path,
    workspace: Path,
    source_id: str,
    content_hash: str,
    *,
    model: str = "jev-latest",
    question_version: str = "v1",
    policy_version: str = "v1",
    usefulness_threshold: float = 0.7,
    context_threshold: float = 0.6,
) -> dict[str, Any]:
    """Extract distinct actionable claims from a Jev-filtered source revision offline."""
    if not isinstance(source_id, str) or not source_id.startswith("x:") or not source_id[2:].isdigit():
        raise ValueError(f"Invalid X source ID: '{source_id}'; expected format x:<numeric_id>")

    if (
        not isinstance(content_hash, str)
        or len(content_hash) != 64
        or not all(c in "0123456789abcdefABCDEF" for c in content_hash)
    ):
        raise ValueError(f"Invalid content hash: '{content_hash}'; expected 64-character hex string")
    content_hash = content_hash.lower()

    vault_path, workspace_path = _safe_paths(Path(vault), Path(workspace))

    proposals_dir = workspace_path / "proposals"
    _validate_safe_artifact_target(proposals_dir, vault_path)

    # 1. Deterministic revision lookup and context assembly
    with SourceStore(workspace_path) as store:
        record = store.get(source_id, content_hash)
        if record is None:
            raise ValueError(
                f"Source '{source_id}' with content hash '{content_hash}' not found in store"
            )

        def deterministic_lookup(rel_id: str) -> SourceRecord | None:
            return store.get_deterministic(rel_id)

        bundle = build_context(record, deterministic_lookup)

    source_hash = record.content_hash
    context_hash = compute_context_hash(bundle)
    input_hash = compute_input_hash(record.source_id, source_hash)
    policy_key = compute_policy_version_key(
        question_version, policy_version, usefulness_threshold, context_threshold
    )

    # 2. Check existing matching Jev filter assessment in StageCache
    filter_cache_key = StageCache.key(
        "filter", input_hash, context_hash, model, policy_key, schema_version=1
    )

    with StageCache(workspace_path) as cache:
        filter_cached = cache.get(filter_cache_key)
        if filter_cached is None:
            raise ValueError(
                f"No matching Jev filter assessment found in cache for source '{source_id}' "
                f"and revision '{source_hash}'. Evaluate with jev-evaluate before extraction."
            )

        # Validate exact source, context, model, and policy identity
        if filter_cached.get("source_id") != record.source_id:
            raise ValueError(
                f"Filter assessment source_id mismatch: '{filter_cached.get('source_id')}' != '{record.source_id}'"
            )
        if filter_cached.get("source_hash") != source_hash:
            raise ValueError(
                f"Filter assessment source_hash mismatch: '{filter_cached.get('source_hash')}' != '{source_hash}'"
            )
        if filter_cached.get("context_hash") != context_hash:
            raise ValueError(
                f"Filter assessment context_hash mismatch: '{filter_cached.get('context_hash')}' != '{context_hash}'"
            )
        if filter_cached.get("model") != model:
            raise ValueError(
                f"Filter assessment model mismatch: '{filter_cached.get('model')}' != '{model}'"
            )
        if filter_cached.get("question_version") != question_version:
            raise ValueError(
                f"Filter assessment question_version mismatch: '{filter_cached.get('question_version')}' != '{question_version}'"
            )
        if filter_cached.get("policy_version") != policy_version:
            raise ValueError(
                f"Filter assessment policy_version mismatch: '{filter_cached.get('policy_version')}' != '{policy_version}'"
            )
        if filter_cached.get("usefulness_threshold") != usefulness_threshold:
            raise ValueError(
                f"Filter assessment usefulness_threshold mismatch: '{filter_cached.get('usefulness_threshold')}' != '{usefulness_threshold}'"
            )
        if filter_cached.get("context_threshold") != context_threshold:
            raise ValueError(
                f"Filter assessment context_threshold mismatch: '{filter_cached.get('context_threshold')}' != '{context_threshold}'"
            )

        assessment = filter_cached.get("assessment")
        if not isinstance(assessment, dict):
            raise ValueError("Invalid assessment payload in filter cache")

        if assessment.get("bypass") is not False:
            raise ValueError(
                f"Filter assessment for source '{source_id}' has bypass=True; extraction requires live assessment"
            )

        decision = assessment.get("decision")
        if decision != "extract":
            raise ValueError(
                f"Filter assessment decision for source '{source_id}' is '{decision}' (expected 'extract')"
            )

        # 3. Check extraction cache for idempotent replay
        extract_cache_key = StageCache.key(
            "claim_extract", input_hash, context_hash, model, policy_key, schema_version=1
        )
        extract_cached = cache.get(extract_cache_key)
        if extract_cached is not None:
            if (
                extract_cached.get("source_id") != record.source_id
                or extract_cached.get("content_hash") != source_hash
                or extract_cached.get("context_hash") != context_hash
                or extract_cached.get("model") != model
                or extract_cached.get("policy_version") != policy_version
                or extract_cached.get("question_version", question_version) != question_version
                or extract_cached.get("usefulness_threshold", usefulness_threshold) != usefulness_threshold
                or extract_cached.get("context_threshold", context_threshold) != context_threshold
            ):
                raise ValueError("Cached extraction identity mismatch")

            json_ref = extract_cached.get("proposal_json_ref")
            md_ref = extract_cached.get("proposal_md_ref")
            if not json_ref or not md_ref:
                raise ValueError("Cached extraction missing proposal file references")

            cached_json_path = workspace_path / json_ref
            cached_md_path = workspace_path / md_ref

            _validate_safe_artifact_target(cached_json_path, vault_path)
            _validate_safe_artifact_target(cached_md_path, vault_path)

            if not cached_json_path.is_file():
                raise ValueError(
                    f"Cached proposal JSON artifact missing: '{cached_json_path}'"
                )
            if not cached_md_path.is_file():
                raise ValueError(
                    f"Cached proposal Markdown artifact missing: '{cached_md_path}'"
                )

            cached_claims_raw = extract_cached.get("claims")
            if not isinstance(cached_claims_raw, list):
                raise ValueError("Cached extraction claims payload must be a list")

            # Revalidate exact quote offsets against pinned source for all cached claims
            for raw_claim in cached_claims_raw:
                try:
                    claim_obj = Claim.model_validate(raw_claim)
                except Exception as exc:
                    raise ValueError(f"Tampered cached claim structure: {exc}") from exc
                _verify_exact_quote_and_offsets(record.text, source_hash, claim_obj)

            # Revalidate proposal JSON artifact on disk
            try:
                disk_proposal = json.loads(cached_json_path.read_text(encoding="utf-8"))
            except Exception as exc:
                raise ValueError(f"Cached proposal JSON artifact is invalid: {exc}") from exc

            disk_claims_raw = disk_proposal.get("claims")
            if not isinstance(disk_claims_raw, list):
                raise ValueError("Proposal JSON artifact claims payload must be a list")
            if len(disk_claims_raw) != len(cached_claims_raw):
                raise ValueError("Discrepancy between cached claims and proposal JSON artifact claims count")

            for disk_claim_raw in disk_claims_raw:
                try:
                    claim_obj = Claim.model_validate(disk_claim_raw)
                except Exception as exc:
                    raise ValueError(f"Tampered proposal JSON artifact claim structure: {exc}") from exc
                _verify_exact_quote_and_offsets(record.text, source_hash, claim_obj)

            return {
                "status": "completed",
                "source_id": record.source_id,
                "content_hash": source_hash,
                "context_hash": context_hash,
                "context_status": bundle.context_status.value,
                "missing_ids": bundle.missing_ids,
                "claim_count": extract_cached.get("claim_count", 0),
                "claims": cached_claims_raw,
                "proposal_json_ref": json_ref,
                "proposal_md_ref": md_ref,
                "cached": True,
                "verified": False,
                "published": False,
            }

        # 4. Conservative deterministic offline claim extraction
        claims = extract_claim_proposals(record, bundle)

        # 5. Deterministic exact substring and offset check for all claims
        for claim in claims:
            _verify_exact_quote_and_offsets(record.text, source_hash, claim)

        # 6. Persist proposals outside vault keyed by full extraction cache key
        base_name = f"claim_proposals_{extract_cache_key}"
        json_filename = f"{base_name}.json"
        md_filename = f"{base_name}.md"

        json_path = proposals_dir / json_filename
        md_path = proposals_dir / md_filename

        _validate_safe_artifact_target(json_path, vault_path)
        _validate_safe_artifact_target(md_path, vault_path)

        proposal_json_ref = f"proposals/{json_filename}"
        proposal_md_ref = f"proposals/{md_filename}"

        if not md_path.exists():
            rendered_md = _render_human_readable_proposal(record, bundle, claims)
            md_path.parent.mkdir(parents=True, exist_ok=True)
            md_path.write_bytes(rendered_md.encode("utf-8"))

        serialized_claims = [claim.model_dump(mode="json") for claim in claims]

        machine_proposal = {
            "schema_version": 1,
            "cache_key": extract_cache_key,
            "source_id": record.source_id,
            "content_hash": source_hash,
            "context_hash": context_hash,
            "context_status": bundle.context_status.value,
            "missing_ids": bundle.missing_ids,
            "model": model,
            "question_version": question_version,
            "policy_version": policy_version,
            "usefulness_threshold": usefulness_threshold,
            "context_threshold": context_threshold,
            "status": "completed",
            "claim_count": len(claims),
            "claims": serialized_claims,
            "proposal_json_ref": proposal_json_ref,
            "proposal_md_ref": proposal_md_ref,
            "verified": False,
            "published": False,
            "staging": True,
            "disclaimer": "UNVERIFIED / UNPUBLISHED — STAGING ONLY",
        }
        if not json_path.exists():
            _write_json(json_path, machine_proposal)

        cache.put(extract_cache_key, machine_proposal)

        return {
            "status": "completed",
            "source_id": record.source_id,
            "content_hash": source_hash,
            "context_hash": context_hash,
            "context_status": bundle.context_status.value,
            "missing_ids": bundle.missing_ids,
            "claim_count": len(claims),
            "claims": serialized_claims,
            "proposal_json_ref": proposal_json_ref,
            "proposal_md_ref": proposal_md_ref,
            "cached": False,
            "verified": False,
            "published": False,
        }
