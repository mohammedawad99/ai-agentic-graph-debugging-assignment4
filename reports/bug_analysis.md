# Bug Analysis — Luigi Bug 3 (`TupleParameter` round-trip parsing)

Focused analysis of the selected defect (BugsInPy **Luigi bug 3**), how it was localized through the
graph-guided investigation, and its root cause. Every claim is tagged **Extracted** (read directly from
source/artifacts), **Inferred** (reasoned from those facts), or **Verified** (confirmed by an executed
before/after test). No new evidence is invented here — all of it is linked below.

## 1. Summary
- **Symptom (Verified):** round-tripping a tuple through `TupleParameter` —
  `TupleParameter().parse(TupleParameter().serialize((1, 2, 3)))` — raises
  `TypeError: 'int' object is not iterable` instead of returning `(1, 2, 3)`.
- **Location (Extracted):** `luigi/parameter.py` → class `TupleParameter` (≈L1066), method `.parse()`
  (≈L1095), in the vendored buggy source `target_repo/luigi_buggy/luigi/parameter.py`.
- **Buggy commit (Extracted):** `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`.

## 2. How the bug was localized (graph-guided)
- **Extracted:** the Graphify graph (`artifacts/graphify/graph.json`) exposes the node
  `luigi_parameter_tupleparameter` (`TupleParameter`) with an **inherits** edge to
  `luigi_parameter_listparameter` (`ListParameter`) and a **method** edge to
  `luigi_parameter_tupleparameter_parse` (`.parse()`).
- **Inferred:** because `TupleParameter` defines `parse` but **not** `serialize`, the graph's
  class/inheritance view points to an *asymmetry* — `serialize` is inherited from `ListParameter` while
  `parse` is overridden locally. That asymmetry is the investigative lead the graph surfaces before any
  raw-source reading (see `reports/graph_guided_agent.md` and `obsidian/hot.md`).
- **Verified:** the deterministic graph-guided agent reaches the same `TupleParameter.parse` neighborhood
  recorded in `artifacts/validation/graph_guided_agent_files_read.txt`.

## 3. Root cause (the asymmetry)
- **Extracted:** `ListParameter.serialize` is `json.dumps(...)`. `TupleParameter` inherits it, so
  `serialize((1, 2, 3))` produces the **list-shaped JSON string** `"[1, 2, 3]"` — not a tuple-of-tuples.
- **Extracted:** the buggy `TupleParameter.parse` first tries
  `tuple(tuple(x) for x in json.loads(x, object_pairs_hook=_FrozenOrderedDict))`, then on failure used a
  **too-narrow** `except ValueError:` returning `literal_eval(x)` **not wrapped** in `tuple(...)`.
- **Inferred + Verified:** for input `"[1, 2, 3]"`, `json.loads` returns the list `[1, 2, 3]`; the
  generator then evaluates `tuple(1)` on an `int`, raising **`TypeError`** (not `ValueError`). The narrow
  `except ValueError` does not catch it, so the `TypeError` escapes — the observed crash.

## 4. The fix (minimal, two lines)
**Extracted** from `target_repo/luigi_buggy/luigi/parameter.py` (L1117–L1118) and
`artifacts/validation/stage10_fix_diff.txt`:
```python
except (ValueError, TypeError):          # widened guard (was: except ValueError)
    return tuple(literal_eval(x))         # wrap in tuple(...) (was: return literal_eval(x))
```
- **Inferred:** widening the guard to `(ValueError, TypeError)` lets the fallback handle the list-shaped
  input; wrapping in `tuple(...)` makes the fallback return a real tuple, so the round-trip yields
  `(1, 2, 3)`. This matches the BugsInPy reference fix and is intentionally **minimal** (no unrelated
  refactors).

## 5. Evidence (links — not re-derived here)
- `reports/bug_fix_validation.md` — full before/after method, exact Docker command, root-cause write-up.
- `artifacts/validation/stage10_before_failure.txt` — failing-before log (`TypeError`, 1 failed).
- `artifacts/validation/stage10_after_success.txt` — passing-after log (`1 passed`).
- `artifacts/validation/stage10_fix_diff.txt` — the exact two-line diff.
- `target_repo/luigi_buggy/luigi/parameter.py` — the fixed source (L1066/L1095/L1117–L1118).
- Graph / vault context: `artifacts/graphify/GRAPH_REPORT.md`, `obsidian/hot.md`,
  `obsidian/reverse-engineering-analysis.md`, `reports/reverse_engineering.md`.

## 6. Honest scope
- **Verified** evidence comes from a **focused** regression test (`TestSerializeTupleParameter`) under
  **Docker / Python 3.8.20**; the full upstream Luigi suite was **not** run and is **not** claimed.
- Token/centrality framing elsewhere is a triage aid — this page does **not** claim centrality or graph
  position *proves* the root cause; the root cause is established by the code reading + executed test above.
