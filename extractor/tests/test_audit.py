import json
from pathlib import Path

import pytest

from kb_pipeline.audit import audit, snapshot, verify_snapshot


def test_audit_reports_existing_issues_without_modifying_notes(tmp_path):
    vault = tmp_path / "vault"
    notes = vault / "Pojęcia"
    notes.mkdir(parents=True)
    first = notes / "first.md"
    first.write_text('---\nid: shared\naliases: [shortcut]\n---\n# Hi\n[[missing]] [[second]] [[shortcut]]', encoding="utf-8")
    (notes / "second.md").write_text('---\nid: shared\n---\n# Second\n[[first]]', encoding="utf-8")
    (vault / "empty.md").write_bytes(b"")
    (notes / "bad.md").write_text('---\ninvalid: [\n---\n[[shortcut]]', encoding="utf-8")
    (notes / "third.md").write_text('---\naliases: [shortcut]\n---\n[[shortcut]]', encoding="utf-8")
    before = {p: p.read_bytes() for p in vault.rglob("*.md")}
    report = audit(vault)
    assert report["counts"]["markdown"] == 5
    assert report["empty_files"] == ["empty.md"]
    assert report["duplicate_ids"]["shared"] == ["Pojęcia/first.md", "Pojęcia/second.md"]
    assert report["invalid_yaml"][0]["path"] == "Pojęcia/bad.md"
    assert {i["target"] for i in report["broken_links"]} == {"missing"}
    assert {i["target"] for i in report["ambiguous_links"]} == {"shortcut"}
    assert before == {p: p.read_bytes() for p in vault.rglob("*.md")}


def test_snapshot_includes_untracked_but_not_secrets_and_detects_corruption(tmp_path):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Pojęcia").mkdir()
    (vault / "Pojęcia" / "new.md").write_text("untracked", encoding="utf-8")
    (vault / "extractor").mkdir()
    (vault / "extractor" / ".env").write_text("SECRET_TOKEN=private")
    (vault / ".obsidian").mkdir()
    (vault / ".obsidian" / "graph.json").write_text("{}")
    dest = tmp_path / "snapshot"
    manifest = snapshot(vault, dest)
    assert [f["path"] for f in manifest["files"]] == ["Pojęcia/new.md"]
    assert "SECRET_TOKEN" not in (dest / "manifest.json").read_text()
    assert verify_snapshot(dest) == []
    (dest / "files" / "Pojęcia" / "new.md").write_text("corrupted")
    assert verify_snapshot(dest) == ["Pojęcia/new.md"]
    with pytest.raises(FileExistsError):
        snapshot(vault, dest)
    with pytest.raises(ValueError):
        snapshot(vault, vault / "backup")
