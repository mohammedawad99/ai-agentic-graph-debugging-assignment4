# Index — Luigi Bug 3 Knowledge Vault

Navigation hub for the Assignment 04 knowledge vault. Pages are grounded in the **real Graphify
artifacts** (`artifacts/graphify/graph.json`, `GRAPH_REPORT.md`) and the **vendored source**
(`target_repo/luigi_buggy/`). Anything not yet verified is labeled *planned (Stage 7)*.

## How to read this vault (recommended order)
1. **[[graphify-overview]]** — how the graph was built (no-LLM AST route) and what artifacts exist.
2. **[[architecture-map]]** — macro view of the codebase from the graph + source paths.
3. **[[graph-communities]]** — communities/hubs from `GRAPH_REPORT.md` (macro reading).
4. **[[parameter-subsystem]]** — meso view: the parameter classes around the bug.
5. **[[hot]]** — micro view: the focused bug context (`TupleParameter.parse`).
6. **[[reverse-engineering-analysis]]** — Stage 7 macro→meso→micro analysis (evidence-tagged).
7. **[[bug-investigation-seed]]** — seed for the later investigation (Stages 8–10).
8. **[[token-efficiency-plan]]** — what the later baseline-vs-graph comparison will measure.

## Supporting pages
- [[sources]] — provenance: every artifact/source path this vault relies on.
- [[open-questions]] — what Stage 7 still needs to verify.
- [[README]] — what this directory is and how to open it.

## Target at a glance (grounded)
- **Project:** Luigi (workflow / DAG engine), via BugsInPy — buggy commit `a0f1db01…`.
- **Bug:** 3 — `TupleParameter.parse` in `luigi/parameter.py`.
- **Graph node:** `luigi_parameter_tupleparameter` → `TupleParameter` @ `luigi/parameter.py:L1066`
  (method node `luigi_parameter_tupleparameter_parse` → `.parse()` @ `L1095`).
- **Graph size:** `graph.json` = **6,771 nodes / 15,365 links**; `GRAPH_REPORT.md` = **6,705 nodes /
  13,222 edges / 326 communities** (post-dedup view). **Token cost: 0** (no LLM used).

## Honesty note
This is an **early knowledge vault**, not the final reverse-engineering analysis. Final macro/meso/micro
interpretation, hub/bottleneck ranking, and the bug fix all happen in later stages.
