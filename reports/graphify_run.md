# Graphify Run Report — Stage 5

> **Status: SUCCESS.** Real Graphify artifacts were produced from the vendored Luigi buggy source. Nothing
> was fabricated. Token cost: **0** (no LLM/API used — code-only AST extraction).

## 1. Stage name and date/time
Stage 5 — Graphify setup and first graph run. Date: 2026-06-14 (run timestamps in
`artifacts/graphify/graphify_run.log`).

## 2. How the earlier blocker was resolved
The first attempt was marked BLOCKED because the CLI command `graphify` could not be found. Root cause:
the **PyPI package is named `graphifyy` (double-y)** while the installed CLI is `graphify`. Resolved by
installing the official tool:
```
uv tool install graphifyy        # installs CLI: graphify (0.8.39) + graphify-mcp
```
A second, smaller blocker then appeared: `graphify extract` refused to run because the vendored tree
contains **24 docs + 39 images** (e.g. `luigi/static/visualiser/` web assets, `doc/`) that would need an
**LLM API key** for semantic extraction. Per the no-paid-API rule, we used the tool's **no-LLM code path**
instead (the tool itself states "a code-only corpus needs no key").

## 3. Input path
`target_repo/luigi_buggy/` (vendored Luigi source; 264 code files extracted).

## 4. Target commit
Luigi buggy commit `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`. (Graphify's `GRAPH_REPORT.md` stamps
"Built from commit `1233ed16`" — that is **our** repo HEAD at run time, not Luigi's; the *content* graphed
is the vendored Luigi buggy source.)

## 5. Graphify command(s) used (exact)
```
# 1) AST code-graph build — NO LLM key (code-only corpus):
graphify update target_repo/luigi_buggy --no-cluster
# 2) Clustering + report + Obsidian-wiki links — NO LLM (--no-label keeps placeholder community names):
graphify cluster-only target_repo/luigi_buggy --no-label
# 3) Large-graph visual (HTML collapsible tree; standard graph.html viz is skipped above 5000 nodes):
graphify tree --graph target_repo/luigi_buggy/graphify-out/graph.json \
              --output target_repo/luigi_buggy/graphify-out/GRAPH_TREE.html --label luigi_buggy
```
(An earlier `graphify extract target_repo/luigi_buggy --out . --no-cluster` failed with
*"no LLM API key found (63 doc/paper/image file(s) need semantic extraction)"* — recorded in the run log.)

## 6. Environment / tool version
- Tool: **Graphify 0.8.39** (PyPI `graphifyy`), executables `graphify`, `graphify-mcp`.
- Host Python: `Python 3.12.3`; uv `0.11.9`.
- LLM backend: **none** (no API key used; semantic/INFERRED-by-LLM step not run).

## 7. Output directory
Graphify writes to `<path>/graphify-out/` by default. We ran with that default, **copied the final
artifacts** into `artifacts/graphify/`, and then **removed** `target_repo/luigi_buggy/graphify-out/`
(including its `cache/`) so the vendored source stays pristine.

## 8. Artifact list (`artifacts/graphify/`)
- `graph.json` — machine-readable graph (6.0 MB). **Real.**
- `GRAPH_REPORT.md` — human report with community hubs, Obsidian `[[wiki-links]]` (92 KB).
- `GRAPH_TREE.html` — interactive D3 collapsible-tree visual (460 KB).
- `.graphify_labels.json`, `.graphify_root` — graph metadata.
- `manifest.json` — corpus scan manifest (file inventory) from the extract probe.
- `graphify_run.log` — full command/run log (incl. the failed extract attempt + canonical sequence).

## 9. graph.json validation summary
Valid JSON, top-level `dict`. Keys: `['input_tokens', 'links', 'nodes', 'output_tokens']`.
- **nodes: 6,771**
- **edges (`links`): 15,365**
- `input_tokens: 0`, `output_tokens: 0` (no LLM cost).
- Node schema: `id, label, file_type, source_file, source_location, _origin`.
- Edge schema: `source, target, relation, context, confidence, weight, source_file, source_location`.
- **Bug node present:** `TupleParameter` → node id `luigi_parameter_tupleparameter` (good for Stage 7 traceability).

> Count note (honest): `graph.json` retains **6,771 nodes / 15,365 edges** (from the `update` build).
> `GRAPH_REPORT.md` reports **6,705 nodes / 13,222 edges / 326 communities** because `cluster-only`
> re-derived/dedup'd same-named symbols and **refused to shrink** the authoritative `graph.json`. Both
> numbers are real outputs of the same run; the larger graph.json is the canonical artifact.

## 10. GRAPH_REPORT.md status
Present (92 KB). Contains Summary (nodes/edges/communities), Extraction quality (86% EXTRACTED / 14%
INFERRED), Graph Freshness, and **Community Hubs** navigation using Obsidian `[[wiki-links]]`.

## 11. Visual artifact status
`GRAPH_TREE.html` (460 KB) produced. The default `graph.html` force-directed viz was **skipped by the
tool** because the graph exceeds its 5,000-node viz limit; the collapsible tree is the supported large-graph
visual.

## 12. Wiki / Obsidian-compatible output status
Yes — `GRAPH_REPORT.md` emits `[[wiki-links]]` (e.g. `[[_COMMUNITY_Community 0|Community 0]]`), directly
usable when building the Obsidian vault in Stage 6.

## 13. Confirmation no Luigi source was changed
Confirmed — `git status --porcelain target_repo/luigi_buggy` → **0 entries**; the temporary in-tree
`graphify-out/` was removed.

## 14. Confirmation no bug fix was applied
Confirmed — `luigi/parameter.py:1117` still `except ValueError:`; fixed pattern
`except (ValueError, TypeError)` is absent.

## 15. Tracking note (OD-5)
`artifacts/graphify/*.json` is currently matched by `.gitignore`, so `graph.json`, `.graphify_labels.json`,
and `manifest.json` are ignored. To give graders the graph evidence, these will be **force-added**
(`git add -f`) at the Stage 5 commit (resolves OD-5: keep the full `graph.json` tracked). Decision recorded
as **D-008**.

## 16. Next planned stage
Stage 6 — Obsidian vault construction (now unblocked: real `graph.json` + Obsidian-wiki `GRAPH_REPORT.md`).
