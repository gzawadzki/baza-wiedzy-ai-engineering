"""Fetch new X posts for a list of engineers into a raw cache in the workspace.

Network access is limited to apify_x.fetch_account (injectable for tests). No LLM
calls and no writes to the vault: raw results and the state file live in the
workspace directory (gitignored).
"""

from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from . import clm_source
from .apify_x import build_query, fetch_account
from .period import parse_day

DEFAULT_DAYS = 14
DEFAULT_LIMIT = 80
STATE_NAME = "fetch_state.json"
RAW_DIR = "raw"
CACHE_DIR = "cache"
HANDLE_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")
EXTRACTOR_DIR = Path(__file__).resolve().parents[1]
DEFAULT_ACCOUNTS = EXTRACTOR_DIR / "accounts.txt"
DEFAULT_WORKSPACE = EXTRACTOR_DIR.parent.parent / "kb-workspace"  # poza repo, obok niego

FetchFn = Callable[..., "list[dict[str, Any]]"]


def normalize_handle(raw: str) -> str:
    return raw.strip().lstrip("@")


def parse_accounts(path: Path) -> list[str]:
    """One handle per line; '#' starts a comment (whole line or trailing)."""
    handles: list[str] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        handle = normalize_handle(line.split("#", 1)[0])
        if handle:
            handles.append(handle)
    return unique_handles(handles)


