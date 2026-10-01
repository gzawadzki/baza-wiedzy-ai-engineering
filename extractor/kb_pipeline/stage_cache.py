"""Workspace-local persistence for pipeline artifacts and runs."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

from .schemas import RunManifest


class StageCache:
    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.workspace / "stage_cache.sqlite3")
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    key TEXT PRIMARY KEY,
                    value_json TEXT NOT NULL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS manifests (
                    run_id TEXT PRIMARY KEY,
                    manifest_json TEXT NOT NULL
                )
            """)

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> StageCache:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @staticmethod
    def key(stage: str, input_hash: str, context_hash: str, model: str,
            prompt_version: str, schema_version: int = 1) -> str:
        parts = [stage, input_hash, context_hash, model, prompt_version, schema_version]
        encoded = json.dumps(parts, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def get(self, key: str) -> dict | None:
        row = self.connection.execute("SELECT value_json FROM artifacts WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, key: str, value: dict) -> None:
        def check_fields(item: object) -> None:
            if isinstance(item, dict):
                for name, nested in item.items():
                    if isinstance(name, str):
                        field = name.lower().replace("-", "_")
                        if (field in {"headers", "authorization", "cookie", "api_key", "password", "token"}
                                or field.endswith("_token") or "credential" in field or "secret" in field):
                            raise ValueError("artifact contains sensitive fields")
                    check_fields(nested)
            elif isinstance(item, list):
                for nested in item:
                    check_fields(nested)

        check_fields(value)
        payload = json.dumps(value, ensure_ascii=False, allow_nan=False)
        with self.connection:
            self.connection.execute("""
                INSERT INTO artifacts (key, value_json) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json
            """, (key, payload))

    def persist_manifest(self, manifest: RunManifest) -> None:
        with self.connection:
            self.connection.execute("""
                INSERT INTO manifests (run_id, manifest_json) VALUES (?, ?)
                ON CONFLICT(run_id) DO UPDATE SET manifest_json=excluded.manifest_json
            """, (manifest.run_id, manifest.model_dump_json()))

    def load_manifest(self, run_id: str) -> RunManifest | None:
        row = self.connection.execute("SELECT manifest_json FROM manifests WHERE run_id=?", (run_id,)).fetchone()
        return RunManifest.model_validate_json(row[0]) if row else None
