# Repository Selection Report (Summary)

How the final target was chosen. Full scoring lives in the working notes; this is the decision summary.

## 1. Initial selection — PySnooper bug 3
Three candidate repos were inspected (BugsInPy, martinpeck/broken-python, andela/buggy-python).
`broken-python` and `buggy-python` were tiny, syntax-error teaching repos (no real tests, GUI/interactive).
Within BugsInPy, **PySnooper bug 3** was the cleanest: a one-line logic bug
(`output_path` → `output`) in a small debugging library, and the **only** case that reproduced directly on the host's Python 3.12.
**Initial pick:** PySnooper bug 3.

## 2. Moodle size instruction changed the decision
The Moodle box added: for excellent (grade-100) submissions, the codebase should be **significant —
~10,000+ LOC and ~70+ code files**. PySnooper (~5 files / ~700 LOC) is far below that bar, so the
selection was re-opened with **size + architectural richness** as first-class criteria.

## 3. Size-driven re-selection
Measured candidate BugsInPy projects (core source, excluding tests):

| Project | Core files | Core LOC | Dependency risk | Notes |
|--------|-----------:|---------:|-----------------|-------|
| **luigi** | ~96 (buggy commit, incl. tests dirs) | ~27.6k | moderate (tornado, dateutil) | DAG/scheduler — rich graph story |
| **tornado** | ~34 non-test | ~24–40k | **lowest (zero third-party)** | clean bug, fewer source files |
| httpie | ~78 | ~9.8k | moderate (+ likely httpbin) | near-exact size fit |
| black | ~41 | ~17.6k | moderate (+ vendored grammar) | fixtures inflate counts |
| PySnooper | ~5 | ~0.7k | lowest | too small (now safety net) |

## 4. Luigi vs Tornado vs PySnooper
- **PySnooper:** rejected as final — too small for the grade-100 reading (kept only as emergency net). _(D-002)_
- **Tornado:** strong fallback — zero-dependency, very clean `url_concat` bug, bug logic verified; but
  **~34 non-test source files** is weaker against the "≥70 files" reading. _(D-003)_
- **Luigi:** satisfies **both** LOC (~27.6k) **and** file-count (~96) criteria, with an ideal
  hubs/communities/paths story for Graphify (it is literally a DAG engine). _(D-001)_

## 5. Cross-cutting blocker discovered
BugsInPy's 2018–2020 commits are pinned to **Python 3.7/3.8** and generally **do not import on Python 3.12**
(e.g. `from collections import Mapping`). Faithful reproduction therefore uses **Docker / Python 3.8** _(D-005)_.

## 6. Final decision
**Selected: Luigi — bug 3 (BugsInPy).** Confirmed reproducible (see `reports/bug_validation.md`).
Fallback: Tornado bug 9. Safety net: PySnooper bug 3.