def unique_handles(handles: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for handle in handles:
        handle = normalize_handle(handle)
        if handle and handle.lower() not in seen:
            seen.add(handle.lower())
            result.append(handle)
    return result


def load_env(path: Path | None = None) -> None:
    """Load extractor/.env into os.environ without overriding existing values."""
    path = path or EXTRACTOR_DIR / ".env"
    if not path.is_file():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
        return
    load_dotenv(dotenv_path=path, override=False)


def redact(message: str) -> str:
    token = os.getenv("APIFY_API_TOKEN", "").strip()
    return message.replace(token, "***") if token else message


# --- state -----------------------------------------------------------------

def load_state(workspace: Path) -> dict[str, Any]:
    path = workspace / STATE_NAME
    if not path.exists():
        return {"version": 1, "accounts": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} jest uszkodzony ({exc}); napraw albo usun plik") from exc
    if not isinstance(state, dict) or not isinstance(state.get("accounts"), dict):
        raise ValueError(f"{path} ma nieoczekiwany format")
    return state


def save_state(workspace: Path, state: dict[str, Any]) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    path = workspace / STATE_NAME
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def last_success(state: dict[str, Any], handle: str) -> str | None:
    value = state["accounts"].get(handle.lower(), {}).get("last_success")
    if value is None:
        return None
    parse_day(value)
    return value


# --- raw cache -------------------------------------------------------------

def tweet_id(item: dict[str, Any]) -> str:
    return str(item.get("id") or item.get("id_str") or "")


def _read_list(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, list):
        raise ValueError(f"{path.name} nie jest lista")
    return [item for item in payload if isinstance(item, dict)]


def known_ids(workspace: Path, handle: str, cache_dir: Path | None) -> set[str]:
    """Ids from earlier raw files of this handle (read only), incl. legacy cache."""
    paths: list[Path] = []
    raw_dir = workspace / RAW_DIR / handle.lower()
    if raw_dir.is_dir():
        paths.extend(sorted(raw_dir.glob("*.json")))
    if cache_dir is not None and cache_dir.is_dir():
        wanted = f"{handle.lower()}_raw_tweets.json"
        paths.extend(p for p in cache_dir.iterdir() if p.is_file() and p.name.lower() == wanted)
    cached = workspace / CACHE_DIR / f"{handle.lower()}_raw_tweets.json"
    if cached.is_file():
        paths.append(cached)
    ids: set[str] = set()
    for path in paths:
        ids.update(found for found in map(tweet_id, _read_list(path)) if found)
    return ids


def update_cache(workspace: Path, handle: str, new: list[dict[str, Any]]) -> Path:
    """Merged, deduped <handle>_raw_tweets.json: a drop-in --cache-dir for `run`/`run --offline`."""
    cache = workspace / CACHE_DIR
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / f"{handle.lower()}_raw_tweets.json"
    merged = {tweet_id(i): i for i in (_read_list(path) if path.exists() else [])}
    merged.update({tweet_id(i): i for i in new})
    ordered = sorted(merged.values(), key=lambda i: int(tweet_id(i)))
    path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_raw(workspace: Path, handle: str, items: list[dict[str, Any]], stamp: str) -> Path:
    raw_dir = workspace / RAW_DIR / handle.lower()
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{stamp}.json"
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


# --- planning and run ------------------------------------------------------

def plan_account(
    handle: str,
    *,
    state: dict[str, Any],
    since: str | None,
    until: str | None,
    today: date,
    default_days: int,
    open_window: bool = False,
) -> dict[str, Any]:
    if not HANDLE_RE.match(handle):
        raise ValueError(f"niepoprawny handle: {handle!r}")
    if since:
        effective, source = since, "--since"
    elif open_window:  # import of existing files: no implicit lower bound
        return {"handle": handle, "since": None, "since_source": "all", "until": until,
                "query": build_query(handle, None, until)}
    elif (stored := last_success(state, handle)) is not None:
        effective, source = stored, "state"
    else:
        effective, source = (today - timedelta(days=default_days)).isoformat(), f"default-{default_days}d"
    if until and parse_day(effective) >= parse_day(until):
        raise ValueError(f"since {effective} nie jest wczesniejsze niz until {until}")
    return {
        "handle": handle,
        "since": effective,
        "since_source": source,
        "until": until,
        "query": build_query(handle, effective, until),
    }


def run_fetch(
    *,
    handles: list[str],
    workspace: Path,
    since: str | None = None,
    until: str | None = None,
    limit: int = DEFAULT_LIMIT,
    default_days: int = DEFAULT_DAYS,
    dry_run: bool = False,
    fetch_fn: FetchFn = fetch_account,
    cache_dir: Path | None = None,
    now: datetime | None = None,
    backend: str = "apify",
    limited: bool = True,
    update_state: bool = True,
    open_window: bool = False,
    describe: Callable[[str, dict[str, Any]], str] | None = None,
) -> dict[str, Any]:
    """limited: the backend honours `limit` (Apify); then a full page means a cut-off window.
    update_state=False (import of old files) never moves the per-handle watermark."""
    if since:
        parse_day(since)
    if until:
        parse_day(until)
    if since and until and parse_day(since) >= parse_day(until):
        raise ValueError("since musi byc wczesniejsze niz until")
    if limit < 1:
        raise ValueError("limit musi byc dodatni")
    now = now or datetime.now(timezone.utc)
    today = now.date()
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    state = load_state(workspace)
    report: dict[str, Any] = {
        "dry_run": dry_run, "backend": backend, "workspace": str(workspace), "accounts": {},
    }
    for handle in unique_handles(handles):
        row: dict[str, Any] = {"status": "ok"}
        report["accounts"][handle] = row
        try:
            plan = plan_account(
                handle, state=state, since=since, until=until, today=today,
                default_days=default_days, open_window=open_window,
            )
            row.update({k: plan[k] for k in ("since", "since_source", "until", "query")})
            if backend != "apify":
                row["query"] = None
            if describe is not None:
                row["plan"] = describe(handle, plan)
            if dry_run:
                row["status"] = "dry-run"
                continue
            seen = known_ids(workspace, handle, cache_dir)
            fetched = fetch_fn(handle, since=plan["since"], until=until, limit=limit)
            new: list[dict[str, Any]] = []
            for item in fetched:
                found = tweet_id(item) if isinstance(item, dict) else ""
                if found and found not in seen:
                    seen.add(found)
                    new.append(item)
            truncated = limited and len(fetched) >= limit
            row.update({"fetched": len(fetched), "new": len(new), "truncated": truncated})
            if new:
                row["raw_file"] = str(write_raw(workspace, handle, new, stamp))
                row["cache_file"] = str(update_cache(workspace, handle, new))
            # A partial window (explicit --until, or hit the limit) must not move the
            # watermark, otherwise older posts would be skipped on the next run.
            if update_state and until is None and not truncated:
                state["accounts"][handle.lower()] = {
                    "last_success": today.isoformat(),
                    "last_run_at": now.isoformat(timespec="seconds"),
                    "new": len(new),
                }
                save_state(workspace, state)
            else:
                row["state_updated"] = False
        except Exception as exc:  # per-account isolation; others must still run
            row["status"] = "error"
            row["error"] = redact(f"{type(exc).__name__}: {exc}")
    return report


def format_report(report: dict[str, Any]) -> str:
    mode = " (dry-run, bez pobierania)" if report["dry_run"] else ""
    lines = [f"fetch [{report['backend']}]{mode}; workspace: {report['workspace']}"]
    for handle, row in report["accounts"].items():
        if row["status"] == "error":
            lines.append(f"  @{handle}: BLAD - {row['error']}")
        elif report["dry_run"]:
            detail = row.get("plan") or row.get("query") or ""
            lines.append(f"  @{handle}: od {row['since'] or 'poczatku'} ({row['since_source']}) | {detail}")
        else:
            note = " [ucieto limitem; watermark nie przesuniety]" if row.get("truncated") else ""
            if row.get("state_updated") is False and not row.get("truncated"):
                note = " [stan (watermark) nie zmieniony]"
            lines.append(
                f"  @{handle}: nowych {row['new']} (pobrano {row['fetched']}, od {row['since'] or 'poczatku'}){note}"
            )
    if not report["dry_run"]:
        total = sum(row.get("new", 0) for row in report["accounts"].values())
        errors = sum(row["status"] == "error" for row in report["accounts"].values())
        lines.append(f"razem nowych: {total}; bledy: {errors}")
    return "\n".join(lines)


VAULT_DIRS = ("Pojecia", "Narzedzia", "Procesy", "Zasady", "\u0179r\u00f3d\u0142a", ".obsidian")


def inside_vault(workspace: Path) -> bool:
    repo = EXTRACTOR_DIR.parent.resolve()
    target = workspace.resolve()
    return any(target == repo / name or (repo / name) in target.parents for name in VAULT_DIRS)


def resolve_handles(args, backend: str, clm_dir: Path) -> list[str]:
    """--handle > --accounts > (clm: enabled CLM authors | apify: extractor/accounts.txt)."""
    if args.handle:
        return unique_handles(args.handle)
    if args.accounts:
        return parse_accounts(args.accounts)
    if backend == "clm" and not args.from_raw_dir:
        return unique_handles(clm_source.enabled_handles(clm_dir))
    return parse_accounts(DEFAULT_ACCOUNTS)


def run_command(args) -> int:
    """CLI entry: returns the process exit code."""
    if inside_vault(args.workspace):
        print("Workspace nie moze lezec w vaulcie (Pojecia/Narzedzia/Procesy/Zasady/Zrodla).")
        return 1
    backend = args.backend
    clm_dir = clm_source.resolve_clm_dir(args.clm_dir)
    importing = args.from_raw_dir is not None
    try:
        handles = resolve_handles(args, backend, clm_dir)
    except (OSError, ValueError) as exc:
        print(f"Nie mozna ustalic listy kont: {exc}")
        return 1
    if not handles:
        print("Brak kont do pobrania (pusta lista).")
        return 1
    load_env()
    kwargs: dict[str, Any] = {}
    if importing:
        raw_dir = args.from_raw_dir
        if not raw_dir.is_dir():
            print(f"Brak katalogu --from-raw-dir: {raw_dir}")
            return 1
        kwargs.update(
            backend="clm-import", limited=False, update_state=False, open_window=True,
            fetch_fn=_import_fetch(raw_dir), describe=_import_describe(raw_dir),
        )
    elif backend == "clm":
        if not args.dry_run and not (clm_dir / clm_source.FETCH_SCRIPT).is_file():
            print(f"Brak {clm_source.FETCH_SCRIPT} w {clm_dir} (ustaw CLM_DIR albo --clm-dir).")
            return 1
        kwargs.update(
            backend="clm", limited=False,
            fetch_fn=clm_source.make_clm_fetch(
                clm_dir, args.workspace / "clm_tmp", python=os.getenv("CLM_PYTHON") or None
            ),
            describe=lambda handle, plan: (
                f"CLM {clm_source.FETCH_SCRIPT} --days {clm_source.days_since(plan['since'], datetime.now(timezone.utc).date())}"
                f" (cwd {clm_dir})"
            ),
        )
    else:
        if not args.dry_run and not os.getenv("APIFY_API_TOKEN", "").strip():
            print("Brak APIFY_API_TOKEN (ustaw w extractor/.env). Nic nie pobrano.")
            return 1
        kwargs.update(backend="apify", fetch_fn=fetch_account)
    try:
        report = run_fetch(
            handles=handles,
            workspace=args.workspace,
            since=args.since,
            until=args.until,
            limit=args.limit,
            default_days=args.default_days,
            dry_run=args.dry_run,
            cache_dir=args.cache_dir,
            **kwargs,
        )
    except (OSError, ValueError) as exc:
        print(redact(f"Blad: {exc}"))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else format_report(report))
    return 1 if any(row["status"] == "error" for row in report["accounts"].values()) else 0


def _import_fetch(raw_dir: Path) -> FetchFn:
    def fetch(handle: str, *, since: str | None, until: str | None, limit: int) -> list[dict[str, Any]]:
        since_day = parse_day(since) if since else None
        until_day = parse_day(until) if until else None
        files, posts, _ = clm_source.read_raw_dir(raw_dir, handle, since=since_day, until=until_day)
        if not files:
            raise FileNotFoundError(f"brak plikow {handle}_raw_*.json w {raw_dir}")
        return posts

    return fetch


def _import_describe(raw_dir: Path) -> Callable[[str, dict[str, Any]], str]:
    def describe(handle: str, plan: dict[str, Any]) -> str:
        names = [p.name for p in clm_source.raw_files_for(raw_dir, handle)] if raw_dir.is_dir() else []
        return "import: " + (", ".join(names) if names else "BRAK PLIKOW")

    return describe
