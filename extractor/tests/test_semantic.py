from datetime import datetime, timezone
from unittest.mock import Mock

import pytest

from kb_pipeline.schemas import (
    Claim,
    ClaimType,
    Evidence,
    SourceRecord,
    VerificationRelation,
)
from kb_pipeline.semantic import SemanticCheckerError, assess_claim


def make_source(**kwargs) -> SourceRecord:
    data = {
        "source_id": "x:100",
        "author": "tester",
        "text": "Production deployments require robust canary verification stages.",
        "fetched_at": datetime.now(timezone.utc),
        "raw_ref": "cache:fixture:0",
        "content_hash": "a" * 64,
    }
    return SourceRecord(**(data | kwargs))


def make_claim(**kwargs) -> Claim:
    data = {
        "claim_id": "x:100:0",
        "source_ids": ["x:100"],
        "text": "Production deployments benefit from canary stages.",
        "kind": ClaimType.observation,
        "evidence": [
            Evidence(
                source_id="x:100",
                quote="Production deployments require robust canary verification stages.",
            )
        ],
    }
    return Claim(**(data | kwargs))


def test_missing_quote_does_not_call_checker():
    sources = {
        "x:100": make_source(
            text="Completely different source content without matching keywords."
        )
    }
    claim = make_claim()
    checker = Mock()

    result = assess_claim(
        claim,
        sources,
        checker,
        model="eval-model",
        prompt_version="v1",
    )

    assert result.quote_matches is False
    assert result.source_supported is False
    assert result.independently_validated is False
    assert result.relation is VerificationRelation.unsupported
    checker.assert_not_called()


def test_missing_source_record_does_not_call_checker():
    sources = {}
    claim = make_claim()
    checker = Mock()

    result = assess_claim(
        claim,
        sources,
        checker,
        model="eval-model",
        prompt_version="v1",
    )

    assert result.quote_matches is False
    assert result.source_supported is False
    assert result.independently_validated is False
    checker.assert_not_called()


def test_unsupported_verdict_retained_without_subsequent_attempts():
    sources = {"x:100": make_source()}
    claim = make_claim()

    checker = Mock(
        side_effect=[
            (VerificationRelation.unsupported, "Evidence text does not back claim"),
            (VerificationRelation.supports, "Supported on retry"),
        ]
    )

    result = assess_claim(
        claim,
        sources,
        checker,
        model="eval-model",
        prompt_version="v1",
        max_attempts=3,
    )

    assert checker.call_count == 1
    assert result.quote_matches is True
    assert result.relation is VerificationRelation.unsupported
    assert result.source_supported is False
    assert result.independently_validated is False
    assert result.reason == "Evidence text does not back claim"


def test_uncertain_verdict_retained_without_subsequent_attempts():
    sources = {"x:100": make_source()}
    claim = make_claim()

    checker = Mock(
        side_effect=[
            (VerificationRelation.uncertain, "Ambiguous context"),
            (VerificationRelation.supports, "Supported on retry"),
        ]
    )

    result = assess_claim(
        claim,
        sources,
        checker,
        model="eval-model",
        prompt_version="v1",
        max_attempts=3,
    )

    assert checker.call_count == 1
    assert result.quote_matches is True
    assert result.relation is VerificationRelation.uncertain
    assert result.source_supported is False
    assert result.independently_validated is False
    assert result.reason == "Ambiguous context"


def test_retry_succeeds_after_transient_exceptions_within_max_attempts():
    sources = {"x:100": make_source()}
    claim = make_claim()

    checker = Mock(
        side_effect=[
            RuntimeError("First temporary failure"),
            RuntimeError("Second temporary failure"),
            (VerificationRelation.supports, "Evidence confirms claim"),
        ]
    )

    result = assess_claim(
        claim,
        sources,
        checker,
        model="eval-model",
        prompt_version="v1",
        max_attempts=3,
    )

    assert checker.call_count == 3
    assert result.quote_matches is True
    assert result.relation is VerificationRelation.supports
    assert result.source_supported is True
    assert result.independently_validated is False
    assert result.reason == "Evidence confirms claim"


def test_exhausted_retries_raise_semantic_checker_error():
    sources = {"x:100": make_source()}
    claim = make_claim()

    checker = Mock(
        side_effect=[
            RuntimeError("First failure"),
            RuntimeError("Second failure"),
        ]
    )

    with pytest.raises(SemanticCheckerError) as exc_info:
        assess_claim(
            claim,
            sources,
            checker,
            model="eval-model",
            prompt_version="v1",
            max_attempts=2,
        )

    assert checker.call_count == 2
    assert isinstance(exc_info.value, RuntimeError)
    assert exc_info.value.__cause__ is not None
    assert str(exc_info.value.__cause__) == "Second failure"


def test_supports_relation_sets_flags_and_clears_metadata():
    sources = {"x:100": make_source()}
    claim = make_claim()

    checker = Mock(return_value=(VerificationRelation.supports, "Direct support found"))

    result = assess_claim(
        claim,
        sources,
        checker,
        model="eval-model",
        prompt_version="v1",
    )

    assert result.quote_matches is True
    assert result.relation is VerificationRelation.supports
    assert result.source_supported is True
    assert result.independently_validated is False
    assert result.reason == "Direct support found"
    assert result.model is None
    assert result.prompt_version is None
    assert result.response_ref is None
    assert result.evidence == claim.evidence


def test_contradicts_relation_sets_flags():
    sources = {"x:100": make_source()}
    claim = make_claim()

    checker = Mock(
        return_value=(VerificationRelation.contradicts, "Direct contradiction found")
    )

    result = assess_claim(
        claim,
        sources,
        checker,
        model="eval-model",
        prompt_version="v1",
    )

    assert result.quote_matches is True
    assert result.relation is VerificationRelation.contradicts
    assert result.source_supported is False
    assert result.independently_validated is False
    assert result.reason == "Direct contradiction found"
    assert result.model is None
    assert result.prompt_version is None
    assert result.response_ref is None
    assert result.evidence == claim.evidence


def test_string_relation_value_conversion():
    sources = {"x:100": make_source()}
    claim = make_claim()

    checker = Mock(return_value=("supports", "Textual supports"))
    result = assess_claim(claim, sources, checker, model="eval-model", prompt_version="v1")
    assert result.relation is VerificationRelation.supports
    assert result.source_supported is True
    assert result.independently_validated is False

    checker = Mock(return_value=("contradicts", "Textual contradicts"))
    result = assess_claim(claim, sources, checker, model="eval-model", prompt_version="v1")
    assert result.relation is VerificationRelation.contradicts
    assert result.source_supported is False
    assert result.independently_validated is False


def test_invalid_max_attempts_raises_value_error():
    sources = {"x:100": make_source()}
    claim = make_claim()
    checker = Mock()

    for invalid in [0, -1, -10]:
        with pytest.raises(ValueError) as exc_info:
            assess_claim(
                claim,
                sources,
                checker,
                model="eval-model",
                prompt_version="v1",
                max_attempts=invalid,
            )
        assert "max_attempts" in str(exc_info.value)

    checker.assert_not_called()


def test_default_arguments_execution():
    sources = {"x:100": make_source()}
    claim = make_claim()
    checker = Mock(return_value=(VerificationRelation.supports, "Default test"))

    result = assess_claim(claim, sources, checker)
    assert result.quote_matches is True
    assert result.relation is VerificationRelation.supports
    assert result.source_supported is True
    assert result.independently_validated is False
    assert checker.call_count == 1
