import hashlib
import json
import os
from pathlib import Path

import pytest

from kb_pipeline.publication import (
    PublicationConflict,
    PublicationInterrupted,
    PublicationRejected,
    apply_publication,
    plan_publication,
    recover_publication,
    rollback_publication,
)
from kb_pipeline.schemas import NotePatch

REPO_VAULT = Path(__file__).resolve().parents[2]


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _vault_hashes(vault: Path) -> dict[str, str]:
    return {
        path.relative_to(vault).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in vault.rglob("*")
        if path.is_file()
    }


def _make_vault(root: Path) -> Path:
    vault = root / "vault"
    for name in ("Pojęcia", "Procesy", "Narzędzia", "Zasady"):
        (vault / name).mkdir(parents=True)
    return vault


def _note(note_id: str, claim_id: str, body: str) -> str:
    return (
        "---\n"
        f"note_id: {note_id}\n"
        "kb_managed: true\n"
        "claim_ids:\n"
        f"  - {claim_id}\n"
        "---\n"
        f"{body}\n"
    )


def _patch(note_id: str, relative_path: str, claim_id: str, body: str, base_hash: str | None) -> NotePatch:
    return NotePatch(
        note_id=note_id,
        relative_path=relative_path,
        claim_ids=[claim_id],
        base_hash=base_hash,
        proposed_content=_note(note_id, claim_id, body),
    )


def _assert_not_repo(vault: Path) -> None:
    assert vault.resolve() != REPO_VAULT.resolve()
    assert REPO_VAULT.resolve() not in vault.resolve().parents


def test_apply_writes_only_managed_files_and_keeps_journal_outside_vault(tmp_path):
    vault = _make_vault(tmp_path)
    _assert_not_repo(vault)
    untouched = vault / "Zasady" / "Manual.md"
    untouched.write_bytes(b"leave me\n")
    existing = vault / "Pojęcia" / "Existing.md"
    original = _note("existing-1", "c1", "before").encode("utf-8")
    existing.write_bytes(original)
    before_untouched = untouched.read_bytes()
    patches = [
        _patch("new-1", "Procesy/New.md", "c2", "created", None),
        _patch("existing-1", "Pojęcia/Existing.md", "c1", "after", _hash_file(existing)),
    ]
    workspace = tmp_path / "workspace"

    receipt = apply_publication(patches, vault, workspace)

    assert receipt.status == "committed"
    assert (vault / "Procesy" / "New.md").read_text(encoding="utf-8") == patches[0].proposed_content
    assert (vault / "Pojęcia" / "Existing.md").read_text(encoding="utf-8") == patches[1].proposed_content
    assert untouched.read_bytes() == before_untouched
    journal = workspace / receipt.journal_ref
    backup = workspace / receipt.backup_ref
    assert journal.is_file()
    assert backup.is_dir()
    assert vault.resolve() not in journal.resolve().parents
    assert (backup / "Pojęcia" / "Existing.md").read_bytes() == original
    assert (vault / "Procesy" / "New.md").read_bytes() == patches[0].proposed_content.encode("utf-8")
    assert not any(path.name.endswith(".pubtmp") for path in vault.rglob("*"))


def test_second_apply_is_idempotent(tmp_path):
    vault = _make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    patch = _patch("n1", "Narzędzia/Tool.md", "c1", "same", None)
    first = apply_publication([patch], vault, workspace)
    target = vault / "Narzędzia" / "Tool.md"
    before = target.read_bytes()
    stamp = target.stat().st_mtime_ns

    second = apply_publication([patch], vault, workspace)

    assert first.status == "committed"
    assert second.status == "already_committed"
    assert second.publication_id == first.publication_id
    assert target.read_bytes() == before
    assert target.stat().st_mtime_ns == stamp


def test_manual_edit_before_apply_does_not_overwrite(tmp_path):
    vault = _make_vault(tmp_path)
    existing = vault / "Pojęcia" / "Existing.md"
    original = _note("existing-1", "c1", "before")
    existing.write_bytes(original.encode("utf-8"))
    patch = _patch("existing-1", "Pojęcia/Existing.md", "c1", "after", _hash_file(existing))
    plan_publication([patch], vault)
    existing.write_bytes(_note("existing-1", "c1", "manual").encode("utf-8"))

    with pytest.raises(PublicationConflict):
        apply_publication([patch], vault, tmp_path / "workspace")

    assert existing.read_text(encoding="utf-8") == _note("existing-1", "c1", "manual")


