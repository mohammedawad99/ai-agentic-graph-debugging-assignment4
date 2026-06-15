# Index — Luigi Bug 3 Knowledge Vault

Navigation hub for the Assignment 04 knowledge vault. This is the **final repository knowledge vault**:
pages are grounded in the **real Graphify artifacts** (`artifacts/graphify/graph.json`,
`GRAPH_REPORT.md`) and the **vendored source** (`target_repo/luigi_buggy/`). Facts are tagged
**EXTRACTED / INFERRED / interpretation** at point of use.

## How to read this vault (recommended order)
1. **[[graphify-overview]]** — how the graph was built (no-LLM AST route) and what artifacts exist.
2. **[[architecture-map]]** — macro view of the codebase from the graph + source paths.
3. **[[graph-communities]]** — communities/hubs from `GRAPH_REPORT.md` (macro reading).
4. **[[parameter-subsystem]]** — meso view: the parameter classes around the bug.
5. **[[hot]]** — micro view: the focused bug context (`TupleParameter.parse`).
6. **[[reverse-engineering-analysis]]** — macro→meso→micro analysis (evidence-tagged).
7. **[[research-questions]]** — explicit answers to the eight assignment research questions (RQ1–RQ8).
8. **[[bug-investigation-seed]]** — the original investigation seed (historical context).
9. **[[token-efficiency-plan]]** — the design the baseline-vs-graph comparison followed (now measured in
   `reports/token_efficiency.md`).

## Supporting pages
- [[sources]] — provenance: every artifact/source path this vault relies on.
- [[open-questions]] — questions raised during the investigation and how they were resolved.
- [[README]] — what this directory is and how to open it.

## Target at a glance (grounded)
- **Project:** Luigi (workflow / DAG engine), via BugsInPy — buggy commit `a0f1db01…`.
- **Bug:** 3 — `TupleParameter.parse` in `luigi/parameter.py`.
- **Graph node:** `luigi_parameter_tupleparameter` → `TupleParameter` @ `luigi/parameter.py:L1066`
  (method node `luigi_parameter_tupleparameter_parse` → `.parse()` @ `L1095`).
- **Graph size:** `graph.json` = **6,771 nodes / 15,365 links**; `GRAPH_REPORT.md` = **6,705 nodes /
  13,222 edges / 326 communities** (post-dedup view). **Token cost: 0** (no LLM used).

## Status note
This is the **final repository knowledge vault**. The macro/meso/micro interpretation, hub/centrality
reading, and the bug fix are all complete: the bug is **fixed** in
`target_repo/luigi_buggy/luigi/parameter.py` (Stage 10) with before/after proof in
`reports/bug_fix_validation.md`, and the full reverse-engineering analysis is in
[[reverse-engineering-analysis]] / `reports/reverse_engineering.md`. Each claim remains tagged
**EXTRACTED / INFERRED / interpretation** so graders can separate graph facts from analysis.
