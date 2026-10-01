"""Deterministic assessment of TypeSafe filter answers."""

from __future__ import annotations

import math

from .schemas import ContextBundle, FilterAssessment, FilterDecision


_LOW_USE_CONFIDENCE = 0.2
_TOPIC_OPTIONS = frozenset({"compaction", "evals", "harness", "other"})


def _finite_probability(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number")
    try:
        probability = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{field} must be a finite probability") from exc
    if not math.isfinite(probability) or not 0 <= probability <= 1:
        raise ValueError(f"{field} must be finite and between 0 and 1")
    return probability


def _noul(answer: object, field: str) -> float:
    if not isinstance(answer, dict) or answer.get("type") != "noul":
        raise ValueError(f"{field} must be a noul answer")
    if "noul" not in answer:
        raise ValueError(f"{field}.noul is required")
    return _finite_probability(answer["noul"], f"{field}.noul")


def _topic(answer: object) -> tuple[str, dict[str, float]]:
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        raise ValueError("answers.topic must be a choice answer")

    choice = answer.get("choice")
    if not isinstance(choice, str) or choice not in _TOPIC_OPTIONS:
        raise ValueError("answers.topic.choice is not an expected topic")

    raw_probabilities = answer.get("probabilities")
    if not isinstance(raw_probabilities, dict) or set(raw_probabilities) != _TOPIC_OPTIONS:
        raise ValueError("answers.topic.probabilities has unexpected topic labels")

    probabilities = {
        label: _finite_probability(value, f"answers.topic.probabilities.{label}")
        for label, value in raw_probabilities.items()
    }
    if not math.isclose(
        math.fsum(probabilities.values()), 1.0, rel_tol=1e-6, abs_tol=1e-6
    ):
        raise ValueError("answers.topic.probabilities must sum to one")

    if "confidence" not in answer:
        raise ValueError("answers.topic.confidence is required")
    _finite_probability(answer["confidence"], "answers.topic.confidence")
    return choice, probabilities


def assess_filter(
    bundle: ContextBundle,
    response: dict,
    *,
    usefulness_threshold: float = 0.7,
    context_threshold: float = 0.6,
    question_version: str = "v1",
    policy_version: str = "v1",
    raw_response_ref: str | None = None,
) -> FilterAssessment:
    usefulness_threshold = _finite_probability(
        usefulness_threshold, "usefulness_threshold"
    )
    context_threshold = _finite_probability(context_threshold, "context_threshold")

    if not isinstance(response, dict):
        raise ValueError("TypeSafe response must be an object")

    model = response.get("model")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("TypeSafe response model is required")

    answers = response.get("answers")
    if not isinstance(answers, dict):
        raise ValueError("TypeSafe response answers must be an object")

    engineering_value = _noul(
        answers.get("engineering_value"), "answers.engineering_value"
    )
    context_sufficient = _noul(
        answers.get("context_sufficient"), "answers.context_sufficient"
    )
    topic, topic_probabilities = _topic(answers.get("topic"))

    if context_sufficient < context_threshold:
        decision = FilterDecision.defer
        reason_code = "insufficient_context"
    elif engineering_value >= usefulness_threshold:
        decision = FilterDecision.extract
        reason_code = "sufficient_value_and_context"
    elif engineering_value <= _LOW_USE_CONFIDENCE:
        decision = FilterDecision.reject
        reason_code = "low_engineering_value"
    else:
        decision = FilterDecision.defer
        reason_code = "borderline_engineering_value"

    probabilities = {
        "engineering_value": engineering_value,
        "context_sufficient": context_sufficient,
        **topic_probabilities,
    }
    return FilterAssessment(
        source_id=bundle.focus.source_id,
        decision=decision,
        reason_code=reason_code,
        engineering_score=engineering_value,
        topic=topic,
        probabilities=probabilities,
        model=model,
        question_version=question_version,
        policy_version=policy_version,
        raw_response_ref=raw_response_ref,
        bypass=False,
    )
