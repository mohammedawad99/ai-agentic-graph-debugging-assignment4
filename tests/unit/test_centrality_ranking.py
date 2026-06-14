"""Unit tests for the Stage 12 centrality-based suspect ranking (synthetic fixture)."""

from __future__ import annotations

import json
from pathlib import Path

from ex04_graph_debugger import centrality_ranking as cr

# Small synthetic graph: a relevant low-degree bug node, a high-degree hub with no
# relevance, a vendored JS node (must be excluded), and a non-luigi node (excluded).
NODES = [
    {
        "id": "luigi_parameter_tupleparameter_parse",
        "label": ".parse()",
        "file_type": "code",
        "source_file": "luigi/parameter.py",
        "source_location": "L1095",
    },
    {
        "id": "luigi_parameter_tupleparameter",
        "label": "TupleParameter",
        "file_type": "code",
        "source_file": "luigi/parameter.py",
        "source_location": "L1066",
    },
    {
        "id": "luigi_hub",
        "label": "BigHub",
        "file_type": "code",
        "source_file": "luigi/scheduler.py",
        "source_location": "L1",
    },
    {
        "id": "vendor_d3",
        "label": "d3",
        "file_type": "code",
        "source_file": "luigi/static/visualiser/lib/d3/d3.min.js",
        "source_location": "L1",
    },
    {
        "id": "test_node",
        "label": "SomeTest",
        "file_type": "code",
        "source_file": "test/parameter_test.py",
        "source_location": "L1",
    },
]
LINKS = [
    {"source": "luigi_hub", "target": "a"},
    {"source": "luigi_hub", "target": "b"},
    {"source": "luigi_hub", "target": "c"},
    {"source": "luigi_hub", "target": "d"},
    {"source": "luigi_parameter_tupleparameter", "target": "luigi_parameter_tupleparameter_parse"},
]


def test_degree_map_counts_both_endpoints() -> None:
    deg = cr.degree_map(LINKS)
    assert deg["luigi_hub"] == 4
    assert deg["luigi_parameter_tupleparameter_parse"] == 1


def test_candidate_filter_excludes_vendor_and_nonluigi() -> None:
    assert cr._is_candidate(NODES[0]) is True  # luigi/parameter.py
    assert cr._is_candidate(NODES[3]) is False  # vendored d3 js
    assert cr._is_candidate(NODES[4]) is False  # test/ (not luigi/)


def test_relevance_scores_bug_node_above_hub() -> None:
    rel_bug, _ = cr.relevance_score(NODES[0])  # ".parse()" + parameter.py
    rel_hub, _ = cr.relevance_score(NODES[2])  # "BigHub" + scheduler.py
    assert rel_bug > rel_hub


def test_ranking_includes_bug_node_and_finds_targets() -> None:
    records = cr.rank_suspects(NODES, LINKS)
    ids = [r["node_id"] for r in records]
    assert "luigi_parameter_tupleparameter_parse" in ids  # candidate, ranked
    assert "vendor_d3" not in ids and "test_node" not in ids  # filtered out
    tr = cr._target_rank(records, "luigi_parameter_tupleparameter_parse")
    assert tr["found"] is True and tr["rank"] >= 1
    fr = cr._file_rank(records, "luigi/parameter.py")
    assert fr["found"] is True and fr["nodes_from_file"] == 2


def test_build_report_flags_no_llm_no_cost() -> None:
    rep = cr.build_report(NODES, LINKS)
    assert rep["graphify_used"] is True
    assert rep["llm_used"] is False
    assert rep["api_cost_usd"] == 0
    assert rep["bug_fix_applied_in_this_stage"] is False
    assert rep["graph_summary"]["candidate_nodes_considered"] == 3  # parse, TupleParameter, hub


def test_run_writes_to_tmp_not_tracked_artifacts(tmp_path) -> None:
    prod = Path("artifacts/validation/centrality_suspect_ranking.json")
    before = prod.read_bytes() if prod.exists() else None
    cr.run(out_dir=str(tmp_path))
    data = json.loads((tmp_path / "centrality_suspect_ranking.json").read_text())
    assert data["extension_name"] == "centrality-based suspect ranking"
    assert (prod.read_bytes() if prod.exists() else None) == before  # tracked file untouched
