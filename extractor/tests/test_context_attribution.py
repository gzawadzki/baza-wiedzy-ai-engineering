"""PKG-2A: author text, parent, and quoted post stay separated, with real attribution."""

from datetime import datetime, timezone

from kb_pipeline.assemble import assemble_post
from kb_pipeline.context import build_context
from kb_pipeline.decisions import ContextCitation, classify_quote, parse_summary
from kb_pipeline.run_flow import _bundle, process_post
from kb_pipeline.schemas import ContextStatus

PARENT = {
    "id": "10",
    "username": "ada",
    "full_text": "The canary must pass before the checkpoint rule is applied.",
    "in_reply_to_status_id": "9",
    "created_at": "Wed Sep 02 00:00:00 +0000 2026",
}
GRANDPARENT = {
    "id": "9",
    "username": "bob",
    "full_text": "Thread root: checkpoints exist to bound recovery cost.",
    "created_at": "Tue Sep 01 00:00:00 +0000 2026",
}
QUOTE_OTHER = {
    "id": "99",
    "username": "vendor",
    "full_text": "Our product doubles throughput on every agent run.",
    "created_at": "Mon Aug 31 00:00:00 +0000 2026",
}
REPLY = {
    "id": "11",
    "username": "kun",
    "full_text": "Stosuję regułę rodzica dopiero po kanarku, nie wcześniej.",
    "in_reply_to_status_id": "10",
    "conversation_id": "9",
    "created_at": "Thu Sep 03 00:00:00 +0000 2026",
}
REPLY_WITH_QUOTE = {**REPLY, "quoted_status_id": "99", "quotedTweet": QUOTE_OTHER}

JEV_PASS = {
    "model": "jev-test",
    "answers": {
        "engineering_value": {"type": "noul", "noul": 0.9},
        "context_sufficient": {"type": "noul", "noul": 0.9},
        "topic": {
            "type": "choice",
            "choice": "other",
            "probabilities": {"compaction": 0, "evals": 0, "harness": 0, "other": 1},
            "confidence": 1,
        },
    },
}
CLM_KEEP = {
    "model": "clm-latest",
    "answers": {
        "focus_claim": {"type": "noul", "noul": 0.82},
        "promotion": {"type": "noul", "noul": 0.04},
    },
}
CATEGORY_OK = {"category": "Zasady"}
OWN_QUOTE = "Stosuję regułę rodzica dopiero po kanarku, nie wcześniej."
PARENT_QUOTE = "The canary must pass before the checkpoint rule is applied."
QUOTE_QUOTE = "Our product doubles throughput on every agent run."


def _pipeline(**overrides):
    calls = {
        "local_filter": lambda assembled: CLM_KEEP,
        "jev_evaluate": lambda bundle: JEV_PASS,
        "categorize": lambda assembled: CATEGORY_OK,
        "summarize": lambda document, category: {
            "title": "Kanarek przed regułą",
            "summary": "Regułę rodzica stosuj dopiero po kanarku.",
            "quote": OWN_QUOTE,
        },
    }
    calls.update(overrides)
    return calls


def test_reply_with_parent_keeps_author_text_alone_and_records_the_parent():
    assembled = assemble_post(REPLY, handle="kun", known_items=[PARENT, GRANDPARENT])
    bundle = _bundle(assembled)

    assert bundle.focus.text == REPLY["full_text"]
    assert PARENT_QUOTE not in bundle.focus.text
    assert GRANDPARENT["full_text"] not in bundle.focus.text
    assert bundle.focus.reply_to_id == "x:10"
    assert bundle.focus.conversation_id == "x:9"
    assert bundle.missing_ids == []
    assert bundle.context_status is ContextStatus.complete

    parent = next(item for item in bundle.related if item.source.source_id == "x:10")
    grandparent = next(item for item in bundle.related if item.source.source_id == "x:9")
    assert parent.role == "parent"
    assert parent.source.author == "ada"
    assert parent.provenance == "cache:index"
    assert grandparent.role == "thread"
    assert grandparent.source.author == "bob"
    assert parent.source.text == PARENT_QUOTE
    assert grandparent.source.text == GRANDPARENT["full_text"]


