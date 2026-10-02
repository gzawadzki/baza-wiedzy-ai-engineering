from kb_pipeline.assemble import assemble_post
from kb_pipeline.local_gate import (
    CategoryUncertain,
    category_from_clm,
    decide_clm,
    resolve_promotion_mode,
    screen_focus,
)
from kb_pipeline.run_flow import process_post


def _post(text: str, **extra) -> dict:
    return {
        "id": "11",
        "username": "kun",
        "full_text": text,
        "created_at": "Thu Sep 03 00:00:00 +0000 2026",
        **extra,
    }


def _clm(claim: float, promo: float = 0.0) -> dict:
    return {
        "model": "clm-latest",
        "answers": {
            "focus_claim": {"type": "noul", "noul": claim},
            "promotion": {"type": "noul", "noul": promo},
        },
    }


def test_obvious_junk_never_reaches_clm():
    calls = []
    for text in ("lol", "thanks", "https://example.com", "", "@chris_j_paxton"):
        result = process_post(
            _post(text),
            handle="kun",
            local_filter=lambda assembled: calls.append(assembled) or _clm(0.9),
            jev_evaluate=lambda bundle: calls.append("jev"),
            categorize=lambda assembled: calls.append("category"),
            summarize=lambda document, category: calls.append("summary"),
        )
        assert result.status == "reject"
        assert result.reason in {"reaction_only", "link_only", "empty_focus"}
    assert calls == []


def _jev(engineering: float = 0.9, context: float = 0.9) -> dict:
    return {
        "model": "jev-test",
        "answers": {
            "engineering_value": {"type": "noul", "noul": engineering},
            "context_sufficient": {"type": "noul", "noul": context},
            "topic": {
                "type": "choice",
                "choice": "other",
                "probabilities": {"compaction": 0, "evals": 0, "harness": 0, "other": 1},
                "confidence": 1,
            },
        },
    }


def test_decide_clm_low_claim_and_legacy_promotion_reject():
    assert decide_clm(_clm(0.2)) == ("reject", "low_focus_claim")
    # decide_clm keeps the historical hard reject unless asked (offline flow unchanged)
    assert decide_clm(_clm(0.9, 0.95)) == ("reject", "promotion")
    assert decide_clm(_clm(0.9, 0.95), promotion_mode="reject") == ("reject", "promotion")
    assert decide_clm(_clm(0.55, 0.2)) == ("keep", "clm_focus_claim")


def test_promotion_advisory_never_rejects_alone():
    assert decide_clm(_clm(0.9, 0.95), promotion_mode="advisory") == ("keep", "clm_promotion_advisory")
    assert decide_clm(_clm(0.5, 0.75), promotion_mode="advisory") == ("keep", "clm_promotion_advisory")
    # below the bar nothing changes
    assert decide_clm(_clm(0.5, 0.74), promotion_mode="advisory") == ("keep", "clm_focus_claim")
    # other CLM outcomes are unchanged: low claim still rejects, invalid still defers
    assert decide_clm(_clm(0.1, 0.99), promotion_mode="advisory") == ("reject", "low_focus_claim")
    assert decide_clm({"answers": {}}, promotion_mode="advisory") == ("defer", "local_filter_invalid")
    try:
        decide_clm(_clm(0.9), promotion_mode="nope")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown mode must fail")


def test_resolve_promotion_mode_default_is_advisory():
    assert resolve_promotion_mode(None) == "advisory"
    assert resolve_promotion_mode("") == "advisory"
    assert resolve_promotion_mode(" Reject ") == "reject"


def test_flagged_promotion_goes_to_jev_by_default_and_can_extract():
    calls = []
    result = process_post(
        _post("Prompt caching cuts cost: keep the static prefix first, then reasoning effort low for routing."),
        handle="kun",
        local_filter=lambda assembled: calls.append("clm") or _clm(0.6, 0.97),
        jev_evaluate=lambda bundle: calls.append("jev") or _jev(),
        categorize=lambda assembled: calls.append("category") or {"category": "Zasady"},
        summarize=lambda document, category: calls.append("summary") or {
            "title": "Cache prefiksu", "summary": "Statyczny prefiks na poczatek.",
            "quote": "keep the static prefix first",
        },
    )
    assert calls == ["clm", "jev", "category", "summary"]
    assert result.status == "extract"
    assert result.clm_reason == "clm_promotion_advisory"


