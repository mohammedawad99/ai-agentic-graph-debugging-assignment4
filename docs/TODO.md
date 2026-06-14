# TODO — Stage-by-Stage Execution Checklist

**Project:** Agentic, graph-guided debugging of a real Python bug — Assignment 04 (group `MaRs-777`)
**Repository:** `ai-agentic-graph-debugging-assignment4` · branch `main`
**Document status:** TODO stage (Stage 3, IN_PROGRESS). This list operationalizes `docs/PRD.md` and
`docs/PLAN.md`. It does **not** implement anything.

## 1. Project status summary
- **Done & committed:** Stage 0 skeleton + requirements audit (`3fc110d`), Stage 1 PRD (`018c580`), Stage 2 PLAN (`8a7ff9c`), Stage 3 TODO (`485f3b5`).
- **Done & committed:** Stage 4 — target repository acquisition (Luigi source vendored to `target_repo/luigi_buggy/`, validated) — commit `1299535`.
- **Next up:** Stage 5 — Graphify setup and first graph run (PLANNED).
- **Confirmed target:** Luigi bug 3 (BugsInPy), buggy commit `a0f1db01…`; fail→pass validated in a **temporary candidate repo** under Docker/Python 3.8.20.
- **Not started (planned):** Luigi import into this repo, Graphify, Obsidian analysis, reverse-engineering, baseline, agent, fix, token comparison, extension, doc hardening, audit, submission.

## 2. Status legend
| Status | Meaning |
|--------|---------|
| **DONE** | Complete **with in-repo evidence** (commit/artifact exists). |
| **IN_PROGRESS** | Actively being worked; not yet evidenced. |
| **PLANNED** | Defined, not started. |
| **BLOCKED** | Cannot proceed until a dependency/decision is resolved. |
| **DEFERRED** | Intentionally postponed (may become optional). |

## 3. Core rules
- **R1 — Evidence rule:** no stage is marked **DONE** unless reproducible in-repo evidence exists (commit, artifact, or log).
- **R2 — Gate rule:** implementation (Stage 4+) starts **only after** PRD, PLAN, and TODO are committed.
- **R3 — Honesty rule:** numbers are labeled `measured | estimated | manual`; no fabricated evidence; no overclaiming; no self-score.
- **R4 — Vendoring rule (D-007):** the Luigi source is **vendored** under `target_repo/luigi_buggy/` (tracked, Apache-2.0, LICENSE preserved, no nested `.git`) and kept **pristine** at the buggy commit; source changes are allowed only in the later bug-fix stage (Stage 10), captured as diff/logs.

## 4. Stage table
| # | Stage | Status | Goal | Entry criteria | Exit criteria | Expected commit message |
|---|-------|--------|------|----------------|---------------|--------------------------|
| 0 | Skeleton + Requirements Audit | **DONE** | repo structure + audit | course brief | skeleton + audit committed | `Initialize assignment 4 repository skeleton` |
| 1 | PRD | **DONE** | product requirements | Stage 0 done | PRD committed | `Write assignment 4 PRD` |
| 2 | Technical PLAN | **DONE** | implementation strategy | PRD done | PLAN committed | `Write assignment 4 technical plan` |
| 3 | TODO | **IN_PROGRESS** | execution checklist | PLAN done | TODO reviewed + committed | `Write assignment 4 execution TODO` |
| 4 | Target repo acquisition | **DONE** (`1299535`) | import Luigi@buggy | TODO committed (R2) | target present + provenance + counts verified (vendored, pristine) | `Acquire Luigi buggy target repository` |
| 5 | Graphify first run | **PLANNED** | build code graph | Stage 4 done | `graph.json` + `GRAPH_REPORT.md` present + run logged | `Add Graphify graph and report for Luigi` |
| 6 | Obsidian vault | **PLANNED** | active knowledge vault | Stage 5 done | linked vault (index/hot + pages) resolves | `Build Obsidian vault for Luigi analysis` |
| 7 | Reverse engineering | **PLANNED** | macro/meso/micro + diagrams | Stage 5–6 done | RE notes + block + OOP diagrams present | `Add reverse-engineering analysis and diagrams` |
| 8 | Baseline naive run | **PLANNED** | uninformed investigation metrics | Stage 4 done | baseline report + logs present | `Add baseline naive investigation run` |
| 9 | Graph-guided agent | **PLANNED** | LangGraph graph-guided run | Stage 5–6 done | graph-guided report + logs present | `Add graph-guided LangGraph agent workflow` |
| 10 | Fix + before/after | **PLANNED** | minimal fix + proof | Stage 4 (+9) done | fail-before + pass-after logs + diff evidence | `Add Luigi bug 3 fix with before/after evidence` |
| 11 | Token-efficiency comparison | **PLANNED** | baseline vs graph-guided | Stages 8–9 done | comparison report (labeled) present | `Add token-efficiency comparison report` |
| 12 | Original extension | **PLANNED** | one extension implemented | Stage 5 (+9) done | extension code + output + doc present | `Add centrality-based suspect ranking extension` |
| 13 | README/docs hardening | **PLANNED** | finalize docs | Stages 5–12 done | docs consistent with artifacts | `Harden README and documentation` |
| 14 | Quality gates + final audit | **PLANNED** | gates pass + audit | Stage 13 done | gates green + `final_audit.md` complete | `Run quality gates and final audit` |
| 15 | Moodle submission prep | **PLANNED** | wrapper PDF + submit | Stage 14 done | template PDF ready (outside repo if required) | _(no repo commit unless template required in-repo)_ |

