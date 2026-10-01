from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

from kb_pipeline import clm_source, fetch_x
from kb_pipeline.apify_x import build_query
from kb_pipeline.fetch_x import parse_accounts, run_fetch

EXTRACTOR = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 10, 2, 10, 0, tzinfo=timezone.utc)


class FakeFetch:
    def __init__(self, data=None, fail=()):
        self.data = data or {}
        self.fail = set(fail)
        self.calls: list[dict] = []

    def __call__(self, handle, *, since, until, limit):
        self.calls.append({"handle": handle, "since": since, "until": until, "limit": limit})
        if handle in self.fail:
            raise RuntimeError("Apify padl, token=sekret-token-123")
        return [dict(item) for item in self.data.get(handle, [])]


def tweets(*ids):
    return [{"id": str(i), "text": f"t{i}", "created_at": "Sun Sep 20 12:05:11 +0000 2026"} for i in ids]


def fetch(tmp_path, fake, handles=("alice", "bob"), **kwargs):
    return run_fetch(handles=list(handles), workspace=tmp_path / "ws", fetch_fn=fake, now=NOW, **kwargs)


def test_parse_accounts_ignores_comments_blanks_at_and_duplicates(tmp_path):
    path = tmp_path / "accounts.txt"
    path.write_text("# lista\nalice\n\n@Bob  # trailing\n  \nALICE\n", encoding="utf-8")
    assert parse_accounts(path) == ["alice", "Bob"]


def test_repo_accounts_file_lists_requested_handles():
    assert parse_accounts(EXTRACTOR / "accounts.txt") == [
        "karminski3", "HamelHusain", "kunchenguid", "DrJimFan", "JustinLin610",
    ]


def test_build_query_matches_fetch_account_format():
    assert build_query("@alice", "2026-09-01", "2026-10-01") == "from:alice since:2026-09-01 until:2026-10-01"
    assert build_query("alice", None, None) == "from:alice"


def test_multiple_accounts_write_one_raw_file_each_and_report_counts(tmp_path):
    fake = FakeFetch({"alice": tweets(1, 2), "bob": tweets(3)})
    report = fetch(tmp_path, fake)
    assert [c["handle"] for c in fake.calls] == ["alice", "bob"]
    assert report["accounts"]["alice"]["new"] == 2
    assert report["accounts"]["bob"]["new"] == 1
    for handle, count in (("alice", 2), ("bob", 1)):
        files = list((tmp_path / "ws" / "raw" / handle).glob("*.json"))
        assert len(files) == 1
        assert len(json.loads(files[0].read_text(encoding="utf-8"))) == count
    text = fetch_x.format_report(report)
    assert "@alice: nowych 2" in text and "@bob: nowych 1" in text


def test_since_defaults_to_n_days_then_comes_from_state(tmp_path):
    fake = FakeFetch({"alice": tweets(1)})
    first = fetch(tmp_path, fake, handles=("alice",))
    assert fake.calls[0]["since"] == "2026-09-18"
    assert first["accounts"]["alice"]["since_source"] == "default-14d"
    state = json.loads((tmp_path / "ws" / "fetch_state.json").read_text(encoding="utf-8"))
    assert state["accounts"]["alice"]["last_success"] == "2026-10-02"

    later = run_fetch(
        handles=["alice"], workspace=tmp_path / "ws", fetch_fn=fake,
        now=datetime(2026, 10, 9, 8, 0, tzinfo=timezone.utc),
    )
    assert fake.calls[1]["since"] == "2026-10-02"
    assert later["accounts"]["alice"]["since_source"] == "state"


def test_explicit_since_overrides_state(tmp_path):
    fake = FakeFetch()
    fetch(tmp_path, fake, handles=("alice",))
    fetch(tmp_path, fake, handles=("alice",), since="2026-01-01")
    assert fake.calls[1]["since"] == "2026-01-01"


