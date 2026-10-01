"""Render an extracted post without inventing vault links."""

from __future__ import annotations

import re
from pathlib import Path

from .run_flow import FlowResult

_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def safe_note_name(title: str, source_id: str, published_at: str | None) -> str:
    clean = re.sub(r'[\/:*?"<>|#^\[\]]', "", title)
    clean = re.sub(r"\s+", " ", clean).strip() or "wpis"
    if clean.upper().split(" ")[0] in _RESERVED:
        clean = f"wpis {clean}"
    prefix = ""
    if published_at and len(published_at) >= 10 and published_at[:4].isdigit() and published_at[4] == "-":
        prefix = published_at[:10] + " "
    elif published_at:
        try:
            from datetime import datetime
            prefix = datetime.strptime(published_at, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d ")
        except ValueError:
            prefix = ""
    numeric = source_id[2:] if source_id.startswith("x:") else source_id
    return f"{prefix}{clean[:80].rstrip()} {numeric}.md"


def render_note(result: FlowResult, handle: str) -> str:
    if result.summary is None or result.assembled is None or result.category is None:
        raise ValueError("notatka wymaga kategorii i podsumowania")
    summary = result.summary
    assembled = result.assembled
    meta = [
        f"- **Autor:** [[{handle} — Indeks|@{handle}]] | **Źródło:** [Post na X]({assembled.url})",
        f"- **Kategoria:** {result.category}",
    ]
    if summary.get("topic"):
        meta.append(f"- **Temat:** {summary['topic']}")
    meta.extend([
        f"- **Kontekst:** {'niepełny, brak ' + ', '.join(assembled.missing_ids) if assembled.missing_ids else 'wątek dostępny albo wpis samodzielny'}",
    ])
    lines = [
        "---",
        "typ: wpis-źródłowy",
        f"autor: \"@{handle}\"",
        f"data: \"{assembled.published_at or ''}\"",
        f"źródło: \"{assembled.url}\"",
        f"kategoria: \"{result.category}\"",
        f"tweet_id: \"{result.source_id}\"",
        "tagi:",
        f"  - {handle.lower()}",
        "  - ai-engineering",
        "  - wpis-atomowy",
        "---",
        "",
        f"# {summary['title']}",
        "",
        *meta,
        "",
        "## Podsumowanie",
        "",
        str(summary["summary"]),
        "",
        "## Oryginalny cytat",
        "",
        f"> {summary['quote']}",
        "",
    ]
    return "\n".join(lines)


def write_staging(results: list[FlowResult], handle: str, directory: Path) -> list[str]:
    directory.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for result in results:
        if result.status != "extract":
            continue
        name = safe_note_name(str(result.summary["title"]), result.source_id, result.assembled.published_at)
        path = directory / name
        path.write_text(render_note(result, handle), encoding="utf-8")
        written.append(str(path))
    return written
