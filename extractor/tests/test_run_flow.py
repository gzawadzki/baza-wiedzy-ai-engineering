from kb_pipeline.assemble import assemble_post, image_refs
from kb_pipeline.decisions import resolve_extraction_model
from kb_pipeline.notes import render_note
from kb_pipeline.period import in_period
from kb_pipeline.run_flow import process_post


PARENT = {
    "id": "10",
    "username": "ada",
    "full_text": "Parent explains the checkpoint rule in detail.",
    "created_at": "Wed Sep 02 00:00:00 +0000 2026",
}
REPLY = {
    "id": "11",
    "username": "kun",
    "full_text": "Use the parent rule only after the canary passes.",
    "in_reply_to_status_id": "10",
    "quoted_status_id": "99",
    "quotedTweet": {"id": "99", "text": "Quoted advertisement, not the parent."},
    "created_at": "Thu Sep 03 00:00:00 +0000 2026",
    "media": [{
        "type": "photo",
        "url": "https://pbs.twimg.com/media/abc.jpg",
        "alt_text": "diagram of a canary",
    }],
}
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


def test_period_is_inclusive_and_does_not_invent_missing_dates():
    assert in_period({"created_at": "Tue Sep 01 00:00:00 +0000 2026"}, since=None, until=None)
    assert in_period({"created_at": "Tue Sep 01 23:00:00 +0000 2026"}, since=__import__("datetime").date(2026, 9, 1), until=__import__("datetime").date(2026, 9, 2))
    assert not in_period({"created_at": "Wed Sep 02 00:00:00 +0000 2026"}, since=None, until=__import__("datetime").date(2026, 9, 2))
    assert not in_period({"text": "no date"}, since=None, until=None)


def test_thread_ocr_and_quote_stay_distinct():
    assembled = assemble_post(REPLY, handle="kun", known_items=[PARENT], ocr_url=lambda url: "OCR canary threshold")
    assert "Parent explains the checkpoint rule" in assembled.document
    assert assembled.document.index("[watek @ada") < assembled.document.index("[wpis @kun")
    assert "Quoted advertisement" in assembled.document
    assert assembled.document.index("[cytat") != assembled.document.index("[watek")
    assert "OCR canary threshold" not in assembled.document
    assert "pbs.twimg.com" not in assembled.document
    assert assembled.ocr_status == "ignored"
    assert assembled.missing_ids == []
    assert image_refs({"media": [{"type": "photo", "url": "http://evil.example/a.jpg"}]}) == []


def test_missing_parent_is_explicit_and_not_taken_from_quote():
    assembled = assemble_post(REPLY, handle="kun", known_items=[])
    assert "10" in assembled.missing_ids
    assert "Parent explains" not in assembled.document
    assert "[BRAK KONTEKSTU]" in assembled.document
    assert "Quoted advertisement" in assembled.document


def test_filters_run_in_order_and_extraction_cannot_invent_a_quote():
    calls = []

    def local_filter(assembled) -> dict:
        calls.append("clm")
        assert "canary passes" in assembled.focus_evidence
        assert "OCR canary threshold" not in assembled.focus_evidence
        assert "Parent explains" in assembled.context_text
        assert "Parent explains" not in assembled.focus_evidence
        return {
            "model": "clm-latest",
            "answers": {
                "focus_claim": {"type": "noul", "noul": 0.82},
                "promotion": {"type": "noul", "noul": 0.04},
            },
        }

    def jev(bundle):
        calls.append("jev")
        assert "canary passes" in bundle.focus.text
        assert "OCR canary threshold" not in bundle.focus.text
        return JEV_PASS

    def categorize(assembled) -> dict:
        calls.append("category")
        assert "canary" in assembled.focus_evidence
        return {"category": "Zasady"}

    def summarize(document: str, category: str) -> dict:
        calls.append(("summary", category))
        return {
            "title": "Kanarek przed regułą",
            "summary": "Regułę z wątku stosuj dopiero po przejściu kanarka.",
            "quote": "missing quote",
            "topic": "kanarek",
        }

    result = process_post(
        REPLY, handle="kun", known_items=[PARENT], ocr_url=lambda url: "OCR canary threshold",
        local_filter=local_filter, jev_evaluate=jev, categorize=categorize, summarize=summarize,
    )
    assert calls == ["clm", "jev", "category", ("summary", "Zasady")]
    assert result.status == "defer"
    assert result.category == "Zasady"

    def grounded(document: str, category: str) -> dict:
        return {
            "title": "Kanarek przed regułą",
            "summary": "Regułę stosuj po kanarku.",
            "quote": "Use the parent rule only after the canary passes.",
        }

    passed = process_post(
        REPLY, handle="kun", known_items=[PARENT], ocr_url=lambda url: "OCR canary threshold",
        local_filter=local_filter, jev_evaluate=jev, categorize=categorize, summarize=grounded,
    )
    assert passed.status == "extract"
    note = render_note(passed, "kun")
    assert "kategoria: \"Zasady\"" in note
    assert "[[Harness" not in note
    assert resolve_extraction_model("openrouter/space-bunny") == "stealth/space-bunny-alpha"


def test_local_drop_does_not_call_jev_or_extraction():
    calls = []
    result = process_post(
        REPLY, handle="kun", known_items=[PARENT],
        local_filter=lambda assembled: calls.append("clm") or {
            "answers": {"focus_claim": {"type": "noul", "noul": 0.1}, "promotion": {"type": "noul", "noul": 0.0}}
        },
        jev_evaluate=lambda bundle: calls.append("jev"),
        categorize=lambda assembled: calls.append("category"),
        summarize=lambda document, category: calls.append("summary"),
    )
    assert calls == ["clm"]
    assert result.status == "reject"
