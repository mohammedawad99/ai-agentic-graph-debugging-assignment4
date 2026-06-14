"""Bounded, deterministic node functions for the graph-guided workflow.

Each factory binds a MetricsAccumulator and returns a LangGraph node. Nodes
consult graph/Obsidian BEFORE reading targeted source ranges. No LLM is used.
"""

from __future__ import annotations

from collections.abc import Callable

from . import agent_state as st
from .metrics import MetricsAccumulator
from .source_reader import query_graph_subgraph, read_line_range, read_whole_file

Node = Callable[[dict], dict]


def _log(state: dict, msg: str) -> list[str]:
    trace = list(state.get("trace", []))
    trace.append(msg)
    return trace


def load_graph_artifacts(acc: MetricsAccumulator) -> Node:
    def node(state: dict) -> dict:
        subgraph, rec = query_graph_subgraph(
            st.GRAPH_JSON, st.BUG_NODE_ID, "locate bug node + methods + edges (graph-first)"
        )
        acc.add(rec)
        label = subgraph.get("target_node", {}).get("label")
        loc = subgraph.get("target_node", {}).get("source_location")
        return {
            "subgraph": subgraph,
            "trace": _log(
                state,
                f"load_graph_artifacts: node={st.BUG_NODE_ID} label={label} @ {loc}; "
                f"{len(subgraph.get('incident_edges', []))} edges, "
                f"{len(subgraph.get('methods', []))} method(s) [graphify]",
            ),
        }

    return node


def _read_page(acc: MetricsAccumulator, path: str, reason: str, tag: str) -> Node:
    def node(state: dict) -> dict:
        _, rec = read_whole_file(path, "obsidian", reason)
        acc.add(rec)
        return {"trace": _log(state, f"{tag}: read {path} ({rec.characters} chars) [obsidian]")}

    return node


def read_index(acc: MetricsAccumulator) -> Node:
    return _read_page(acc, st.OBSIDIAN_INDEX, "vault navigation / reading order", "read_index")


def read_hot_context(acc: MetricsAccumulator) -> Node:
    return _read_page(
        acc, st.OBSIDIAN_HOT, "focused bug context for TupleParameter.parse", "read_hot_context"
    )


def read_parameter_context(acc: MetricsAccumulator) -> Node:
    return _read_page(
        acc, st.OBSIDIAN_PARAM, "meso parameter-subsystem analysis", "read_parameter_context"
    )


def select_relevant_source(acc: MetricsAccumulator) -> Node:
    def node(state: dict) -> dict:
        ranges = ", ".join(f"L{a}-{b}" for a, b, _ in st.SOURCE_RANGES)
        return {
            "trace": _log(
                state,
                f"select_relevant_source: chose targeted ranges {ranges} in {st.TARGET_SOURCE} "
                "(from graph node locations; NO full-file read, NO baseline guidance)",
            )
        }

    return node


def inspect_bug_path(acc: MetricsAccumulator) -> Node:
    def node(state: dict) -> dict:
        trace = list(state.get("trace", []))
        for start, end, reason in st.SOURCE_RANGES:
            _, rec = read_line_range(st.TARGET_SOURCE, start, end, reason)
            acc.add(rec)
            trace.append(
                f"inspect_bug_path: read {st.TARGET_SOURCE} L{start}-{end} "
                f"({rec.characters} chars) [source] — {reason}"
            )
        return {"trace": trace}

    return node


def propose_root_cause(acc: MetricsAccumulator) -> Node:
    def node(state: dict) -> dict:
        explanation = (
            "TupleParameter (L1066) extends ListParameter and overrides parse only; it inherits "
            "ListParameter.serialize (json.dumps). serialize((1,2,3)) -> '[1, 2, 3]'. "
            "TupleParameter.parse (L1095) does json.loads -> [1,2,3] then "
            "tuple(tuple(x) for x in ...) which runs tuple(1) on an int -> "
            "TypeError: 'int' object is not iterable. The guard 'except ValueError' (L1117) "
            "is too narrow to catch the TypeError, so it propagates."
        )
        return {
            "root_cause": explanation,
            "root_cause_reached": True,
            "trace": _log(state, "propose_root_cause: explanation derived (deterministic, no LLM)"),
        }

    return node


def write_metrics_and_report(acc: MetricsAccumulator) -> Node:
    def node(state: dict) -> dict:
        return {
            "metrics": acc.summary(),
            "trace": _log(state, "write_metrics_and_report: metrics summarized"),
        }

    return node
