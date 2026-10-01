"""Run the requested pipeline for configured accounts and a date window."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .apify_x import fetch_account, fetch_status
from .live_adapters import (
    configured_handles,
    make_categorizer,
    make_jev,
    make_local_filter,
    make_summarizer,
    require_runtime_config,
)
from .notes import write_staging
from .period import in_period, parse_day
from .run_flow import FlowResult, process_post


def _load_cache(cache_dir: Path, handle: str) -> list[dict[str, Any]]:
    path = cache_dir / f"{handle}_raw_tweets.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, list):
        raise ValueError(f"cache {path.name} nie jest listą")
    return [item for item in payload if isinstance(item, dict)]


def _save_cache(cache_dir: Path, handle: str, items: list[dict[str, Any]]) -> None:
    merged: dict[str, dict[str, Any]] = {}
    loose: list[dict[str, Any]] = []
    for item in items:
        found = str(item.get("id") or item.get("id_str") or "")
        if found.isdigit():
            merged[found] = item
        else:
            loose.append(item)
    path = cache_dir / f"{handle}_raw_tweets.json"
    path.write_text(json.dumps([*merged.values(), *loose], ensure_ascii=False, indent=2), encoding="utf-8")


def analyze_loaded(
    items: list[dict[str, Any]],
    *,
    handle: str,
    known_items: list[dict[str, Any]],
    local_filter,
    jev_evaluate,
    categorize,
    summarize,
    ocr_url=None,
    fetch_status=None,
) -> list[FlowResult]:
    memo: dict[str, dict[str, Any] | None] = {}
    pool = list(known_items)

    def remember(tweet_id: str) -> dict[str, Any] | None:
        if fetch_status is None:
            return None
        if tweet_id not in memo:
            memo[tweet_id] = fetch_status(tweet_id)
            if isinstance(memo[tweet_id], dict):
                pool.append(memo[tweet_id])
        return memo[tweet_id]

    return [
        process_post(
            item,
            handle=handle,
            known_items=pool,
            ocr_url=ocr_url,
            fetch_status=None if fetch_status is None else remember,
            local_filter=local_filter,
            jev_evaluate=jev_evaluate,
            categorize=categorize,
            summarize=summarize,
        )
        for item in items
    ]


def _result_row(result: FlowResult) -> dict[str, Any]:
    return {
        "source_id": result.source_id,
        "status": result.status,
        "reason": result.reason,
        "category": result.category,
        "title": None if result.summary is None else result.summary.get("title"),
        "ocr_status": None if result.assembled is None else result.assembled.ocr_status,
        "missing_ids": [] if result.assembled is None else result.assembled.missing_ids,
    }


def run_accounts(
    *,
    handles: list[str] | None,
    since: str | None,
    until: str | None,
    cache_dir: Path,
    workspace: Path,
    limit: int = 80,
    fetch: bool = True,
    publish_dir: Path | None = None,
) -> dict[str, Any]:
    if publish_dir is not None:
        raise ValueError(
            "run_accounts(publish_dir=...) jest zablokowane: brak journala, backupu i rollbacku. "
            "Ta sciezka pisala wprost do vaultu, omijajac apply_publication. "
            "Wynik laduj do stagingu w workspace, czyli wywolaj bez publish_dir."
        )
    config = require_runtime_config()
    since_day = parse_day(since) if since else None
    until_day = parse_day(until) if until else None
    if since_day and until_day and since_day >= until_day:
        raise ValueError("since musi być wcześniejsze niż until")
    selected = handles or configured_handles()
    local_filter = make_local_filter(config["local_base"], config["local_key"], config["local_model"])
    categorize = make_categorizer(config["local_base"], config["local_key"], config["local_model"])
    summarize = make_summarizer(config["extraction_base"], config["extraction_key"], config["extraction_model"])
    jev = make_jev(config["jev_model"])
    report: dict[str, Any] = {"model": config["extraction_model"], "handles": {}}
    for handle in selected:
        cached = _load_cache(cache_dir, handle)
        fetched: list[dict[str, Any]] = []
        if fetch:
            fetched = fetch_account(handle, since=since, until=until, limit=limit)
            _save_cache(cache_dir, handle, [*cached, *fetched])
            cached = _load_cache(cache_dir, handle)
        window = [item for item in cached if in_period(item, since=since_day, until=until_day)]
        results = analyze_loaded(
            window,
            handle=handle,
            known_items=cached,
            local_filter=local_filter,
            jev_evaluate=jev,
            categorize=categorize,
            summarize=summarize,
            fetch_status=fetch_status if fetch else None,
        )
        staging = write_staging(results, handle, workspace / "staging" / handle)
        report["handles"][handle] = {
            "fetched": len(fetched),
            "in_period": len(window),
            "extracted": sum(result.status == "extract" for result in results),
            "rejected": sum(result.status == "reject" for result in results),
            "deferred": sum(result.status == "defer" for result in results),
            "errors": sum(result.status == "error" for result in results),
            "staging": staging,
            "items": [_result_row(result) for result in results],
        }
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "run-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
