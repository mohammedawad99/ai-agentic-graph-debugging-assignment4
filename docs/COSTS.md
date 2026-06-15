# Costs & Resource Awareness — Assignment 04 (MaRs-777)

## Current status
- **No paid API usage to date — through Stage 9.** Selection, validation, Graphify, Obsidian, reverse
  engineering, the naive baseline, and the **graph-guided agent (Stage 9)** all ran with **no billed LLM
  API calls**.
- **Stage 9 agent: `llm_used = false`, `api_cost_usd = 0`.** The graph-guided workflow is a **deterministic
  LangGraph** state machine (no API key required) — see `docs/DECISIONS.md` D-012.
- No secrets or API keys are stored in the repository (`.env` is git-ignored; only `.env.example` exists).

## Measured run costs so far (estimate, `characters/4`; D-011)
- Stage 8 baseline (naive): ~24,482 est. tokens, $0 (raw-source reading; no LLM).
- Stage 9 graph-guided agent: ~3,631 est. tokens, $0 (deterministic LangGraph; no LLM) — commit `3b0e3c0`.
- Stage 10 bug fix + before/after proof: **$0 / no LLM API** (manual 2-line fix + Docker/Python 3.8 pytest) — commit `a3c59f1`.
- Stage 11 token-efficiency comparison: **$0 / no LLM API** (pure arithmetic over committed Stage 8/9 metrics) — commit `dad0413`.
- Stage 12 original extension (centrality suspect ranking): **$0 / no LLM API** (deterministic stdlib analytic over `graph.json`) — commit `de32d76`.
- Stage 13 final audit + docs hardening: **$0 / no LLM API** (documentation + local quality gates only).
- **Whole project to date: $0 in LLM/API costs** (Graphify no-key, agent + extension deterministic, fix manual under Docker).
- **Final result (controlled, NOT universal):** graph-guided ~3,631 vs baseline ~24,482 est. tokens →
  **−85.17% (~6.74×) less context** for the same root cause. Estimate via `chars/4`, not exact tokenization.

## Future token / cost tracking (agent stage)
The **token-efficiency experiment** will compare two workflows on the same Luigi bug:
- **Baseline (naive):** unguided exploration of the codebase.
- **Graph-guided:** investigation steered by the Graphify graph (hubs, paths, communities).

For each workflow we will record:
- total tokens (prompt + completion),
- number of files / text units read,
- number of iterations / agent steps,
- wall-clock (informational),
- approximate monetary cost (if a paid model is used).

## Provenance labeling rule (mandatory)
Every numeric value reported anywhere in this repo must carry one of these labels:
- **measured** — taken directly from API/tool usage metadata or a counter in our code;
- **estimated** — derived/extrapolated (method stated);
- **manual count** — hand-counted by the student (what was counted stated).

Unlabeled numbers are not permitted. This rule is enforced by review and noted in `docs/QUALITY.md`.

## Cost-control intentions
- Prefer small, cached prompts and reuse of graph artifacts to keep the graph-guided run cheap.
- Use the most capable Claude model only where it adds value; record the model used.
- Avoid re-running expensive steps; persist intermediate artifacts under `artifacts/`.
