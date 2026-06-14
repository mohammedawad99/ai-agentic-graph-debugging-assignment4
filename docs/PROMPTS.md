# Prompts Log — Assignment 04 (MaRs-777)

Summaries of the instructions that drove each stage. These are **paraphrased prompt summaries**,
not verbatim private content and not fabricated. Hidden/internal reasoning is intentionally excluded.

## P-01 — Repository selection
**Stage:** selection.
**Summary:** Evaluate three candidate Python bug repos (BugsInPy, broken-python, buggy-python) against ~10 criteria (setup, bug clarity, test reproducibility, size, Graphify/Obsidian value, architecture, token-efficiency potential, dependency risk, report potential). Inspect read-only, clone only to a temp candidate area, no implementation/fix/commit. Produce a strict selection report.
**Outcome:** Initial pick = PySnooper bug 3 (clean, reproducible on 3.12, but small).

## P-02 — Size-driven re-selection
**Stage:** re-selection.
**Summary:** Moodle adds a size expectation for excellent submissions (~10k+ LOC, ~70+ files). Re-open selection, prefer BugsInPy, measure LOC/file counts, weigh size vs manageability and dependency risk. Produce a new strict report with ≥3 stronger candidates.
**Outcome:** Luigi bug 3 chosen (size + DAG/Graphify richness); Tornado bug 9 as fallback; PySnooper demoted to safety net. Discovered cross-cutting blocker: BugsInPy 2018–2020 commits need Python 3.7/3.8 (won't import on 3.12).

## P-03 — Docker-based faithful validation
**Stage:** validation.
**Summary:** Reproduce Luigi bug 3 faithfully in Python 3.8 via Docker. Record clean state and proof the regression test is absent at the buggy commit; overlay the fixed-commit test; capture failing-before; apply a guarded minimal patch; capture passing-after; revert both files and all artifacts; confirm pristine. Validation only — no commit/implementation, no patch left applied.
**Outcome:** `Luigi confirmed`. Failing-before `TypeError: 'int' object is not iterable`; passing-after `1 passed`; tree reverted to clean at the buggy commit.

## P-04 — Final repository skeleton + Requirements Audit
**Stage:** scaffolding (current).
**Summary:** Create the final repo `ai-agentic-graph-debugging-assignment4` (group `MaRs-777`) with a fixed directory structure, README, requirements-audit table (45 requirements), decisions/prompts/AI-workflow/costs/quality/checklist docs, PRD/PLAN/TODO placeholders, uv-compatible `pyproject.toml`, `.env.example`, `.gitignore`, package and test placeholders, and report stubs. Skeleton + audit only — no clone of Luigi, no Graphify, no agent, no fix, no commit.
**Outcome:** Recorded in this repo; see `reports/` and `docs/`.

> Later stages (Graphify, Obsidian, agent workflow, fix, token-efficiency) will append P-05+ here as they run.
