# Bug Investigation Seed (for Stages 7 & 10)

A seed for the later graph-guided investigation and fix. **No fix is claimed here.** The bug is **not**
fixed in this repository, and no agent has run yet.

## Candidate bug path (grounded)
- Entry: `luigi.TupleParameter` (exported via `luigi/__init__` → `imports` edge to the bug node).
- Defect site: `TupleParameter.parse` (`luigi/parameter.py:L1095`).
- Inheritance: `TupleParameter` → `ListParameter` (L1006) → `Parameter` (L93).
- Test surface: `test/parameter_test.py` (180 nodes) holds the regression test class
  `TestSerializeTupleParameter::testSerialize` (added from the fixed commit during validation).

## Known pre-validation result (earlier, candidate repo — NOT re-run in this repo)
- Environment: Docker `python:3.8-slim` (Python 3.8.20).
- Failing-before: `TypeError: 'int' object is not iterable`.
- Known fix (reserved for Stage 10, not applied): `except (ValueError, TypeError):` + `return tuple(literal_eval(x))`.
- See `reports/bug_validation.md` for the candidate-repo evidence.

## What still must be PROVEN inside this final repo (Stage 10)
- [ ] Reproduce **failing-before** on the vendored source under Docker/Python 3.8 → capture log.
- [ ] Apply the minimal fix to `target_repo/luigi_buggy/luigi/parameter.py` (Stage 10 only).
- [ ] Reproduce **passing-after** with the same test → capture log.
- [ ] Confirm the diff is confined to `TupleParameter.parse` (no unrelated changes).

## What Stage 7 should produce first
- A verified macro→meso→micro reading and a hub/community ranking (see [[graph-communities]]).
- A traceability chain: public API → `parse` → callers → test (using `graph.json` edges).

Links: [[hot]] · [[parameter-subsystem]] · [[graph-communities]] · [[token-efficiency-plan]] · [[index]]
