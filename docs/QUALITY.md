# Quality Gates — Assignment 04 (MaRs-777)

Final quality-gate record for the completed repository. The gates below were defined early, executed
throughout implementation, and re-run during the final audit / grade-polish pass. **Current final status:
all project gates pass.** Commands are real and reproducible; the latest gate-run evidence is recorded at
the bottom of this file.

## Gates
| # | Gate | Command | Pass condition |
|---|------|---------|----------------|
| Q1 | Tests | `uv run pytest` | all tests pass; bug regression test behaves as documented |
| Q2 | Lint | `uv run ruff check .` | no lint errors (rule set `E,F,W,I,N,UP,B,C4,SIM`) |
| Q3 | Format | `uv run ruff format --check .` | no formatting diffs |
| Q4 | File line-count rule | custom check: every `*.py` under `src/` ≤ **150 code lines** | no file exceeds 150 |
| Q5 | Secret scan | grep/secret-scan over tracked files | no API keys/secrets committed |
| Q6 | Artifact scan | check no large/raw generated artifacts or raw target source committed | only intended artifacts tracked |
| Q7 | README/docs consistency | manual + checklist cross-check | README claims match repo reality |
| Q8 | No fake evidence | review of logs/screenshots/graphs vs sources | all evidence reproducible |
| Q9 | No overclaiming | audit status labels vs actual artifacts | no stage claimed before complete |
| Q10 | Coverage | `uv run pytest --cov=src/ex04_graph_debugger` | coverage **≥ 85%** (`[tool.coverage.report] fail_under = 85`) |
| Q11 | Version | `tests/unit/test_version.py` | package version `1.00`, in sync across `pyproject.toml` / `version.py` / `__init__` |

## Guideline applicability (V3 mapping)
The course's V3 service-SDK guidelines are mapped to this project honestly. This is a **deterministic
analysis/agent workflow**, not a hosted service SDK, so several service-runtime items are **N/A by
design** rather than skipped:

| Guideline area | Applicability | Rationale |
|----------------|:------------:|-----------|
| SDK architecture | **Adapted** | Not a service-SDK product; the project logic is modularized as a small package in `src/ex04_graph_debugger/` (agent, nodes, state, source reader, metrics, centrality), each file ≤150 code lines. |
| API Gatekeeper | **N/A** | The final submitted workflow makes **no external API/LLM calls** (`llm_used = false`); there is no external surface to gate. |
| Rate limits | **N/A** | No runtime external API calls, so there is nothing to rate-limit. |
| Queue management | **N/A** | No asynchronous external request queue; the workflow is a synchronous, deterministic StateGraph. |
| Cost tracking | **DONE** | `$0` external API cost, documented in `docs/COSTS.md` (`api_cost_usd = 0`). |
| Per-mechanism PRD | **DONE** | `docs/PRD_graph_guided_agent.md` and `docs/PRD_centrality_ranking.md` (plus the overall `docs/PRD.md`). |
| Versioning | **DONE** | Version starts at `1.00` (`pyproject.toml` + `src/ex04_graph_debugger/version.py`, guarded by Q11). |
| Coverage gate | **DONE** | `fail_under = 85`; latest run **97%** (Q10). |