---

## Stage 0 — Repository skeleton and requirements audit — **DONE**
- [x] Create repo structure + `.gitignore` / `.env.example` / `pyproject.toml`
- [x] `docs/REQUIREMENTS_AUDIT.md` (45 requirements)
- [x] `reports/repository_selection.md`, `reports/bug_validation.md`
- [x] Decisions D-001…D-006
**Validation:** `git show 3fc110d --stat` · **Evidence:** commit `3fc110d`, README, audit, selection/validation reports.
**Risks/blockers:** none (complete).

## Stage 1 — PRD — **DONE**
- [x] Full `docs/PRD.md` (30 sections; FR/NFR/AC)
- [x] GitHub-status reflected honestly
**Validation:** `git show 018c580 --stat` · **Evidence:** commit `018c580`, `docs/PRD.md`.
**Risks/blockers:** none.

## Stage 2 — Technical PLAN — **DONE**
- [x] Full `docs/PLAN.md` (30 sections; agent states; baseline vs graph-guided)
**Validation:** `git show 8a7ff9c --stat` · **Evidence:** commit `8a7ff9c`, `docs/PLAN.md`.
**Risks/blockers:** none.

## Stage 3 — TODO — **IN_PROGRESS**
- [x] Draft full stage-by-stage TODO (this file)
- [ ] Student review of TODO
- [ ] Commit TODO (`Write assignment 4 execution TODO`)
**Goal:** complete and review `docs/TODO.md`; **no implementation.**
**Validation:** `sed -n '1,320p' docs/TODO.md`; `git diff -- docs/TODO.md` · **Evidence (on commit):** TODO commit hash.
**Exit criteria:** TODO reviewed and committed → unlocks Stage 4 (R2).
**Risks/blockers:** none.

## Stage 4 — Target repository acquisition — **DONE** (commit `1299535`)
- [x] Fetch Luigi buggy commit `a0f1db01…` (temp clone) and verify `rev-parse HEAD` matches
- [x] Vendor source into `target_repo/luigi_buggy/` excluding `.git`/`.github`/caches; no nested `.git` (D-007)
- [x] Preserve upstream `LICENSE`; record provenance in `target_repo/README.md`
- [x] Verify file/LOC counts (measured: **244** py files / **58,636** LOC, full tree) and log in `reports/target_repository_acquisition.md`
- [x] Confirm vendored source is pristine/buggy (line 1118 `return literal_eval(x)`; fixed pattern absent) — **no fix applied**
- [x] Reconcile PLAN/TODO/README vendoring policy with D-007 (done this stage; vendored & tracked)
- [x] Reconcile `docs/PRD.md` and `docs/AI_WORKFLOW.md` with D-007 (no residual contradictions remain)
- [ ] (Later, Stage 10) overlay regression test from fixed commit `3a0bfbff…` for the fix proof
**Validation:** `test ! -d target_repo/luigi_buggy/.git`; `find target_repo/luigi_buggy -name '*.py' | wc -l`; grep buggy/fixed patterns; `git rev-parse` in temp clone.
**Evidence (Stage 4):** `target_repo/luigi_buggy/**` (vendored source), `target_repo/README.md` (provenance + policy), `reports/target_repository_acquisition.md` (method + validation), and `docs/DECISIONS.md` **D-007** (vendoring decision).
**Evidence status:** acquisition done, validated, reconciled in docs, and **committed** as `1299535 Acquire Luigi buggy target repository` (R1 satisfied — vendored tree now tracked).
**Risks/blockers:** none outstanding (policy reconciled via D-007); Docker needed for later test stages.

