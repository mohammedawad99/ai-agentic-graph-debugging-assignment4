# Decisions Log — Assignment 04 (MaRs-777)

Architecture/strategy decisions. Each entry: context → decision → consequence. Dates are absolute.

## D-001 — Select Luigi bug 3 as the final target
**Date:** 2026-06-14
**Context:** Need a real, reproducible Python bug in a codebase large/rich enough for a grade-100 interpretation, but still manageable.
**Decision:** Use **Luigi, bug 3** from **BugsInPy** — defect in `TupleParameter.parse` (`luigi/parameter.py`), regression test `test/parameter_test.py::TestSerializeTupleParameter::testSerialize`, buggy commit `a0f1db01…`.
**Consequence:** ~96 source files / ~27.6k LOC at the buggy commit; clean one-function logic bug; strong DAG/Graphify story. Requires Python 3.8 (see D-005).

## D-002 — Reject PySnooper as too small for the grade-100 interpretation
**Date:** 2026-06-14
**Context:** PySnooper bug 3 was the first pick — clean and the only bug reproducible directly on Python 3.12.
**Decision:** Reject as the *final* target (keep only as an emergency safety net).
**Consequence:** PySnooper is ~5 source files / ~700 LOC — far below the Moodle "significant, ~10k+ LOC, ~70+ files" bar for an excellent submission.

## D-003 — Reject Tornado as the fallback (weaker non-test source file count)
**Date:** 2026-06-14
**Context:** Tornado bug 9 scored highest on setup safety (zero third-party deps) and bug cleanliness, and its bug logic was verified.
**Decision:** Keep Tornado as a strong fallback but not the primary, because its **non-test source file count (~34)** is weaker against the "≥70 files" reading; Luigi satisfies both LOC and file-count criteria.
**Consequence:** If Luigi later proves unworkable, switch to Tornado bug 9 (`url_concat` None-handling).

## D-004 — Prefer LangGraph for the agent workflow (unless evidence later favors CrewAI)
**Date:** 2026-06-14
**Context:** Assignment allows LangGraph or CrewAI.
**Decision:** Default to **LangGraph** for explicit graph-structured control flow that mirrors the graph-guided thesis; revisit only if implementation evidence favors CrewAI.
**Consequence:** Agent deps are added in the agent stage; `config/default.toml` defaults `agent.framework = "langgraph"`.

## D-005 — Use Docker / Python 3.8 for faithful BugsInPy validation and tests
**Date:** 2026-06-14
**Context:** Luigi 2.8.3 (buggy commit) uses `from collections import Mapping`, which fails to import on the host's Python 3.12.
**Decision:** Run all faithful validation/tests in **Docker `python:3.8-slim` (Python 3.8.20)**.
**Consequence:** Reproducible fail→pass already shown in the candidate repo (`reports/bug_validation.md`). Final-repo runs will use the same image.

## D-006 — No implementation before PRD / PLAN / TODO approval
**Date:** 2026-06-14
**Context:** Course process emphasizes planning and review before coding.
**Decision:** This repository stays at **skeleton + requirements audit**; no agent code, no Graphify run, no bug fix until `docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md` are written and approved.
**Consequence:** `src/` and `tests/` carry placeholders only; status labels in the audit reflect this.

## D-007 — Vendor the buggy Luigi source into the repo (supersedes the "git-ignore raw source" note)
**Date:** 2026-06-14
**Context:** Stage 4 acquisition. The earlier PLAN (§6/§18, rule R4) proposed keeping the raw Luigi source
git-ignored under `target_repo/luigi/` and never committing it. For reproducibility (graders and Graphify
should read the exact target without re-cloning) the source is instead **vendored** into the tracked path
`target_repo/luigi_buggy/`.
**Alternatives considered:**
- **(A) Git-ignored scripted clone** — keep an acquisition script + commit metadata; graders re-clone the
  buggy commit themselves. *Pros:* no third-party source in our history; smallest repo. *Cons:* graders
  depend on network/upstream availability; the "exact source analyzed" is not directly visible; Graphify and
  the Obsidian/RE evidence point at files not present in the repo.
