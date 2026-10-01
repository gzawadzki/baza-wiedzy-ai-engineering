"""Per-stage usage measurement and the attempts/tokens budget.

Two rules the pipeline needed and did not have:

* **Usage is measured or it is unknown.** A provider that returns no usage
  block gives ``{"status": "not_measured"}``, never ``0``. Zero is a measurement;
  an absent measurement is a gap, and the gap is reported as a gap.
* **A budget is a limit and a reservation, not a cost guarantee.** The limit is
  enforced *before* the call that would exceed it, so the run stops instead of
  degrading. A reservation is only as good as what has actually been measured:
  with ``fake-offline`` providers nothing reports tokens, so the reservation is
  recorded as not measurable rather than invented.

Nothing here talks to a network. Budget accounting is provider-injected and
offline-testable.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

# Usage keys a provider may report, mirroring the Jev response contract.
_TOKEN_KEYS = ("input_tokens", "output_tokens")

MEASURED = "measured"
NOT_MEASURED = "not_measured"


class BudgetExceeded(RuntimeError):
    """A hard stop: the run must not continue past its own limit.

    This is deliberately not a ``defer`` and not an ``error`` of the content:
    the flow stops, the reason is recorded, and no degraded call is made.
    """

    def __init__(self, *, stage: str, kind: str, limit: int, observed: int) -> None:
        super().__init__(
            f"budget limit reached at stage '{stage}': {kind} limit {limit}, "
            f"already used {observed}; the run stops instead of degrading"
        )
        self.stage = stage
        self.kind = kind
        self.limit = limit
        self.observed = observed


def sanitize_usage(usage: Any) -> dict[str, int] | None:
    """Extract measurable token counts, or ``None`` when nothing was reported.

    Reuses the shape the Jev provider already returns. Only non-negative ints
    are accepted; anything else means "not measured", not zero.
    """
    if not isinstance(usage, dict):
        return None
    measured = {
        key: int(usage[key])
        for key in _TOKEN_KEYS
        if type(usage.get(key)) is int and usage.get(key) >= 0
    }
    return measured or None


@dataclass
class StageUsage:
    """Measured (or explicitly unmeasured) work done for one stage."""

    stage: str
    attempts: int = 0
    replays: int = 0
    duration_seconds: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost: float | None = None

    @property
    def tokens_measured(self) -> bool:
        return self.input_tokens is not None or self.output_tokens is not None

    @property
    def total_tokens(self) -> int | None:
        if not self.tokens_measured:
            return None
        return int(self.input_tokens or 0) + int(self.output_tokens or 0)

    def to_dict(self) -> dict[str, Any]:
        total = self.total_tokens
        return {
            "stage": self.stage,
            "attempts": self.attempts,
            "replays": self.replays,
            "duration_seconds": (
                None if self.duration_seconds is None else round(self.duration_seconds, 6)
            ),
            "tokens": (
                {
                    "status": MEASURED,
                    "input": self.input_tokens,
                    "output": self.output_tokens,
                    "total": total,
                }
                if self.tokens_measured
                else {
                    "status": NOT_MEASURED,
                    "reason": "provider returned no token usage",
                    "input": None,
                    "output": None,
                    "total": None,
                }
            ),
            "cost": (
                {"status": MEASURED, "value": self.cost}
                if self.cost is not None
                else {
                    "status": NOT_MEASURED,
                    "reason": "provider returned no cost; not a zero cost",
                }
            ),
        }


class UsageLedger:
    """Per-stage usage for one invocation. Aggregation never invents numbers."""

    def __init__(self) -> None:
        self._stages: dict[str, StageUsage] = {}
        self._order: list[str] = []

    def _entry(self, stage: str) -> StageUsage:
        if stage not in self._stages:
            self._stages[stage] = StageUsage(stage=stage)
            self._order.append(stage)
        return self._stages[stage]

    def record_call(
        self, stage: str, *, duration: float | None, usage: Any = None, cost: Any = None
    ) -> None:
        entry = self._entry(stage)
        entry.attempts += 1
        if duration is not None:
            entry.duration_seconds = (entry.duration_seconds or 0.0) + duration
        measured = sanitize_usage(usage)
        if measured is not None:
            entry.input_tokens = (entry.input_tokens or 0) + int(measured.get("input_tokens", 0))
            entry.output_tokens = (entry.output_tokens or 0) + int(measured.get("output_tokens", 0))
        if isinstance(cost, (int, float)) and not isinstance(cost, bool):
            entry.cost = round((entry.cost or 0.0) + float(cost), 6)

    def record_replay(self, stage: str) -> None:
        self._entry(stage).replays += 1

    def record_duration(self, stage: str, duration: float) -> None:
        entry = self._entry(stage)
        entry.duration_seconds = (entry.duration_seconds or 0.0) + duration

    def entry(self, stage: str) -> StageUsage:
        return self._entry(stage)

    def to_dict(self) -> dict[str, Any]:
        stages = [self._stages[stage].to_dict() for stage in self._order]
        totals = [self._stages[stage] for stage in self._order]
        measured = [entry.total_tokens for entry in totals if entry.total_tokens is not None]
        costs = [entry.cost for entry in totals if entry.cost is not None]
        durations = [
            entry.duration_seconds for entry in totals if entry.duration_seconds is not None
        ]
        attempts = sum(entry.attempts for entry in totals)
        return {
            "stages": stages,
            "totals": {
                "attempts": attempts,
                "replays": sum(entry.replays for entry in totals),
                "tokens": (
                    {"status": MEASURED, "total": sum(measured)}
                    if measured
                    else {
                        "status": NOT_MEASURED,
                        "reason": "no stage reported token usage",
                        "total": None,
                    }
                ),
                "cost": (
                    {"status": MEASURED, "value": sum(costs)}
                    if costs
                    else {
                        "status": NOT_MEASURED,
                        "reason": "no stage reported cost; not a zero cost",
                        "total": None,
                    }
                ),
                "duration_seconds": round(sum(durations), 6) if durations else None,
            },
            "note": (
                "'not_measured' means the provider did not report it. It is not a zero "
                "and not a claim about cost."
            ),
        }


@dataclass
class FlowBudget:
    """Attempts/tokens limits, enforced before the call that would exceed them.

    ``max_tokens`` is a *reservation* built from what has been measured so far.
    Two counters are kept apart: ``measured`` is what a provider actually
    reported, and ``charged`` is what the limit is applied to. A call that
    reported nothing is charged the largest measured call.

    That charge is **not** a proven upper bound. It assumes every unmeasured
    call cost no more than the largest measured one, and a provider that reports
    nothing at all has told us nothing about its cost, its size, or how many
    calls the run would want. So the limit is a guard against the spending the
    run can actually see, not a promise about the bill. The attempt limit is the
    only one that counts calls unconditionally.
    """

    max_attempts: int | None = None
    max_tokens: int | None = None
    _attempts: int = field(default=0, init=False)
    _measured: int = field(default=0, init=False)
    _charged: int = field(default=0, init=False)
    _unmeasured: int = field(default=0, init=False)
    _max_call_tokens: int = field(default=0, init=False)
    _has_measurement: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        for name, value in (("max_attempts", self.max_attempts), ("max_tokens", self.max_tokens)):
            if value is not None and (type(value) is not int or value < 0):
                raise ValueError(f"{name} must be a non-negative integer or None")

    @property
    def enabled(self) -> bool:
        return self.max_attempts is not None or self.max_tokens is not None

    @property
    def attempts_used(self) -> int:
        return self._attempts

    @property
    def measured_tokens(self) -> int | None:
        """Tokens a provider actually reported, or ``None`` while nothing was."""
        return self._measured if self._has_measurement else None

    def reservation(self) -> int:
        """Tokens reserved for the next call: the largest call measured so far."""
        return self._max_call_tokens

    def before_call(self, stage: str) -> None:
        """Refuse the call that would break a limit. Raises before any spend."""
        if self.max_attempts is not None and self._attempts >= self.max_attempts:
            raise BudgetExceeded(
                stage=stage, kind="attempts", limit=self.max_attempts, observed=self._attempts
            )
        if self.max_tokens is not None:
            reserved = self._max_call_tokens
            if self._attempts and not self._has_measurement:
                # One call was allowed to obtain a measurement. If the provider
                # still reports nothing, a token limit cannot be enforced, so the
                # run stops instead of pretending the limit holds.
                raise BudgetExceeded(
                    stage=stage,
                    kind="tokens_unmeasurable",
                    limit=self.max_tokens,
                    observed=self._attempts,
                )
            if self._charged + reserved > self.max_tokens:
                raise BudgetExceeded(
                    stage=stage,
                    kind="tokens",
                    limit=self.max_tokens,
                    observed=self._charged,
                )

    def after_call(self, stage: str, usage: Mapping[str, Any] | None) -> None:
        self._attempts += 1
        measured = sanitize_usage(usage)
        if measured is None:
            if self._has_measurement:
                # Charged the largest measured call. This narrows the limit; it
                # does not prove what the call cost.
                self._charged += self._max_call_tokens
                self._unmeasured += 1
            return
        self._has_measurement = True
        spent = int(measured.get("input_tokens", 0)) + int(measured.get("output_tokens", 0))
        self._measured += spent
        self._charged += spent
        self._max_call_tokens = max(self._max_call_tokens, spent)

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_attempts": self.max_attempts,
            "max_tokens": self.max_tokens,
            "attempts_used": self._attempts,
            "tokens_measured": (
                self.measured_tokens if self.measured_tokens is not None else NOT_MEASURED
            ),
            "tokens_charged": self._charged if self._has_measurement else NOT_MEASURED,
            "unmeasured_calls": self._unmeasured,
            "reservation_tokens": (
                self.reservation() if self._has_measurement else NOT_MEASURED
            ),
            "reservation_basis": (
                "largest measured call so far; not a bound on what an unmeasured "
                "call costs"
                if self._has_measurement
                else "not measurable: no provider reported token usage yet"
            ),
            "enforcement": "checked before each provider call; a breach stops the run",
            "unmeasurable_policy": (
                "with max_tokens set, at most one call is allowed before a measurement "
                "exists; if the provider still reports nothing the run stops, because a "
                "token limit that cannot be measured is not a limit. That one call is a "
                "known, reported exception - never a silent, unbounded probe"
            ),
            "charge_policy": (
                "a call that reports nothing is charged the largest measured call. That "
                "narrows the limit; it is a reservation, not a measured cost and not a "
                "proven upper bound"
            ),
            "not_guaranteed": (
                "no token or cost bound is proven. Only the attempts limit counts every "
                "call. Tokens are bounded solely by what providers reported; cost is "
                "unmeasured wherever a provider reports none"
            ),
            "guarantee": (
                "A limit on attempts, and a reservation on tokens built from measured "
                "calls. This is not a cost guarantee and not a proven token bound: "
                "providers that report no usage leave both unmeasured."
            ),
        }


def summarise(payloads: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Merge per-source usage payloads into one run-level manifest.

    A run covers several sources and each has its own ledger; the totals are
    summed where something was measured and stay ``not_measured`` where nothing
    was. Adding numbers is safe: nothing here invents a zero.
    """
    stages: dict[str, dict[str, Any]] = {}
    for payload in payloads:
        for stage in payload.get("stages", []):
            name = str(stage.get("stage"))
            entry = stages.get(name)
            if entry is None:
                entry = {
                    "stage": name,
                    "attempts": 0,
                    "replays": 0,
                    "duration_seconds": 0.0,
                    "tokens": {
                        "status": NOT_MEASURED,
                        "reason": "provider returned no token usage",
                        "input": None,
                        "output": None,
                        "total": None,
                    },
                    "cost": {"status": NOT_MEASURED, "reason": "not measured", "value": None},
                    "measured_calls": 0,
                    "calls": 0,
                }
                stages[name] = entry
            entry["attempts"] += int(stage.get("attempts", 0))
            entry["replays"] += int(stage.get("replays", 0))
            duration = stage.get("duration_seconds")
            if duration is not None:
                entry["duration_seconds"] = float(entry["duration_seconds"]) + float(duration)
            entry["calls"] += 1
            tokens = stage.get("tokens") or {}
            if tokens.get("status") == MEASURED:
                entry["measured_calls"] += 1
                current = entry["tokens"]
                if current.get("status") == MEASURED:
                    current["input"] = (current.get("input") or 0) + (tokens.get("input") or 0)
                    current["output"] = (current.get("output") or 0) + (tokens.get("output") or 0)
                    current["total"] = int(current["input"]) + int(current["output"])
                else:
                    current.update(
                        {
                            "status": MEASURED,
                            "input": tokens.get("input"),
                            "output": tokens.get("output"),
                            "total": tokens.get("total"),
                        }
                    )
            cost = stage.get("cost") or {}
            if cost.get("status") == MEASURED and cost.get("value") is not None:
                current_cost = entry["cost"]
                if current_cost.get("status") == MEASURED and current_cost.get("value") is not None:
                    current_cost["value"] = round(float(current_cost["value"]) + float(cost["value"]), 6)
                else:
                    entry["cost"] = {"status": MEASURED, "value": float(cost["value"])}
    ordered = list(stages.values())
    for entry in ordered:
        entry["duration_seconds"] = round(entry["duration_seconds"], 6)
        if entry["measured_calls"] < entry["calls"]:
            measured = entry["tokens"] if entry["tokens"]["status"] == MEASURED else {}
            entry["tokens"] = {
                "status": NOT_MEASURED,
                "reason": (
                    f"{entry['calls'] - entry['measured_calls']} of {entry['calls']} calls "
                    "reported no token usage; the measured ones are summed and the "
                    "unmeasured ones are not counted as zero"
                ),
                "measured_calls": entry["measured_calls"],
                "input": measured.get("input"),
                "output": measured.get("output"),
                "total": measured.get("total"),
            }
        else:
            entry.pop("measured_calls", None)
            entry.pop("calls", None)
    measured_totals = [
        entry["tokens"]["total"]
        for entry in ordered
        if entry["tokens"].get("total") is not None
    ]
    costs = [
        entry["cost"]["value"]
        for entry in ordered
        if entry["cost"].get("status") == MEASURED and entry["cost"].get("value") is not None
    ]
    durations = [entry["duration_seconds"] for entry in ordered if entry["duration_seconds"]]
    return {
        "stages": ordered,
        "totals": {
            "attempts": sum(entry["attempts"] for entry in ordered),
            "replays": sum(entry["replays"] for entry in ordered),
            "tokens": (
                {"status": MEASURED, "total": sum(measured_totals)}
                if measured_totals
                else {
                    "status": NOT_MEASURED,
                    "reason": "no stage reported token usage",
                    "total": None,
                }
            ),
            "cost": (
                {"status": MEASURED, "value": round(sum(costs), 6)}
                if costs
                else {
                    "status": NOT_MEASURED,
                    "reason": "no stage reported cost; not a zero cost",
                    "total": None,
                }
            ),
            "duration_seconds": round(sum(durations), 6) if durations else None,
        },
        "note": (
            "'not_measured' means the provider did not report it. It is not a zero "
            "and not a claim about cost."
        ),
    }


class _Timer:
    """Monotonic duration of a block, kept out of the accounting decisions."""

    def __init__(self) -> None:
        self.started = time.monotonic()

    def elapsed(self) -> float:
        return time.monotonic() - self.started
