# Index — Luigi Bug 3 Knowledge Vault (PLACEHOLDER)

> Status: **skeleton**. This Obsidian vault is populated after the Graphify run (PLAN steps 4–5).
> Links below are intentional placeholders; target pages are created in later stages.

## Entry points
- [[hot]] — graph hubs / hotspots (most-connected and most-changed code)
- [[macro-architecture]] — system-level view (subsystems, package map) _(later)_
- [[meso-subsystem-parameter]] — the `parameter` subsystem around the bug _(later)_
- [[micro-tupleparameter-parse]] — the defect site `TupleParameter.parse` _(later)_
- [[bug-3-root-cause]] — root-cause narrative _(later)_
- [[graph-report]] — summary mirror of `artifacts/graphify/GRAPH_REPORT.md` _(later)_

## Target at a glance
- **Project:** Luigi (workflow / DAG scheduling engine), via BugsInPy
- **Bug:** 3 — `TupleParameter.parse` in `luigi/parameter.py`
- **Regression test:** `test/parameter_test.py::TestSerializeTupleParameter::testSerialize`
- **Validated:** fail→pass confirmed in Docker / Python 3.8.20 (see `reports/bug_validation.md`)

## How to read this vault (planned)
1. Start at **macro** (whole-system shape) →
2. zoom to **meso** (the parameter subsystem) →
3. zoom to **micro** (the buggy function and its callers/callees).

_No analysis content is asserted yet; nothing here is final._
