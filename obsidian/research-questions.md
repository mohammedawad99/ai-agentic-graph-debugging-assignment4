# Research Questions (RQ1–RQ8)

Explicit answers to the eight assignment research questions, each grounded in in-repo evidence and
stated with honest limitations. Concise here; deeper detail is in the linked reports and vault pages.

## RQ1 — What is the actual architecture of the project?
Luigi is a **workflow / DAG engine**: `Task` units declare dependencies (`requires`) and outputs
(`Target`), a scheduler/worker pair executes the DAG, and `Parameter` classes type-and-(de)serialize task
inputs. The Graphify graph is **6,771 nodes / 15,365 edges**. Evidence: `reports/reverse_engineering.md`
(§4 macro), `artifacts/graphify/GRAPH_REPORT.md`, `artifacts/diagrams/architecture_block.mmd`,
[[architecture-map]]. *Limitation:* the macro picture is read from the graph + key source paths, not an
exhaustive module-by-module audit.

## RQ2 — What are the central components and their responsibilities?
Core clusters: **task model** (`task.py` — `Task`, `Register`), **parameters** (`parameter.py` —
`Parameter` → `ListParameter` → `TupleParameter`, etc.), **scheduling** (`scheduler.py`, `worker.py`),
**targets/IO** (`target.py`, `local_target.py`), and **CLI** (`cmdline_parser.py`,
`interface.py`). Evidence: `reports/reverse_engineering.md` §5 (meso), [[parameter-subsystem]],
[[graph-communities]]. *Limitation:* responsibilities summarized from the graph + headline source, not
full behavioral coverage.

## RQ3 — Where are God-nodes, mixed responsibilities, or risky hubs?
High-degree hubs in `GRAPH_REPORT.md` cluster around the **task/register** and **scheduler** subsystems
(many incoming dependency edges) and the **`Parameter` family** (broad reuse). These are *risk hubs* —
changes ripple widely. Evidence: `reports/reverse_engineering.md` §5–6, [[graph-communities]], and the
centrality view in `reports/original_extension.md`. *Limitation:* "God-node" here means high graph
centrality, **not** an asserted code-smell verdict; it is a triage signal.

## RQ4 — How were block architecture and OOP/class schemas extracted?
The block architecture comes from Graphify's module/community structure
(`GRAPH_REPORT.md` → `artifacts/diagrams/architecture_block.mmd`). The OOP/class schema (the
`Parameter → ListParameter → TupleParameter` hierarchy and the `parse`/`serialize` methods) was read from
the graph's **inherits**/**method** edges in `graph.json` and confirmed against source, rendered as
`artifacts/diagrams/oop_parameter_diagram.mmd`. Evidence: `reports/reverse_engineering.md` §4–6,
[[architecture-map]], [[parameter-subsystem]].

## RQ5 — How was the bug identified and what is the root cause?
The graph surfaced an **asymmetry**: `TupleParameter` overrides `parse` but **inherits**
`ListParameter.serialize` (`json.dumps`). So `serialize((1,2,3))` → `"[1, 2, 3]"`; the buggy `parse` does
`json.loads` → `[1,2,3]` then `tuple(1)` → **`TypeError`**, which the narrow `except ValueError` misses.
Fix: `except (ValueError, TypeError)` + `return tuple(literal_eval(x))`. Evidence:
`reports/bug_analysis.md`, `reports/bug_fix_validation.md`, `artifacts/diagrams/bug_path.mmd`, [[hot]].
*Limitation:* confirmed by a **focused** Docker/Python 3.8.20 regression test, not the full suite.

## RQ6 — What is the advantage of graph navigation over linear reading?
Graph navigation lets the investigation jump **straight to the bug neighborhood** via inheritance/method
edges instead of scanning files top-to-bottom. In the controlled comparison it read fewer characters to
reach the same root cause. Evidence: `reports/token_efficiency.md`, `reports/graph_guided_agent.md`,
`reports/baseline_naive_investigation.md`. *Limitation:* a **single-case** result, not a universal claim.

## RQ7 — How did the agent reduce context/tokens, and what did it not reduce?
By routing through Graphify/Obsidian first, the graph-guided run used **~3,631** vs the naive baseline
**~24,482** estimated tokens (`chars/4`) — **≈85.17% (~6.74×) less context** — for the same root cause.
It did **not** reduce the *number of investigation steps* (8 graph states vs 5 naive rounds) and does
**not** reduce model-reasoning cost (the workflow is deterministic, no LLM). Evidence:
`reports/token_efficiency.md`, `artifacts/validation/token_efficiency_comparison.json`. *Limitation:*
token figures are estimates, not exact tokenizer counts.

## RQ8 — What original extensions would be useful, and what was implemented?
Useful directions: centrality-based suspect ranking, change-impact (blast-radius) analysis, and
community-aware test prioritization. **Implemented:** a deterministic, no-LLM **centrality + relevance
suspect ranking** over `graph.json` that places the bug method `TupleParameter.parse` at **rank #6 of
2,169** candidates. Evidence: `reports/original_extension.md`,
`src/ex04_graph_debugger/centrality_ranking.py`, `docs/PRD_centrality_ranking.md`,
`artifacts/validation/centrality_suspect_ranking.{json,csv}`. *Limitation:* a **triage heuristic**, not
proof of root cause.

## Related
- [[index]] · [[hot]] · [[reverse-engineering-analysis]] · [[architecture-map]] · [[parameter-subsystem]]
- Reports: `reports/reverse_engineering.md`, `reports/bug_analysis.md`, `reports/bug_fix_validation.md`,
  `reports/token_efficiency.md`, `reports/original_extension.md`.
