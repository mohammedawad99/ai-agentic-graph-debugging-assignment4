# Bug-Fix Validation — Stage 10

## 1. Stage name and date/time
Stage 10 — Bug fix and before/after proof. Date: 2026-06-14.

## 2. Purpose
Apply the **minimal** fix to Luigi `TupleParameter.parse` and prove **failure before** and **success after**
with a focused regression test, run faithfully under Docker / Python 3.8.20.

## 3. Bug summary
`luigi.TupleParameter().parse(luigi.TupleParameter().serialize((1, 2, 3)))` raises
`TypeError: 'int' object is not iterable` instead of returning `(1, 2, 3)`.

## 4. Root cause
`TupleParameter` (L1066) overrides `parse` only and inherits `ListParameter.serialize` (`json.dumps`):
`serialize((1,2,3)) == "[1, 2, 3]"`. `parse` then `json.loads` → `[1,2,3]` and runs
`tuple(tuple(x) for x in [1,2,3])`, i.e. `tuple(1)` on an int → `TypeError`. The original guard
`except ValueError:` is too narrow to catch the `TypeError`, so it propagates.

## 5. Minimal fix
Two lines, confined to `TupleParameter.parse` (`luigi/parameter.py`), no unrelated refactor:
```diff
-        except ValueError:
-            return literal_eval(x)
+        except (ValueError, TypeError):
+            return tuple(literal_eval(x))
```
**Why two lines (honest note):** widening the `except` alone stops the crash but is **insufficient** — the
fallback `literal_eval("[1, 2, 3]")` returns a **list** `[1,2,3]`, so the round-trip yields a list and the
test then fails with `AssertionError ((1,2,3) != [1,2,3])`. Wrapping it in `tuple(...)` makes the round-trip
correct. This is exactly the upstream BugsInPy fix. (An intermediate run with only the `except` change is
recorded in the trace — it changed `TypeError` → `AssertionError`, confirming the second line is required.)

## 6. Regression test
**Added** (none existed at the buggy commit): `TestSerializeTupleParameter.testSerialize` in
`target_repo/luigi_buggy/test/parameter_test.py`:
```python
class TestSerializeTupleParameter(LuigiTestCase):
    def testSerialize(self):
        the_tuple = (1, 2, 3)
        param = luigi.TupleParameter()
        self.assertEqual(param.parse(param.serialize(the_tuple)), the_tuple)
```

## 7. Before-fix evidence (buggy source)
- **Command:** `docker run --rm -v "$PWD":/work -w /work python:3.8-slim bash -lc "pip install -e . --no-deps && pip install tornado<5 python-dateutil==2.7.5 mock psutil pytest && pytest -rA -q test/parameter_test.py::TestSerializeTupleParameter::testSerialize"` (via `sg docker`).
- **Expected & observed:** FAIL with `TypeError: 'int' object is not iterable` at `luigi/parameter.py:1116`.
- **Evidence file:** `artifacts/validation/stage10_before_failure.txt`
  - Key line: `E   TypeError: 'int' object is not iterable` → `1 failed, 2 warnings in 0.46s`.

## 8. After-fix evidence (patched source)
- **Command:** identical to §7 (same Docker image, same test).
- **Expected & observed:** PASS.
- **Evidence file:** `artifacts/validation/stage10_after_success.txt`
  - Key line: `PASSED test/parameter_test.py::TestSerializeTupleParameter::testSerialize` → `1 passed, 2 warnings in 0.16s`.

## 9. Diff evidence
`artifacts/validation/stage10_fix_diff.txt` — the 2-line source fix + the added regression test (no other changes).

## 10. Quality gates (project — our own code, run in the uv env)
| Gate | Command | Result |
|------|---------|--------|
| Tests | `uv run pytest` | **6 passed** |
| Lint | `uv run ruff check .` | **All checks passed** |
| Format | `uv run ruff format --check .` | **clean** |
- The **Luigi** regression test runs under **Docker/Python 3.8.20** (Luigi 2.8.3 cannot import on the host's
  3.12). Only the **focused** `TupleParameter` test was run — this is **not** a full upstream-suite claim.

## 11. Scope confirmation
- No Graphify rerun; `artifacts/graphify/` unchanged.
- No Obsidian edits.
- No baseline metric edits (`artifacts/validation/baseline_naive_*` unchanged).
- No graph-guided metric edits (`artifacts/validation/graph_guided_agent_*` unchanged).
- No final token comparison produced.

## 12. Current limitation
This is **bug-fix validation only**, not the final token-efficiency comparison. The before/after proof is a
focused regression test, not a full upstream test run.

## 13. Next stage
Stage 11 — token-efficiency comparison (baseline vs graph-guided).
