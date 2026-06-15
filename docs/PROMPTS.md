# Prompts Log — Assignment 04 (MaRs-777)

Summaries of the instructions that drove each stage. These are **paraphrased prompt summaries**,
not verbatim private content and not fabricated. Hidden/internal reasoning is intentionally excluded.

## P-01 — Repository selection
**Stage:** selection.
**Summary:** Evaluate three candidate Python bug repos (BugsInPy, broken-python, buggy-python) against ~10 criteria (setup, bug clarity, test reproducibility, size, Graphify/Obsidian value, architecture, token-efficiency potential, dependency risk, report potential). Inspect read-only, clone only to a temp candidate area, no implementation/fix/commit. Produce a strict selection report.
**Outcome:** Initial pick = PySnooper bug 3 (clean, reproducible on 3.12, but small).

## P-02 — Size-driven re-selection
**Stage:** re-selection.
**Summary:** Moodle adds a size expectation for excellent submissions (~10k+ LOC, ~70+ files). Re-open selection, prefer BugsInPy, measure LOC/file counts, weigh size vs manageability and dependency risk. Produce a new strict report with ≥3 stronger candidates.
**Outcome:** Luigi bug 3 chosen (size + DAG/Graphify richness); Tornado bug 9 as fallback; PySnooper demoted to safety net. Discovered cross-cutting blocker: BugsInPy 2018–2020 commits need Python 3.7/3.8 (won't import on 3.12).

## P-03 — Docker-based faithful validation
**Stage:** validation.
**Summary:** Reproduce Luigi bug 3 faithfully in Python 3.8 via Docker. Record clean state and proof the regression test is absent at the buggy commit; overlay the fixed-commit test; capture failing-before; apply a guarded minimal patch; capture passing-after; revert both files and all artifacts; confirm pristine. Validation only — no commit/implementation, no patch left applied.
**Outcome:** `Luigi confirmed`. Failing-before `TypeError: 'int' object is not iterable`; passing-after `1 passed`; tree reverted to clean at the buggy commit.

## P-04 — Final repository skeleton + Requirements Audit
**Stage:** scaffolding.
**Summary:** Create the final repo `ai-agentic-graph-debugging-assignment4` (group `MaRs-777`) with a fixed directory structure, README, requirements-audit table (45 requirements), decisions/prompts/AI-workflow/costs/quality/checklist docs, PRD/PLAN/TODO placeholders, uv-compatible `pyproject.toml`, `.env.example`, `.gitignore`, package and test placeholders, and report stubs. Skeleton + audit only — no clone of Luigi, no Graphify, no agent, no fix, no commit.
**Outcome:** Recorded in this repo; see `reports/` and `docs/`.

## P-05 — Target repository acquisition
**Intent:** Vendor the exact Luigi buggy source into the repo. **Allowed:** clone the buggy commit to a temp
area, copy into `target_repo/luigi_buggy/` excluding `.git`/`.github`/caches, preserve LICENSE. **Prohibited:**
patches, fix, Graphify, agent, commit during acquisition. **Result:** vendored source (244 py / 58.6k LOC),
no nested `.git`, decision D-007. **Commit:** `1299535`.

## P-06 — Graphify setup/run (graphifyy discovery)
**Intent:** Build a real code graph. **Allowed:** install the official tool; run no-LLM. **Prohibited:**
fabricate artifacts, install unverified packages. **Result:** PyPI package is **`graphifyy`** (CLI `graphify`);
no-key route (`update`/`cluster-only --no-label`) → `graph.json` (6,771/15,365), `GRAPH_REPORT.md`,
`GRAPH_TREE.html`; D-008. **Report:** `reports/graphify_run.md`. **Commit:** `feb78ea`.

## P-07 — Obsidian vault creation
**Intent:** Document the graph as a navigable vault. **Allowed:** write linked Markdown grounded in
`graph.json`/`GRAPH_REPORT.md`/source. **Prohibited:** fabricated findings; claim later stages done.
**Result:** `obsidian/` (index, hot + analysis pages), D-009. **Report:** `reports/obsidian_vault.md`. **Commit:** `6cdfd2f`.

## P-08 — Reverse engineering analysis
**Intent:** Macro→meso→micro analysis + diagrams. **Allowed:** read graph/source read-only; tag
EXTRACTED/INFERRED/interpretation. **Prohibited:** edit source, fix, overclaim. **Result:**
`reports/reverse_engineering.md`, 3 `.mmd` diagrams, D-010. **Commit:** `8991916`.

## P-09 — Baseline naive investigation
**Intent:** Measure raw-source context cost (no graph/Obsidian/agent). **Allowed:** raw `grep`/`sed`/`wc`,
chars/4 estimate. **Prohibited:** use graph artifacts; apply fix. **Result:** 4 files / 97,926 chars / ~24,482
est. tokens / 5 rounds, D-011. **Report:** `reports/baseline_naive_investigation.md`. **Commit:** `8904b57`.

## P-10 — LangGraph graph-guided agent
**Intent:** Bounded graph/Obsidian-first context routing, measured. **Allowed:** add `src/` modules (≤150
lines) + tests, deps via uv. **Prohibited:** apply fix; require an API key; claim final comparison.
**Result:** deterministic LangGraph (no LLM, $0): 5 files / 14,523 chars / ~3,631 est. tokens / 8 states, D-012.
**Report:** `reports/graph_guided_agent.md`. **Commit:** `3b0e3c0`.

## P-11 — Bug fix + before/after validation
**Intent:** Apply the minimal fix with rigorous before/after proof. **Allowed:** edit `parameter.py` + add a
regression test; Docker/Python 3.8. **Prohibited:** unrelated refactor; rerun final comparison.
**Result:** two-line fix (`except (ValueError, TypeError)` + `tuple(literal_eval(x))`); before `TypeError`,
after `1 passed`; D-013. **Report:** `reports/bug_fix_validation.md`. **Commit:** `a3c59f1`.

## P-12 — Token-efficiency comparison
**Intent:** Compare baseline vs graph-guided from committed metrics. **Allowed:** arithmetic over Stage 8/9
JSON. **Prohibited:** rerun runs; overwrite metrics; universal-benchmark claim. **Result:** −20,851
(−85.17%, ~6.74×); controlled single-case, D-014. **Report:** `reports/token_efficiency.md`. **Commit:** `dad0413`.

## P-13 — Original extension / centrality ranking
**Intent:** Add original value — rank suspect nodes. **Allowed:** stdlib-only `src/` module + tests, read-only
on `graph.json`. **Prohibited:** rerun Graphify; claim it proves root cause. **Result:** centrality+relevance
blend; bug method ranks **#6 / 2,169**; D-015. **Report:** `reports/original_extension.md`. **Commit:** `de32d76`.

## P-14 — Final audit + documentation hardening
**Intent:** Make the repo submission-ready. **Allowed:** edit docs/README/checklist; run gates. **Prohibited:**
touch code/source/artifacts; overclaim. **Result:** README rewrite, `reports/final_audit.md`, checklist aligned;
gates green. **Commits:** `cf55bac`, `39e4912`.

## P-15 — Scope correction (external submission is not a repo stage)
**Intent:** Drop the external submission-packaging steps from repository scope so the repo ends at Stage 13.
**Allowed:** doc edits only. **Prohibited:** create a PDF; add new stages; claim the work was submitted.
**Result:** repo ends at Stage 13; the external submission is framed as a manual step outside the repository.
**Commit:** `2561f1b`.

> This log covers the full workflow (P-01 … P-15). Summaries are paraphrased, not verbatim, and not fabricated.
