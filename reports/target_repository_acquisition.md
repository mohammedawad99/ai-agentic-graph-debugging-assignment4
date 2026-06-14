# Target Repository Acquisition Report — Stage 4

Acquisition of the exact Luigi buggy source into the assignment repository. **Acquisition only** —
no Graphify, no agent, no patch, no fix, no commit.

## 1. Acquisition method
Temporary clone outside the final repo, then a clean copy into the repo **without** upstream VCS metadata:
1. `git init` in `/tmp/ex04_luigi_source`; add remote `https://github.com/spotify/luigi.git`.
2. `git fetch --depth 1 origin a0f1db01…` then `git checkout FETCH_HEAD`.
3. Verified `git rev-parse HEAD` equals the target commit.
4. `rsync -a` into `target_repo/luigi_buggy/` excluding `.git`, `.github`, `__pycache__`, `*.pyc`,
   `.pytest_cache`, `*.egg-info`, `build/`, `dist/`.
5. Preserved upstream `LICENSE`.
6. No nested git repository created inside `target_repo/luigi_buggy/`.

## 2. Exact upstream commit verified
`a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4` (Luigi 2.8.3) — confirmed via `git rev-parse HEAD` in the
temporary clone; the clean checkout had an empty `git status`.

## 3. Final target path
`target_repo/luigi_buggy/` (top-level mirrors upstream: `luigi/`, `test/`, `doc/`, `examples/`, `bin/`,
`scripts/`, `setup.py`, `LICENSE`, `README.rst`, etc.).

## 4. Nested .git avoided
**Yes.** `test ! -d target_repo/luigi_buggy/.git` → `OK: no nested .git`. `.github` was also excluded.

## 5. Python file count
**244** Python files (`find target_repo/luigi_buggy -name "*.py" | wc -l`).

## 6. Python LOC
**58,636** total Python lines (`find … -name "*.py" -print0 | xargs -0 wc -l | tail -1`).
> Note: this counts the **whole** vendored tree (incl. `test/`, `doc/`, `examples/`). The core `luigi/`
> package is the focus for analysis; the full-tree counts are reported here for provenance and comfortably
> exceed the grade-100 size bar.

## 7. License / provenance files found
`target_repo/luigi_buggy/LICENSE` (Apache-2.0). No separate `NOTICE`/`COPYING` upstream. Provenance also
recorded in `target_repo/README.md`.

## 8. Confirmation no bug fix was applied
Vendored source is **pristine/buggy**:
- Buggy line present: `target_repo/luigi_buggy/luigi/parameter.py:1118` → `return literal_eval(x)`.
- Buggy guard present: line 1117 `except ValueError:` (within `TupleParameter.parse`, class at line 1066).
- Fixed pattern `except (ValueError, TypeError)` → **not present** (`none (good: not fixed)`).

## 9. Files changed / created in the assignment repo
- **Created:** `target_repo/luigi_buggy/**` (vendored source); `reports/target_repository_acquisition.md` (this file).
- **Updated:** `target_repo/README.md` (now documents the vendored source + policy change);
  `docs/DECISIONS.md` (D-007 vendoring decision); `docs/TODO.md` (Stage 4 → IN_PROGRESS, evidence noted).
- **Not touched:** all Luigi logic (no patches). `docs/PRD.md` left unchanged (out of this round's allowed edits).

## 10. Reconciliation status (resolved — all docs)
The vendoring policy is **approved and fully reconciled before the Stage-4 commit** (decision **D-007**).
Updated to match the vendored-and-tracked policy: `docs/PLAN.md` (§1 overview, §5 flow, §6 acquisition,
§18 fix policy, §22 security, §27 milestone, plus risk/gate rows), `docs/TODO.md` (rule R4 + Stage 4),
`target_repo/README.md`, `README.md`, `docs/DECISIONS.md` (D-007 with alternatives/tradeoff/guardrails),
`docs/PRD.md` (§8, §9, FR-01, §26, §28), and `docs/AI_WORKFLOW.md` (vendored-source handling policy).
**No residual policy contradiction remains.**

## 11. Status
Stage 4 acquisition performed and validated. **No commit and no push were made.** The vendored source is
currently **untracked** in git (`?? target_repo/luigi_buggy/`).