def test_rollback_restores_hashes_and_removes_created_files(tmp_path):
    vault = _make_vault(tmp_path)
    existing = vault / "Pojęcia" / "Existing.md"
    original = _note("existing-1", "c1", "before")
    existing.write_bytes(original.encode("utf-8"))
    other = vault / "Zasady" / "Keep.md"
    other.write_bytes(b"keep\n")
    before = _vault_hashes(vault)
    patches = [
        _patch("new-1", "Procesy/Nested/New.md", "c2", "created", None),
        _patch("existing-1", "Pojęcia/Existing.md", "c1", "after", _hash_file(existing)),
    ]
    workspace = tmp_path / "workspace"
    receipt = apply_publication(patches, vault, workspace)

    rolled = rollback_publication(receipt.publication_id, vault, workspace)

    assert rolled.status == "rolled_back"
    assert _vault_hashes(vault) == before
    assert not (vault / "Procesy" / "Nested").exists()
    again = rollback_publication(receipt.publication_id, vault, workspace)
    assert again.status == "already_rolled_back"
    assert _vault_hashes(vault) == before


def test_later_manual_edit_blocks_rollback_without_overwrite(tmp_path):
    vault = _make_vault(tmp_path)
    first = vault / "Pojęcia" / "One.md"
    second = vault / "Procesy" / "Two.md"
    patches = [
        _patch("one", "Pojęcia/One.md", "c1", "one", None),
        _patch("two", "Procesy/Two.md", "c2", "two", None),
    ]
    workspace = tmp_path / "workspace"
    receipt = apply_publication(patches, vault, workspace)
    edited = _note("two", "c2", "manual edit")
    second.write_text(edited, encoding="utf-8")
    published_first = first.read_bytes()

    with pytest.raises(PublicationConflict):
        rollback_publication(receipt.publication_id, vault, workspace)

    assert first.read_bytes() == published_first
    assert second.read_text(encoding="utf-8") == edited
    journal = json.loads((workspace / receipt.journal_ref).read_text(encoding="utf-8"))
    assert journal["status"] == "committed"


def test_interrupted_apply_recovers_without_finishing_writes(tmp_path):
    vault = _make_vault(tmp_path)
    before = _vault_hashes(vault)
    patches = [
        _patch("one", "Pojęcia/One.md", "c1", "one", None),
        _patch("two", "Procesy/Two.md", "c2", "two", None),
    ]
    workspace = tmp_path / "workspace"

    with pytest.raises(PublicationInterrupted):
        apply_publication(patches, vault, workspace, interrupt_after=1)

    assert (vault / "Pojęcia" / "One.md").is_file()
    assert not (vault / "Procesy" / "Two.md").exists()
    with pytest.raises(PublicationRejected):
        apply_publication(patches, vault, workspace)

    recovered = recover_publication(vault, workspace)

    assert recovered.status == "rolled_back"
    assert _vault_hashes(vault) == before
    assert not (vault / "Procesy" / "Two.md").exists()
    replay = apply_publication(patches, vault, workspace)
    assert replay.status == "committed"
    assert (vault / "Procesy" / "Two.md").is_file()


def test_lock_and_workspace_guards(tmp_path):
    vault = _make_vault(tmp_path)
    patch = _patch("n1", "Zasady/Rule.md", "c1", "body", None)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "publication.lock").write_text("held", encoding="utf-8")
    before = _vault_hashes(vault)

    with pytest.raises(PublicationRejected):
        apply_publication([patch], vault, workspace)
    assert _vault_hashes(vault) == before

    inside = vault / "outside-looking"
    with pytest.raises(PublicationRejected):
        apply_publication([patch], vault, inside)
    assert not inside.exists()


def test_recover_breaks_dead_lock_but_not_live_lock(tmp_path):
    vault = _make_vault(tmp_path)
    workspace = tmp_path / "workspace"
    patch = _patch("n1", "Zasady/Rule.md", "c1", "body", None)
    with pytest.raises(PublicationInterrupted):
        apply_publication([patch], vault, workspace, interrupt_after=1)
    journal_path = next((workspace / "publications").glob("*/journal.json"))
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    lock = workspace / "publication.lock"
    lock.write_text(json.dumps({"pid": os.getpid(), "publication_id": journal["publication_id"]}), encoding="utf-8")

    with pytest.raises(PublicationRejected):
        recover_publication(vault, workspace)
    assert (vault / "Zasady" / "Rule.md").is_file()

    lock.write_text(json.dumps({"pid": 2**31 - 1, "publication_id": journal["publication_id"]}), encoding="utf-8")
    recovered = recover_publication(vault, workspace)
    assert recovered.status == "rolled_back"
    assert not (vault / "Zasady" / "Rule.md").exists()
    assert not lock.exists()


def test_repo_vault_bytes_stay_untouched(tmp_path):
    marker = REPO_VAULT / "00 Start.md"
    before = marker.read_bytes() if marker.is_file() else None
    vault = _make_vault(tmp_path)
    apply_publication(
        [_patch("n1", "Pojęcia/Temp.md", "c1", "temp", None)],
        vault,
        tmp_path / "workspace",
    )
    if before is not None:
        assert marker.read_bytes() == before
