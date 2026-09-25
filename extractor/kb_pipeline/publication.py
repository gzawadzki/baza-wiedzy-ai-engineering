from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict

from .schemas import NotePatch

ALLOWLIST_DIRS = ("Pojęcia", "Procesy", "Narzędzia", "Zasady")

_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)}
)

_DELIMITER_PATTERN = re.compile(r"^(?:---|\.\.\.)[ \t]*(?:\r?\n|$)", re.MULTILINE)


class PublicationRejected(ValueError):
    pass


class PublicationConflict(ValueError):
    pass


class PlannedWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    relative_path: str
    note_id: str
    action: Literal["create", "replace"]
    base_hash: str | None = None
    proposed_hash: str

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


PublicationWrite = PlannedWrite


class PublicationPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    publication_id: str
    writes: list[PlannedWrite]

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def validate_relative_note_path(relative_path: str) -> str:
    if not isinstance(relative_path, str):
        raise PublicationRejected("Relative path must be a string")
    if not relative_path.strip():
        raise PublicationRejected("Relative path cannot be empty")
    if "\\" in relative_path:
        raise PublicationRejected("Backslashes are not permitted in relative paths")
    if ":" in relative_path:
        raise PublicationRejected("Colons and drive letters are not permitted in relative paths")
    if relative_path.startswith("/"):
        raise PublicationRejected("Absolute paths are not permitted")

    segments = relative_path.split("/")
    if any(s == "" for s in segments):
        raise PublicationRejected("Empty path segments are not permitted")
    if any(s == ".." for s in segments):
        raise PublicationRejected("Parent directory traversal segments are not permitted")
    if any(s == "." for s in segments):
        raise PublicationRejected("Current directory segments are not permitted")
    if len(segments) < 2:
        raise PublicationRejected("Relative path must contain a directory and a filename")

    for seg in segments:
        if seg.endswith(" ") or seg.endswith("."):
            raise PublicationRejected(f"Path segment '{seg}' cannot end in space or dot")
        if seg.startswith(" "):
            raise PublicationRejected(f"Path segment '{seg}' cannot start with space")

        stem = seg.split(".")[0].upper()
        if stem in _RESERVED_NAMES:
            raise PublicationRejected(f"Reserved device name '{seg}' is not permitted")

        if "." in seg:
            base = seg.rsplit(".", 1)[0]
            if base.endswith(" ") or base.endswith("."):
                raise PublicationRejected(f"Filename stem '{base}' cannot end in space or dot")

    top_dir = segments[0]
    if top_dir not in ALLOWLIST_DIRS:
        raise PublicationRejected(f"Path '{relative_path}' is outside allowlist directories")

    return "/".join(segments)


def _is_symlink_or_junction(path: Path) -> bool:
    if path.is_symlink():
        return True
    if hasattr(path, "is_junction") and path.is_junction():
        return True
    return False


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if text.startswith("\ufeff"):
        text = text[1:]

    if text.startswith("---\r\n"):
        offset = 5
    elif text.startswith("---\n"):
        offset = 4
    else:
        raise PublicationRejected("Frontmatter must open with '---'")

    match = _DELIMITER_PATTERN.search(text[offset:])
    if not match:
        raise PublicationRejected("Unclosed frontmatter")

    yaml_text = text[offset : offset + match.start()]
    body_text = text[offset + match.end() :]

    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        raise PublicationRejected(f"Invalid YAML in frontmatter: {exc}")

    if not isinstance(data, dict):
        raise PublicationRejected("Frontmatter must parse to a mapping")

    return data, body_text


def _validate_proposed_content(patch: NotePatch) -> None:
    data, body = _parse_frontmatter(patch.proposed_content)

    if not body.strip():
        raise PublicationRejected("Body after frontmatter must contain non-whitespace text")

    front_note_id = data.get("note_id")
    if front_note_id is None or str(front_note_id) != str(patch.note_id):
        raise PublicationRejected(
            f"note_id mismatch: frontmatter has {front_note_id!r}, patch has {patch.note_id!r}"
        )

    kb_val = data.get("kb_managed")
    if kb_val is not True and not (isinstance(kb_val, str) and kb_val.lower() == "true"):
        raise PublicationRejected("Frontmatter kb_managed must be true")

    claim_ids = data.get("claim_ids")
    if not isinstance(claim_ids, list):
        raise PublicationRejected("Frontmatter claim_ids must be a list")

    front_claims_set = set(str(c) for c in claim_ids)
    patch_claims_set = set(str(c) for c in patch.claim_ids)
    if not patch_claims_set.issubset(front_claims_set):
        raise PublicationRejected(
            f"Frontmatter claim_ids do not cover patch claim_ids: missing {patch_claims_set - front_claims_set}"
        )


def _collect_vault_entries(vault: Path) -> dict[str, str]:
    entries: dict[str, str] = {}

    def _walk(current_dir: Path, current_rel: str) -> None:
        try:
            items = list(current_dir.iterdir())
        except OSError:
            return
        for item in items:
            rel = f"{current_rel}/{item.name}" if current_rel else item.name
            entries[rel.casefold()] = rel
            if not _is_symlink_or_junction(item) and item.is_dir():
                _walk(item, rel)

    _walk(vault, "")
    return entries