def test_related_records_keep_their_own_source_dates():
    bundle = _bundle(assemble_post(REPLY, handle="kun", known_items=[PARENT]))

    assert bundle.focus.published_at == datetime(2026, 9, 3, tzinfo=timezone.utc)
    parent = bundle.related[0].source
    assert parent.published_at == datetime(2026, 9, 2, tzinfo=timezone.utc)
    assert parent.published_at != bundle.focus.published_at


def test_missing_parent_is_explicit_without_invented_content():
    bundle = _bundle(assemble_post(REPLY, handle="kun", known_items=[]))

    assert bundle.missing_ids == ["x:10"]
    assert bundle.related == []
    assert bundle.focus.text == REPLY["full_text"]
    assert PARENT_QUOTE not in bundle.focus.text
    assert bundle.context_status is ContextStatus.unavailable
    # the relation itself stays None when nothing is known about it
    assert assemble_post(
        {"id": "12", "username": "kun", "full_text": "Samodzielny wpis bez relacji."},
        handle="kun",
    ).conversation_id is None


def test_quoted_post_is_related_with_its_own_author_not_merged_into_focus():
    bundle = _bundle(assemble_post(REPLY_WITH_QUOTE, handle="kun", known_items=[PARENT, QUOTE_OTHER]))

    assert bundle.focus.quoted_source_id == "x:99"
    assert QUOTE_QUOTE not in bundle.focus.text
    quote = next(item for item in bundle.related if item.source.source_id == "x:99")
    assert quote.role == "quote"
    assert quote.source.author == "vendor"
    assert quote.source.published_at == datetime(2026, 8, 31, tzinfo=timezone.utc)


def test_quote_must_come_from_the_author_text_not_from_context():
    related = [
        (ContextCitation(role="parent", author="ada", source_id="x:10", provenance="cache:index"), PARENT_QUOTE),
        (ContextCitation(role="quote", author="vendor", source_id="x:99", provenance="actor:quotedTweet"), QUOTE_QUOTE),
    ]
    assert classify_quote(OWN_QUOTE, REPLY["full_text"], related) == "author"
    assert classify_quote(PARENT_QUOTE, REPLY["full_text"], related) == "context"
    assert classify_quote(QUOTE_QUOTE, REPLY["full_text"], related) == "context"
    assert classify_quote("Cytat, którego nie ma nigdzie.", REPLY["full_text"], related) == "absent"


def test_quote_from_another_author_is_rejected_but_keeps_its_attribution():
    calls = []

    def summarize(document: str, category: str) -> dict:
        calls.append(document)
        return {
            "title": "Kanarek przed regułą",
            "summary": "Regułę rodzica stosuj dopiero po kanarku.",
            "quote": QUOTE_QUOTE,  # verbatim, but written by another author
        }

    result = process_post(
        REPLY_WITH_QUOTE, handle="kun", known_items=[PARENT, QUOTE_OTHER],
        **_pipeline(summarize=summarize),
    )

    assert calls == [REPLY["full_text"]]  # the author text, not the concatenated document
    assert result.status == "reject"
    assert "spoza tekstu autora" in result.reason
    assert [(c.role, c.author, c.source_id) for c in result.context_citations] == [("quote", "vendor", "x:99")]


def test_parent_quote_cannot_be_passed_off_as_the_author_original_quote():
    result = process_post(
        REPLY, handle="kun", known_items=[PARENT],
        **_pipeline(summarize=lambda document, category: {
            "title": "Kanarek przed regułą",
            "summary": "Regułę rodzica stosuj dopiero po kanarku.",
            "quote": PARENT_QUOTE,
        }),
    )

    assert result.status == "reject"
    assert [(c.role, c.author, c.source_id) for c in result.context_citations] == [("parent", "ada", "x:10")]


def test_own_quote_is_accepted_and_whole_context_reaches_jev():
    seen = {}

    def jev(bundle):
        seen["bundle"] = bundle
        return JEV_PASS

    result = process_post(REPLY, handle="kun", known_items=[PARENT], **_pipeline(jev_evaluate=jev))

    assert result.status == "extract"
    assert result.summary["quote"] == OWN_QUOTE
    assert PARENT_QUOTE in seen["bundle"].related[0].source.text
    assert PARENT_QUOTE not in seen["bundle"].focus.text


