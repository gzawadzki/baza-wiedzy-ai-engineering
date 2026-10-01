"""Local CLM System One client. The embedder stays behind clm-serve."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

DEFAULT_BASE_URL = "http://127.0.0.1:8700"
DEFAULT_MODEL = "clm-latest"


class ClmError(RuntimeError):
    pass


def base_url() -> str:
    return os.getenv("CLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def model_name() -> str:
    return os.getenv("CLM_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def _request(path: str, payload: dict | None = None, *, timeout: float = 25) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    key = os.getenv("CLM_API_KEY", "").strip()
    if key:
        headers["Authorization"] = f"Bearer {key}"
    request = urllib.request.Request(base_url() + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise ClmError(f"CLM {path} HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ClmError(f"CLM {path} niedostępny: {exc}") from exc
    if not isinstance(body, dict):
        raise ClmError(f"CLM {path} nie zwrócił obiektu")
    return body


def require_ready() -> dict[str, Any]:
    """Fail before a run if clm-serve cannot see the Qwen embedder."""
    health = _request("/health", timeout=10)
    if health.get("ok") is not True:
        raise ClmError(f"CLM nie jest gotowy: {health}")
    if health.get("embedder") is not True:
        raise ClmError("CLM nie widzi embeddera na http://127.0.0.1:8090")
    if model_name() not in set(health.get("models") or []):
        raise ClmError(f"CLM nie serwuje modelu {model_name()}")
    return health


def system_one(state: Any, questions: dict[str, dict], *, model: str | None = None) -> dict:
    return _request("/v1/systemone", {
        "state": state,
        "model": model or model_name(),
        "questions": questions,
    })
