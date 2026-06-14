# Open Questions (for Stage 7)

Things this vault deliberately does **not** assert yet — to be verified in the reverse-engineering stage.

## Graph reading
- [x] **(Stage 7, partial)** Degree-based hub ranking computed: top God-nodes are vendored d3 JS libs
  (measurement artifact); top core hub is `scheduler` (deg≈137). See [[graph-communities]].
  - [ ] Still open: a formal **betweenness/centrality** ranking (not just degree).
- [ ] Give real **names** to the placeholder communities on the bug path (Community 1, Community 58, …) — still open (no LLM).
- [x] **(Stage 7, partial)** Macro subsystem grouping sketched from node counts + degree + communities;
  exact boundaries remain *interpretation* (326 placeholder communities), not edge-proven labels.

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
