"""Single definition point for decision thresholds.

The values are exactly the ones already hardcoded in ``local_gate.py``
(``CLAIM_REJECT``, ``PROMO_REJECT``, ``CATEGORY_CONFIDENCE``) and in the Jev
settings. Moving them here is a reorganisation, **not a change of contract**:
every default equals the previous constant.

Thresholds are decision inputs only. They are recorded in the run manifest and
are deliberately **not** part of any stage cache key, so changing a threshold
recomputes a decision from cached raw provider output instead of paying for a new
provider call.

Thresholds recorded here are operational bars measured on a probe run, not a
measured guarantee of quality.
"""

from __future__ import annotations

import hashlib
import json
from typing import Mapping

DEFAULT_THRESHOLDS: Mapping[str, float] = {
    # local_gate.CLAIM_REJECT
    "focus_claim_reject": 0.30,
    # local_gate.PROMO_REJECT
    "promotion_reject": 0.75,
    # local_gate.CATEGORY_CONFIDENCE
    "category_confidence": 0.50,
    # filtering.assess_filter defaults for the Jev usefulness question
    "jev_usefulness": 0.70,
    # filtering.assess_filter defaults for the context sufficiency question
    "jev_context": 0.60,
    # filtering._LOW_USE_CONFIDENCE: below this the source is rejected outright
    "jev_low_use": 0.20,
    # routing-only topic label; never a category decision
    "jev_topic_routing": 0.20,
}

_THRESHOLD_PROVENANCE: Mapping[str, str] = {
    "focus_claim_reject": "clm-latest probe 2026-09-19 (local_gate comment); not a measured guarantee",
    "promotion_reject": "clm-latest probe 2026-09-19 (local_gate comment); not a measured guarantee",
    "category_confidence": "clm-latest category probe; not a measured guarantee",
    "jev_usefulness": "Jev default setting; not a measured guarantee",
    "jev_context": "Jev default setting; not a measured guarantee",
    "jev_low_use": "filtering._LOW_USE_CONFIDENCE default; not a measured guarantee",
    "jev_topic_routing": "routing-only topic label, never a category decision",
}


def resolve_thresholds(overrides: Mapping[str, float] | None = None) -> dict[str, float]:
    """Return the effective thresholds; unknown keys are rejected."""
    resolved = dict(DEFAULT_THRESHOLDS)
    for key, value in (overrides or {}).items():
        if key not in DEFAULT_THRESHOLDS:
            raise ValueError(f"Unknown threshold '{key}'")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"Threshold '{key}' must be numeric")
        if not 0 <= float(value) <= 1:
            raise ValueError(f"Threshold '{key}' must be between 0 and 1")
        resolved[key] = float(value)
    return resolved


def thresholds_fingerprint(thresholds: Mapping[str, float]) -> str:
    """Stable sha256 over the effective thresholds, for the manifest only."""
    payload = json.dumps(
        {key: round(float(value), 6) for key, value in sorted(thresholds.items())},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def thresholds_manifest(thresholds: Mapping[str, float]) -> dict[str, object]:
    """Manifest block: effective values, fingerprint and per-threshold provenance."""
    return {
        "values": {key: float(value) for key, value in sorted(thresholds.items())},
        "fingerprint": thresholds_fingerprint(thresholds),
        "provenance": dict(_THRESHOLD_PROVENANCE),
        "note": (
            "Thresholds are operational bars, not a measured quality guarantee, "
            "and are not part of any stage cache key."
        ),
    }
