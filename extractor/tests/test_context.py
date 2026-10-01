from datetime import datetime, timezone
import hashlib
import json
import random

from kb_pipeline.context import build_context
from kb_pipeline.schemas import ContextStatus, SourceRecord


def make_source(
    source_id: str,
    *,
    author: str = "tester",
    text: str = "Technical observation about compiler optimizations.",
    reply_to_id: str | None = None,
    quoted_source_id: str | None = None,
    conversation_id: str | None = None,
) -> SourceRecord:
    payload = {
        "author": author,
        "text": text,
        "published_at": None,
        "reply_to_id": reply_to_id,
        "conversation_id": conversation_id,
        "quoted_source_id": quoted_source_id,
        "url": f"https://x.com/{author}/status/{source_id[2:]}",
    }
    content_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    return SourceRecord(
        source_id=source_id,
        author=author,
        text=text,
        fetched_at=datetime.now(timezone.utc),
        reply_to_id=reply_to_id,
        quoted_source_id=quoted_source_id,
        conversation_id=conversation_id,
        raw_ref=f"cache:test:{source_id}",
        content_hash=content_hash,
    )


def test_parent_and_quote_context():
    focus = make_source("x:100", reply_to_id="x:101", quoted_source_id="x:102")
    parent = make_source("x:101", text="Parent tweet providing initial claim.")
    quote = make_source("x:102", text="Quoted tweet referenced for comparison.")
    records = {r.source_id: r for r in (parent, quote)}

    bundle = build_context(focus, records.get)

    assert bundle.focus == focus
    assert bundle.missing_ids == []
    assert bundle.context_status is ContextStatus.complete
    assert len(bundle.related) == 2

    parent_item, quote_item = bundle.related
    assert parent_item.source.source_id == "x:101"
    assert parent_item.role == "parent"
    assert parent_item.provenance == "cache:lookup"

    assert quote_item.source.source_id == "x:102"
    assert quote_item.role == "quote"
    assert quote_item.provenance == "cache:lookup"


def test_missing_parent_without_related_is_unavailable():
    empty_lookup = lambda sid: None

    short_focus = make_source("x:200", reply_to_id="x:201", text="Yes")
    short_bundle = build_context(short_focus, empty_lookup)
    assert short_bundle.related == []
    assert short_bundle.missing_ids == ["x:201"]
    assert short_bundle.context_status is ContextStatus.unavailable

    substantive_focus = make_source(
        "x:202",
        reply_to_id="x:203",
        text="Speculative decoding improves throughput on large models significantly.",
    )
    substantive_bundle = build_context(substantive_focus, empty_lookup)
    assert substantive_bundle.related == []
    assert substantive_bundle.missing_ids == ["x:203"]
    assert substantive_bundle.context_status is ContextStatus.unavailable


def test_partial_when_some_context_present_and_some_missing():
    focus = make_source("x:300", reply_to_id="x:301", quoted_source_id="x:302")
    parent = make_source("x:301", text="Existing parent tweet text.")
    records = {"x:301": parent}

    bundle = build_context(focus, records.get)
    assert len(bundle.related) == 1
    assert bundle.related[0].source.source_id == "x:301"
    assert bundle.related[0].role == "parent"
    assert bundle.missing_ids == ["x:302"]
    assert bundle.context_status is ContextStatus.partial


def test_cycle_handling():
    # Self cycle: tweet claims itself as parent
    self_loop = make_source("x:400", reply_to_id="x:400")
    bundle_self = build_context(self_loop, lambda sid: self_loop if sid == "x:400" else None)
    assert bundle_self.related == []
    assert bundle_self.missing_ids == ["x:400"]
    assert bundle_self.context_status is ContextStatus.unavailable

    # Mutual 2-node cycle: focus -> A -> focus
    a = make_source("x:402", reply_to_id="x:401")
    focus_mutual = make_source("x:401", reply_to_id="x:402")
    store = {"x:401": focus_mutual, "x:402": a}
    bundle_mutual = build_context(focus_mutual, store.get)
    assert [item.source.source_id for item in bundle_mutual.related] == ["x:402"]
    assert bundle_mutual.missing_ids == ["x:401"]
    assert bundle_mutual.context_status is ContextStatus.partial

    # 3-node cycle: focus -> A -> B -> A
    node_b = make_source("x:405", reply_to_id="x:404")
    node_a = make_source("x:404", reply_to_id="x:405")
    focus_three = make_source("x:403", reply_to_id="x:404")
    store_three = {"x:403": focus_three, "x:404": node_a, "x:405": node_b}
    bundle_three = build_context(focus_three, store_three.get)
    assert [item.source.source_id for item in bundle_three.related] == ["x:404", "x:405"]
    assert [item.role for item in bundle_three.related] == ["parent", "thread"]
    assert bundle_three.missing_ids == ["x:404"]
    assert bundle_three.context_status is ContextStatus.partial


def test_quote_cycle_marked_unresolved():
    # Self quote cycle
    self_quote = make_source("x:410", quoted_source_id="x:410")
    bundle_self_q = build_context(self_quote, lambda sid: self_quote if sid == "x:410" else None)
    assert bundle_self_q.related == []
    assert bundle_self_q.missing_ids == ["x:410"]
    assert bundle_self_q.context_status is ContextStatus.unavailable

    # Mutual quote cycle
    q2 = make_source("x:412", quoted_source_id="x:411")
    q1 = make_source("x:411", quoted_source_id="x:412")
    focus = make_source("x:413", quoted_source_id="x:411")
    store = {"x:411": q1, "x:412": q2}
    bundle = build_context(focus, store.get)
    assert [item.source.source_id for item in bundle.related] == ["x:411", "x:412"]
    assert bundle.missing_ids == ["x:411"]
    assert bundle.context_status is ContextStatus.partial


