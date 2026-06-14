"""Unit tests for the Stage 9 graph-guided agent workflow."""

from __future__ import annotations

import json
from pathlib import Path

from ex04_graph_debugger import graph_guided_agent as gga
from ex04_graph_debugger.metrics import MetricsAccumulator, ReadRecord, estimate_tokens


def test_estimate_tokens_chars_div_4() -> None:
    assert estimate_tokens(0) == 0
    assert estimate_tokens(4) == 1
    assert estimate_tokens(97926) == 24482  # matches the Stage 8 baseline method


def test_metrics_accumulator_totals() -> None:
    acc = MetricsAccumulator()
    acc.add(ReadRecord(path="a.md", source_type="obsidian", reason="r", characters=40))
    acc.add(
        ReadRecord(
            path="a.md", source_type="source", reason="r2", characters=60, start_line=1, end_line=3
        )
    )
    s = acc.summary()
    assert s["total_files_read"] == 1  # same path counted once
    assert s["total_text_units_read"] == 2
    assert s["total_characters_read"] == 100
    assert s["estimated_tokens"] == 25


def test_workflow_loads_real_graph_metadata() -> None:
    # The workflow must be able to extract the bug node from the real graph.json.
    from ex04_graph_debugger import agent_state as st
    from ex04_graph_debugger.source_reader import query_graph_subgraph

    subgraph, rec = query_graph_subgraph(st.GRAPH_JSON, st.BUG_NODE_ID, "test")
    assert subgraph["target_node"]["label"] == "TupleParameter"
    assert subgraph["total_nodes_in_graph"] > 1000
    assert rec.source_type == "graphify"


def test_run_produces_expected_flags(tmp_path, monkeypatch) -> None:
    metrics = gga.run()
    assert metrics["graphify_used"] is True
    assert metrics["obsidian_used"] is True
    assert metrics["agent_used"] is True
    assert metrics["llm_used"] is False
    assert metrics["api_cost_usd"] == 0
    assert metrics["bug_fix_applied"] is False
    assert metrics["root_cause_reached"] is True
    assert metrics["investigation_rounds"] == 8
    # Graph-guided run should read far less than the naive baseline.
    assert metrics["estimated_tokens"] < metrics["baseline_reference"]["baseline_estimated_tokens"]


def test_run_does_not_modify_target_source() -> None:
    src = Path("target_repo/luigi_buggy/luigi/parameter.py")
    before = src.read_bytes()
    gga.run()
    assert src.read_bytes() == before  # workflow is read-only on the target


def test_metrics_file_is_valid_json_after_run() -> None:
    gga.run()
    data = json.loads(Path("artifacts/validation/graph_guided_agent_metrics.json").read_text())
    assert data["framework"] == "langgraph"
    assert "TupleParameter" in data["root_cause"]
