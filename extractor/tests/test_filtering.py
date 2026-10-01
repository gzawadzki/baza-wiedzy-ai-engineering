from copy import deepcopy
from datetime import datetime, timezone

import pytest

from kb_pipeline.filtering import assess_filter
from kb_pipeline.schemas import (
    ContextBundle,
    ContextItem,
    ContextStatus,
    FilterDecision,
    SourceRecord,
)


TOPIC_OPTIONS = ("compaction", "evals", "harness", "other")


def make_source(**overrides) -> SourceRecord:
    values = {
        "source_id": "x:100",
        "author": "tester",
        "text": "A concrete source",
        "fetched_at": datetime.now(timezone.utc),
        "raw_ref": "cache:fixture:filter",
        "content_hash": "b" * 64,
    }
    return SourceRecord(**(values | overrides))


def make_bundle(**overrides) -> ContextBundle:
    values = {
        "focus": make_source(),
        "related": [],
        "missing_ids": [],
        "context_status": ContextStatus.complete,
    }
    return ContextBundle(**(values | overrides))


def make_topic(
    choice: str = "harness",
    probabilities: dict[str, float] | None = None,
    confidence: float = 1.0,
) -> dict:
    if probabilities is None:
        probabilities = dict.fromkeys(TOPIC_OPTIONS, 0.0)
        probabilities[choice] = 1.0
    return {
        "type": "choice",
        "choice": choice,
        "probabilities": probabilities,
        "confidence": confidence,
    }


def make_response(
    *,
    engineering_value=0.91,
    context_sufficient=0.84,
    topic: dict | None = None,
    **overrides,
) -> dict:
    values = {
        "model": "jev-1.13.0",
        "answers": {
            "engineering_value": {"type": "noul", "noul": engineering_value},
            "context_sufficient": {
                "type": "noul",
                "noul": context_sufficient,
            },
            "topic": make_topic() if topic is None else topic,
        },
    }
    return values | overrides


def test_assessment_keeps_topic_distribution_and_run_metadata():
    probabilities = {
        "compaction": 0.12,
        "evals": 0.13,
        "harness": 0.17,
        "other": 0.58,
    }
    bundle = make_bundle()
    response = make_response(
        model="jev-1.14.1",
        engineering_value=0.88,
        context_sufficient=0.79,
        topic=make_topic("other", probabilities, confidence=0.31),
    )

    result = assess_filter(
        bundle,
        response,
        question_version="questions-2026-09",
        policy_version="policy-2026-09",
        raw_response_ref="raw:filter:42",
    )

    assert result.source_id == bundle.focus.source_id
    assert result.decision is FilterDecision.extract
    assert result.engineering_score == 0.88
    assert result.topic == "other"
    assert result.model == "jev-1.14.1"
    assert result.probabilities == {
        "engineering_value": 0.88,
        "context_sufficient": 0.79,
        **probabilities,
    }
    assert result.question_version == "questions-2026-09"
    assert result.policy_version == "policy-2026-09"
    assert result.raw_response_ref == "raw:filter:42"
    assert result.bypass is False


def test_context_judgment_drives_a_very_short_reply():
    focus = make_source(source_id="x:101", text="Exactly.", reply_to_id="x:102")
    parent = make_source(source_id="x:102", text="Use a canary before shifting all traffic.")
    bundle = make_bundle(
        focus=focus,
        related=[
            ContextItem(source=parent, role="parent", provenance="cache:fixture")
        ],
    )

    result = assess_filter(bundle, make_response())

    assert result.decision is FilterDecision.extract
    assert result.engineering_score == 0.91
    assert result.topic == "harness"


def test_an_unavailable_context_label_does_not_override_sufficient_judgment():
    bundle = make_bundle(
        focus=make_source(source_id="x:103", reply_to_id="x:999"),
        missing_ids=["x:999"],
        context_status=ContextStatus.unavailable,
    )
    response = make_response(
        engineering_value=0.83,
        context_sufficient=0.92,
        topic=make_topic(
            "other",
            {"compaction": 0.1, "evals": 0.1, "harness": 0.4, "other": 0.4},
            confidence=0.2,
        ),
    )

    result = assess_filter(bundle, response)

    assert result.decision is FilterDecision.extract
    assert result.topic == "other"
    assert result.probabilities["other"] == 0.4


