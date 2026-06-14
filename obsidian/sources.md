# Sources & Provenance

Every artifact this vault relies on. No claim in the vault should go beyond these.

## Graph artifacts (Stage 5 — committed `feb78ea`)
- `artifacts/graphify/graph.json` — 6,771 nodes / 15,365 links; keys `nodes, links, input_tokens, output_tokens`.
- `artifacts/graphify/GRAPH_REPORT.md` — 6,705 nodes / 13,222 edges / 326 communities; 86% EXTRACTED / 14% INFERRED.
- `artifacts/graphify/GRAPH_TREE.html` — interactive visual.
- `artifacts/graphify/manifest.json`, `.graphify_labels.json`, `.graphify_root`, `graphify_run.log` — metadata/log.
- `reports/graphify_run.md` — run report (commands, counts, evidence).

## Vendored source (Stage 4 — committed `1299535`)
- `target_repo/luigi_buggy/luigi/parameter.py` — bug file (`TupleParameter` L1066, `.parse()` L1095).
- Buggy commit: `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`; LICENSE preserved (Apache-2.0).

## Prior validation evidence
- `reports/bug_validation.md` — candidate-repo fail→pass under Docker/Python 3.8.20 (`TypeError: 'int' object is not iterable`).

## Project docs
- `docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`, `docs/DECISIONS.md` (D-007 vendoring, D-008 Graphify).

Back to [[index]].
