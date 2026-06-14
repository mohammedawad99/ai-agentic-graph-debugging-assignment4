# PLAN — Implementation & Architecture Plan

**Project:** Agentic, graph-guided debugging of a real Python bug
**Repository:** `ai-agentic-graph-debugging-assignment4` (group `MaRs-777`)
**Course:** Agentic Software Engineering / Vibe Coding — Assignment 04
**Document status:** PLAN stage. The final repo currently contains **skeleton + PRD + this PLAN only**.
Luigi is not cloned, Graphify has not run, the agent is not built, and the fix is not applied.
This document translates `docs/PRD.md` into an implementation strategy; it does **not** implement anything.

---

## 1. Plan overview
This plan turns the PRD into a concrete, staged build: vendor the target (Luigi at the buggy commit) into
the tracked `target_repo/luigi_buggy/` (kept pristine; **D-007**), generate a Graphify code graph, document it as an Obsidian vault, then run a
LangGraph agent in two modes — **baseline naive** and **graph-guided** — on the same bug, measure their
cost, apply a minimal real fix with before/after proof, and report a token-efficiency comparison plus one
original extension. Every stage produces in-repo, reproducible evidence with provenance labels.

## 2. Current status and boundaries
- **Done:** repo skeleton, `docs/REQUIREMENTS_AUDIT.md`, `docs/PRD.md` (committed `018c580`), GitHub repo pushed (`main`).
- **Confirmed:** target = Luigi bug 3 (BugsInPy); buggy commit `a0f1db01…`; fail→pass validated in a **temporary candidate repo** under Docker/Python 3.8.20.
- **Not done (planned):** Luigi import into this repo, Graphify run, Obsidian analysis, agent, diagrams, fix, token report, extension, final audit.
- **Boundary:** this stage writes PLAN only — no code, no clone, no Graphify, no agent, no fix, no commit.

## 3. Architecture principles
1. **Graph-before-code:** navigation decisions come from the graph first; raw files are read only when justified.
2. **Bounded & measurable:** every agent run has a step cap and emits counters (files read, iterations, tokens).
3. **Determinism where possible:** target tests run in a pinned Docker/Python 3.8 image for reproducibility.
4. **Separation of concerns:** target source (third-party) is isolated from our code, artifacts, and docs.
5. **Small modules:** our Python files stay ≤150 lines; logic is split into focused modules.
6. **Honesty by construction:** numbers carry `measured | estimated | manual` labels; nothing is claimed before its artifact exists.
7. **Idempotent stages:** re-running a stage reproduces its artifacts without manual cleanup surprises.

## 4. Repository structure plan
```
src/ex04_graph_debugger/
  config.py            # load config/default.toml + .env (no secrets in repo)
  graph_io.py          # load/normalize graph.json; node/edge/centrality queries
  metrics.py           # counters: files/text-units read, iterations, tokens (+provenance labels)
  workflow_baseline.py # naive mode driver
  workflow_graph.py    # graph-guided mode driver (LangGraph)
  agent_states.py      # state/node definitions for the LangGraph graph
  patcher.py           # apply/revert minimal patch in the target working area
  docker_runner.py     # build the docker command to run the Luigi regression test
  reporting.py         # assemble reports/*.md tables from metrics
  extensions/          # the chosen original extension (one module)
scripts/
  check_line_limit.py  # 150-line gate
  secret_scan.py       # secret gate
tests/
  unit/                # unit tests for our modules
  integration/         # end-to-end (mocked LLM) workflow tests
```
Each module is single-purpose to respect the 150-line rule. No module imports the target source directly;
the target is accessed only as files on disk and via the Docker test runner.

## 5. Data / artifact flow
```
Luigi@buggy ──vendor──> target_repo/luigi_buggy/ (tracked, pristine; .git excluded)
        │
        ├─ Graphify ──> artifacts/graphify/graph.json ──> GRAPH_REPORT.md (+ graph.html?)
        │                                   │
        │                                   ├─> obsidian/ (index.md, hot.md, analysis pages)
        │                                   └─> graph_io.py (agent reads here)
        │
        ├─ workflow_baseline ─┐
        ├─ workflow_graph ────┤── metrics.py ──> reports/token_efficiency.md
        │                     └── logs ───────> artifacts/validation/
        │
        └─ patcher + docker_runner ──> failing-before / passing-after logs ──> reports/before_after.md
```

## 6. Target-repo acquisition plan
- **Where:** `target_repo/luigi_buggy/` — **vendored and tracked** in this repo (approved policy, **D-007**),
  kept **pristine** at the verified buggy commit. Upstream `.git`/`.github` are **excluded** (no nested repo);
  upstream `LICENSE`/provenance are **preserved**. No bug fix is applied during acquisition.
