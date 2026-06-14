# Graph Communities & Hubs (macro reading)

Initial community/hub notes from `artifacts/graphify/GRAPH_REPORT.md`. Community **names are placeholders**
("Community N") because clustering ran with `--no-label` (no LLM naming) — semantic naming is *planned
(Stage 7)*.

## Macro summary (grounded — `GRAPH_REPORT.md`)
- **6,705 nodes · 13,222 edges · 326 communities** (249 shown, 77 thin omitted).
- Extraction quality: **86% EXTRACTED · 14% INFERRED** (1,877 inferred edges, avg confidence 0.54).
- Token cost: **0** (no LLM).
- The report lists communities as `[[_COMMUNITY_Community N]]` navigation links (Obsidian-compatible).

## Communities relevant to the bug (grounded — member lists in `GRAPH_REPORT.md`)
- **Community 58** (cohesion 0.06, 20 nodes) — *serialization / parameter cluster*: members include
  `JSONEncoder`, `_DictParamEncoder`, `DictParameter`, `_FrozenOrderedDict`, **`ListParameter`** (the bug
  class's base), plus "Parameter whose value is a `list`" and "Parse an individual value from the input."
  → directly relevant to [[parameter-subsystem]] and [[hot]].
- **Community 1** (cohesion 0.03, 53 nodes) — *command-line cluster*: members include `CmdlineParser`,
  `ChoiceParameter`, "Load the --module parameter", "Helper for parsing command line arguments." The bug
  node has an INFERRED `uses` edge into this cluster.

## Hubs (Stage 7 — degree from `graph.json`)
Initial degree (in+out) ranking computed from `graph.json` edges:
- **Highest degree overall = vendored JS libs:** `d3.min.js` (deg≈481), `dagre-d3.min.js` (deg≈218) under
  `luigi/static/visualiser/`. These are **graph God-nodes but NOT core architecture** — a measurement
  artifact from bundling the web UI.
- **Highest-degree CORE nodes:** `MockTarget` (test utility, deg≈250), `luigi` package root (≈223),
  **`scheduler`** (`luigi_scheduler_scheduler`, deg≈137), `six` compat (≈114).
- **Reading:** the runtime center of mass is the **scheduler/worker** core; `parameter.py` (111 nodes) is a
  mid-sized, well-defined subsystem where the bug lives.
- **Still placeholder / open:** real community *names* (no LLM) and a formal centrality (betweenness)
  ranking — see [[open-questions]] and [[reverse-engineering-analysis]].

## What needs Stage 7 verification
- Real names for Community 1 / Community 58 (and others on the bug path).
- Degree/centrality-based hub ranking (macro → meso → micro).
- Whether any community is an over-connected bottleneck.

Links: [[architecture-map]] · [[parameter-subsystem]] · [[hot]] · [[graphify-overview]] · [[open-questions]]
