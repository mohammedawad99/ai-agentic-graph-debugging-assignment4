# Submission Checklist — Assignment 04 (MaRs-777)

Tick only when real, in-repo evidence exists. Mirrors `docs/REQUIREMENTS_AUDIT.md`.

## Identity & submission
- [x] Public GitHub repo created and pushed (R-01) — https://github.com/mohammedawad99/ai-agentic-graph-debugging-assignment4
- [x] Group code `MaRs-777` present in README/docs (R-02)
- [ ] Final Moodle submission link recorded — **pending** (wrapper PDF + submit not done)

## Selection & validation
- [x] Luigi bug 3 selected with justification (R-03)
- [x] Size / grade-100 interpretation documented (R-04)
- [x] Docker / Python 3.8 validation documented (R-43)
- [x] Failing-before captured (R-24) — `artifacts/validation/stage10_before_failure.txt` (commit `a3c59f1`)
- [x] Passing-after captured (R-25) — `artifacts/validation/stage10_after_success.txt` (commit `a3c59f1`)
- [x] Before/after reproduced inside final repo (R-23) — Docker/Python 3.8.20 (commit `a3c59f1`)

## Graphify
- [x] Graphify run produced outputs (R-06) — commit `feb78ea`
- [x] `graph.json` present (R-07) — `artifacts/graphify/graph.json` (6,771 nodes / 15,365 edges)
- [x] `GRAPH_REPORT.md` present (R-08) — `artifacts/graphify/GRAPH_REPORT.md` (+ `GRAPH_TREE.html`)

## Obsidian vault
- [x] `index.md` complete (R-10)
- [x] `hot.md` complete (R-11)
- [x] Linked analysis pages, macro/meso/micro (R-12, R-14) — commit `6cdfd2f`

## Reverse engineering & diagrams
- [x] RE write-up (R-05, R-13) — `reports/reverse_engineering.md` (commit `8991916`)
- [x] Block architecture diagram (R-15) — `artifacts/diagrams/architecture_block.mmd`
- [x] OOP / class diagram (R-16) — `artifacts/diagrams/oop_parameter_diagram.mmd`

## Agent workflow & debugging
- [x] Agent workflow (LangGraph) runs (R-17) — deterministic, no LLM (commit `3b0e3c0`)
- [x] Graph-guided path (R-18)
- [x] Baseline naive path (R-19) — commit `8904b57`
- [x] Bug detection + root cause (R-20, R-21)
- [x] Real fix applied (R-22) — `except (ValueError, TypeError)` + `tuple(literal_eval(x))` (commit `a3c59f1`)
- [x] Before/after proof in repo (R-23)

## Token efficiency
- [x] Token counts (labeled `estimated` via chars/4) (R-26) — baseline 24,482 vs graph-guided 3,631
- [x] Files/text units read (R-27) — baseline 4/4 vs graph-guided 5/7
- [x] Iteration counts (R-28) — baseline 5 rounds vs graph-guided 8 states
- [x] Comparison report (R-29) — `reports/token_efficiency.md` (+ JSON/CSV) — commit `dad0413`

## Polish & integrity
- [x] Original extension (R-30) — centrality-based suspect ranking (`reports/original_extension.md`) — commit `de32d76`
- [x] Diagrams present (R-31) — 3 `.mmd` diagrams + `GRAPH_TREE.html`; referenced in README (no raster screenshots included)
- [x] README with required sections (R-32) — hardened in Stage 13
- [x] AI workflow doc (R-33)
- [x] Prompts doc (R-34)
- [x] Decisions doc (R-35) — D-001 … D-015
- [x] Costs doc (R-36) — $0, no LLM/API
- [x] Quality gates defined (R-37)
- [x] uv configured (R-38)
- [x] Ruff clean (R-39) — `uv run ruff check .` → All checks passed
- [x] pytest green (R-40) — 13 passed
- [x] 150-line rule enforced (R-41) — 7 `src/` files, max 142 code lines
- [x] No secrets committed (R-42)
- [x] No overclaiming (R-44, ongoing)
- [x] Final audit complete (R-45) — `reports/final_audit.md` (Stage 13; commit `cf55bac`)

> The only outstanding item is the **Moodle wrapper PDF + submission** (and recording the link).
