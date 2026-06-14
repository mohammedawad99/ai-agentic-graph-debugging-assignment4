# Reverse Engineering Analysis — Stage 7

## 1. Stage name and date/time
Stage 7 — Reverse engineering analysis. Date: 2026-06-14.

## 2. Inputs used (real artifacts only)
- `artifacts/graphify/graph.json` (6,771 nodes / 15,365 links), `artifacts/graphify/GRAPH_REPORT.md`
- `target_repo/luigi_buggy/luigi/parameter.py`, `luigi/cmdline_parser.py` (read-only)
- Existing Obsidian pages; `reports/graphify_run.md`, `reports/bug_validation.md`

## 3. Method: Macro → Meso → Micro
Top-down: (A) whole-system shape from node counts/degree + the report's communities; (B) the parameter
subsystem around the defect; (C) the exact `TupleParameter.parse` bug path. Each claim is tagged
**EXTRACTED** (directly in graph/source), **INFERRED** (Graphify heuristic edge), or **interpretation**.

## 4. Macro architecture analysis
- **Code mass (EXTRACTED — node counts in `graph.json`).** Largest core code files: `luigi/scheduler.py`
  (135 nodes), `luigi/parameter.py` (111), `luigi/format.py` (83), `luigi/worker.py` (79), then
  `luigi/contrib/*` (hadoop/bigquery/s3) and `luigi/tools/range.py`. Tests are a large share of the corpus
  (e.g. `test/scheduler_api_test.py` 207, `test/parameter_test.py` 180).
- **Hubs by degree (EXTRACTED, with caveat).** Highest-degree nodes are **vendored JS libraries**
  (`d3.min.js` deg≈481, `dagre-d3.min.js` deg≈218) under `luigi/static/visualiser/` — these are **graph
  God-nodes but not core architecture**; they belong to the web UI and are a measurement artifact, not a
  design center. The highest-degree **core** nodes are `MockTarget` (test utility, deg≈250), the `luigi`
  package root (deg≈223), and **`scheduler`** (`luigi_scheduler_scheduler`, deg≈137) — consistent with
  Luigi being a **scheduler/worker DAG engine**.
- **Modular structure (interpretation, supported by paths + communities).** The tree separates a runtime
  core (`task`, `scheduler`, `worker`, `parameter`, `configuration`), a broad `contrib/` integration layer,
  CLI (`cmdline.py`, `cmdline_parser.py`), and a `static/` web UI. `GRAPH_REPORT.md` finds **326
  communities** (placeholder-named, `--no-label`), so exact subsystem boundaries are **partial evidence**,
  not proven cluster labels.
- **CLI / scheduling / parameters / config / worker (mixed).** CmdlineParser exists at
  `luigi/cmdline_parser.py:L28` (EXTRACTED node). The link from the parameter system to the CLI is
  **INFERRED** (see §6), not an EXTRACTED call edge.

## 5. Meso — parameter / serialization subsystem
- `luigi/parameter.py` contributes **111 code nodes** (EXTRACTED). Class family (EXTRACTED, source lines):
  - `Parameter(object)` @ **L93** — base.
  - `DictParameter(Parameter)` @ **L950** (parse L989, serialize L1002, normalize L983).
  - `ListParameter(Parameter)` @ **L1006** — `parse` L1046 → `list(json.loads(x, …))`; `serialize` L1055
    → `json.dumps(x, cls=_DictParamEncoder)`; `normalize` L1037 → `_recursively_freeze(x)`.
  - `TupleParameter(ListParameter)` @ **L1066** — `parse` **L1095** (override).
- **Key structural finding (EXTRACTED).** `TupleParameter` has **no `serialize` node** in the graph and no
  `serialize` in its source body → it **inherits `ListParameter.serialize` (`json.dumps`)** but **overrides
  `parse`**. This serialize/parse asymmetry is the root of the bug (see §6).
- **Inheritance edges (EXTRACTED in `graph.json`):** `TupleParameter --inherits--> ListParameter`;
  `ListParameter`/`DictParameter --inherits--> Parameter`.
- **CLI/config link (INFERRED).** The bug class carries an INFERRED `uses → CmdlineParser` edge; the
  source docstring also notes a "tuple string may come from a config file or from cli execution," so
  parameter parsing sits where **CLI/config string inputs** become typed task arguments.

## 6. Micro — `TupleParameter.parse` (L1095) bug path
Source (`luigi/parameter.py`, ≈L1115–L1118), unchanged:
```python
try:
    return tuple(tuple(x) for x in json.loads(x, object_pairs_hook=_FrozenOrderedDict))
except ValueError:
    return literal_eval(x)
```
- **Why list/tuple/int handling matters.** Serialization (inherited) does `json.dumps((1,2,3)) == "[1, 2, 3]"`.
  On `parse`, `json.loads("[1, 2, 3]")` returns the **flat list `[1,2,3]`**, and `tuple(tuple(x) for x in …)`
  applies `tuple(1)` to an **int element** → `TypeError: 'int' object is not iterable`.
