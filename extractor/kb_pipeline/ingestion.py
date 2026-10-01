"""Offline normalization of the existing Apify JSON caches (no provider calls)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .schemas import ContextStatus, SourceRecord


def _id(value: Any) -> str | None:
    if value is None or value == "":
        return None
    value = str(value)
    return f"x:{value}" if value.isdigit() else None


def _published(value: Any) -> datetime | None:
    if not value:
        return None
    for fmt in ("%a %b %d %H:%M:%S %z %Y",):
        try:
            return datetime.strptime(value, fmt)
        except (ValueError, TypeError):
            pass
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result if result.tzinfo else result.replace(tzinfo=timezone.utc)
    except (ValueError, AttributeError):
        return None


def normalize(item: dict[str, Any], *, handle: str, fetched_at: datetime, raw_ref: str) -> SourceRecord:
    source_id = _id(item.get("id") or item.get("id_str") or item.get("tweet_id"))
    if source_id is None:
        raise ValueError("missing or invalid stable tweet ID")
    text = item.get("full_text") or item.get("text") or item.get("displayText")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("missing text")
    author = item.get("username") or handle
    reply = item.get("replyTo")
    quote = item.get("quotedTweet")
    reply_id = _id(item.get("in_reply_to_status_id") or item.get("inReplyToStatusId") or (reply.get("id") if isinstance(reply, dict) else None))
    quote_id = _id(item.get("quoted_status_id") or item.get("quotedStatusId") or (quote.get("id") if isinstance(quote, dict) else None))
    conversation = _id(item.get("conversation_id") or item.get("conversationId"))
    # No context is considered complete merely because the actor returned relation IDs.
    status = ContextStatus.partial if reply_id or quote_id or (conversation and conversation != source_id) else ContextStatus.unavailable
    url = item.get("url") or item.get("twitterUrl") or f"https://x.com/{author}/status/{source_id[2:]}"
    published_at = _published(item.get("created_at") or item.get("createdAt"))
    payload = {"author": author, "text": text, "published_at": published_at.isoformat() if published_at else None,
               "reply_to_id": reply_id, "conversation_id": conversation, "quoted_source_id": quote_id, "url": url}
    content_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    return SourceRecord(source_id=source_id, author=author, url=url, text=text, published_at=published_at,
                        fetched_at=fetched_at, language=item.get("lang"), reply_to_id=reply_id,
                        conversation_id=conversation, quoted_source_id=quote_id, raw_ref=raw_ref,
                        content_hash=content_hash, context_status=status)


def read_cache(path: Path):
    """Yield records or per-item errors; never silently discard a short reply."""
    items = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(items, list):
        raise ValueError("cache must contain a JSON list")
    fetched_at = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
    handle = path.name.removesuffix("_raw_tweets.json")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            yield index, None, item, "not a JSON object"
            continue
        try:
            record = normalize(item, handle=handle, fetched_at=fetched_at, raw_ref=f"cache:{path.name}:{index}")
            yield index, record, item, None
        except ValueError as exc:
            yield index, None, item, str(exc)
