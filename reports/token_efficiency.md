# Token-Efficiency Comparison — Stage 11

## 1. Stage name and date/time
Stage 11 — Token-efficiency comparison (naive baseline vs graph-guided agent). Date: 2026-06-14.

## 2. Purpose
Compare the **context volume read** by two documented investigation protocols on the **same** Luigi
`TupleParameter` bug: the Stage 8 controlled **naive baseline** and the Stage 9 deterministic
**graph-guided** LangGraph workflow. Built **only** from the committed Stage 8/9 metrics — neither run was
re-executed.

## 3. Measurement method
`estimated_tokens = characters / 4` — a consistent **estimate**, applied identically to both runs (D-011).
**Not** exact model tokenization. The measured quantity is the **volume of text context each protocol
read**, not LLM reasoning quality.

## 4. Source metrics and provenance
- Baseline: `artifacts/validation/baseline_naive_metrics.json` (Stage 8, commit `8904b57`).
- Graph-guided: `artifacts/validation/graph_guided_agent_metrics.json` (Stage 9, commit `3b0e3c0`).
- Both were read **read-only**; this stage produced `token_efficiency_comparison.json` + `.csv` and this report.

## 5. Comparison table
| Metric | Naive baseline | Graph-guided agent | Delta / interpretation |
|--------|---------------:|-------------------:|------------------------|
| **Estimated tokens** | 24,482 | 3,631 | **−20,851 (−85.17%)** — primary result, lower is better |
| **Characters read** | 97,926 | 14,523 | −83,403 (−85.17%) — lower is better |
| Files read | 4 | 5 | +1 — **not** the win (graph-guided adds graph/Obsidian inputs) |
| Text units read | 4 | 7 | +3 — graph-guided reads **more but smaller** units |
| Rounds / states | 5 | 8 | +3 — graph-guided models orchestration explicitly; **not** a win |
| Root cause reached | yes | yes | both reached it |
| LLM / API cost | $0 (no LLM) | $0 (deterministic, no LLM) | neither used a paid API |

## 6. Calculations
- **Estimated token reduction:** `24,482 − 3,631 = 20,851` → `20,851 / 24,482 × 100 ≈ 85.17%`.
- **Graph-guided token ratio:** `3,631 / 24,482 × 100 ≈ 14.83%` of the baseline.
- **Factor improvement:** `24,482 / 3,631 ≈ 6.74×` less context.
- **Character reduction:** `97,926 − 14,523 = 83,403` → `≈ 85.17%` (tracks tokens, since tokens are chars/4).

## 7. Main result
The graph-guided workflow read about **3,631 estimated tokens** of context vs **24,482** for the naive
baseline — about **20,851 fewer estimated tokens**, or **≈85.17% less context** (**≈6.74×**), while **both**
reached the same root cause.

## 8. Important nuance (read carefully)
- Graph-guided read **more** files (5 vs 4) and **more** text units (7 vs 4), but each unit is **small and
  targeted** (a graph sub-graph extract, three Obsidian pages, three short source line-ranges) instead of a
  few **large** whole files (the baseline read all of `parameter.py` ~44k chars and `parameter_test.py`
  ~46k chars).
- Graph-guided has **more workflow states** (8 vs 5) because it models the orchestration explicitly (load
  graph → read index → read hot → … ). **More states is not presented as a win.**
- The single demonstrated benefit is **reduced context volume** (tokens/characters), not fewer files or
  fewer states.

## 9. What this comparison proves
- Under these two documented protocols, steering with **Graphify + Obsidian** let the investigation reach
  the same root cause while reading **~85% less context** (chars/4 estimate). The graph artifacts let the
  agent jump to `TupleParameter.parse` and its neighborhood instead of reading whole large files.

## 10. What this comparison does NOT prove
- It is **not** a universal benchmark and does **not** imply ~85% savings on other bugs, codebases, or
  agents. One bug, one codebase, two fixed protocols.
- It does **not** use exact model tokenization (chars/4 estimate only).
- The baseline was **not** a blind discovery — it was a controlled raw-source protocol starting from the
  known symptom; a different naive investigator might read more or less.
- It measures **context volume**, not solution correctness, latency, or LLM reasoning cost.

## 11. Relation to Graphify and Obsidian
The graph-guided run consumed (a) a **small extracted sub-graph** from `graph.json` (the bug node + methods
+ incident edges) and (b) three **Obsidian** pages (`index.md`, `hot.md`, `parameter-subsystem.md`) as
**steering context** *before* reading any source. These pointed it straight at `TupleParameter.parse`
(L1095) and its `ListParameter` base, so only **three short source ranges** were read — the source of the
context savings.

## 12. Relation to Stage 10
The **bug fix** and its before/after proof live in Stage 10 (`reports/bug_fix_validation.md`, commit
`a3c59f1`). The fix is **excluded** from this token-comparison measurement — Stage 11 compares only the
**investigation** context volume of the two protocols.

## 13. Limitations
- `characters/4` is coarse; real tokenizers differ.
- Both protocols are **protocol-defined**, not empirical averages over many investigators/agents.
- The graph-guided run is deterministic (no LLM), so this measures **context routing**, not model reasoning.
- Single-case study; relative result only.

## 14. Reproducibility
- Inputs: `artifacts/validation/baseline_naive_metrics.json`, `artifacts/validation/graph_guided_agent_metrics.json`.
- Outputs: `artifacts/validation/token_efficiency_comparison.json`, `artifacts/validation/token_efficiency_table.csv`.
- Recompute by reading the two metric files and applying the §6 formulas.

## 15. Confirmation
- No baseline rerun · no graph-guided rerun · no metric artifacts overwritten.
- No Luigi source changed · no Graphify artifacts changed · no Obsidian pages changed.

## 16. Next stage
Stage 12 — original extension (centrality-based suspect ranking), per `docs/TODO.md`.
