# TODO — Stage-by-Stage Execution Checklist

**Project:** Agentic, graph-guided debugging of a real Python bug — Assignment 04 (group `MaRs-777`)
**Repository:** `ai-agentic-graph-debugging-assignment4` · branch `main`
**Document status:** TODO stage (Stage 3, IN_PROGRESS). This list operationalizes `docs/PRD.md` and
`docs/PLAN.md`. It does **not** implement anything.

## 1. Project status summary
- **Done & committed:** Stage 0 skeleton + requirements audit (`3fc110d`), Stage 1 PRD (`018c580`), Stage 2 PLAN (`8a7ff9c`), Stage 3 TODO (`485f3b5`).
- **Done & committed:** Stage 4 — target repository acquisition (Luigi source vendored to `target_repo/luigi_buggy/`, validated) — commit `1299535`.
- **Done & committed:** Stage 5 — Graphify run with the official `graphifyy` tool (no LLM key). Real artifacts in `artifacts/graphify/` (`graph.json` 6,771 nodes / 15,365 edges, `GRAPH_REPORT.md`, `GRAPH_TREE.html`) — commit `feb78ea`.
- **Done & committed:** Stage 6 — Obsidian vault under `obsidian/` (9 required + 2 optional pages, grounded in real Graphify artifacts) — commit `6cdfd2f`.
- **Done & committed:** Stage 7 — Reverse engineering analysis: report + 3 Mermaid diagrams + Obsidian analysis page (macro/meso/micro, evidence-tagged) — commit `8991916`.
- **Done & committed:** Stage 8 — Baseline naive investigation (controlled, no graph/agent): 4 files / ~24,482 est. tokens (chars/4) / 5 rounds, root cause reached — commit `8904b57`.
- **Done & committed:** Stage 9 — Graph-guided agent (LangGraph, deterministic/no-LLM): 5 files / ~3,631 est. tokens / 8 states, root cause reached; 6 tests pass, ruff clean — commit `3b0e3c0`.
- **Next up:** Stage 10 — Bug fix and before/after proof (PLANNED).
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
| 5 | Graphify first run | **DONE** (`feb78ea`) | build code graph | Stage 4 done | `graph.json` + `GRAPH_REPORT.md` present + run logged | `Run Graphify on Luigi target repository` |
| 6 | Obsidian vault | **DONE** (`6cdfd2f`) | active knowledge vault | Stage 5 done | linked vault (index/hot + pages) resolves | `Build Obsidian knowledge vault` |
| 7 | Reverse engineering | **DONE** (`8991916`) | macro/meso/micro + diagrams | Stage 5–6 done | RE notes + block + OOP diagrams present | `Analyze Luigi architecture and bug path` |
| 8 | Baseline naive run | **DONE** (`8904b57`) | uninformed investigation metrics | Stage 4 done | baseline report + logs present | `Measure naive baseline investigation` |
| 9 | Graph-guided agent | **DONE** (`3b0e3c0`) | LangGraph graph-guided run | Stage 5–6 done | graph-guided report + logs present | `Implement graph-guided agent workflow` |
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

## Stage 5 — Graphify setup and first graph run — **DONE** (commit `feb78ea`)
- [x] Resolve the "graphify not found" blocker — official PyPI package is **`graphifyy`**; install via `uv tool install graphifyy` (Graphify 0.8.39) — **D-008**
- [x] Build the graph **without an LLM key** (code-only corpus): `graphify update … --no-cluster`, then `graphify cluster-only … --no-label`, then `graphify tree …`
- [x] Collect artifacts → `artifacts/graphify/`: `graph.json`, `GRAPH_REPORT.md`, `GRAPH_TREE.html`, metadata, `manifest.json`, run log
- [x] Validate `graph.json`: valid JSON, **6,771 nodes / 15,365 edges** (token cost 0); `TupleParameter` node present
- [x] Keep vendored source pristine (removed in-tree `graphify-out/` incl. cache) — verified 0 changes
- [x] Resolve OD-5: **track full `graph.json`** via `git add -f` at commit (past `artifacts/graphify/*.json` ignore) — D-008
- [x] Commit Stage 5 artifacts — commit `feb78ea Run Graphify on Luigi target repository` (Stage 5 DONE)
**Validation:** `python -c "import json;json.load(open('artifacts/graphify/graph.json'))"` → valid; `GRAPH_REPORT.md` present; `GRAPH_TREE.html` present.
**Artifacts:** `artifacts/graphify/{graph.json, GRAPH_REPORT.md, GRAPH_TREE.html, .graphify_labels.json, .graphify_root, manifest.json, graphify_run.log}`; report `reports/graphify_run.md`.
**Risks/blockers:** none outstanding. Note: standard `graph.html` viz skipped (>5000 nodes) → used `GRAPH_TREE.html` instead; `GRAPH_REPORT.md` reports 6,705/13,222 after dedup vs graph.json 6,771/15,365 (both real; documented in `reports/graphify_run.md` §9).

