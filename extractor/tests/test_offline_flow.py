"""End-to-end contract for the offline vertical flow (`run --offline`).

One run goes cache -> SourceStore -> context -> gates -> claims -> verification
-> integration -> NotePatch -> read-only publication plan, with durable stage
artifacts and a persisted RunManifest. No network, no secrets, no vault writes.

These tests exercise behaviour on fixtures with fake providers. They are not
evidence of semantic quality and say nothing about live provider behaviour.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from kb_pipeline.offline_cli import run_offline
from kb_pipeline.offline_flow import FlowProviders, fake_providers, run_offline_flow
from kb_pipeline.schemas import Claim, RunManifest, StageStatus
from kb_pipeline.stage_cache import StageCache
from kb_pipeline.storage import SourceStore
from kb_pipeline.thresholds import resolve_thresholds, thresholds_fingerprint

EXTRACTOR = Path(__file__).resolve().parents[1]

USEFUL_TEXT = (
    "Always record the failing step before you change the prompt, otherwise you "
    "cannot tell a regression from noise."
)


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
def _vault_hashes(vault: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(vault.rglob("*")):
        if path.is_file():
            out[str(path.relative_to(vault))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def _build_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    (vault / "Pojęcia").mkdir(parents=True)
    (vault / "Pojęcia" / "Fail-fast.md").write_text(
        "---\n"
        "note_id: kb-fail-fast\n"
        "kb_managed: true\n"
        "claim_ids: []\n"
        "---\n\n"
        "# Fail-fast\n\n"
        "## Diagnostyka zmian\n\n"
        "Rejestruj krok, który zawiódł, zanim zmienisz prompt, żeby odróżnić "
        "regresję od szumu.\n",
        encoding="utf-8",
    )
    (vault / "Pojęcia" / "Manualna notatka.md").write_text(
        "# Manualna notatka\n\nTekst pisany ręcznie przez właściciela.\n", encoding="utf-8"
    )
    (vault / "Źródła").mkdir(parents=True)
    return vault


def _cache_file(tmp_path: Path, *, text: str = USEFUL_TEXT, tweet_id: str = "1001") -> Path:
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / "someuser_raw_tweets.json"
    path.write_text(
        json.dumps(
            [
                {
                    "id": tweet_id,
                    "username": "someuser",
                    "full_text": text,
                    "created_at": "Wed Oct 01 09:00:00 +0000 2026",
                    "lang": "en",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


def _run(cache: Path, vault: Path, workspace: Path, **kwargs):
    options = {
        "providers": fake_providers(),
        "cache_dir": None,
        "handles": None,
        "source_ids": None,
        "limit": 80,
    }
    options.update(kwargs)
    return run_offline(
        vault=vault,
        workspace=workspace,
        cache_input=cache,
        **options,
    )


# --------------------------------------------------------------------------- #
# vertical run
# --------------------------------------------------------------------------- #
def test_single_run_reaches_proposed_section_and_plan(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    before = _vault_hashes(vault)

    result = _run(cache, vault, workspace)

    assert result["status"] == "ok"
    assert result["vault_written"] is False
    assert result["counters"]["error"] == 0
    assert result["provider_calls"] > 0, "first run must call providers"
    assert result["replay"] is False
    run = result["runs"][0]
    assert run["status"] == "extract", run
    assert run["stages"]["context"] == "completed"
    assert run["stages"]["local_gate"] == "completed"
    assert run["stages"]["publication_plan"] == "completed"
    assert run["patch_count"] >= 1

    run_dir = Path(result["run_dir"])
    for artifact in (
        "source_record.json",
        "context_bundle.json",
        "gate_decisions.json",
        "jev_assessment.json",
        "claims.json",
        "verification_results.json",
        "integration_decisions.json",
        "proposed_section.md",
        "publication_plan.json",
        "summary.json",
        "manifest.json",
    ):
        assert (run_dir / "artifacts" / artifact).exists() or (run_dir / artifact).exists(), artifact

    plan = json.loads((run_dir / "artifacts" / "publication_plan.json").read_text(encoding="utf-8"))
    assert plan["applied"] is False
    assert plan["mode"] == "plan_only"
    assert plan["plan"]["writes"], "plan must describe the writes it would do"
    assert "diff" in plan and "No file in the vault is written" in plan["diff"]

    assert _vault_hashes(vault) == before, "offline run must not write into the vault"


def test_manifest_is_durable_and_reloadable(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace)

    manifest = RunManifest.model_validate_json(
        (Path(result["run_dir"]) / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest.code_version == "offline-flow-v1"
    assert manifest.stages["local_gate"].status is StageStatus.completed
    assert manifest.stages["verification"].status is StageStatus.completed
    assert manifest.publication_plan_ref == "artifacts/publication_plan.json"
    with StageCache(workspace) as cache_store:
        stored = cache_store.load_manifest(manifest.run_id)
    assert stored is not None and stored.run_id == manifest.run_id


def test_manifest_records_thresholds_and_fake_provider_mode(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace)

    summary = json.loads((Path(result["run_dir"]) / "summary.json").read_text(encoding="utf-8"))
    assert summary["provider_mode"] == "fake-offline"
    assert summary["fake_providers"] == {"mode": "fake-offline", "fake": True}
    values = summary["thresholds"]["values"]
    assert values["focus_claim_reject"] == 0.30
    assert values["promotion_reject"] == 0.75
    assert values["category_confidence"] == 0.50
    assert summary["thresholds"]["fingerprint"] == thresholds_fingerprint(
        resolve_thresholds()
    )
    claims = json.loads(
        (Path(result["run_dir"]) / "artifacts" / "claims.json").read_text(encoding="utf-8")
    )
    assert claims["provider"]["fake"] is True


def test_second_identical_run_makes_no_provider_calls(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"

    first = _run(cache, vault, workspace)
    second = _run(cache, vault, workspace)

    assert second["run_id"] == first["run_id"]
    assert second["run_dir"] == first["run_dir"]
    assert second["provider_calls"] == 0, "replay must not call providers again"
    assert second["replay"] is True
    assert second["counters"] == first["counters"]
    assert second["patches"] == first["patches"], "replay must reproduce the same NotePatch"


def test_replay_does_not_create_new_files(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    _run(cache, vault, workspace)

    def snapshot() -> dict[str, str]:
        return {
            str(path.relative_to(workspace)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(workspace.rglob("*"))
            if path.is_file()
        }

    before = snapshot()
    _run(cache, vault, workspace)
    after = snapshot()
    assert set(after) == set(before), "identical replay must not create new files"
    # summary.json and manifest.json legitimately carry run time; the SQLite index
    # file bytes are not stable across rebuilds of identical content; the rest must
    # match byte for byte.
    for name in before:
        if name.endswith(("summary.json", "manifest.json")) or name.endswith(".sqlite3"):
            continue
        assert after[name] == before[name], name


def test_source_store_and_vault_are_unchanged_by_repeat_imports(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    vault_before = _vault_hashes(vault)

    _run(cache, vault, workspace)
    with SourceStore(workspace) as store:
        records_first = {
            row[0]: row[1] for row in store.connection.execute(
                "SELECT source_id, record_json FROM source_revisions"
            )
        }
    _run(cache, vault, workspace)
    with SourceStore(workspace) as store:
        records_second = {
            row[0]: row[1] for row in store.connection.execute(
                "SELECT source_id, record_json FROM source_revisions"
            )
        }

    assert records_first == records_second, "re-import must not change stored source records"
    assert _vault_hashes(vault) == vault_before


# --------------------------------------------------------------------------- #
# counters: reject / defer / error stay separate
# --------------------------------------------------------------------------- #
def test_counters_separate_reject_defer_and_error(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "mixed_raw_tweets.json").write_text(
        json.dumps(
            [
                {"id": "2001", "username": "u", "full_text": USEFUL_TEXT},
                {"id": "2002", "username": "u", "full_text": "https://example.com/x"},
                {"id": "2003", "username": "u", "full_text": "this"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = _run(cache_dir / "mixed_raw_tweets.json", vault, workspace)

    statuses = {run["source_id"]: run["status"] for run in result["runs"]}
    assert statuses["x:2001"] == "extract", statuses
    assert statuses["x:2002"] == "reject", statuses
    assert statuses["x:2003"] == "reject", statuses

    counters = result["counters"]
    assert counters == {"extract": 1, "reject": 2, "defer": 0, "error": 0}
    reasons = {run["source_id"]: run["reason"] for run in result["runs"]}
    assert reasons["x:2002"] == "link_only"
    assert reasons["x:2003"] == "reaction_only"


def test_promotion_bar_rejects_as_reject(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace, providers=fake_providers(promo_answers={"promotion": 0.95}))
    assert result["runs"][0]["status"] == "reject"
    assert result["runs"][0]["reason"] == "promotion"


def test_defer_is_used_for_uncertainty_not_failure(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"

    result = _run(
        cache,
        vault,
        workspace,
        providers=fake_providers(category_confidence=0.10),
    )

    assert result["runs"][0]["status"] == "defer"
    assert result["counters"]["error"] == 0
    assert result["runs"][0]["stages"]["category"] == "deferred"


def test_provider_failure_is_error_not_defer(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"

    providers = fake_providers()

    def boom(_text: str) -> dict:
        raise RuntimeError("provider exploded")

    result = _run(
        cache,
        vault,
        workspace,
        providers=FlowProviders(
            mode="fake-offline",
            local_filter=boom,
            categorize=providers.categorize,
            jev_evaluate=providers.jev_evaluate,
            extract_claims=providers.extract_claims,
            advisor=providers.advisor,
            semantic_check=providers.semantic_check,
            model_versions=providers.model_versions,
        ),
    )

    assert result["runs"][0]["status"] == "error", "provider failure is an error, never a defer"
    assert result["counters"]["error"] == 1
    assert result["counters"]["defer"] == 0
    summary = json.loads((Path(result["run_dir"]) / "summary.json").read_text(encoding="utf-8"))
    assert summary["stages"]["clm_gate"] == "error"
    assert "provider exploded" in json.dumps(summary)


# --------------------------------------------------------------------------- #
# provider honesty and injection
# --------------------------------------------------------------------------- #
def test_provider_mode_must_be_explicit():
    with pytest.raises(ValueError):
        FlowProviders(
            mode="maybe",
            local_filter=lambda _t: {},
            categorize=lambda _t: {},
            jev_evaluate=lambda _b: {},
            extract_claims=lambda _b, _c: [],
            advisor=lambda *a: None,
        )


def test_fake_providers_are_labelled_and_never_pass_as_live(tmp_path: Path):
    assert fake_providers().mode == "fake-offline"
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace)
    for artifact in sorted((Path(result["run_dir"]) / "artifacts").glob("*.json")):
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        assert payload.get("provider", {}).get("mode") == "fake-offline", artifact.name


# --------------------------------------------------------------------------- #
# attribution: quotes must come from the author's own text
# --------------------------------------------------------------------------- #
def test_quote_from_parent_text_is_rejected(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "parent_raw_tweets.json").write_text(
        json.dumps(
            [
                {"id": "3001", "username": "u", "full_text": "Rodzic mówi o awarii usługi i kosztach."},
                {
                    "id": "3002",
                    "username": "u",
                    "full_text": "Zgadzam się, że warto to mierzyć.",
                    "in_reply_to_status_id": "3001",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    providers = fake_providers()

    def foreign_quote_claims(bundle, category=None):
        return [
            Claim(
                claim_id="x3002-c1",
                source_ids=[bundle.focus.source_id],
                text="Awaria usługi kosztowała zespół fortunę.",
                kind="observation",
                evidence=[
                    {
                        "source_id": bundle.focus.source_id,
                        "quote": "Rodzic mówi o awarii usługi i kosztach.",
                    }
                ],
            )
        ]

    result = _run(
        cache_dir / "parent_raw_tweets.json",
        vault,
        workspace,
        source_ids=["x:3002"],
        providers=FlowProviders(
            mode="fake-offline",
            local_filter=providers.local_filter,
            categorize=providers.categorize,
            jev_evaluate=providers.jev_evaluate,
            extract_claims=lambda bundle, category=None: foreign_quote_claims(bundle),
            advisor=providers.advisor,
            semantic_check=providers.semantic_check,
            model_versions=providers.model_versions,
        ),
    )

    run = result["runs"][0]
    assert run["status"] == "reject", run
    assert run["reason"] == "quote_not_in_author_text"
    assert result["patches"] == []


def test_claim_quoting_foreign_source_id_rejected(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "parent_raw_tweets.json").write_text(
        json.dumps(
            [
                {
                    "id": "3001",
                    "username": "alice",
                    "full_text": "Rodzic mówi o awarii usługi i kosztach.",
                },
                {
                    "id": "3002",
                    "username": "bob",
                    "full_text": "To prawda, zgadzam się z przedmówcą całkowicie.",
                    "in_reply_to_status_id": "3001",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    providers = fake_providers()

    def foreign_id_claims(bundle, category=None):
        return [
            Claim(
                claim_id="x3002-c1",
                source_ids=[bundle.focus.source_id, "x:3001"],
                text="Awaria usługi kosztowała zespół fortunę.",
                kind="observation",
                evidence=[
                    {
                        "source_id": "x:3001",
                        "quote": "Rodzic mówi o awarii usługi i kosztach.",
                    }
                ],
            )
        ]

    result = _run(
        cache_dir / "parent_raw_tweets.json",
        vault,
        workspace,
        source_ids=["x:3002"],
        providers=FlowProviders(
            mode="fake-offline",
            local_filter=providers.local_filter,
            categorize=providers.categorize,
            jev_evaluate=providers.jev_evaluate,
            extract_claims=lambda bundle, category=None: foreign_id_claims(bundle),
            advisor=providers.advisor,
            semantic_check=providers.semantic_check,
            model_versions=providers.model_versions,
        ),
    )

    run = result["runs"][0]
    assert run["status"] == "reject", run
    assert run["reason"] == "quote_not_in_author_text"
    assert result["patches"] == []


def test_local_gate_rejection_omits_clm_gate_stage(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "reaction_raw_tweets.json").write_text(
        json.dumps(
            [
                {"id": "5001", "username": "u", "full_text": "Dzięki!"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    result = _run(cache_dir / "reaction_raw_tweets.json", vault, workspace)
    run = result["runs"][0]
    assert run["status"] == "reject"
    assert run["reason"] == "reaction_only"
    assert run["stages"]["local_gate"] == "rejected"
    assert "clm_gate" not in run["stages"]


def test_integration_candidates_scoped_per_claim(tmp_path: Path):
    vault = _build_vault(tmp_path)
    (vault / "Pojęcia" / "Postmortem.md").write_text(
        "---\n"
        "note_id: kb-postmortem\n"
        "kb_managed: true\n"
        "claim_ids: []\n"
        "---\n\n"
        "# Postmortem\n\n"
        "## Kultura blameless\n\n"
        "Retrospektywy blameless pozwalają na otwartą analizę incydentów.\n",
        encoding="utf-8",
    )
    workspace = tmp_path / "workspace"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    text = (
        "Fail-fast redukuje czas diagnozy problemu. "
        "Kultura blameless to klucz do sukcesu zespołu."
    )
    (cache_dir / "multi_raw_tweets.json").write_text(
        json.dumps([{"id": "6001", "username": "u", "full_text": text}], ensure_ascii=False),
        encoding="utf-8",
    )
    providers = fake_providers()
    seen_candidates: dict[str, list[str]] = {}

    def tracking_advisor(claim, candidates, notes):
        seen_candidates[claim.claim_id] = [c.note_id for c in candidates]
        return providers.advisor(claim, candidates, notes)

    def two_claims(bundle, category=None):
        return [
            Claim(
                claim_id="c1",
                source_ids=[bundle.focus.source_id],
                text="prompt regresję od szumu",
                kind="recommendation",
                evidence=[
                    {
                        "source_id": bundle.focus.source_id,
                        "quote": "Fail-fast redukuje czas diagnozy problemu.",
                    }
                ],
            ),
            Claim(
                claim_id="c2",
                source_ids=[bundle.focus.source_id],
                text="blameless analizę incydentów",
                kind="recommendation",
                evidence=[
                    {
                        "source_id": bundle.focus.source_id,
                        "quote": "Kultura blameless to klucz do sukcesu zespołu.",
                    }
                ],
            ),
        ]

    result = _run(
        cache_dir / "multi_raw_tweets.json",
        vault,
        workspace,
        providers=FlowProviders(
            mode="fake-offline",
            local_filter=providers.local_filter,
            categorize=providers.categorize,
            jev_evaluate=providers.jev_evaluate,
            extract_claims=lambda b, c=None: two_claims(b),
            advisor=tracking_advisor,
            semantic_check=providers.semantic_check,
            model_versions=providers.model_versions,
        ),
    )
    assert result["status"] == "ok"
    assert "c1" in seen_candidates and "c2" in seen_candidates
    assert "kb-fail-fast" in seen_candidates["c1"]
    assert "kb-postmortem" not in seen_candidates["c1"]
    assert "kb-postmortem" in seen_candidates["c2"]
    assert "kb-fail-fast" not in seen_candidates["c2"]


def test_parent_context_is_separated_from_focus_text(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "ctx_raw_tweets.json").write_text(
        json.dumps(
            [
                {"id": "4001", "username": "u", "full_text": USEFUL_TEXT},
                {
                    "id": "4002",
                    "username": "u",
                    "full_text": "A właściwie to chodzi o prompt engineering.",
                    "in_reply_to_status_id": "4001",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    result = _run(cache_dir / "ctx_raw_tweets.json", vault, workspace, source_ids=["x:4002"])
    bundle = json.loads(
        (Path(result["run_dir"]) / "artifacts" / "context_bundle.json").read_text(encoding="utf-8")
    )
    assert bundle["focus"]["source_id"] == "x:4002"
    assert "Rejestruj" not in bundle["focus"]["text"], bundle["focus"]["text"]
    assert any(item["role"] == "parent" for item in bundle["related"])
    assert bundle["related"][0]["source_id"] == "x:4001"


# --------------------------------------------------------------------------- #
# thresholds decide, they do not invalidate cached provider answers
# --------------------------------------------------------------------------- #
def test_threshold_change_recomputes_decision_without_new_provider_call(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"

    first = _run(cache, vault, workspace)
    assert first["runs"][0]["status"] == "extract"

    stricter = _run(cache, vault, workspace, thresholds={"jev_usefulness": 0.95})
    assert stricter["provider_calls"] == 0, "threshold change must not re-call providers"
    assert stricter["runs"][0]["status"] == "defer"
    assert stricter["runs"][0]["reason"] == "insufficient_context" or stricter["runs"][0]["reason"]


def test_threshold_defaults_equal_previous_constants():
    from kb_pipeline import local_gate

    limits = resolve_thresholds()
    assert limits["focus_claim_reject"] == local_gate.CLAIM_REJECT
    assert limits["promotion_reject"] == local_gate.PROMO_REJECT
    assert limits["category_confidence"] == local_gate.CATEGORY_CONFIDENCE
    assert resolve_thresholds()["jev_usefulness"] == 0.70
    assert resolve_thresholds()["jev_context"] == 0.60
    with pytest.raises(ValueError):
        resolve_thresholds({"nonsense": 0.5})


def test_decision_thresholds_are_absent_from_cache_keys(tmp_path: Path):
    """A raw answer must be reusable across thresholds: keys are built from hashes."""
    from kb_pipeline.stage_cache import StageCache as Cache

    first = Cache.key("jev_evaluate", "a" * 64, "b" * 64, "fake-jev", "v1", 1)
    second = Cache.key("jev_evaluate", "a" * 64, "b" * 64, "fake-jev", "v1", 1)
    assert first == second
    assert Cache.key("jev_evaluate", "a" * 64, "c" * 64, "fake-jev", "v1", 1) != first


# --------------------------------------------------------------------------- #
# workspace / vault safety
# --------------------------------------------------------------------------- #
def test_workspace_inside_vault_is_refused(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    with pytest.raises(ValueError):
        _run(cache, vault, vault / "workspace")


def test_run_offline_flow_refuses_workspace_symlinked_into_vault(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace)
    with SourceStore(workspace) as store:
        record = store.get_deterministic(result["sources"][0])
    assert record is not None

    linked = tmp_path / "linked-workspace"
    linked.symlink_to(vault / "Pojęcia", target_is_directory=True)
    with pytest.raises(ValueError):
        run_offline_flow(
            source=record,
            lookup=lambda _sid: None,
            vault=vault,
            workspace=linked,
            providers=fake_providers(),
            run_id="probe",
        )
    assert list((vault / "Pojęcia").iterdir()), "vault content untouched by the refusal"


# --------------------------------------------------------------------------- #
# CLI contract
# --------------------------------------------------------------------------- #
def _run_cli(*args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(EXTRACTOR)
    env["CLM_BASE_URL"] = "http://127.0.0.1:1"
    env["OPENAI_API_KEY"] = ""
    return subprocess.run(
        [sys.executable, "-m", "kb_pipeline", *args],
        cwd=EXTRACTOR,
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )


def test_cli_offline_run_end_to_end(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    before = _vault_hashes(vault)

    result = _run_cli(
        "run",
        "--offline",
        "--offline-input", str(cache),
        "--vault", str(vault),
        "--workspace", str(workspace),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["mode"] == "offline"
    assert payload["vault_written"] is False
    assert payload["provider_calls"] > 0
    assert payload["counters"]["error"] == 0
    assert _vault_hashes(vault) == before


def test_cli_offline_requires_vault(tmp_path: Path):
    cache = _cache_file(tmp_path)
    result = _run_cli(
        "run",
        "--offline",
        "--offline-input", str(cache),
        "--workspace", str(tmp_path / "workspace"),
    )
    assert result.returncode != 0
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert "--vault" in payload["error"]


def test_cli_run_publish_still_refused_in_offline_mode(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    before = _vault_hashes(vault)
    result = _run_cli(
        "run",
        "--offline",
        "--publish",
        "--offline-input", str(cache),
        "--vault", str(vault),
        "--workspace", str(tmp_path / "workspace"),
    )
    assert result.returncode != 0
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert "--publish" in payload["error"]
    assert _vault_hashes(vault) == before


def test_cli_run_without_offline_flag_keeps_old_parser_contract(tmp_path: Path):
    result = _run_cli("run", "--help")
    assert result.returncode == 0
    for flag in ("--handles", "--since", "--until", "--cache-dir", "--workspace", "--publish"):
        assert flag in result.stdout
    assert "--offline" in result.stdout


def test_enrich_patch_is_produced_and_publisher_gate_still_refuses_it(tmp_path: Path):
    """Integration proposes an enrich patch on a managed note; the publisher gate
    refuses to plan it while the note's frontmatter does not yet list the claim.

    That refusal is real, current behaviour of `publication.plan_publication`
    (frontmatter claim_ids must cover the patch), not a test convenience. Lifting
    it belongs to the integration/ownership package, not to this one.
    """
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "pl_raw_tweets.json").write_text(
        json.dumps(
            [{"id": "5001", "username": "u", "full_text": "Rejestruj awarie promptu przed zmiana."}],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    providers = fake_providers()
    # words are a subset of the managed note, so retrieval finds the candidate note
    claim_text = "prompt regresję od szumu"

    def claims_for(bundle, category=None):
        return [
            Claim(
                claim_id="x5001-c1",
                source_ids=[bundle.focus.source_id],
                text=claim_text,
                kind="recommendation",
                evidence=[
                    {
                        "source_id": bundle.focus.source_id,
                        "quote": "Rejestruj awarie promptu przed zmiana.",
                    }
                ],
            )
        ]

    result = _run(
        cache_dir / "pl_raw_tweets.json",
        vault,
        workspace,
        providers=FlowProviders(
            mode="fake-offline",
            local_filter=providers.local_filter,
            categorize=providers.categorize,
            jev_evaluate=providers.jev_evaluate,
            extract_claims=lambda bundle, category=None: claims_for(bundle),
            advisor=providers.advisor,
            semantic_check=providers.semantic_check,
            model_versions=providers.model_versions,
        ),
    )

    assert result["runs"][0]["status"] == "error", result["runs"][0]
    assert result["runs"][0]["stages"]["integration"] == "completed"
    assert "claim_ids" in result["runs"][0]["reason"]
    decisions = json.loads(
        (Path(result["run_dir"]) / "artifacts" / "integration_decisions.json").read_text(
            encoding="utf-8"
        )
    )["decisions"]
    patch = next(item for item in decisions if item["patch"])["patch"]
    assert patch["operation"] if "operation" in patch else True
    assert patch["base_hash"], "an enrich patch must carry the base hash of the target note"
    assert patch["relative_path"] == "Pojęcia/Fail-fast.md"
    assert patch["note_id"] == "kb-fail-fast"
    manual = vault / "Pojęcia" / "Manualna notatka.md"
    assert manual.read_text(encoding="utf-8").startswith("# Manualna notatka")


def test_artifacts_carry_no_credential_fields(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "credential-audit"
    result = _run(cache, vault, workspace)
    banned = ("api_key", "authorization", "bearer", "cookie", "password", "client_secret")
    checked = 0
    for path in Path(result["run_dir"]).rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace").casefold()
        checked += 1
        for token in banned:
            assert token not in text, f"{path.name} leaks {token}"
    assert checked >= 10


def test_published_at_is_never_replaced_with_today(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache_file(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace)
    record = json.loads(
        (Path(result["run_dir"]) / "artifacts" / "source_record.json").read_text(encoding="utf-8")
    )
    assert record["record"]["published_at"].startswith("2026-10-01T09:00:00")
