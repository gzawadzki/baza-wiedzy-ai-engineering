from pathlib import Path
import pytest
from kb_pipeline.retrieval import reindex, search


@pytest.fixture
def test_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    vault.mkdir()

    pojecia = vault / "Pojęcia"
    pojecia.mkdir()
    (pojecia / "Kompaktowanie.md").write_text(
        """---
aliases: [Safe Checkpoint, Bezpieczny punkt]
status: published
---

# Kompaktowanie kontekstu

Pierwsza sekcja o kompaktowaniu pamięci agenta.

## Kryterium bezpiecznego punktu

Punkt jest bezpieczny, jeśli stan agenta został utrwalony na dysku.

## Szczegóły implementacji

Wymaga weryfikacji testowej.
""",
        encoding="utf-8",
    )

    procesy = vault / "Procesy"
    procesy.mkdir()
    (procesy / "Praca z harnessem.md").write_text(
        """---
note_id: custom-process-01
status: draft
---

# Harness

Zarządzanie sesjami agenta i ewaluacja.
""",
        encoding="utf-8",
    )

    zrodla = vault / "Źródła"
    zrodla.mkdir()
    (zrodla / "KunChen.md").write_text(
        """---
aliases: [Kun Chen Notes]
---

# Wskazówki Kuna Chena

Notatki źródłowe dotyczące architektury pamięci agenta.
""",
        encoding="utf-8",
    )

    return vault


def test_reindex_and_section_retrieval(test_vault: Path, tmp_path: Path):
    db_path = tmp_path / "index.sqlite3"
    count = reindex(test_vault, db_path)
    assert count == 5  # Kompaktowanie (3 sections) + Harness (1) + KunChen (1)

    results = search(db_path, "bezpiecznego punktu")
    assert len(results) >= 1
    top = results[0]
    assert top["path"] == "Pojęcia/Kompaktowanie.md"
    assert top["heading"] == "Kryterium bezpiecznego punktu"
    assert top["anchor"] == "kryterium-bezpiecznego-punktu"
    assert top["status"] == "published"
    assert isinstance(top["note_id"], str)
    assert top["score"] > 0
    assert "bezpiecznego punktu" in top["snippet"].lower()


def test_aliases_pl_and_en(test_vault: Path, tmp_path: Path):
    db_path = tmp_path / "index.sqlite3"
    reindex(test_vault, db_path)

    en_results = search(db_path, "Safe Checkpoint")
    assert len(en_results) >= 1
    assert any(r["path"] == "Pojęcia/Kompaktowanie.md" for r in en_results)

    pl_results = search(db_path, "Bezpieczny punkt")
    assert len(pl_results) >= 1
    assert any(r["path"] == "Pojęcia/Kompaktowanie.md" for r in pl_results)


def test_source_exclusion_by_default(test_vault: Path, tmp_path: Path):
    db_path = tmp_path / "index.sqlite3"
    reindex(test_vault, db_path)

    default_results = search(db_path, "Wskazówki")
    assert not any(r["path"].startswith("Źródła/") for r in default_results)

    source_results = search(db_path, "Wskazówki", include_sources=True)
    assert any(r["path"] == "Źródła/KunChen.md" for r in source_results)


def test_stale_removal_on_reindex(test_vault: Path, tmp_path: Path):
    db_path = tmp_path / "index.sqlite3"
    reindex(test_vault, db_path)

    results_before = search(db_path, "Harness")
    assert any(r["path"] == "Procesy/Praca z harnessem.md" for r in results_before)

    # Delete note and reindex
    (test_vault / "Procesy" / "Praca z harnessem.md").unlink()
    reindex(test_vault, db_path)

    results_after = search(db_path, "Harness")
    assert not any(r["path"] == "Procesy/Praca z harnessem.md" for r in results_after)


def test_safe_search_queries(test_vault: Path, tmp_path: Path):
    db_path = tmp_path / "index.sqlite3"
    reindex(test_vault, db_path)

    malformed_queries = [
        "",
        "   ",
        '"unclosed quote',
        "test ( unmatched",
        "AND",
        "OR",
        "NOT",
        "*",
        ":::;;;!!!",
        "Kompaktowanie AND OR",
        "-",
    ]

    for q in malformed_queries:
        res = search(db_path, q)
        assert isinstance(res, list)


def test_deterministic_fallback_note_id(test_vault: Path, tmp_path: Path):
    db_path = tmp_path / "index.sqlite3"
    reindex(test_vault, db_path)

    results = search(db_path, "Kompaktowanie")
    note_id_first = results[0]["note_id"]
    assert note_id_first
    assert len(note_id_first) == 16

    # Reindex again and verify note_id is identical
    reindex(test_vault, db_path)
    results_second = search(db_path, "Kompaktowanie")
    assert results_second[0]["note_id"] == note_id_first


def test_database_inside_vault_prohibited(test_vault: Path):
    inside_db = test_vault / "index.sqlite3"
    with pytest.raises(ValueError, match="outside the vault"):
        reindex(test_vault, inside_db)


def test_skip_symlinks(test_vault: Path, tmp_path: Path):
    link_file = test_vault / "Pojęcia" / "SymlinkNote.md"
    target = test_vault / "Procesy" / "Praca z harnessem.md"
    try:
        link_file.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks not supported on this platform/environment")

    db_path = tmp_path / "index.sqlite3"
    reindex(test_vault, db_path)

    results = search(db_path, "Harness")
    assert not any(r["path"] == "Pojęcia/SymlinkNote.md" for r in results)
