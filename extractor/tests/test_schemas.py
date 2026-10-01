from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from kb_pipeline.schemas import (
    Claim, ClaimType, ContextBundle, ContextStatus, Evidence, FilterAssessment,
    FilterDecision, RunManifest, SourceRecord, StageRecord, StageStatus,
)


def source(**kwargs):
    data = dict(source_id="x:123", author="tester", text="Test text", fetched_at=datetime.now(timezone.utc),
                raw_ref="cache:fixture:0", content_hash="a" * 64)
    return SourceRecord(**(data | kwargs))


def test_source_requires_stable_id_and_never_fabricates_published_at():
    record = source(reply_to_id="x:456", conversation_id="x:123", quoted_source_id="x:789")
    assert record.published_at is None
    assert record.context_status is ContextStatus.unavailable
    assert SourceRecord.model_validate_json(record.model_dump_json()) == record
    with pytest.raises(ValidationError):
        source(source_id="x:")
    with pytest.raises(ValidationError):
        source(source_id="generated:1")


def test_claim_evidence_and_context_are_explicit():
    bundle = ContextBundle(focus=source(), context_status=ContextStatus.partial, missing_ids=["x:456"])
    assert bundle.related == []
    claim = Claim(claim_id="x:123:0", source_ids=["x:123"], text="Test", kind=ClaimType.observation,
                  evidence=[Evidence(source_id="x:123", quote="Test text", start=0, end=9)])
    assert claim.interpretation is None
    with pytest.raises(ValidationError):
        Claim.model_validate(claim.model_dump() | {"evidence": []})


def test_invalid_evidence_and_decisions_fail():
    with pytest.raises(ValidationError):
        Evidence(source_id="x:1", quote="x", start=4, end=3)
    with pytest.raises(ValidationError):
        Claim(claim_id="x:123:0", source_ids=["x:123"], text="Test", kind="opinion",
              evidence=[Evidence(source_id="x:456", quote="Test")])
    with pytest.raises(ValidationError):
        FilterAssessment(source_id="x:123", decision=FilterDecision.reject, reason_code="noise",
                         probabilities={"engineering": 1.2}, model="jev", question_version="v1", policy_version="v1")


def test_manifest_distinguishes_unmeasured_cost_from_zero_and_errors_from_rejects():
    manifest = RunManifest(run_id="run-1", created_at=datetime.now(timezone.utc), code_version="v1",
                           policy_version="v1", stages={"filter": StageRecord(status=StageStatus.error, error="API timeout", attempts=1)})
    assert manifest.cost is None
    assert manifest.stages["filter"].status is StageStatus.error
    assert manifest.model_dump(mode="json")["schema_version"] == 1