## Q4 — 150-line rule (detail)
- Applies to Python source under `src/` (the project's own code).
- The target project (`target_repo/luigi`) is third-party and exempt from our line rule.
- A small checker script will be added under `src/ex04_graph_debugger/` (or `scripts/`) in the implementation stage; configured via `pyproject.toml [tool.ex04.quality] max_python_file_lines = 150`.

## Q5 — Secret scan (detail)
- Patterns: `ANTHROPIC_API_KEY=`, `OPENAI_API_KEY=`, `sk-`, `-----BEGIN ... KEY-----`, generic high-entropy tokens.
- `.env` is git-ignored; only `.env.example` (no real values) is tracked.

## Gate-run evidence (Stage 9 — first code added; commit `3b0e3c0`)
| Gate | Command | Result (2026-06-14) |
|------|---------|---------------------|
| Q1 Tests | `uv run pytest` | **6 passed** (`tests/unit/test_graph_guided_agent.py`) |
| Q2 Lint | `uv run ruff check .` | **All checks passed** |
| Q3 Format | `uv run ruff format --check .` | **7 files already formatted** |
| Q4 Line limit | `wc -l src/ex04_graph_debugger/*.py` | all ≤150 (max 137) |
- Ruff is scoped to our code via `[tool.ruff] extend-exclude = ["target_repo", "artifacts", "obsidian", ".venv"]`
  so the vendored Luigi source (Stage-4) is **not** linted (it has thousands of pre-existing upstream style issues).
- Q5 secret-scan, Q6 artifact-scan, and the dedicated Q4 checker script run as part of the final audit (Stage 13).

## Stage 10 — bug-fix test evidence (commit `a3c59f1`)
- Project gates re-run after the fix: `uv run pytest` → **6 passed**; `uv run ruff check .` → **All checks passed**; `uv run ruff format --check .` → **clean**.
- **Luigi targeted regression** (`TestSerializeTupleParameter::testSerialize`) runs under **Docker/Python 3.8.20**
  (Luigi 2.8.3 cannot import on the host's 3.12): **before** = `TypeError` (1 failed); **after** = `1 passed`.
  This is a **focused** test, not a full upstream-suite run (stated honestly in `reports/bug_fix_validation.md`).
- **Idempotent test gate:** `graph_guided_agent.run()` takes an optional `out_dir`; the unit tests pass a
  pytest `tmp_path`, so `uv run pytest` no longer mutates the tracked Stage 9 artifacts
  (`artifacts/validation/graph_guided_agent_*`). A guard test (`test_run_does_not_touch_tracked_artifacts`)
  asserts this. Production behaviour is unchanged (`out_dir=None` → `artifacts/validation/`).

## Stage 11 — token-efficiency comparison consistency check (commit `dad0413`)
The comparison JSON is validated against the committed Stage 8/9 metrics with:
```
python3 -c "import json;d=json.load(open('artifacts/validation/token_efficiency_comparison.json'));\
assert d['baseline']['estimated_tokens']==24482 and d['graph_guided']['estimated_tokens']==3631;\
assert d['deltas']['token_savings']==20851 and d['deltas']['token_reduction_percent']==85.17;\
assert d['deltas']['baseline_to_graph_guided_factor']==6.74;\
assert d['interpretation']['universal_claim'] is False;print('OK')"
```
Source metric files (`baseline_naive_metrics.json`, `graph_guided_agent_metrics.json`) are **read-only** in
this stage (`git diff` over them must be empty). No LLM/API used.

## Stage 12 — original extension test evidence (commit `de32d76`)
- `uv run pytest` → **13 passed** (6 new in `tests/unit/test_centrality_ranking.py` — degree, relevance,
  ranking order, candidate filter, known-target detection, idempotent `out_dir` write).
- `uv run ruff check .` → **All checks passed**; `uv run ruff format --check .` → clean.
- `src/ex04_graph_debugger/centrality_ranking.py` ≤ 150 code lines; deterministic, no LLM/API; reads
  `graph.json` read-only.

## Stage 13 — final audit gate run (commit `cf55bac`)
At the final audit: `uv run pytest` → **13 passed**; `uv run ruff check .` → **All checks passed**;
`uv run ruff format --check .` → clean; line-count guard → **0 violations** (7 `src/` files, max 142 code
lines). No protected artifact mutated by the audit. Recorded in `reports/final_audit.md`.

## Final polish pass — gate run (grade-100 hardening)
After widening the Ruff rule set to `E,F,W,I,N,UP,B,C4,SIM`, adding the coverage gate, and adding the
version guard:
- `uv run pytest` → **16 passed** (3 new in `tests/unit/test_version.py`).
- `uv run pytest --cov=src/ex04_graph_debugger` → **coverage 97%** (gate `fail_under = 85` reached).
- `uv run ruff check .` → **All checks passed** (widened rule set).
- `uv run ruff format --check .` → **clean** (11 files).
- Line-count guard → **0 violations** (`src/` files ≤ 150 code lines; `version.py` added).
- Ruff remains scoped to our code via `extend-exclude = ["target_repo", "artifacts", "obsidian", ".venv"]`
  so the vendored Luigi source is **not** linted.

## Execution policy
- Gates run **before any commit intended for submission** and again in the **final audit** (`reports/final_audit.md`).
- A failing gate is fixed; results are never suppressed or faked.
