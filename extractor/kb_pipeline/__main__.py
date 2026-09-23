"""Phase 0 offline CLI. Run from extractor/: python -m kb_pipeline ..."""

import argparse
import json
from pathlib import Path

from .audit import audit, snapshot, verify_snapshot
from .claim_extraction import extract_live_claims
from .jev_provider import JevError
from .live_jev import evaluate_live_source
from .pilot import run_pilot
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
    elif args.command == "verify-snapshot":
        errors = verify_snapshot(args.destination)
        print(json.dumps({"verified": not errors, "mismatches": errors}, ensure_ascii=False))
        if errors:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
