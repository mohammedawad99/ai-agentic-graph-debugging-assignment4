"""Stage 9 — bounded, deterministic graph-guided agent (LangGraph).

Consults Graphify + Obsidian BEFORE reading targeted source ranges, and measures
files/text-units/tokens/rounds for the later (Stage 11) comparison. No LLM/API is used.
Run:  uv run python -m ex04_graph_debugger.graph_guided_agent
"""

from __future__ import annotations

import json
from pathlib import Path

from langgraph.graph import END, START, StateGraph

from . import agent_state as st
from . import nodes
from .agent_state import AgentState
from .metrics import MetricsAccumulator

# Ordered, bounded states (graph/Obsidian first, source last). 8 states.
ORDER = [
    "load_graph_artifacts",
    "read_index",
    "read_hot_context",
    "read_parameter_context",
    "select_relevant_source",
    "inspect_bug_path",
    "propose_root_cause",
    "write_metrics_and_report",
]


def build_graph(acc: MetricsAccumulator):
    g = StateGraph(AgentState)
    factories = {
        "load_graph_artifacts": nodes.load_graph_artifacts,
        "read_index": nodes.read_index,
        "read_hot_context": nodes.read_hot_context,
        "read_parameter_context": nodes.read_parameter_context,
        "select_relevant_source": nodes.select_relevant_source,
        "inspect_bug_path": nodes.inspect_bug_path,
        "propose_root_cause": nodes.propose_root_cause,
        "write_metrics_and_report": nodes.write_metrics_and_report,
    }
    for name in ORDER:
        g.add_node(name, factories[name](acc))
    g.add_edge(START, ORDER[0])
    for a, b in zip(ORDER, ORDER[1:], strict=False):
        g.add_edge(a, b)
    g.add_edge(ORDER[-1], END)
    return g.compile()


def run() -> dict:
    """Execute the workflow and return the full metrics dict."""
    acc = MetricsAccumulator()
    app = build_graph(acc)
    final = app.invoke({"trace": []})

    summary = final["metrics"]
    metrics = {
        "created_at_utc": "2026-06-14",
        **summary,
        "investigation_rounds": len(ORDER),
        "root_cause_reached": bool(final.get("root_cause_reached")),
        "graphify_used": True,
        "obsidian_used": True,
        "agent_used": True,
        "llm_used": False,
        "api_cost_usd": 0,
        "bug_fix_applied": False,
        "framework": "langgraph",
        "baseline_reference": st.BASELINE_REFERENCE,
        "root_cause": final.get("root_cause", ""),
    }
    _persist(metrics, final.get("trace", []))
    return metrics


def _persist(metrics: dict, trace: list[str]) -> None:
    Path("artifacts/validation").mkdir(parents=True, exist_ok=True)
    Path(st.METRICS_OUT).write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    lines = ["# Graph-guided agent trace (LangGraph; graph/Obsidian-first; no LLM)"]
    lines += [f"{i + 1:2d}. {msg}" for i, msg in enumerate(trace)]
    et = metrics["estimated_tokens"]
    lines += [
        "",
        f"files_read={metrics['total_files_read']} text_units={metrics['total_text_units_read']} "
        f"chars={metrics['total_characters_read']} estimated_tokens={et} "
        f"rounds={metrics['investigation_rounds']} "
        f"root_cause_reached={metrics['root_cause_reached']}",
        f"graphify_used={metrics['graphify_used']} obsidian_used={metrics['obsidian_used']} "
        f"agent_used={metrics['agent_used']} llm_used={metrics['llm_used']} "
        f"api_cost_usd={metrics['api_cost_usd']} bug_fix_applied={metrics['bug_fix_applied']}",
    ]
    Path(st.TRACE_OUT).write_text("\n".join(lines) + "\n", encoding="utf-8")

    fr = ["# Graph-guided agent — text units read (targeted; graph/Obsidian-first)"]
    for r in metrics["records"]:
        rng = f" L{r['start_line']}-{r['end_line']}" if r.get("start_line") else ""
        fr.append(
            f"[{r['source_type']}] {r['path']}{rng}  chars={r['characters']} "
            f"est_tokens={r['estimated_tokens_chars_div_4']}  — {r['reason']}"
        )
    fr.append(f"\nTOTAL chars={metrics['total_characters_read']} est_tokens={et}")
    Path(st.FILES_READ_OUT).write_text("\n".join(fr) + "\n", encoding="utf-8")


def main() -> None:
    m = run()
    print(
        json.dumps(
            {
                k: m[k]
                for k in (
                    "total_files_read",
                    "total_text_units_read",
                    "total_characters_read",
                    "estimated_tokens",
                    "investigation_rounds",
                    "root_cause_reached",
                    "graphify_used",
                    "obsidian_used",
                    "agent_used",
                    "llm_used",
                    "api_cost_usd",
                    "bug_fix_applied",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
