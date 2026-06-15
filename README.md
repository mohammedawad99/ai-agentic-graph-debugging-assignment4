# ai-agentic-graph-debugging-assignment4

**Agentic, graph-guided debugging of a real Python bug** — Assignment 04, _Agentic Software Engineering / Vibe Coding_.

- **Group code:** `MaRs-777`
- **Repository:** https://github.com/mohammedawad99/ai-agentic-graph-debugging-assignment4 (branch `main`)
- **Selected target:** **Luigi — bug 3** from the **BugsInPy** dataset
  - File under investigation: `luigi/parameter.py` → `TupleParameter.parse` (vendored at `target_repo/luigi_buggy/`)
  - Buggy commit: `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`
  - Regression test: `test/parameter_test.py::TestSerializeTupleParameter::testSerialize`

## What this project does
Reverse-engineers an unfamiliar Python codebase (**Luigi**), builds a code graph with **Graphify**,
documents it as an **Obsidian** knowledge vault, then runs a **deterministic LangGraph agent workflow**
that investigates the bug **graph-guided**, compared against a **baseline naive** workflow on **token
efficiency** — then applies a **minimal real fix** with **before/after test proof**, plus an **original
extension** (centrality-based suspect ranking).

## Headline results
- **Bug fix (Stage 10):** `TupleParameter.parse` round-trip raised `TypeError: 'int' object is not iterable`;
  the minimal 2-line fix makes the regression test pass — **before: `1 failed (TypeError)` → after: `1 passed`**,
  proven faithfully under **Docker / Python 3.8.20**. See `reports/bug_fix_validation.md`.
- **Token efficiency (Stage 11, controlled single-case):** graph-guided **~3,631** vs naive baseline
  **~24,482** estimated tokens (`chars/4`) = **−20,851 (≈85.17%, ~6.74×) less context**, both reaching the
  same root cause. See `reports/token_efficiency.md`.
- **Original extension (Stage 12):** a deterministic, no-LLM centrality ranking places the bug method
  **`TupleParameter.parse` at rank #6 of 2,169** candidates (13 of the top 20 in `luigi/parameter.py`).
  See `reports/original_extension.md`.

## Architecture / Graphify / Obsidian summary
- **Graphify** (`graphifyy`, no LLM key) built `artifacts/graphify/graph.json` — **6,771 nodes / 15,365
  edges** — plus `GRAPH_REPORT.md` and a `GRAPH_TREE.html` visual.
- **Obsidian vault** (`obsidian/`) documents the graph macro→meso→micro (`index.md`, `hot.md`,
  `architecture-map.md`, `parameter-subsystem.md`, `graph-communities.md`, `reverse-engineering-analysis.md`).
- **Diagrams** (`artifacts/diagrams/*.mmd`): block architecture, `Parameter`→`ListParameter`→`TupleParameter`
  OOP, and the micro bug path.
- **Root cause:** `TupleParameter` overrides `parse` only and inherits `ListParameter.serialize` (`json.dumps`),
  so `serialize((1,2,3))` → `"[1, 2, 3]"`; `parse` then `json.loads` → `[1,2,3]` and runs `tuple(1)` → `TypeError`,
  which the narrow `except ValueError` does not catch.

## Research Questions (RQ1–RQ8)
Explicit answers (concise here; full versions with evidence links in `obsidian/research-questions.md`):
- **RQ1 — Architecture?** Luigi is a workflow/DAG engine (`Task`/`Target`/scheduler/`Parameter`); graph =
  6,771 nodes / 15,365 edges. → `reports/reverse_engineering.md`, `artifacts/diagrams/architecture_block.mmd`.
- **RQ2 — Central components?** Task model, parameters, scheduling, targets/IO, CLI. →
  `reports/reverse_engineering.md` §5, `obsidian/parameter-subsystem.md`.
- **RQ3 — God-nodes / risky hubs?** High-centrality hubs at task/register, scheduler, and the `Parameter`
  family (triage signal, not a smell verdict). → `obsidian/graph-communities.md`, `reports/original_extension.md`.
- **RQ4 — Block & OOP schema extraction?** From Graphify module/community structure and `inherits`/`method`
  edges in `graph.json`, confirmed vs source. → `artifacts/diagrams/{architecture_block,oop_parameter_diagram}.mmd`.
- **RQ5 — Bug & root cause?** `TupleParameter` inherits `ListParameter.serialize` (`json.dumps`) but
  overrides `parse`; round-trip `"[1, 2, 3]"` → `tuple(1)` → `TypeError`. Fix: widen guard + `tuple(...)`. →
  `reports/bug_analysis.md`, `reports/bug_fix_validation.md`, `artifacts/diagrams/bug_path.mmd`.
- **RQ6 — Graph vs linear reading?** Jumps to the bug neighborhood via edges; fewer characters to the same
  root cause (single-case). → `reports/token_efficiency.md`.
- **RQ7 — Token reduction (and what not)?** ~3,631 vs ~24,482 est. tokens (≈85.17%); did **not** reduce
  step count or model-reasoning cost (deterministic, no LLM). → `reports/token_efficiency.md`.
