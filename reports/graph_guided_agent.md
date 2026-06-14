# Graph-Guided Agent Workflow — Stage 9

## 1. Stage name and date/time
Stage 9 — Graph-guided agent workflow. Date: 2026-06-14.

## 2. Purpose
Build and run a **bounded, agentic graph-guided workflow** that consults **Graphify + Obsidian before raw
source** to locate and explain the `TupleParameter` bug path, measuring files/text-units/tokens/rounds for
the later (Stage 11) comparison against the Stage 8 naive baseline. **No bug fix is applied.**

## 3. Framework used: LangGraph
**LangGraph** (`uv add langgraph` → `langgraph>=1.2.5`). The workflow is a compiled `StateGraph` with 8
ordered nodes (`langgraph.graph.StateGraph`, `START`, `END`). No CrewAI; no fallback substitution.

## 4. Whether LLM/API was used
**No LLM. No API key. API cost: $0.** This is a **deterministic** LangGraph state machine whose nodes are
tool-like readers of graph/Obsidian/source artifacts. Honest flags in the metrics JSON:
`llm_used: false`, `api_cost_usd: 0`, `agent_used: true`. The "agent" contribution is the bounded,
graph-first **context routing/orchestration**, not text generation.

## 5. Inputs used
- `artifacts/graphify/graph.json` (queried programmatically for the bug sub-graph).
- `obsidian/index.md`, `obsidian/hot.md`, `obsidian/parameter-subsystem.md`.
- `target_repo/luigi_buggy/luigi/parameter.py` (only **targeted line ranges**, read-only).
- The Stage 8 baseline metrics are stored as a **reference for later context only** — they did **not** guide
  navigation.

## 6. Workflow states (8, bounded)
`load_graph_artifacts → read_index → read_hot_context → read_parameter_context → select_relevant_source →
inspect_bug_path → propose_root_cause → write_metrics_and_report`. Graph/Obsidian are consulted **before**
any source read; source reads are limited to graph-derived line ranges.

## 7. Step-by-step trace (`artifacts/validation/graph_guided_agent_trace.log`)
1. `load_graph_artifacts` — `graph.json` → node `luigi_parameter_tupleparameter` (TupleParameter @ L1066); 6 incident edges, 1 method node. [graphify]
2. `read_index` — `obsidian/index.md` (2,043 chars). [obsidian]
3. `read_hot_context` — `obsidian/hot.md` (2,736 chars). [obsidian]
4. `read_parameter_context` — `obsidian/parameter-subsystem.md` (2,988 chars). [obsidian]
5. `select_relevant_source` — chose ranges L90–135, L1006–1066, L1066–1120 (from graph node locations; **no** full-file read, **no** baseline guidance).
6. `inspect_bug_path` — `parameter.py` L90–135 (1,780 chars) [source].
7. `inspect_bug_path` — `parameter.py` L1006–1066 (1,455 chars) [source].
8. `inspect_bug_path` — `parameter.py` L1066–1120 (1,731 chars) [source].
9. `propose_root_cause` — explanation derived (deterministic, no LLM).
10. `write_metrics_and_report` — metrics summarized.

## 8. Files / text units read
| Source | Path | Range | Chars | Est. tokens |
|--------|------|-------|------:|------------:|
| graphify | `artifacts/graphify/graph.json` (sub-graph extract) | — | 1,790 | 448 |
| obsidian | `obsidian/index.md` | full | 2,043 | 511 |
| obsidian | `obsidian/hot.md` | full | 2,736 | 684 |
| obsidian | `obsidian/parameter-subsystem.md` | full | 2,988 | 747 |
| source | `…/luigi/parameter.py` | L90–135 | 1,780 | 445 |
| source | `…/luigi/parameter.py` | L1006–1066 | 1,455 | 364 |
| source | `…/luigi/parameter.py` | L1066–1120 | 1,731 | 433 |
| **Total** | 5 files / 7 units | — | **14,523** | **3,631** |

> Note on the graphify unit: `graph.json` (6 MB) is **parsed programmatically** to navigate; only the small
> **extracted sub-graph** (target node + methods + incident edges, 1,790 chars) is counted as consumed
> context. Parsing cost is navigation, not LLM context.

## 9. Token estimation method
`estimated_tokens = characters / 4` — the **same** estimate used for the Stage 8 baseline (D-011), labeled
an estimate (not exact API tokenization).

## 10. Metrics summary (`artifacts/validation/graph_guided_agent_metrics.json`)
- total_files_read: 5 · total_text_units_read: 7 · total_characters_read: 14,523 · estimated_tokens: 3,631
- investigation_rounds: 8 · root_cause_reached: true · framework: langgraph
- graphify_used: true · obsidian_used: true · agent_used: true · llm_used: false · api_cost_usd: 0 · bug_fix_applied: false

## 11. Root cause reached? — **Yes**
Reached deterministically from the graph-derived neighborhood + targeted ranges (no full-file scan).

## 12. Explanation produced by the workflow
> TupleParameter (L1066) extends ListParameter and overrides `parse` only; it inherits
> `ListParameter.serialize` (`json.dumps`). `serialize((1,2,3))` → `"[1, 2, 3]"`. `TupleParameter.parse`
> (L1095) does `json.loads` → `[1,2,3]` then `tuple(tuple(x) for x in …)` which runs `tuple(1)` on an int →
> `TypeError: 'int' object is not iterable`. The guard `except ValueError` (L1117) is too narrow to catch the
> `TypeError`, so it propagates.

## 13. Baseline reference (context only — NOT the final comparison)
Stored in the metrics JSON: `baseline_estimated_tokens: 24482`, `baseline_files_read: 4`, `baseline_rounds: 5`.

**Preliminary observation (NOT FINAL — the real comparison is Stage 11):** under this protocol the
graph-guided run consumed ~3,631 est. tokens vs ~24,482 for the naive baseline (≈85% fewer; ~6.7×), reading
5 targeted files/extracts instead of 4 large full files. This is a single deterministic run under a fixed
protocol, **not** the validated Stage 11 token-efficiency comparison.

## 14. Limitations
- Deterministic, no-LLM workflow — it measures **graph-guided context routing**, not LLM reasoning cost.
- `characters/4` is a coarse token estimate; real tokenizers differ.
- Both runs are **protocol-defined**, not empirical human/agent averages; the comparison value is relative.
- The graphify "context" is the extracted sub-graph, not the full 6 MB file (stated above).

## 15. Confirmations
- **Graphify used** (true) · **Obsidian used** (true) · **agent workflow used** (true, LangGraph).
- **No Luigi source changed** (read-only; targeted ranges only).
- **No bug fix applied** (`except ValueError:` still present; fixed pattern absent).
- **No final token-efficiency comparison claimed** (reserved for Stage 11; `reports/token_efficiency.md` not written).

## 16. Commit evidence
Committed and pushed as `3b0e3c0 Implement graph-guided agent workflow`.

## 17. Next stage
Stage 10 — bug fix and before/after proof (per `docs/TODO.md`).
