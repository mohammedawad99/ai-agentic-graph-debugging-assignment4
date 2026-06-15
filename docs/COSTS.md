# Costs & Resource Awareness — Assignment 04 (MaRs-777)

## Final result (whole project)
- **$0 external API cost.** Every project run — selection, Docker validation, Graphify, Obsidian, reverse
  engineering, baseline, graph-guided agent, bug fix, token comparison, and the centrality extension — ran
  with **no billed LLM/API calls**.
- **No paid LLM/API in execution:** Graphify ran no-key; the graph-guided agent and the extension are
  **deterministic** (`llm_used = false`, `api_cost_usd = 0`, D-012/D-015); the fix was applied manually under
  Docker/Python 3.8.
- No secrets or API keys are stored in the repository (`.env` is git-ignored; only `.env.example` exists).

## Measured run costs so far (estimate, `characters/4`; D-011)
- Stage 8 baseline (naive): ~24,482 est. tokens, $0 (raw-source reading; no LLM).
- Stage 9 graph-guided agent: ~3,631 est. tokens, $0 (deterministic LangGraph; no LLM) — commit `3b0e3c0`.
- Stage 10 bug fix + before/after proof: **$0 / no LLM API** (manual 2-line fix + Docker/Python 3.8 pytest) — commit `a3c59f1`.
- Stage 11 token-efficiency comparison: **$0 / no LLM API** (pure arithmetic over committed Stage 8/9 metrics) — commit `dad0413`.
- Stage 12 original extension (centrality suspect ranking): **$0 / no LLM API** (deterministic stdlib analytic over `graph.json`) — commit `de32d76`.
- Stage 13 final audit + docs hardening: **$0 / no LLM API** (documentation + local quality gates only) — commit `cf55bac`.
- **Whole project to date: $0 in LLM/API costs** (Graphify no-key, agent + extension deterministic, fix manual under Docker).
- **Final result (controlled, NOT universal):** graph-guided ~3,631 vs baseline ~24,482 est. tokens →
  **−85.17% (~6.74×) less context** for the same root cause. Estimate via `chars/4`, not exact tokenization.

## Token-efficiency experiment (done — Stage 11)
The comparison between the two workflows on the same Luigi bug is complete (`reports/token_efficiency.md`):
- **Baseline (naive):** unguided raw-source reading — 4 files / ~24,482 est. tokens / 5 rounds.
- **Graph-guided:** Graphify/Obsidian-steered routing — 5 files / ~3,631 est. tokens / 8 states.
Both reached the same root cause; the result is a **controlled, single-case** comparison (not universal),
estimated via `chars/4` (not exact tokenization).

## Provenance labeling rule (mandatory)
Every numeric value reported anywhere in this repo must carry one of these labels:
- **measured** — taken directly from API/tool usage metadata or a counter in our code;
- **estimated** — derived/extrapolated (method stated);
- **manual count** — hand-counted by the student (what was counted stated).

Unlabeled numbers are not permitted. This rule is enforced by review and noted in `docs/QUALITY.md`.

## How cost was kept at $0
- The graph-guided agent and the extension were built **deterministic** (no LLM call), so investigation
  cost is **context volume**, not paid tokens.
- Graphify ran via its **no-key** code path; the bug fix was a manual 2-line edit validated under Docker.
- Intermediate artifacts are persisted under `artifacts/` and reused, so no step is re-run unnecessarily.