- **(B) Vendored source (chosen)** — copy the exact buggy tree into `target_repo/luigi_buggy/`. *Pros:*
  reviewers and Graphify read the precise analyzed source directly; evidence (graphs, notes, diffs) maps to
  in-repo files; reproducible without re-cloning. *Cons:* third-party source enters our history; larger repo.
**Tradeoff:** for a reverse-engineering / graph-analysis / evidence-based-debugging assignment, direct
reviewer access to the exact source (B) outweighs the larger repo size (A). Apache-2.0 permits redistribution
with the preserved `LICENSE`, so vendoring is licit.
**Decision:** Vendor the Luigi source at the buggy commit `a0f1db01…` into `target_repo/luigi_buggy/`,
**excluding** upstream `.git` and `.github`, **preserving** `LICENSE` (Apache-2.0), with **no nested git
repo** and **no patches/fix** applied (source kept pristine/buggy). Source edits are permitted only in the
later bug-fix stage (Stage 10); until then the tree stays the exact buggy version.
**Evidence / guardrails:** verified `git rev-parse HEAD == a0f1db01…` in the temp clone; `no nested .git`;
`LICENSE` preserved; buggy line present at `luigi/parameter.py:1118`, fixed pattern absent; provenance in
`target_repo/README.md`; method + checks in `reports/target_repository_acquisition.md`. Committed as
`1299535 Acquire Luigi buggy target repository` (pushed to `origin/main`).
**Consequence:** the vendored tree is tracked deliberately (not git-ignored). All planning/process docs were
**reconciled to this policy before the Stage-4 commit**: `docs/PLAN.md` (§1/§5/§6/§18/§22), `docs/TODO.md`
(rule R4, Stage 4), `README.md`, `docs/PRD.md` (§8 in-scope, §9 out-of-scope, FR-01, §26 constraints, §28
milestone), and `docs/AI_WORKFLOW.md` (vendored-source handling policy). No residual contradiction remains.

## D-008 — Use the official Graphify package `graphifyy` (no-LLM code-graph build); track `graph.json`
**Date:** 2026-06-14
**Context:** Stage 5. The CLI `graphify` was initially "not found" because the **PyPI package is
`graphifyy` (double-y)** while the command is `graphify`. Also, `graphify extract` requires an LLM API key
when the corpus contains docs/images (the vendored tree has `doc/` + `luigi/static/` web assets) — but we
use **no paid APIs/secrets**.
**Alternatives considered:** (A) write our own AST grapher — **rejected** (assignment requires the real
Graphify tool); (B) supply an LLM key for full semantic extraction — **rejected** (no paid API); (C) use
Graphify's **no-LLM code path** on the code corpus — **chosen**.
**Decision:** Install the official tool via `uv tool install graphifyy` (Graphify 0.8.39) and build the
graph with the **no-LLM** commands: `graphify update <path> --no-cluster` (AST), then
`graphify cluster-only <path> --no-label` (clustering + `GRAPH_REPORT.md`, placeholder community names),
then `graphify tree …` for a large-graph HTML visual. Docs/images are not graphed (code-only corpus → no
key). Also resolves **OD-5**: the full `graph.json` is **tracked** (force-added past the
`artifacts/graphify/*.json` ignore rule) so graders can access the graph evidence.
**Evidence / guardrails:** real artifacts in `artifacts/graphify/` (`graph.json` 6,771 nodes / 15,365
edges; `GRAPH_REPORT.md`; `GRAPH_TREE.html`); token cost 0; vendored source verified pristine (in-tree
`graphify-out/` removed); bug still unfixed; full method in `reports/graphify_run.md` and
`artifacts/graphify/graphify_run.log`. Committed as `feb78ea Run Graphify on Luigi target repository`
(pushed to `origin/main`).