- **RQ8 — Original extension?** Deterministic centrality+relevance suspect ranking; bug method ranks
  **#6/2,169**. → `reports/original_extension.md`, `docs/PRD_centrality_ranking.md`.

Full answers: **`obsidian/research-questions.md`** (linked from `obsidian/index.md`).

## How to reproduce
```bash
uv sync --extra dev               # install deps (incl. pytest, ruff)
uv run pytest                     # project unit tests (16 pass, coverage ≥85% gate)
uv run ruff check .               # lint
uv run ruff format --check .      # format check
# Optional — regenerate the extension / graph-guided metrics (deterministic, no LLM):
uv run python -m ex04_graph_debugger.graph_guided_agent
uv run python -m ex04_graph_debugger.centrality_ranking
```
The **Luigi regression test** runs under Docker / Python 3.8 (Luigi 2.8.3 cannot import on host 3.12) —
exact command in `reports/bug_fix_validation.md`.

## Evidence map
| Stage | Report | Key artifacts |
|------|--------|---------------|
| Selection / acquisition | `reports/repository_selection.md`, `reports/target_repository_acquisition.md` | `target_repo/luigi_buggy/` |
| Graphify | `reports/graphify_run.md` | `artifacts/graphify/{graph.json, GRAPH_REPORT.md, GRAPH_TREE.html}` |
| Obsidian | — | `obsidian/*.md` |
| Reverse engineering | `reports/reverse_engineering.md` | `artifacts/diagrams/*.mmd` |
| Baseline (naive) | `reports/baseline_naive_investigation.md` | `artifacts/validation/baseline_naive_*` |
| Graph-guided agent | `reports/graph_guided_agent.md` | `artifacts/validation/graph_guided_agent_*`, `src/ex04_graph_debugger/` |
| Bug fix | `reports/bug_fix_validation.md` | `artifacts/validation/stage10_*` |
| Token efficiency | `reports/token_efficiency.md` | `artifacts/validation/token_efficiency_*` |
| Original extension | `reports/original_extension.md` | `artifacts/validation/centrality_suspect_ranking.*` |
| Final audit | `reports/final_audit.md` | — |

## Stage status (all implementation stages complete)
| # | Stage | Commit |
|---|-------|--------|
| 0–3 | Skeleton, PRD, PLAN, TODO | `3fc110d`, `018c580`, `8a7ff9c`, `485f3b5` |
| 4 | Target acquisition (vendored, D-007) | `1299535` |
| 5 | Graphify run | `feb78ea` |
| 6 | Obsidian vault | `6cdfd2f` |
| 7 | Reverse engineering + diagrams | `8991916` |
| 8 | Baseline naive investigation | `8904b57` |
| 9 | Graph-guided LangGraph agent | `3b0e3c0` |
| 10 | Bug fix + before/after proof | `a3c59f1` |
| 11 | Token-efficiency comparison | `dad0413` |
| 12 | Original extension | `de32d76` |
| 13 | README/docs hardening + final audit | `cf55bac` |

**Repository work is complete (Stages 0–13).** All quality gates pass and the final audit is done
(`reports/final_audit.md`). Submitting on Moodle is a manual step performed **outside this repository** and
is not tracked as a repo artifact, stage, or task.

## Repository layout
```
docs/        PRD, PLAN, TODO, requirements audit, AI workflow, prompts, decisions, costs, quality, checklist
src/         ex04_graph_debugger/ — graph-guided agent (LangGraph) + centrality ranking (≤150 lines/file)
tests/       unit/ — pytest tests for the agent and the extension
config/      default.toml (target + validation metadata)
target_repo/ vendored Luigi buggy source under luigi_buggy/ (tracked, pristine + Stage-10 fix; D-007)
artifacts/   graphify/ (graph), diagrams/ (.mmd), validation/ (metrics, before/after, rankings)
obsidian/    knowledge vault (index.md, hot.md, macro/meso/micro analysis pages)
reports/     selection, graphify, RE, baseline, graph-guided, bug-fix, token-efficiency, extension, final audit
```

## Tooling
- **uv** for environment/runs, **Ruff** for lint/format, **pytest** for tests (gate evidence in `docs/QUALITY.md`).
- **Docker + Python 3.8** for faithful BugsInPy validation (Luigi requires 3.8-era stdlib).
- Every Python file under `src/` is ≤150 code lines (project rule).

## Honest non-claims
- Token counts are **estimates** (`characters / 4`), **not** exact model-tokenizer counts.
- The token comparison is a **controlled, single-case** study — **not** a universal benchmark; it does not
  imply ~85% savings on other bugs.
- The centrality ranking is a **triage heuristic**, **not** proof of root cause.
- The graph-guided agent and the extension are **deterministic and use no LLM / no paid API ($0)**.
- The Luigi regression is a **focused** test, not a full upstream-suite run.

## Evidence & honesty policy
All metrics are labeled **measured / estimated / manual**. No fabricated evidence, no overclaiming, and
no self-assigned grade. See `docs/AI_WORKFLOW.md` and `reports/final_audit.md`.