def plan_publication(
    patches: Iterable[NotePatch | dict[str, Any]],
    vault: Path | str,
) -> PublicationPlan:
    vault_path = Path(vault).resolve()
    if not vault_path.exists() or not vault_path.is_dir():
        raise PublicationRejected(f"Vault directory does not exist or is not a directory: {vault}")

    existing_entries = _collect_vault_entries(vault_path)
    planned_cases: dict[str, str] = {}
    writes: list[PlannedWrite] = []

    for item in patches:
        if isinstance(item, dict):
            patch = NotePatch(**item)
        elif isinstance(item, NotePatch):
            patch = item
        elif (
            hasattr(item, "relative_path")
            and hasattr(item, "note_id")
            and hasattr(item, "claim_ids")
            and hasattr(item, "proposed_content")
        ):
            patch = NotePatch(
                note_id=item.note_id,
                relative_path=item.relative_path,
                section=getattr(item, "section", None),
                claim_ids=list(item.claim_ids),
                base_hash=getattr(item, "base_hash", None),
                proposed_content=item.proposed_content,
            )
        else:
            raise PublicationRejected(f"Unsupported patch type: {type(item)}")

        rel_path = validate_relative_note_path(patch.relative_path)
        rel_cf = rel_path.casefold()

        if rel_cf in planned_cases:
            raise PublicationRejected(
                f"Duplicate or colliding path in publication plan: '{rel_path}' collides with '{planned_cases[rel_cf]}'"
            )
        planned_cases[rel_cf] = rel_path

        # Case-collision check against existing files
        if rel_cf in existing_entries:
            exact_existing = existing_entries[rel_cf]
            if exact_existing != rel_path:
                raise PublicationRejected(
                    f"Case collision with existing path '{exact_existing}': '{rel_path}'"
                )

        # Case-collision check against existing parent directories
        segments = rel_path.split("/")
        for i in range(1, len(segments)):
            prefix = "/".join(segments[:i])
            prefix_cf = prefix.casefold()
            if prefix_cf in existing_entries:
                exact_prefix = existing_entries[prefix_cf]
                if exact_prefix != prefix:
                    raise PublicationRejected(
                        f"Case collision with existing directory '{exact_prefix}': '{prefix}'"
                    )

        # Symlink and escape checks
        current = vault_path
        for seg in segments:
            current = current / seg
            if _is_symlink_or_junction(current):
                raise PublicationRejected(f"Path or parent is a symlink: '{current}'")

        try:
            target_path = (vault_path / rel_path).resolve()
        except (RuntimeError, OSError) as exc:
            raise PublicationRejected(f"Cannot resolve path '{rel_path}': {exc}")

        if not target_path.is_relative_to(vault_path) or target_path == vault_path:
            raise PublicationRejected(f"Destination resolves outside vault: '{rel_path}'")

        # Validate proposed content frontmatter and body
        _validate_proposed_content(patch)

        # Determine action and check existing file conditions
        file_path = vault_path / rel_path
        if file_path.exists():
            if file_path.is_dir():
                raise PublicationRejected(f"Destination '{rel_path}' is an existing directory")

            if patch.base_hash is None:
                raise PublicationRejected(f"Destination file '{rel_path}' already exists but base_hash is None")

            action = "replace"
            current_bytes = file_path.read_bytes()
            current_hash = hashlib.sha256(current_bytes).hexdigest()

            if current_hash != patch.base_hash:
                raise PublicationConflict(
                    f"Base hash mismatch for '{rel_path}': expected {patch.base_hash}, found {current_hash}"
                )

            try:
                current_text = current_bytes.decode("utf-8-sig")
            except UnicodeDecodeError:
                raise PublicationRejected(f"Existing file '{rel_path}' is not valid UTF-8")

            existing_data, _ = _parse_frontmatter(current_text)

            existing_kb = existing_data.get("kb_managed")
            if existing_kb is not True and not (isinstance(existing_kb, str) and existing_kb.lower() == "true"):
                raise PublicationRejected(f"Existing file '{rel_path}' is not kb_managed")

            existing_note_id = existing_data.get("note_id")
            if existing_note_id is not None and str(existing_note_id) != str(patch.note_id):
                raise PublicationRejected(
                    f"Existing note_id mismatch for '{rel_path}': expected {patch.note_id}, found {existing_note_id}"
                )
        else:
            if patch.base_hash is not None:
                raise PublicationRejected(f"Cannot replace non-existent file '{rel_path}' with base_hash")
            action = "create"

        proposed_bytes = patch.proposed_content.encode("utf-8")
        proposed_hash = hashlib.sha256(proposed_bytes).hexdigest()

        writes.append(
            PlannedWrite(
                relative_path=rel_path,
                note_id=patch.note_id,
                action=action,
                base_hash=patch.base_hash,
                proposed_hash=proposed_hash,
            )
        )

    writes_payload = [
        {
            "action": w.action,
            "base_hash": w.base_hash,
            "note_id": w.note_id,
            "proposed_hash": w.proposed_hash,
            "relative_path": w.relative_path,
        }
        for w in writes
    ]
    canonical_json = json.dumps(writes_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    publication_id = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    return PublicationPlan(
        publication_id=publication_id,
        writes=writes,
    )