def test_dedupe_against_previous_raw_files_and_within_a_batch(tmp_path):
    fake = FakeFetch({"alice": tweets(1, 2, 2)})
    assert fetch(tmp_path, fake, handles=("alice",))["accounts"]["alice"]["new"] == 2
    fake.data["alice"] = tweets(2, 3)
    report = run_fetch(
        handles=["alice"], workspace=tmp_path / "ws", fetch_fn=fake, since="2026-09-01",
        now=datetime(2026, 10, 3, 10, 0, tzinfo=timezone.utc),
    )
    row = report["accounts"]["alice"]
    assert (row["fetched"], row["new"]) == (2, 1)
    saved = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((tmp_path / "ws" / "raw" / "alice").glob("*.json"))]
    assert [[t["id"] for t in batch] for batch in saved] == [["1", "2"], ["3"]]


def test_dedupe_uses_legacy_cache_and_writes_no_file_when_nothing_new(tmp_path):
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "Alice_raw_tweets.json").write_text(json.dumps(tweets(1)), encoding="utf-8")
    fake = FakeFetch({"alice": tweets(1)})
    report = fetch(tmp_path, fake, handles=("alice",), cache_dir=cache)
    assert report["accounts"]["alice"]["new"] == 0
    assert "raw_file" not in report["accounts"]["alice"]
    assert not (tmp_path / "ws" / "raw").exists()
    assert (cache / "Alice_raw_tweets.json").read_text(encoding="utf-8") == json.dumps(tweets(1))


def test_one_account_error_does_not_stop_others_or_move_its_state(tmp_path):
    fake = FakeFetch({"alice": tweets(1), "carol": tweets(5)}, fail={"bob"})
    report = fetch(tmp_path, fake, handles=("alice", "bob", "carol"))
    assert [report["accounts"][h]["status"] for h in ("alice", "bob", "carol")] == ["ok", "error", "ok"]
    assert report["accounts"]["carol"]["new"] == 1
    assert report["accounts"]["bob"]["error"].startswith("RuntimeError")
    state = json.loads((tmp_path / "ws" / "fetch_state.json").read_text(encoding="utf-8"))
    assert set(state["accounts"]) == {"alice", "carol"}
    assert "BLAD" in fetch_x.format_report(report)


def test_error_text_never_contains_the_token(tmp_path, monkeypatch):
    monkeypatch.setenv("APIFY_API_TOKEN", "sekret-token-123")
    report = fetch(tmp_path, FakeFetch(fail={"alice"}), handles=("alice",))
    assert "sekret-token-123" not in json.dumps(report)
    assert "***" in report["accounts"]["alice"]["error"]


def test_dry_run_makes_no_calls_and_writes_nothing(tmp_path):
    fake = FakeFetch({"alice": tweets(1)})
    report = fetch(tmp_path, fake, until="2026-10-01", dry_run=True)
    assert fake.calls == []
    assert not (tmp_path / "ws").exists()
    row = report["accounts"]["alice"]
    assert row["status"] == "dry-run"
    assert row["query"] == "from:alice since:2026-09-18 until:2026-10-01"
    assert "dry-run" in fetch_x.format_report(report)


def test_truncated_or_until_runs_do_not_move_the_watermark(tmp_path):
    fake = FakeFetch({"alice": tweets(1, 2)})
    report = fetch(tmp_path, fake, handles=("alice",), limit=2)
    assert report["accounts"]["alice"]["truncated"] is True
    assert not (tmp_path / "ws" / "fetch_state.json").exists()
    fetch(tmp_path, fake, handles=("alice",), until="2026-10-01")
    assert not (tmp_path / "ws" / "fetch_state.json").exists()


def test_invalid_input_is_rejected(tmp_path):
    with pytest.raises(ValueError):
        fetch(tmp_path, FakeFetch(), since="2026-13-40")
    with pytest.raises(ValueError):
        fetch(tmp_path, FakeFetch(), since="2026-10-02", until="2026-10-01")
    report = fetch(tmp_path, FakeFetch(), handles=("bad handle!",))
    assert report["accounts"]["bad handle!"]["status"] == "error"


def test_corrupt_state_file_fails_loudly(tmp_path):
    (tmp_path / "ws").mkdir()
    (tmp_path / "ws" / "fetch_state.json").write_text("{nope", encoding="utf-8")
    with pytest.raises(ValueError):
        fetch(tmp_path, FakeFetch())


def _cli(*args, env_extra=None):
    import os

    env = {**os.environ, "APIFY_API_TOKEN": ""}
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, "-m", "kb_pipeline", "fetch", *args],
        cwd=EXTRACTOR, capture_output=True, text=True, check=False, env=env,
    )


