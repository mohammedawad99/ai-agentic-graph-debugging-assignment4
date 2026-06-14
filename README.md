# ai-agentic-graph-debugging-assignment4

**Agentic, graph-guided debugging of a real Python bug** — Assignment 04, _Agentic Software Engineering / Vibe Coding_.

- **Group code:** `MaRs-777`
- **Selected target:** **Luigi — bug 3** from the **BugsInPy** dataset
  - File under investigation: `luigi/parameter.py` → `TupleParameter.parse`
  - Regression test: `test/parameter_test.py::TestSerializeTupleParameter::testSerialize`
  - Buggy commit: `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`

## What this project will do (scope)
Reverse-engineer an unfamiliar Python codebase (Luigi), build a code graph with **Graphify**, document it as an **Obsidian** knowledge vault, then run an **AI agent workflow** (LangGraph preferred) that investigates and fixes the bug **graph-guided**, compared against a **baseline naive** workflow on **token efficiency**, with **before/after test proof**.

## Validation summary (done)
The selected bug was **faithfully reproduced and validated in Docker** using **Python 3.8.20**:
- Failing-before: target test raised `TypeError: 'int' object is not iterable` on the buggy commit.
- Passing-after: the known 2-line fix to `TupleParameter.parse` made the same test pass.
- The temporary validation checkout was **reverted to pristine** afterward.
- **No final fix is implemented in this repository yet.** See `reports/bug_validation.md`.

## Current repository status
> **Skeleton + Requirements Audit ONLY.**
> There are **no** final Graphify artifacts, **no** Obsidian analysis pages beyond placeholders, **no** AI agent, and **no** bug fix in this repository yet. Nothing here claims a completed stage that has not been completed.

## Planned workflow stages
1. **Skeleton + Requirements Audit** ← _current stage_
2. PRD / PLAN / TODO approval (`docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`)
3. Bring in target source (Luigi at the buggy commit) — under `target_repo/` (git-ignored), never committed raw
4. **Graphify** run → `graph.json`, `GRAPH_REPORT.md` (`artifacts/graphify/`)
5. **Obsidian vault** → `obsidian/index.md`, `obsidian/hot.md`, linked analysis pages (macro/meso/micro)
6. Architecture **block diagram** + **OOP diagram** (`artifacts/diagrams/`)
7. **AI agent workflow** (LangGraph) — baseline vs graph-guided
8. **Bug fix** + **before/after** test proof
9. **Token-efficiency comparison** report
10. Final README, screenshots/diagrams, original extensions, **final audit**

## Repository layout
```
docs/        requirements audit, PRD/PLAN/TODO, AI workflow, prompts, decisions, costs, quality, checklist
src/         ex04_graph_debugger package (placeholder; implemented in later stages)
tests/       unit/ and integration/ (empty; tests added with implementation)
config/      default.toml (target + validation metadata)
target_repo/ where Luigi source will be placed later (git-ignored; not present yet)
artifacts/   graphify/, screenshots/, diagrams/, validation/ outputs (later stages)
obsidian/    knowledge vault (index.md, hot.md + analysis pages later)
reports/     selection, validation, analysis, token-efficiency, before/after, final audit
```

## Tooling
- **uv** for environment/runs, **Ruff** for lint/format, **pytest** for tests.
- **Docker + Python 3.8** for faithful BugsInPy validation (Luigi requires 3.8-era stdlib).
- See `docs/QUALITY.md` for the planned quality gates (including the ≤150-line Python file rule and secret scanning).

## Evidence & honesty policy
All token counts and metrics will be explicitly labeled **measured / estimated / manual**. No fabricated evidence, no overclaiming, and no self-assigned grade. See `docs/AI_WORKFLOW.md`.
