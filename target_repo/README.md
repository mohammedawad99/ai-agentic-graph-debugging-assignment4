# target_repo/

Holds the **vendored Luigi source** under investigation for Assignment 04.

## Current contents
- **`luigi_buggy/`** — the Luigi source at the **buggy commit**
  `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`, vendored into this repo (Stage 4 acquisition).
  The upstream `.git` and `.github` were **excluded**; no nested git repository exists here.
  Upstream `LICENSE` (Apache-2.0) is preserved at `luigi_buggy/LICENSE`.

## Vendoring policy (updated)
- This source is **vendored as evidence** so graders/Graphify can read the exact target without
  re-cloning. This is a deliberate change from the earlier "git-ignore the raw source" note — see
  `docs/DECISIONS.md` **D-007**.
- The vendored source is kept **pristine**: no bug fix and no patches are applied here. The buggy line
  remains at `luigi_buggy/luigi/parameter.py:1118` (`return literal_eval(x)`).
- Faithful runs/tests against this source use **Docker `python:3.8-slim`** (see `docs/DECISIONS.md` D-005).
- Our own derived artifacts (graphs, notes, diffs, logs) live in `artifacts/`, `obsidian/`, `reports/`.

## Provenance
- Upstream project: Luigi — https://github.com/spotify/luigi
- Dataset: BugsInPy → project `luigi`, bug `3`
- Buggy commit (vendored here): `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`
- Fixed commit (regression-test overlay source, later stage): `3a0bfbff69addfb3be1107adab3d4914bcae3e4b`
- File / symbol under investigation: `luigi/parameter.py` → `TupleParameter.parse`
- Acquisition method & verification: see `reports/target_repository_acquisition.md`.
