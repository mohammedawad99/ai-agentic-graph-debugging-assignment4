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
> **Skeleton + PRD/PLAN/TODO done; Stage 4 (target acquisition) complete** (commit `1299535`). **Stage 5 (Graphify) complete** (commit `feb78ea`) — real graph built with the official `graphifyy` tool (no LLM key): `artifacts/graphify/graph.json` (6,771 nodes / 15,365 edges), `GRAPH_REPORT.md`, and a `GRAPH_TREE.html` visual; see `reports/graphify_run.md`.
> **Stage 6 (Obsidian vault) complete** (commit `6cdfd2f`). **Stage 7 (reverse engineering) is IN PROGRESS** — `reports/reverse_engineering.md` + Mermaid diagrams (`artifacts/diagrams/architecture_block.mmd`, `oop_parameter_diagram.mmd`, `bug_path.mmd`) + `obsidian/reverse-engineering-analysis.md`, all evidence-tagged (EXTRACTED/INFERRED); commit pending.
> The buggy Luigi source is vendored under `target_repo/luigi_buggy/` (pristine, no fix applied).
> Still **no** AI agent, **no** baseline, **no** token comparison, and **no** bug fix yet.
> There are still **no** Graphify artifacts, **no** Obsidian analysis pages beyond placeholders, **no** AI agent, and **no** bug fix in this repository yet. Nothing here claims a completed stage that has not been completed.

## Planned workflow stages
1. **Skeleton + Requirements Audit** ✅
2. PRD / PLAN / TODO ✅ (`docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`)
3. **Target source acquisition** ✅ — Luigi at the buggy commit **vendored** under `target_repo/luigi_buggy/` (tracked, pristine, LICENSE preserved; commit `1299535`; see `docs/DECISIONS.md` D-007)
4. **Graphify** run → `graph.json`, `GRAPH_REPORT.md` (`artifacts/graphify/`) ✅ (commit `feb78ea`)
5. **Obsidian vault** → `obsidian/index.md`, `obsidian/hot.md`, linked analysis pages (macro/meso/micro) ✅ (commit `6cdfd2f`)
6. Reverse engineering + architecture **block diagram** + **OOP diagram** (`artifacts/diagrams/`) ← _next stage_
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
target_repo/ vendored Luigi buggy source under luigi_buggy/ (tracked, pristine; D-007)
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