- **Why the guard fails.** The `except ValueError:` is **too narrow**: a `TypeError` (not a `ValueError`)
  escapes instead of falling back to `literal_eval`. The inner-comment design only anticipated `ValueError`
  from non-JSON tuple strings, not `TypeError` from flat-list JSON.
- **Symptom (from earlier validation, candidate repo, Docker/Python 3.8.20):**
  `TypeError: 'int' object is not iterable`. See `reports/bug_validation.md`.
- **No fix applied here.** The known Stage-10 fix (`except (ValueError, TypeError):` + `return tuple(literal_eval(x))`)
  is documented but **not** applied; buggy `except ValueError:` remains.

## 7. Graph evidence table
| Finding | Source artifact | Evidence (node / community) | Confidence |
|---|---|---|---|
| `TupleParameter` is the bug class | graph.json | `luigi_parameter_tupleparameter` @ L1066 | EXTRACTED |
| Bug method is `.parse()` | graph.json | `luigi_parameter_tupleparameter_parse` @ L1095 | EXTRACTED |
| Inherits `ListParameter` | graph.json | edge `tupleparameter --inherits--> listparameter` | EXTRACTED |
| No serialize override (inherits) | graph.json | no `tupleparameter_serialize` node | EXTRACTED (absence) |
| Parameter system size | graph.json | 111 code nodes with `source_file=luigi/parameter.py` | EXTRACTED |
| Scheduler is a core hub | graph.json | `luigi_scheduler_scheduler` degree ≈137 | EXTRACTED |
| Top God-nodes are vendored JS | graph.json | `d3.min.js` deg≈481 (web UI) | EXTRACTED (caveat: not core) |
| Parameters relate to CLI | graph.json | `tupleparameter --uses--> cmdlineparser` | INFERRED (conf 0.54 band) |
| Parameter cluster | GRAPH_REPORT.md | Community 58 (ListParameter, DictParameter, `_FrozenOrderedDict`) | EXTRACTED (placeholder name) |
| Command-line cluster | GRAPH_REPORT.md | Community 1 (CmdlineParser, ChoiceParameter) | EXTRACTED (placeholder name) |

## 8. Source evidence table
| File | Line(s) | Meaning |
|---|---|---|
| `luigi/parameter.py` | L93 | `class Parameter(object)` — base |
| `luigi/parameter.py` | L1006 / L1046 / L1055 | `ListParameter`; `parse` → `list(json.loads)`; `serialize` → `json.dumps` |
| `luigi/parameter.py` | L1066 / L1095 | `TupleParameter`; overriding `parse` (bug site) |
| `luigi/parameter.py` | L1115–L1118 | `tuple(tuple(x) …)` + narrow `except ValueError:` |
| `luigi/parameter.py` | L950 / L989 / L1002 | `DictParameter` (sibling param type) |
| `luigi/cmdline_parser.py` | L28 | `class CmdlineParser` — CLI value source |

## 9. Diagrams created
- `artifacts/diagrams/architecture_block.mmd` — macro block diagram (Entry/CLI → Parameters → Task/Scheduler/Worker; bug site highlighted).
- `artifacts/diagrams/oop_parameter_diagram.mmd` — class diagram (`Parameter`→`ListParameter`→`TupleParameter`, `DictParameter`; parse/serialize; override note).
- `artifacts/diagrams/bug_path.mmd` — micro flow of the `TypeError` and the un-caught path.

## 10. What is confirmed (this stage)
- The bug class/method, its inheritance, and the **serialize(inherited)/parse(override) asymmetry** are
  graph- and source-grounded.
- The macro picture (scheduler/worker/parameter core + contrib + CLI + web-UI assets) is consistent across
  node counts, degree, and the report's communities — with the explicit caveat that top God-nodes are
  vendored JS and community names are placeholders.

## 11. What remains for Stage 8/9/10
- Stage 8 (baseline) and Stage 9 (graph-guided agent): localize the bug under controlled, measured runs.
- Stage 10: reproduce failing-before / passing-after in this repo under Docker, then apply the minimal fix.
- Stage 7 leftovers (still open): real community names + formal centrality-based hub ranking, and verifying
  the INFERRED parameter→CLI call path (see `obsidian/open-questions.md`).

## 12. Confirmations
- No Luigi source changed (read-only inspection of `target_repo/luigi_buggy/`).
- No Graphify artifacts changed (`artifacts/graphify/` untouched).
- No agent run. No baseline run. **No bug fix applied** (buggy `except ValueError:` still present).

## 13. Next stage
Stage 8 — Baseline naive investigation.
