"""Local gate. Obvious junk is code. CLM only judges the author's own text."""

from __future__ import annotations

import re

from .assemble import AssembledPost
from .decisions import CATEGORIES
from .thresholds import DEFAULT_THRESHOLDS

_REACTION = frozenset({
    "this", "that", "same", "agreed", "agree", "exactly", "yes", "yeah", "yep", "yup",
    "no", "nah", "nope", "lol", "lmao", "lmfao", "haha", "hahaha", "wow", "nice", "cool",
    "based", "true", "facts", "fact", "thanks", "thank", "ty", "gm", "gn", "following",
    "follow", "congrats", "congratulations", "interesting", "insane", "huge", "fire",
    "goat", "real", "mood", "ok", "okay", "sure", "right", "indeed", "totally",
    "absolutely", "wild", "crazy", "bro", "sir", "ratio", "sameee", "xd", "hehe",
    "tak", "nie", "dzięki", "dzieki", "super", "ekstra", "brawo", "gratulacje",
    "dokładnie", "dokladnie", "prawda", "spoko", "git", "no", "aha", "mhm",
    "哈哈", "哈哈哈", "笑死", "确实", "对", "牛", "赞", "谢谢", "同意",
})
_URL = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_WORD = re.compile(r"[^\W\d_]{2,}", re.UNICODE)


def screen_focus(assembled: AssembledPost) -> tuple[str, str] | None:
    """Reject obvious non-claims before spending a model call. None means the model may judge."""
    focus = assembled.focus_evidence.strip()
    if not focus:
        return "reject", "empty_focus"
    cleaned = _URL.sub(" ", focus)
    cleaned = re.sub(r"@\w+", " ", cleaned).replace("#", " ")
    words = _WORD.findall(cleaned)
    if not words:
        return "reject", "link_only" if _URL.search(focus) else "empty_focus"
    if all(word.casefold() in _REACTION for word in words):
        return "reject", "reaction_only"
    return None


# Reject bars measured on clm-latest, 2026-09-19, focus text only, default noul wording.
# A real rule in English and Polish stayed above 0.50. A Chinese rule was 0.39.
# Reactions and thanks stayed under 0.26. Hiring and course ads scored promo above 0.93.
# These bars only reject. Anything clearer goes to Jev.
#
# ``thresholds.DEFAULT_THRESHOLDS`` is the single definition site of these three
# values. The names below stay as the public spelling of this module and are
# bound to that owner, so there is no second copy to drift. No model policy
# changed: the numbers are the same ones the code used before.
CLAIM_REJECT = DEFAULT_THRESHOLDS["focus_claim_reject"]
PROMO_REJECT = DEFAULT_THRESHOLDS["promotion_reject"]
CATEGORY_CONFIDENCE = DEFAULT_THRESHOLDS["category_confidence"]


def filter_questions() -> dict[str, dict]:
    return {
        "focus_claim": {
            "type": "noul",
            "instructions": (
                "Does this text, in any language, tell an implementer a concrete rule, "
                "limit, procedure, mechanism, or result they can apply?"
            ),
        },
        "promotion": {
            "type": "noul",
            "instructions": (
                "Is this text mainly asking the reader to buy, apply, follow, subscribe, "
                "or wait for a launch, rather than explaining how to build or operate a system?"
            ),
        },
    }


def category_question() -> dict[str, dict]:
    return {
        "category": {
            "type": "choice",
            "instructions": "Which single knowledge-base category fits this text?",
            "criteria": {
                "Pojęcia": "A mechanism, concept, or model behavior.",
                "Procesy": "A procedure, decision criterion, or validation method.",
                "Narzędzia": "A concrete tool, library, or product and how it is used.",
                "Zasady": "A rule, heuristic, or prohibition about when to apply something.",
            },
        }
    }


PROMOTION_MODES = ("advisory", "reject")
DEFAULT_PROMOTION_MODE = "advisory"
PROMOTION_ADVISORY_REASON = "clm_promotion_advisory"


def resolve_promotion_mode(value: str | None) -> str:
    """Validate a promotion mode; None or empty means the default (advisory)."""
    mode = (value or DEFAULT_PROMOTION_MODE).strip().lower()
    if mode not in PROMOTION_MODES:
        raise ValueError(f"clm promotion mode must be one of {', '.join(PROMOTION_MODES)}")
    return mode


class CategoryUncertain(ValueError):
    """CLM could not pick a category with enough confidence. A defer, not a failure."""


def decide_clm(
    response: dict,
    *,
    focus_claim_reject: float = CLAIM_REJECT,
    promotion_reject: float = PROMO_REJECT,
    promotion_mode: str = "reject",
) -> tuple[str, str]:
    """Code owns the threshold. CLM does not return keep or drop.

    ``promotion_mode="reject"`` keeps the historical hard reject. ``"advisory"``
    never rejects on the promotion score: a high score is reported as
    ``clm_promotion_advisory`` (status keep) and Jev decides. The run pipeline
    defaults to advisory; this function keeps ``reject`` so the offline flow and its
    manifest are unchanged.
    """
    promotion_mode = resolve_promotion_mode(promotion_mode)
    if not isinstance(response, dict):
        return "defer", "local_filter_invalid"
    answers = response.get("answers")
    if not isinstance(answers, dict):
        return "defer", "local_filter_invalid"
    claim = _noul(answers.get("focus_claim"))
    promo = _noul(answers.get("promotion"))
    if claim is None or promo is None:
        return "defer", "local_filter_invalid"
    promoted = promo >= promotion_reject
    if promoted and promotion_mode == "reject":
        return "reject", "promotion"
    if claim < focus_claim_reject:
        return "reject", "low_focus_claim"
    if promoted:
        return "keep", PROMOTION_ADVISORY_REASON
    return "keep", "clm_focus_claim"


def category_from_clm(response: dict, *, category_confidence: float = CATEGORY_CONFIDENCE) -> str:
    answers = response.get("answers") if isinstance(response, dict) else None
    answer = answers.get("category") if isinstance(answers, dict) else None
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        raise ValueError("kategoria CLM jest niekompletna")
    choice = answer.get("choice")
    confidence = answer.get("confidence")
    if choice not in CATEGORIES or isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("kategoria CLM jest niekompletna")
    if float(confidence) < category_confidence:
        raise CategoryUncertain("category_uncertain")
    return str(choice)


def _noul(answer: object) -> float | None:
    if not isinstance(answer, dict) or answer.get("type") != "noul":
        return None
    value = answer.get("noul")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    if not 0 <= number <= 1:
        return None
    return number
