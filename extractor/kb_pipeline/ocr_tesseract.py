"""Local Tesseract OCR. The embedder does not see images."""

from __future__ import annotations

import io
import os
import subprocess
from pathlib import Path

from .live_adapters import download_image

_DEFAULT_BIN = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
_DEFAULT_DATA = Path(r"D:\projects\kb-clm-screen\tessdata")


def tesseract_bin() -> Path:
    configured = os.getenv("TESSERACT_CMD", "").strip()
    if configured:
        return Path(configured)
    if _DEFAULT_BIN.exists():
        return _DEFAULT_BIN
    return Path("tesseract")


def tessdata_dir() -> Path | None:
    configured = os.getenv("TESSDATA_PREFIX", "").strip()
    if configured:
        path = Path(configured)
        return path if (path / "eng.traineddata").exists() else path.parent
    if (_DEFAULT_DATA / "eng.traineddata").exists():
        return _DEFAULT_DATA
    install = _DEFAULT_BIN.parent / "tessdata"
    return install if install.exists() else None


def ocr_bytes(data: bytes, *, timeout: float = 30) -> str:
    from PIL import Image

    image = Image.open(io.BytesIO(data))
    image.seek(0)
    if image.mode not in {"RGB", "L"}:
        image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    command = [str(tesseract_bin()), "stdin", "stdout", "-l", _languages(), "--psm", "3", "--oem", "1"]
    data_dir = tessdata_dir()
    if data_dir is not None:
        command.extend(["--tessdata-dir", str(data_dir)])
    completed = subprocess.run(
        command,
        input=buffer.getvalue(),
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or f"tesseract zakończył się kodem {completed.returncode}")
    return completed.stdout.decode("utf-8", errors="replace").strip()


def ocr_url(url: str) -> str | None:
    text = ocr_bytes(download_image(url, timeout=12), timeout=12)
    return text or None


def _languages() -> str:
    data_dir = tessdata_dir()
    wanted = ["eng", "chi_sim", "pol"]
    if data_dir is None:
        return "eng"
    present = [lang for lang in wanted if (data_dir / f"{lang}.traineddata").exists()]
    return "+".join(present or ["eng"])
