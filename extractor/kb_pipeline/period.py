"""Date window for fetched posts. Missing dates stay missing."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any


def parse_day(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("okres musi mieć postać YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise ValueError("okres musi mieć postać YYYY-MM-DD")
    return parsed


def published_at(item: dict[str, Any]) -> datetime | None:
    value = item.get("created_at") or item.get("createdAt")
    if not value or not isinstance(value, str):
        return None
    for parser in (
        lambda raw: datetime.strptime(raw, "%a %b %d %H:%M:%S %z %Y"),
        lambda raw: datetime.fromisoformat(raw.replace("Z", "+00:00")),
    ):
        try:
            parsed = parser(value)
        except (ValueError, TypeError):
            continue
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


def in_period(item: dict[str, Any], *, since: date | None, until: date | None) -> bool:
    """Inclusive start, exclusive end. A missing publication date is not today."""
    published = published_at(item)
    if published is None:
        return False
    day = published.date()
    if since is not None and day < since:
        return False
    if until is not None and day >= until:
        return False
    return True
