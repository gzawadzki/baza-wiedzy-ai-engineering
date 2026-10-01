"""Phase 0 offline CLI. Run from extractor/: python -m kb_pipeline ..."""

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from .account_run import run_accounts
from .clm_screen import screen_cache
from .audit import audit, snapshot, verify_snapshot
from .claim_extraction import extract_live_claims
from .jev_provider import JevError
from .live_adapters import configured_handles
from .live_jev import evaluate_live_source
from .offline_cli import resume_offline, run_offline
from .offline_flow import fake_providers
from .pilot import run_pilot
from .search_cli import RetrievalError, reindex_vault, search_index
from .storage import SourceStore


def main():
    parser = argparse.ArgumentParser(
        description="Offline vault audit, snapshot, and pilot dry-run (no publication)"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    a = commands.add_parser("audit", help="Inspect knowledge without changing the vault")
    a.add_argument("--vault", type=Path, required=True)
    a.add_argument("--report", type=Path, required=True)
    s = commands.add_parser("snapshot", help="Copy knowledge with a SHA-256 manifest")
    s.add_argument("--vault", type=Path, required=True)
    s.add_argument("--destination", type=Path, required=True)
    v = commands.add_parser("verify-snapshot")
    v.add_argument("--destination", type=Path, required=True)
    i = commands.add_parser("import-cache", help="Import existing JSON without network or vault writes")
    i.add_argument("--input", type=Path, required=True, help="Cache JSON file or directory")
    i.add_argument("--vault", type=Path, required=True)
    i.add_argument("--workspace", type=Path, required=True, help="Operational state outside the vault")
    p = commands.add_parser(
        "pilot-dry-run", help="Run the offline pilot without publishing or changing the vault"
    )
    p.add_argument("--vault", type=Path, required=True)
    p.add_argument("--workspace", type=Path, required=True, help="Operational state outside the vault")
    p.add_argument("--fixture", type=Path, required=True, help="Offline fixture JSON")
    j = commands.add_parser(
        "jev-evaluate", help="Evaluate an imported source with TypeSafe Jev filtering"
    )
    j.add_argument("--vault", type=Path, required=True)
    j.add_argument("--workspace", type=Path, required=True, help="Operational state outside the vault")
    j.add_argument("--source-id", type=str, required=True, help="X source ID (x:<numeric_id>)")
    j.add_argument("--content-hash", type=str, default=None, help="Content hash for ambiguous revisions")
    j.add_argument("--refresh", action="store_true", default=False, help="Refresh evaluation instead of using cache")
    j.add_argument("--model", type=str, default="jev-latest", help="TypeSafe model identifier")
    c = commands.add_parser(
        "claim-extract", help="Extract claims for an imported source revision filtered by Jev"
    )
    c.add_argument("--vault", type=Path, required=True, help="Vault directory")
    c.add_argument("--workspace", type=Path, required=True, help="Operational state outside the vault")
    c.add_argument("--source-id", type=str, required=True, help="X source ID (x:<numeric_id>)")
    c.add_argument("--content-hash", type=str, required=True, help="Content hash for the source revision")
    c.add_argument("--model", type=str, default="jev-latest", help="TypeSafe model identifier")
    r = commands.add_parser(
        "run",
        help="Pobierz okres, OCR i wątek, filtruj CLM+Jev, kategoryzuj, ekstrahuj "
             "(--offline: pełny przebieg offline od cache do propozycji sekcji)",
    )
    r.add_argument("--handles", default="", help="Konta X, rozdzielone przecinkami")
    r.add_argument("--since", default=None, help="Początek okresu YYYY-MM-DD, włącznie")
    r.add_argument("--until", default=None, help="Koniec okresu YYYY-MM-DD, wyłącznie")
    r.add_argument("--cache-dir", type=Path, default=Path("."))
    r.add_argument("--workspace", type=Path, required=True)
    r.add_argument("--vault", type=Path, default=None)
    r.add_argument("--limit", type=int, default=80)
    r.add_argument("--cache-only", action="store_true")
    r.add_argument("--publish", action="store_true", help="Zapisz notatki do vault/Źródła")
    r.add_argument(
        "--offline",
        action="store_true",
        help="Pionowy przebieg offline: cache -> źródła -> kontekst -> bramki -> tezy -> "
             "NotePatch -> plan publikacji (read-only, wstrzyknięci dostawcy fake)",
    )
    r.add_argument(
        "--offline-input",
        type=Path,
        default=None,
        help="Jawne wejście cache dla --offline: plik <handle>_raw_tweets.json "
             "albo katalog takich plików (bez sieci)",
    )
    r.add_argument(
        "--source-id",
        action="append",
        default=None,
        help="Ogranicz --offline do tych identyfikatorów x:<id> (powtarzalne)",
    )
    r.add_argument(
        "--run-id",
        default=None,
        help="Jawny identyfikator przebiegu dla --offline (domyślnie wyliczany z wejścia)",
    )
    r.add_argument(
        "--max-attempts",
        type=int,
        default=None,
        help="Twardy limit wywołań dostawcy na przebieg; przekroczenie zatrzymuje przebieg",
    )
    r.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Twardy limit tokenów na przebieg, z rezerwacją na podstawie zmierzonych wywołań",
    )
    rs = commands.add_parser(
        "resume",
        help="Kontynuuj przerwany przebieg offline z jego własnych punktów kontrolnych",
    )
    rs.add_argument("--run-id", required=True, help="Identyfikator przebiegu do wznowienia")
    rs.add_argument(
        "--workspace",
        type=Path,
        required=True,
        help="Workspace z punktami kontrolnymi tego przebiegu",
    )
    rs.add_argument(
        "--vault",
        type=Path,
        default=None,
        help="Vault używany read-only; domyślnie z deskryptora przebiegu",
    )
    rs.add_argument("--max-attempts", type=int, default=None)
    rs.add_argument("--max-tokens", type=int, default=None)
    s = commands.add_parser("screen-cache", help="Lokalny CLM na pobranym cache, bez Jev i bez vaulta")
    s.add_argument("--cache-dir", type=Path, default=Path("."))
    s.add_argument("--workspace", type=Path, required=True)
    s.add_argument("--handles", default="")
    s.add_argument("--workers", type=int, default=4)
    ri = commands.add_parser(
        "reindex",
        help="Rebuild the read-only section index from the vault into the workspace",
    )
    ri.add_argument("--vault", type=Path, required=True, help="Vault directory, read only")
    ri.add_argument(
        "--workspace", type=Path, required=True, help="Operational state outside the vault"
    )
    se = commands.add_parser("search", help="Query the workspace index; never writes to the vault")
    se.add_argument("query", help="Search phrase, e.g. \"kompaktowanie kontekstu\"")
    se.add_argument(
        "--workspace", type=Path, required=True, help="Workspace holding the retrieval index"
    )
    se.add_argument("--format", choices=("json",), default="json", help="Output format (json)")
    se.add_argument("--limit", type=int, default=10, help="Maximum number of results (1-100)")
    se.add_argument(
        "--include-sources",
        action="store_true",
        help="Also return sections from the Źródła/ evidence layer",
    )
    se.add_argument(
        "--vault",
        type=Path,
        default=None,
        help="Optional vault directory, resolved read-only and echoed in the output",
    )
    args = parser.parse_args()
    if args.command == "audit":
        result = audit(args.vault)
        report = args.report.resolve()
        vault = args.vault.resolve()
        if report == vault or vault in report.parents:
            parser.error("Report must live outside the vault")
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Audit: {result['counts']['markdown']} markdown files; report: {report}")
    elif args.command == "snapshot":
        result = snapshot(args.vault, args.destination)
        print(f"Snapshot: {len(result['files'])} files; manifest: {args.destination / 'manifest.json'}")
    elif args.command == "import-cache":
        vault = args.vault.resolve(strict=True)
        workspace = args.workspace.resolve()
        if workspace == vault or vault in workspace.parents:
            parser.error("Workspace must live outside the vault")
        paths = sorted(args.input.glob("*_raw_tweets.json")) if args.input.is_dir() else [args.input]
        with SourceStore(workspace) as store:
            result = {path.name: store.import_cache(path) for path in paths}
        print(json.dumps(result, ensure_ascii=False))
    elif args.command == "pilot-dry-run":
        try:
            result = run_pilot(args.vault, args.workspace, args.fixture)
        except (OSError, TypeError, ValueError) as exc:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=True))
            raise SystemExit(1) from None
        print(json.dumps(result, ensure_ascii=True))
        if result.get("status") == "error":
            raise SystemExit(1)
    elif args.command == "jev-evaluate":
        try:
            result = evaluate_live_source(
                vault=args.vault,
                workspace=args.workspace,
                source_id=args.source_id,
                content_hash=args.content_hash,
                refresh=args.refresh,
                model=args.model,
            )
        except (OSError, TypeError, ValueError, JevError) as exc:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=True))
            raise SystemExit(1) from None
        print(json.dumps(result, ensure_ascii=True))
        if result.get("status") == "error":
            raise SystemExit(1)
    elif args.command == "claim-extract":
        try:
            result = extract_live_claims(
                vault=args.vault,
                workspace=args.workspace,
                source_id=args.source_id,
                content_hash=args.content_hash,
                model=args.model,
            )
        except (OSError, TypeError, ValueError) as exc:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=True))
            raise SystemExit(1) from None
        print(json.dumps(result, ensure_ascii=True))
        if result.get("status") == "error":
            raise SystemExit(1)
    elif args.command == "screen-cache":
        workspace = args.workspace.resolve()
        cache_dir = args.cache_dir.resolve()
        if workspace == cache_dir or cache_dir in workspace.parents:
            parser.error("Workspace must live outside the cache directory")
        handles = [part.strip().lstrip("@") for part in args.handles.split(",") if part.strip()] or None
        try:
            result = screen_cache(cache_dir, workspace, handles=handles, workers=args.workers)
        except (OSError, RuntimeError, ValueError) as exc:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
            raise SystemExit(1) from None
        print(json.dumps({"status": "ok", "posts": result["posts"], "counts": result["counts"], "by_handle": result["by_handle"]}, ensure_ascii=False))
    elif args.command == "run":
        if args.publish:
            print(json.dumps({
                "status": "error",
                "error": "run --publish jest zablokowane: brak journala, backupu i rollbacku.",
                "detail": (
                    "Ta sciezka pisala wprost do vaultu/Źródła, omijajac apply_publication. "
                    "Uzyj run bez --publish (wynik laduje do stagingu w workspace) albo poczekaj "
                    "na podlaczenie bezpiecznego publishera."
                ),
            }, ensure_ascii=False))
            raise SystemExit(2)
        handles = [part.strip().lstrip("@") for part in args.handles.split(",") if part.strip()] or None
        if args.offline:
            if args.vault is None:
                print(json.dumps({
                    "status": "error",
                    "error": "run --offline wymaga --vault (używane tylko read-only).",
                }, ensure_ascii=False))
                raise SystemExit(1)
            try:
                result = run_offline(
                    vault=args.vault,
                    workspace=args.workspace,
                    cache_input=args.offline_input,
                    cache_dir=args.cache_dir,
                    handles=handles,
                    source_ids=args.source_id,
                    limit=args.limit,
                    providers=fake_providers(),
                    run_id=args.run_id,
                    max_attempts=args.max_attempts,
                    max_tokens=args.max_tokens,
                )
            except (OSError, RuntimeError, ValueError) as exc:
                print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
                raise SystemExit(1) from None
            print(json.dumps(result, ensure_ascii=False))
            if result["counters"]["error"] or result.get("budget_stopped"):
                raise SystemExit(1)
            return
        publish_dir = None
        try:
            result = run_accounts(
                handles=handles or configured_handles(),
                since=args.since,
                until=args.until,
                cache_dir=args.cache_dir,
                workspace=args.workspace,
                limit=args.limit,
                fetch=not args.cache_only,
                publish_dir=publish_dir,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
            raise SystemExit(1) from None
        print(json.dumps({"status": "ok", "handles": {name: {key: value[key] for key in ("fetched", "in_period", "extracted", "rejected", "deferred", "errors")} for name, value in result["handles"].items()}}, ensure_ascii=False))
    elif args.command == "resume":
        try:
            result = resume_offline(
                workspace=args.workspace,
                run_id=args.run_id,
                vault=args.vault,
                max_attempts=args.max_attempts,
                max_tokens=args.max_tokens,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
            raise SystemExit(1) from None
        print(json.dumps(result, ensure_ascii=False))
        if result["counters"]["error"] or result.get("budget_stopped"):
            raise SystemExit(1)
    elif args.command == "reindex":
        try:
            result = reindex_vault(args.vault, args.workspace)
        except RetrievalError as exc:
            print(json.dumps(exc.payload(), ensure_ascii=False))
            raise SystemExit(1) from None
        print(json.dumps(result, ensure_ascii=False))
    elif args.command == "search":
        try:
            result = search_index(
                args.workspace,
                args.query,
                vault=args.vault,
                include_sources=args.include_sources,
                limit=args.limit,
            )
        except RetrievalError as exc:
            print(json.dumps(exc.payload(), ensure_ascii=False))
            raise SystemExit(1) from None
        print(json.dumps(result, ensure_ascii=False))
    elif args.command == "verify-snapshot":
        errors = verify_snapshot(args.destination)
        print(json.dumps({"verified": not errors, "mismatches": errors}, ensure_ascii=False))
        if errors:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
