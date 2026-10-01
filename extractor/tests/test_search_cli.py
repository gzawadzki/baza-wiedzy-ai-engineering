"""Offline tests for the search/reindex CLI branches (PKG-2C).

Synthetic vault only; no network, no source writes.
"""

import json
import sys
from pathlib import Path

import pytest

from kb_pipeline import __main__ as cli
from kb_pipeline.search_cli import (
    RetrievalError,
    index_path,
    reindex_vault,
    search_index,
)


@pytest.fixture
def synthetic_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    (vault / "Pojęcia").mkdir(parents=True)
    (vault / "Procesy").mkdir()
    (vault / "Źródła").mkdir()

    (vault / "Pojęcia" / "Kompaktowanie.md").write_text(
        """---
aliases: [Safe Checkpoint, Bezpieczny punkt kompaktowania]
status: published
---

# Kompaktowanie kontekstu

Krótka sekcja o kompaktowaniu pamięci agenta. To pojęcie opisuje granice kontekstu.

## Kryterium bezpiecznego punktu

Stan agenta musi zostać utrwalony na dysku przed kompaktowaniem (safe checkpoint,
angielski synonim używany w źródłach).
""",
        encoding="utf-8",
    )
    (vault / "Procesy" / "Praca z harnessem.md").write_text(
        """---
note_id: custom-process-01
status: draft
---

# Harness

Ewaluacja sesji agenta i zbieranie trace'ów.
""",
        encoding="utf-8",
    )
    (vault / "Źródła" / "KunChen.md").write_text(
        """---
aliases: [Kun Chen Notes]
---

# Wskazówki Kuna Chena

Notatki źródłowe o architekturze pamięci agenta.
""",
        encoding="utf-8",
    )
    return vault


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "workspace"
    ws.mkdir()
    return ws


