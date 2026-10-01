"""Post pipeline. Code owns the order; models only answer their stage.

Context contract: ``ContextBundle.focus.text`` is the author's own text only. Parents,
thread ancestors, and quoted posts stay in ``related`` with role, author, and
provenance. A claim quote is validated against the author's text, never against the
concatenated document.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable

from .assemble import AssembledPost, RelatedPiece, assemble_post
from .context import build_context
from .decisions import ContextCitation, ForeignQuoteError, parse_category, parse_summary
from .filtering import assess_filter
from .local_gate import decide_clm, screen_focus
from .schemas import ContextBundle, ContextStatus, FilterDecision, SourceRecord

_X_TWITTER_DATE = "%a %b %d %H:%M:%S %z %Y"


@dataclass
class FlowResult:
    source_id: str
    status: str
    reason: str
    category: str | None = None
    summary: dict[str, str | None] | None = None
    assembled: AssembledPost | None = None
    jev_topic: str | None = None
    context_citations: list[ContextCitation] = field(default_factory=list)


def process_post(
    item: dict[str, Any],
    *,
    handle: str,
    known_items: list[dict[str, Any]] | None = None,
    ocr_url: Callable[[str], str | None] | None = None,
    fetch_status: Callable[[str], dict[str, Any] | None] | None = None,
    local_filter: Callable[[AssembledPost], dict],
    jev_evaluate: Callable[[ContextBundle], dict],
    categorize: Callable[[AssembledPost], dict],
    summarize: Callable[[str, str], dict],
) -> FlowResult:
    try:
        assembled = assemble_post(
            item,
            handle=handle,
            known_items=known_items,
            ocr_url=ocr_url,
            fetch_status=fetch_status,
        )
    except ValueError as exc:
        return FlowResult(source_id="x:?", status="error", reason=str(exc))

    screened = screen_focus(assembled)
    if screened is not None:
        status, reason = screened
        return FlowResult(assembled.source_id, status, reason, assembled=assembled)
    try:
        status, reason = decide_clm(local_filter(assembled))
    except Exception as exc:
        # a provider failure is an error, never a defer
        return FlowResult(assembled.source_id, "error", f"lokalny filtr: {exc}", assembled=assembled)
    if status != "keep":
        return FlowResult(assembled.source_id, status, reason, assembled=assembled)

    bundle = _bundle(assembled)
    try:
        assessment = assess_filter(bundle, jev_evaluate(bundle))
    except Exception as exc:
        return FlowResult(assembled.source_id, "error", f"jev: {exc}", assembled=assembled)
    if assessment.decision != FilterDecision.extract:
        return FlowResult(
            assembled.source_id,
            assessment.decision.value,
            assessment.reason_code,
            assembled=assembled,
            jev_topic=assessment.topic,
        )

    try:
        category = parse_category(categorize(assembled))
    except Exception as exc:
        return FlowResult(assembled.source_id, "error", f"kategoria: {exc}", assembled=assembled, jev_topic=assessment.topic)

    related = _related_for_quote_check(bundle)
    try:
        response = summarize(assembled.focus_evidence, category)
    except Exception as exc:
        return FlowResult(
            assembled.source_id,
            "error",
            f"ekstrakcja: {exc}",
            category=category,
            assembled=assembled,
            jev_topic=assessment.topic,
        )

    try:
        summary = parse_summary(response, assembled.focus_evidence, related=related)
    except ForeignQuoteError as exc:
        citation = exc.citation
        citations = [citation] if citation is not None else []
        return FlowResult(
            assembled.source_id,
            "reject",
            f"cytat spoza tekstu autora: {exc}",
            category=category,
            assembled=assembled,
            jev_topic=assessment.topic,
            context_citations=citations,
        )
    except ValueError as exc:
        return FlowResult(
            assembled.source_id,
            "reject",
            f"ekstrakcja: {exc}",
            category=category,
            assembled=assembled,
            jev_topic=assessment.topic,
        )
    return FlowResult(
        assembled.source_id,
        "extract",
        "local_clm_and_jev",
        category=category,
        summary=summary,
        assembled=assembled,
        jev_topic=assessment.topic,
    )


def _parse_published(value: str | None) -> datetime | None:
    """Keep the source date. An unparseable date stays None, never today's date."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        pass
    for pattern in (_X_TWITTER_DATE, "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, pattern)
        except ValueError:
            continue
    return None


def _x_id(value: str | None) -> str | None:
    if not value:
        return None
    return value if value.startswith("x:") else f"x:{value}"


def _record(
    *,
    source_id: str,
    author: str,
    text: str,
    url: str | None,
    published_at: str | None,
    reply_to_id: str | None,
    conversation_id: str | None,
    quoted_source_id: str | None,
    raw_ref: str,
) -> SourceRecord:
    return SourceRecord(
        source_id=source_id,
        author=author or "nieznany",
        url=url,
        text=text,
        published_at=_parse_published(published_at),
        fetched_at=datetime.now(timezone.utc),
        reply_to_id=_x_id(reply_to_id),
        conversation_id=_x_id(conversation_id),
        quoted_source_id=_x_id(quoted_source_id),
        raw_ref=raw_ref,
        content_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        context_status=ContextStatus.unavailable,
    )


def _bundle(assembled: AssembledPost) -> ContextBundle:
    """Author text in focus, parents and quotes in related, explicit gaps in missing_ids."""
    focus = _record(
        source_id=assembled.source_id,
        author=assembled.author,
        text=assembled.focus_evidence,
        url=assembled.url,
        published_at=assembled.published_at,
        reply_to_id=assembled.reply_to_id,
        conversation_id=assembled.conversation_id,
        quoted_source_id=assembled.quoted_source_id,
        raw_ref="pipeline:assembled",
    )
    records: dict[str, SourceRecord] = {}
    provenance: dict[str, str] = {}
    for piece in assembled.related:
        record = _piece_record(piece)
        records.setdefault(record.source_id, record)
        provenance.setdefault(record.source_id, piece.provenance)

    def lookup(source_id: str) -> SourceRecord | None:
        return records.get(source_id)

    bundle = build_context(
        focus,
        lookup,
        provenance_for=provenance.get,
        extra_missing_ids=[_x_id(value) for value in assembled.missing_ids],
    )
    return bundle


def _piece_record(piece: RelatedPiece) -> SourceRecord:
    return _record(
        source_id=piece.source_id,
        author=piece.author,
        text=piece.text or "(brak tekstu wpisu)",
        url=piece.url,
        published_at=piece.published_at,
        reply_to_id=piece.reply_to_id,
        conversation_id=None,
        quoted_source_id=piece.quoted_source_id,
        raw_ref=f"pipeline:related:{piece.provenance}",
    )


def _related_for_quote_check(bundle: ContextBundle) -> list[tuple[ContextCitation, str]]:
    return [
        (
            ContextCitation(
                role=item.role,
                author=item.source.author,
                source_id=item.source.source_id,
                provenance=item.provenance,
            ),
            item.source.text,
        )
        for item in bundle.related
    ]