def test_provider_failure_is_an_error_and_uncertainty_stays_a_defer():
    def boom(assembled):
        raise RuntimeError("provider 503")

    failed = process_post(REPLY, handle="kun", known_items=[PARENT], **_pipeline(local_filter=boom))
    assert failed.status == "error"
    assert "503" in failed.reason

    jev_uncertain = {
        "model": "jev-test",
        "answers": {
            "engineering_value": {"type": "noul", "noul": 0.30},
            "context_sufficient": {"type": "noul", "noul": 0.30},
            "topic": {
                "type": "choice",
                "choice": "other",
                "probabilities": {"compaction": 0, "evals": 0, "harness": 0, "other": 1},
                "confidence": 1,
            },
        },
    }
    deferred = process_post(REPLY, handle="kun", known_items=[PARENT], **_pipeline(jev_evaluate=lambda bundle: jev_uncertain))
    assert deferred.status == "defer"

    def extraction_down(document: str, category: str) -> dict:
        raise TimeoutError("model timeout")

    provider = process_post(REPLY, handle="kun", known_items=[PARENT], **_pipeline(summarize=extraction_down))
    assert provider.status == "error"


def test_fetched_parent_keeps_fetch_provenance_and_missing_quote_id():
    known_quote_only = {key: value for key, value in REPLY_WITH_QUOTE.items() if key != "quotedTweet"}
    bundle = _bundle(assemble_post(
        known_quote_only, handle="kun", known_items=[],
        fetch_status=lambda source_id: {"10": PARENT, "9": GRANDPARENT}.get(source_id),
    ))
    parent = bundle.related[0]
    assert parent.source.source_id == "x:10"
    assert parent.provenance == "cache:fetch"
    # x:99 is a known source id whose text could not be obtained
    assert bundle.missing_ids == ["x:99"]
    assert bundle.context_status is ContextStatus.partial


def test_inline_actor_context_is_attributed_to_the_actor():
    item = {
        "id": "21",
        "username": "kun",
        "full_text": "Zgadzam się z regułą powyżej, tylko po kanarku.",
        "in_reply_to_status_id": "20",
        "replyTo": {"id": "20", "username": "ada", "text": "Reguła brzmi: najpierw kanarek."},
    }
    bundle = _bundle(assemble_post(item, handle="kun", known_items=[]))
    parent = bundle.related[0]
    assert parent.provenance == "actor:replyTo"
    assert parent.source.author == "ada"
    assert bundle.missing_ids == []


def test_parse_summary_keeps_its_signature_and_rejects_foreign_quotes():
    payload = {"title": "T", "summary": "S", "quote": OWN_QUOTE}
    assert parse_summary(payload, REPLY["full_text"])["quote"] == OWN_QUOTE

    from kb_pipeline.decisions import ForeignQuoteError

    related = [(ContextCitation(role="parent", author="ada", source_id="x:10"), PARENT_QUOTE)]
    try:
        parse_summary({**payload, "quote": PARENT_QUOTE}, REPLY["full_text"], related=related)
    except ForeignQuoteError as exc:
        assert exc.citation is not None and exc.citation.author == "ada"
    else:
        raise AssertionError("foreign quote must not pass as the author's quote")


def test_build_context_keeps_missing_ids_to_known_unavailable_sources():
    from kb_pipeline.schemas import SourceRecord
    import hashlib
    from datetime import datetime as dt

    def record(source_id: str, text: str, **kwargs) -> SourceRecord:
        return SourceRecord(
            source_id=source_id,
            author="ada",
            text=text,
            fetched_at=dt(2026, 9, 3, tzinfo=timezone.utc),
            raw_ref="test",
            content_hash=hashlib.sha256(text.encode()).hexdigest(),
            **kwargs,
        )

    focus = record("x:11", REPLY["full_text"], reply_to_id="x:10", conversation_id="x:9")
    bundle = build_context(focus, lambda source_id: None, extra_missing_ids=["x:99"])
    assert bundle.missing_ids == ["x:10", "x:99"]
    assert bundle.related == []
    assert bundle.context_status is ContextStatus.unavailable
