"""Durable run state: descriptor, stage checkpoints, artifact integrity, resume.

A run had to be re-derivable from scratch: an interruption lost the knowledge of
how far it had got, and a lost artifact was indistinguishable from a completed
stage. This module adds the missing state, in the run's own directory, written
atomically after every stage:

``run_descriptor.json``
    What the run was: workspace-relative inputs, sources, provider mode, prompt
    and schema versions, thresholds. ``resume`` needs it to know what to
    continue, and refuses to guess when it is gone.
``checkpoints.json``
    Per source and stage: status, the stage cache key, and the digest of every
    artifact the stage wrote.
``artifacts/raw/<stage>.json``
    The raw provider response of a provider stage, next to its digest. A
    resumed run serves a completed provider stage from here, so it does not
    repeat the call even if the stage cache database is gone.

Integrity is explicit. An artifact that is missing or whose digest no longer
matches is reported as a problem, the stage is recomputed, and the reason is
carried into the run summary. Nothing is silently trusted or silently redone.

Checkpoints never live in the vault, and they are operational state, not
knowledge: no claim, no note, no decision.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from .schemas import SCHEMA_VERSION
from .stage_cache import assert_no_sensitive_fields

CHECKPOINT_VERSION = 1
DESCRIPTOR_VERSION = 1


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes((text + "\n").encode("utf-8"))
    os.replace(temporary, path)


def file_digest(path: Path) -> str | None:
    """SHA-256 of a file, or ``None`` when it is not there."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


