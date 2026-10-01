"""Screen cached posts with the local CLM gate. No fetch, Jev, extraction, or vault write."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .assemble import assemble_post
from .clm_client import require_ready, system_one
from .local_gate import decide_clm, filter_questions, screen_focus
from .period import published_at


def cache_handles(cache_dir: Path) -> list[str]:
    return sorted(path.name.removesuffix("_raw_tweets.json") for path in cache_dir.glob("*_raw_tweets.json"))


def _load(cache_dir: Path, handle: str) -> list[dict[str, Any]]:
    payload = json.loads((cache_dir / f"{handle}_raw_tweets.json").read_text(encoding="utf-8-sig"))
    if not isinstance(payload, list):
        raise ValueError(f"cache {handle} nie jest listą")
    return [item for item in payload if isinstance(item, dict)]


def _row(handle: str, assembled, status: str, reason: str, scores: dict[str, float] | None = None) -> dict[str, Any]:
    published = published_at({"created_at": assembled.published_at}) if assembled.published_at else None
    return {
        "source_id": assembled.source_id,
        "handle": handle,
        "status": status,
        "reason": reason,
        "published": None if published is None else published.date().isoformat(),
        "ocr_status": assembled.ocr_status,
        "images": assembled.image_count,
        "missing_parents": assembled.missing_ids,
        "scores": scores or {},
        "focus": assembled.focus_evidence[:240],
    }


def _judge(assembled) -> dict[str, Any]:
    # The embedder context is 2048 tokens. A full screenshot OCR can stall or reset it.
    response = system_one(assembled.focus_evidence[:1800], filter_questions())
    status, reason = decide_clm(response)
    answers = response.get("answers") if isinstance(response, dict) else {}
    scores = {}
    if isinstance(answers, dict):
        for key in ("focus_claim", "promotion"):
            answer = answers.get(key)
            if isinstance(answer, dict) and isinstance(answer.get("noul"), (int, float)):
                scores[key] = round(float(answer["noul"]), 4)
    return {"status": status, "reason": reason, "scores": scores}


def screen_cache(
    cache_dir: Path,
    workspace: Path,
    *,
    handles: list[str] | None = None,
    workers: int = 4,
) -> dict[str, Any]:
    selected = handles or cache_handles(cache_dir)
    loaded = {handle: _load(cache_dir, handle) for handle in selected}
    require_ready()
    rows: list[dict[str, Any]] = []
    pending = []
    for handle, items in loaded.items():
        for item in items:
            text = item.get("full_text") or item.get("text") or ""
            if isinstance(text, str) and text.startswith("RT @"):
                rows.append({"source_id": f"x:{item.get('id')}", "handle": handle, "status": "reject", "reason": "retweet", "scores": {}})
                continue
            try:
                assembled = assemble_post(item, handle=handle, known_items=items)
            except ValueError as exc:
                rows.append({"source_id": "x:?", "handle": handle, "status": "error", "reason": str(exc), "scores": {}})
                continue
            screened = screen_focus(assembled)
            if screened is not None:
                status, reason = screened
                rows.append(_row(handle, assembled, status, reason))
                continue
            pending.append((handle, assembled))

    def run(job):
        handle, assembled = job
        try:
            judged = _judge(assembled)
        except Exception as exc:
            return _row(handle, assembled, "error", f"clm: {exc}")
        return _row(handle, assembled, judged["status"], judged["reason"], judged["scores"])

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        rows.extend(pool.map(run, pending))
    counts: dict[str, int] = {}
    by_handle: dict[str, dict[str, int]] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
        bucket = by_handle.setdefault(row["handle"], {})
        bucket[row["reason"]] = bucket.get(row["reason"], 0) + 1
    report = {
        "cache_dir": str(cache_dir),
        "posts": len(rows),
        "counts": counts,
        "by_handle": by_handle,
        "items": rows,
    }
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "clm-screen.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report
