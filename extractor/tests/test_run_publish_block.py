"""Regression: `run --publish` must refuse before any provider call or vault write.

Reproduces the audited defect: the `run` command wrote rendered notes straight
into ``vault/Źródła/<handle>/Wpisy`` via ``notes.write_staging``, bypassing
``publication.apply_publication`` and therefore bypassing allowlist, journal,
backup and rollback.

These tests drive the real CLI in a subprocess. No network, no secrets.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

EXTRACTOR = Path(__file__).resolve().parents[1]

HANDLES = {"A": "1", "B": "2"}


def _vault_hashes(vault: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(vault.rglob("*")):
        if path.is_file():
            out[str(path.relative_to(vault))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def _build_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    (vault / "Pojęcia").mkdir(parents=True)
    (vault / "Pojęcia" / "Harness.md").write_text("# Harness\n\nNotatka testowa.\n", encoding="utf-8")
    (vault / "Źródła").mkdir(parents=True)
    return vault


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(EXTRACTOR)
    # Belt and braces: even if a future change re-enabled provider calls, the
    # refusal must not depend on reaching them.
    env["CLM_BASE_URL"] = "http://127.0.0.1:1"
    return subprocess.run(
        [sys.executable, "-m", "kb_pipeline", *args],
        cwd=EXTRACTOR,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_run_publish_refused_with_nonzero_exit(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    before = _vault_hashes(vault)

    result = _run_cli(
        "run",
        "--handles", "someuser",
        "--workspace", str(workspace),
        "--vault", str(vault),
        "--publish",
        "--cache-only",
        "--limit", "1",
    )

    assert result.returncode != 0, f"odmowa musi miec niezerowy kod zakonczenia: {result}"

    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["status"] == "error"
    assert "--publish" in payload["error"]
    assert "journal" in payload["error"]


def test_run_publish_leaves_vault_byte_identical(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    before = _vault_hashes(vault)

    result = _run_cli(
        "run",
        "--handles", "someuser",
        "--workspace", str(workspace),
        "--vault", str(vault),
        "--publish",
        "--cache-only",
        "--limit", "1",
    )
    assert result.returncode != 0

    after = _vault_hashes(vault)
    assert after == before, "odmowa --publish nie moze zmienic ani jednego bajtu w vaulcie"


def test_run_publish_refused_before_any_workspace_artifact(tmp_path: Path):
    """The refusal happens before provider calls, so no staging is produced."""
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"

    result = _run_cli(
        "run",
        "--handles", "someuser",
        "--workspace", str(workspace),
        "--vault", str(vault),
        "--publish",
        "--cache-only",
        "--limit", "1",
    )
    assert result.returncode != 0
    assert not workspace.exists() or not any(workspace.rglob("run-report.json"))


def test_run_without_publish_still_refuses_publish_flag_only_on_flag(tmp_path: Path):
    """Sanity: the gate keys off --publish, and the arg parser still accepts run."""
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"

    result = _run_cli(
        "run",
        "--handles", "someuser",
        "--workspace", str(workspace),
        "--vault", str(vault),
        "--cache-only",
        "--limit", "1",
    )
    # Without --publish the command proceeds past the gate. It may still fail on
    # runtime config (CLM absent), but it must NOT be the --publish refusal.
    if result.returncode != 0:
        stdout = result.stdout.strip()
        assert "--publish jest zablokowane" not in stdout
        assert "--publish jest zablokowane" not in result.stderr


def test_run_accounts_direct_call_refuses_publish_dir(tmp_path: Path):
    """The nearest direct entry must not bypass the refusal."""
    from kb_pipeline.account_run import run_accounts

    try:
        run_accounts(
            handles=["someuser"],
            since=None,
            until=None,
            cache_dir=tmp_path,
            workspace=tmp_path / "workspace",
            publish_dir=tmp_path / "vault" / "Źródła",
        )
    except ValueError as exc:
        assert "--publish" in str(exc) or "publish_dir" in str(exc)
        assert "zablokowane" in str(exc)
    else:
        raise AssertionError("run_accounts z publish_dir musi odmowic")


def test_publish_dir_is_not_written_even_if_flag_were_bypassed(tmp_path: Path):
    """Guard the removed code path: no handle/Wpisy tree may be produced."""
    vault = _build_vault(tmp_path)
    result = _run_cli(
        "run",
        "--handles", "someuser",
        "--workspace", str(tmp_path / "workspace"),
        "--vault", str(vault),
        "--publish",
        "--cache-only",
        "--limit", "1",
    )
    assert result.returncode != 0
    for handle in HANDLES:
        assert not (vault / "Źródła" / handle).exists()