def _vault_digest(vault: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    for path in sorted(vault.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(vault).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


# --- reindex -------------------------------------------------------------


def test_reindex_writes_only_workspace(synthetic_vault: Path, workspace: Path):
    before = _vault_digest(synthetic_vault)
    result = reindex_vault(synthetic_vault, workspace)

    assert result["status"] == "ok"
    assert result["sections"] == 4
    assert result["vault_writes"] == 0
    assert index_path(workspace).is_file()
    assert _vault_digest(synthetic_vault) == before
    assert str(index_path(workspace).resolve()).startswith(str(workspace.resolve()))


def test_reindex_is_idempotent_and_content_stable(synthetic_vault: Path, workspace: Path):
    first = reindex_vault(synthetic_vault, workspace)
    second = reindex_vault(synthetic_vault, workspace)

    assert first["sections"] == second["sections"]
    assert first["fingerprint"] == second["fingerprint"]
    assert first["index"] == second["index"]
    assert search_index(workspace, "kompaktowanie") == search_index(workspace, "kompaktowanie")


def test_reindex_after_note_edit_reflects_change(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    (synthetic_vault / "Procesy" / "Praca z harnessem.md").unlink()
    result = reindex_vault(synthetic_vault, workspace)

    assert result["sections"] == 3
    hits = search_index(workspace, "harness")["results"]
    assert not any(item["path"] == "Procesy/Praca z harnessem.md" for item in hits)


def test_reindex_rejects_missing_vault(workspace: Path, tmp_path: Path):
    with pytest.raises(RetrievalError) as excinfo:
        reindex_vault(tmp_path / "nie-ma-mnie", workspace)
    assert excinfo.value.code == "missing_vault"


def test_reindex_rejects_missing_workspace(synthetic_vault: Path, tmp_path: Path):
    with pytest.raises(RetrievalError) as excinfo:
        reindex_vault(synthetic_vault, tmp_path / "nie-ma-workspace")
    assert excinfo.value.code == "missing_workspace"


# --- search --------------------------------------------------------------


def test_search_polish_diacritics(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    for query in ("pojęcie", "pojecie", "Bezpieczny punkt kompaktowania"):
        result = search_index(workspace, query)
        assert result["count"] >= 1, query
        assert any(item["path"] == "Pojęcia/Kompaktowanie.md" for item in result["results"]), query


def test_search_english_query(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    result = search_index(workspace, "safe checkpoint")
    assert any(item["path"] == "Pojęcia/Kompaktowanie.md" for item in result["results"])

    notes = search_index(workspace, "safe checkpoint")
    assert any(item["path"] == "Pojęcia/Kompaktowanie.md" for item in notes["results"])


def test_search_json_is_deterministic_and_serializable(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    payload = search_index(workspace, "harness")
    first = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    second = json.dumps(search_index(workspace, "harness"), ensure_ascii=False, sort_keys=True)
    assert first == second

    hit = payload["results"][0]
    assert set(hit) == {"path", "note_id", "heading", "anchor", "snippet", "score", "status"}


def test_search_excludes_sources_by_default(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    default_hits = search_index(workspace, "Wskazówki")["results"]
    assert not any(item["path"].startswith("Źródła/") for item in default_hits)

    with_sources = search_index(workspace, "Wskazówki", include_sources=True)["results"]
    assert any(item["path"] == "Źródła/KunChen.md" for item in with_sources)


def test_search_missing_index_is_understandable(workspace: Path):
    with pytest.raises(RetrievalError) as excinfo:
        search_index(workspace, "cokolwiek")
    assert excinfo.value.code == "missing_index"
    assert "reindex" in (excinfo.value.hint or "")
    payload = excinfo.value.payload()
    assert payload["status"] == "error"
    assert "code" in payload and "error" in payload


def test_search_rejects_empty_query(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    with pytest.raises(RetrievalError) as excinfo:
        search_index(workspace, "   ")
    assert excinfo.value.code == "empty_query"


def test_search_rejects_bad_limit(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    with pytest.raises(RetrievalError) as excinfo:
        search_index(workspace, "harness", limit=0)
    assert excinfo.value.code == "invalid_limit"


def test_search_does_not_write_anything(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    vault_before = _vault_digest(synthetic_vault)
    index_before = index_path(workspace).read_bytes()
    info_before = (workspace / "retrieval" / "index-info.json").read_bytes()

    search_index(workspace, "kompaktowanie")

    assert _vault_digest(synthetic_vault) == vault_before
    assert index_path(workspace).read_bytes() == index_before
    assert (workspace / "retrieval" / "index-info.json").read_bytes() == info_before


def test_optional_vault_selector_is_read_only(synthetic_vault: Path, workspace: Path):
    reindex_vault(synthetic_vault, workspace)
    before = _vault_digest(synthetic_vault)
    payload = search_index(workspace, "harness", vault=synthetic_vault)

    assert payload["vault"] == synthetic_vault.resolve().as_posix()
    assert _vault_digest(synthetic_vault) == before

    with pytest.raises(RetrievalError) as excinfo:
        search_index(workspace, "harness", vault=workspace / "nie-ma-mnie")
    assert excinfo.value.code == "missing_vault"


# --- CLI -----------------------------------------------------------------


def _run_cli(monkeypatch, capsys, argv: list[str]) -> tuple[int, dict]:
    monkeypatch.setattr(sys, "argv", ["kb_pipeline", *argv])
    code = 0
    try:
        cli.main()
    except SystemExit as exc:
        code = exc.code or 0
    out = capsys.readouterr().out.strip().splitlines()
    return code, json.loads(out[-1])


def test_cli_reindex_and_search(monkeypatch, capsys, synthetic_vault: Path, workspace: Path):
    code, payload = _run_cli(
        monkeypatch,
        capsys,
        ["reindex", "--vault", str(synthetic_vault), "--workspace", str(workspace)],
    )
    assert code == 0
    assert payload["status"] == "ok"
    assert payload["sections"] == 4
    assert payload["vault_writes"] == 0

    code, payload = _run_cli(
        monkeypatch, capsys, ["search", "pojęcie", "--workspace", str(workspace), "--format", "json"]
    )
    assert code == 0
    assert payload["command"] == "search"
    assert payload["query"] == "pojęcie"
    assert any(item["path"] == "Pojęcia/Kompaktowanie.md" for item in payload["results"])


def test_cli_reindex_printed_json_is_byte_stable(monkeypatch, capsys, synthetic_vault, workspace):
    lines = []
    for _ in range(2):
        monkeypatch.setattr(
            sys,
            "argv",
            ["kb_pipeline", "reindex", "--vault", str(synthetic_vault), "--workspace", str(workspace)],
        )
        cli.main()
        lines.append(capsys.readouterr().out.strip())
    assert lines[0] == lines[1]


def test_cli_search_missing_index_exit_code(monkeypatch, capsys, workspace: Path):
    code, payload = _run_cli(
        monkeypatch, capsys, ["search", "cokolwiek", "--workspace", str(workspace)]
    )
    assert code == 1
    assert payload["status"] == "error"
    assert payload["code"] == "missing_index"


def test_cli_search_empty_query_exit_code(monkeypatch, capsys, synthetic_vault, workspace):
    _run_cli(
        monkeypatch,
        capsys,
        ["reindex", "--vault", str(synthetic_vault), "--workspace", str(workspace)],
    )
    code, payload = _run_cli(monkeypatch, capsys, ["search", "  ", "--workspace", str(workspace)])
    assert code == 1
    assert payload["code"] == "empty_query"


def test_cli_help_lists_retrieval_commands(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["kb_pipeline", "--help"])
    with pytest.raises(SystemExit):
        cli.main()
    out = capsys.readouterr().out
    assert "reindex" in out
    assert "search" in out
