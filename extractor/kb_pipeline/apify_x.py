"""Apify fetch for a date window and missing thread posts."""

from __future__ import annotations

import os
from typing import Any


def _client():
    token = os.getenv("APIFY_API_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Brak APIFY_API_TOKEN")
    from apify_client import ApifyClient
    return ApifyClient(token)


def _collect(query: str, limit: int) -> list[dict[str, Any]]:
    client = _client()
    run = client.actor("scrape.badger/twitter-tweets-scraper").call(run_input={
        "mode": "Advanced Search",
        "query": query,
        "query_type": "Latest",
        "max_results": limit,
    })
    dataset_id = getattr(run, "default_dataset_id", None) or (run.get("defaultDatasetId") if isinstance(run, dict) else None)
    if not dataset_id:
        raise RuntimeError("Apify nie zwrócił datasetu")
    return [item for item in client.dataset(dataset_id).iterate_items() if isinstance(item, dict)]


def fetch_account(handle: str, *, since: str | None, until: str | None, limit: int) -> list[dict[str, Any]]:
    query = f"from:{handle.lstrip('@')}"
    if since:
        query += f" since:{since}"
    if until:
        query += f" until:{until}"
    return _collect(query, limit)


def fetch_status(tweet_id: str, *, limit: int = 20) -> dict[str, Any] | None:
    if not tweet_id.isdigit():
        return None
    for item in _collect(f"conversation_id:{tweet_id}", limit):
        found = str(item.get("id") or item.get("id_str") or "")
        if found == tweet_id:
            return item
    return None
