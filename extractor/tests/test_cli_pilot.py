from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

EXTRACTOR = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "pilot_context.json"


def _hash_tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _run(vault: Path, workspace: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "kb_pipeline",
            "pilot-dry-run",
            "--vault",
            str(vault),
            "--workspace",
            str(workspace),
            "--fixture",
            str(FIXTURE),
        ],
        cwd=EXTRACTOR,
        capture_output=True,
        text=True,
        check=False,
    )


def test_pilot_dry_run_cli_writes_repeatable_artifacts_without_vault_changes(tmp_path):
    vault = tmp_path / "vault"
    notes = vault / "Pojęcia"
    notes.mkdir(parents=True)
    (notes / "Context compaction.md").write_text(
        "# Context compaction\n\nA synthetic candidate note for the offline search.\n",
        encoding="utf-8",
    )
    (vault / ".obsidian").mkdir()
    (vault / ".obsidian" / "app.json").write_text('{"fixture": true}\n', encoding="utf-8")
    workspace = tmp_path / "workspace"
    before = _hash_tree(vault)

    first = _run(vault, workspace)

    assert first.returncode == 0, first.stderr
    first_summary = json.loads(first.stdout)
    assert first_summary["status"] == "completed"
    assert first_summary["proposed_claim_ids"] == ["synthetic-compaction-claim"]
    proposal = Path(first_summary["proposal_path"])
    assert proposal.is_file()
    assert not proposal.resolve().is_relative_to(vault.resolve())
    proposal_bytes = proposal.read_bytes()
    run_id = first_summary["run_id"]

    second = _run(vault, workspace)

    assert second.returncode == 0, second.stderr
    second_summary = json.loads(second.stdout)
    assert second_summary["run_id"] == run_id
    assert second_summary["proposal_path"] == first_summary["proposal_path"]
    assert proposal.read_bytes() == proposal_bytes
    assert [path.name for path in workspace.iterdir() if path.is_dir()] == [run_id]
    assert _hash_tree(vault) == before
