# Obsidian Vault — Luigi Bug 3

This directory is an **Obsidian knowledge vault** for Assignment 04. Pages are plain Markdown linked with
`[[wiki-links]]`.

## How to open
- **Obsidian:** "Open folder as vault" → select this `obsidian/` directory. Internal `[[links]]` and the
  graph view will work.
- **Plain Markdown:** any viewer/GitHub works; start at **[[index]]**.

## Start here
- **[[index]]** — navigation hub and recommended reading order.

## Scope / honesty
Every architecture or graph claim is grounded in `artifacts/graphify/graph.json`,
`artifacts/graphify/GRAPH_REPORT.md`, or the vendored source `target_repo/luigi_buggy/`, and tagged
**EXTRACTED / INFERRED / interpretation** at point of use. This is the **final repository knowledge
vault**; the full reverse-engineering analysis is in [[reverse-engineering-analysis]] and the bug **is
fixed** in `target_repo/luigi_buggy/luigi/parameter.py` (Stage 10) with before/after proof in
`reports/bug_fix_validation.md`. See [[sources]] for provenance.
