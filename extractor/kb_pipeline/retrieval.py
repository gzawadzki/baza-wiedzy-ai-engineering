"""Read-only SQLite FTS5 section index and retrieval for Obsidian knowledge base."""

from __future__ import annotations

import hashlib
import re
import sqlite3
from pathlib import Path
from typing import Any

import yaml

CANONICAL_DIRS = ("Pojęcia", "Procesy", "Narzędzia", "Zasady")
SOURCE_DIRS = ("Źródła",)


def _make_anchor(heading: str) -> str:
    cleaned = heading.strip().lower()
    cleaned = re.sub(r"[^\w\s-]", "", cleaned)
    cleaned = re.sub(r"[\s_]+", "-", cleaned).strip("-")
    return cleaned


def _frontmatter(text: str) -> tuple[dict[str, Any] | None, str]:
    if not (text.startswith("---\n") or text.startswith("---\r\n")):
        return None, text
    end = re.search(r"\n---(?:\r)?\n|\n\.\.\.(?:\r)?\n", text[4:])
    if end is None:
        return None, text
    raw_front = text[4 : 4 + end.start()]
    body = text[4 + end.end() :]
    try:
        data = yaml.safe_load(raw_front)
        if isinstance(data, dict):
            return data, body
    except yaml.YAMLError:
        pass
    return None, body


def _split_sections(body: str, stem: str) -> list[tuple[str, str, str]]:
    sections: list[tuple[str, str, str]] = []
    current_heading = stem
    current_anchor = ""
    current_lines: list[str] = []
    in_code_block = False

    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            current_lines.append(line)
            continue

        if not in_code_block and re.match(r"^#{1,6}\s+", line):
            text_block = "\n".join(current_lines).strip()
            if text_block or current_anchor:
                sections.append((current_heading, current_anchor, text_block))
            current_heading = re.sub(r"^#{1,6}\s+", "", line).strip()
            current_anchor = _make_anchor(current_heading)
            current_lines = []
        else:
            current_lines.append(line)

    text_block = "\n".join(current_lines).strip()
    if text_block or current_anchor or not sections:
        sections.append((current_heading, current_anchor, text_block))

    return sections


def sanitize_query(query: str) -> str:
    tokens = re.findall(r'"([^"]*)"|(\S+)', query)
    parts = []
    for phrase, word in tokens:
        if phrase:
            cleaned = re.sub(r"[^\w\s-]", " ", phrase).strip()
            if cleaned:
                parts.append(f'"{cleaned}"')
        elif word:
            has_star = word.endswith("*") and len(word) > 1
            cleaned = re.sub(r"[^\w]", "", word)
            if cleaned:
                if has_star:
                    parts.append(f'"{cleaned}"*')
                else:
                    parts.append(f'"{cleaned}"')
    return " ".join(parts)


def reindex(vault: Path, db_path: Path) -> int:
    vault = Path(vault).resolve(strict=True)
    db_path = Path(db_path).resolve()

    if db_path == vault or vault in db_path.parents:
        raise ValueError("Database must live outside the vault")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        with conn:
            conn.execute("DROP TABLE IF EXISTS sections_fts")
            conn.execute("""
                CREATE VIRTUAL TABLE sections_fts USING fts5(
                    path UNINDEXED,
                    note_id UNINDEXED,
                    heading,
                    anchor UNINDEXED,
                    content,
                    aliases,
                    status UNINDEXED,
                    is_source UNINDEXED,
                    tokenize = 'unicode61'
                )
            """)

            indexed_count = 0
            all_dirs = [(d, False) for d in CANONICAL_DIRS] + [(d, True) for d in SOURCE_DIRS]

            for dir_name, is_source in all_dirs:
                dir_path = vault / dir_name
                if not dir_path.is_dir() or dir_path.is_symlink():
                    continue

                for file_path in sorted(dir_path.rglob("*.md")):
                    if file_path.is_symlink() or not file_path.is_file():
                        continue
                    if any(parent.is_symlink() for parent in file_path.parents if parent != vault):
                        continue

                    rel_path = file_path.relative_to(vault).as_posix()
                    raw_text = file_path.read_text(encoding="utf-8-sig", errors="replace")

                    front, body = _frontmatter(raw_text)
                    front = front or {}

                    raw_id = front.get("note_id") or front.get("id")
                    if raw_id is not None and str(raw_id).strip():
                        note_id = str(raw_id).strip()
                    else:
                        note_id = hashlib.sha256(rel_path.encode("utf-8")).hexdigest()[:16]

                    status = str(front["status"]) if front.get("status") is not None else None

                    aliases_raw = front.get("aliases", [])
                    if isinstance(aliases_raw, list):
                        aliases_list = [str(a).strip() for a in aliases_raw if a is not None and str(a).strip()]
                    elif isinstance(aliases_raw, str) and aliases_raw.strip():
                        aliases_list = [aliases_raw.strip()]
                    else:
                        aliases_list = []
                    aliases_text = " ".join(aliases_list)

                    sections = _split_sections(body, file_path.stem)
                    for heading, anchor, content in sections:
                        conn.execute(
                            """
                            INSERT INTO sections_fts (
                                path, note_id, heading, anchor, content, aliases, status, is_source
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                rel_path,
                                note_id,
                                heading,
                                anchor,
                                content,
                                aliases_text,
                                status,
                                1 if is_source else 0,
                            ),
                        )
                        indexed_count += 1

        return indexed_count
    finally:
        conn.close()


def search(
    db_path: Path,
    query: str,
    *,
    include_sources: bool = False,
    limit: int = 10,
) -> list[dict[str, Any]]:
    if limit <= 0 or not query or not query.strip():
        return []

    db_path = Path(db_path).resolve()
    if not db_path.is_file():
        return []

    sanitized = sanitize_query(query)
    if not sanitized:
        return []

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        where_source = "" if include_sources else "AND is_source = 0"
        sql = f"""
            SELECT
                path,
                note_id,
                heading,
                anchor,
                snippet(sections_fts, -1, '', '', '...', 32) AS snippet,
                content,
                rank AS raw_score,
                status
            FROM sections_fts
            WHERE sections_fts MATCH ? {where_source}
            ORDER BY rank
            LIMIT ?
        """
        cursor = conn.execute(sql, (sanitized, limit))
        results: list[dict[str, Any]] = []
        for row in cursor:
            snip = row["snippet"] or ""
            if not snip.strip():
                content = row["content"] or ""
                snip = content[:200].strip()
            score = round(abs(float(row["raw_score"])), 6)
            results.append(
                {
                    "path": row["path"],
                    "note_id": row["note_id"],
                    "heading": row["heading"],
                    "anchor": row["anchor"],
                    "snippet": snip,
                    "score": score,
                    "status": row["status"],
                }
            )
        return results
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()