def test_shared_parent_and_quote_not_marked_missing():
    # Tweet quotes the same tweet it is replying to (shared node in DAG)
    shared = make_source("x:450", text="Shared parent and quote.")
    focus = make_source("x:451", reply_to_id="x:450", quoted_source_id="x:450")
    store = {"x:450": shared}
    bundle = build_context(focus, store.get)
    assert [item.source.source_id for item in bundle.related] == ["x:450"]
    assert bundle.missing_ids == []
    assert bundle.context_status is ContextStatus.complete


def test_shared_ancestor_and_quote_not_marked_missing():
    # Tweet quotes an ancestor reached via reply chain
    ancestor = make_source("x:460", text="Root ancestor.")
    parent = make_source("x:461", reply_to_id="x:460", text="Direct parent.")
    focus = make_source("x:462", reply_to_id="x:461", quoted_source_id="x:460")
    store = {"x:460": ancestor, "x:461": parent}
    bundle = build_context(focus, store.get)
    assert [item.source.source_id for item in bundle.related] == ["x:461", "x:460"]
    assert bundle.missing_ids == []
    assert bundle.context_status is ContextStatus.complete


def test_depth_and_items_bounds():
    # Chain of depth 4: focus -> n1 -> n2 -> n3 -> n4
    n4 = make_source("x:504")
    n3 = make_source("x:503", reply_to_id="x:504")
    n2 = make_source("x:502", reply_to_id="x:503")
    n1 = make_source("x:501", reply_to_id="x:502")
    focus = make_source("x:500", reply_to_id="x:501")
    store = {r.source_id: r for r in (focus, n1, n2, n3, n4)}

    # Bound max_depth = 2: visits n1 (depth 1), n2 (depth 2); n3 is unvisited and missing
    bundle_depth = build_context(focus, store.get, max_depth=2)
    assert [item.source.source_id for item in bundle_depth.related] == ["x:501", "x:502"]
    assert bundle_depth.missing_ids == ["x:503"]
    assert bundle_depth.context_status is ContextStatus.partial

    # Bound max_items = 1: visits only n1; n2 is unvisited and missing
    bundle_items = build_context(focus, store.get, max_items=1)
    assert [item.source.source_id for item in bundle_items.related] == ["x:501"]
    assert bundle_items.missing_ids == ["x:502"]
    assert bundle_items.context_status is ContextStatus.partial

    # Bound max_depth = 0: no relations visited, focus.reply_to_id is missing, no related context -> unavailable
    bundle_zero = build_context(focus, store.get, max_depth=0)
    assert bundle_zero.related == []
    assert bundle_zero.missing_ids == ["x:501"]
    assert bundle_zero.context_status is ContextStatus.unavailable


def test_deterministic_ordering():
    p2 = make_source("x:602")
    p1 = make_source("x:601", reply_to_id="x:602")
    q1 = make_source("x:603")
    focus = make_source("x:600", reply_to_id="x:601", quoted_source_id="x:603")
    store = {r.source_id: r for r in (focus, p1, p2, q1)}

    first_bundle = build_context(focus, store.get)
    expected_related = [item.source.source_id for item in first_bundle.related]
    expected_roles = [item.role for item in first_bundle.related]

    for _ in range(25):
        shuffled_keys = list(store.keys())
        random.shuffle(shuffled_keys)
        shuffled_store = {k: store[k] for k in shuffled_keys}
        bundle = build_context(focus, shuffled_store.get)
        assert [item.source.source_id for item in bundle.related] == expected_related
        assert [item.role for item in bundle.related] == expected_roles
        assert bundle.missing_ids == first_bundle.missing_ids
        assert bundle.context_status == first_bundle.context_status


def test_thread_ancestors_role():
    t2 = make_source("x:703")
    t1 = make_source("x:702", reply_to_id="x:703")
    p = make_source("x:701", reply_to_id="x:702")
    focus = make_source("x:700", reply_to_id="x:701")
    store = {r.source_id: r for r in (focus, p, t1, t2)}

    bundle = build_context(focus, store.get)
    assert [item.source.source_id for item in bundle.related] == ["x:701", "x:702", "x:703"]
    assert [item.role for item in bundle.related] == ["parent", "thread", "thread"]
    assert bundle.missing_ids == []
    assert bundle.context_status is ContextStatus.complete


def test_standalone_focus_without_relations():
    focus = make_source("x:800")
    bundle = build_context(focus, lambda sid: None)
    assert bundle.related == []
    assert bundle.missing_ids == []
    assert bundle.context_status is ContextStatus.complete


def test_conversation_id_distinct_from_parent():
    queried = []

    def tracking_lookup(sid: str):
        queried.append(sid)
        return None

    focus = make_source("x:900", conversation_id="x:999")
    bundle = build_context(focus, tracking_lookup)
    assert queried == []
    assert bundle.related == []
    assert bundle.missing_ids == []
    assert bundle.context_status is ContextStatus.complete