## Stage 6 — Obsidian vault construction — **DONE** (commit `6cdfd2f`)
- [x] `index.md` navigation hub (reading order: graphify → architecture → communities → parameter → hot)
- [x] `hot.md` bug context (`TupleParameter.parse`, node `luigi_parameter_tupleparameter`, L1066/L1095)
- [x] `graphify-overview.md`, `architecture-map.md`, `parameter-subsystem.md`, `graph-communities.md`
- [x] `bug-investigation-seed.md`, `token-efficiency-plan.md`, `README.md` (+ optional `sources.md`, `open-questions.md`)
- [x] Link pages with `[[wiki-links]]`; ground every claim in `graph.json`/`GRAPH_REPORT.md`/source (else label *planned*)
- [x] Report `reports/obsidian_vault.md`; design decision **D-009**
- [x] Commit Stage 6 vault — commit `6cdfd2f Build Obsidian knowledge vault` (Stage 6 DONE)
**Validation:** 9 required pages + 2 optional present; `[[wiki-links]]` resolve; `index.md` references ≥3 pages; no Luigi/Graphify-artifact edits.
**Artifacts:** `obsidian/*.md`, `reports/obsidian_vault.md`.
**Risks/blockers:** none — community names are placeholders (no LLM); real naming/hub ranking deferred to Stage 7 (labeled).

## Stage 7 — Reverse engineering analysis — **DONE** (commit `8991916`)
- [x] Macro graph reading (node counts + degree hubs; God-node caveat = vendored d3 JS)
- [x] Meso subsystem analysis (`Parameter`→`ListParameter`→`TupleParameter`, `DictParameter`)
- [x] Micro bug-path analysis (`TupleParameter.parse` L1095; serialize/parse asymmetry; `TypeError`)
- [x] Identify hubs / communities with measured degree (scheduler deg≈137; Community 1 / 58)
- [x] Document the parameter serialization path (inherited `json.dumps` vs overridden `parse`)
- [x] Block architecture diagram → `artifacts/diagrams/architecture_block.mmd`
- [x] OOP/class diagram → `artifacts/diagrams/oop_parameter_diagram.mmd` (+ `bug_path.mmd`)
- [x] Report `reports/reverse_engineering.md`; Obsidian `reverse-engineering-analysis.md` + cross-links; decision D-010
- [x] Commit Stage 7 — commit `8991916 Analyze Luigi architecture and bug path` (Stage 7 DONE); embed diagrams in README deferred to Stage 13 polish
**Validation:** 3 `.mmd` diagrams + RE report + Obsidian page present; RE claims tagged EXTRACTED/INFERRED/interpretation; no Luigi/Graphify-artifact edits.
**Artifacts:** `reports/reverse_engineering.md`, `artifacts/diagrams/*.mmd`, `obsidian/reverse-engineering-analysis.md` (+ updated pages).
**Risks/blockers:** community naming + formal centrality ranking still open (no LLM) — tracked in `obsidian/open-questions.md`.

## Stage 8 — Baseline naive investigation — **DONE** (commit `8904b57`)
- [x] Define naive protocol (raw source only; NO Graphify/Obsidian/agent) — controlled, honest baseline
- [x] Count files / text units read (4 full files)
- [x] Estimate tokens via `characters/4` (labeled estimate, **D-011**) — 97,926 chars → ~24,482 est. tokens
- [x] Count investigation rounds (5)
- [x] Record root cause reached (yes — only after reading full `parameter.py` + base classes + test file)
- [x] Save report + machine-readable metrics + trace + files-read list
- [x] Commit Stage 8 — commit `8904b57 Measure naive baseline investigation` (Stage 8 DONE)
**Validation:** `baseline_naive_metrics.json` valid (graphify/obsidian/agent/fix = false); report tables labeled estimate.
**Artifacts:** `reports/baseline_naive_investigation.md`, `artifacts/validation/baseline_naive_{metrics.json,trace.log,files_read.txt}`.
**Risks/blockers:** token estimate is coarse (OD-3); baseline is protocol-defined, not an empirical average (OD-4) — both stated in the report's Limitations.

## Stage 9 — Graph-guided agent workflow — **DONE** (commit `3b0e3c0`)
- [x] Implement LangGraph workflow — 8 bounded states (`metrics`, `source_reader`, `agent_state`, `nodes`, `graph_guided_agent`; all ≤150 lines) — confirms LangGraph over CrewAI (OD-6 / D-012)
- [x] Enforce bounded steps + controlled context (graph sub-graph + 3 Obsidian pages + 3 targeted source ranges; NO full-file read)
- [x] Consult Graphify/Obsidian **before** raw code (trace shows graph-first ordering)
- [x] Record files/tokens/rounds (same `chars/4` method as baseline): 5 files / 7 units / 14,523 chars / **3,631 est. tokens** / 8 rounds
- [x] **Deterministic, no-LLM** workflow → `llm_used:false`, `api_cost_usd:0` (no API key needed — D-012)
- [x] Save report + metrics + trace + files-read; add unit tests (6 pass); ruff clean
- [x] Commit Stage 9 — commit `3b0e3c0 Implement graph-guided agent workflow` (Stage 9 DONE)
**Validation:** `graph_guided_agent_metrics.json` flags graphify/obsidian/agent=true, bug_fix=false; `uv run pytest` (6 pass); `uv run ruff check .` / `format --check` clean.
**Artifacts:** `src/ex04_graph_debugger/{metrics,source_reader,agent_state,nodes,graph_guided_agent}.py`, `tests/unit/test_graph_guided_agent.py`, `reports/graph_guided_agent.md`, `artifacts/validation/graph_guided_agent_{metrics.json,trace.log,files_read.txt}`.
**Risks/blockers:** none — no API key required (deterministic). Final baseline-vs-graph comparison reserved for Stage 11 (not claimed here).

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
