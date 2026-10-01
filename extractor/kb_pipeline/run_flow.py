"""Four-stage post pipeline. Code owns the order; models only answer their stage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .assemble import AssembledPost, assemble_post
from .decisions import parse_category, parse_summary
from .filtering import assess_filter
from .local_gate import decide_clm, screen_focus
from .schemas import ContextBundle, FilterDecision


@dataclass
class FlowResult:
    source_id: str
    status: str
    reason: str
    category: str | None = None
    summary: dict[str, str | None] | None = None
    assembled: AssembledPost | None = None
    jev_topic: str | None = None


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
        return FlowResult(assembled.source_id, "defer", f"lokalny filtr: {exc}", assembled=assembled)
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
        return FlowResult(assembled.source_id, "defer", f"kategoria: {exc}", assembled=assembled, jev_topic=assessment.topic)

    try:
        summary = parse_summary(summarize(assembled.document, category), assembled.document)
    except Exception as exc:
        return FlowResult(
            assembled.source_id,
            "defer",
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


def _bundle(assembled: AssembledPost) -> ContextBundle:
    from datetime import datetime, timezone
    import hashlib

    from .schemas import ContextStatus, SourceRecord

    status = ContextStatus.partial if assembled.missing_ids else ContextStatus.complete
    published = None
    content_hash = hashlib.sha256(assembled.document.encode("utf-8")).hexdigest()
    record = SourceRecord(
        source_id=assembled.source_id,
        author=assembled.author,
        url=assembled.url,
        text=assembled.document,
        published_at=published,
        fetched_at=datetime.now(timezone.utc),
        reply_to_id=None,
        conversation_id=None,
        quoted_source_id=None,
        raw_ref="pipeline:assembled",
        content_hash=content_hash,
        context_status=status,
    )
    return ContextBundle(
        focus=record,
        missing_ids=[f"x:{value}" if value.isdigit() else value for value in assembled.missing_ids],
        context_status=status,
    )
