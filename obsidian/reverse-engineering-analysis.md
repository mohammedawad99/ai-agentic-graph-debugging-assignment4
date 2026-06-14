# Reverse Engineering Analysis (Stage 7)

Evidence-based macro→meso→micro read of Luigi, centered on the bug. Full version:
`reports/reverse_engineering.md`. Tags: **EXTRACTED** (in graph/source), **INFERRED** (Graphify heuristic),
*interpretation*.

## Macro (whole system)
- **Core code mass (EXTRACTED node counts):** `scheduler.py` (135), **`parameter.py` (111)**, `format.py`
  (83), `worker.py` (79), plus a large `contrib/` layer and a heavy test surface.
- **Core hubs by degree (EXTRACTED):** `scheduler` (deg≈137), `luigi` package root (≈223), `MockTarget`
  (test util, ≈250). → Luigi reads as a **scheduler/worker DAG engine**.
- **Caveat (honesty):** the *highest*-degree nodes are **vendored d3 JS libs** (`d3.min.js` ≈481) under
  `static/visualiser/` — graph God-nodes, **not** core architecture. Community names are placeholders
  (`--no-label`), so subsystem boundaries are *interpretation*, not proven labels.

## Meso (parameter subsystem)
- Family (EXTRACTED, `luigi/parameter.py`): `Parameter` (L93) → `ListParameter` (L1006) → `TupleParameter`
  (L1066); sibling `DictParameter` (L950). See [[parameter-subsystem]].
- **Key finding:** `TupleParameter` **overrides `parse` only** and **inherits `ListParameter.serialize`
  (`json.dumps`)** — there is no serialize node for it in the graph. This serialize/parse **asymmetry** is
  why the bug exists.
- Parameter values flow in from **CLI/config** (CmdlineParser @ `cmdline_parser.py:L28`); the
  parameter→CLI graph edge is **INFERRED**, but the source docstring confirms config/CLI string inputs.
- Clusters: **Community 58** (parameter/serialization) and **Community 1** (command-line). See [[graph-communities]].

## Micro (the bug path)
- `serialize((1,2,3))` (inherited) → `"[1, 2, 3]"`; `parse` does `json.loads` → `[1,2,3]`, then
  `tuple(tuple(x) for x in [1,2,3])` → `tuple(1)` → **`TypeError: 'int' object is not iterable`**.
- The guard `except ValueError:` (L1117) is **too narrow** and does not catch the `TypeError`. See [[hot]].
- **No fix is applied** in this repo; the Stage-10 fix is documented only.

## Diagrams
- [[architecture-map]] context + `artifacts/diagrams/architecture_block.mmd`
- `artifacts/diagrams/oop_parameter_diagram.mmd` (class diagram)
- `artifacts/diagrams/bug_path.mmd` (micro flow)

## Still open (Stage 7 did not resolve)
- Real community names + formal centrality hub ranking; verifying the INFERRED parameter→CLI call path.
  See [[open-questions]].

Links: [[index]] · [[hot]] · [[parameter-subsystem]] · [[graph-communities]] · [[bug-investigation-seed]]
