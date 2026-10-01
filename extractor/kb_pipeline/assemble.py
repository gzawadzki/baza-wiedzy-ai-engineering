"""Build the text a filter may see: post, thread, and image text. No guessed parents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import urlparse

PHOTO_TYPES = {"photo", "image"}
STILL_TYPES = PHOTO_TYPES | {"animated_gif"}
ALLOWED_IMAGE_HOSTS = frozenset({"pbs.twimg.com", "ton.twimg.com"})


@dataclass(frozen=True)
class RelatedPiece:
    """A parent, thread ancestor, or quoted post kept apart from the author's own text."""

    source_id: str
    role: str  # "parent" | "thread" | "quote"
    author: str
    text: str
    provenance: str  # cache:index | cache:fetch | actor:replyTo | actor:quotedTweet
    url: str | None = None
    published_at: str | None = None
    reply_to_id: str | None = None
    quoted_source_id: str | None = None


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
    related: list[RelatedPiece] = field(default_factory=list)
    reply_to_id: str | None = None
    conversation_id: str | None = None
    quoted_source_id: str | None = None


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


def _conversation_id(item: dict[str, Any]) -> str | None:
    value = item.get("conversation_id") or item.get("conversationId")
    text = str(value) if value is not None else ""
    return text if text.isdigit() else None


def _created_at(item: dict[str, Any]) -> str | None:
    value = item.get("created_at") or item.get("createdAt")
    return value if isinstance(value, str) and value.strip() else None


def _piece_author(item: dict[str, Any]) -> str | None:
    value = item.get("username") or item.get("author") or item.get("screen_name")
    return str(value) if isinstance(value, str) and value.strip() else None


def _piece_url(item: dict[str, Any], source_id: str, author: str | None) -> str | None:
    value = item.get("url") or item.get("twitterUrl")
    if isinstance(value, str) and value.strip():
        return value.strip()
    if author and source_id.isdigit():
        return f"https://x.com/{author}/status/{source_id}"
    return None


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
    chain: list[tuple[dict[str, Any], str]] = []
    missing: list[str] = []
    seen = {tweet_id(item)}
    current = _reply_id(item)
    depth = 0
    while current:
        depth += 1
        if current in seen:
            # a known id that is already available in the chain, not a missing source
            break
        if depth > max_depth:
            missing.append(current)
            break
        seen.add(current)
        parent = by_id.get(current)
        provenance = "cache:index"
        if parent is None and fetch_status is not None:
            fetched = fetch_status(current)
            if isinstance(fetched, dict) and tweet_id(fetched) == current:
                parent = fetched
                provenance = "cache:fetch"
                by_id[current] = fetched
        if parent is None:
            reply = item.get("replyTo") if depth == 1 and isinstance(item.get("replyTo"), dict) else None
            inline = _text(reply) if isinstance(reply, dict) and str(reply.get("id") or current) == current else ""
            if inline:
                chain.append((
                    {
                        "id": current,
                        "username": reply.get("username") or reply.get("screen_name"),
                        "full_text": inline,
                    },
                    "actor:replyTo",
                ))
                break
            missing.append(current)
            break
        chain.append((parent, provenance))
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
    quote_provenance = "cache:index"
    if quote_id and quote is None and fetch_status is not None:
        fetched = fetch_status(quote_id)
        if isinstance(fetched, dict) and tweet_id(fetched) == quote_id:
            quote = fetched
            quote_provenance = "cache:fetch"
    if quote_id and quote is None:
        quoted = item.get("quotedTweet") if isinstance(item.get("quotedTweet"), dict) else None
        inline = _text(quoted) if isinstance(quoted, dict) else ""
        if inline and str(quoted.get("id") or quote_id) == quote_id:
            quote = {"id": quote_id, "username": quoted.get("username"), "full_text": inline}
            quote_provenance = "actor:quotedTweet"
        elif quote_id not in missing:
            missing.append(quote_id)

    del ocr_url  # images are ignored; the argument stays so older callers do not break
    image_count = sum(
        len(image_refs(piece)) for piece in [*[parent for parent, _ in ancestors], item, *([quote] if quote else [])]
    )
    context_parts = [_render_piece(parent, "watek") for parent, _ in ancestors]
    if quote is not None:
        context_parts.append(_render_piece(quote, "cytat"))
    parts = [*context_parts, _render_piece(item, "wpis")]
    if missing:
        parts.append("[BRAK KONTEKSTU] " + ", ".join(missing))
    author = item.get("username") or handle
    url = item.get("url") or item.get("twitterUrl") or f"https://x.com/{author}/status/{found}"
    published = _created_at(item)

    related: list[RelatedPiece] = []
    last_parent = len(ancestors) - 1
    for position, (piece, provenance) in enumerate(ancestors):
        piece_id = tweet_id(piece)
        if not piece_id:
            continue
        piece_author = _piece_author(piece)
        related.append(RelatedPiece(
            source_id=f"x:{piece_id}",
            role="parent" if position == last_parent else "thread",
            author=piece_author or "nieznany",
            text=_text(piece),
            provenance=provenance,
            url=_piece_url(piece, piece_id, piece_author),
            published_at=_created_at(piece),
            reply_to_id=_reply_id(piece),
            quoted_source_id=_quote_id(piece),
        ))
    if quote is not None and quote_id:
        quote_author = _piece_author(quote)
        related.append(RelatedPiece(
            source_id=f"x:{quote_id}",
            role="quote",
            author=quote_author or "nieznany",
            text=_text(quote),
            provenance=quote_provenance,
            url=_piece_url(quote, quote_id, quote_author),
            published_at=_created_at(quote),
            reply_to_id=_reply_id(quote),
            quoted_source_id=_quote_id(quote),
        ))
    return AssembledPost(
        source_id=f"x:{found}",
        author=str(author),
        url=str(url),
        published_at=published,
        is_reply=bool(_reply_id(item) or missing),
        document="\n\n".join(parts),
        missing_ids=missing,
        ocr_status="ignored" if image_count else "not_needed",
        image_count=image_count,
        focus_evidence=focus_evidence(item),
        context_text="\n\n".join(context_parts),
        related=related,
        reply_to_id=f"x:{_reply_id(item)}" if _reply_id(item) else None,
        conversation_id=f"x:{_conversation_id(item)}" if _conversation_id(item) else None,
        quoted_source_id=f"x:{quote_id}" if quote_id else None,
    )
