"""Read-only context readers that produce tracked ReadRecords.

These helpers never modify any file. They are the only way the graph-guided
workflow consumes context, so every read is measured.
"""

from __future__ import annotations

import json
from pathlib import Path

from .metrics import ReadRecord


def read_whole_file(path: str, source_type: str, reason: str) -> tuple[str, ReadRecord]:
    """Read an entire small text file (e.g. an Obsidian page)."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    return text, ReadRecord(path=path, source_type=source_type, reason=reason, characters=len(text))


def read_line_range(
    path: str, start: int, end: int, reason: str, source_type: str = "source"
) -> tuple[str, ReadRecord]:
    """Read an inclusive 1-based line range from a source file (targeted, not full-file)."""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines(True)
    end = min(end, len(lines))
    text = "".join(lines[start - 1 : end])
    rec = ReadRecord(
        path=path,
        source_type=source_type,
        reason=reason,
        characters=len(text),
        start_line=start,
        end_line=end,
    )
    return text, rec


def query_graph_subgraph(graph_path: str, node_id: str, reason: str) -> tuple[dict, ReadRecord]:
    """Parse graph.json programmatically and extract ONLY the relevant sub-graph.

    The full graph.json is parsed (a navigation cost, not LLM context); the
    *context consumed* is the small extracted subgraph (the target node, its
    methods, and incident edges). Only that small extract is measured.
    """
    data = json.loads(Path(graph_path).read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    links = data.get("links", [])
    target = nodes.get(node_id)
    incident = [ln for ln in links if ln.get("source") == node_id or ln.get("target") == node_id]
    method_ids = {ln["target"] for ln in incident if ln.get("relation") == "method"}
    methods = [nodes[m] for m in method_ids if m in nodes]
    subgraph = {
        "target_node": target,
        "methods": methods,
        "incident_edges": incident,
        "total_nodes_in_graph": len(nodes),
        "total_links_in_graph": len(links),
    }
    extract = json.dumps(subgraph, indent=0)
    rec = ReadRecord(
        path=graph_path,
        source_type="graphify",
        reason=reason,
        characters=len(extract),
    )
    return subgraph, rec
