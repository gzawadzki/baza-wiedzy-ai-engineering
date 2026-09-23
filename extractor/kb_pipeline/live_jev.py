"""Live Jev evaluation and filtering for imported source records."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .context import build_context
from .filtering import assess_filter
from .jev_provider import JevError, evaluate_jev
from .pilot import _safe_paths
from .schemas import ContextBundle, SourceRecord
from .stage_cache import StageCache
from .storage import SourceStore


def compute_context_hash(bundle: ContextBundle) -> str:
    """Compute a deterministic SHA-256 hash for related context and missing IDs."""
    data = {
        "related": [
            {
                "source_id": item.source.source_id,
                "content_hash": item.source.content_hash,
                "role": item.role,
                "provenance": item.provenance,
            }
            for item in bundle.related
        ],
        "missing_ids": sorted(bundle.missing_ids),
        "context_status": bundle.context_status.value,
    }
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sanitize_usage(usage: Any) -> dict[str, int]:
    """Extract safe token counts without persisting sensitive keys."""
    if not isinstance(usage, dict):
        return {}
    sanitized: dict[str, int] = {}
    for key in ("input_tokens", "output_tokens"):
        val = usage.get(key)
        if type(val) is int and val >= 0:
            sanitized[key] = val
    return sanitized


def _write_json(path: Path, value: Any) -> None:
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((payload + "\n").encode("utf-8"))


def evaluate_live_source(
    vault: Path,
    workspace: Path,
    source_id: str,
    *,
    content_hash: str | None = None,
    refresh: bool = False,
    model: str = "jev-latest",
    question_version: str = "v1",
    policy_version: str = "v1",
    api_key: str | None = None,
    transport: Callable | None = None,
    usefulness_threshold: float = 0.7,
    context_threshold: float = 0.6,
) -> dict[str, Any]:
    """Evaluate an imported source with TypeSafe Jev and return a summary."""
    if not isinstance(source_id, str) or not source_id.startswith("x:") or not source_id[2:].isdigit():
        raise ValueError(f"Invalid X source ID: '{source_id}'; expected format x:<numeric_id>")

    if content_hash is not None:
        if (
            not isinstance(content_hash, str)
            or len(content_hash) != 64
            or not all(c in "0123456789abcdefABCDEF" for c in content_hash)
        ):
            raise ValueError(f"Invalid content hash: '{content_hash}'; expected 64-character hex string")
        content_hash = content_hash.lower()

    vault_path, workspace_path = _safe_paths(Path(vault), Path(workspace))

    with SourceStore(workspace_path) as store:
        if content_hash is not None:
            record = store.get(source_id, content_hash)
            if record is None:
                raise ValueError(
                    f"Source '{source_id}' with content hash '{content_hash}' not found in store"
                )
        else:
            revisions = store.get_revisions(source_id)
            if not revisions:
                raise ValueError(f"Source '{source_id}' not found in store")
            if len(revisions) > 1:
                raise ValueError(
                    f"Source '{source_id}' has multiple revisions ({', '.join(revisions)}); specify --content-hash"
                )
            record = store.get(source_id, revisions[0])
            if record is None:
                raise ValueError(f"Source '{source_id}' could not be loaded from store")

        def deterministic_lookup(rel_id: str) -> SourceRecord | None:
            return store.get_deterministic(rel_id)

        bundle = build_context(record, deterministic_lookup)

    source_hash = record.content_hash
    context_hash = compute_context_hash(bundle)
    cache_key = StageCache.key("filter", source_hash, context_hash, model, question_version, schema_version=1)

    artifact_dir = workspace_path / "artifacts"
    artifact_filename = f"filter_{record.source_id.replace(':', '_')}_{source_hash[:16]}.json"
    artifact_rel_ref = f"artifacts/{artifact_filename}"

    with StageCache(workspace_path) as cache:
        if not refresh:
            cached = cache.get(cache_key)
            if cached is not None:
                assessment_data = cached.get("assessment", {})
                return {
                    "status": "completed",
                    "source_id": record.source_id,
                    "content_hash": source_hash,
                    "source_hash": source_hash,
                    "context_hash": context_hash,
                    "context_status": bundle.context_status.value,
                    "decision": assessment_data.get("decision"),
                    "reason_code": assessment_data.get("reason_code"),
                    "engineering_score": assessment_data.get("engineering_score"),
                    "topic": assessment_data.get("topic"),
                    "probabilities": assessment_data.get("probabilities", {}),
                    "model": cached.get("model", model),
                    "question_version": cached.get("question_version", question_version),
                    "policy_version": cached.get("policy_version", policy_version),
                    "usage": cached.get("usage", {}),
                    "cached": True,
                    "artifact_ref": cached.get("raw_response_ref") or artifact_rel_ref,
                }

        raw_response = evaluate_jev(
            bundle,
            api_key=api_key,
            model=model,
            transport=transport,
        )

        sanitized_usage = _sanitize_usage(raw_response.get("usage"))
        sanitized_answers = {
            "engineering_value": raw_response["answers"]["engineering_value"],
            "context_sufficient": raw_response["answers"]["context_sufficient"],
            "topic": raw_response["answers"]["topic"],
        }

        assessment = assess_filter(
            bundle,
            raw_response,
            usefulness_threshold=usefulness_threshold,
            context_threshold=context_threshold,
            question_version=question_version,
            policy_version=policy_version,
            raw_response_ref=artifact_rel_ref,
        )

        artifact_data = {
            "source_id": record.source_id,
            "source_hash": source_hash,
            "context_hash": context_hash,
            "model": model,
            "question_version": question_version,
            "policy_version": policy_version,
            "answers": sanitized_answers,
            "assessment": assessment.model_dump(mode="json"),
            "usage": sanitized_usage,
            "raw_response_ref": artifact_rel_ref,
        }

        _write_json(artifact_dir / artifact_filename, artifact_data)
        cache.put(cache_key, artifact_data)

        return {
            "status": "completed",
            "source_id": record.source_id,
            "content_hash": source_hash,
            "source_hash": source_hash,
            "context_hash": context_hash,
            "context_status": bundle.context_status.value,
            "decision": assessment.decision.value,
            "reason_code": assessment.reason_code,
            "engineering_score": assessment.engineering_score,
            "topic": assessment.topic,
            "probabilities": assessment.probabilities,
            "model": model,
            "question_version": question_version,
            "policy_version": policy_version,
            "usage": sanitized_usage,
            "cached": False,
            "artifact_ref": artifact_rel_ref,
        }