def test_cli_dry_run_needs_no_token_and_makes_no_files(tmp_path):
    ws = tmp_path / "ws"
    result = _cli("--backend", "apify", "--handle", "alice", "--handle", "@bob", "--workspace", str(ws),
                  "--dry-run", "--since", "2026-09-01")
    assert result.returncode == 0, result.stderr
    assert "from:alice since:2026-09-01" in result.stdout and "from:bob" in result.stdout
    assert not ws.exists()


def test_command_without_token_refuses_before_any_fetch(tmp_path, monkeypatch, capsys):
    import argparse

    monkeypatch.setattr(fetch_x, "load_env", lambda path=None: None)
    monkeypatch.delenv("APIFY_API_TOKEN", raising=False)
    monkeypatch.setattr(fetch_x, "fetch_account", lambda *a, **k: pytest.fail("no network expected"))
    args = argparse.Namespace(
        handle=["alice"], accounts=None, workspace=tmp_path / "ws", since=None, until=None,
        limit=10, default_days=14, dry_run=False, cache_dir=None, json=False,
        backend="apify", clm_dir=None, from_raw_dir=None,
    )
    assert fetch_x.run_command(args) == 1
    assert "Brak APIFY_API_TOKEN" in capsys.readouterr().out
    assert not (tmp_path / "ws").exists()


def test_cli_refuses_workspace_inside_vault():
    result = _cli("--handle", "alice", "--dry-run", "--workspace", str(EXTRACTOR.parent / "Pojecia" / "ws"))
    assert result.returncode == 1
    assert "vaulcie" in result.stdout


# --- CLM backend -----------------------------------------------------------

def clm_post(i, author="alice", created="Fri Sep 25 12:00:00 +0000 2026", **extra):
    post = {
        "id": str(i), "author": author, "author_id": "1", "conversation_id": str(i),
        "created_at": created, "created_at_iso": "2026-09-25T12:00:00+00:00",
        "text": f"post {i}", "is_reply": False, "in_reply_to_status_id": None,
        "in_reply_to_user": None, "likes": 3, "retweets": 1, "reply_count": 0,
        "url": f"https://x.com/{author}/status/{i}", "media": [],
    }
    post.update(extra)
    return post


def make_clm_dir(tmp_path, authors=None):
    clm = tmp_path / "CLM"
    clm.mkdir()
    (clm / "fetch_raw_history_30d.py").write_text("# fake\n", encoding="utf-8")
    (clm / "x_cookies.json").write_text('{"auth_token": "FAKE", "ct0": "FAKE"}', encoding="utf-8")
    authors = authors if authors is not None else [
        {"handle": "alice", "user_id": "11", "enabled": True},
        {"handle": "bob", "user_id": "22", "enabled": False},
        {"handle": "carol", "user_id": "33", "enabled": True},
    ]
    (clm / "monitored_authors.json").write_text(json.dumps(authors), encoding="utf-8")
    return clm


