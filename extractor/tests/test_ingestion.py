import json
from datetime import datetime, timezone

import pytest

from kb_pipeline.ingestion import normalize
from kb_pipeline.storage import SourceStore


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_normalizer_preserves_short_reply_and_separates_quote_from_parent():
    record = normalize({"id": "123", "text": "Yes", "in_reply_to_status_id": "456", "quoted_status_id": "789",
                        "conversation_id": "456", "created_at": "not a date", "quotedText": "unrelated"},
                       handle="example", fetched_at=NOW, raw_ref="cache:fixture:0")
    assert record.text == "Yes"
    assert record.reply_to_id == "x:456"
    assert record.quoted_source_id == "x:789"
    assert record.conversation_id == "x:456"
    assert record.published_at is None
    assert record.context_status.value == "partial"
    with pytest.raises(ValueError, match="stable tweet ID"):
        normalize({"text": "No ID"}, handle="example", fetched_at=NOW, raw_ref="cache:fixture:1")


def test_import_is_idempotent_persistent_and_preserves_revisions(tmp_path):
    cache = tmp_path / "example_raw_tweets.json"
    entries = [{"id": "123", "text": "Yes", "created_at": "Sun Sep 20 12:05:11 +0000 2026"},
               {"text": "no ID"}]
    cache.write_text(json.dumps(entries), encoding="utf-8")
    workspace = tmp_path / "workspace"
    with SourceStore(workspace) as store:
        assert store.import_cache(cache) == {"new_revisions": 1, "unchanged": 0, "errors": 1}
        assert store.import_cache(cache) == {"new_revisions": 0, "unchanged": 1, "errors": 1}
        original = store.connection.execute("SELECT content_hash FROM source_revisions").fetchone()[0]
        assert store.get("x:123", original).published_at.year == 2026
    entries[0]["text"] = "Changed"
    cache.write_text(json.dumps(entries), encoding="utf-8")
    with SourceStore(workspace) as store:
        assert store.import_cache(cache)["new_revisions"] == 1
        assert store.get("x:123", original).text == "Yes"
        assert store.connection.execute("SELECT count(*) FROM source_revisions").fetchone()[0] == 2
        assert store.connection.execute("SELECT count(*) FROM import_errors").fetchone()[0] == 1


def test_invalid_cache_does_not_modify_database(tmp_path):
    cache = tmp_path / "example_raw_tweets.json"
    cache.write_text("{", encoding="utf-8")
    with SourceStore(tmp_path / "workspace") as store:
        with pytest.raises(json.JSONDecodeError):
            store.import_cache(cache)
        assert store.connection.execute("SELECT count(*) FROM source_revisions").fetchone()[0] == 0
