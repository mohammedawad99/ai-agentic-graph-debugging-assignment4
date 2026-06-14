# Original Extension — Centrality-Based Suspect Ranking (Stage 12)

## 1. Stage name and date/time
Stage 12 — Original extension: centrality-based suspect ranking. Date: 2026-06-14.

## 2. Purpose
A deterministic, no-LLM tool that reads the committed Graphify graph and **triages** which Luigi code
nodes to inspect first for a bug, by blending **graph centrality** with **keyword relevance**. It turns the
static graph into an automatic "where to look" ranking.

## 3. Why this is an original extension
It goes **beyond** the required flow (Graphify run, Obsidian vault, graph-guided agent, fix, token
comparison): none of those *rank* the codebase by bug-suspicion. This adds a reusable, stdlib-only
analytic that scores **2,169** candidate nodes and surfaces the defect neighborhood automatically — a
generalizable triage step a future investigator (human or agent) could run before reading any source.

## 4. Input artifacts used (read-only)
- `artifacts/graphify/graph.json` (Stage 5; 6,771 nodes / 15,365 links). No rerun, no edit.

## 5. Algorithm
- **Graph parsing:** load `nodes`/`links` from `graph.json` (stdlib `json`).
- **Candidate filtering:** keep `file_type=code` nodes whose `source_file` starts with `luigi/` and is
  **not** a vendored web asset (`static/visualiser`, `.js/.css/.html/fonts`). This excludes the huge
  `d3.min.js` (185 nodes) and other viz/minified assets, and excludes tests and rationale nodes — so the
  ranking is **code-investigation oriented**, not "highest degree in the whole graph". → **2,169** candidates.
- **Centrality:** `degree` = number of incident links over the **full** graph; `normalized_centrality =
  degree / max_candidate_degree`.
- **Relevance:** count distinct **query terms** found (case-insensitive) in a node's label + path +
  location + id, normalized by the number of terms. Terms: `tuple, parameter, parse, serialize, json,
  literal_eval, typeerror, iterable, list`.
- **Final ranking formula:** `final = 0.6 * relevance + 0.4 * normalized_centrality`, sorted descending
  (tie-break: relevance, then degree).

## 6. Top 20 suspects (`artifacts/validation/centrality_suspect_ranking_top20.txt`)
| Rank | Label | Path:loc | final | rel | ndeg |
|----:|-------|----------|------:|----:|-----:|
| 1 | MockTarget | luigi/mock.py:L104 | 0.40 | 0.00 | 1.00 |
| 2 | scheduler | luigi/scheduler.py:L126 | 0.219 | 0.00 | 0.548 |
| 3 | ._parse_list() | luigi/parameter.py:L254 | 0.206 | 0.333 | 0.016 |
| 4 | .parse() | luigi/parameter.py:L1046 (ListParameter) | 0.203 | 0.333 | 0.008 |
| 5 | .serialize() | luigi/parameter.py:L1055 (ListParameter) | 0.203 | 0.333 | 0.008 |
| **6** | **.parse() (TupleParameter)** | **luigi/parameter.py:L1095** | **0.203** | 0.333 | 0.008 |
| 7 | parameter.py (module) | luigi/parameter.py:L1 | 0.192 | 0.111 | 0.312 |
| 8 | six.py | luigi/six.py:L1 | 0.182 | 0.00 | 0.456 |
| 9 | CmdlineParser | luigi/cmdline_parser.py:L28 | 0.158 | 0.111 | 0.228 |
| 10 | S3Client | luigi/contrib/s3.py:L95 | 0.155 | 0.00 | 0.388 |
| 11 | Parameter | luigi/parameter.py:L93 | 0.153 | 0.111 | 0.216 |
| 12 | ParameterException | luigi/parameter.py:L65 | 0.150 | 0.111 | 0.208 |
| 13 | ListParameter | luigi/parameter.py:L1006 | 0.148 | 0.222 | 0.036 |
| 14 | .parse() | luigi/parameter.py:L1243 | 0.144 | 0.222 | 0.028 |
| 15 | **TupleParameter (class)** | luigi/parameter.py:L1066 | 0.143 | 0.222 | 0.024 |
| 16–20 | … | luigi/parameter.py (parse/parser methods) | … | … | … |

**13 of the top 20 are in `luigi/parameter.py`** — the file that contains the bug.

## 7. Known bug-target evaluation
| Target | Found? | Rank | Interpretation |
|--------|:------:|:----:|----------------|
| `parameter.py` (file) | yes | **best rank 3** | The bug file dominates the top of the ranking (111 of its nodes are candidates). |
| `TupleParameter.parse` (bug method) | yes | **6 / 2,169** | The exact defect method is in the top 6 — found via relevance, not degree. |
| `TupleParameter` (class) | yes | 15 / 2,169 | The class itself ranks high. |
| `ListParameter.serialize` (root culprit) | yes | **5** | The inherited `json.dumps` serialize that causes the round-trip mismatch is top 5 — a meaningful hint. |

The heuristic surfaces the defect **neighborhood** at the very top without any LLM.

## 8. What the extension adds beyond Graphify/Obsidian/agent
- Graphify *builds* the graph; Obsidian *documents* it; the agent *navigates* a known target. This extension
  **ranks unknown candidates** — it would help locate a defect you did **not** already know, by combining
  structure (centrality) with a small query vocabulary. It is reusable on any Graphify graph.

## 9. Limitations and non-claims
- Centrality + keyword relevance is a **triage heuristic, NOT proof of causality**. It does **not** always
  find bugs and does **not** prove a root cause; it ranks where to look first.
- Pure high-degree hubs with zero relevance (e.g. `MockTarget` #1, `scheduler` #2) can top the list — this
  is **why** the score blends in relevance, and why the bug method still reaches #6.
- Degree is a coarse centrality; results depend on the chosen query terms and the candidate filter.
- This is a **single-case** demonstration on one graph, not a benchmark.

## 10. Reproducibility commands
```
uv run python -m ex04_graph_debugger.centrality_ranking
uv run pytest tests/unit/test_centrality_ranking.py
```
Outputs: `artifacts/validation/centrality_suspect_ranking.{json,csv}` and `…_top20.txt`.

## 11. Quality evidence
`uv run pytest` → **13 passed** (6 new fixture-based tests for degree/relevance/ranking/filter/targets/idempotence);
`uv run ruff check .` → **All checks passed**; `uv run ruff format --check .` → clean; module ≤150 code lines.

## 12. Confirmation
- Graphify artifact read **read-only**; no Graphify rerun; no Obsidian edit.
- No baseline / graph-guided / token-efficiency / Stage-10 artifacts changed.
- No Luigi source/test changed; the applied bug fix is unchanged.
- **No LLM / API**: `llm_used=false`, `api_cost_usd=0`.

## 13. Commit evidence
Committed and pushed as `de32d76 Add centrality suspect ranking extension`.

## 14. Next stage
Stage 13 — final audit / packaging (per `docs/TODO.md`).
