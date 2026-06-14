# Bug Validation Report (Summary) — Luigi bug 3

Faithful reproduction of the selected bug. Performed in a **temporary candidate repo**, which was
reverted to pristine afterward. **No fix is implemented in this final repo yet.**

## Environment
- Runtime: **Docker**, native Linux engine (invoked via `sg docker -c …`), image **`python:3.8-slim`**.
- In-container Python: **3.8.20**.
- Command category used (not full logs):
  `docker run --rm -v "$PWD":/work -w /work python:3.8-slim bash -lc "pip install -e . --no-deps && pip install tornado<5 python-dateutil==2.7.5 mock psutil pytest && pytest <target test>"`

## Target
- Buggy commit: **`a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`** (Luigi 2.8.3).
- File / symbol: `luigi/parameter.py` → **`TupleParameter.parse`**.
- Regression test: `test/parameter_test.py::TestSerializeTupleParameter::testSerialize`.

## Procedure & results
1. **Clean baseline confirmed** at buggy commit (`git status` empty).
2. **Regression test overlaid from fixed commit** `3a0bfbff69addfb3be1107adab3d4914bcae3e4b`:
   - Proof the test is **absent at the buggy commit**: `class TestSerializeTupleParameter` occurrences —
     buggy = **0**, fixed = **1** (this is the standard BugsInPy layout: buggy source + fixed-commit test).
3. **Failing-before** (buggy source):
   ```
   TypeError: 'int' object is not iterable   (luigi/parameter.py: tuple(tuple(x) for x in json.loads(...)))
   1 failed
   ```
4. **Temporary minimal patch** (guarded; exactly the BugsInPy fix), inside `TupleParameter.parse`:
   ```diff
   -        except ValueError:
   -            return literal_eval(x)
   +        except (ValueError, TypeError):
   +            return tuple(literal_eval(x))
   ```
5. **Passing-after** (same command): `1 passed`.
6. **Cleanup → pristine:** reverted `luigi/parameter.py` and `test/parameter_test.py`; removed
   `*.egg-info`, `__pycache__`, `.pytest_cache`, build artifacts; final `git status` **empty**; HEAD unchanged.

## Root cause (one line)
`serialize((1,2,3))` yields `"[1, 2, 3]"`; on parse, `json.loads` gives `[1,2,3]` and
`tuple(tuple(x) for x in …)` does `tuple(1)` → `TypeError`. The buggy `except ValueError:` doesn't
catch `TypeError`, so it escapes instead of falling back to `literal_eval`.

## Status
**Luigi confirmed.** The bug reproduces and the known fix resolves it under Python 3.8.
Final-repo before/after reproduction is a later stage (`reports/before_after.md`).
