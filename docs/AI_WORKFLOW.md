# AI Workflow & Responsibility Policy — Assignment 04 (MaRs-777)

## Role of AI in this project
AI (Claude Code) assists across the lifecycle: **planning, repository selection, codebase analysis,
validation, and later implementation** of the Graphify post-processing, the Obsidian vault, the
agent workflow, and the bug fix. AI is a tool that accelerates and structures the work.

## Human responsibility (non-negotiable)
- The **student remains fully responsible** for every artifact and claim in this repository.
- **All AI output is reviewed by the student before it is committed.**
- **No commit is made before review.**
- **No unverified claim is accepted.** Statements of fact (test results, token counts, graph metrics)
  must be backed by in-repo evidence and labeled by provenance.
- AI-suggested code is read, understood, and tested before it is trusted.

## Where AI is used per stage
| Stage | AI assistance | Human verification |
|-------|---------------|--------------------|
| Selection / re-selection | inspect candidates, score, draft reports | confirm counts, accept final pick |
| Validation | run Docker fail→pass, capture logs | confirm reverted pristine state |
| Skeleton + audit (now) | scaffold files, draft requirement mapping | review structure & wording |
| Graphify | run tool, summarize graph | sanity-check nodes/edges vs source |
| Obsidian | draft linked pages | verify links + technical accuracy |
| Agent workflow | implement baseline & graph-guided runs | review code, re-run, inspect logs |
| Fix + before/after | propose patch, run tests | confirm diff + pass/fail logs |
| Token efficiency | tabulate counts | confirm provenance labels |

## Evidence & honesty rules
1. Every metric is labeled **measured**, **estimated**, or **manual count** (see `docs/COSTS.md`).
2. No stage is reported complete until its real artifacts exist in the repo (see `docs/REQUIREMENTS_AUDIT.md` status labels).
3. No fabricated screenshots, logs, graphs, or prompts.
4. No self-assigned grade.
5. Quality gates (`docs/QUALITY.md`) run before submission; failures are fixed, not hidden.

## Commit discipline
- Work happens on a branch; nothing is committed or pushed without explicit student review and approval.
- Generated heavy artifacts are git-ignored or stored deliberately. The target source is **vendored** under `target_repo/luigi_buggy/` (tracked, Apache-2.0, LICENSE/provenance preserved, upstream `.git` excluded; **D-007**).

## Vendored-source handling policy (D-007)
- The vendored Luigi source is kept **pristine** at the buggy commit `a0f1db01…`.
- AI assistance may **inspect** the vendored source only through the planned stages (Graphify, Obsidian, reverse engineering, agent investigation) and **must not silently modify it**.
- **Any** change to the vendored source must be **stage-gated and documented**: source edits are **forbidden before the Stage 10 bug-fix stage**, where the minimal fix is applied and captured as controlled before/after **diffs and logs**.
- A patch demonstrated during validation is reverted so the analyzed tree stays the exact buggy version unless Stage 10 deliberately applies it.
