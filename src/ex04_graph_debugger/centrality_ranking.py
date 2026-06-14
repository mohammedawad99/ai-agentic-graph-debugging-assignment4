"""Original extension (Stage 12): centrality-based suspect ranking.

Deterministic, no-LLM, stdlib-only triage heuristic. Reads the committed Graphify
graph read-only and ranks Luigi *production* code nodes by a transparent blend of
graph centrality (normalized degree) and keyword relevance to the bug query terms.
Run:  uv run python -m ex04_graph_debugger.centrality_ranking
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

GRAPH_JSON = "artifacts/graphify/graph.json"
QUERY_TERMS = ["tuple", "parameter", "parse", "serialize", "json", "literal_eval",
               "typeerror", "iterable", "list"]  # fmt: skip
W_REL, W_CEN = 0.6, 0.4
TARGET_FILE = "luigi/parameter.py"
TUPLE_NODE = "luigi_parameter_tupleparameter"
PARSE_NODE = "luigi_parameter_tupleparameter_parse"
OUT = {
    "json": "artifacts/validation/centrality_suspect_ranking.json",
    "csv": "artifacts/validation/centrality_suspect_ranking.csv",
    "top": "artifacts/validation/centrality_suspect_ranking_top20.txt",
}
CSV_COLS = ["rank", "node_id", "label", "path", "degree",
            "normalized_centrality", "relevance_score", "final_score"]  # fmt: skip
_VENDOR_EXT = (".js", ".css", ".html", ".woff", ".woff2", ".ttf", ".eot", ".svg")


def _is_vendor(source_file: str) -> bool:
    s = (source_file or "").lower()
    return "static/visualiser" in s or s.endswith(_VENDOR_EXT)


def _is_candidate(node: dict) -> bool:
    """Luigi production code only (excludes vendored web assets, tests, rationale)."""
    sf = str(node.get("source_file", ""))
    return node.get("file_type") == "code" and sf.startswith("luigi/") and not _is_vendor(sf)


def load_graph(path: str = GRAPH_JSON) -> tuple[list, list]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("nodes", []), data.get("links", [])


def degree_map(links: list) -> Counter:
    deg: Counter = Counter()
    for ln in links:
        deg[ln.get("source")] += 1
        deg[ln.get("target")] += 1
    return deg


def relevance_score(node: dict) -> tuple[float, int]:
    keys = ("label", "source_file", "source_location", "id")
    text = " ".join(str(node.get(k, "")) for k in keys).lower()
    hits = sum(1 for t in QUERY_TERMS if t in text)
    return round(hits / len(QUERY_TERMS), 4), hits


def rank_suspects(nodes: list, links: list) -> list[dict]:
    deg = degree_map(links)
    candidates = [n for n in nodes if _is_candidate(n)]
    max_deg = max((deg[n["id"]] for n in candidates), default=1) or 1
    records = []
    for n in candidates:
        d = deg[n["id"]]
        norm = round(d / max_deg, 4)
        rel, hits = relevance_score(n)
        final = round(W_REL * rel + W_CEN * norm, 4)
        records.append({
            "node_id": n["id"], "label": n.get("label"), "path": n.get("source_file"),
            "source_location": n.get("source_location"), "degree": d,
            "normalized_centrality": norm, "relevance_score": rel, "relevance_hits": hits,
            "final_score": final, "reason": f"{hits} term hit(s); degree {d} (norm {norm})",
        })  # fmt: skip
    records.sort(key=lambda r: (r["final_score"], r["relevance_score"], r["degree"]), reverse=True)
    for i, r in enumerate(records, 1):
        r["rank"] = i
    return records


def _target_rank(records: list[dict], node_id: str) -> dict:
    for r in records:
        if r["node_id"] == node_id:
            return {"found": True, "rank": r["rank"], "final_score": r["final_score"]}
    return {"found": False, "rank": None, "final_score": None}


def _file_rank(records: list[dict], path: str) -> dict:
    hits = [r for r in records if r["path"] == path]
    best = hits[0]["rank"] if hits else None
    return {"found": bool(hits), "best_rank": best, "nodes_from_file": len(hits)}


def build_report(nodes: list, links: list, top_n: int = 25) -> dict:
    records = rank_suspects(nodes, links)
    return {
        "created_at_utc": "2026-06-14",
        "extension_name": "centrality-based suspect ranking",
        "graph_source": GRAPH_JSON,
        "graphify_used": True,
        "obsidian_used": False,
        "llm_used": False,
        "api_cost_usd": 0,
        "bug_fix_applied_in_this_stage": False,
        "method": {
            "centrality": "degree centrality (full graph), normalized by max candidate degree",
            "relevance_query_terms": QUERY_TERMS,
            "scoring_formula": f"final = {W_REL}*relevance + {W_CEN}*normalized_centrality",
            "candidate_filter": "code under luigi/, excluding vendored web assets",
        },
        "graph_summary": {
            "total_nodes": len(nodes),
            "total_links": len(links),
            "candidate_nodes_considered": len(records),
        },
        "ranking": records[:top_n],
        "known_bug_targets": {
            "parameter_py": _file_rank(records, TARGET_FILE),
            "TupleParameter": _target_rank(records, TUPLE_NODE),
            "TupleParameter_parse": _target_rank(records, PARSE_NODE),
        },
        "limitations": (
            "Centrality + keyword relevance is a triage heuristic, NOT proof of causality. It does "
            "not always find bugs and does not prove a root cause; it ranks where to look first. "
            "Degree is a coarse centrality; results depend on the query terms and the filter."
        ),
        "_all_records": records,
    }


def _persist(report: dict, out_dir: str | None = None) -> None:
    base = Path(out_dir) if out_dir else None
    paths = {k: (base / Path(v).name if base else Path(v)) for k, v in OUT.items()}
    records = report.pop("_all_records")
    paths["json"].parent.mkdir(parents=True, exist_ok=True)
    paths["json"].write_text(json.dumps(report, indent=2), encoding="utf-8")
    with paths["csv"].open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLS)
        w.writerows([[r[c] for c in CSV_COLS] for r in records])
    top = ["# Centrality-based suspect ranking — top 20 (Luigi production code)"]
    for r in records[:20]:
        top.append(
            f"{r['rank']:2d}. {r['label']}  [{r['path']}:{r['source_location']}]  "
            f"final={r['final_score']} rel={r['relevance_score']} ndeg={r['normalized_centrality']}"  # noqa: E501
        )
    paths["top"].write_text("\n".join(top) + "\n", encoding="utf-8")


def run(out_dir: str | None = None) -> dict:
    nodes, links = load_graph()
    report = build_report(nodes, links)
    _persist(dict(report), out_dir)
    return report


def main() -> None:
    r = run()
    print(json.dumps({
        "candidate_nodes": r["graph_summary"]["candidate_nodes_considered"],
        "known_bug_targets": r["known_bug_targets"],
        "top3": [(x["rank"], x["label"], x["final_score"]) for x in r["ranking"][:3]],
    }, indent=2))  # fmt: skip


if __name__ == "__main__":
    main()
