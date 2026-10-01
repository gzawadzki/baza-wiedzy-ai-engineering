"""Build the text a filter may see: post, thread, and image text. No guessed parents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import urlparse

PHOTO_TYPES = {"photo", "image"}
STILL_TYPES = PHOTO_TYPES | {"animated_gif"}
ALLOWED_IMAGE_HOSTS = frozenset({"pbs.twimg.com", "ton.twimg.com"})


@dataclass
class ImageRef:
    url: str
    media_type: str
    alt_text: str | None = None
    label: str = "obraz"


@dataclass
class AssembledPost:
    source_id: str
    author: str
    url: str
    published_at: str | None
    is_reply: bool
    document: str
    missing_ids: list[str] = field(default_factory=list)
    ocr_status: str = "not_needed"
    image_count: int = 0
    focus_evidence: str = ""
    context_text: str = ""


def tweet_id(item: dict[str, Any]) -> str | None:
    value = item.get("id") or item.get("id_str") or item.get("tweet_id")
    if value is None:
        return None
    text = str(value)
    return text if text.isdigit() else None


def _text(item: dict[str, Any]) -> str:
    value = item.get("full_text") or item.get("text") or item.get("displayText") or ""
    return value.strip() if isinstance(value, str) else ""


def _host_ok(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in ALLOWED_IMAGE_HOSTS


def image_refs(item: dict[str, Any]) -> list[ImageRef]:
    media = item.get("media") or []
    if not isinstance(media, list):
        return []
    refs: list[ImageRef] = []
    for entry in media:
        if not isinstance(entry, dict):
            continue
        media_type = str(entry.get("type") or "")
        url = entry.get("url") or entry.get("media_url_https") or entry.get("preview_image_url")
        if not isinstance(url, str) or not _host_ok(url):
            continue
        alt = entry.get("alt_text") or entry.get("ext_alt_text")
        alt_text = alt.strip() if isinstance(alt, str) and alt.strip() else None
        if media_type in STILL_TYPES:
            refs.append(ImageRef(url=url, media_type=media_type, alt_text=alt_text, label="obraz"))
        elif media_type == "video":
            refs.append(ImageRef(url=url, media_type=media_type, alt_text=alt_text, label="miniatura-wideo"))
    return refs


def _reply_id(item: dict[str, Any]) -> str | None:
    reply = item.get("replyTo") if isinstance(item.get("replyTo"), dict) else {}
    value = item.get("in_reply_to_status_id") or item.get("inReplyToStatusId") or reply.get("id")
    text = str(value) if value is not None else ""
    return text if text.isdigit() else None


def _quote_id(item: dict[str, Any]) -> str | None:
    quote = item.get("quotedTweet") if isinstance(item.get("quotedTweet"), dict) else {}
    value = item.get("quoted_status_id") or item.get("quotedStatusId") or quote.get("id")
    text = str(value) if value is not None else ""
    return text if text.isdigit() else None


def _index(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for item in items:
        if isinstance(item, dict) and (found := tweet_id(item)):
            indexed[found] = item
    return indexed


def _ancestor_chain(
    item: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
    *,
    fetch_status: Callable[[str], dict[str, Any] | None] | None,
    max_depth: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    chain: list[dict[str, Any]] = []
    missing: list[str] = []
    seen = {tweet_id(item)}
    current = _reply_id(item)
    depth = 0
    while current:
        depth += 1
        if current in seen or depth > max_depth:
            missing.append(current)
            break
        seen.add(current)
        parent = by_id.get(current)
        if parent is None and fetch_status is not None:
            fetched = fetch_status(current)
            if isinstance(fetched, dict) and tweet_id(fetched) == current:
                parent = fetched
                by_id[current] = fetched
        if parent is None:
            reply = item.get("replyTo") if depth == 1 and isinstance(item.get("replyTo"), dict) else None
            inline = _text(reply) if isinstance(reply, dict) and str(reply.get("id") or current) == current else ""
            if inline:
                chain.append({"id": current, "username": reply.get("username") or reply.get("screen_name"), "full_text": inline, "_provenance": "actor:replyTo"})
                break
            missing.append(current)
            break
        chain.append(parent)
        current = _reply_id(parent)
    chain.reverse()
    return chain, missing


def focus_evidence(item: dict[str, Any]) -> str:
    """Author prose only. Attached images are ignored."""
    return _text(item)


def _render_piece(item: dict[str, Any], role: str) -> str:
    author = item.get("username") or item.get("author") or "nieznany"
    return "\n".join([
        f"[{role} @{author} id:{tweet_id(item) or '?'}]",
        _text(item) or "(brak tekstu wpisu)",
    ])


def assemble_post(
    item: dict[str, Any],
    *,
    handle: str,
    known_items: list[dict[str, Any]] | None = None,
    ocr_url: Callable[[str], str | None] | None = None,
    fetch_status: Callable[[str], dict[str, Any] | None] | None = None,
    max_depth: int = 8,
) -> AssembledPost:
    found = tweet_id(item)
    if not found:
        raise ValueError("brak stabilnego ID wpisu")
    by_id = _index([item, *(known_items or [])])
    ancestors, missing = _ancestor_chain(item, by_id, fetch_status=fetch_status, max_depth=max_depth)
    quote_id = _quote_id(item)
    quote = by_id.get(quote_id) if quote_id else None
    if quote_id and quote is None and fetch_status is not None:
        fetched = fetch_status(quote_id)
        if isinstance(fetched, dict) and tweet_id(fetched) == quote_id:
            quote = fetched
    if quote_id and quote is None:
        quoted = item.get("quotedTweet") if isinstance(item.get("quotedTweet"), dict) else None
        inline = _text(quoted) if isinstance(quoted, dict) else ""
        if inline and str(quoted.get("id") or quote_id) == quote_id:
            quote = {"id": quote_id, "username": quoted.get("username"), "full_text": inline}
        elif quote_id not in missing:
            missing.append(quote_id)

    del ocr_url  # images are ignored; the argument stays so older callers do not break
    image_count = sum(len(image_refs(piece)) for piece in [*ancestors, item, *([quote] if quote else [])])
    context_parts = [_render_piece(parent, "watek") for parent in ancestors]
    if quote is not None:
        context_parts.append(_render_piece(quote, "cytat"))
    parts = [*context_parts, _render_piece(item, "wpis")]
    if missing:
        parts.append("[BRAK KONTEKSTU] " + ", ".join(missing))
    author = item.get("username") or handle
    url = item.get("url") or item.get("twitterUrl") or f"https://x.com/{author}/status/{found}"
    published = item.get("created_at") or item.get("createdAt")
    return AssembledPost(
        source_id=f"x:{found}",
        author=str(author),
        url=str(url),
        published_at=published if isinstance(published, str) else None,
        is_reply=bool(_reply_id(item) or missing),
        document="\n\n".join(parts),
        missing_ids=missing,
        ocr_status="ignored" if image_count else "not_needed",
        image_count=image_count,
        focus_evidence=focus_evidence(item),
        context_text="\n\n".join(context_parts),
    )
