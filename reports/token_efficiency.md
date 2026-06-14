# Token-Efficiency Comparison (PLACEHOLDER)

> Status: **placeholder**. Produced in the agent-workflow stage. All numbers will be labeled
> **measured / estimated / manual count** (see `docs/COSTS.md`). No values are filled yet.

## Planned comparison table
| Metric | Baseline (naive) | Graph-guided | Provenance |
|--------|------------------|--------------|------------|
| Total tokens (prompt+completion) | _tbd_ | _tbd_ | measured |
| Files / text units read | _tbd_ | _tbd_ | measured |
| Iterations / agent steps | _tbd_ | _tbd_ | measured |
| Wall-clock (info) | _tbd_ | _tbd_ | measured |
| Reached correct fix? | _tbd_ | _tbd_ | observed |

## Method (to finalize)
- Same bug, same model, same success criterion (regression test passes).
- Baseline explores without the graph; graph-guided uses `graph.json` hubs/paths.
- Counters implemented in `src/ex04_graph_debugger/`; raw logs saved under `artifacts/validation/`.

_No results yet._
