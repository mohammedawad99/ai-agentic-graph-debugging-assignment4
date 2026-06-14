# PRD — Product Requirements Document

**Project:** Agentic, graph-guided debugging of a real Python bug
**Repository:** `ai-agentic-graph-debugging-assignment4`
**Group code:** `MaRs-777`
**Course:** Agentic Software Engineering / Vibe Coding — Assignment 04
**Repository (live):** https://github.com/mohammedawad99/ai-agentic-graph-debugging-assignment4 — branch `main`, remote `origin`, latest commit `3fc110d "Initialize assignment 4 repository skeleton"`.
**Document status:** PRD stage. The GitHub repository **already exists and is pushed**; it currently
contains the **skeleton + docs (including this PRD)**. **No Luigi source is cloned yet, Graphify has not
run, the agent is not implemented, and the final bug fix is not applied.** Every forward-looking item
below is explicitly labeled **planned**.

---

## 1. Project overview
This project reverse-engineers an unfamiliar, mid-sized Python codebase (**Luigi**), builds a **code
graph** with **Graphify**, documents it as an **Obsidian knowledge vault**, and then runs an **AI agent
workflow** that investigates and fixes a **real, validated bug** in a **graph-guided** manner. The
central thesis is measured, not assumed: that steering an agent with a code graph makes bug
investigation **more token-efficient** than naive, unguided exploration — demonstrated by a controlled
comparison with **before/after test proof**.

## 2. Assignment context
Assignment 04 requires: reverse engineering of an unfamiliar Python codebase; Graphify outputs
(`graph.json`, `GRAPH_REPORT.md`); an Obsidian vault with linked pages (`index.md`, `hot.md`); an AI
agent workflow using **LangGraph or CrewAI**; a graph-guided bug investigation; a real bug fix with
before/after evidence; a **token-efficiency comparison** (baseline vs graph-guided); an architecture
block diagram and an OOP diagram; and a professional README with explanation, diagrams, workflow, root
cause, fix, and original extensions. The course further emphasizes engineering discipline (uv, Ruff,
pytest, a 150-line Python file rule, no secrets, no overclaiming).

## 3. Problem statement
Debugging an unfamiliar large codebase by reading files naively is expensive: an AI agent burns tokens
re-reading irrelevant modules, follows long trial-and-error paths, and may still miss the defect's true
location. A structural **code graph** (functions, classes, modules and their relationships) offers a
cheaper navigation strategy — hubs, communities, and call paths point the agent toward the defect
before it reads raw source. This project asks: **does graph-guidance reduce tokens, files read, and
iterations needed to locate and fix a real bug, without sacrificing correctness?**

## 4. Target users / readers
| Reader | What they need from this project |
|--------|----------------------------------|
| **Course grader** | Clear evidence each requirement is met; reproducible artifacts; honest status labels. |
| **Lecturer** | Demonstrated understanding of agentic, graph-guided engineering and the efficiency thesis. |
| **Student team (authors, MaRs-777)** | A disciplined plan, traceable decisions, and reusable structure. |
| **Future developer / reviewer** | Enough documentation to re-run the workflow, understand the bug, and extend the approach. |

