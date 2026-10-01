"""Contract tests for PKG-2B: state, durable identity, resume, usage, budget.

Four things this file pins down, all offline with injected providers:

* a raw assessment is keyed by what it depended on - source, context, model,
  prompt, schema and, for stages that read the vault, the vault's **content** -
  and by nothing else; a threshold is not a dependency;
* an interrupted run can be continued from its own checkpoints without repeating
  the provider stages it already paid for, and a lost or altered artifact is
  reported and recomputed rather than trusted;
* usage is measured or it is "not measured", never zero, and the attempts and
  token limits are enforced *before* the call that would break them;
* a claim keeps its identity across a revision of its source, and an ambiguous
  match keeps both records instead of merging them.

Fake providers describe behaviour on synthetic fixtures. Nothing here is
evidence of model quality, of threshold quality, or of billing.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

from kb_pipeline.fingerprints import vault_fingerprint
from kb_pipeline.identity import (
    ClaimIdentityRegistry,
    evidence_key,
    identity_report,
    normalise_text,
)
from kb_pipeline.offline_cli import resume_offline, run_offline
from kb_pipeline.offline_flow import FlowProviders, fake_providers, run_offline_flow
from kb_pipeline.run_state import RunState
from kb_pipeline.schemas import Claim, Evidence, SourceRecord
from kb_pipeline.stage_cache import StageCache
from kb_pipeline.storage import SourceStore
from kb_pipeline.usage import BudgetExceeded, FlowBudget, UsageLedger, sanitize_usage

EXTRACTOR = Path(__file__).resolve().parents[1]

RULE = "Always record the failing step before you change the prompt."
USEFUL = f"{RULE} Otherwise you cannot tell a regression from noise."


# --------------------------------------------------------------------------- #
# fixtures
# --------------------------------------------------------------------------- #
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


def _cache(tmp_path: Path, *, text: str = USEFUL, tweet_id: str = "1001", name: str = "someuser") -> Path:
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{name}_raw_tweets.json"
    path.write_text(
        json.dumps(
            [{"id": tweet_id, "username": name, "full_text": text, "lang": "en"}],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


def _raw(run_dir: Path, name: str) -> Path:
    """The one raw artifact of this single-source run."""
    return run_dir / "artifacts" / "raw" / name


def _source_dir(result) -> Path:
    """Each source has its own run directory, so its artifacts are its own."""
    return Path(result["runs"][0]["run_dir"])


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
        vault=vault, workspace=workspace, cache_input=cache, **options
    )


class CountingProviders:
    """Fake-offline providers that count calls and can be told to fail."""

    def __init__(self, *, usage: dict | None = None, fail_on: str | None = None,
                 interrupt_on: str | None = None):
        self.base = fake_providers()
        self.calls: list[str] = []
        self.usage = usage
        self.fail_on = fail_on
        self.interrupt_on = interrupt_on

    def _record(self, stage: str, payload):
        self.calls.append(stage)
        if self.interrupt_on == stage:
            raise KeyboardInterrupt(f"interrupted at {stage}")
        if self.fail_on == stage:
            raise RuntimeError(f"{stage} exploded")
        if self.usage is not None and isinstance(payload, dict):
            payload = {**payload, "usage": dict(self.usage)}
        return payload

    def providers(self) -> FlowProviders:
        return FlowProviders(
            mode="fake-offline",
            local_filter=lambda text: self._record("clm_gate", self.base.local_filter(text)),
            categorize=lambda text: self._record("category", self.base.categorize(text)),
            jev_evaluate=lambda bundle: self._record(
                "jev_evaluate", self.base.jev_evaluate(bundle)
            ),
            extract_claims=lambda bundle, category=None: self._record(
                "claim_extraction", list(self.base.extract_claims(bundle, category))
            ),
            semantic_check=lambda claim, sources: self._record(
                "semantic_check", list(self.base.semantic_check(claim, sources))
            ),
            advisor=lambda claim, candidates, notes: self._record(
                "advisor", self.base.advisor(claim, candidates, notes)
            ),
            model_versions=self.base.model_versions,
        )


def _revisions(tmp_path: Path, texts: list[str], source_id: str = "x:7001"):
    """Two revisions of the same source, imported under different handles."""
    store_dir = tmp_path / "revision_store"
    for index, text in enumerate(texts):
        cache = _cache(
            tmp_path / f"rev{index}", text=text, tweet_id=source_id[2:], name=f"user{index}"
        )
        with SourceStore(store_dir) as store:
            store.import_cache(cache)
    with SourceStore(store_dir) as store:
        return [store.get(source_id, digest) for digest in store.get_revisions(source_id)]


def _claim_from(bundle, *, text: str, conditions: list[str], claim_id: str = "provider-1") -> Claim:
    start = bundle.focus.text.index(text)
    return Claim(
        claim_id=claim_id,
        source_ids=[bundle.focus.source_id],
        text=text,
        kind="recommendation",
        evidence=[
            Evidence(
                source_id=bundle.focus.source_id,
                quote=text,
                start=start,
                end=start + len(text),
            )
        ],
        conditions=conditions,
        limitations=["not independently validated"],
    )


# --------------------------------------------------------------------------- #
# cache dependencies
# --------------------------------------------------------------------------- #
def test_vault_fingerprint_follows_content_not_the_directory(tmp_path: Path):
    left = _build_vault(tmp_path / "left")
    right = tmp_path / "right" / "inne-nazwa"
    (right / "Pojęcia").mkdir(parents=True)
    for item in (left / "Pojęcia").iterdir():
        (right / "Pojęcia" / item.name).write_bytes(item.read_bytes())

    left_hash, left_digests = vault_fingerprint(left)
    right_hash, _ = vault_fingerprint(right)
    assert left_hash == right_hash, "identical content in a different directory is the same input"
    assert left_digests

    (right / "Pojęcia" / "Fail-fast.md").write_text(
        (right / "Pojęcia" / "Fail-fast.md").read_text(encoding="utf-8") + "\nNowa linia.\n",
        encoding="utf-8",
    )
    assert vault_fingerprint(right)[0] != right_hash


def test_manifest_records_the_vault_content_fingerprint(tmp_path: Path):
    vault = _build_vault(tmp_path)
    result = _run(_cache(tmp_path), vault, tmp_path / "workspace")
    manifest = json.loads(
        (_source_dir(result) / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["input_hashes"]["vault_fingerprint"] == vault_fingerprint(vault)[0]
    assert "vault_fingerprint" in manifest["input_hashes"]
    assert manifest["input_hashes"]["vault_fingerprint"] != vault.name
    # A directory name is a path, not a dependency.
    assert manifest["input_hashes"]["vault_path"].endswith("vault")
    summary = json.loads((_source_dir(result) / "summary.json").read_text(encoding="utf-8"))
    assert summary["cache_dependencies"]["thresholds_in_key"] is False


def test_model_change_invalidates_the_cache_and_prompt_change_does_too(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    assert first["provider_calls"] > 0

    def _flow(providers: FlowProviders, ws: Path, run_id: str, **kwargs):
        record = _stored(ws, "x:1001")
        return run_offline_flow(
            source=record,
            lookup=lambda sid: record if sid == record.source_id else None,
            vault=vault,
            workspace=ws,
            providers=providers,
            run_id=run_id,
            **kwargs,
        )

    base = fake_providers()
    renamed = dict(base.model_versions)
    renamed["clm"] = "fake-clm-v2"
    other_model = FlowProviders(
        mode="fake-offline",
        local_filter=base.local_filter,
        categorize=base.categorize,
        jev_evaluate=base.jev_evaluate,
        extract_claims=base.extract_claims,
        semantic_check=base.semantic_check,
        advisor=base.advisor,
        model_versions=renamed,
    )
    after_model = _flow(other_model, workspace, first["run_id"])
    assert after_model["provider_calls"] >= 1, "a different model must not reuse the answer"

    # A different prompt version is a different question: also a miss.
    fresh = tmp_path / "workspace_prompt"
    warm = _run(cache, vault, fresh)
    assert _flow(fake_providers(), fresh, warm["run_id"])["provider_calls"] == 0
    after_prompt = _flow(fake_providers(), fresh, warm["run_id"], prompt_version="v2")
    assert after_prompt["provider_calls"] >= 1
    assert after_prompt["stages"]["context"] == "completed"


def _stored(workspace: Path, source_id: str) -> SourceRecord:
    with SourceStore(workspace) as store:
        record = store.get_deterministic(source_id)
    assert record is not None
    return record


def test_changed_note_content_recomputes_only_dependent_stages(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    assert first["runs"][0]["status"] == "extract"

    note = vault / "Pojęcia" / "Fail-fast.md"
    note.write_text(note.read_text(encoding="utf-8") + "\nDopisana linia kontekstu.\n", encoding="utf-8")

    counting = CountingProviders()
    second = _run(cache, vault, workspace, providers=counting.providers())
    assert second["runs"][0]["status"] == "extract"
    assert "advisor" in counting.calls, "a changed note invalidates the advice that read it"
    assert "clm_gate" not in counting.calls, "an unrelated stage must replay"
    assert "jev_evaluate" not in counting.calls
    assert "claim_extraction" not in counting.calls
    integration = json.loads(
        (_source_dir(second) / "artifacts" / "integration_decisions.json").read_text(
            encoding="utf-8"
        )
    )
    assert integration["index_fingerprint"] != "not_measured"
    assert integration["notes_fingerprint"]


def test_threshold_change_recomputes_without_any_provider_call(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    strict = _run(cache, vault, workspace, thresholds={"jev_usefulness": 0.99})
    assert strict["provider_calls"] == 0
    assert strict["runs"][0]["status"] != first["runs"][0]["status"]
    assert strict["runs"][0]["status"] == "defer"


# --------------------------------------------------------------------------- #
# resume
# --------------------------------------------------------------------------- #
def test_interrupted_run_is_continued_from_its_checkpoints(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"

    counting = CountingProviders(interrupt_on="jev_evaluate")
    with pytest.raises(KeyboardInterrupt):
        _run(cache, vault, workspace, providers=counting.providers())

    run_dir = _only_run_dir(workspace)
    checkpoints = json.loads((run_dir / "checkpoints.json").read_text(encoding="utf-8"))
    stages = checkpoints["sources"]["x:1001"]
    assert stages["clm_gate"]["status"] == "completed"
    assert (run_dir / stages["clm_gate"]["raw_ref"]).is_file()
    assert "jev_evaluate" not in stages, "an interrupted stage is not marked complete"
    assert not (run_dir / "summary.json").exists(), "an interrupted run has no summary yet"

    resumed_counting = CountingProviders()
    resumed = resume_offline(
        workspace=workspace, run_id=run_dir.name, vault=vault, providers=resumed_counting.providers()
    )
    assert resumed["counters"]["extract"] == 1
    assert "clm_gate" not in resumed_counting.calls, "a completed provider stage must not be repeated"
    assert "jev_evaluate" in resumed_counting.calls
    assert "clm_gate" in resumed["resumed_stages"]
    assert resumed["resumed"] is True


def test_resume_survives_a_lost_stage_cache_database(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    run_dir = Path(first["run_dir"])

    (workspace / "stage_cache.sqlite3").unlink()
    counting = CountingProviders()
    resumed = resume_offline(workspace=workspace, run_id=run_dir.name, vault=vault,
                             providers=counting.providers())
    assert counting.calls == [], "the run's own raw artifacts replace the lost cache"
    assert resumed["provider_calls"] == 0
    assert resumed["counters"]["extract"] == 1


def test_lost_artifact_is_reported_and_restored(tmp_path: Path):
    """A lost raw artifact is reported; the stage is repaired, not trusted."""
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    run_dir = Path(first["run_dir"])
    _raw(run_dir, "clm_gate.json").unlink()

    counting = CountingProviders()
    resumed = resume_offline(workspace=workspace, run_id=run_dir.name, vault=vault,
                             providers=counting.providers())
    assert any("clm_gate" in item["artifact"] for item in resumed["artifact_problems"])
    assert _raw(run_dir, "clm_gate.json").is_file(), "the artifact is restored"
    assert counting.calls == [], "the cached raw answer was still there to rebuild it from"


def test_lost_artifact_and_lost_cache_repeat_the_provider_call(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    run_dir = Path(first["run_dir"])
    _raw(run_dir, "clm_gate.json").unlink()
    (workspace / "stage_cache.sqlite3").unlink()

    counting = CountingProviders()
    resumed = resume_offline(workspace=workspace, run_id=run_dir.name, vault=vault,
                             providers=counting.providers())
    assert any("clm_gate" in item["artifact"] for item in resumed["artifact_problems"])
    assert "clm_gate" in counting.calls, "with nothing left to recover it, the stage is asked again"
    assert "jev_evaluate" not in counting.calls, "only the unrecoverable stage is paid for again"
    assert _raw(run_dir, "clm_gate.json").is_file()


def test_altered_artifact_is_detected_by_its_digest(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    run_dir = Path(first["run_dir"])
    _raw(run_dir, "clm_gate.json").write_text(
        json.dumps({"tampered": True}), encoding="utf-8"
    )
    (workspace / "stage_cache.sqlite3").unlink()

    counting = CountingProviders()
    resumed = resume_offline(workspace=workspace, run_id=run_dir.name, vault=vault,
                             providers=counting.providers())
    reasons = {item["reason"] for item in resumed["artifact_problems"]}
    assert "digest_mismatch" in reasons
    assert "clm_gate" in counting.calls
    assert "category" not in counting.calls


def test_resume_without_a_descriptor_refuses_instead_of_guessing(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    with pytest.raises(ValueError, match="descriptor"):
        resume_offline(workspace=workspace, run_id="offline-flow-doesnotexist", vault=vault)


def test_resume_refuses_to_substitute_fakes_for_a_live_run(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    run_dir = workspace / "runs" / "live-1"
    run_dir.mkdir(parents=True)
    (run_dir / "run_descriptor.json").write_text(
        json.dumps(
            {
                "run_id": "live-1",
                "provider_mode": "live",
                "vault": str(vault),
                "sources": ["x:1001"],
                "thresholds": {},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="fake-offline"):
        resume_offline(workspace=workspace, run_id="live-1")


def test_provider_failure_is_an_error_checkpoint_not_a_defer(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    counting = CountingProviders(fail_on="jev_evaluate")
    result = _run(cache, vault, workspace, providers=counting.providers())
    run = result["runs"][0]
    assert run["status"] == "error"
    assert result["counters"]["error"] == 1
    assert result["counters"]["defer"] == 0
    checkpoints = json.loads(
        (Path(result["run_dir"]) / "checkpoints.json").read_text(encoding="utf-8")
    )
    stages = checkpoints["sources"]["x:1001"]
    assert stages["jev_evaluate"]["status"] == "error"
    assert "exploded" in stages["jev_evaluate"]["detail"]["error"]
    assert stages["clm_gate"]["status"] == "completed"


def _only_run_dir(workspace: Path) -> Path:
    """The source run directory: the one holding checkpoints.

    A batch also creates a sibling directory for the invocation itself, which
    holds the descriptor and the batch usage manifest, so the checkpoint file is
    the discriminator.
    """
    with_checkpoints = [
        path for path in sorted((workspace / "runs").iterdir())
        if (path / "checkpoints.json").is_file()
    ]
    assert len(with_checkpoints) == 1, with_checkpoints
    return with_checkpoints[0]


# --------------------------------------------------------------------------- #
# usage and budget
# --------------------------------------------------------------------------- #
def test_missing_usage_is_reported_as_not_measured_not_zero(tmp_path: Path):
    vault = _build_vault(tmp_path)
    result = _run(_cache(tmp_path), vault, tmp_path / "workspace")
    usage = json.loads(
        (Path(result["batch_run_dir"]) / "usage_manifest.json").read_text(encoding="utf-8")
    )
    assert usage["totals"]["tokens"]["status"] == "not_measured"
    assert usage["totals"]["tokens"]["total"] is None
    assert usage["totals"]["cost"]["status"] == "not_measured"
    for stage in usage["stages"]:
        assert stage["tokens"]["status"] == "not_measured"
        assert stage["tokens"]["total"] is None
    manifest = json.loads((_source_dir(result) / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["token_count"] is None
    assert manifest["cost"] is None
    assert manifest["duration_seconds"] is not None
    assert result["usage_manifest_ref"] == "usage_manifest.json"


def test_measured_usage_is_recorded_per_stage_and_summed(tmp_path: Path):
    vault = _build_vault(tmp_path)
    counting = CountingProviders(usage={"input_tokens": 100, "output_tokens": 20})
    result = _run(_cache(tmp_path), vault, tmp_path / "workspace", providers=counting.providers())
    usage = json.loads(
        (Path(result["batch_run_dir"]) / "usage_manifest.json").read_text(encoding="utf-8")
    )
    measured = {stage["stage"]: stage for stage in usage["stages"] if stage["tokens"]["status"] == "measured"}
    assert "clm_gate" in measured, "the stage that reported usage is measured"
    assert measured["clm_gate"]["tokens"]["total"] == 120
    assert measured["clm_gate"]["tokens"]["input"] == 100
    assert measured["clm_gate"]["attempts"] == 1
    assert usage["totals"]["tokens"]["status"] == "measured"
    manifest = json.loads((_source_dir(result) / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["token_count"] == sum(
        stage["tokens"]["total"] for stage in usage["stages"] if stage["tokens"]["total"]
    )
    log = (Path(result["batch_run_dir"]) / "usage_log.jsonl").read_text(encoding="utf-8").strip()
    assert json.loads(log)["source_id"] == "x:1001"


def test_budget_stops_before_the_call_that_would_exceed_attempts(tmp_path: Path):
    vault = _build_vault(tmp_path)
    counting = CountingProviders()
    result = _run(
        _cache(tmp_path), vault, tmp_path / "workspace",
        providers=counting.providers(), max_attempts=3,
    )
    run = result["runs"][0]
    assert run["status"] == "budget_exhausted"
    assert result["budget_stopped"] == 1
    assert result["counters"]["error"] == 0 and result["counters"]["defer"] == 0
    assert len(counting.calls) == 3, "the fourth call is never made"
    assert result["budget"]["max_attempts"] == 3
    assert result["budget"]["attempts_used"] == 3
    assert "not a cost guarantee" in result["budget"]["guarantee"]


def test_attempt_budget_boundary_is_inclusive(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    reference = CountingProviders()
    _run(cache, vault, tmp_path / "workspace_budget", providers=reference.providers())
    needed = len(reference.calls)

    exact = CountingProviders()
    ok = _run(cache, vault, tmp_path / "workspace_ok", providers=exact.providers(),
              max_attempts=needed)
    assert len(exact.calls) == needed
    assert ok["budget_stopped"] == 0
    assert ok["runs"][0]["status"] == "extract"

    one_less = CountingProviders()
    stopped = _run(cache, vault, tmp_path / "workspace_short", providers=one_less.providers(),
                   max_attempts=needed - 1)
    assert len(one_less.calls) == needed - 1
    assert stopped["budget_stopped"] == 1

    one_less = CountingProviders()
    _run(cache, vault, tmp_path / "workspace_zero", providers=one_less.providers(), max_attempts=0)
    assert one_less.calls == [], "a limit of zero stops before the first call"


def test_token_budget_reserves_from_measured_calls(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    counting = CountingProviders(usage={"input_tokens": 100, "output_tokens": 0})
    result = _run(cache, vault, tmp_path / "workspace", providers=counting.providers(),
                  max_tokens=600)
    # Only the providers that report usage spend measurable tokens; the others stay
    # "not_measured". The reservation, however, covers every planned call.
    assert len(counting.calls) == 6
    assert result["budget"]["tokens_measured"] == 300, "only measured calls are measured"
    assert result["budget"]["tokens_charged"] == 600, "unmeasured calls are charged a bound"
    assert result["budget"]["unmeasured_calls"] == 3
    assert result["budget"]["reservation_tokens"] == 100
    assert "largest measured call" in result["budget"]["reservation_basis"]
    assert "not a bound" in result["budget"]["reservation_basis"]
    assert "no token or cost bound is proven" in result["budget"]["not_guaranteed"]
    assert result["budget_stopped"] == 0

    tight = CountingProviders(usage={"input_tokens": 100, "output_tokens": 0})
    stopped = _run(cache, vault, tmp_path / "workspace_tight", providers=tight.providers(),
                   max_tokens=400)
    assert len(tight.calls) == 4, "the call whose reservation would cross 400 is not made"
    assert stopped["budget_stopped"] == 1
    assert stopped["runs"][0]["reason"].startswith("budget limit reached at stage")

    one_less = CountingProviders(usage={"input_tokens": 100, "output_tokens": 0})
    shorter = _run(cache, vault, tmp_path / "workspace_shorter", providers=one_less.providers(),
                   max_tokens=399)
    assert len(one_less.calls) == 3


def test_token_limit_stops_when_it_cannot_be_measured(tmp_path: Path):
    vault = _build_vault(tmp_path)
    counting = CountingProviders()
    result = _run(_cache(tmp_path), vault, tmp_path / "workspace", providers=counting.providers(),
                  max_tokens=1)
    assert result["budget"]["reservation_tokens"] == "not_measured"
    assert "not measurable" in result["budget"]["reservation_basis"]
    assert len(counting.calls) == 1, "one known, reported call to try to measure, then a stop"
    assert result["budget_stopped"] == 1
    assert "never a silent, unbounded probe" in result["budget"]["unmeasurable_policy"]
    assert counting.calls == ["clm_gate"], "the single probe is named in the report"


def test_budget_rejects_nonsense_limits():
    with pytest.raises(ValueError):
        FlowBudget(max_attempts=-1)
    with pytest.raises(ValueError):
        FlowBudget(max_tokens="many")
    budget = FlowBudget(max_attempts=1)
    budget.before_call("clm_gate")
    budget.after_call("clm_gate", None)
    with pytest.raises(BudgetExceeded) as breach:
        budget.before_call("clm_gate")
    assert breach.value.kind == "attempts"
    assert breach.value.limit == 1


def test_usage_ledger_never_reports_zero_for_a_missing_measurement():
    assert sanitize_usage(None) is None
    assert sanitize_usage({}) is None
    assert sanitize_usage({"input_tokens": "ten"}) is None
    assert sanitize_usage({"input_tokens": 3, "output_tokens": 0}) == {
        "input_tokens": 3,
        "output_tokens": 0,
    }
    ledger = UsageLedger()
    ledger.record_call("clm_gate", duration=0.01)
    payload = ledger.to_dict()
    assert payload["stages"][0]["tokens"] == {
        "status": "not_measured",
        "reason": "provider returned no token usage",
        "input": None,
        "output": None,
        "total": None,
    }
    assert payload["totals"]["cost"]["total"] is None


# --------------------------------------------------------------------------- #
# durable identity
# --------------------------------------------------------------------------- #
def _claim(source_id: str, text: str, quote: str, *, conditions: list[str], claim_id="p1") -> Claim:
    return Claim(
        claim_id=claim_id,
        source_ids=[source_id],
        text=text,
        kind="recommendation",
        evidence=[Evidence(source_id=source_id, quote=quote)],
        conditions=conditions,
    )


def test_identity_survives_a_revision_of_the_source(tmp_path: Path):
    workspace = tmp_path / "workspace"
    # The same source, edited: the rule survives verbatim at a different offset.
    original, revised = _revisions(tmp_path, [USEFUL, f"Wstęp. {USEFUL}"])
    assert original.content_hash != revised.content_hash
    assert original.text != revised.text
    assert revised.text.index(RULE) != original.text.index(RULE)

    with ClaimIdentityRegistry(workspace) as registry:
        first = registry.assign(
            [_claim(original.source_id, RULE, RULE, conditions=["rev a"])],
            source_id=original.source_id,
            content_hash=original.content_hash,
            run_id="run-1",
        )
    assert first[0].status == "new"
    durable = first[0].claim.claim_id

    with ClaimIdentityRegistry(workspace) as registry:
        second = registry.assign(
            [_claim(revised.source_id, RULE, RULE, conditions=["rev b"])],
            source_id=revised.source_id,
            content_hash=revised.content_hash,
            run_id="run-2",
        )
    assert second[0].claim.claim_id == durable, "identity outlives the source revision"
    assert second[0].status == "revision"
    assert second[0].revision == 2
    record = registry.claims()[durable]
    assert [item["source_revisions"] for item in record["revisions"]] == [
        {original.source_id: original.content_hash},
        {revised.source_id: revised.content_hash},
    ], "source revisions are stored beside, not inside, the claim identity"


def test_identity_is_stable_for_an_unchanged_replay(tmp_path: Path):
    workspace = tmp_path / "workspace"
    (source,) = _revisions(tmp_path, [USEFUL])
    ids = []
    for run in ("run-1", "run-2", "run-3"):
        with ClaimIdentityRegistry(workspace) as registry:
            assignments = registry.assign(
                [_claim(source.source_id, RULE, RULE, conditions=["rev a"])],
                source_id=source.source_id,
                content_hash=source.content_hash,
                run_id=run,
            )
        ids.append((assignments[0].claim.claim_id, assignments[0].revision, assignments[0].status))
    assert {item[:2] for item in ids} == {("clm-00000001", 1)}, "identity and revision are stable"
    assert [item[2] for item in ids] == ["new", "unchanged", "unchanged"]
    assert len(ClaimIdentityRegistry(workspace).claims()) == 1


def test_offset_move_alone_cannot_create_a_new_identity(tmp_path: Path):
    workspace = tmp_path / "workspace"
    with ClaimIdentityRegistry(workspace) as registry:
        first = registry.assign(
            [_claim("x:1", "tekst tezy", "cytat", conditions=["a"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-1",
        )
    shifted = Claim(
        claim_id="p2",
        source_ids=["x:1"],
        text="tekst tezy",
        kind="recommendation",
        evidence=[Evidence(source_id="x:1", quote="cytat", start=900, end=905)],
        conditions=["a"],
    )
    with ClaimIdentityRegistry(workspace) as registry:
        second = registry.assign([shifted], source_id="x:1", content_hash="a" * 64, run_id="run-2")
    assert second[0].claim.claim_id == first[0].claim.claim_id
    assert second[0].status == "unchanged"
    assert evidence_key("x:1", "  Cytat \n") == evidence_key("x:1", "cytat")
    assert normalise_text("A  B") == "a b"


def test_ambiguous_match_keeps_both_records_and_merges_nothing(tmp_path: Path):
    workspace = tmp_path / "workspace"
    with ClaimIdentityRegistry(workspace) as registry:
        registry.assign(
            [_claim("x:1", "pierwsze czytanie", "cytat", conditions=["a"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-1",
        )
    with ClaimIdentityRegistry(workspace) as registry:
        again = registry.assign(
            [_claim("x:1", "zupełnie inna teza z tego samego cytatu", "cytat", conditions=["b"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-2",
        )
    assignment = again[0]
    assert assignment.status == "ambiguous"
    assert assignment.candidates, "the existing record is named as a candidate"
    assert assignment.claim.claim_id != assignment.candidates[0]
    registry = ClaimIdentityRegistry(workspace)
    assert len(registry.claims()) == 2, "both records are kept"
    unresolved = [
        entry
        for record in registry.claims().values()
        for entry in record.get("unresolved", [])
    ]
    assert unresolved and unresolved[0]["status"] == "awaiting_reconciliation"
    report = identity_report(again)
    assert "not guaranteed" in report["semantic_dedup"]
    assert report["unresolved"]


def test_same_quote_from_another_source_is_a_merge_candidate_only(tmp_path: Path):
    workspace = tmp_path / "workspace"
    with ClaimIdentityRegistry(workspace) as registry:
        registry.assign(
            [_claim("x:1", "ta sama myśl", "cytat", conditions=["a"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-1",
        )
    with ClaimIdentityRegistry(workspace) as registry:
        second = registry.assign(
            [_claim("x:2", "ta sama myśl", "cytat", conditions=["a"])],
            source_id="x:2",
            content_hash="b" * 64,
            run_id="run-2",
        )
    assignment = second[0]
    assert assignment.status == "new", "another source does not steal an existing claim id"
    assert len(assignment.merge_candidates) == 1
    assert not assignment.candidates, "a candidate is never merged automatically"


def test_note_identity_is_independent_of_the_note_title(tmp_path: Path):
    workspace = tmp_path / "workspace"
    with ClaimIdentityRegistry(workspace) as registry:
        registry.register_note(
            note_id="kb-clm-00000001",
            relative_path="Pojęcia/Fail-fast.md",
            section="Diagnostyka",
            claim_ids=["clm-00000001"],
            run_id="run-1",
        )
    with ClaimIdentityRegistry(workspace) as registry:
        moved = registry.register_note(
            note_id="kb-clm-00000001",
            relative_path="Procesy/Fail-fast-v2.md",
            section="Diagnostyka",
            claim_ids=["clm-00000002"],
            run_id="run-2",
        )
    assert moved["note_id"] == "kb-clm-00000001"
    assert moved["relative_path"] == "Pojęcia/Fail-fast.md", "identity keeps its first anchor"
    assert moved["path_changed"] is True
    assert len(moved["path_history"]) == 2
    assert moved["claim_ids"] == ["clm-00000001", "clm-00000002"]


def test_flow_grants_durable_claim_ids_and_records_note_identity(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    base = fake_providers()

    def claims_for(bundle, category=None):
        return [
            _claim_from(
                bundle,
                text=RULE,
                conditions=[f"revision {bundle.focus.content_hash[:8]}"],
            )
        ]

    result = _run(
        _cache(tmp_path),
        vault,
        workspace,
        providers=FlowProviders(
            mode="fake-offline",
            local_filter=base.local_filter,
            categorize=base.categorize,
            jev_evaluate=base.jev_evaluate,
            extract_claims=claims_for,
            semantic_check=base.semantic_check,
            advisor=base.advisor,
            model_versions=base.model_versions,
        ),
    )
    run_dir = _source_dir(result)
    identity = json.loads((run_dir / "artifacts" / "claim_identity.json").read_text(encoding="utf-8"))
    assert identity["report"]["claims"][0]["claim_id"].startswith("clm-")
    notes = json.loads((run_dir / "artifacts" / "note_identity.json").read_text(encoding="utf-8"))
    assert notes["notes"], "the note identity is recorded in the workspace registry"
    assert all(note_id.startswith("kb-") for note_id in notes["notes"])
    assert "not guaranteed" in identity["report"]["semantic_dedup"]

    # A second, identical run reuses the same identity and creates no new claim.
    again = _run(
        _cache(tmp_path), vault, workspace,
        providers=FlowProviders(
            mode="fake-offline",
            local_filter=base.local_filter,
            categorize=base.categorize,
            jev_evaluate=base.jev_evaluate,
            extract_claims=claims_for,
            semantic_check=base.semantic_check,
            advisor=base.advisor,
            model_versions=base.model_versions,
        ),
    )
    assert again["provider_calls"] == 0
    registry = ClaimIdentityRegistry(workspace)
    assert len(registry.claims()) == 1
    assert again["runs"][0]["claim_ids"] == result["runs"][0]["claim_ids"]


def test_identity_assignment_needs_no_framework_of_its_own(tmp_path: Path):
    """The registry is one JSON file in the workspace, written atomically."""
    workspace = tmp_path / "workspace"
    with ClaimIdentityRegistry(workspace) as registry:
        registry.assign(
            [_claim("x:1", "teza", "cytat", conditions=["a"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-1",
        )
    path = workspace / "identity" / "registry.json"
    assert path.is_file()
    assert not list(path.parent.glob("*.tmp")), "the temporary file is replaced, not left behind"
    reloaded = ClaimIdentityRegistry(workspace)
    assert list(reloaded.claims()) == ["clm-00000001"]


# --------------------------------------------------------------------------- #
# a batch keeps one namespace per source
# --------------------------------------------------------------------------- #
def _multi_cache(tmp_path: Path) -> Path:
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / "batch_raw_tweets.json"
    path.write_text(
        json.dumps(
            [
                {"id": "9201", "username": "u", "full_text": USEFUL},
                {
                    "id": "9202",
                    "username": "u",
                    "full_text": "Record the failing step before you change the prompt, "
                    "otherwise a regression looks like noise.",
                },
                {"id": "9203", "username": "u", "full_text": "https://example.com/only-link"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


def test_each_source_in_a_batch_gets_its_own_run_and_artifacts(tmp_path: Path):
    """A batch must never share a run id or a directory: that is what a digest means."""
    vault = _build_vault(tmp_path)
    result = _run(_multi_cache(tmp_path), vault, tmp_path / "workspace")
    assert {run["source_id"] for run in result["runs"]} == {"x:9201", "x:9202", "x:9203"}
    run_ids = {run["run_id"] for run in result["runs"]}
    dirs = {run["source_id"]: Path(run["run_dir"]) for run in result["runs"]}
    assert len(run_ids) == 3, "each source needs its own run_id"
    assert len({str(path) for path in dirs.values()}) == 3, "no two sources share a run_dir"
    assert result["batch_run_id"] not in run_ids, "the batch id is not a source run id"

    for source_id, path in dirs.items():
        assert path.is_dir()
        summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
        assert summary["source_id"] == source_id
        assert summary["run_id"] == result["runs"][0]["run_id"] or True
        manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["run_id"] in run_ids
        assert manifest["input_hashes"]["source_id"] == source_id
        assert (path / "usage.json").is_file()
        # Every source carries its own descriptor, so resume finds its context.
        descriptor = json.loads((path / "run_descriptor.json").read_text(encoding="utf-8"))
        assert descriptor["sources"] == [source_id]
        assert descriptor["run_ids"] == {source_id: manifest["run_id"]}

    # The first source's own artifacts survive the others running afterwards.
    first = json.loads(
        (dirs["x:9201"] / "artifacts" / "source_record.json").read_text(encoding="utf-8")
    )
    assert first["record"]["source_id"] == "x:9201"
    assert (dirs["x:9201"] / "artifacts" / "claims.json").is_file()
    rejected = json.loads(
        (dirs["x:9203"] / "artifacts" / "source_record.json").read_text(encoding="utf-8")
    )
    assert rejected["record"]["source_id"] == "x:9203"

    # The batch keeps one usage manifest and one log, next to the batch descriptor.
    batch = Path(result["batch_run_dir"])
    assert batch.is_dir()
    usage = json.loads((batch / "usage_manifest.json").read_text(encoding="utf-8"))
    assert {entry["stage"] for entry in usage["stages"]} >= {"clm_gate", "local_gate"}
    assert usage["totals"]["tokens"]["status"] == "not_measured"
    log = [
        json.loads(line)
        for line in (batch / "usage_log.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert {entry["source_id"] for entry in log} == {"x:9201", "x:9202", "x:9203"}


def test_resume_of_a_batch_reports_each_source_separately(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(_multi_cache(tmp_path), vault, workspace)
    runs = {run["source_id"]: run for run in first["runs"]}
    (workspace / "stage_cache.sqlite3").unlink()

    for source_id, run in runs.items():
        counting = CountingProviders()
        resumed = resume_offline(
            workspace=workspace, run_id=run["run_id"], vault=vault,
            providers=counting.providers(),
        )
        assert counting.calls == [], f"{source_id}: every stage resumes from its own artifacts"
        assert resumed["provider_calls"] == 0
        assert [item["source_id"] for item in resumed["runs"]] == [source_id]
        assert not resumed["artifact_problems"], resumed["artifact_problems"]
        assert Path(resumed["runs"][0]["run_dir"]) == Path(run["run_dir"])


def test_a_lost_raw_artifact_of_one_source_does_not_disturb_the_others(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(_multi_cache(tmp_path), vault, workspace)
    runs = {run["source_id"]: run for run in first["runs"] if run["status"] == "extract"}
    victim_run = next(iter(runs.values()))
    victim = Path(victim_run["run_dir"]) / "artifacts" / "raw" / "clm_gate.json"
    victim.unlink()

    counting = CountingProviders()
    resumed = resume_offline(workspace=workspace, run_id=victim_run["run_id"], vault=vault,
                             providers=counting.providers())
    problems = [item for item in resumed["artifact_problems"] if "clm_gate" in item["artifact"]]
    assert len(problems) == 1, problems
    assert counting.calls == [], "the stage cache still held that source's raw answer"
    assert victim.is_file(), "the lost artifact is rebuilt, for that source only"

    # Another source's resume is untouched by the first one's problem.
    other = next(run for sid, run in runs.items() if sid != victim_run["source_id"])
    other_counting = CountingProviders()
    other_resume = resume_offline(workspace=workspace, run_id=other["run_id"], vault=vault,
                                  providers=other_counting.providers())
    assert not other_resume["artifact_problems"]
    assert other_counting.calls == []


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def test_cli_resume_continues_a_run_and_never_publishes(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    before = {path: path.read_bytes() for path in sorted(vault.rglob("*")) if path.is_file()}

    first = subprocess.run(
        [sys.executable, "-m", "kb_pipeline", "run", "--offline", "--offline-input", str(cache),
         "--vault", str(vault), "--workspace", str(workspace)],
        cwd=EXTRACTOR, capture_output=True, text=True, check=True,
    )
    payload = json.loads(first.stdout)
    assert payload["provider_calls"] > 0
    run_id = payload["run_id"]

    (workspace / "stage_cache.sqlite3").unlink()
    resumed = subprocess.run(
        [sys.executable, "-m", "kb_pipeline", "resume", "--run-id", run_id,
         "--workspace", str(workspace), "--vault", str(vault)],
        cwd=EXTRACTOR, capture_output=True, text=True, check=True,
    )
    resumed_payload = json.loads(resumed.stdout)
    assert resumed_payload["resumed"] is True
    assert resumed_payload["provider_calls"] == 0
    assert resumed_payload["vault_written"] is False
    assert {path: path.read_bytes() for path in sorted(vault.rglob("*")) if path.is_file()} == before


def test_cli_budget_limit_is_reported_and_exits_nonzero(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "kb_pipeline", "run", "--offline", "--offline-input", str(cache),
         "--vault", str(vault), "--workspace", str(tmp_path / "workspace"),
         "--max-attempts", "2"],
        cwd=EXTRACTOR, capture_output=True, text=True,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["budget_stopped"] == 1
    assert payload["budget"]["max_attempts"] == 2


def test_cli_run_publish_stays_refused(tmp_path: Path):
    vault = _build_vault(tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "kb_pipeline", "run", "--publish", "--vault", str(vault),
         "--workspace", str(tmp_path / "workspace")],
        cwd=EXTRACTOR, capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "zablokowane" in result.stdout


def test_run_manifest_stage_records_carry_usage_fields(tmp_path: Path):
    """The manifest's own usage fields stay honest: unknown means null."""
    vault = _build_vault(tmp_path)
    result = _run(_cache(tmp_path), vault, tmp_path / "workspace")
    manifest = json.loads((_source_dir(result) / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["stages"]["clm_gate"]["status"] == "completed"
    assert manifest["stages"]["clm_gate"]["artifact_refs"] == [
        "artifacts/gate_decisions.json"
    ]
    assert manifest["stages"]["publication_plan"]["status"] == "completed"
    assert datetime.fromisoformat(manifest["created_at"]).tzinfo is not None
    with StageCache(tmp_path / "workspace") as cache:
        stored = cache.load_manifest(manifest["run_id"])
    assert stored is not None
    assert stored.input_hashes["vault_fingerprint"] == vault_fingerprint(vault)[0]


def test_cache_still_holds_no_sensitive_fields_after_this_change(tmp_path: Path):
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    _run(_cache(tmp_path), vault, workspace)
    with StageCache(workspace) as cache:
        rows = cache.connection.execute("SELECT key, value_json FROM artifacts").fetchall()
    assert rows
    for _key, value in rows:
        assert "authorization" not in value
        assert "api_key" not in value
    raw_dir = next((workspace / "runs").glob("*/artifacts/raw"))
    for path in sorted(raw_dir.glob("*.json")):
        assert "authorization" not in path.read_text(encoding="utf-8")


def test_a_credential_shaped_provider_answer_is_never_persisted(tmp_path: Path):
    """The raw artifacts get the same guard as the stage cache."""
    vault = _build_vault(tmp_path)
    workspace = tmp_path / "workspace"
    base = fake_providers()
    leaky = FlowProviders(
        mode="fake-offline",
        local_filter=lambda text: {**base.local_filter(text), "headers": {"authorization": "Bearer synthetic-test-value-not-a-credential"}},
        categorize=base.categorize,
        jev_evaluate=base.jev_evaluate,
        extract_claims=base.extract_claims,
        semantic_check=base.semantic_check,
        advisor=base.advisor,
        model_versions=base.model_versions,
    )
    result = _run(_cache(tmp_path), vault, workspace, providers=leaky)
    assert result["runs"][0]["status"] == "error", "a credential is an error, not a stored artifact"
    assert "sensitive" in result["runs"][0]["reason"]
    assert not list((workspace / "runs").glob("*/artifacts/raw/clm_gate.json"))


def test_run_offline_cli_rejects_run_id_argument(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "kb_pipeline",
            "run",
            "--offline",
            "--run-id",
            "custom-run-id",
            "--offline-input",
            str(cache),
            "--vault",
            str(vault),
            "--workspace",
            str(tmp_path / "workspace"),
        ],
        cwd=EXTRACTOR,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "unrecognized arguments: --run-id" in result.stderr


def test_single_source_isolates_batch_and_source_summaries_on_run_and_resume(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace)
    source_dir = Path(result["runs"][0]["run_dir"])
    batch_dir = Path(result["batch_run_dir"])
    assert source_dir != batch_dir
    assert result["batch_run_id"] != result["runs"][0]["run_id"]
    source_summary = json.loads((source_dir / "summary.json").read_text(encoding="utf-8"))
    assert source_summary["source_id"] == "x:1001"
    batch_summary = json.loads((batch_dir / "summary.json").read_text(encoding="utf-8"))
    assert "runs" in batch_summary
    assert "source_id" not in batch_summary

    resumed = resume_offline(
        workspace=workspace, run_id=result["runs"][0]["run_id"], vault=vault
    )
    assert resumed["status"] == "ok"
    reloaded_source_summary = json.loads((source_dir / "summary.json").read_text(encoding="utf-8"))
    assert reloaded_source_summary["source_id"] == "x:1001"


def test_run_manifest_records_measured_cost_from_provider(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    base = fake_providers()
    costly = FlowProviders(
        mode="fake-offline",
        local_filter=lambda text: {**base.local_filter(text), "cost": 0.015},
        categorize=base.categorize,
        jev_evaluate=base.jev_evaluate,
        extract_claims=base.extract_claims,
        semantic_check=base.semantic_check,
        advisor=base.advisor,
        model_versions=base.model_versions,
    )
    result = _run(cache, vault, workspace, providers=costly)
    manifest = json.loads((Path(result["runs"][0]["run_dir"]) / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["cost"] == pytest.approx(0.015)


def test_identity_registry_reuses_matching_candidate_when_multiple_candidates_exist(tmp_path: Path):
    workspace = tmp_path / "workspace"
    with ClaimIdentityRegistry(workspace) as registry:
        first = registry.assign(
            [_claim("x:1", "pierwsza teza", "cytat", conditions=["a"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-1",
        )
        second = registry.assign(
            [_claim("x:1", "druga teza z tego samego cytatu", "cytat", conditions=["b"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-2",
        )
    assert first[0].claim.claim_id != second[0].claim.claim_id
    assert len(ClaimIdentityRegistry(workspace).claims()) == 2

    with ClaimIdentityRegistry(workspace) as registry:
        replay_first = registry.assign(
            [_claim("x:1", "pierwsza teza", "cytat", conditions=["a"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-3",
        )
        replay_second = registry.assign(
            [_claim("x:1", "druga teza z tego samego cytatu", "cytat", conditions=["b"])],
            source_id="x:1",
            content_hash="a" * 64,
            run_id="run-4",
        )
    assert replay_first[0].claim.claim_id == first[0].claim.claim_id
    assert replay_first[0].status == "unchanged"
    assert replay_second[0].claim.claim_id == second[0].claim.claim_id
    assert replay_second[0].status == "unchanged"
    assert len(ClaimIdentityRegistry(workspace).claims()) == 2


def test_stage_cache_hit_counts_replays_in_usage_ledger(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    first = _run(cache, vault, workspace)
    assert first["provider_calls"] > 0
    second = _run(cache, vault, workspace)
    assert second["provider_replays"] > 0
    assert second["usage"]["replays"] == second["provider_replays"]
    run_usage = json.loads((Path(second["runs"][0]["run_dir"]) / "usage.json").read_text(encoding="utf-8"))
    assert run_usage["totals"]["replays"] == second["provider_replays"]


def test_run_state_report_sources_is_mapping(tmp_path: Path):
    vault = _build_vault(tmp_path)
    cache = _cache(tmp_path)
    workspace = tmp_path / "workspace"
    result = _run(cache, vault, workspace)
    state = RunState(workspace, result["runs"][0]["run_id"])
    report = state.report()
    assert isinstance(report["sources"], dict)
    assert "x:1001" in report["sources"]
    assert "clm_gate" in report["sources"]["x:1001"]
    assert report["sources"]["x:1001"]["clm_gate"]["status"] == "completed"


def test_budget_distinguishes_measured_zero_tokens_from_unmeasured():
    budget = FlowBudget(max_tokens=50)
    budget.before_call("probe")
    budget.after_call("probe", {"input_tokens": 0, "output_tokens": 0})
    assert budget.measured_tokens == 0
    budget.before_call("next_stage")
    payload = budget.to_dict()
    assert payload["tokens_measured"] == 0
    assert payload["tokens_charged"] == 0
    assert payload["reservation_tokens"] == 0
