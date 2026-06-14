# Quality Gates — Assignment 04 (MaRs-777)

Planned, runnable gates. They are **defined now** and executed in later stages once code/tests exist.
Nothing here is claimed to pass yet (no implementation in the skeleton stage).

## Gates
| # | Gate | Command (planned) | Pass condition |
|---|------|-------------------|----------------|
| Q1 | Tests | `uv run pytest` | all tests pass; bug regression test behaves as documented |
| Q2 | Lint | `uv run ruff check .` | no lint errors |
| Q3 | Format | `uv run ruff format --check .` | no formatting diffs |
| Q4 | File line-count rule | custom check: every `*.py` under `src/` ≤ **150 lines** | no file exceeds 150 lines |
| Q5 | Secret scan | grep/secret-scan over tracked files | no API keys/secrets committed |
| Q6 | Artifact scan | check no large/raw generated artifacts or raw target source committed | only intended artifacts tracked |
| Q7 | README/docs consistency | manual + checklist cross-check | README claims match repo reality |
| Q8 | No fake evidence | review of logs/screenshots/graphs vs sources | all evidence reproducible |
| Q9 | No overclaiming | audit status labels vs actual artifacts | no stage claimed before complete |

## Q4 — 150-line rule (detail)
- Applies to Python source under `src/` (the project's own code).
- The target project (`target_repo/luigi`) is third-party and exempt from our line rule.
- A small checker script will be added under `src/ex04_graph_debugger/` (or `scripts/`) in the implementation stage; configured via `pyproject.toml [tool.ex04.quality] max_python_file_lines = 150`.

## Q5 — Secret scan (detail)
- Patterns: `ANTHROPIC_API_KEY=`, `OPENAI_API_KEY=`, `sk-`, `-----BEGIN ... KEY-----`, generic high-entropy tokens.
- `.env` is git-ignored; only `.env.example` (no real values) is tracked.

## Gate-run evidence (Stage 9 — first code added)
| Gate | Command | Result (2026-06-14) |
|------|---------|---------------------|
| Q1 Tests | `uv run pytest` | **6 passed** (`tests/unit/test_graph_guided_agent.py`) |
| Q2 Lint | `uv run ruff check .` | **All checks passed** |
| Q3 Format | `uv run ruff format --check .` | **7 files already formatted** |
| Q4 Line limit | `wc -l src/ex04_graph_debugger/*.py` | all ≤150 (max 137) |
- Ruff is scoped to our code via `[tool.ruff] extend-exclude = ["target_repo", "artifacts", "obsidian", ".venv"]`
  so the vendored Luigi source (Stage-4) is **not** linted (it has thousands of pre-existing upstream style issues).
- Q5 secret-scan, Q6 artifact-scan, and the dedicated Q4 checker script run in the final audit (Stage 14).

## Execution policy
- Gates run **before any commit intended for submission** and again in the **final audit** (`reports/final_audit.md`).
- A failing gate is fixed; results are never suppressed or faked.