def test_flagged_promotion_is_rejected_by_jev_when_it_is_really_an_ad():
    calls = []
    result = process_post(
        _post("We are hiring AI engineers. Apply now."),
        handle="kun",
        local_filter=lambda assembled: calls.append("clm") or _clm(0.45, 0.94),
        jev_evaluate=lambda bundle: calls.append("jev") or _jev(engineering=0.05),
        categorize=lambda assembled: calls.append("category"),
        summarize=lambda document, category: calls.append("summary"),
    )
    assert calls == ["clm", "jev"]
    assert result.status == "reject"
    assert result.reason == "low_engineering_value"
    assert result.clm_reason == "clm_promotion_advisory"


def test_promotion_reject_mode_restores_hard_reject_without_jev():
    calls = []
    result = process_post(
        _post("We are hiring AI engineers. Apply now."),
        handle="kun",
        local_filter=lambda assembled: calls.append("clm") or _clm(0.45, 0.94),
        jev_evaluate=lambda bundle: calls.append("jev"),
        categorize=lambda assembled: None,
        summarize=lambda document, category: None,
        promotion_mode="reject",
    )
    assert calls == ["clm"]
    assert result.status == "reject"
    assert result.reason == "promotion"


def test_short_reply_without_context_is_deferred_not_rejected():
    result = process_post(
        _post("Can you share the repo for that?", in_reply_to_status_id="10"),
        handle="kun",
        local_filter=lambda assembled: _clm(0.4, 0.1),
        jev_evaluate=lambda bundle: _jev(engineering=0.5, context=0.2),
        categorize=lambda assembled: None,
        summarize=lambda document, category: None,
    )
    assert result.status == "defer"
    assert result.reason == "insufficient_context"


def test_category_uncertain_is_a_defer_not_an_error():
    def uncertain(assembled):
        raise CategoryUncertain("category_uncertain")

    result = process_post(
        _post("Use a held-out set before trusting any judge model."),
        handle="kun",
        local_filter=lambda assembled: _clm(0.6, 0.1),
        jev_evaluate=lambda bundle: _jev(),
        categorize=uncertain,
        summarize=lambda document, category: None,
    )
    assert result.status == "defer"
    assert result.reason == "category_uncertain"
    assert result.jev_topic == "other"


def test_category_from_clm_low_confidence_raises_category_uncertain():
    low = {"answers": {"category": {"type": "choice", "choice": "Zasady", "confidence": 0.2}}}
    try:
        category_from_clm(low)
    except CategoryUncertain as exc:
        assert isinstance(exc, ValueError)
    else:
        raise AssertionError("expected CategoryUncertain")
    # an incomplete answer is still a plain ValueError, not an uncertainty
    try:
        category_from_clm({"answers": {}})
    except CategoryUncertain:
        raise AssertionError("incomplete answer must not be CategoryUncertain")
    except ValueError:
        pass


def test_parent_claim_is_not_sent_to_clm_as_focus():
    assembled = assemble_post(
        {
            "id": "11",
            "username": "kun",
            "full_text": "this",
            "in_reply_to_status_id": "10",
            "created_at": "Thu Sep 03 00:00:00 +0000 2026",
        },
        handle="kun",
        known_items=[{
            "id": "10",
            "username": "ada",
            "full_text": "Never grade the model with the same context it wrote.",
        }],
    )
    assert screen_focus(assembled) == ("reject", "reaction_only")
    assert "Never grade" not in assembled.focus_evidence
    assert "Never grade" in assembled.context_text


def test_attached_images_are_ignored():
    assembled = assemble_post(
        {
            **_post("diagram"),
            "media": [
                {"type": "photo", "url": "https://pbs.twimg.com/media/a.jpg", "alt_text": "grader diagram"},
                {"type": "video", "url": "https://pbs.twimg.com/media/b.jpg"},
            ],
        },
        handle="kun",
        ocr_url=lambda url: "Separate the grader from the generator context.",
    )
    assert assembled.focus_evidence == "diagram"
    assert "grader diagram" not in assembled.document
    assert assembled.ocr_status == "ignored"

def test_analyze_loaded_passes_promotion_mode_through():
    from kb_pipeline.account_run import analyze_loaded

    items = [_post("Cache the static prefix and lower reasoning effort to cut cost.")]
    common = dict(
        handle="kun", known_items=items,
        local_filter=lambda assembled: _clm(0.6, 0.97),
        jev_evaluate=lambda bundle: _jev(engineering=0.05),
        categorize=lambda assembled: None,
        summarize=lambda document, category: None,
    )
    advisory = analyze_loaded(items, **common)[0]
    assert (advisory.status, advisory.reason) == ("reject", "low_engineering_value")
    hard = analyze_loaded(items, promotion_mode="reject", **common)[0]
    assert (hard.status, hard.reason) == ("reject", "promotion")
