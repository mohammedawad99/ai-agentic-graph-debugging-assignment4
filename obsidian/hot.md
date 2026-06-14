# Hot — Hubs & Hotspots (PLACEHOLDER)

> Status: **skeleton**. Real hubs/hotspots are derived from `artifacts/graphify/graph.json` after the Graphify run.
> No node/edge metrics are claimed yet.

## What this page will contain
- **Hubs:** highest-degree nodes (functions/classes/modules most connected in the code graph).
- **Hotspots:** code central to the bug's call paths (around `TupleParameter.parse`).
- **Communities:** clusters (e.g., core `task`/`parameter`/`scheduler`/`worker` vs `contrib`).
- **Paths:** routes from public API (`luigi.TupleParameter`) to the defect and its tests.

## Expected hot candidates (hypothesis only — to be verified from the graph)
- `luigi/parameter.py` — `Parameter`, `ListParameter`, `TupleParameter` (defect lives here)
- `luigi/task.py` — `Task` (central type many parameters attach to)
- `luigi/scheduler.py`, `luigi/worker.py` — execution hubs

> These are **hypotheses**, not measurements. They will be replaced by graph-derived rankings,
> each with its degree/centrality value labeled as **measured** from `graph.json`.

Back to [[index]].
