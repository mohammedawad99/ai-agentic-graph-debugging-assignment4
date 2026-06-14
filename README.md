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
> **Stage 6 (Obsidian vault) complete** (commit `6cdfd2f`). **Stage 7 (reverse engineering) complete** (commit `8991916`). **Stage 8 (baseline naive investigation) complete** (commit `8904b57`) — 4 files / ~24,482 est. tokens / 5 rounds. **Stage 9 (graph-guided agent workflow) complete** (commit `3b0e3c0`) — a **deterministic LangGraph** workflow (no LLM, $0): graph/Obsidian-first context routing reads 5 targeted files / ~3,631 est. tokens / 8 states, root cause reached; see `reports/graph_guided_agent.md`.
> **Stage 10 (bug fix + before/after proof) complete** (commit `a3c59f1`) — the minimal 2-line fix to `TupleParameter.parse` is applied to `target_repo/luigi_buggy/` with a focused regression test; proven under Docker/Python 3.8.20 (before: `TypeError: 'int' object is not iterable`; after: `1 passed`); see `reports/bug_fix_validation.md`. **Stage 11 (token-efficiency comparison) is next.**
> **Stage 11 (token-efficiency comparison) complete** (commit `dad0413`) — graph-guided **~3,631** vs baseline **~24,482** est. tokens (`chars/4`) = **−20,851 (≈85.17%, ~6.74×) less context**, both reaching the same root cause; a **controlled** comparison (NOT a universal benchmark), $0/no LLM; see `reports/token_efficiency.md`. **Stage 12 (original extension — centrality-based suspect ranking) is next.** Still **no** original extension and **no** final audit yet. Nothing here claims a completed stage that has not been completed.

## Planned workflow stages
1. **Skeleton + Requirements Audit** ✅
2. PRD / PLAN / TODO ✅ (`docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`)
3. **Target source acquisition** ✅ — Luigi at the buggy commit **vendored** under `target_repo/luigi_buggy/` (tracked, pristine, LICENSE preserved; commit `1299535`; see `docs/DECISIONS.md` D-007)
4. **Graphify** run → `graph.json`, `GRAPH_REPORT.md` (`artifacts/graphify/`) ✅ (commit `feb78ea`)
5. **Obsidian vault** → `obsidian/index.md`, `obsidian/hot.md`, linked analysis pages (macro/meso/micro) ✅ (commit `6cdfd2f`)
6. Reverse engineering + architecture **block diagram** + **OOP diagram** (`artifacts/diagrams/`) ✅ (commit `8991916`)
7. **Baseline naive investigation** (Stage 8) ✅ (commit `8904b57`); **graph-guided LangGraph agent** (Stage 9) ✅ (commit `3b0e3c0`, deterministic/no LLM)
8. **Bug fix** + **before/after** test proof ✅ (commit `a3c59f1`, proven under Docker/Python 3.8)
9. **Token-efficiency comparison** report ✅ (commit `dad0413`, ~85% less context)
10. Original extension, final README, screenshots/diagrams, **final audit** ← _next stage_

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
