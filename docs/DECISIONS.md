# Decisions Log — Assignment 04 (MaRs-777)

Architecture/strategy decisions. Each entry: context → decision → consequence. Dates are absolute.

## D-001 — Select Luigi bug 3 as the final target
**Date:** 2026-06-14
**Context:** Need a real, reproducible Python bug in a codebase large/rich enough for a grade-100 interpretation, but still manageable.
**Decision:** Use **Luigi, bug 3** from **BugsInPy** — defect in `TupleParameter.parse` (`luigi/parameter.py`), regression test `test/parameter_test.py::TestSerializeTupleParameter::testSerialize`, buggy commit `a0f1db01…`.
**Consequence:** ~96 source files / ~27.6k LOC at the buggy commit; clean one-function logic bug; strong DAG/Graphify story. Requires Python 3.8 (see D-005).

## D-002 — Reject PySnooper as too small for the grade-100 interpretation
**Date:** 2026-06-14
**Context:** PySnooper bug 3 was the first pick — clean and the only bug reproducible directly on Python 3.12.
**Decision:** Reject as the *final* target (keep only as an emergency safety net).
**Consequence:** PySnooper is ~5 source files / ~700 LOC — far below the Moodle "significant, ~10k+ LOC, ~70+ files" bar for an excellent submission.

## D-003 — Reject Tornado as the fallback (weaker non-test source file count)
**Date:** 2026-06-14
**Context:** Tornado bug 9 scored highest on setup safety (zero third-party deps) and bug cleanliness, and its bug logic was verified.
**Decision:** Keep Tornado as a strong fallback but not the primary, because its **non-test source file count (~34)** is weaker against the "≥70 files" reading; Luigi satisfies both LOC and file-count criteria.
**Consequence:** If Luigi later proves unworkable, switch to Tornado bug 9 (`url_concat` None-handling).

## D-004 — Prefer LangGraph for the agent workflow (unless evidence later favors CrewAI)
**Date:** 2026-06-14
**Context:** Assignment allows LangGraph or CrewAI.
**Decision:** Default to **LangGraph** for explicit graph-structured control flow that mirrors the graph-guided thesis; revisit only if implementation evidence favors CrewAI.
**Consequence:** Agent deps are added in the agent stage; `config/default.toml` defaults `agent.framework = "langgraph"`.

## D-005 — Use Docker / Python 3.8 for faithful BugsInPy validation and tests
**Date:** 2026-06-14
**Context:** Luigi 2.8.3 (buggy commit) uses `from collections import Mapping`, which fails to import on the host's Python 3.12.
**Decision:** Run all faithful validation/tests in **Docker `python:3.8-slim` (Python 3.8.20)**.
**Consequence:** Reproducible fail→pass already shown in the candidate repo (`reports/bug_validation.md`). Final-repo runs will use the same image.

## D-006 — No implementation before PRD / PLAN / TODO approval
**Date:** 2026-06-14
**Context:** Course process emphasizes planning and review before coding.
**Decision:** This repository stays at **skeleton + requirements audit**; no agent code, no Graphify run, no bug fix until `docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md` are written and approved.
**Consequence:** `src/` and `tests/` carry placeholders only; status labels in the audit reflect this.
