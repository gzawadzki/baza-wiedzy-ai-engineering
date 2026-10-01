"""Read-only vault audit and opt-in, content-addressed knowledge snapshot."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import yaml

KNOWLEDGE_DIRS = ("Pojęcia", "Procesy", "Narzędzia", "Zasady", "Źródła", "Skrzynka")
LINK = re.compile(r"(?<!\\)\[\[([^\]]+)\]\]")
URL = re.compile(r"https?://(?:www\.)?(?:x\.com|twitter\.com)/[^\s\])>\"']+/status/\d+")
BASELINE_QUERIES = (
    "kompaktowanie", "checkpoint", "persistencja", "compaction", "stan agenta",
)


def knowledge_files(vault: Path) -> list[Path]:
    """Select only knowledge files; never include .env, config, scripts or secrets."""
    files = [p for p in vault.iterdir() if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".md", ".canvas"}]
    for directory in KNOWLEDGE_DIRS:
        base = vault / directory
        if not base.is_dir() or base.is_symlink():
            continue
        files.extend(p for p in base.rglob("*") if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".md", ".canvas"})
    # Refuse to follow symlinked parents, including symlinked subfolders.
    return sorted((p for p in files if not any(parent.is_symlink() for parent in p.parents if parent != vault)), key=lambda p: p.relative_to(vault).as_posix())


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, None
    end = re.search(r"\n---(?:\r)?\n|\n\.\.\.(?:\r)?\n", text[4:])
    if end is None:
        return None, "unclosed frontmatter"
    try:
        value = yaml.safe_load(text[4:4 + end.start()])
        if value is not None and not isinstance(value, dict):
            return None, "frontmatter must be a mapping"
        return value or {}, None
    except yaml.YAMLError as exc:
        return None, f"invalid YAML ({type(exc).__name__})"


def audit(vault: Path) -> dict:
    vault = vault.resolve(strict=True)
    files = knowledge_files(vault)
    notes = [p for p in files if p.suffix.lower() == ".md"]
    stems = defaultdict(list)
    paths = set()
    for p in notes:
        rel = p.relative_to(vault).with_suffix("").as_posix()
        paths.add(rel.casefold())
        stems[p.stem.casefold()].append(p.relative_to(vault).as_posix())
    aliases = defaultdict(list)
    content = {}
    yaml_errors = []
    ids, urls = defaultdict(list), defaultdict(list)
    empty = []
    coverage = {"source_links_in_canonical_notes": 0, "canonical_notes_with_source_links": 0}
    for p in notes:
        rel = p.relative_to(vault).as_posix()
        text = p.read_text(encoding="utf-8-sig", errors="replace")
        content[rel] = text
        if not text.strip():
            empty.append(rel)
        front, error = _frontmatter(text)
        if error:
            yaml_errors.append({"path": rel, "error": error})
        if front:
            for key in ("id", "note_id"):
                if front.get(key):
                    ids[str(front[key])].append(rel)
            for alias in front.get("aliases", []) if isinstance(front.get("aliases", []), list) else []:
                if isinstance(alias, str):
                    aliases[alias.casefold()].append(rel)
        for url in set(URL.findall(text)):
            urls[url].append(rel)
        if not rel.startswith("Źródła/"):
            matches = URL.findall(text)
            coverage["source_links_in_canonical_notes"] += len(matches)
            coverage["canonical_notes_with_source_links"] += bool(matches)
    targets = defaultdict(list)
    for key, group in stems.items():
        targets[key].extend(group)
    for key, group in aliases.items():
        targets[key].extend(group)
    broken, ambiguous = [], []
    for rel, text in content.items():
        for match in LINK.finditer(text):
            target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
            if not target:  # local heading link
                continue
            target = target.removesuffix(".md")
            candidates = sorted(set(targets.get(target.casefold(), []) if "/" not in target else ([target + ".md"] if target.casefold() in paths else [])))
            if not candidates:
                broken.append({"path": rel, "target": target})
            elif len(candidates) > 1:
                ambiguous.append({"path": rel, "target": target, "candidates": candidates})
    baseline = {q: [rel for rel, text in content.items() if q.casefold() in text.casefold()] for q in BASELINE_QUERIES}
    return {
        "version": 1, "vault": str(vault),
        "counts": {"knowledge_files": len(files), "markdown": len(notes), "by_directory": dict(sorted(Counter(p.relative_to(vault).parts[0] if len(p.relative_to(vault).parts) > 1 else "." for p in files).items()))},
        "empty_files": empty, "invalid_yaml": yaml_errors,
        "duplicate_ids": {k: v for k, v in ids.items() if len(v) > 1},
        "duplicate_source_urls": {k: v for k, v in urls.items() if len(v) > 1},
        "duplicate_stems": {k: v for k, v in stems.items() if len(v) > 1},
        "aliases": dict(sorted(aliases.items())),
        "broken_links": broken, "ambiguous_links": ambiguous,
        "source_link_proxy": coverage,
        "baseline_search": baseline,
        "scope": "Existing state before publication; source-link counts are a proxy, not claim-level attribution.",
    }


def snapshot(vault: Path, destination: Path) -> dict:
    """Copy actual working-tree knowledge (including untracked), excluding credentials."""
    vault = vault.resolve(strict=True)
    destination = destination.resolve()
    if destination == vault or vault in destination.parents:
        raise ValueError("Snapshot must live outside the vault")
    if destination.exists():
        raise FileExistsError(destination)
    files = knowledge_files(vault)
    destination.mkdir(parents=True)
    manifest = {"version": 1, "vault": str(vault), "created_at": datetime.now(timezone.utc).isoformat(), "files": []}
    for source in files:
        rel = source.relative_to(vault)
        data = source.read_bytes()
        target = destination / "files" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if digest(target.read_bytes()) != digest(data):
            raise IOError(f"Snapshot mismatch: {rel}")
        manifest["files"].append({"path": rel.as_posix(), "bytes": len(data), "sha256": digest(data)})
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def verify_snapshot(destination: Path) -> list[str]:
    manifest = json.loads((destination / "manifest.json").read_text(encoding="utf-8"))
    errors = []
    for entry in manifest["files"]:
        rel = Path(entry["path"])
        if rel.is_absolute() or ".." in rel.parts:
            errors.append(entry["path"])
            continue
        path = destination / "files" / rel
        if not path.is_file() or path.is_symlink() or len(path.read_bytes()) != entry["bytes"] or digest(path.read_bytes()) != entry["sha256"]:
            errors.append(entry["path"])
    return errors
