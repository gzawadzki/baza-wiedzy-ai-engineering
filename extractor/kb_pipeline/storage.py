"""SQLite operational state for offline source import; vault files are never written here."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .ingestion import read_cache
from .schemas import SourceRecord


class SourceStore:
    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.workspace / "sources.sqlite3")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS source_revisions (
                source_id TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                record_json TEXT NOT NULL,
                raw_json TEXT NOT NULL,
                PRIMARY KEY (source_id, content_hash)
            );
            CREATE TABLE IF NOT EXISTS import_errors (
                cache_name TEXT NOT NULL,
                item_index INTEGER NOT NULL,
                reason TEXT NOT NULL,
                PRIMARY KEY (cache_name, item_index)
            );
        """)
        self.connection.commit()

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def get(self, source_id: str, content_hash: str) -> SourceRecord | None:
        row = self.connection.execute("SELECT record_json FROM source_revisions WHERE source_id=? AND content_hash=?",
                                      (source_id, content_hash)).fetchone()
        return SourceRecord.model_validate_json(row[0]) if row else None

    def import_cache(self, path: Path) -> dict[str, int]:
        if not path.name.endswith("_raw_tweets.json"):
            raise ValueError("expected <handle>_raw_tweets.json")
        counts = {"new_revisions": 0, "unchanged": 0, "errors": 0}
        # Invalid JSON raises before the first write, preserving the previous import.
        entries = list(read_cache(path))
        with self.connection:
            for index, record, raw, error in entries:
                if error:
                    self.connection.execute("INSERT OR REPLACE INTO import_errors VALUES (?, ?, ?)", (path.name, index, error))
                    counts["errors"] += 1
                    continue
                self.connection.execute("DELETE FROM import_errors WHERE cache_name=? AND item_index=?", (path.name, index))
                cursor = self.connection.execute(
                    "INSERT OR IGNORE INTO source_revisions VALUES (?, ?, ?, ?)",
                    (record.source_id, record.content_hash, record.model_dump_json(),
                     json.dumps(raw, ensure_ascii=False, sort_keys=True)),
                )
                counts["new_revisions" if cursor.rowcount else "unchanged"] += 1
        return counts