@dataclass
class RunState:
    """Checkpoints and descriptor for one ``run_id`` inside a workspace."""

    workspace: Path
    run_id: str
    _checkpoints: dict[str, dict[str, Any]] = field(default_factory=dict, init=False)
    _problems: list[dict[str, Any]] = field(default_factory=list, init=False)
    _loaded: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.workspace = Path(self.workspace).resolve()
        self.run_dir = self.workspace / "runs" / self.run_id
        self.artifact_dir = self.run_dir / "artifacts"
        self.raw_dir = self.artifact_dir / "raw"
        self.descriptor_path = self.run_dir / "run_descriptor.json"
        self.checkpoints_path = self.run_dir / "checkpoints.json"
        self._load()

    # ------------------------------------------------------------- sources --
    @staticmethod
    def source_slug(source_id: str) -> str:
        """Filesystem-safe name of one source, for logs and reports only.

        A run belongs to exactly one source: ``offline_cli`` derives a distinct
        ``run_id`` and therefore a distinct ``run_dir`` per source, so a batch
        never lets two sources share an artifact or a digest.
        """
        cleaned = re.sub(r"[^A-Za-z0-9_-]", "_", source_id)[:48]
        return f"{cleaned}-{hashlib.sha256(source_id.encode('utf-8')).hexdigest()[:8]}"

    def source_dir(self, source_id: str) -> Path:
        """The directory a source's artifacts live in: its own run directory."""
        return self.run_dir

    # ------------------------------------------------------------------ io --
    def _load(self) -> None:
        if self.checkpoints_path.is_file():
            try:
                loaded = json.loads(self.checkpoints_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                loaded = None
            if isinstance(loaded, dict) and isinstance(loaded.get("sources"), dict):
                self._checkpoints = loaded["sources"]
        self._loaded = True

    def _flush(self) -> None:
        _write_json_atomic(
            self.checkpoints_path,
            {
                "version": CHECKPOINT_VERSION,
                "run_id": self.run_id,
                "updated_at": _now(),
                "sources": self._checkpoints,
                "note": (
                    "Operational state only: which stages finished, with which cache key, "
                    "and the digest of each artifact they wrote."
                ),
            },
        )

    # ---------------------------------------------------------- descriptor --
    def write_descriptor(self, descriptor: Mapping[str, Any]) -> dict[str, Any]:
        existing = self.load_descriptor()
        payload = {
            "version": DESCRIPTOR_VERSION,
            "run_id": self.run_id,
            "schema_version": SCHEMA_VERSION,
            **dict(descriptor),
        }
        if existing is not None:
            comparable = {key: value for key, value in existing.items() if key != "written_at"}
            if comparable == payload:
                # An identical run keeps its descriptor byte for byte.
                return existing
        payload = {"written_at": _now(), **payload}
        _write_json_atomic(self.descriptor_path, payload)
        return payload

    def load_descriptor(self) -> dict[str, Any] | None:
        if not self.descriptor_path.is_file():
            return None
        try:
            loaded = json.loads(self.descriptor_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        return loaded if isinstance(loaded, dict) else None

    # ---------------------------------------------------------- checkpoints --
    def checkpoint(self, source_id: str, stage: str) -> dict[str, Any] | None:
        return self._checkpoints.get(source_id, {}).get(stage)

    def stages(self, source_id: str) -> dict[str, Any]:
        return dict(self._checkpoints.get(source_id, {}))

    def record(
        self,
        *,
        source_id: str,
        stage: str,
        status: str,
        cache_key: str | None = None,
        raw_ref: str | None = None,
        artifacts: Sequence[str] = (),
        detail: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Record one stage outcome together with the digest of what it wrote.

        ``artifacts`` are relative to the source's own directory; ``raw_ref`` is
        relative to the run directory, because a resumed run reads it by path.
        """
        digests = {
            ref: file_digest(self.source_dir(source_id) / ref) for ref in artifacts if ref
        }
        entry: dict[str, Any] = {
            "stage": stage,
            "status": status,
            "recorded_at": _now(),
            "cache_key": cache_key,
            "raw_ref": raw_ref,
            "raw_digest": file_digest(self.run_dir / raw_ref) if raw_ref else None,
            "artifacts": sorted(digests),
            "artifact_digests": digests,
            "detail": dict(detail or {}),
        }
        self._checkpoints.setdefault(source_id, {})[stage] = entry
        self._flush()
        return entry

    # ------------------------------------------------------------ integrity --
    def verify(self, source_id: str) -> list[dict[str, Any]]:
        """Re-check every recorded artifact of a source. Problems are explicit."""
        problems: list[dict[str, Any]] = []
        for stage, entry in sorted(self._checkpoints.get(source_id, {}).items()):
            for ref, expected in sorted((entry.get("artifact_digests") or {}).items()):
                path = self.source_dir(source_id) / ref
                if not path.is_file():
                    problems.append(
                        {"source_id": source_id, "stage": stage, "artifact": ref, "reason": "missing"}
                    )
                    continue
                actual = file_digest(path)
                if actual != expected:
                    problems.append(
                        {
                            "source_id": source_id,
                            "stage": stage,
                            "artifact": ref,
                            "reason": "digest_mismatch",
                            "expected": expected,
                            "actual": actual,
                        }
                    )
            raw_ref = entry.get("raw_ref")
            if raw_ref and entry.get("raw_digest"):
                path = self.run_dir / raw_ref
                if not path.is_file() or file_digest(path) != entry["raw_digest"]:
                    problems.append(
                        {
                            "source_id": source_id,
                            "stage": stage,
                            "artifact": raw_ref,
                            "reason": "missing" if not path.is_file() else "digest_mismatch",
                        }
                    )
        self._problems.extend(problems)
        return problems

    @property
    def problems(self) -> list[dict[str, Any]]:
        return list(self._problems)

    def invalidate(self, source_id: str, stage: str, reason: str) -> None:
        """Mark a checkpoint unusable so the stage is recomputed, keeping the reason."""
        entry = self._checkpoints.get(source_id, {}).get(stage)
        if entry is None:
            return
        entry["status"] = "invalid"
        entry["invalidated_at"] = _now()
        entry["invalidated_reason"] = reason
        self._flush()

    # -------------------------------------------------------- raw responses --
    def raw_path(self, source_id: str, stage: str) -> Path:
        return self.raw_dir / f"{stage}.json"

    def raw_ref(self, source_id: str, stage: str) -> str:
        return f"artifacts/raw/{stage}.json"

    def write_raw(self, source_id: str, stage: str, payload: Mapping[str, Any]) -> str:
        # The same credential guard as the stage cache: a live adapter must not be
        # able to write a header or a key into the run's artifacts.
        assert_no_sensitive_fields(dict(payload))
        _write_json_atomic(self.raw_path(source_id, stage), dict(payload))
        return self.raw_ref(source_id, stage)

    def read_raw(self, source_id: str, stage: str, cache_key: str) -> dict[str, Any] | None:
        """Recover a completed provider stage from its own artifact.

        Returns the stored value only when the checkpoint says the stage is
        finished, the key still matches and the digest still holds. Anything
        else is ``None`` — the caller then recomputes and says so.
        """
        entry = self.checkpoint(source_id, stage)
        if entry is None or entry.get("status") != "completed":
            return None
        if entry.get("cache_key") != cache_key:
            return None
        raw_ref = entry.get("raw_ref")
        if not raw_ref:
            return None
        path = self.run_dir / raw_ref
        if not path.is_file():
            self.invalidate(source_id, stage, "raw_artifact_missing")
            return None
        expected = entry.get("raw_digest")
        if expected and file_digest(path) != expected:
            self.invalidate(source_id, stage, "raw_artifact_digest_mismatch")
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self.invalidate(source_id, stage, "raw_artifact_unreadable")
            return None
        if not isinstance(payload, dict) or "value" not in payload:
            self.invalidate(source_id, stage, "raw_artifact_incomplete")
            return None
        return payload

    # --------------------------------------------------------------- report --
    def stage_status(self, source_id: str, stage: str) -> str | None:
        entry = self.checkpoint(source_id, stage)
        return None if entry is None else str(entry.get("status"))

    def completed_stages(self, source_id: str) -> list[str]:
        return [
            stage
            for stage, entry in sorted(self._checkpoints.get(source_id, {}).items())
            if entry.get("status") == "completed"
        ]

    def report(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "run_dir": str(self.run_dir),
            "descriptor_present": self.descriptor_path.is_file(),
            "sources": {
                source_id: {
                    stage: {
                        "status": entry.get("status"),
                        "cache_key": entry.get("cache_key"),
                        "invalidated_reason": entry.get("invalidated_reason"),
                    }
                    for stage, entry in sorted(stages.items())
                }
                for source_id, stages in sorted(self._checkpoints.items())
            },
            "problems": self._problems,
        }
