"""CLM backend: X GraphQL raw history via the user's separate CLM repo (read only).

The CLM repo is never modified: its script runs with cwd=CLM_DIR (so it finds its own
x_cookies.json; this module never opens that file), but with a throw-away authors file and
--out inside the kb workspace, so CLM's monitored_authors.json is not touched. Raw posts are
normalized to the shape kb_pipeline already consumes (see ingestion.normalize/assemble).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .period import in_period, parse_day

DEFAULT_CLM_DIR = Path(r"D:\projects\CLM")
AUTHORS_FILE = "monitored_authors.json"
FETCH_SCRIPT = "fetch_raw_history_30d.py"
COOKIES_FILE = "x_cookies.json"
TIMEOUT_S = 900
_PROBLEM = re.compile(r"\[!\].*(HTTP \d{3}|Blad sieci|Traceback)", re.IGNORECASE)

Runner = Callable[..., Any]


def resolve_clm_dir(cli_value: Path | None) -> Path:
    return Path(cli_value or os.getenv("CLM_DIR") or DEFAULT_CLM_DIR)


def read_authors(clm_dir: Path) -> list[dict[str, Any]]:
    path = clm_dir / AUTHORS_FILE
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, list):
        raise ValueError(f"{path} nie jest lista")
    return [row for row in payload if isinstance(row, dict) and row.get("handle")]


def enabled_handles(clm_dir: Path) -> list[str]:
    return [str(row["handle"]) for row in read_authors(clm_dir) if row.get("enabled", True)]


def normalize_post(item: dict[str, Any], handle: str) -> dict[str, Any] | None:
    """CLM raw tweet -> kb_pipeline raw shape. Original fields are kept; aliases are added.

    Returns None for items without a numeric id or text (counted by the caller).
    """
    found = str(item.get("id") or item.get("id_str") or "")
    text = item.get("full_text") or item.get("text")
    if not found.isdigit() or not isinstance(text, str) or not text.strip():
        return None
    author = str(item.get("username") or item.get("author") or handle)
    out = dict(item)
    out["id"] = found
    out["full_text"] = text
    out["text"] = text
    out["username"] = author
    out["url"] = item.get("url") or f"https://x.com/{author}/status/{found}"
    if item.get("conversation_id"):
        out["conversation_id"] = str(item["conversation_id"])
    reply_to = item.get("in_reply_to_status_id")
    if reply_to:
        out["in_reply_to_status_id"] = str(reply_to)
    if "in_reply_to_screen_name" not in out and item.get("in_reply_to_user"):
        out["in_reply_to_screen_name"] = item["in_reply_to_user"]
    for src, dst in (("likes", "favorite_count"), ("retweets", "retweet_count")):
        if dst not in out and src in item:
            out[dst] = item[src]
    media = []
    for entry in item.get("media") or []:
        if isinstance(entry, dict) and entry.get("url"):
            media.append({"url": entry["url"], "type": entry.get("type", "photo")})
    out["media"] = media
    out["source_backend"] = "clm"
    return out


def normalize_posts(items: list[Any], handle: str, *, since: date | None = None, until: date | None = None):
    """Return (posts, skipped). since/until use the period.py window (inclusive/exclusive)."""
    posts: list[dict[str, Any]] = []
    skipped = 0
    for item in items:
        post = normalize_post(item, handle) if isinstance(item, dict) else None
        if post is None:
            skipped += 1
        elif since is None and until is None or in_period(post, since=since, until=until):
            posts.append(post)
    return posts, skipped


def days_since(since: str, today: date) -> int:
    return max(1, (today - parse_day(since)).days + 1)


def make_clm_fetch(
    clm_dir: Path,
    work_dir: Path,
    *,
    python: str | None = None,
    runner: Runner = subprocess.run,
    timeout: int = TIMEOUT_S,
    today: Callable[[], date] = lambda: datetime.now(timezone.utc).date(),
):
    """Build a fetch function with the same signature as apify_x.fetch_account."""

    def fetch(handle: str, *, since: str | None, until: str | None, limit: int) -> list[dict[str, Any]]:
        if not (clm_dir / FETCH_SCRIPT).is_file():
            raise RuntimeError(f"brak {FETCH_SCRIPT} w {clm_dir} (ustaw CLM_DIR / --clm-dir)")
        if not (clm_dir / COOKIES_FILE).is_file():  # existence only, never read
            raise RuntimeError(f"brak {COOKIES_FILE} w {clm_dir}")
        entry = next((r for r in read_authors(clm_dir) if str(r["handle"]).lower() == handle.lower()), None)
        if entry is None or not entry.get("user_id"):
            raise RuntimeError(f"@{handle} nie ma user_id w {AUTHORS_FILE} CLM; dodaj go tam")
        canonical = str(entry["handle"])
        out = work_dir / handle.lower()
        out.mkdir(parents=True, exist_ok=True)
        authors_tmp = out / "authors.json"
        authors_tmp.write_text(
            json.dumps([{"handle": canonical, "name": entry.get("name", canonical),
                         "user_id": str(entry["user_id"]), "enabled": True}], ensure_ascii=False),
            encoding="utf-8",
        )
        target = out / "raw" / f"{canonical}_raw_30d.json"
        target.unlink(missing_ok=True)  # never mistake a stale file for this run
        days = days_since(since, today()) if since else 14
        cmd = [python or sys.executable, str(clm_dir / FETCH_SCRIPT),
               "--authors", str(authors_tmp), "--days", str(days), "--out", str(out / "raw")]
        proc = runner(cmd, cwd=str(clm_dir), capture_output=True, text=True, encoding="utf-8",
                      errors="replace", timeout=timeout, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        stdout = getattr(proc, "stdout", "") or ""
        problems = [line.strip() for line in stdout.splitlines() if _PROBLEM.search(line)]
        if proc.returncode != 0:
            tail = ((getattr(proc, "stderr", "") or stdout).strip().splitlines() or [""])[-1][:200]
            raise RuntimeError(f"{FETCH_SCRIPT} zakonczyl sie kodem {proc.returncode}: {tail}")
        if problems:  # the script exits 0 even after HTTP/network errors, with partial data
            raise RuntimeError(f"CLM zglosil blad pobierania: {problems[0][:200]}")
        if not target.is_file():
            raise RuntimeError(f"CLM nie utworzyl {target.name}")
        payload = json.loads(target.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, list):
            raise ValueError(f"{target.name} nie jest lista")
        since_day = parse_day(since) if since else None
        until_day = parse_day(until) if until else None
        posts, _ = normalize_posts(payload, handle, since=since_day, until=until_day)
        return posts

    return fetch


def raw_files_for(raw_dir: Path, handle: str) -> list[Path]:
    """CLM files <handle>_raw_<N>d.json and kb files <handle>_raw_tweets.json (case-insensitive)."""
    pattern = re.compile(rf"^{re.escape(handle)}_raw_(\d+d|tweets)\.json$", re.IGNORECASE)
    return sorted(p for p in raw_dir.iterdir() if p.is_file() and pattern.match(p.name))


def read_raw_dir(raw_dir: Path, handle: str, *, since: date | None, until: date | None):
    """Return (files, posts, skipped) merged across all matching files, deduped by id."""
    files = raw_files_for(raw_dir, handle)
    merged: dict[str, dict[str, Any]] = {}
    skipped = 0
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, list):
            raise ValueError(f"{path.name} nie jest lista")
        posts, bad = normalize_posts(payload, handle, since=since, until=until)
        skipped += bad
        for post in posts:
            merged.setdefault(post["id"], post)
    return files, sorted(merged.values(), key=lambda p: int(p["id"])), skipped