## 5. Selected target
- **Project:** **Luigi** (Spotify's Python workflow / DAG scheduling engine).
- **Source dataset:** **BugsInPy** (curated real bugs with buggy/fixed commits and tests).
- **Bug:** **bug 3** — defect in `TupleParameter.parse` (`luigi/parameter.py`).
- **Buggy commit:** `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4` (Luigi 2.8.3).
- **Fixed commit (regression-test source):** `3a0bfbff69addfb3be1107adab3d4914bcae3e4b`.
- **Regression test:** `test/parameter_test.py::TestSerializeTupleParameter::testSerialize`.
- **Reason for choosing Luigi:** it satisfies the grade-100 size bar (see §6) **and** has an ideal graph
  story — a DAG/scheduler engine literally organized around tasks, parameters, dependencies, a
  scheduler, and workers, giving meaningful hubs, communities, and paths to analyze. The bug itself is a
  clean, isolated, one-function logic defect with a deterministic regression test — large enough to be
  interesting, small enough to fix minimally.

## 6. Grade-100 interpretation
The Moodle instruction states that, for excellent submissions, the codebase should be **significant —
approximately 10,000+ lines of code and at least 70 code files**. Interpretation adopted here:

- **Meaningful codebase:** the target must have real architecture (multiple subsystems, classes, and
  inter-module relationships), not a toy script.
- **Size target:** **~10,000+ Python LOC and ~70+ Python files.** Luigi at the buggy commit is
  **~96 files / ~27.6k LOC** (measured during selection), comfortably above both thresholds.
- **Why PySnooper was rejected:** PySnooper bug 3 was clean and reproduced even on Python 3.12, but the
  library is **~5 source files / ~700 LOC** — an order of magnitude below the bar. It is retained only as
  an emergency safety net, not the target. _(see `docs/DECISIONS.md` D-002)_
- **Why Tornado remains a fallback but Luigi is stronger:** Tornado bug 9 is excellent on setup safety
  (zero third-party dependencies) and bug cleanliness, and its bug logic was verified — but it has only
  **~34 non-test source files**, weaker against the "≥70 files" reading. Luigi satisfies **both** the LOC
  and the file-count criteria and offers a richer graph, so Luigi is primary and Tornado is the fallback.
  _(see `docs/DECISIONS.md` D-001, D-003)_

## 7. Goals and success criteria
- **G1 — Reverse engineering:** produce a defensible macro→meso→micro understanding of Luigi centered on
  the bug, evidenced by graph reading and Obsidian notes.
- **G2 — Graph artifacts:** generate Graphify `graph.json` and `GRAPH_REPORT.md` and use them, not just store them.
- **G3 — Agentic fix:** an AI agent (LangGraph preferred) localizes and fixes the bug graph-guided.
- **G4 — Proof:** failing-before and passing-after evidence for the regression test, reproduced in this repo.
- **G5 — Efficiency:** a measured comparison showing the graph-guided workflow reads fewer files/units,
  takes fewer iterations, and/or uses fewer tokens than the baseline, with honest provenance labels.
- **G6 — Original extension:** at least one capability beyond the minimum (see §20).
- **G7 — Discipline:** all quality gates pass; no secrets; no overclaiming.

**Success = all of G1–G7 evidenced in-repo**, with the regression test passing after the fix and the
efficiency comparison showing a real, labeled difference (or honestly reporting if it does not).

## 8. In-scope items
- Cloning Luigi at the buggy commit **into a git-ignored working area** (later stage).
- Graphify graph generation and reading (macro/meso/micro).
- Obsidian vault with linked analysis pages.
- One LangGraph (or CrewAI) agent workflow with two modes: baseline naive and graph-guided.
- Investigating, root-causing, and **minimally fixing only Luigi bug 3**.
- Before/after test evidence under Docker / Python 3.8.
- Token-efficiency comparison and one original extension.
- Architecture block diagram and OOP/class diagram.

## 9. Out-of-scope items
- Fixing any Luigi bug other than bug 3; refactoring Luigi's architecture.
- Upgrading Luigi to modern Python or modifying upstream beyond the minimal patch.
- Committing the raw cloned Luigi source into this repository.
- Production deployment, packaging for distribution, or performance tuning of Luigi.
- Any claim of being "production-ready."

## 10. Functional requirements
| ID | Requirement |
|----|-------------|
| FR-01 | Acquire Luigi at commit `a0f1db01…` into a git-ignored working area; record provenance. |
| FR-02 | Run Graphify over the target and produce `graph.json`. |
| FR-03 | Produce `GRAPH_REPORT.md` summarizing nodes, edges, hubs, and communities. |
| FR-04 | Provide graph **reading evidence** at macro, meso, and micro levels. |
| FR-05 | Build an Obsidian vault with `index.md` navigation and linked analysis pages. |
| FR-06 | Provide `hot.md` capturing hubs/hotspots and the bug's focused context. |
| FR-07 | Implement an AI agent workflow (LangGraph preferred) with a **baseline naive** mode. |
| FR-08 | Implement a **graph-guided** mode that consults graph artifacts before reading raw code. |
| FR-09 | Agent localizes the defect (`TupleParameter.parse`) and explains detection. |
| FR-10 | Produce a written **root-cause** analysis. |
| FR-11 | Apply a **minimal real patch** fixing only bug 3. |
| FR-12 | Capture **failing-before** evidence for the regression test (in this repo). |
| FR-13 | Capture **passing-after** evidence for the same test (in this repo). |
| FR-14 | Record per-mode metrics: files/text units read, iterations, token counts/estimates. |
| FR-15 | Produce the **token-efficiency comparison** report (baseline vs graph-guided). |
| FR-16 | Produce a **block architecture diagram** and an **OOP/class diagram**. |
| FR-17 | Implement at least one **original extension** (see §20). |
| FR-18 | Provide a complete README and the supporting docs (AI workflow, prompts, decisions, costs, quality). |
| FR-19 | Provide a quality-gate checker for the **150-line** Python file rule over `src/`. |
| FR-20 | Provide a reproducible run path using **Docker / Python 3.8** for target tests. |

## 11. Non-functional requirements
| ID | Requirement |
|----|-------------|
| NFR-01 | **Reproducibility:** documented commands re-create artifacts and test results. |
| NFR-02 | **Honesty:** every numeric claim labeled measured / estimated / manual; no fabricated evidence. |
| NFR-03 | **Bounded agent cost:** agent runs use bounded steps and controlled context (no uncontrolled full-repo reads). |
| NFR-04 | **Maintainability:** project Python files ≤ 150 lines; clear module boundaries. |
| NFR-05 | **Security:** no secrets/API keys committed; `.env` git-ignored. |
| NFR-06 | **Tooling consistency:** uv for env/runs, Ruff for lint/format, pytest for tests. |
| NFR-07 | **Portability:** target validation isolated in Docker so host Python version is irrelevant. |
| NFR-08 | **Traceability:** requirements ↔ artifacts ↔ evidence cross-referenced (`docs/REQUIREMENTS_AUDIT.md`). |
| NFR-09 | **Readability:** documentation is professional, specific, and free of marketing language. |
| NFR-10 | **Minimal footprint:** large generated artifacts are git-ignored or deliberately curated. |

## 12. Acceptance criteria
| ID | Criterion (met when…) |
|----|------------------------|
| AC-01 | `artifacts/graphify/graph.json` exists and is valid JSON with node/edge counts reported. |
| AC-02 | `artifacts/graphify/GRAPH_REPORT.md` exists and references hubs/communities derived from `graph.json`. |
| AC-03 | `obsidian/index.md` links to ≥3 analysis pages that resolve; `obsidian/hot.md` lists graph-derived hubs. |
| AC-04 | The repo contains a failing-before log and a passing-after log for the regression test, both reproducible under Docker/Python 3.8. |
| AC-05 | The applied fix is a minimal diff confined to `TupleParameter.parse`; no unrelated changes. |
| AC-06 | `reports/token_efficiency.md` contains a baseline-vs-graph-guided table with files-read, iterations, and token values, each provenance-labeled. |
| AC-07 | At least one original extension is implemented and described, with its output committed. |
| AC-08 | Block architecture diagram and OOP diagram are present and embedded in the README. |
| AC-09 | All quality gates (pytest, Ruff check/format, 150-line rule, secret scan) pass before submission. |
| AC-10 | `docs/REQUIREMENTS_AUDIT.md` shows every mandatory requirement satisfied with in-repo evidence; no overclaiming. |

## 13. Required deliverables
- **GitHub repository** (public) with group code `MaRs-777` — **done:** created and pushed at
  https://github.com/mohammedawad99/ai-agentic-graph-debugging-assignment4 (branch `main`, commit `3fc110d`).
  The repo currently holds the skeleton + docs; the deliverables below are still **planned**.
- **README.md** — full explanation, diagrams, workflow, root cause, fix, extensions.
- **Graphify artifacts** — `artifacts/graphify/graph.json`, `GRAPH_REPORT.md` (+ any HTML graph if generated).
- **Obsidian vault** — `obsidian/index.md`, `obsidian/hot.md`, plus linked analysis pages.
- **Bug analysis report** — `reports/bug_analysis.md`.
- **Token-efficiency report** — `reports/token_efficiency.md`.
- **Before/after report** — `reports/before_after.md` (+ logs under `artifacts/validation/`).
- **Architecture diagrams** — block diagram and **OOP/class diagram** under `artifacts/diagrams/`.
- **Agent workflow** — code under `src/ex04_graph_debugger/` (baseline + graph-guided).

## 14. Reverse engineering requirements
- **Macro graph reading:** whole-system shape — packages/subsystems and their coarse dependencies.
- **Meso subsystem analysis:** the `parameter` subsystem (and neighbors `task`, `scheduler`, `worker`) around the bug.
- **Micro bug-path analysis:** the defect site `TupleParameter.parse`, its callers/callees, and the path from the public API (`luigi.TupleParameter`) to the failing test.
- **Hubs:** identify highest-degree/most-central nodes and justify with graph metrics.
- **Communities:** identify clusters (e.g., core vs `contrib`) and where the bug sits.
- **God nodes / bottlenecks:** flag oversized or overly-connected nodes that concentrate risk.
- **Traceability:** explicit mapping requirement → graph evidence → source location → test.

## 15. Graphify requirements
- Produce **`graph.json`** (machine-readable graph of nodes/edges).
- Produce **`GRAPH_REPORT.md`** (human summary: counts, hubs, communities, notable structures).
- Include **graph/HTML artifacts** if the tool generates an interactive view (otherwise note none).
- Provide **reading evidence**: concrete observations drawn from the graph that guided the investigation,
  not just stored files. All metrics labeled **measured** from `graph.json`.

## 16. Obsidian requirements
- The vault is an **active knowledge space**, not a dump: pages are written to be read and navigated.
- **Linked Markdown pages** using `[[wiki-links]]` that resolve within the vault.
- **`index.md`** provides navigation across macro/meso/micro pages and reports.
- **`hot.md`** captures the focused bug context (hubs/hotspots and the defect's path).

## 17. Agentic AI requirements
- **Framework:** **LangGraph preferred**; switch to CrewAI only if later implementation evidence favors it _(docs/DECISIONS.md D-004)_.
- **Graph-before-code:** the graph-guided mode consults graph artifacts (hubs, paths, communities) **before** reading raw source.
- **Bounded steps:** each run has an explicit step/iteration cap.
- **Controlled context:** the agent reads selected, justified files — **no uncontrolled reading of all files**.
- The **baseline** mode deliberately omits graph guidance to make the comparison meaningful.

## 18. Bug investigation requirements
- **Failing-before evidence:** the regression test fails on the buggy source (captured log).
- **Root cause:** a written explanation of why the defect occurs.
- **Minimal patch:** the smallest correct change, confined to `TupleParameter.parse`.
- **Passing-after evidence:** the same test passes post-fix (captured log).
- **Cleanup / reproducibility:** documented commands; isolated Docker/Python 3.8 run; no stray artifacts.

## 19. Token-efficiency requirements
- Run **baseline naive** and **graph-guided** workflows on the **same** bug, model, and success criterion.
- Record for each: **number of files / text units read**, **number of iterations / agent steps**,
  **token counts or estimates**, and whether the correct fix was reached.
- Present a side-by-side comparison in `reports/token_efficiency.md`.
- **Label every value** as **measured**, **estimated**, or **manual count** (per `docs/COSTS.md`).
- Report honestly if the graph-guided advantage is small, absent, or context-dependent.

## 20. Original extension requirements
At least **one** capability beyond the assignment minimum, with committed output. Candidate options:
- **Centrality-based suspect ranking** — rank likely defect sites by graph centrality and compare to the actual bug location.
- **Impact report** — what depends on `TupleParameter.parse`; blast radius of the change.
- **Before/after graph comparison** — graph diff between buggy and fixed commits.
- **Dynamic `hot.md` generation** — auto-produce `hot.md` from `graph.json`.
- **Traceability path report** — automated path from public API → defect → test.

The chosen extension is finalized in PLAN; this PRD only fixes the requirement that one exists.

## 21. Documentation requirements
- **README.md:** project title, context, group code, selected target, validation summary, workflow, root
  cause, fix, diagrams/screenshots, original extensions, honesty policy. No self-score.
- **`docs/AI_WORKFLOW.md`:** how AI is used per stage; student responsibility; review-before-commit.
- **`docs/PROMPTS.md`:** paraphrased prompt summaries per stage (no fabricated or hidden content).
- **`docs/DECISIONS.md`:** numbered decisions with context and consequence.
- **`docs/COSTS.md`:** cost awareness and the provenance-labeling rule.
- **`docs/QUALITY.md`:** the quality gates and how they run.

## 22. Quality requirements
- **uv** for environment and command execution (`uv run …`).
- **pytest** for the test suite (target tests run under Docker/Python 3.8).
- **Ruff** for lint (`ruff check`) and format (`ruff format --check`).
- **150-line rule:** every Python file under `src/` ≤ 150 lines, enforced by a checker.
- **No secrets** committed; **no fake evidence**; **no overclaiming** (status labels must match reality).

## 23. Security / configuration requirements
- Secrets only in a local, git-ignored `.env`; the repo ships `.env.example` with empty placeholders.
- No API keys, tokens, or private data in tracked files; a secret scan runs before submission.
- Configuration centralized in `config/default.toml`; runtime/model choices documented, not hard-coded with secrets.
- The agent stage may require an LLM API key locally; it is never committed and its presence is optional until that stage.

## 24. Risks and mitigations
| Risk | Mitigation |
|------|------------|
| Luigi requires Python 3.7/3.8 (won't import on host 3.12). | Run all target tests in Docker `python:3.8-slim` _(D-005)_. |
| Graphify scope explodes on ~27.6k LOC. | Focus analysis on the core subsystem (task/parameter/scheduler/worker); note exclusions. |
| Token measurement may be imprecise. | Label provenance; prefer measured counters; state estimation method when used. |
| Agent reads too much (defeats the thesis). | Enforce bounded steps and controlled, justified file access (NFR-03). |
| Graph-guided advantage could be small. | Report honestly; the contribution is the measured comparison, not a guaranteed win. |
| Accidental commit of raw target source/secrets. | `.gitignore` for `target_repo/luigi/` and `.env`; artifact/secret scans in quality gates. |
| Overclaiming completed stages. | Status labels in `REQUIREMENTS_AUDIT.md`; evidence policy (§27). |

## 25. Assumptions
- BugsInPy metadata for Luigi bug 3 is accurate (validated: fail→pass already reproduced in a candidate repo).
- Docker Desktop with WSL integration remains available for Python 3.8 runs.
- Graphify can ingest a Python project of this size and emit `graph.json` + a report.
- An LLM API key will be available locally for the agent stage (not required before then).

## 26. Constraints
- Faithful target tests run only under **Python 3.8** (via Docker), not the host's 3.12.
- The fix must remain **minimal** and confined to the bug; no broader refactoring.
- The raw Luigi source must **not** be committed to this repository.
- Work proceeds stage-by-stage; **no implementation before PRD/PLAN/TODO approval** _(D-006)_.
- No paid services beyond a single LLM provider used locally in the agent stage.

## 27. Evidence policy
- **Planned vs actual:** forward-looking items are labeled *planned*; only in-repo artifacts are called done.
- **Measured vs estimated vs manual:** every metric carries one of these labels; unlabeled numbers are disallowed.
- **No fake screenshots/logs:** all images and logs must be reproducible from documented commands.
- **No premature claims:** no Graphify graph, Obsidian analysis, agent result, or fix is claimed before its artifact exists in the repo.
- The current truthful state: the **GitHub repo exists and is pushed** with **skeleton + docs/PRD only**;
  Luigi is not cloned, Graphify has not run, the agent is not built, and the fix is not applied.
  Validation of the bug was done in a *temporary candidate repo* and is summarized here, not re-claimed as final-repo evidence.

## 28. Milestones / high-level stages
1. **Skeleton + Requirements Audit** — done (prior stage); **GitHub repo created and pushed** (`main`, `3fc110d`).
2. **PRD** — this document.
3. **PLAN / TODO** — finalize and approve.
4. **Acquire target** — Luigi at buggy commit into git-ignored `target_repo/`.
5. **Graphify** — `graph.json` + `GRAPH_REPORT.md`.
6. **Obsidian vault** — `index.md`, `hot.md`, analysis pages.
7. **Diagrams** — block + OOP.
8. **Agent workflow** — baseline + graph-guided.
9. **Fix + before/after** — minimal patch, fail→pass evidence in-repo.
10. **Token efficiency** — comparison report.
11. **Extension + polish + final audit.**

## 29. Definition of done
The project is done when **all of G1–G7 (§7)** are evidenced and **AC-01…AC-10 (§12)** hold:
all mandatory deliverables exist in the repo with reproducible evidence; the regression test passes
after a minimal fix; the token-efficiency comparison is complete and provenance-labeled; one original
extension is implemented; all quality gates pass; `docs/REQUIREMENTS_AUDIT.md` and the final audit show
no missing mandatory requirement and no overclaiming.

## 30. Open questions
- **OQ-1:** Which Graphify output format/granularity (function-level vs module-level) best supports the agent? _(resolve in Graphify stage)_
- **OQ-2:** Final choice of the original extension (centrality ranking vs impact report vs graph-diff). _(resolve in PLAN)_
- **OQ-3:** Token accounting fidelity — can we capture exact provider token usage, or must some values be estimated? _(resolve in agent stage)_
- **OQ-4:** Baseline fairness — what exact constraints make the naive baseline a fair, non-strawman comparison? _(resolve in PLAN)_
- **OQ-5:** How much of Luigi's `contrib/` to include in the graph without diluting the core analysis? _(resolve in Graphify stage)_
- **OQ-6:** Confirm LangGraph over CrewAI once a thin prototype exists _(D-004)_.
