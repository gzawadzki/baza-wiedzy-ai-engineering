from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

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


class PublicationInterrupted(RuntimeError):
    """Raised when a simulated or real crash stops apply before commit."""

    def __init__(self, publication_id: str, applied: int):
        super().__init__(
            f"Publication '{publication_id}' interrupted after {applied} write(s); recover required"
        )
        self.publication_id = publication_id
        self.applied = applied


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

    filename = segments[-1]
    if not filename.casefold().endswith(".md"):
        raise PublicationRejected(
            f"Destination filename must end with '.md' case-insensitively: '{relative_path}'"
        )
    stem_part = filename[:-3]
    if not stem_part or stem_part.endswith(" ") or stem_part.endswith("."):
        raise PublicationRejected(
            f"Destination filename stem cannot be empty or end in dot or space: '{filename}'"
        )

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


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str, str]:
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

    return data, body_text, yaml_text


def _validate_frontmatter_kb_managed(yaml_text: str, data: dict[str, Any]) -> None:
    kb_val = data.get("kb_managed")
    if not isinstance(kb_val, bool) or kb_val is not True:
        raise PublicationRejected("Frontmatter kb_managed must be boolean True")

    try:
        node = yaml.compose(yaml_text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise PublicationRejected(f"Invalid YAML in frontmatter: {exc}")

    if isinstance(node, yaml.MappingNode):
        for k_node, v_node in node.value:
            if isinstance(k_node, yaml.ScalarNode) and k_node.value == "kb_managed":
                if (
                    not isinstance(v_node, yaml.ScalarNode)
                    or v_node.tag != "tag:yaml.org,2002:bool"
                    or v_node.value.lower() != "true"
                ):
                    raise PublicationRejected(
                        "Frontmatter kb_managed must be boolean True (cannot be string or YAML yes/on)"
                    )


def _validate_proposed_content(patch: NotePatch) -> None:
    data, body, yaml_text = _parse_frontmatter(patch.proposed_content)

    if not body.strip():
        raise PublicationRejected("Body after frontmatter must contain non-whitespace text")

    front_note_id = data.get("note_id")
    if front_note_id is None or str(front_note_id) != str(patch.note_id):
        raise PublicationRejected(
            f"note_id mismatch: frontmatter has {front_note_id!r}, patch has {patch.note_id!r}"
        )

    _validate_frontmatter_kb_managed(yaml_text, data)

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


def _coerce_patch(item: NotePatch | dict[str, Any]) -> NotePatch:
    if isinstance(item, dict):
        return NotePatch(**item)
    if isinstance(item, NotePatch):
        return item
    if (
        hasattr(item, "relative_path")
        and hasattr(item, "note_id")
        and hasattr(item, "claim_ids")
        and hasattr(item, "proposed_content")
    ):
        return NotePatch(
            note_id=item.note_id,
            relative_path=item.relative_path,
            section=getattr(item, "section", None),
            claim_ids=list(item.claim_ids),
            base_hash=getattr(item, "base_hash", None),
            proposed_content=item.proposed_content,
        )
    raise PublicationRejected(f"Unsupported patch type: {type(item)}")


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
        patch = _coerce_patch(item)

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

            existing_data, _, existing_yaml = _parse_frontmatter(current_text)
            _validate_frontmatter_kb_managed(existing_yaml, existing_data)

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


_JOURNAL_NAME = "journal.json"
_LOCK_NAME = "publication.lock"
_PUB_TMP_SUFFIX = ".pubtmp"
_IN_PROGRESS = frozenset({"preparing", "applying", "rolling_back"})


class PublicationReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    publication_id: str
    status: Literal["committed", "already_committed"]
    journal_ref: str
    backup_ref: str | None = None
    managed_paths: list[str] = Field(default_factory=list)


class RollbackReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    publication_id: str
    status: Literal["rolled_back", "already_rolled_back"]
    restored_paths: list[str] = Field(default_factory=list)


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _reject_symlink_parents(path: Path) -> None:
    current = path
    while True:
        if current.exists() and _is_symlink_or_junction(current):
            raise PublicationRejected(f"Refusing symlink or junction: '{current}'")
        if current == current.parent:
            break
        current = current.parent


def _workspace_roots(vault: Path | str, workspace: Path | str) -> tuple[Path, Path]:
    vault_path = Path(vault).resolve(strict=False)
    if not vault_path.exists() or not vault_path.is_dir():
        raise PublicationRejected(f"Vault directory does not exist or is not a directory: {vault}")
    _reject_symlink_parents(vault_path)

    workspace_path = Path(workspace)
    _reject_symlink_parents(workspace_path)
    workspace_abs = Path(os.path.abspath(workspace_path))
    vault_abs = Path(os.path.abspath(vault_path))
    if _is_within(workspace_abs, vault_abs) or workspace_abs == vault_abs:
        raise PublicationRejected("Workspace must be outside the vault")

    workspace_path.mkdir(parents=True, exist_ok=True)
    workspace_real = workspace_path.resolve(strict=True)
    vault_real = vault_path.resolve(strict=True)
    if _is_within(workspace_real, vault_real) or workspace_real == vault_real:
        raise PublicationRejected("Workspace must be outside the vault")
    return vault_real, workspace_real


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _atomic_write(dest: Path, data: bytes) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f".{dest.name}{_PUB_TMP_SUFFIX}"
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(tmp, flags)
    try:
        os.write(fd, data)
        os.fsync(fd)
    except Exception:
        os.close(fd)
        tmp.unlink(missing_ok=True)
        raise
    os.close(fd)
    try:
        os.replace(tmp, dest)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def _lock_path(workspace: Path) -> Path:
    return workspace / _LOCK_NAME


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import ctypes

        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _acquire_lock(workspace: Path, publication_id: str) -> None:
    path = _lock_path(workspace)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    try:
        fd = os.open(path, flags)
    except FileExistsError as exc:
        raise PublicationRejected("Another publication holds the lock") from exc
    try:
        payload = json.dumps({"pid": os.getpid(), "publication_id": publication_id}).encode("utf-8")
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def _release_lock(workspace: Path) -> None:
    _lock_path(workspace).unlink(missing_ok=True)


def _publication_dir(workspace: Path, publication_id: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{64}", publication_id):
        raise PublicationRejected("publication_id must be a 64-character sha256 hex digest")
    return workspace / "publications" / publication_id


def _journal_path(workspace: Path, publication_id: str) -> Path:
    return _publication_dir(workspace, publication_id) / _JOURNAL_NAME


def _journal_ref(publication_id: str) -> str:
    return f"publications/{publication_id}/journal.json"


def _backup_ref(publication_id: str) -> str:
    return f"publications/{publication_id}/backup"


def _load_journal(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PublicationRejected(f"Unreadable publication journal: {path}") from exc
    if not isinstance(data, dict):
        raise PublicationRejected("Publication journal must be an object")
    writes = data.get("writes")
    if not isinstance(writes, list):
        raise PublicationRejected("Publication journal writes must be a list")
    for write in writes:
        if not isinstance(write, dict):
            raise PublicationRejected("Publication journal write must be an object")
        validate_relative_note_path(str(write.get("relative_path", "")))
    return data


def _save_journal(path: Path, journal: dict[str, Any]) -> None:
    _atomic_write(path, (json.dumps(journal, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def _iter_journals(workspace: Path) -> list[tuple[Path, dict[str, Any]]]:
    root = workspace / "publications"
    if not root.exists():
        return []
    found: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.glob(f"*/{_JOURNAL_NAME}")):
        found.append((path, _load_journal(path)))
    return found


def _in_progress_journals(workspace: Path) -> list[dict[str, Any]]:
    return [journal for _, journal in _iter_journals(workspace) if journal.get("status") in _IN_PROGRESS]


def _content_hash(patch: NotePatch) -> str:
    return _sha256_bytes(patch.proposed_content.encode("utf-8"))


def _find_already_committed(
    workspace: Path,
    vault: Path,
    patches: Sequence[NotePatch],
) -> dict[str, Any] | None:
    expected: dict[str, tuple[str, str]] = {}
    for patch in patches:
        rel = validate_relative_note_path(patch.relative_path)
        digest = _content_hash(patch)
        identity = (digest, patch.note_id)
        if rel in expected and expected[rel] != identity:
            raise PublicationRejected(f"Conflicting proposed content for '{rel}'")
        expected[rel] = identity
    matches: list[dict[str, Any]] = []
    for _, journal in _iter_journals(workspace):
        if journal.get("status") != "committed":
            continue
        writes = journal["writes"]
        paths = [write["relative_path"] for write in writes]
        if set(paths) != set(expected):
            continue
        if any(
            write["proposed_hash"] != expected[write["relative_path"]][0]
            or write["note_id"] != expected[write["relative_path"]][1]
            for write in writes
        ):
            continue
        if all(_file_hash_or_none(vault / write["relative_path"]) == write["proposed_hash"] for write in writes):
            matches.append(journal)
    if len(matches) > 1:
        raise PublicationRejected("Multiple committed journals match this publication")
    return matches[0] if matches else None


def _file_hash_or_none(path: Path) -> str | None:
    if _is_symlink_or_junction(path):
        raise PublicationConflict(f"Refusing symlink at '{path}'")
    if not path.exists():
        return None
    if not path.is_file():
        raise PublicationConflict(f"Expected a file at '{path}'")
    return _sha256_file(path)


def _pre_image_matches(vault: Path, write: Mapping[str, Any]) -> bool:
    path = vault / write["relative_path"]
    current = _file_hash_or_none(path)
    if write["action"] == "create":
        return current is None
    return current == write["base_hash"]


def _proposed_matches(vault: Path, write: Mapping[str, Any]) -> bool:
    return _file_hash_or_none(vault / write["relative_path"]) == write["proposed_hash"]


def _receipt_from_journal(journal: dict[str, Any], status: Literal["committed", "already_committed"]) -> PublicationReceipt:
    publication_id = journal["publication_id"]
    writes = journal["writes"]
    backup_ref = _backup_ref(publication_id) if any(write["action"] == "replace" for write in writes) else None
    return PublicationReceipt(
        publication_id=publication_id,
        status=status,
        journal_ref=_journal_ref(publication_id),
        backup_ref=backup_ref,
        managed_paths=[write["relative_path"] for write in writes],
    )


def _created_directories(vault: Path, relative_path: str) -> list[str]:
    created: list[str] = []
    parts = relative_path.split("/")[:-1]
    current = vault
    rel_parts: list[str] = []
    for part in parts:
        current = current / part
        rel_parts.append(part)
        if not current.exists():
            created.append("/".join(rel_parts))
    return created


def _restore_write(vault: Path, workspace: Path, publication_id: str, write: Mapping[str, Any]) -> None:
    dest = vault / write["relative_path"]
    if _is_symlink_or_junction(dest):
        raise PublicationConflict(f"Refusing symlink at '{dest}'")
    if write["action"] == "create":
        if dest.exists():
            dest.unlink()
        return
    backup = _publication_dir(workspace, publication_id) / "backup" / write["relative_path"]
    if not backup.is_file():
        raise PublicationConflict(f"Missing backup for '{write['relative_path']}'")
    data = backup.read_bytes()
    if _sha256_bytes(data) != write["base_hash"]:
        raise PublicationConflict(f"Backup hash mismatch for '{write['relative_path']}'")
    _atomic_write(dest, data)


def _remove_empty_created_dirs(vault: Path, relative_dirs: Sequence[str]) -> None:
    for relative in sorted(relative_dirs, key=lambda item: item.count("/"), reverse=True):
        path = vault / relative
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def _rollback_journal(vault: Path, workspace: Path, journal: dict[str, Any]) -> RollbackReceipt:
    publication_id = str(journal["publication_id"])
    if journal.get("vault") != str(vault):
        raise PublicationRejected("Journal vault does not match the requested vault")
    if journal.get("status") == "rolled_back":
        return RollbackReceipt(publication_id=publication_id, status="already_rolled_back", restored_paths=[])
    if journal.get("status") not in {"committed", "applying", "preparing", "rolling_back"}:
        raise PublicationRejected(f"Cannot roll back publication in status '{journal.get('status')}'")

    writes = journal["writes"]
    for write in writes:
        if write.get("phase") == "restored":
            if not _pre_image_matches(vault, write):
                raise PublicationConflict(
                    f"Later change blocks rollback of '{write['relative_path']}'"
                )
            continue
        if _proposed_matches(vault, write) or _pre_image_matches(vault, write):
            continue
        raise PublicationConflict(
            f"Later change blocks rollback of '{write['relative_path']}'"
        )

    journal["status"] = "rolling_back"
    _save_journal(_journal_path(workspace, publication_id), journal)

    restored: list[str] = []
    for write in reversed(writes):
        if write.get("phase") == "restored" or not _proposed_matches(vault, write):
            if not _pre_image_matches(vault, write):
                raise PublicationConflict(
                    f"Later change blocks rollback of '{write['relative_path']}'"
                )
            write["phase"] = "restored"
            _save_journal(_journal_path(workspace, publication_id), journal)
            continue
        _restore_write(vault, workspace, publication_id, write)
        write["phase"] = "restored"
        restored.append(write["relative_path"])
        _save_journal(_journal_path(workspace, publication_id), journal)

    _remove_empty_created_dirs(vault, journal.get("created_directories") or [])
    journal["status"] = "rolled_back"
    _save_journal(_journal_path(workspace, publication_id), journal)
    return RollbackReceipt(
        publication_id=publication_id,
        status="rolled_back",
        restored_paths=list(reversed(restored)),
    )


def apply_publication(
    patches: Iterable[NotePatch | dict[str, Any]],
    vault: Path | str,
    workspace: Path | str,
    *,
    interrupt_after: int | None = None,
) -> PublicationReceipt:
    """Publish planned notes one file at a time.

    Each replacement is an atomic rename of that file only. Several files are not one
    vault-wide transaction. A crash leaves a journal; call ``recover_publication``.
    ``interrupt_after`` is a crash seam for tests and must not be used in production.
    """
    if interrupt_after is not None and interrupt_after < 0:
        raise PublicationRejected("interrupt_after cannot be negative")

    vault_path, workspace_path = _workspace_roots(vault, workspace)
    coerced = [_coerce_patch(item) for item in patches]
    _acquire_lock(workspace_path, "pending")
    try:
        active = _in_progress_journals(workspace_path)
        if active:
            raise PublicationRejected(
                "An unfinished publication journal exists; recover it before applying another"
            )
        already = _find_already_committed(workspace_path, vault_path, coerced)
        if already is not None:
            if already.get("vault") != str(vault_path):
                raise PublicationRejected("Committed journal vault does not match the requested vault")
            return _receipt_from_journal(already, "already_committed")

        plan = plan_publication(coerced, vault_path)
        publication_id = plan.publication_id
        pub_dir = _publication_dir(workspace_path, publication_id)
        journal_file = pub_dir / _JOURNAL_NAME
        if journal_file.exists():
            existing = _load_journal(journal_file)
            if existing.get("status") == "committed":
                if all(_proposed_matches(vault_path, write) for write in existing["writes"]):
                    return _receipt_from_journal(existing, "already_committed")
                raise PublicationConflict(
                    f"Committed publication '{publication_id}' no longer matches the vault"
                )
            if existing.get("status") != "rolled_back":
                raise PublicationRejected(
                    f"Publication '{publication_id}' is {existing.get('status')}; recover it before retrying"
                )
        elif pub_dir.exists():
            for child in pub_dir.rglob("*"):
                if child.is_file():
                    child.unlink()

        staged: list[tuple[PlannedWrite, bytes, list[str]]] = []
        created_directories: list[str] = []
        for patch, write in zip(coerced, plan.writes, strict=True):
            payload = patch.proposed_content.encode("utf-8")
            if _sha256_bytes(payload) != write.proposed_hash:
                raise PublicationRejected(f"Proposed bytes do not match the plan for '{write.relative_path}'")
            new_dirs = _created_directories(vault_path, write.relative_path)
            for directory in new_dirs:
                if directory not in created_directories:
                    created_directories.append(directory)
            staged.append((write, payload, new_dirs))

        pub_dir.mkdir(parents=True, exist_ok=True)
        for write, payload, _dirs in staged:
            _atomic_write(pub_dir / "staging" / write.relative_path, payload)
            if write.action == "replace":
                original = (vault_path / write.relative_path).read_bytes()
                if _sha256_bytes(original) != write.base_hash:
                    raise PublicationConflict(f"Base hash changed for '{write.relative_path}'")
                _atomic_write(pub_dir / "backup" / write.relative_path, original)

        journal: dict[str, Any] = {
            "schema_version": 1,
            "publication_id": publication_id,
            "vault": str(vault_path),
            "status": "applying",
            "created_directories": created_directories,
            "writes": [
                {
                    "relative_path": write.relative_path,
                    "note_id": write.note_id,
                    "action": write.action,
                    "base_hash": write.base_hash,
                    "proposed_hash": write.proposed_hash,
                    "phase": "pending",
                }
                for write, _payload, _dirs in staged
            ],
        }
        _save_journal(journal_file, journal)
        if interrupt_after == 0:
            raise PublicationInterrupted(publication_id, 0)

        for index, (write, payload, _dirs) in enumerate(staged):
            dest = vault_path / write.relative_path
            if _is_symlink_or_junction(dest) or any(
                _is_symlink_or_junction(vault_path / "/".join(write.relative_path.split("/")[:i]))
                for i in range(1, len(write.relative_path.split("/")))
            ):
                raise PublicationRejected(f"Path or parent is a symlink: '{write.relative_path}'")
            current = _file_hash_or_none(dest)
            if write.action == "create" and current is not None:
                raise PublicationConflict(f"Create target appeared before write: '{write.relative_path}'")
            if write.action == "replace" and current != write.base_hash:
                raise PublicationConflict(f"Base hash changed before write: '{write.relative_path}'")
            _atomic_write(dest, payload)
            if _sha256_file(dest) != write.proposed_hash:
                raise PublicationConflict(f"Written hash mismatch for '{write.relative_path}'")
            journal["writes"][index]["phase"] = "applied"
            _save_journal(journal_file, journal)
            if interrupt_after is not None and index + 1 == interrupt_after:
                raise PublicationInterrupted(publication_id, index + 1)

        journal["status"] = "committed"
        _save_journal(journal_file, journal)
        return _receipt_from_journal(journal, "committed")
    finally:
        _release_lock(workspace_path)


def rollback_publication(
    publication_id: str,
    vault: Path | str,
    workspace: Path | str,
) -> RollbackReceipt:
    """Restore one committed publication. A later manual edit is a conflict, not an overwrite."""
    vault_path, workspace_path = _workspace_roots(vault, workspace)
    journal_file = _journal_path(workspace_path, publication_id)
    if not journal_file.is_file():
        raise PublicationRejected(f"No journal for publication '{publication_id}'")
    _acquire_lock(workspace_path, publication_id)
    try:
        journal = _load_journal(journal_file)
        if journal.get("publication_id") != publication_id:
            raise PublicationRejected("Journal publication_id does not match the path")
        if journal.get("status") in _IN_PROGRESS:
            raise PublicationRejected("Unfinished publication must be recovered, not rolled back as committed")
        return _rollback_journal(vault_path, workspace_path, journal)
    finally:
        _release_lock(workspace_path)


def recover_publication(
    vault: Path | str,
    workspace: Path | str,
    publication_id: str | None = None,
) -> RollbackReceipt:
    """Roll back a publication interrupted before commit. Does not finish the remaining writes."""
    vault_path, workspace_path = _workspace_roots(vault, workspace)
    lock = _lock_path(workspace_path)
    if lock.exists():
        try:
            owner = json.loads(lock.read_text(encoding="utf-8"))
            pid = int(owner.get("pid", -1))
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError):
            pid = -1
        if _pid_alive(pid):
            raise PublicationRejected("Publication lock is held by a live process")
        lock.unlink()

    if publication_id is None:
        active = _in_progress_journals(workspace_path)
        if len(active) != 1:
            raise PublicationRejected("Expected exactly one unfinished publication to recover")
        publication_id = str(active[0]["publication_id"])

    journal_file = _journal_path(workspace_path, publication_id)
    if not journal_file.is_file():
        raise PublicationRejected(f"No journal for publication '{publication_id}'")
    _acquire_lock(workspace_path, publication_id)
    try:
        journal = _load_journal(journal_file)
        if journal.get("status") == "committed":
            raise PublicationRejected("Committed publication requires rollback, not recovery")
        return _rollback_journal(vault_path, workspace_path, journal)
    finally:
        _release_lock(workspace_path)
