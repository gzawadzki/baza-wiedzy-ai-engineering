"""Live Jev evaluation and filtering for imported source records."""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .context import build_context
from .filtering import assess_filter
from .jev_provider import JevError, evaluate_jev
from .pilot import _is_within, _safe_paths
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


def compute_input_hash(source_id: str, content_hash: str) -> str:
    """Compute a deterministic hash combining source identity and content hash."""
    payload = {"source_id": source_id, "content_hash": content_hash}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compute_policy_version_key(
    question_version: str,
    policy_version: str,
    usefulness_threshold: float,
    context_threshold: float,
) -> str:
    """Compute a deterministic key combining question version, policy version, and thresholds."""
    payload = {
        "question_version": question_version,
        "policy_version": policy_version,
        "usefulness_threshold": round(float(usefulness_threshold), 4),
        "context_threshold": round(float(context_threshold), 4),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _clean_token(val: str) -> str:
    """Sanitize identifiers for safe filenames."""
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in val)


def _validate_safe_artifact_target(target_path: Path, vault_path: Path) -> None:
    """Ensure that the artifact target path does not resolve inside the vault or traverse symlinks into it."""
    vault_entry = Path(os.path.abspath(vault_path))
    resolved_vault = vault_path.resolve(strict=True)

    check_node: Path | None = target_path
    while check_node is not None and check_node != check_node.parent:
        if check_node.is_symlink():
            link_target = Path(os.path.abspath(check_node.resolve(strict=False)))
            if _is_within(link_target, vault_entry) or _is_within(link_target, resolved_vault):
                raise ValueError(
                    f"Artifact path '{target_path}' traverses a symlink pointing inside the vault: '{link_target}'"
                )
        check_node = check_node.parent

    resolved_target = target_path.resolve(strict=False)
    target_entry = Path(os.path.abspath(resolved_target))
    if _is_within(target_entry, vault_entry) or _is_within(resolved_target, resolved_vault):
        raise ValueError(
            f"Artifact destination '{target_path}' resolves inside the vault: '{resolved_target}'"
        )


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

    # Validate that workspace artifacts directory does not point into the vault
    artifact_dir = workspace_path / "artifacts"
    _validate_safe_artifact_target(artifact_dir, vault_path)

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

    input_hash = compute_input_hash(record.source_id, source_hash)
    policy_key = compute_policy_version_key(
        question_version, policy_version, usefulness_threshold, context_threshold
    )
    cache_key = StageCache.key("filter", input_hash, context_hash, model, policy_key, schema_version=1)

    with StageCache(workspace_path) as cache:
        if not refresh:
            cached = cache.get(cache_key)
            if (
                cached is not None
                and cached.get("source_id") == record.source_id
                and cached.get("source_hash") == source_hash
                and cached.get("context_hash") == context_hash
                and cached.get("model") == model
                and cached.get("question_version") == question_version
                and cached.get("policy_version") == policy_version
                and cached.get("usefulness_threshold") == usefulness_threshold
                and cached.get("context_threshold") == context_threshold
            ):
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
                    "artifact_ref": cached.get("raw_response_ref"),
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

        # Construct immutable artifact filename incorporating source_id, hashes, model, and policy
        source_id_clean = _clean_token(record.source_id)
        model_clean = _clean_token(model)
        policy_clean = _clean_token(policy_version)
        base_filename = (
            f"filter_{source_id_clean}_{source_hash[:10]}_{context_hash[:10]}_{model_clean}_{policy_clean}"
        )
        artifact_filename = f"{base_filename}.json"
        artifact_path = artifact_dir / artifact_filename

        if artifact_path.exists() or artifact_path.is_symlink():
            counter = 1
            while True:
                candidate = f"{base_filename}_rev{counter}.json"
                cand_path = artifact_dir / candidate
                if not cand_path.exists() and not cand_path.is_symlink():
                    artifact_filename = candidate
                    artifact_path = cand_path
                    break
                counter += 1

        _validate_safe_artifact_target(artifact_path, vault_path)
        artifact_rel_ref = f"artifacts/{artifact_filename}"

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
            "usefulness_threshold": usefulness_threshold,
            "context_threshold": context_threshold,
            "answers": sanitized_answers,
            "assessment": assessment.model_dump(mode="json"),
            "usage": sanitized_usage,
            "raw_response_ref": artifact_rel_ref,
        }

        _write_json(artifact_path, artifact_data)
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
