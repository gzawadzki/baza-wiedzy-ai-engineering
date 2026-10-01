"""CLI-side driver for the offline vertical flow (``run --offline``).

Loads an explicit cache input into the workspace ``SourceStore`` and runs the
flow for every selected source. The vault is read-only input here: it is indexed
into the workspace and planned against, never written.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .offline_flow import FlowProviders, run_offline_flow
from .storage import SourceStore
from .thresholds import resolve_thresholds


def _input_files(input_path: Path) -> list[Path]:
    if input_path.is_dir():
        return sorted(input_path.glob("*_raw_tweets.json"))
    return [input_path]


def _source_ids(store: SourceStore) -> list[str]:
    rows = store.connection.execute(
        "SELECT DISTINCT source_id FROM source_revisions ORDER BY source_id"
    ).fetchall()
    return [row[0] for row in rows]


def run_offline(
    *,
    vault: Path,
    workspace: Path,
    cache_input: Path | None,
    cache_dir: Path | None,
    handles: list[str] | None,
    source_ids: list[str] | None,
    limit: int,
    providers: FlowProviders,
    thresholds: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Import the cache, then run one flow per source. No network, no vault writes."""
    vault_path = Path(vault).resolve(strict=True)
    workspace_path = Path(workspace).resolve()
    if workspace_path == vault_path or vault_path in workspace_path.parents:
        raise ValueError("Workspace must live outside the vault")

    limits = resolve_thresholds(thresholds)
    inputs = []
    if cache_input is not None:
        inputs.append(Path(cache_input))
    if cache_dir is not None:
        inputs.extend(path for path in _input_files(Path(cache_dir)) if path not in inputs)
    inputs = [path for path in inputs if path.exists()]
    if not inputs:
        raise ValueError(
            "No cache input found; pass --offline-input PATH or --cache-dir with "
            "<handle>_raw_tweets.json files"
        )
    if handles:
        wanted = {handle.lstrip("@") for handle in handles}
        filtered = [path for path in inputs if path.stem.removesuffix("_raw_tweets") in wanted]
        inputs = filtered or inputs

    imported: dict[str, dict[str, int]] = {}
    with SourceStore(workspace_path) as store:
        for path in inputs:
            imported[path.name] = store.import_cache(path)
        available = _source_ids(store)
        selected = [sid for sid in available if not source_ids or sid in set(source_ids)]
        if source_ids:
            unknown = sorted(set(source_ids) - set(selected))
            if unknown:
                raise ValueError(f"Unknown source IDs: {', '.join(unknown)}")
        if limit > 0:
            selected = selected[:limit]
        if not selected:
            raise ValueError("No source records matched the selection")

        identity = hashlib.sha256(
            json.dumps(
                {"sources": selected, "vault": str(vault_path), "code": "offline-flow-v1"},
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()[:16]
        run_id = f"offline-flow-{identity}"

        def lookup(source_id: str, _store=store):
            return _store.get_deterministic(source_id)

        results = [
            run_offline_flow(
                source=record,
                lookup=lookup,
                vault=vault_path,
                workspace=workspace_path,
                providers=providers,
                run_id=run_id,
                thresholds=limits,
            )
            for record in (lookup(source_id) for source_id in selected)
        ]

    counters = {"extract": 0, "reject": 0, "defer": 0, "error": 0}
    for result in results:
        for key, value in result["counters"].items():
            counters[key] = counters.get(key, 0) + value
    provider_calls = sum(result["provider_calls"] for result in results)
    return {
        "status": "ok",
        "mode": "offline",
        "run_id": run_id,
        "run_dir": results[0]["run_dir"],
        "vault": str(vault_path),
        "vault_written": False,
        "cache_import": imported,
        "sources": selected,
        "counters": counters,
        "provider_mode": providers.mode,
        "provider_calls": provider_calls,
        "replay": provider_calls == 0,
        "patches": [
            patch for result in results for patch in result.get("patches", [])
        ],
        "runs": [
            {
                "source_id": result["source_id"],
                "status": result["status"],
                "reason": result["reason"],
                "stages": result["stages"],
                "provider_calls": result["provider_calls"],
                "patch_count": result.get("patch_count", 0),
                "publication_plan_ref": result.get("publication_plan_ref"),
            }
            for result in results
        ],
    }