## Stage 5 — Graphify setup and first graph run — **PLANNED**
- [ ] Install/configure Graphify if needed (record steps; no global installs without note)
- [ ] Run Graphify on `target_repo/luigi_buggy/` (scope to core if needed; log exclusions)
- [ ] Collect `graph.json`, `GRAPH_REPORT.md`, and `graph.html` if generated → `artifacts/graphify/`
- [ ] Validate artifact presence + `graph.json` is valid JSON with node/edge counts
- [ ] Decide `graph.json` tracking (force-add vs reduced `graph.core.json`) — OD-5
- [ ] Document command + output in `artifacts/validation/graphify_run.log`
**Validation:** `python -c "import json;json.load(open('artifacts/graphify/graph.json'))"`; file existence checks.
**Artifacts:** `artifacts/graphify/*`, run log.
**Risks/blockers:** Graphify output format may differ → adapt `graph_io.py`; size/noise → scope + log.

## Stage 6 — Obsidian vault construction — **PLANNED**
- [ ] `index.md` navigation hub
- [ ] `hot.md` hubs/hotspots + defect path
- [ ] `macro-architecture.md`, `meso-subsystem-parameter.md`, `micro-tupleparameter-parse.md`
- [ ] `bug-3-root-cause.md`, `before-after.md`, `token-efficiency.md`, `graph-report.md`
- [ ] Link pages with `[[wiki-links]]`; ensure they resolve
- [ ] Ensure vault reads as active knowledge, not a file dump
**Validation:** check `[[links]]` resolve; `index.md` references ≥3 pages.
**Artifacts:** `obsidian/*.md`.
**Risks/blockers:** depends on Stage 5 graph data (metrics labeled `measured`).

## Stage 7 — Reverse engineering analysis — **PLANNED**
- [ ] Macro graph reading (subsystem map, biggest clusters)
- [ ] Meso subsystem analysis (`parameter` + `task`/`scheduler`/`worker`)
- [ ] Micro bug-path analysis (`TupleParameter.parse`, callers/callees, API→test path)
- [ ] Identify hubs / communities / God nodes-bottlenecks (with measured values)
- [ ] Document the parameter serialization path
- [ ] Block architecture diagram → `artifacts/diagrams/`
- [ ] OOP/class diagram (`Parameter`→`ListParameter`→`TupleParameter`) → `artifacts/diagrams/`
**Validation:** diagrams exist and embed in README; RE claims cite graph nodes.
**Artifacts:** `reports/bug_analysis.md` (partial), `artifacts/diagrams/*`, Obsidian micro/meso/macro pages.
**Risks/blockers:** graph granularity decision (OD-2).

## Stage 8 — Baseline naive investigation — **PLANNED**
- [ ] Define naive workflow (no graph/hot context)
- [ ] Count files / text units read
- [ ] Measure or estimate tokens (label provenance; state method if estimated)
- [ ] Count iterations / steps
- [ ] Record whether/when root cause is reached
- [ ] Save baseline report + raw logs
**Validation:** counters present in logs; report table populated with labels.
**Artifacts:** `artifacts/validation/baseline_*.log`, baseline section of `reports/token_efficiency.md`.
**Risks/blockers:** token-accounting fidelity (OD-3); baseline fairness (OD-4).

## Stage 9 — Graph-guided agent workflow — **PLANNED**
- [ ] Implement/configure LangGraph workflow (states per `docs/PLAN.md` §14)
- [ ] Enforce bounded steps + controlled context (no uncontrolled full-repo reads)
- [ ] Consult Graphify/Obsidian **before** raw code
- [ ] Record files / tokens / iterations (same counters as baseline)
- [ ] Save graph-guided report + raw logs
**Validation:** run completes within step cap; logs show graph-first ordering.
**Artifacts:** `src/ex04_graph_debugger/*`, `artifacts/validation/graph_guided_*.log`, report section.
**Risks/blockers:** requires local LLM key (agent stage only); confirm LangGraph vs CrewAI (OD-6).

