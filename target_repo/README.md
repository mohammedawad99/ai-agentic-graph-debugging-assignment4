# target_repo/ — placeholder

The **Luigi** source (at buggy commit `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`) will be placed
here in a later stage (PLAN step 3). **It is not present yet** and is **not cloned in this stage.**

## Rules
- The raw cloned source is **git-ignored** (see `.gitignore`: `target_repo/luigi/`) and **never committed raw**.
- Only our own derived artifacts (graphs, notes, diffs) are committed, in `artifacts/`, `obsidian/`, `reports/`.
- Faithful runs/tests against this source use **Docker `python:3.8-slim`** (see `docs/DECISIONS.md` D-005).

## Provenance (for the later clone)
- Upstream: https://github.com/spotify/luigi
- Dataset: BugsInPy → project `luigi`, bug `3`
- Buggy commit: `a0f1db01ddab5b4b2bda3fbe58bad09a6d94a7b4`
- Fixed commit (for regression-test overlay): `3a0bfbff69addfb3be1107adab3d4914bcae3e4b`
- File/symbol under investigation: `luigi/parameter.py` → `TupleParameter.parse`