- **How:** shallow-fetch the exact buggy commit into a **temporary** working area, mirroring the validated procedure:
  `git init` → add origin `spotify/luigi` → `git fetch --depth 1 origin a0f1db01…` → `git checkout FETCH_HEAD`,
  then copy the checked-out tree into `target_repo/luigi_buggy/` excluding `.git`/`.github`/caches/build outputs.
- **Regression test overlay:** the target test ships with the **fixed** commit (`3a0bfbff…`), so overlay
  `test/parameter_test.py` from the fixed commit onto the buggy source — exactly as BugsInPy does — and
  record this as an intentional, documented overlay (proof: class absent at buggy, present at fixed).
- **Provenance:** record commit IDs, upstream URL, and overlay note in `target_repo/README.md` and `config/default.toml`.

## 7. Docker / Python 3.8 validation plan
- **Image:** `python:3.8-slim` (in-container Python 3.8.20), invoked via the available native docker
  (`sg docker -c …` if the user is not in the docker group).
- **Install (minimal):** `pip install -e . --no-deps` then `tornado<5 python-dateutil==2.7.5 mock psutil pytest`.
- **Test command (category):**
  `docker run --rm -v "$PWD":/work -w /work python:3.8-slim bash -lc "<install> && pytest -q <target test>"`.
- **Logs:** captured to `artifacts/validation/` (e.g., `failing_before.log`, `passing_after.log`).
- **Rationale:** Luigi 2.8.3 uses `from collections import Mapping` (removed in 3.10) → must run on 3.8 (D-005).

## 8. Graphify execution plan
- **Input:** `target_repo/luigi_buggy/` (focus on core: `luigi/` package; note any `contrib/` exclusions).
- **Run:** execute Graphify per its documented CLI/usage; capture stdout/stderr to `artifacts/validation/graphify_run.log`.
- **Scope control:** if the full repo is too large/noisy, scope to the core subsystem (`parameter`, `task`, `scheduler`, `worker`) and **log what was excluded** (no silent truncation).
- **Output target:** `artifacts/graphify/` (see §9). Re-runs overwrite deterministically.
- **Reading:** translate graph into observations (hubs, communities, paths) used by Obsidian and the agent.

## 9. Graphify artifact management
| Artifact | Path | Tracked? | Notes |
|----------|------|----------|-------|
| `graph.json` | `artifacts/graphify/graph.json` | curated (see note) | machine-readable nodes/edges; `.gitignore` currently ignores `artifacts/graphify/*.json` — will **force-add** the final curated graph or store a compressed/curated copy so graders can access it |
| `GRAPH_REPORT.md` | `artifacts/graphify/GRAPH_REPORT.md` | yes | human summary: counts, hubs, communities, bottlenecks |
| `graph.html` (if generated) | `artifacts/graphify/graph.html` | yes if small | interactive view; otherwise note "not generated" |
| run log | `artifacts/validation/graphify_run.log` | yes | provenance of the run |

> Decision to resolve in the Graphify stage: keep `graph.json` tracked (force-add) vs. ship a reduced
> `graph.core.json`. Either way the graders must be able to see the graph evidence (AC-01).

## 10. Obsidian vault plan
Pages (linked via `[[wiki-links]]`, navigable from `index.md`):
- `index.md` — navigation hub (macro→meso→micro, reports).
- `hot.md` — hubs/hotspots + the bug's focused context (the defect path).
- `macro-architecture.md` — subsystem map of Luigi.
- `meso-subsystem-parameter.md` — the `parameter` subsystem and neighbors.
- `micro-tupleparameter-parse.md` — the defect site, callers/callees.
- `bug-3-root-cause.md` — root-cause narrative (mirrors `reports/bug_analysis.md`).
- `before-after.md` — fail→pass evidence summary (mirrors `reports/before_after.md`).
- `token-efficiency.md` — comparison summary (mirrors `reports/token_efficiency.md`).
- `graph-report.md` — readable mirror/links to `GRAPH_REPORT.md`.
All metrics on these pages are labeled by provenance; pages are written to be read, not dumped.

