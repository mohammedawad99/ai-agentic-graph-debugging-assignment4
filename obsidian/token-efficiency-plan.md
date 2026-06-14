# Token-Efficiency Plan (preparation only)

Prepares the later baseline-vs-graph-guided comparison (Stage 11). **No final comparison numbers here** —
only already-measured Graphify artifact facts. All future numbers will be labeled
**measured / estimated / manual**.

## Already-measured facts (grounded)
- Graphify build **token cost: 0 input / 0 output** (no LLM; AST/no-key route).
- Graph size: `graph.json` = **6,771 nodes / 15,365 links** (6.0 MB); `GRAPH_REPORT.md` 92 KB; `GRAPH_TREE.html` 460 KB.
- The graph + `GRAPH_REPORT.md` are the **shared input** the graph-guided workflow will consult before reading raw code.

## What the comparison will measure (Stage 11)
Two workflows, same bug (`TupleParameter.parse`), same model, same success criterion (regression test passes):

| Metric | Baseline (naive) | Graph-guided | Provenance (later) |
|--------|------------------|--------------|--------------------|
| Total tokens (prompt+completion) | _tbd_ | _tbd_ | measured/estimated |
| Files / text units read | _tbd_ | _tbd_ | measured |
| Iterations / agent steps | _tbd_ | _tbd_ | measured |
| Reached correct fix? | _tbd_ | _tbd_ | observed |
| Steps to root cause | _tbd_ | _tbd_ | measured |

## Why graph-guidance should help (hypothesis — to verify)
- The bug node and its neighborhood are directly addressable in `graph.json`
  (`luigi_parameter_tupleparameter` → `.parse()`), so a graph-guided agent can jump to
  `luigi/parameter.py` instead of scanning 244 files / ~58k LOC.
- This is a **hypothesis**, not a result; the real numbers come from Stage 11.

Links: [[bug-investigation-seed]] · [[graphify-overview]] · [[index]]