## D-009 — Obsidian vault structure: macro→micro navigation, grounded-or-labeled
**Date:** 2026-06-14
**Context:** Stage 6. The vault must be an *active knowledge space* that graders can navigate, built from
the real Graphify artifacts without over-claiming.
**Decision:** Structure `obsidian/` as a hub-and-spoke vault entered from `index.md`, in macro→micro order:
`graphify-overview` → `architecture-map` → `graph-communities` → `parameter-subsystem` → `hot` →
`bug-investigation-seed` → `token-efficiency-plan`, plus `sources`/`open-questions`/`README`. **Grounding
rule:** every architecture/graph statement must be backed by `graph.json`, `GRAPH_REPORT.md`, or a source
path; anything else is explicitly tagged *planned (Stage 7)*. Community **names stay placeholders**
("Community N") because clustering used `--no-label` (no LLM); semantic naming + hub ranking are deferred
to Stage 7.
**Consequence:** the vault is honest and reviewer-navigable now, and Stage 7 has a clear, labeled backlog
in `obsidian/open-questions.md`. Pages link via `[[wiki-links]]`; code is referenced by relative path.
Committed as `6cdfd2f Build Obsidian knowledge vault` (pushed to `origin/main`).

## D-010 — Reverse-engineering method: evidence tags, degree-based hubs, Mermaid `.mmd` diagrams
**Date:** 2026-06-14
**Context:** Stage 7 must reverse-engineer Luigi from the real graph without overclaiming. Graphify ran
no-LLM, so communities are unnamed and only structural (AST/heuristic) edges exist.
**Decision:**
- **Evidence tagging** — every claim is tagged **EXTRACTED** (in `graph.json`/`GRAPH_REPORT.md`/source),
  **INFERRED** (Graphify heuristic edge, ~0.54 confidence band), or *interpretation*. Nothing is said to be
  "proved" by Graphify unless directly present.
- **Hubs by degree** — rank hubs by node degree computed from `graph.json` (no LLM). Explicitly flag the
  top God-nodes as **vendored d3 JS libraries** (web-UI bundling artifact, not core architecture). Formal
  betweenness/centrality and real community names remain open (`obsidian/open-questions.md`).
- **Diagrams as Mermaid `.mmd`** under `artifacts/diagrams/` (text, diff-able, no binary/fabricated images):
  `architecture_block.mmd`, `oop_parameter_diagram.mmd`, `bug_path.mmd`.
**Consequence:** a defensible, honest Stage-7 analysis (`reports/reverse_engineering.md` +
`obsidian/reverse-engineering-analysis.md`) that graders can verify against the artifacts; rendering the
diagrams into the README is deferred to Stage 13 polish. No bug fix, agent, or baseline implied.
Committed as `8991916 Analyze Luigi architecture and bug path` (pushed to `origin/main`).

## D-011 — Baseline token estimate via `characters / 4`; controlled (not blind) baseline protocol
**Date:** 2026-06-14
**Context:** Stage 8 needs a comparable cost number for the naive (no-graph) investigation, with no paid API
to produce exact token counts (OD-3). It also must be honest that the bug is already known (OD-4).
**Decision:**
- **Token estimate** = `characters / 4`, applied consistently and **labeled an estimate** (not exact API
  tokenization). The same method will be applied to the graph-guided run for a like-for-like Stage 11
  comparison.
- **Controlled baseline** — the run is a **fixed protocol** measuring how much raw-code context a naive
  investigator must read starting from the symptom + raw repo; it does **not** claim blind discovery. The
  baseline path uses **no** Graphify/Obsidian/agent inputs (recorded as `false` in the metrics JSON).
**Consequence:** baseline = **4 files / 97,926 chars / ~24,482 est. tokens / 5 rounds**, root cause reached
(`reports/baseline_naive_investigation.md`, `artifacts/validation/baseline_naive_metrics.json`). Limitations
(coarse estimate; protocol-defined, not an empirical average) are stated in the report. No comparison is
claimed complete yet. Committed as `8904b57 Measure naive baseline investigation` (pushed to `origin/main`).