## 11. Reverse engineering plan
- **Macro:** whole-system shape — packages/subsystems and coarse dependencies; identify the biggest clusters.
- **Meso:** zoom into the `parameter` subsystem (+ `task`, `scheduler`, `worker`); how parameters attach to tasks.
- **Micro:** `TupleParameter.parse` → its inheritance (`ListParameter`→`Parameter`), callers/callees, and the path from `luigi.TupleParameter` public API to the failing test.
- **Hubs:** rank nodes by degree/centrality from `graph.json`; justify with measured values.
- **Communities:** detect clusters (core vs `contrib`); locate where the bug sits.
- **God nodes / bottlenecks:** flag oversized/over-connected nodes (e.g., `task.py`/`scheduler.py` candidates) as risk concentrators.
- **Traceability:** maintain a chain requirement → graph node → source location → test, surfaced in `hot.md` and the audit.

## 12. Diagram plan
- **Architecture block diagram** — subsystem boxes and data/control flow (Mermaid or drawn), in `artifacts/diagrams/` and embedded in README.
- **OOP / class diagram** — `Parameter` → `ListParameter` → `TupleParameter` (and related types), key methods incl. `parse`/`serialize`.
- **Bug-path diagram** — API → `serialize` → `parse` → `json.loads`/`literal_eval` → test, marking where the `TypeError` escapes.
- **Before/after evidence diagram (if useful)** — compact visual of fail→pass.
Diagrams are generated/authored artifacts (no fabricated screenshots); source kept where practical.

## 13. Agent architecture
- **Framework:** **LangGraph preferred** (D-004). Reason: the assignment's thesis is a **bounded,
  measurable, graph-structured** investigation. LangGraph models the workflow as an explicit **state graph**
  with discrete nodes and transitions, which (a) maps cleanly to "graph-before-code" stages, (b) makes
  **step caps and stopping conditions** first-class, and (c) makes per-node **metrics capture** (files read,
  tokens, iterations) straightforward. CrewAI's role/agent abstraction is more about multi-agent
  collaboration than a controlled, instrumented single pipeline; we adopt it only if a thin prototype shows
  a concrete advantage.
- **Inputs:** `graph.json`, `obsidian/index.md`, `obsidian/hot.md`, target file list, the regression test id.
- **Outputs:** candidate root cause, proposed minimal patch, before/after test results, a metrics record.
- **Stopping conditions:** regression test passes after patch; OR step cap reached; OR no further graph-justified file to read.
- **Guardrails:** controlled context (only justified files), bounded steps, no uncontrolled full-repo reads,
  no network beyond the LLM call, patch limited to the defect function, all actions logged.

## 14. Agent workflow states (planned LangGraph nodes)
1. `load_graph_artifacts` — load `graph.json` + centrality/hubs.
2. `read_index` — read `obsidian/index.md` for orientation.
3. `read_hot_context` — read `hot.md` (defect path, hubs).
4. `select_relevant_files` — choose a minimal, justified file set from the graph.
5. `inspect_bug_path` — read only those files around `TupleParameter.parse`.
6. `propose_root_cause` — articulate why the defect occurs.
7. `verify_with_test` — run failing-before in Docker to confirm the symptom.
8. `propose_patch` — minimal change confined to the function.
9. `run_after_test` — run passing-after in Docker.
10. `write_report` — emit metrics + narrative to `reports/`.
Transitions include a bounded retry loop (`select_relevant_files`↔`inspect_bug_path`) capped by step budget.

## 15. Baseline naive workflow plan
- **Behavior:** no graph/hot context; explores the target by walking files (e.g., directory order or broad reads).
- **Reads:** potentially many files/text units across `luigi/`; this is the point — it is uninformed.
- **Token accounting:** prefer **measured** provider token usage; if unavailable, **estimated** via a documented tokenizer/heuristic (e.g., chars/4) — labeled as such.
- **Iteration counting:** one iteration per agent step / LLM call; counter in `metrics.py`.
- **Fairness:** same model, same success criterion (regression test passes), same step-cap ceiling so the comparison is honest (OQ-4).

## 16. Graph-guided workflow plan
- **Behavior:** starts from `graph.json` + `index.md` + `hot.md`; uses hubs/paths to jump near the defect.
- **Reads:** a small, justified subset of files (ideally `parameter.py` and immediate neighbors).
- **Tracking:** same counters as baseline (files/text units, iterations, tokens), same provenance labels.
- **Expectation (to verify, not assume):** fewer files read and fewer iterations than baseline, reaching the same fix.

