"""State and constants for the graph-guided LangGraph workflow."""

from __future__ import annotations

from typing import TypedDict

# Repo-relative input locations (graph/Obsidian consulted BEFORE source).
GRAPH_JSON = "artifacts/graphify/graph.json"
OBSIDIAN_INDEX = "obsidian/index.md"
OBSIDIAN_HOT = "obsidian/hot.md"
OBSIDIAN_PARAM = "obsidian/parameter-subsystem.md"
TARGET_SOURCE = "target_repo/luigi_buggy/luigi/parameter.py"

# The graph node that identifies the bug class (known from Graphify, Stage 5/7).
BUG_NODE_ID = "luigi_parameter_tupleparameter"

# Targeted source ranges (chosen FROM the graph node locations, not by scanning).
# Parameter basics, ListParameter (incl. inherited serialize), TupleParameter (bug).
SOURCE_RANGES = [
    (90, 135, "Parameter base class basics (graph node @ L93)"),
    (
        1006,
        1066,
        "ListParameter parse/serialize — inherited serialize is json.dumps (graph node @ L1006)",
    ),
    (1066, 1120, "TupleParameter class + overridden parse — bug method (graph node @ L1066/L1095)"),
]

# Output locations.
METRICS_OUT = "artifacts/validation/graph_guided_agent_metrics.json"
TRACE_OUT = "artifacts/validation/graph_guided_agent_trace.log"
FILES_READ_OUT = "artifacts/validation/graph_guided_agent_files_read.txt"

# Baseline reference (Stage 8, commit 8904b57) — context only, NOT navigation input.
BASELINE_REFERENCE = {
    "baseline_estimated_tokens": 24482,
    "baseline_files_read": 4,
    "baseline_rounds": 5,
}


class AgentState(TypedDict, total=False):
    """Workflow state threaded through the LangGraph nodes."""

    trace: list[str]  # human-readable step log
    subgraph: dict  # extracted graph facts about the bug node
    root_cause: str  # explanation produced by propose_root_cause
    root_cause_reached: bool
    metrics: dict  # final metrics summary
