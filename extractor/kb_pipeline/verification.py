"""Offline quote and semantic verification for claims against source records."""

from __future__ import annotations

import re
from typing import Callable, Mapping

from .schemas import (
    Claim,
    SourceRecord,
    VerificationRelation,
    VerificationResult,
)

_WS_PATTERN = re.compile(r"\s+")
_CJK_WS_PATTERN = re.compile(
    r"(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])"
)


def _collapse_whitespace(text: str) -> str:
    return _WS_PATTERN.sub(" ", text).strip()


def _cjk_collapse(text: str) -> str:
    return _CJK_WS_PATTERN.sub("", text)


def _matches_quote(target: str, quote: str, *, is_slice: bool) -> bool:
    norm_quote = _collapse_whitespace(quote)
    if not norm_quote:
        return False

    if is_slice:
        if target == quote:
            return True
        norm_target = _collapse_whitespace(target)
        if norm_target == norm_quote:
            return True
        return _cjk_collapse(norm_target) == _cjk_collapse(norm_quote)

    if quote in target:
        return True
    norm_target = _collapse_whitespace(target)
    if norm_quote in norm_target:
        return True
    return _cjk_collapse(norm_quote) in _cjk_collapse(norm_target)


def verify_claim(
    claim: Claim,
    sources: Mapping[str, SourceRecord],
    semantic_check: Callable[[Claim, Mapping[str, SourceRecord]], tuple[VerificationRelation, str]] | None = None,
) -> VerificationResult:
    """Verify claim evidence quotes against sources and optionally assess semantic relation."""
    if not claim.evidence:
        return VerificationResult(
            claim_id=claim.claim_id,
            quote_matches=False,
            relation=VerificationRelation.unsupported,
            source_supported=False,
            independently_validated=False,
            reason="Claim contains no evidence",
            evidence=[],
        )

    for ev in claim.evidence:
        source = sources.get(ev.source_id)
        if source is None:
            return VerificationResult(
                claim_id=claim.claim_id,
                quote_matches=False,
                relation=VerificationRelation.unsupported,
                source_supported=False,
                independently_validated=False,
                reason=f"Source record '{ev.source_id}' not found",
                evidence=claim.evidence,
            )

        source_text = source.text
        if not _collapse_whitespace(ev.quote):
            return VerificationResult(
                claim_id=claim.claim_id,
                quote_matches=False,
                relation=VerificationRelation.unsupported,
                source_supported=False,
                independently_validated=False,
                reason=f"Evidence quote for source '{ev.source_id}' is empty",
                evidence=claim.evidence,
            )

        if ev.start is not None and ev.end is not None:
            if ev.start < 0 or ev.end > len(source_text) or ev.start >= ev.end:
                return VerificationResult(
                    claim_id=claim.claim_id,
                    quote_matches=False,
                    relation=VerificationRelation.unsupported,
                    source_supported=False,
                    independently_validated=False,
                    reason=f"Evidence offsets [{ev.start}:{ev.end}] are out of range for source '{ev.source_id}'",
                    evidence=claim.evidence,
                )

            slice_text = source_text[ev.start:ev.end]
            if not _matches_quote(slice_text, ev.quote, is_slice=True):
                return VerificationResult(
                    claim_id=claim.claim_id,
                    quote_matches=False,
                    relation=VerificationRelation.unsupported,
                    source_supported=False,
                    independently_validated=False,
                    reason=f"Quote does not match source '{ev.source_id}' at offsets [{ev.start}:{ev.end}]",
                    evidence=claim.evidence,
                )
        else:
            if not _matches_quote(source_text, ev.quote, is_slice=False):
                return VerificationResult(
                    claim_id=claim.claim_id,
                    quote_matches=False,
                    relation=VerificationRelation.unsupported,
                    source_supported=False,
                    independently_validated=False,
                    reason=f"Quote not found in source '{ev.source_id}'",
                    evidence=claim.evidence,
                )

    if semantic_check is None:
        return VerificationResult(
            claim_id=claim.claim_id,
            quote_matches=True,
            relation=VerificationRelation.uncertain,
            source_supported=False,
            independently_validated=False,
            reason="Evidence quotes verified; semantic check not provided",
            evidence=claim.evidence,
        )

    relation, reason = semantic_check(claim, sources)
    if isinstance(relation, str):
        relation = VerificationRelation(relation)

    return VerificationResult(
        claim_id=claim.claim_id,
        quote_matches=True,
        relation=relation,
        source_supported=(relation == VerificationRelation.supports),
        independently_validated=False,
        reason=reason,
        evidence=claim.evidence,
    )
