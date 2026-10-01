"""CLI-side driver for the offline vertical flow (``run --offline``, ``resume``).

Loads an explicit cache input into the workspace ``SourceStore`` and runs the
flow for every selected source. The vault is read-only input here: it is indexed
into the workspace and planned against, never written.

The same driver continues a run: ``resume_offline`` reads the run's own
descriptor, serves completed provider stages from their durable artifacts, and
reports what it resumed, what it recomputed and what it found broken. When the
descriptor is gone it refuses and says so, instead of guessing a run.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .offline_flow import CODE_VERSION, PROMPT_VERSION, FlowProviders, run_offline_flow
from .run_state import RunState
from .schemas import SCHEMA_VERSION
from .storage import SourceStore
from .thresholds import resolve_thresholds
from .usage import FlowBudget, summarise


def _input_files(input_path: Path) -> list[Path]:
    if input_path.is_dir():
        return sorted(input_path.glob("*_raw_tweets.json"))
    return [input_path]


def _source_ids(store: SourceStore) -> list[str]:
    rows = store.connection.execute(
        "SELECT DISTINCT source_id FROM source_revisions ORDER BY source_id"
    ).fetchall()
    return [row[0] for row in rows]


def _derive_run_id(selected: list[str], vault: Path, providers: FlowProviders) -> str:
    """The batch identity: one id for the whole invocation."""
    identity = hashlib.sha256(
        json.dumps(
            {
                "sources": selected,
                "vault": str(vault),
                "code": CODE_VERSION,
                "provider_mode": providers.mode,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:16]
    return f"offline-flow-{identity}"


def _derive_source_run_id(source_id: str, vault: Path) -> str:
    """One run id per source, so a batch never shares artifacts or a digest."""
    identity = hashlib.sha256(
        json.dumps(
            {"sources": [source_id], "vault": str(vault), "code": CODE_VERSION},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:16]
    return f"offline-flow-{identity}"


def _write_run_usage_manifest(run_dir: Path, results: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate the per-source usage ledgers of one invocation into the run."""
    payloads: list[Mapping[str, Any]] = []
    for result in results:
        path = Path(str(result["source_dir"])) / str(result.get("usage_ref", "usage.json"))
        if not path.is_file():
            continue
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
    payload = summarise(payloads)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "usage_manifest.json").write_bytes(
        (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode(
            "utf-8"
        )
    )
    # One appended line per source and invocation: the history of this run, kept
    # with the batch rather than overwritten by the next invocation.
    for result in results:
        source_usage = Path(result["run_dir"]) / "usage.json"
        if not source_usage.is_file():
            continue
        try:
            entry = json.loads(source_usage.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        with (run_dir / "usage_log.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "recorded_at": datetime.now(timezone.utc).isoformat(),
                        "run_id": result["run_id"],
                        "source_id": result["source_id"],
                        "status": result["status"],
                        **entry,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                    allow_nan=False,
                )
                + "\n"
            )
    return payload


def _aggregate(results: list[dict[str, Any]], providers: FlowProviders, run_id: str) -> dict[str, Any]:
    counters: dict[str, int] = {}
    for result in results:
        for key, value in result["counters"].items():
            counters[key] = counters.get(key, 0) + value
    provider_calls = sum(result["provider_calls"] for result in results)
    return {
        "counters": counters,
        "provider_calls": provider_calls,
        "provider_replays": sum(result["provider_replays"] for result in results),
        "resumed_stages": sorted(
            {stage for result in results for stage in result["resume"]["resumed_stages"]}
        ),
        "recomputed_stages": sorted(
            {stage for result in results for stage in result["resume"]["recomputed_stages"]}
        ),
        "artifact_problems": [
            problem
            for result in results
            for problem in result["resume"]["artifact_problems"]
        ],
    }


def _run_report(
    *,
    results: list[dict[str, Any]],
    providers: FlowProviders,
    run_id: str,
    run_dir: Path,
    vault: Path,
    batch_dir: Path | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    totals = _aggregate(results, providers, run_id)
    # The batch artifacts describe the invocation; each source keeps its own
    # run directory with its own summary, manifest and usage.
    batch = Path(batch_dir) if batch_dir is not None else Path(run_dir)
    usage = _write_run_usage_manifest(batch, results)
    report = {
        "status": "ok",
        "mode": "offline",
        "run_id": run_id,
        "run_dir": str(run_dir),
        "batch_run_id": batch.name,
        "batch_run_dir": str(batch),
        "vault": str(vault),
        "vault_written": False,
        "counters": totals["counters"],
        "budget_stopped": any(result["status"] == "budget_exhausted" for result in results),
        "provider_mode": providers.mode,
        "provider_calls": totals["provider_calls"],
        "provider_replays": totals["provider_replays"],
        "replay": totals["provider_calls"] == 0,
        "resumed_stages": totals["resumed_stages"],
        "recomputed_stages": totals["recomputed_stages"],
        "artifact_problems": totals["artifact_problems"],
        "usage": usage["totals"],
        "usage_manifest_ref": "usage_manifest.json",
        "patches": [patch for result in results for patch in result.get("patches", [])],
        "runs": [
            {
                "source_id": result["source_id"],
                "run_id": result["run_id"],
                "run_dir": result["run_dir"],
                "status": result["status"],
                "reason": result["reason"],
                "stages": result["stages"],
                "provider_calls": result["provider_calls"],
                "resumed_stages": result["resume"]["resumed_stages"],
                "recomputed_stages": result["resume"]["recomputed_stages"],
                "claim_ids": result.get("claim_ids", []),
                "patch_count": result.get("patch_count", 0),
                "summary_ref": str(Path(result["run_dir"]) / "summary.json"),
                "manifest_ref": result["manifest_ref"],
                "usage_ref": str(Path(result["run_dir"]) / "usage.json"),
                "artifact_problems": result["resume"]["artifact_problems"],
                "publication_plan_ref": result.get("publication_plan_ref"),
            }
            for result in results
        ],
        **(dict(extra) if extra else {}),
    }
    # The batch summary sits with the batch; the per-source ones stay with their
    # source, so a two-source run keeps both.
    (batch / "summary.json").write_bytes(
        (
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
            + "\n"
        ).encode("utf-8")
    )
    return report


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
    run_id: str | None = None,
    max_attempts: int | None = None,
    max_tokens: int | None = None,
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
        if not filtered:
            # Strict: a handle that matches nothing is an error, never a silent
            # fallback to the unfiltered input.
            raise ValueError(
                f"No cache input matched handles: {', '.join(sorted(wanted))}"
            )
        inputs = filtered

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

        batch_run_id = run_id or _derive_run_id(selected, vault_path, providers)
        batch_state = RunState(workspace_path, batch_run_id)
        source_runs = {
            source_id: run_id if run_id else _derive_source_run_id(source_id, vault_path)
            for source_id in selected
        }
        descriptor = {
            "vault": str(vault_path),
            "workspace": str(workspace_path),
            "sources": selected,
            "run_ids": source_runs,
            "batch_run_id": batch_run_id,
            "provider_mode": providers.mode,
            "provider_model_versions": dict(providers.model_versions),
            "prompt_version": PROMPT_VERSION,
            "code_version": CODE_VERSION,
            "schema_version": SCHEMA_VERSION,
            "thresholds": dict(limits),
            "cache_inputs": [str(path) for path in inputs],
            "max_attempts": max_attempts,
            "max_tokens": max_tokens,
        }
        batch_state.write_descriptor(descriptor)
        # Every source's own run directory also carries a descriptor naming that
        # one source, so `resume --run-id <source run>` finds its own context.
        for source_id, source_run in source_runs.items():
            RunState(workspace_path, source_run).write_descriptor(
                {**descriptor, "sources": [source_id], "run_ids": {source_id: source_run}}
            )
        budget = FlowBudget(max_attempts=max_attempts, max_tokens=max_tokens)

        def lookup(source_id: str, _store=store):
            return _store.get_deterministic(source_id)

        results = [
            run_offline_flow(
                source=record,
                lookup=lookup,
                vault=vault_path,
                workspace=workspace_path,
                providers=providers,
                run_id=source_runs[record.source_id],
                thresholds=limits,
                budget=budget,
            )
            for record in (lookup(source_id) for source_id in selected)
        ]

    return _run_report(
        results=results,
        providers=providers,
        run_id=batch_run_id,
        run_dir=Path(results[0]["run_dir"]),
        batch_dir=batch_state.run_dir,
        vault=vault_path,
        extra={
            "cache_import": imported,
            "sources": selected,
            "budget": budget.to_dict(),
        },
    )


def resume_offline(
    *,
    workspace: Path,
    run_id: str,
    vault: Path | None = None,
    providers: FlowProviders | None = None,
    max_attempts: int | None = None,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    """Continue an interrupted run from its own checkpoints.

    The run must be able to describe itself: without ``run_descriptor.json``
    there is nothing to continue from, and this refuses instead of starting a
    fresh run under the old id.
    """
    workspace_path = Path(workspace).resolve()
    state = RunState(workspace_path, run_id)
    descriptor = state.load_descriptor()
    if descriptor is None:
        raise ValueError(
            f"Run '{run_id}' has no descriptor at {state.descriptor_path}; "
            "resume needs to know what the run was. Start a new run instead."
        )
    run_providers = providers or fake_offline_providers(descriptor)
    vault_path = Path(vault or descriptor["vault"]).resolve(strict=True)
    sources = list(descriptor.get("sources") or [])
    if not sources:
        raise ValueError(f"Run '{run_id}' descriptor lists no sources")
    limits = resolve_thresholds(descriptor.get("thresholds"))
    budget = FlowBudget(
        max_attempts=max_attempts
        if max_attempts is not None
        else descriptor.get("max_attempts"),
        max_tokens=max_tokens if max_tokens is not None else descriptor.get("max_tokens"),
    )

    if not (workspace_path / "sources.sqlite3").is_file():
        raise ValueError(
            "This workspace has no source store, so the run cannot be continued; "
            "re-import the cache with run --offline first."
        )

    with SourceStore(workspace_path) as store:

        def lookup(source_id: str, _store=store):
            return _store.get_deterministic(source_id)

        # A run belongs to one source, so each source resumes in its own run
        # directory; the descriptor's run_ids say which one is which.
        run_ids = dict(descriptor.get("run_ids") or {})
        results = [
            run_offline_flow(
                source=lookup(source_id),
                lookup=lookup,
                vault=vault_path,
                workspace=workspace_path,
                providers=run_providers,
                run_id=run_ids.get(source_id, run_id),
                thresholds=limits,
                budget=budget,
                resume=True,
            )
            for source_id in sources
        ]
        checkpoints = {
            source_run: RunState(workspace_path, source_run).report()
            for source_run in sorted(set(run_ids.values()) | {run_id})
        }

    return _run_report(
        results=results,
        providers=run_providers,
        run_id=run_id,
        run_dir=state.run_dir,
        vault=vault_path,
        extra={
            "resumed": True,
            "provider_mode_note": (
                "resumed with fake-offline providers; a live run must inject its own "
                "providers explicitly"
            ),
            "budget": budget.to_dict(),
            "checkpoints": checkpoints,
        },
    )


def fake_offline_providers(descriptor: Mapping[str, Any]) -> FlowProviders:
    """The offline provider set a run was started with.

    Resuming a live run with fakes would silently change the answers, so this
    refuses: a live run must pass its own providers in.
    """
    from .offline_flow import fake_providers

    mode = descriptor.get("provider_mode")
    if mode != "fake-offline":
        raise ValueError(
            f"Run was started with provider_mode={mode!r}; resume will not substitute "
            "fake-offline providers for it. Inject the same providers explicitly."
        )
    return fake_providers()
