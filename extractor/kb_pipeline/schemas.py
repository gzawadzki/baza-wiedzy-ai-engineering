"""Versioned, provider-independent contracts for the offline knowledge pipeline.

These models describe evidence and decisions, not guarantees of factual correctness.
Do not serialize credentials or provider request headers into artifacts.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SCHEMA_VERSION = 1


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[1] = SCHEMA_VERSION


class ContextStatus(str, Enum):
    complete = "complete"
    partial = "partial"
    unavailable = "unavailable"


class SourceRecord(Contract):
    source_id: str = Field(min_length=3)  # x:<tweet_id>
    author: str = Field(min_length=1)
    url: str | None = None
    text: str = Field(min_length=1)
    published_at: datetime | None = None
    fetched_at: datetime
    language: str | None = None
    reply_to_id: str | None = None
    conversation_id: str | None = None
    quoted_source_id: str | None = None
    raw_ref: str
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    context_status: ContextStatus = ContextStatus.unavailable

    @field_validator("source_id", "reply_to_id", "conversation_id", "quoted_source_id")
    @classmethod
    def stable_x_id(cls, value: str | None) -> str | None:
        if value is not None and (not value.startswith("x:") or not value[2:].isdigit()):
            raise ValueError("X source IDs must be stable x:<numeric_id> identifiers")
        return value


class ContextItem(Contract):
    source: SourceRecord
    role: Literal["parent", "quote", "thread"]
    provenance: str = Field(min_length=1)  # e.g. cache:<handle>, apify:<actor>


class ContextBundle(Contract):
    focus: SourceRecord
    related: list[ContextItem] = Field(default_factory=list)
    missing_ids: list[str] = Field(default_factory=list)
    context_status: ContextStatus


class FilterDecision(str, Enum):
    extract = "extract"
    reject = "reject"
    defer = "defer"


class FilterAssessment(Contract):
    source_id: str
    decision: FilterDecision
    reason_code: str = Field(min_length=1)
    engineering_score: float | None = None
    topic: str | None = None
    probabilities: dict[str, float] = Field(default_factory=dict)
    model: str
    question_version: str
    policy_version: str
    raw_response_ref: str | None = None
    bypass: bool = False

    @field_validator("probabilities")
    @classmethod
    def bounded_probabilities(cls, values: dict[str, float]) -> dict[str, float]:
        if any(not 0 <= p <= 1 for p in values.values()):
            raise ValueError("probabilities must be between 0 and 1")
        return values


class ClaimType(str, Enum):
    recommendation = "recommendation"
    observation = "observation"
    experiment = "experiment"
    hypothesis = "hypothesis"
    opinion = "opinion"
    limitation = "limitation"


class Evidence(Contract):
    source_id: str
    quote: str = Field(min_length=1)
    start: int | None = Field(default=None, ge=0)
    end: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def offsets_valid(self):
        if (self.start is None) != (self.end is None):
            raise ValueError("offsets must be provided together")
        if self.end is not None and self.end <= self.start:
            raise ValueError("end must be greater than start")
        return self


class Claim(Contract):
    claim_id: str = Field(min_length=1)  # stable source + extraction slot, not paraphrase hash
    source_ids: list[str] = Field(min_length=1)
    text: str = Field(min_length=1)
    kind: ClaimType
    evidence: list[Evidence] = Field(min_length=1)
    scope: str | None = None
    conditions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    technology: str | None = None
    interpretation: str | None = None

    @model_validator(mode="after")
    def evidence_belongs_to_sources(self):
        if any(e.source_id not in self.source_ids for e in self.evidence):
            raise ValueError("evidence source must be listed in source_ids")
        return self


class VerificationRelation(str, Enum):
    supports = "supports"
    contradicts = "contradicts"
    unsupported = "unsupported"
    uncertain = "uncertain"


class VerificationResult(Contract):
    claim_id: str
    quote_matches: bool
    relation: VerificationRelation
    source_supported: bool
    independently_validated: bool = False
    reason: str
    evidence: list[Evidence] = Field(default_factory=list)
    model: str | None = None
    prompt_version: str | None = None
    response_ref: str | None = None


class IntegrationOperation(str, Enum):
    enrich = "enrich"
    add_evidence = "add_evidence"
    create = "create"
    record_conflict = "record_conflict"
    duplicate = "duplicate"
    defer = "defer"


class NotePatch(Contract):
    note_id: str
    relative_path: str  # publisher validates allowlist, symlinks and path safety
    section: str | None = None
    claim_ids: list[str] = Field(min_length=1)
    base_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    proposed_content: str = Field(min_length=1)


class IntegrationDecision(Contract):
    operation: IntegrationOperation
    claim_ids: list[str] = Field(min_length=1)
    candidate_note_ids: list[str] = Field(default_factory=list)
    rationale: str
    patch: NotePatch | None = None
    conflicting_claim_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def patch_matches_claims(self):
        if self.patch and not set(self.patch.claim_ids).issubset(self.claim_ids):
            raise ValueError("patch claim IDs must belong to decision")
        return self


class StageStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    rejected = "rejected"
    deferred = "deferred"
    error = "error"


class StageRecord(Contract):
    status: StageStatus
    artifact_refs: list[str] = Field(default_factory=list)
    error: str | None = None
    attempts: int = Field(default=0, ge=0)


class RunManifest(Contract):
    run_id: str = Field(min_length=1)
    created_at: datetime
    code_version: str
    prompt_versions: dict[str, str] = Field(default_factory=dict)
    model_versions: dict[str, str] = Field(default_factory=dict)
    policy_version: str
    input_hashes: dict[str, str] = Field(default_factory=dict)
    stages: dict[str, StageRecord] = Field(default_factory=dict)
    token_count: int | None = Field(default=None, ge=0)
    cost: float | None = Field(default=None, ge=0)
    duration_seconds: float | None = Field(default=None, ge=0)
    publication_plan_ref: str | None = None
    backup_ref: str | None = None
