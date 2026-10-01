"""Live adapters for the four-stage pipeline. Credentials stay in the environment."""

from __future__ import annotations

import base64
import json
import os
import urllib.request
from typing import Any, Callable
from urllib.parse import urlparse

from .assemble import ALLOWED_IMAGE_HOSTS
from .assemble import AssembledPost
from .clm_client import model_name, require_ready, system_one
from .decisions import (
    parse_json_object,
    resolve_extraction_model,
    summary_messages,
)
from .local_gate import category_from_clm, category_question, filter_questions
from .jev_provider import evaluate_jev
from .schemas import ContextBundle

MAX_IMAGE_BYTES = 8_000_000


class _AllowlistedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlparse(newurl).hostname not in ALLOWED_IMAGE_HOSTS:
            raise ValueError("przekierowanie obrazu wyszło poza dozwolone hosty")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_image(url: str, *, timeout: float = 20) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_IMAGE_HOSTS:
        raise ValueError("adres obrazu jest spoza dozwolonych hostów")
    opener = urllib.request.build_opener(_AllowlistedRedirect)
    request = urllib.request.Request(url, headers={"User-Agent": "kb-pipeline-ocr"})
    with opener.open(request, timeout=timeout) as response:
        data = response.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("obraz przekracza limit rozmiaru")
    return data


def _chat_content(base_url: str, api_key: str, model: str, messages: list[dict], *, timeout: float) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key or "not-needed", base_url=base_url, timeout=timeout)
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=messages,
        )
    except Exception:
        response = client.chat.completions.create(model=model, temperature=0, messages=messages)
    content = response.choices[0].message.content
    if not isinstance(content, str) or not content.strip():
        raise ValueError("pustą odpowiedź modelu")
    return content


def make_local_filter(base_url: str, api_key: str, model: str) -> Callable[[AssembledPost], dict]:
    def _filter(assembled: AssembledPost) -> dict:
        return system_one(assembled.focus_evidence, filter_questions(), model=model)
    return _filter


def make_categorizer(base_url: str, api_key: str, model: str) -> Callable[[AssembledPost], dict]:
    def _category(assembled: AssembledPost) -> dict:
        response = system_one(assembled.focus_evidence, category_question(), model=model)
        return {"category": category_from_clm(response)}
    return _category


def make_summarizer(base_url: str, api_key: str, model: str) -> Callable[[str, str], dict]:
    resolved = resolve_extraction_model(model)

    def _summary(document: str, category: str) -> dict:
        return parse_json_object(
            _chat_content(base_url, api_key, resolved, summary_messages(document, category), timeout=120)
        )
    return _summary


def make_ocr(base_url: str, api_key: str, model: str, download: Callable[[str], bytes] = download_image) -> Callable[[str], str | None]:
    from openai import OpenAI

    client = OpenAI(api_key=api_key or "not-needed", base_url=base_url, timeout=90)

    def _ocr(url: str) -> str | None:
        image = base64.b64encode(download(url)).decode("ascii")
        response = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Odczytaj widoczny tekst. Zwróć tylko tekst, bez komentarza. Gdy tekstu nie ma, zwróć pustą odpowiedź."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}},
                ],
            }],
        )
        content = response.choices[0].message.content
        return content.strip() if isinstance(content, str) else None
    return _ocr


def make_jev(model: str = "jev-latest") -> Callable[[ContextBundle], dict]:
    def _evaluate(bundle: ContextBundle) -> dict:
        return evaluate_jev(bundle, model=model)
    return _evaluate


def require_runtime_config() -> dict[str, str]:
    require_ready()
    local_model = model_name()
    ocr_model = os.getenv("LOCAL_OCR_MODEL", "").strip()
    extraction_model = resolve_extraction_model(os.getenv("EXTRACTION_MODEL"))
    extraction_base = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    extraction_key = os.getenv("OPENAI_API_KEY", "").strip()
    missing = []
    if not extraction_key:
        missing.append("OPENAI_API_KEY")
    if not os.getenv("TYPESAFE_API_KEY", "").strip():
        missing.append("TYPESAFE_API_KEY")
    if missing:
        raise RuntimeError("Brak konfiguracji: " + ", ".join(missing))
    return {
        "local_base": os.getenv("CLM_BASE_URL", "http://127.0.0.1:8700").rstrip("/"),
        "local_model": local_model,
        "local_key": os.getenv("CLM_API_KEY", ""),
        "ocr_model": ocr_model,
        "ocr_base": os.getenv("LOCAL_OCR_BASE_URL", "").rstrip("/"),
        "ocr_key": os.getenv("LOCAL_OCR_API_KEY", "not-needed"),
        "extraction_model": extraction_model,
        "extraction_base": extraction_base,
        "extraction_key": extraction_key,
        "jev_model": os.getenv("JEV_MODEL", "jev-latest"),
    }


def configured_handles() -> list[str]:
    raw = os.getenv("TWITTER_HANDLES") or os.getenv("TWITTER_HANDLE") or ""
    handles = [part.strip().lstrip("@") for part in raw.split(",") if part.strip()]
    return handles or [
        "kunchenguid", "karminski3", "simonw", "HamelHusain", "teortaxesTex", "DrJimFan", "JustinLin610",
    ]