## 17. Token-efficiency measurement plan
Comparison table in `reports/token_efficiency.md`:
| Metric | Baseline | Graph-guided | Provenance |
|--------|----------|--------------|------------|
| Total tokens (prompt+completion) | … | … | measured/estimated |
| Files / text units read | … | … | measured |
| Iterations / steps | … | … | measured |
| Reached correct fix? | … | … | observed |
| Steps to root cause | … | … | measured |
- **Labels mandatory** (`measured | estimated | manual count`).
- **Outcome quality** recorded alongside cost (cheaper-but-wrong is not a win).
- **Root-cause speed** = steps/iterations until `propose_root_cause` is correct.
- Raw logs under `artifacts/validation/`; honest reporting if the advantage is small or absent.

## 18. Bug fix plan
- **Failing-before:** capture target test failing on buggy source (`TypeError: 'int' object is not iterable`).
- **Minimal patch (known):** in `TupleParameter.parse` — `except (ValueError, TypeError):` and `return tuple(literal_eval(x))`; confined to that function.
- **Passing-after:** same test passes post-patch.
- **Validation clean-state policy:** during measurement/validation, run the test in Docker, apply the patch to a working copy, then restore so the vendored tree returns pristine; remove build/cache artifacts.
- **Vendored-source policy (D-007):** `target_repo/luigi_buggy/` is **kept pristine at the buggy commit** through acquisition and analysis. **Source changes are allowed only in the later bug-fix stage (Stage 10).** The fix and its before/after logs are captured as **evidence** (`reports/before_after.md`, `artifacts/validation/`, plus the diff text); the demonstrated fix is recorded as a diff/logs, so the analyzed source stays the exact buggy version unless/until the bug-fix stage deliberately applies it.

## 19. Testing plan
- **Our project tests (`tests/`):** unit tests for `graph_io`, `metrics`, `patcher`, `config`; integration test for the workflows with a **mocked LLM** (deterministic, no API needed).
- **Luigi regression test:** `test/parameter_test.py::TestSerializeTupleParameter::testSerialize` under Docker/3.8.
- **Docker test commands:** as in §7; logged to `artifacts/validation/`.
- **Smoke tests:** graph loads; config parses; docker runner builds a valid command string.
- **Error-path tests:** malformed/empty `graph.json`; missing target file; patch-guard failure (target text not found) must raise, not silently pass.

## 20. Quality gates
| Gate | Command (planned) | Pass condition |
|------|-------------------|----------------|
| Tests | `uv run pytest` | all pass |
| Lint | `uv run ruff check .` | no errors |
| Format | `uv run ruff format --check .` | no diffs |
| Line limit | `uv run python scripts/check_line_limit.py` | every `src/**/*.py` ≤ 150 lines |
| Secret scan | `uv run python scripts/secret_scan.py` | no secrets in tracked files |
| Artifact scan | manual/script | only the intended vendored source (`target_repo/luigi_buggy/`, no nested `.git`) is tracked; no oversized/generated blobs committed |
| README/docs consistency | review + checklist | claims match repo reality |
Gates run before any submission commit and again in the final audit.

## 21. Configuration plan
- **`config/default.toml`** holds: target metadata (project, bug id, buggy/fixed commits, file/symbol, regression test), validation metadata (Python 3.8.20, image), Graphify output paths, agent framework + token-accounting mode.
- **Token budget metadata:** add a `[agent] step_cap` and an optional `[agent] token_budget` (informational ceiling) so runs are bounded and comparable.
- **Overrides:** `.env` (git-ignored) for the LLM key/model; `config.py` merges TOML + env.

## 22. Security plan
- No secrets in tracked files; only `.env.example` with empty placeholders is committed.
- `.env`, `*.key`, `*.pem` are git-ignored; a secret-scan gate runs before submission.
- No paid API is required by default; an LLM key is needed **only** in the agent stage and stays local.
- The vendored Luigi source (`target_repo/luigi_buggy/`, Apache-2.0, LICENSE preserved) is tracked deliberately (D-007); large generated artifacts are git-ignored or curated.

## 23. Evidence and provenance plan
- **Logs →** `artifacts/validation/` (test logs, graphify run log, workflow logs).
- **Reports →** `reports/` (selection, validation, bug_analysis, token_efficiency, before_after, final_audit).
- **Planned vs actual:** status labels in `docs/REQUIREMENTS_AUDIT.md` and headers; only in-repo artifacts are "done".
- **Measured vs estimated vs manual:** every number labeled; estimation method stated.
- **No fake evidence:** all logs/diagrams reproducible from documented commands; no fabricated screenshots.

