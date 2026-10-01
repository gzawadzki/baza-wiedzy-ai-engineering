"""Workspace-scoped wrappers for the read-only retrieval index (PKG-2C).

The index is built from the vault but always lives in the workspace, outside
the vault. ``reindex`` only writes to the workspace; ``search`` never writes
anywhere. Both commands return deterministic, JSON-serializable payloads so
the CLI stays stable for humans and for agents.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

from .retrieval import reindex as _reindex
from .retrieval import search as _search

INDEX_DIR_NAME = "retrieval"
INDEX_FILE_NAME = "index.sqlite3"
INDEX_INFO_FILE_NAME = "index-info.json"
INDEX_VERSION = 1

DEFAULT_LIMIT = 10
MAX_LIMIT = 100


class RetrievalError(Exception):
    """CLI-facing retrieval failure with a stable machine-readable code."""

    def __init__(self, code: str, message: str, *, hint: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.hint = hint

    def payload(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "status": "error",
            "code": self.code,
            "error": self.message,
        }
        if self.hint:
            data["hint"] = self.hint
        return data


def index_path(workspace: Path) -> Path:
    """Index location inside the workspace; never inside the vault."""

    return Path(workspace).expanduser() / INDEX_DIR_NAME / INDEX_FILE_NAME


def index_info_path(workspace: Path) -> Path:
    return Path(workspace).expanduser() / INDEX_DIR_NAME / INDEX_INFO_FILE_NAME


def _resolve_workspace(workspace: Path) -> Path:
    workspace_path = Path(workspace).expanduser()
    if not workspace_path.exists():
        raise RetrievalError(
            "missing_workspace",
            f"Workspace does not exist: {workspace_path}",
            hint="Create it first or pass --workspace with an existing directory.",
        )
    if not workspace_path.is_dir():
        raise RetrievalError(
            "invalid_workspace",
            f"Workspace is not a directory: {workspace_path}",
        )
    return workspace_path.resolve()


def _resolve_vault(vault: Path) -> Path:
    vault_path = Path(vault).expanduser()
    if not vault_path.exists():
        raise RetrievalError(
            "missing_vault",
            f"Vault does not exist: {vault_path}",
            hint="--vault must point at the knowledge base root directory.",
        )
    if not vault_path.is_dir():
        raise RetrievalError(
            "invalid_vault",
            f"Vault is not a directory: {vault_path}",
        )
    return vault_path.resolve()


def _fingerprint(db_path: Path) -> str:
    """Content hash of the indexed rows; stable across repeated reindex runs."""

    digest = hashlib.sha256()
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = conn.execute(
            """
            SELECT path, note_id, heading, anchor, content, aliases, status, is_source
            FROM sections_fts
            ORDER BY path, anchor, heading, content
            """
        )
        for row in rows:
            for value in row:
                digest.update(b"\x1f")
                digest.update(str(value).encode("utf-8"))
            digest.update(b"\x1e")
    finally:
        conn.close()
    return digest.hexdigest()


def reindex_vault(vault: Path, workspace: Path) -> dict[str, Any]:
    """Rebuild the section index in the workspace from a read-only vault scan."""

    vault_path = _resolve_vault(vault)
    workspace_path = _resolve_workspace(workspace)
    db_path = index_path(workspace_path).resolve()
    if db_path == vault_path or vault_path in db_path.parents:
        raise RetrievalError(
            "index_inside_vault",
            "Index must live outside the vault",
            hint=f"Choose a workspace outside {vault_path}.",
        )

    try:
        sections = _reindex(vault_path, db_path)
    except ValueError as exc:
        raise RetrievalError("index_rejected", str(exc)) from exc
    except sqlite3.Error as exc:
        raise RetrievalError("index_write_failed", f"Index write failed: {exc}") from exc
    except OSError as exc:
        raise RetrievalError("index_write_failed", f"Index write failed: {exc}") from exc

    fingerprint = _fingerprint(db_path)
    info = {
        "index_version": INDEX_VERSION,
        "vault": vault_path.as_posix(),
        "index": db_path.as_posix(),
        "sections": sections,
        "fingerprint": fingerprint,
    }
    info_file = index_info_path(workspace_path)
    info_file.write_text(
        json.dumps(info, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "status": "ok",
        "command": "reindex",
        "vault": vault_path.as_posix(),
        "workspace": workspace_path.as_posix(),
        "index": db_path.as_posix(),
        "sections": sections,
        "fingerprint": fingerprint,
        "vault_writes": 0,
    }


def _load_index_info(workspace_path: Path) -> dict[str, Any]:
    info_file = index_info_path(workspace_path)
    if not info_file.is_file():
        return {}
    try:
        data = json.loads(info_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def search_index(
    workspace: Path,
    query: str,
    *,
    vault: Path | None = None,
    include_sources: bool = False,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    """Query the workspace index read-only; the vault is never written."""

    workspace_path = _resolve_workspace(workspace)
    if vault is not None:
        vault_path: Path | None = _resolve_vault(vault)
    else:
        vault_path = None

    if not query or not query.strip():
        raise RetrievalError(
            "empty_query",
            "Search query is empty",
            hint='Pass a phrase, for example: search "kompaktowanie kontekstu" --workspace ...',
        )
    if limit <= 0 or limit > MAX_LIMIT:
        raise RetrievalError(
            "invalid_limit",
            f"Limit must be between 1 and {MAX_LIMIT}, got {limit}",
        )

    db_path = index_path(workspace_path)
    if not db_path.is_file():
        raise RetrievalError(
            "missing_index",
            f"No retrieval index in workspace: {db_path}",
            hint="Run: reindex --vault ... --workspace ...",
        )

    try:
        results = _search(db_path, query, include_sources=include_sources, limit=limit)
    except sqlite3.Error as exc:
        raise RetrievalError("search_failed", f"Search failed: {exc}") from exc
    except (OSError, ValueError) as exc:
        raise RetrievalError("search_failed", f"Search failed: {exc}") from exc

    info = _load_index_info(workspace_path)
    payload: dict[str, Any] = {
        "status": "ok",
        "command": "search",
        "query": query,
        "workspace": workspace_path.as_posix(),
        "index": db_path.resolve().as_posix(),
        "include_sources": include_sources,
        "limit": limit,
        "count": len(results),
        "results": results,
    }
    if "fingerprint" in info:
        payload["index_fingerprint"] = info["fingerprint"]
    if vault_path is not None:
        payload["vault"] = vault_path.as_posix()
    return payload
