# Requirements Audit — Assignment 04 (Group MaRs-777)

Final traceability of every requirement to its in-repo evidence.

- **Repository status:** complete through **Stage 13** (Stages 0–13 done, committed, and pushed).
- **Final repository-scope correction baseline:** `2561f1b`.
- **Final documentation consistency polish (latest documentation commit):** `a683db1`.
- The external course submission is a **manual step performed outside this repository** — it is **not** a repo
  artifact, stage, or task, and is not tracked here.

**Status legend:** `DONE` (complete with in-repo evidence) · `N/A`. Every `DONE` row names a real evidence path.

| ID | Category | Requirement | M/R | Evidence (path) | Status |
|----|----------|-------------|-----|-----------------|:------:|
| R-01 | Submission | Public GitHub repo pushed | M | `github.com/mohammedawad99/ai-agentic-graph-debugging-assignment4` (branch `main`) | DONE |
| R-02 | Submission | Group code `MaRs-777` visible | M | `README.md`, `docs/*` headers | DONE |
| R-03 | Selection | Luigi/BugsInPy bug 3 selected w/ justification | M | `reports/repository_selection.md`, `docs/DECISIONS.md` D-001 | DONE |
| R-04 | Selection | Meaningful size / grade-100 interpretation | M | `reports/repository_selection.md` (~96 files / ~27.6k LOC); vendored tree 244 py / 58.6k LOC | DONE |
| R-05 | Reverse-eng | Unfamiliar Python codebase analyzed | M | `reports/reverse_engineering.md`, `obsidian/reverse-engineering-analysis.md` | DONE |
| R-06 | Graphify | Graphify outputs produced | M | `artifacts/graphify/`, `reports/graphify_run.md` | DONE |
| R-07 | Graphify | `graph.json` present (valid JSON) | M | `artifacts/graphify/graph.json` (6,771 nodes / 15,365 links) | DONE |
| R-08 | Graphify | `GRAPH_REPORT.md` present | M | `artifacts/graphify/GRAPH_REPORT.md` (+ `GRAPH_TREE.html`) | DONE |
| R-09 | Obsidian | Linked Markdown vault | M | `obsidian/*.md` (resolving `[[links]]`) | DONE |
| R-10 | Obsidian | `index.md` entry page | M | `obsidian/index.md` | DONE |
| R-11 | Obsidian | `hot.md` bug-context page | M | `obsidian/hot.md` | DONE |
| R-12 | Obsidian | Additional linked analysis pages | M | `obsidian/{architecture-map,parameter-subsystem,graph-communities,reverse-engineering-analysis,…}.md` | DONE |
| R-13 | Reverse-eng | Documented reverse engineering | M | `reports/reverse_engineering.md` | DONE |
| R-14 | Graph reading | Macro / meso / micro reading | M | `reports/reverse_engineering.md` §4–6; `obsidian/*` | DONE |
| R-15 | Diagrams | Block architecture diagram | M | `artifacts/diagrams/architecture_block.mmd` | DONE |
| R-16 | Diagrams | OOP / class diagram | M | `artifacts/diagrams/oop_parameter_diagram.mmd` (+ `bug_path.mmd`) | DONE |
| R-17 | Agent | AI agent workflow (LangGraph) | M | `src/ex04_graph_debugger/` (8-state graph), `reports/graph_guided_agent.md` | DONE |
| R-18 | Agent | Graph-guided investigation path | M | `artifacts/validation/graph_guided_agent_*` (graph/Obsidian-first) | DONE |
| R-19 | Agent | Baseline naive path | M | `reports/baseline_naive_investigation.md`, `artifacts/validation/baseline_naive_*` | DONE |
| R-20 | Debugging | Bug detection | M | `reports/reverse_engineering.md`, `reports/graph_guided_agent.md` | DONE |
| R-21 | Debugging | Root-cause explanation | M | `reports/reverse_engineering.md` §6, `reports/bug_fix_validation.md` §4 | DONE |
| R-22 | Debugging | Real code fix | M | `target_repo/luigi_buggy/luigi/parameter.py` (`except (ValueError, TypeError)` + `tuple(literal_eval(x))`), commit `a3c59f1` | DONE |
| R-23 | Debugging | Before/after proof (in repo) | M | `artifacts/validation/stage10_{before_failure,after_success,fix_diff}.txt`, `reports/bug_fix_validation.md` | DONE |
| R-24 | Debugging | Failing test BEFORE fix | M | `artifacts/validation/stage10_before_failure.txt` (`TypeError`, 1 failed) | DONE |
| R-25 | Debugging | Passing test AFTER fix | M | `artifacts/validation/stage10_after_success.txt` (`1 passed`) | DONE |
| R-26 | Tokens | Token counts/estimates (labeled) | M | `reports/token_efficiency.md` (chars/4): baseline 24,482 vs graph-guided 3,631 | DONE |
| R-27 | Tokens | Files / text units read | M | baseline 4/4 vs graph-guided 5/7 (`token_efficiency_comparison.json`) | DONE |
| R-28 | Tokens | Iteration counts | M | baseline 5 rounds vs graph-guided 8 states | DONE |
| R-29 | Tokens | Token-efficiency comparison report | M | `reports/token_efficiency.md` (+ `.json`/`.csv`), commit `dad0413` | DONE |
| R-30 | Originality | Original extension | M | `src/ex04_graph_debugger/centrality_ranking.py`, `reports/original_extension.md` (bug method rank #6/2,169) | DONE |
| R-31 | Evidence | Diagrams present | M | 3 `.mmd` diagrams + `GRAPH_TREE.html` (no raster screenshots included) | DONE |
| R-32 | Docs | README with full explanation | M | `README.md` (context, reproduce, evidence map, results, non-claims) | DONE |
| R-33 | Docs | AI workflow documentation | M | `docs/AI_WORKFLOW.md` | DONE |
| R-34 | Docs | Prompts documentation | M | `docs/PROMPTS.md` (P-01…P-15) | DONE |
| R-35 | Docs | Decisions documentation | M | `docs/DECISIONS.md` (D-001…D-015) | DONE |
| R-36 | Docs | Cost / resource awareness | M | `docs/COSTS.md` ($0 LLM/API for all runs) | DONE |
| R-37 | Quality | Quality gates defined & run | M | `docs/QUALITY.md`; pytest 13 pass / ruff clean | DONE |
| R-38 | Quality | uv usage | M | `pyproject.toml`, README reproduce steps | DONE |
| R-39 | Quality | Ruff lint/format | M | `uv run ruff check .` / `format --check` → clean | DONE |
| R-40 | Quality | pytest test suite | M | `tests/unit/`, `uv run pytest` → 13 passed | DONE |
| R-41 | Quality | 150-line Python file rule | M | 7 `src/` files, max 142 code lines (`docs/QUALITY.md`) | DONE |
| R-42 | Security | No secrets / API keys committed | M | `.gitignore` (`.env` ignored), `.env.example` empty | DONE |
| R-43 | Validation | Docker / Python 3.8 validation | M | `reports/bug_fix_validation.md`, `config/default.toml` (3.8.20) | DONE |
| R-44 | Honesty | No overclaiming / no fake evidence | M | provenance labels; `reports/final_audit.md` claims audit | DONE |
| R-45 | Audit | Final audit | M | `reports/final_audit.md` | DONE |

## Honest limitations (carried into all reports)
- Token figures are **estimates** (`characters / 4`), **not** exact model-tokenizer counts.
- The token comparison is a **controlled, single-case** study — **not** a universal benchmark.
- The centrality ranking is a **triage heuristic**, **not** proof of root cause.
- The agent workflow and the extension are **deterministic and use no LLM / no paid API ($0)**.
- The Luigi regression is a **focused** test under Docker/Python 3.8, not a full upstream-suite run.

## Coverage summary
All mandatory requirements (R-01 … R-45) are **DONE** with in-repo evidence. The only step outside the
repository is the manual Moodle submission, which is **not** a repository deliverable.
