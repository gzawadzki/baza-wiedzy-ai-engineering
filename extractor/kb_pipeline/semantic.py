"""Offline semantic verification for claim extraction."""

from __future__ import annotations

from typing import Callable, Mapping

from .schemas import (
    Claim,
    SourceRecord,
    VerificationRelation,
    VerificationResult,
)
from .verification import verify_claim


class SemanticCheckerError(RuntimeError):
    """Raised when semantic checker fails after retry attempts."""


def assess_claim(
    claim: Claim,
    sources: Mapping[str, SourceRecord],
    checker: Callable[[Claim, Mapping[str, SourceRecord]], tuple[VerificationRelation | str, str]],
    *,
    model: str | None = None,
    prompt_version: str | None = None,
    max_attempts: int = 2,
) -> VerificationResult:
    """Assess semantic relationship between claim and source evidence."""
    if max_attempts < 1:
        raise ValueError(f"max_attempts must be >= 1, got {max_attempts}")

    base_result = verify_claim(claim, sources)
    if not base_result.quote_matches:
        return base_result

    last_error: Exception | None = None
    relation: VerificationRelation | None = None
    reason: str | None = None

    for _ in range(max_attempts):
        try:
            raw_relation, raw_reason = checker(claim, sources)
            if isinstance(raw_relation, str):
                relation = VerificationRelation(raw_relation)
            else:
                relation = raw_relation
            reason = raw_reason
            break
        except Exception as exc:
            last_error = exc
    else:
        raise SemanticCheckerError(
            f"Checker failed after {max_attempts} attempts"
        ) from last_error

    return VerificationResult(
        claim_id=claim.claim_id,
        quote_matches=True,
        relation=relation,
        source_supported=(relation == VerificationRelation.supports),
        independently_validated=False,
        reason=reason,
        evidence=claim.evidence,
        model=model,
        prompt_version=prompt_version,
        response_ref=None,
    )