@pytest.mark.parametrize(
    ("engineering_value", "context_sufficient", "expected"),
    [
        (0.12, 0.94, FilterDecision.reject),
        (0.2, 0.91, FilterDecision.reject),
        (0.21, 0.93, FilterDecision.defer),
        (0.69, 0.92, FilterDecision.defer),
        (0.91, 0.59, FilterDecision.defer),
        (0.12, 0.41, FilterDecision.defer),
    ],
)
def test_probability_bands_select_the_expected_route(
    engineering_value, context_sufficient, expected
):
    response = make_response(
        engineering_value=engineering_value,
        context_sufficient=context_sufficient,
        topic=make_topic(
            "other",
            {"compaction": 0.1, "evals": 0.1, "harness": 0.4, "other": 0.4},
            confidence=0.1,
        ),
    )

    assert assess_filter(make_bundle(), response).decision is expected


def test_changing_the_cutoffs_reuses_an_unchanged_payload():
    response = make_response(
        engineering_value=0.8,
        context_sufficient=0.8,
        topic=make_topic(
            "harness",
            {"compaction": 0.1, "evals": 0.1, "harness": 0.8, "other": 0.0},
            confidence=0.8,
        ),
    )
    original = deepcopy(response)

    baseline = assess_filter(make_bundle(), response, policy_version="baseline")
    stricter = assess_filter(
        make_bundle(),
        response,
        usefulness_threshold=0.9,
        context_threshold=0.7,
        policy_version="stricter",
    )

    assert baseline.decision is FilterDecision.extract
    assert baseline.policy_version == "baseline"
    assert stricter.decision is FilterDecision.defer
    assert stricter.policy_version == "stricter"
    assert response == original


def test_default_thresholds_include_their_boundary_values():
    response = make_response(
        engineering_value=0.7,
        context_sufficient=0.6,
        topic=make_topic(
            "compaction",
            {"compaction": 1.0, "evals": 0.0, "harness": 0.0, "other": 0.0},
            confidence=0.9,
        ),
    )

    assert assess_filter(make_bundle(), response).decision is FilterDecision.extract


@pytest.mark.parametrize(
    "probabilities",
    [
        pytest.param(
            {"compaction": 0.7, "evals": 0.1, "harness": 0.1, "other": 0.05},
            id="not-normalized",
        ),
        pytest.param(
            {
                "compaction": 0.25,
                "evals": 0.25,
                "harness": 0.25,
                "engineering_value": 0.25,
            },
            id="reserved-label",
        ),
        pytest.param(
            {"compaction": 0.5, "evals": 0.5},
            id="missing-label",
        ),
    ],
)
def test_malformed_topic_distributions_are_rejected(probabilities):
    response = make_response(topic=make_topic("other", probabilities))

    with pytest.raises(ValueError, match="probabilities"):
        assess_filter(make_bundle(), response)


def test_topic_distribution_accepts_normalized_rounding():
    probabilities = {
        "compaction": 0.1,
        "evals": 0.2,
        "harness": 0.3000004,
        "other": 0.3999996,
    }
    response = make_response(topic=make_topic("other", probabilities, confidence=0.1))

    result = assess_filter(make_bundle(), response)

    assert result.topic == "other"
    assert result.probabilities["other"] == probabilities["other"]


@pytest.mark.parametrize(
    "response",
    [
        {},
        {"model": "jev-1.13.0"},
        make_response(
            engineering_value={"type": "noul", "confidence": 0.9}
        ),
        make_response(engineering_value=float("nan")),
        make_response(context_sufficient=float("inf")),
        make_response(topic={"type": "noul", "noul": 0.7}),
        make_response(
            topic=make_topic(
                "other",
                {
                    "compaction": 0.4,
                    "evals": 0.3,
                    "harness": 0.3,
                    "other": float("nan"),
                },
            )
        ),
        make_response(
            topic=make_topic(
                "missing_label",
                {"compaction": 0.25, "evals": 0.25, "harness": 0.25, "other": 0.25},
            )
        ),
        make_response(
            topic={
                "type": "choice",
                "choice": "other",
                "probabilities": {
                    "compaction": 0.25,
                    "evals": 0.25,
                    "harness": 0.25,
                    "other": 0.25,
                },
            }
        ),
        make_response(
            topic=make_topic(
                "other",
                {"compaction": 0.25, "evals": 0.25, "harness": 0.25, "other": 0.25},
                confidence=float("nan"),
            )
        ),
    ],
)
def test_incomplete_or_invalid_payloads_raise_value_error(response):
    with pytest.raises(ValueError):
        assess_filter(make_bundle(), response)


def test_topic_concentration_does_not_control_extraction():
    response = make_response(
        topic=make_topic(
            "harness",
            {"compaction": 0.25, "evals": 0.25, "harness": 0.25, "other": 0.25},
            confidence=0.0,
        )
    )

    assert assess_filter(make_bundle(), response).decision is FilterDecision.extract
