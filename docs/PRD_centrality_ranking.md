# PRD — Centrality Suspect Ranking (per-mechanism)

**Mechanism:** the original extension — a deterministic, no-LLM suspect ranking over the code graph.
**Module:** `src/ex04_graph_debugger/centrality_ranking.py`. **Group:** MaRs-777.

## 1. Purpose
Add original analytical value: rank graph nodes as **bug suspects** by blending **graph centrality**
(structural importance) with **lexical relevance** to the bug, to show how graph structure can *triage*
where to look — without claiming it proves the defect.

## 2. Users / reviewer goal
The **reviewer** wants an original, reproducible contribution beyond the required pipeline. The
**student** wants a stdlib-only, $0, deterministic analytic whose output is verifiable against the known
bug location.

## 3. Inputs
- `artifacts/graphify/graph.json` (read-only): nodes + edges.
- A small set of bug-relevant lexical terms (e.g. `tuple`, `parse`, `serialize`, `parameter`).

## 4. Outputs
- Report: `reports/original_extension.md`.
- Ranking: `artifacts/validation/centrality_suspect_ranking.json` (+ `.csv`, `_top20.txt`).
- Result: bug method `TupleParameter.parse` ranks **#6 of 2,169** candidates.

## 5. Functional requirements
- FR1: Compute a degree-based centrality per node from `graph.json`.
- FR2: Compute a lexical relevance score per node from the bug terms.
- FR3: Combine as `final = 0.6 * relevance + 0.4 * normalized_centrality`; rank descending.
- FR4: Persist ranking to §4 paths and flag the known target's rank.

## 6. Non-functional requirements
- NFR1: **Deterministic**, **stdlib-only**, **$0** (`llm_used = false`, `api_cost_usd = 0`).
- NFR2: ≤ **150 code lines** (currently 142); passes Ruff (`E,F,W,I,N,UP,B,C4,SIM`) + format.
- NFR3: Reads `graph.json` **read-only**; idempotent `out_dir` write so tests don't touch tracked artifacts.

## 7. Acceptance criteria
- `uv run python -m ex04_graph_debugger.centrality_ranking` reproduces the committed ranking and the
  #6/2,169 placement.
- `uv run pytest` (incl. `tests/unit/test_centrality_ranking.py`) passes; coverage gate (≥85%) holds.

## 8. Constraints
- No LLM/API; deterministic only.
- **Triage heuristic, not proof** — the ranking does **not** claim to prove the root cause.
- Must not mutate target source or overwrite locked artifacts in tests.

## 9. Evidence links
- `reports/original_extension.md`, `artifacts/validation/centrality_suspect_ranking.{json,csv}`,
  `src/ex04_graph_debugger/centrality_ranking.py`, `tests/unit/test_centrality_ranking.py`.
