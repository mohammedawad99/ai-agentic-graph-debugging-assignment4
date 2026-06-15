# Before / After Proof — Luigi Bug 3

In-repo before/after summary for the `TupleParameter` round-trip fix. The authoritative reproduction
(exact Docker command and full logs) lives in `reports/bug_fix_validation.md`; this page is the concise
comparison. All evidence is linked, not re-derived.

## 1. Code / test before vs after
| Aspect | Before (buggy commit `a0f1db01…`) | After (Stage 10 fix, commit `a3c59f1`) |
|--------|-----------------------------------|----------------------------------------|
| `TupleParameter.parse` fallback | `except ValueError:` → `return literal_eval(x)` | `except (ValueError, TypeError):` → `return tuple(literal_eval(x))` |
| Round-trip `parse(serialize((1,2,3)))` | raises `TypeError: 'int' object is not iterable` | returns `(1, 2, 3)` |
| Regression test `TestSerializeTupleParameter::testSerialize` | **1 failed** (`TypeError`) | **1 passed** |
| Code delta | — | **two-line** change, no unrelated edits |
| Validation environment | Docker / **Python 3.8.20** focused test | Docker / **Python 3.8.20** focused test |

**Evidence:** `artifacts/validation/stage10_before_failure.txt` (failing-before),
`artifacts/validation/stage10_after_success.txt` (passing-after),
`artifacts/validation/stage10_fix_diff.txt` (exact diff),
`target_repo/luigi_buggy/luigi/parameter.py` (L1117–L1118).

## 2. Knowledge-level before vs after
| | Before the fix | After the fix |
|---|----------------|---------------|
| **Investigation knowledge** | The graph-guided reading identified the **bug neighborhood** (`TupleParameter.parse`) and the **inherited-`serialize` / overridden-`parse` asymmetry** as the likely defect. See `reports/graph_guided_agent.md`, `reports/bug_analysis.md`, `obsidian/hot.md`. | The repository holds an **applied fix plus executed before/after regression evidence**, confirming the asymmetry hypothesis. See `reports/bug_fix_validation.md`. |
| **Graphify artifacts** | Built on the pre-fix source. | **Intentionally left as pre-fix evidence** — `artifacts/graphify/*` is *not* regenerated unless explicitly re-run, so the graph reflects the state in which the bug was discovered (documented honestly; not a current-code claim). |

## 3. Honest scope
- The proof is a **focused** regression test (`TestSerializeTupleParameter`) under **Docker / Python
  3.8.20** — exactly **1 failed before** and **1 passed after**. The **full upstream Luigi test suite was
  not run and is not claimed**.
- The fix is **minimal and real** (two lines, scoped to `TupleParameter.parse`); the diff in
  `stage10_fix_diff.txt` shows no unrelated changes.
- Graphify artifacts remaining pre-fix is a deliberate, stated choice — not an implication that the bug is
  still present in the source (it is fixed; see `obsidian/hot.md` "Current repository state" and
  `reports/final_audit.md`).

## 4. Evidence (links)
- `reports/bug_fix_validation.md` · `reports/bug_analysis.md`
- `artifacts/validation/stage10_before_failure.txt` · `artifacts/validation/stage10_after_success.txt`
  · `artifacts/validation/stage10_fix_diff.txt`
- `target_repo/luigi_buggy/luigi/parameter.py`