## 24. Documentation plan
- **README.md** — context, target, validation summary, workflow, root cause, fix, diagrams, extension, honesty policy (kept current each stage).
- **`docs/AI_WORKFLOW.md`** — AI usage per stage + review-before-commit (exists).
- **`docs/PROMPTS.md`** — paraphrased per-stage prompt summaries (append P-05+ as stages run).
- **`docs/DECISIONS.md`** — append new decisions (e.g., extension choice, graph.json tracking).
- **`docs/COSTS.md`** — provenance rule + final token/cost numbers.
- **`docs/QUALITY.md`** — gates (exists; add the two checker scripts when built).
- **`docs/SUBMISSION_CHECKLIST.md`** — ticked only against real evidence.

## 25. Original extension plan
Candidates (2–3 considered; **one required** for final implementation):
1. **Centrality-based suspect ranking** *(required candidate — primary choice)* — rank functions/classes by graph centrality, output a ranked "suspect list", and show how high `TupleParameter.parse` (or its neighborhood) ranks vs. the actual defect. Directly reinforces the graph-guided thesis and reuses `graph_io.py`.
2. **Impact report for the serialization path** *(secondary)* — compute what depends on `TupleParameter.parse`/`serialize` (blast radius) from the graph.
3. **Traceability path report** *(secondary)* — automated path from public API → defect → regression test.
> **Decision pending (OQ-2):** default to **#1 centrality-based suspect ranking** as the required extension;
> confirm during the agent stage. Only the required one must be implemented and evidenced; others remain optional.

## 26. Risk management
| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Docker engine unavailable / WSL integration off | medium | document start steps; native docker via `sg docker`; validated already |
| Graphify install/output differs from expectation | medium | pin/record install steps; log run; adapt parser in `graph_io.py`; fall back to a documented scope |
| Target repo size/noise (~27.6k LOC) | medium | scope to core subsystem; log exclusions; no silent truncation |
| Token measurement inaccuracy | medium | prefer measured usage; else labeled estimate with stated method |
| Overclaiming completed stages | low | status labels + evidence policy + final audit |
| Old Python (3.8) dependency friction | medium | isolate in Docker; minimal pinned deps (tornado<5, dateutil, mock, psutil, pytest) |
| `graph.json` excluded by `.gitignore` | low | force-add curated graph or ship reduced `graph.core.json` (§9) |

## 27. Milestones
| Stage | Name | Output | Status |
|------:|------|--------|--------|
| 0 | Skeleton | repo structure + audit | done |
| 1 | PRD | `docs/PRD.md` | done (`018c580`) |
| 2 | PLAN | `docs/PLAN.md` | this stage |
| 3 | TODO | `docs/TODO.md` task list | planned |
| 4 | Target import | `target_repo/luigi_buggy/` (vendored, pristine; D-007) | in progress (acquired; commit pending) |
| 5 | Graphify | `graph.json`, `GRAPH_REPORT.md` | planned |
| 6 | Obsidian | vault pages | planned |
| 7 | Baseline | naive run + metrics | planned |
| 8 | Graph-guided agent | LangGraph run + metrics | planned |
| 9 | Fix | minimal patch + before/after | planned |
| 10 | Reports | token-efficiency, bug analysis, diagrams | planned |
| 11 | Final audit | `reports/final_audit.md` | planned |

## 28. Definition of done for the PLAN stage
- `docs/PLAN.md` covers all required sections (architecture, artifact flow, agent states, baseline vs graph-guided, measurement, fix, testing, gates, config, security, evidence, extension, risks, milestones).
- The plan is consistent with `docs/PRD.md` and `docs/REQUIREMENTS_AUDIT.md` (no contradictions).
- The preferred agent framework (LangGraph) and the required extension candidate are stated, with open decisions flagged.
- No implementation, clone, Graphify run, agent, or fix performed; no commit in this stage.

## 29. Open decisions
- **OD-1 (OQ-2):** confirm centrality-based suspect ranking as the required extension.
- **OD-2 (OQ-1/OQ-5):** Graphify granularity (function vs module) and how much `contrib/` to include.
- **OD-3 (OQ-3):** token accounting fidelity — exact provider usage vs documented estimate.
- **OD-4 (OQ-4):** exact baseline constraints to keep it a fair (non-strawman) comparison.
- **OD-5 (§9):** track full `graph.json` (force-add) vs ship reduced `graph.core.json`.
- **OD-6 (D-004):** final LangGraph vs CrewAI confirmation after a thin prototype.

## 30. Explicit non-goals
- Not fixing any Luigi bug other than bug 3; not refactoring Luigi.
- Not committing raw Luigi source or large generated blobs.
- Not upgrading Luigi to modern Python; not modifying upstream beyond the minimal patch.
- Not building a multi-agent system if a single bounded pipeline suffices.
- Not claiming "production-ready"; not self-scoring; not claiming any stage before its evidence exists.