class FakeRunner:
    """Stands in for subprocess.run of the CLM script; writes the raw file like the real one."""

    def __init__(self, data, returncode=0, stdout=""):
        self.data, self.returncode, self.stdout = data, returncode, stdout
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append((cmd, kwargs))
        authors = json.loads(Path(cmd[cmd.index("--authors") + 1]).read_text(encoding="utf-8"))
        handle = authors[0]["handle"]
        out = Path(cmd[cmd.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
        if handle in self.data:
            (out / f"{handle}_raw_30d.json").write_text(json.dumps(self.data[handle]), encoding="utf-8")
        return subprocess.CompletedProcess(cmd, self.returncode, stdout=self.stdout, stderr="")


def test_clm_normalization_keeps_fields_and_adds_pipeline_aliases():
    reply = clm_post(7, in_reply_to_status_id="5", in_reply_to_user="dave", is_reply=True,
                     media=[{"url": "https://pbs.twimg.com/a.jpg", "type": "photo", "local_path": "C:/x.jpg"}])
    post = clm_source.normalize_post(reply, "alice")
    assert post["full_text"] == post["text"] == "post 7"
    assert post["username"] == "alice" and post["id"] == "7"
    assert post["favorite_count"] == 3 and post["retweet_count"] == 1
    assert post["in_reply_to_screen_name"] == "dave"
    assert post["media"] == [{"url": "https://pbs.twimg.com/a.jpg", "type": "photo"}]  # no local paths
    assert clm_source.normalize_post({"id": "x", "text": "t"}, "alice") is None
    assert clm_source.normalize_post({"id": "1", "text": "  "}, "alice") is None


def test_clm_normalized_post_is_accepted_by_the_existing_ingestion():
    from kb_pipeline.ingestion import normalize

    post = clm_source.normalize_post(clm_post(7, in_reply_to_status_id="5", is_reply=True, conversation_id="3"), "alice")
    record = normalize(post, handle="alice", fetched_at=NOW, raw_ref="t")
    assert record.source_id == "x:7" and record.reply_to_id == "x:5" and record.author == "alice"
    assert record.published_at is not None


def test_clm_fetch_runs_script_in_clm_dir_with_days_and_temp_authors(tmp_path):
    clm = make_clm_dir(tmp_path)
    runner = FakeRunner({"alice": [clm_post(1), clm_post(2, created="Mon Sep 01 12:00:00 +0000 2026")]})
    fn = clm_source.make_clm_fetch(clm, tmp_path / "tmp", python="PY", runner=runner,
                                   today=lambda: NOW.date())
    posts = fn("alice", since="2026-09-20", until=None, limit=80)
    cmd, kwargs = runner.calls[0]
    assert cmd[0] == "PY" and cmd[1].endswith("fetch_raw_history_30d.py")
    assert cmd[cmd.index("--days") + 1] == "13"  # 2026-09-20 .. 2026-10-02 inclusive
    assert Path(cmd[cmd.index("--authors") + 1]).is_relative_to(tmp_path / "tmp")  # not CLM's own file
    assert Path(cmd[cmd.index("--out") + 1]).is_relative_to(tmp_path / "tmp")
    assert kwargs["cwd"] == str(clm)
    assert [p["id"] for p in posts] == ["1"]  # the Sep 1 post is outside since


def test_clm_fetch_errors_are_explicit(tmp_path):
    clm = make_clm_dir(tmp_path)
    mk = lambda r, d=clm: clm_source.make_clm_fetch(d, tmp_path / "tmp", runner=r)
    with pytest.raises(RuntimeError, match="user_id"):
        mk(FakeRunner({}))("zed", since=None, until=None, limit=1)
    with pytest.raises(RuntimeError, match="kodem 3"):
        mk(FakeRunner({}, returncode=3))("alice", since=None, until=None, limit=1)
    with pytest.raises(RuntimeError, match="blad pobierania"):
        mk(FakeRunner({"alice": [clm_post(1)]}, stdout="  [!] HTTP 401 na stronie 1: x"))(
            "alice", since=None, until=None, limit=1)
    with pytest.raises(RuntimeError, match="nie utworzyl"):
        mk(FakeRunner({}))("alice", since=None, until=None, limit=1)
    (clm / "x_cookies.json").unlink()
    with pytest.raises(RuntimeError, match="x_cookies"):
        mk(FakeRunner({}))("alice", since=None, until=None, limit=1)


def test_clm_enabled_handles_come_from_monitored_authors(tmp_path):
    assert clm_source.enabled_handles(make_clm_dir(tmp_path)) == ["alice", "carol"]


def test_run_fetch_with_clm_fetch_isolates_errors_and_dedupes(tmp_path):
    clm = make_clm_dir(tmp_path)
    runner = FakeRunner({"alice": [clm_post(1), clm_post(2)], "carol": [clm_post(9, "carol")]})
    fn = clm_source.make_clm_fetch(clm, tmp_path / "ws" / "clm_tmp", runner=runner, today=lambda: NOW.date())
    kw = dict(handles=["alice", "zed", "carol"], workspace=tmp_path / "ws", fetch_fn=fn, now=NOW,
              backend="clm", limited=False)
    report = run_fetch(**kw)
    assert [report["accounts"][h]["status"] for h in ("alice", "zed", "carol")] == ["ok", "error", "ok"]
    raw = json.loads(next((tmp_path / "ws" / "raw" / "alice").glob("*.json")).read_text(encoding="utf-8"))
    assert [p["id"] for p in raw] == ["1", "2"] and raw[0]["source_backend"] == "clm"
    again = run_fetch(**kw, since="2026-09-01")
    assert again["accounts"]["alice"]["new"] == 0  # deduped against the earlier raw file
    assert report["backend"] == "clm"


def test_clm_page_sized_result_is_not_treated_as_truncated(tmp_path):
    fn = lambda handle, *, since, until, limit: [clm_post(i) for i in range(1, 4)]
    report = run_fetch(handles=["alice"], workspace=tmp_path / "ws", fetch_fn=fn, now=NOW,
                       backend="clm", limited=False, limit=2)
    assert report["accounts"]["alice"]["truncated"] is False
    assert (tmp_path / "ws" / "fetch_state.json").exists()


def test_import_from_raw_dir_reads_existing_clm_files_without_state_or_calls(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "alice_raw_30d.json").write_text(json.dumps([clm_post(1), clm_post(2), {"id": "bad"}]), encoding="utf-8")
    (raw / "Alice_raw_365d.json").write_text(json.dumps([clm_post(2), clm_post(3)]), encoding="utf-8")
    (raw / "other_raw_30d.json").write_text(json.dumps([clm_post(8, "other")]), encoding="utf-8")
    files, posts, skipped = clm_source.read_raw_dir(raw, "alice", since=None, until=None)
    assert len(files) == 2 and [p["id"] for p in posts] == ["1", "2", "3"] and skipped == 1

    fn = fetch_x._import_fetch(raw)
    kw = dict(handles=["alice", "nofile"], workspace=tmp_path / "ws", fetch_fn=fn, now=NOW,
              backend="clm-import", limited=False, update_state=False, open_window=True)
    report = run_fetch(**kw)
    assert report["accounts"]["alice"]["new"] == 3
    assert report["accounts"]["nofile"]["status"] == "error"
    assert not (tmp_path / "ws" / "fetch_state.json").exists()
    assert run_fetch(**kw)["accounts"]["alice"]["new"] == 0  # re-import is idempotent


def test_cli_import_dry_run_lists_files_and_writes_nothing(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "alice_raw_30d.json").write_text(json.dumps([clm_post(1)]), encoding="utf-8")
    result = _cli("--from-raw-dir", str(raw), "--handle", "alice", "--workspace", str(tmp_path / "ws"), "--dry-run")
    assert result.returncode == 0, result.stderr
    assert "alice_raw_30d.json" in result.stdout
    assert not (tmp_path / "ws").exists()


def test_cli_clm_dry_run_uses_enabled_authors_and_makes_no_calls(tmp_path):
    clm = make_clm_dir(tmp_path)
    result = _cli("--clm-dir", str(clm), "--workspace", str(tmp_path / "ws"), "--dry-run")
    assert result.returncode == 0, result.stderr
    assert "@alice" in result.stdout and "@carol" in result.stdout and "@bob" not in result.stdout
    assert "fetch_raw_history_30d.py --days 15" in result.stdout
    assert not (tmp_path / "ws").exists()
    assert not (clm / "monitored_authors.json").read_text(encoding="utf-8").count("last_sync")


def test_cli_clm_dir_can_come_from_env(tmp_path):
    clm = make_clm_dir(tmp_path)
    result = _cli("--workspace", str(tmp_path / "ws"), "--dry-run", env_extra={"CLM_DIR": str(clm)})
    assert result.returncode == 0 and "@carol" in result.stdout


def test_fetch_maintains_merged_cache_dir_usable_by_run(tmp_path):
    from kb_pipeline.ingestion import read_cache

    fake = FakeFetch({"Alice": tweets(2, 1)})
    fetch(tmp_path, fake, handles=("Alice",))
    fake.data["Alice"] = tweets(3)
    run_fetch(handles=["Alice"], workspace=tmp_path / "ws", fetch_fn=fake, since="2026-09-01",
              now=datetime(2026, 10, 3, 10, 0, tzinfo=timezone.utc))
    cache = tmp_path / "ws" / "cache" / "alice_raw_tweets.json"
    assert [t["id"] for t in json.loads(cache.read_text(encoding="utf-8"))] == ["1", "2", "3"]
    records = [r for _, r, _, err in read_cache(cache) if err is None]
    assert [r.source_id for r in records] == ["x:1", "x:2", "x:3"]
