"""Content fingerprints for cache dependencies.

A stage cache key has to reflect what the raw answer actually depended on: the
stage, the source input, the context, the model, the prompt version, the schema
version and — for every stage that reads the vault or the retrieval index — the
**content** of what it read. A vault directory name is not a dependency. Two
different vaults, or the same vault after an edit, used to share a manifest
field, so a changed note could not invalidate anything.

``vault_fingerprint`` hashes the relative path and the bytes of the files the
indexer and the publisher read. A changed note changes the fingerprint, so
dependent local stages are recomputed, while a stage that never read the vault
keeps its own cache entry and replays without a new provider call.

Read-only: this module opens vault files for reading and writes nothing into
the vault.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .retrieval import CANONICAL_DIRS, SOURCE_DIRS

# The publisher allowlist plus the evidence layer the indexer also reads.
FINGERPRINT_DIRS = tuple(CANONICAL_DIRS) + tuple(SOURCE_DIRS)


def _note_files(vault: Path) -> list[Path]:
    """Every indexable note under the vault, symlinks excluded (as in retrieval)."""
    found: list[Path] = []
    for name in FINGERPRINT_DIRS:
        directory = vault / name
        if not directory.is_dir() or directory.is_symlink():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.is_symlink() or not path.is_file():
                continue
            # Mirror retrieval: a note reached through a symlinked parent is skipped.
            if any(parent.is_symlink() for parent in path.parents if parent != vault):
                continue
            found.append(path)
    return sorted(found, key=lambda item: item.relative_to(vault).as_posix())


def vault_fingerprint(vault: Path) -> tuple[str, dict[str, str]]:
    """SHA-256 over the vault's note paths and bytes, plus the per-file digests.

    Returns the fingerprint and the file digest map. The digest map is what
    ``RunManifest.input_hashes`` and the integration checkpoint reference, so a
    single edited note is visible instead of being averaged away.
    """
    vault_path = Path(vault).resolve(strict=True)
    digests: dict[str, str] = {}
    for path in _note_files(vault_path):
        relative = path.relative_to(vault_path).as_posix()
        digests[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    payload = json.dumps(digests, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest(), digests


def index_fingerprint(vault_digest: str, indexed_sections: int) -> str:
    """Fingerprint of the retrieval index derived from a vault fingerprint.

    Binding the index to the vault content it was built from means a changed
    note invalidates the stages that read candidates, and an unchanged vault
    does not.
    """
    payload = json.dumps(
        {"vault": vault_digest, "sections": int(indexed_sections)},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def notes_digest(note_hashes: Mapping[str, str]) -> str:
    """Fingerprint of the managed notes a stage actually read."""
    payload = json.dumps(
        {str(key): str(value) for key, value in sorted(note_hashes.items())},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def extend_hash(base: str, extra: Mapping[str, Any]) -> str:
    """Extend a hash with additional dependencies, keeping it deterministic."""
    payload = json.dumps(
        {"base": base, "extra": dict(extra)},
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