## D-012 — Graph-guided agent is a deterministic LangGraph workflow (no LLM, no API key)
**Date:** 2026-06-14
**Context:** Stage 9 needs an agentic graph-guided workflow, but the project uses **no paid APIs/secrets**.
The assignment's goal here is **graph-guided orchestration and measured context routing**, not text
generation. Confirms **OD-6** (LangGraph over CrewAI).
**Decision:** Implement the workflow as a **compiled LangGraph `StateGraph`** with 8 bounded, tool-like
nodes that read the graph sub-graph + Obsidian pages **before** targeted source ranges. It is **fully
deterministic**: `llm_used = false`, `api_cost_usd = 0`. The "agent" value is the bounded, graph-first
context routing. Token accounting reuses the baseline's `characters/4` estimate (D-011) for a like-for-like
Stage 11 comparison. Code lives in `src/ex04_graph_debugger/` as small modules (each ≤150 lines), with unit
tests. Ruff is scoped to **our** code (`extend-exclude = target_repo, artifacts, obsidian, .venv`) so the
vendored Luigi source is not linted.
**Consequence:** graph-guided run = **5 files / 14,523 chars / ~3,631 est. tokens / 8 states**, root cause
reached (`reports/graph_guided_agent.md`, `artifacts/validation/graph_guided_agent_metrics.json`). No LLM
dependency or key required. The **final** baseline-vs-graph comparison is deferred to Stage 11 (not claimed
here); a preliminary, clearly-labeled observation appears in the report. Committed as
`3b0e3c0 Implement graph-guided agent workflow` (pushed to `origin/main`).

## D-013 — Minimal Luigi fix = TWO lines (widen except AND wrap literal_eval in tuple)
**Date:** 2026-06-14
**Context:** Stage 10. The bug brief suggested widening `except ValueError` → `except (ValueError, TypeError)`
as the minimal fix. Validation under Docker/Python 3.8 showed that change **alone is insufficient**: it
stops the `TypeError`, but the fallback `literal_eval("[1, 2, 3]")` returns a **list**, so the regression
test then fails with `AssertionError ((1,2,3) != [1,2,3])`.
**Decision:** Apply the **two-line** minimal fix in `TupleParameter.parse` (no unrelated refactor) — exactly
the upstream BugsInPy patch:
```diff
-        except ValueError:
-            return literal_eval(x)
+        except (ValueError, TypeError):
+            return tuple(literal_eval(x))
```
Add a focused regression test `TestSerializeTupleParameter.testSerialize` (none existed at the buggy commit).
The fix is applied to the vendored tree as the Stage-10 evidence (updates D-007/R4: source edits were
deferred to Stage 10, and this is that stage).
**Evidence / guardrails:** before = `TypeError: 'int' object is not iterable` (1 failed); after = `1 passed`
(Docker/Python 3.8.20); diff confined to one function + one test class
(`artifacts/validation/stage10_{before_failure,after_success,fix_diff}.txt`, `reports/bug_fix_validation.md`).
No final token comparison claimed (Stage 11). Committed as `a3c59f1 Fix TupleParameter round-trip parsing`
(pushed to `origin/main`).

## D-014 — Final efficiency comparison uses committed Stage 8/9 metrics + the chars/4 estimate
**Date:** 2026-06-14
**Context:** Stage 11 must compare the naive baseline (Stage 8) and graph-guided agent (Stage 9) **without**
re-running either (re-running risks drift; the graph-guided run is already idempotent, D-012).
**Decision:** Build the comparison **only** from the committed metric files
(`baseline_naive_metrics.json` @ `8904b57`, `graph_guided_agent_metrics.json` @ `3b0e3c0`), applying the
same `characters/4` estimate (D-011). Emit `reports/token_efficiency.md` +
`artifacts/validation/token_efficiency_comparison.json` + `.csv`. Frame the result as a **controlled,
single-case comparison** (`universal_claim=false`), present **context volume** (tokens/chars) as the only
demonstrated win — **not** file count or workflow-state count — and exclude the Stage-10 bug fix from the
measurement.
**Evidence / guardrails:** tokens 24,482 → 3,631 = **−20,851 (−85.17%, ≈6.74×)**; chars −83,403 (−85.17%);
files +1, units +3, states +3 (explicitly **not** wins). No LLM/API ($0). Source metric files unchanged.
Committed as `dad0413 Compare baseline and graph-guided token use` (pushed to `origin/main`).
