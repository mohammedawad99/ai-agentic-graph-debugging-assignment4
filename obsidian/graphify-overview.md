# Graphify Overview

How the code graph for this vault was produced. Grounded in `reports/graphify_run.md`,
`artifacts/graphify/graphify_run.log`, and `artifacts/graphify/GRAPH_REPORT.md`.

## Tool
- **Graphify 0.8.39** (official PyPI package **`graphifyy`**, CLI `graphify`), installed via
  `uv tool install graphifyy`. (See `docs/DECISIONS.md` **D-008**.)

## Command path (no-LLM / no API key)
The vendored tree contains docs + web-asset images, so `graphify extract` demanded an LLM key. We used the
**no-LLM code path** instead (the tool states "a code-only corpus needs no key"):
```
graphify update target_repo/luigi_buggy --no-cluster        # AST build, no key
graphify cluster-only target_repo/luigi_buggy --no-label    # clustering + GRAPH_REPORT.md (placeholder names)
graphify tree --graph .../graph.json --output .../GRAPH_TREE.html --label luigi_buggy
```
- **No LLM semantic extraction was used** (`--no-label` skips LLM community naming; the INFERRED edges come
  from Graphify's AST/static heuristics, not from an LLM call).

## Artifacts (`artifacts/graphify/`)
| File | What it is | Size |
|------|------------|------|
| `graph.json` | machine-readable graph (nodes + links) | ~6.0 MB |
| `GRAPH_REPORT.md` | human report (summary, communities, Obsidian `[[links]]`) | ~92 KB |
| `GRAPH_TREE.html` | interactive D3 collapsible-tree visual | ~460 KB |
| `.graphify_labels.json`, `.graphify_root` | graph metadata | small |
| `manifest.json` | corpus scan manifest | ~57 KB |
| `graphify_run.log` | full command/run log | small |

## Counts (grounded; both numbers are real)
- **`graph.json`:** 6,771 nodes · 15,365 links · `input_tokens: 0` · `output_tokens: 0`.
- **`GRAPH_REPORT.md`:** 6,705 nodes · 13,222 edges · 326 communities (249 shown, 77 thin omitted);
  extraction 86% EXTRACTED / 14% INFERRED (1,877 inferred edges, avg confidence 0.54).
- The small difference (6,771/15,365 vs 6,705/13,222) is from `cluster-only` deduping same-named symbols
  while refusing to shrink the authoritative `graph.json`. Documented in `reports/graphify_run.md` §9.

## Token cost
**0 input / 0 output** — confirmed in `graph.json` and `GRAPH_REPORT.md`. No paid API used.

## Visual
`GRAPH_TREE.html` was generated because the default force-directed `graph.html` is skipped above 5,000
nodes (tool limit).

Related: [[graph-communities]] · [[architecture-map]] · [[index]]
