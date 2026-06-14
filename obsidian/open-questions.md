# Open Questions (for Stage 7)

Things this vault deliberately does **not** assert yet — to be verified in the reverse-engineering stage.

## Graph reading
- [ ] Rank true **hubs / God nodes / bottlenecks** by degree/centrality from `graph.json`
  (candidates to check: `scheduler.py`, `task.py`, `worker.py`, `parameter.py`).
- [ ] Give real **names** to the placeholder communities on the bug path (Community 1, Community 58, …).
- [ ] Confirm the macro subsystem grouping in [[architecture-map]] against actual edges (not just file paths).

## Bug path
- [ ] Enumerate **callers** of `TupleParameter.parse` / `ListParameter.parse` from `graph.json` edges.
- [ ] Trace the full path: public API (`luigi.TupleParameter`) → `parse` → config/CLI inputs → test.
- [ ] Confirm the INFERRED `uses → CmdlineParser` edge corresponds to a real call path (INFERRED, conf may be low).

## Evidence quality
- [ ] Decide how to treat the 14% INFERRED edges (avg confidence 0.54) when reasoning about call paths.
- [ ] Reconcile the 6,771/15,365 (graph.json) vs 6,705/13,222 (report) counts in the Stage 7 write-up.

## Later stages
- [ ] Stage 10: reproduce failing-before / passing-after in this repo under Docker.
- [ ] Stage 11: fill the [[token-efficiency-plan]] table with labeled measurements.

Back to [[index]] · related: [[graph-communities]] · [[bug-investigation-seed]]
