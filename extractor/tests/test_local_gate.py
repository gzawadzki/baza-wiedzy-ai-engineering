from kb_pipeline.assemble import assemble_post
from kb_pipeline.local_gate import decide_clm, screen_focus
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


def test_clm_rejects_low_claim_and_promotion_without_jev():
    assert decide_clm(_clm(0.2)) == ("reject", "low_focus_claim")
    assert decide_clm(_clm(0.9, 0.95)) == ("reject", "promotion")
    assert decide_clm(_clm(0.55, 0.2)) == ("keep", "clm_focus_claim")
    calls = []
    result = process_post(
        _post("We are hiring AI engineers. Apply now."),
        handle="kun",
        local_filter=lambda assembled: calls.append("clm") or _clm(0.45, 0.94),
        jev_evaluate=lambda bundle: calls.append("jev"),
        categorize=lambda assembled: None,
        summarize=lambda document, category: None,
    )
    assert calls == ["clm"]
    assert result.status == "reject"
    assert result.reason == "promotion"


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
