# Baseline Naive Investigation — Stage 8

## 1. Stage name and date/time
Stage 8 — Baseline naive investigation. Date: 2026-06-14.

## 2. Baseline purpose
Estimate the raw-code reading cost of investigating the Luigi `TupleParameter` bug **without** Graphify,
Obsidian, graph-guided navigation, or an agent. This is the **control** that the Stage 9 graph-guided
workflow and the Stage 11 comparison will be measured against.

## 3. Important caveat — controlled baseline, not blind discovery
We already know the bug from prior validation; this is **not** a real blind-discovery claim. The baseline
**simulates how much raw-code context a naive investigator must read** when starting only from the failure
symptom and the raw repository. The measured numbers are the files/text units **intentionally read under
this fixed protocol**. The graph-guided run will follow the same honesty rules and be compared here.

## 4. Inputs allowed (and used)
- Vendored source `target_repo/luigi_buggy/` (read-only).
- Known symptom: `TypeError: 'int' object is not iterable`.
- Known seed expression: `luigi.TupleParameter().parse(luigi.TupleParameter().serialize((1, 2, 3)))`.
- Generic listing/search (`find`, `grep`, `sed`, `wc`).

## 5. Inputs intentionally NOT used (forbidden for the baseline path)
`artifacts/graphify/graph.json`, `GRAPH_REPORT.md`, `GRAPH_TREE.html`, all `obsidian/*.md`,
`reports/reverse_engineering.md`, and the diagrams. **No graph-derived node/community/hub evidence guided
this path.** (They are mentioned here only to record they were excluded.)

## 6. Investigation protocol
1. Start from `target_repo/luigi_buggy/` only. 2. List top-level structure. 3. Broad `grep TupleParameter`.
4. Search `parse`/`serialize`/`literal_eval`/`json.loads`. 5. Read the relevant source modules in full.
6. Track every file/text unit read. 7. Estimate tokens. 8. Count rounds. 9. Decide if root cause reached.
10. Stop before any patch.

## 7. Step-by-step baseline trace (see `artifacts/validation/baseline_naive_trace.log`)
- **Round 1 — structure.** Top level shows `luigi/`, `test/`, `doc/`, `examples/`, `bin/`, `scripts/`,
  `setup.py` — no pointer to the defect.
- **Round 2 — `grep TupleParameter`.** 18 hits: `luigi/__init__.py` (export), `luigi/parameter.py:1066`
  (definition), and many `test/*` usages. The grep locates the class but **not** the faulty method or why.
- **Round 3 — `parse`/`serialize` search in `parameter.py`.** Reveals **30+ `parse`/`serialize` methods**
  across the module (lines 61, 242, 271, …, 989, 1002, 1046, 1055, 1095, …). With no graph, the investigator
  cannot tell which is on the failing path without reading them.
- **Round 4 — class hierarchy.** `Parameter` (L93) → `DictParameter` (L950), `ListParameter` (L1006),
  `TupleParameter` (L1066). To understand `TupleParameter.parse` they must also read `ListParameter`
  (base) and `Parameter`.
- **Round 5 — read modules in full** (the naive read set) and connect serialize→parse:
  `ListParameter.serialize` (L1055, inherited) `json.dumps((1,2,3)) == "[1, 2, 3]"`; `TupleParameter.parse`
  (L1095) `json.loads` → `[1,2,3]` then `tuple(1)` → **`TypeError`**, not caught by `except ValueError`
  (L1117). **Root cause reached.**

## 8. Files / text units read
| File | Range | Reason read | Characters | Est. tokens (chars/4) |
|------|-------|-------------|-----------:|----------------------:|
| `luigi/parameter.py` | full (1–1252) | 30+ parse/serialize methods; must read whole module to locate `TupleParameter.parse` | 44,065 | 11,016 |
| `luigi/__init__.py` | full (1–63) | confirm `luigi.TupleParameter` public export (matches seed expr) | 2,328 | 582 |
| `luigi/cmdline_parser.py` | full (1–151) | `parse` docstring says tuple strings come from config/CLI; naively checked | 5,468 | 1,367 |
| `test/parameter_test.py` | full (1–1202) | scan tests to find/reproduce the serialize→parse round-trip | 46,065 | 11,516 |
| **Total** | 4 files | — | **97,926** | **24,482** |

## 9. Iteration count
**5 investigation rounds** (structure → grep → parse search → hierarchy → full reads).

## 10. Root cause reached? — **Yes**
Yes, but only after reading the full `parameter.py` (and base classes) plus the test file. The investigator
must scan many unrelated parameter classes before isolating `TupleParameter.parse` (L1095) and the narrow
`except ValueError` that fails to catch the `TypeError`.

## 11. Naive baseline conclusion
- **What the investigator finds.** `TupleParameter` (L1066) extends `ListParameter` and overrides `parse`
  only; it inherits `ListParameter.serialize` (`json.dumps`).
- **Why the exception occurs.** Serialization emits `"[1, 2, 3]"`; `parse` does `json.loads` → flat list
  `[1,2,3]`, then `tuple(tuple(x) for x in …)` runs `tuple(1)` on an int → `TypeError: 'int' object is not
  iterable`; `except ValueError` (L1117) is too narrow to catch it.
- **Why this needs broad raw reading.** Without a graph, nothing points to the defect: `parameter.py` is a
  ~1,250-line module with 30+ parse/serialize methods, and the test file is another ~1,200 lines. The naive
  protocol reads ≈98k characters (~24.5k est. tokens) across 4 files to reach the same conclusion that a
  graph-guided run is **expected** (hypothesis, to be measured in Stage 9/11) to reach by jumping directly
  to the `TupleParameter`/`parse` node and its immediate neighbors.

## 12. Metrics summary (`artifacts/validation/baseline_naive_metrics.json`)
- method: `estimated_tokens = characters / 4` (estimate, not exact API tokenization)
- total_files_read: 4 · total_text_units_read: 4 · total_characters_read: 97,926 · estimated_tokens: 24,482
- investigation_rounds: 5 · root_cause_reached: true
- graphify_used: false · obsidian_used: false · agent_used: false · bug_fix_applied: false

## 13. Limitations of this baseline
- It is a **protocol-defined** read set, not an empirical average over many human investigators; a different
  naive investigator might read more (e.g. `task.py`, more tests) or slightly less.
- `characters/4` is a coarse token estimate; real tokenizer counts will differ.
- "Root cause reached" reflects that the information is **present** in the read set, not a timed human trial.
- The comparison value is **relative** (same honesty rules will apply to the graph-guided run), not an
  absolute performance claim.

## 14. Confirmations
- **No Graphify artifacts used** in the baseline path (graph.json/GRAPH_REPORT/GRAPH_TREE excluded).
- **No Obsidian vault used** in the baseline path.
- **No agent run.** No baseline-vs-graph comparison computed yet (Stage 11).
- **No Luigi source changed** (read-only). **No bug fix applied** (`except ValueError:` still present).

## 15. Commit evidence
Committed and pushed as `8904b57 Measure naive baseline investigation`.

## 16. Next stage
Stage 9 — graph-guided agent workflow (the comparison counterpart to this baseline).
