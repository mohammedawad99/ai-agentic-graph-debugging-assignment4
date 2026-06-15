# PRD — Graph-Guided Agent (per-mechanism)

**Mechanism:** the deterministic LangGraph graph-guided investigation workflow.
**Module:** `src/ex04_graph_debugger/graph_guided_agent.py` (+ `nodes.py`, `agent_state.py`,
`source_reader.py`, `metrics.py`). **Group:** MaRs-777.

## 1. Purpose
Investigate Luigi bug 3 by routing through the **Graphify code graph and Obsidian vault first**, reading
raw source only when the graph points to it — so the bug neighborhood is reached with **bounded, measured
context** rather than unguided file scanning. The mechanism produces the data behind the token-efficiency
comparison.

## 2. Users / reviewer goal
The **grader/reviewer** wants to see a real agent workflow (LangGraph) that (a) navigates a code graph,
(b) localizes the defect, and (c) reports its context cost reproducibly and honestly. The **student**
wants a deterministic, $0, re-runnable artifact that is safe to execute in CI/tests.

## 3. Inputs
- Graphify graph: `artifacts/graphify/graph.json` (+ `GRAPH_REPORT.md`).
- Obsidian vault pages: `obsidian/*.md` (notably `hot.md`, `parameter-subsystem.md`).
- Target source (read-only): `target_repo/luigi_buggy/luigi/parameter.py`.

## 4. Outputs
- Report: `reports/graph_guided_agent.md`.
- Metrics JSON: `artifacts/validation/graph_guided_agent_metrics.json` (estimated_tokens = 3,631).
- Trace log: `artifacts/validation/graph_guided_agent_trace.log`.
- Files-read list: `artifacts/validation/graph_guided_agent_files_read.txt`.

## 5. Functional requirements
- FR1: Build an explicit LangGraph `StateGraph` (8 states) that starts from graph/vault context.
- FR2: Localize `TupleParameter.parse` and record the inherited-`serialize` / overridden-`parse`
  asymmetry as the lead.
- FR3: Account every read (path, source type, reason, characters) and emit estimated tokens via
  `characters / 4`.
- FR4: Persist report + metrics + trace + files-read to the paths in §4.

## 6. Non-functional requirements
- NFR1: **Deterministic** — same inputs produce the same outputs (no randomness, no wall-clock in output).
- NFR2: **$0** — no LLM and no external/paid API call (`llm_used = false`, `api_cost_usd = 0`).
- NFR3: Each `src/` file ≤ **150 code lines**; passes Ruff (`E,F,W,I,N,UP,B,C4,SIM`) and format check.
- NFR4: **Idempotent under test** — `run(out_dir=...)` writes to a caller-supplied dir so `pytest` never
  mutates tracked Stage-9 artifacts (guard: `test_run_does_not_touch_tracked_artifacts`).

## 7. Acceptance criteria
- `uv run python -m ex04_graph_debugger.graph_guided_agent` reproduces the committed metrics
  (3,631 est. tokens) and the files-read list.
- The graph-guided estimate is materially below the naive baseline (24,482) for the same root cause.
- `uv run pytest` (incl. the agent tests) passes; coverage gate (≥85%) holds.

## 8. Constraints
- No LLM/API; deterministic only.
- Must **not** mutate target source or overwrite locked artifacts during tests.
- Token figures are **estimates** (`chars/4`), explicitly **not** exact tokenizer counts.

## 9. Evidence links
- `reports/graph_guided_agent.md`, `reports/token_efficiency.md`,
  `artifacts/validation/graph_guided_agent_*`, `src/ex04_graph_debugger/`,
  `tests/unit/test_graph_guided_agent.py`, `docs/QUALITY.md`.