## Stage 10 — Bug fix and before/after proof — **PLANNED**
- [ ] Run failing test **before** fix in Docker/Python 3.8 → capture `failing_before.log`
- [ ] Apply minimal fix in `TupleParameter.parse` (`except (ValueError, TypeError)`, `tuple(literal_eval(x))`)
- [ ] Run passing test **after** fix → capture `passing_after.log`
- [ ] Save patch/diff evidence (recorded diff text; raw tree not committed — R4)
- [ ] Document root cause in `reports/bug_analysis.md`
- [ ] Confirm no unrelated changes (diff confined to the function)
**Validation:** two logs present (fail then pass); diff shows only the target function.
**Artifacts:** `artifacts/validation/failing_before.log`, `passing_after.log`, `reports/before_after.md`.
**Risks/blockers:** Docker availability.

## Stage 11 — Token efficiency comparison — **PLANNED**
- [ ] Compare baseline vs graph-guided: files read, text units, iterations, tokens
- [ ] Add root-cause speed/quality (cheaper-but-wrong is not a win)
- [ ] Label every value `measured | estimated | manual count`
- [ ] Honest note if advantage is small/absent/context-dependent
**Validation:** comparison table complete with provenance labels; numbers traceable to logs.
**Artifacts:** `reports/token_efficiency.md`, `obsidian/token-efficiency.md`.
**Risks/blockers:** depends on Stages 8–9 logs.

## Stage 12 — Original extension — **PLANNED**
- [ ] Implement **centrality-based suspect ranking** (unless evidence favors another — OD-1)
- [ ] Document method + result; show how the defect neighborhood ranks
- [ ] Ensure extension supports assignment goals; avoid overengineering
**Validation:** extension runs and emits a ranked list artifact; described in README.
**Artifacts:** `src/ex04_graph_debugger/extensions/*`, ranking output, README section.
**Risks/blockers:** reuses `graph_io.py` (Stage 5 data).

## Stage 13 — README and documentation hardening — **PLANNED**
- [ ] Update README (usage, workflow, evidence, diagrams, root cause, fix, extension)
- [ ] Update `AI_WORKFLOW`, `PROMPTS`, `DECISIONS`, `COSTS`, `QUALITY`, `SUBMISSION_CHECKLIST`
- [ ] Ensure no contradictions with actual artifacts (status labels accurate)
**Validation:** cross-check README claims vs files; checklist ticked only against evidence.
**Artifacts:** updated `README.md`, `docs/*`.
**Risks/blockers:** none beyond upstream stages.

## Stage 14 — Quality gates and final audit — **PLANNED**
- [ ] `uv run pytest`
- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`
- [ ] line-count check (`src/**/*.py` ≤ 150)
- [ ] secret scan
- [ ] artifact scan (no raw target source / no oversized blobs)
- [ ] verify GitHub pushed + README/docs match repo
- [ ] verify no fake evidence; no self-score in repo
- [ ] verify no external submission PDF in repo unless required
**Validation:** all gate commands pass; `reports/final_audit.md` re-checks every mandatory requirement.
**Artifacts:** `reports/final_audit.md`, gate outputs.
**Risks/blockers:** any failing gate must be fixed, not suppressed.

## Stage 15 — Moodle submission preparation — **PLANNED**
- [ ] Prepare wrapper PDF from the **provided template only**, when ready
- [ ] Include GitHub link + group code `MaRs-777`
- [ ] Use required filename format (e.g., `MaRs-777-ex04.pdf` or the exact required format)
- [ ] No extra text outside the template
- [ ] Submit individually on Moodle
**Validation:** filename + contents match the template/spec; link resolves.
**Artifacts:** wrapper PDF (kept outside the repo unless the spec requires it in-repo).
**Risks/blockers:** confirm exact required filename/format before generating.

---

## Open decisions referenced (from PLAN §29)
- OD-1 extension choice · OD-2 graph granularity/scope · OD-3 token fidelity · OD-4 baseline fairness · OD-5 `graph.json` tracking · OD-6 LangGraph vs CrewAI.

## Reminder
_No implementation, clone, Graphify run, agent, or fix is started in this TODO stage. Stages 4+ begin only after PRD/PLAN/TODO are committed (R2)._
