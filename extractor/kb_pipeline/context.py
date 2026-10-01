"""Offline context assembly for source records."""

from __future__ import annotations

from typing import Callable, Sequence

from .schemas import ContextBundle, ContextItem, ContextStatus, SourceRecord


def build_context(
    focus: SourceRecord,
    lookup: Callable[[str], SourceRecord | None],
    *,
    max_depth: int = 3,
    max_items: int = 12,
    provenance_for: Callable[[str], str] | None = None,
    extra_missing_ids: Sequence[str] | None = None,
) -> ContextBundle:
    """Assemble conversation context for a focus source record offline.

    ``focus.text`` is the author's own text. Parents, thread ancestors, and quoted
    posts live in ``related`` with their own role, author, and provenance; they are
    never merged into the focus text. ``missing_ids`` holds known source ids whose
    text could not be obtained, never guessed ids.
    """
    related: list[ContextItem] = []
    missing_ids: list[str] = []
    visited_ids: set[str] = {focus.source_id}

    def provenance(source_id: str) -> str:
        return provenance_for(source_id) if provenance_for is not None else "cache:lookup"

    def record_missing(source_id: str) -> None:
        if source_id not in missing_ids:
            missing_ids.append(source_id)

    # 1. Walk reply chain along reply_to_id
    reply_path: set[str] = {focus.source_id}
    curr_reply_id = focus.reply_to_id
    depth = 1
    while curr_reply_id is not None:
        if curr_reply_id in reply_path:
            record_missing(curr_reply_id)
            break
        if curr_reply_id in visited_ids:
            break
        if depth > max_depth or len(related) >= max_items:
            record_missing(curr_reply_id)
            break
        record = lookup(curr_reply_id)
        if record is None:
            record_missing(curr_reply_id)
            break
        visited_ids.add(record.source_id)
        visited_ids.add(curr_reply_id)
        reply_path.add(record.source_id)
        reply_path.add(curr_reply_id)
        role = "parent" if depth == 1 else "thread"
        related.append(ContextItem(source=record, role=role, provenance=provenance(record.source_id)))
        curr_reply_id = record.reply_to_id
        depth += 1

    # 2. Walk quote chain along quoted_source_id
    quote_path: set[str] = {focus.source_id}
    curr_quote_id = focus.quoted_source_id
    depth = 1
    while curr_quote_id is not None:
        if curr_quote_id in quote_path:
            record_missing(curr_quote_id)
            break
        if curr_quote_id in visited_ids:
            break
        if depth > max_depth or len(related) >= max_items:
            record_missing(curr_quote_id)
            break
        record = lookup(curr_quote_id)
        if record is None:
            record_missing(curr_quote_id)
            break
        visited_ids.add(record.source_id)
        visited_ids.add(curr_quote_id)
        quote_path.add(record.source_id)
        quote_path.add(curr_quote_id)
        related.append(ContextItem(source=record, role="quote", provenance=provenance(record.source_id)))
        curr_quote_id = record.quoted_source_id
        depth += 1

    for known_id in extra_missing_ids or ():
        record_missing(known_id)

    # Determine context status
    if not missing_ids:
        status = ContextStatus.complete
    elif related:
        status = ContextStatus.partial
    else:
        status = ContextStatus.unavailable

    return ContextBundle(
        focus=focus,
        related=related,
        missing_ids=missing_ids,
        context_status=status,
    )
