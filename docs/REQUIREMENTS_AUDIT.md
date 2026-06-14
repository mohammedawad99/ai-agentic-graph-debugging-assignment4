# Requirements Audit — Assignment 04 (Group MaRs-777)

Traceability of every known requirement to a planned location, validation method, grading risk, and current status.

**Status legend:** `DONE` (complete & evidenced) · `IN-PROGRESS` · `PLANNED` (not started) · `SKELETON` (placeholder created, content later).
**Honesty rule:** a row is only `DONE` when real evidence exists in-repo. No stage is claimed complete before it is.

| ID | Source / Category | Requirement | M/R | Planned file / location | Validation method | Grading risk if missed | Current status |
|----|-------------------|-------------|-----|--------------------------|-------------------|------------------------|----------------|
| R-01 | Submission | Public GitHub repository submission | M | repo root → GitHub remote | repo URL opens; graders can clone | Submission not received → 0 | PLANNED |
| R-02 | Submission | Group code `MaRs-777` visible | M | `README.md`, `docs/*` headers | grep group code in README | Identity/grouping penalty | DONE |
| R-03 | Selection | Selected Luigi/BugsInPy bug 3 with justification | M | `reports/repository_selection.md`, `docs/DECISIONS.md` (D-001) | decision doc + audit cross-ref | Weak/unsuitable target | DONE |
| R-04 | Selection | Meaningful size / grade-100 interpretation (~10k+ LOC, ~70+ files) | M | `reports/repository_selection.md` | LOC/file counts recorded (96 files / ~27.6k LOC at buggy commit) | Under-scoped → capped grade | DONE |
| R-05 | Reverse-eng | Target is an *unfamiliar* Python codebase | M | `target_repo/` (later), `reports/bug_analysis.md` | narrative of first-contact analysis | Looks pre-known → low RE credit | PLANNED |
| R-06 | Graphify | Graphify outputs produced | M | `artifacts/graphify/` | files exist + referenced in report | Core deliverable missing | PLANNED |
| R-07 | Graphify | `graph.json` present | M | `artifacts/graphify/graph.json` | file exists, valid JSON, node/edge counts | Core artifact missing | PLANNED |
| R-08 | Graphify | `GRAPH_REPORT.md` present | M | `artifacts/graphify/GRAPH_REPORT.md` | file exists, summarizes graph | Core artifact missing | PLANNED |
| R-09 | Obsidian | Obsidian vault with linked Markdown | M | `obsidian/` | internal `[[links]]` resolve | Knowledge-vault req missing | SKELETON |
| R-10 | Obsidian | `index.md` entry page | M | `obsidian/index.md` | file exists, links to pages | Vault navigation missing | SKELETON |
| R-11 | Obsidian | `hot.md` (hubs/hotspots) page | M | `obsidian/hot.md` | lists graph hubs/hotspots | Hotspot analysis missing | SKELETON |
| R-12 | Obsidian | Additional linked analysis pages | M | `obsidian/*.md` | multiple cross-linked pages | Thin vault → low marks | PLANNED |
| R-13 | Reverse-eng | Documented reverse engineering of the codebase | M | `reports/bug_analysis.md`, `obsidian/*` | structured RE write-up | Low RE credit | PLANNED |
| R-14 | Graph reading | Macro / meso / micro graph reading | M | `obsidian/*`, `GRAPH_REPORT.md` | three explicit zoom levels | Shallow graph use | PLANNED |
| R-15 | Diagrams | Block architecture diagram | M | `artifacts/diagrams/` + README | image/mermaid rendered in README | Architecture req missing | PLANNED |
| R-16 | Diagrams | OOP / class diagram | M | `artifacts/diagrams/` + README | class diagram of key types | OOP req missing | PLANNED |
| R-17 | Agent | AI agent workflow (LangGraph or CrewAI) | M | `src/ex04_graph_debugger/`, `docs/AI_WORKFLOW.md` | runnable workflow + docs | Central agentic req missing → major loss | PLANNED |
| R-18 | Agent | Graph-guided investigation path | M | `src/...`, `reports/token_efficiency.md` | agent consumes graph artifacts | No graph-guidance → weak thesis | PLANNED |
| R-19 | Agent | Baseline naive investigation path | M | `src/...`, `reports/token_efficiency.md` | baseline run recorded | No comparison baseline | PLANNED |
| R-20 | Debugging | Bug detection | M | `reports/bug_analysis.md` | agent/analysis locates defect | Debugging story incomplete | PLANNED |
| R-21 | Debugging | Root-cause explanation | M | `reports/bug_analysis.md` | written root cause w/ evidence | Shallow analysis | IN-PROGRESS |
| R-22 | Debugging | Real code fix | M | `target_repo/` patch + `reports/before_after.md` | diff applied, test passes | No real fix → major loss | PLANNED |
| R-23 | Debugging | Before/after proof | M | `reports/before_after.md`, `artifacts/validation/` | fail log + pass log captured | Unproven fix | IN-PROGRESS¹ |
| R-24 | Debugging | Failing test BEFORE fix | M | `reports/bug_validation.md`, `artifacts/validation/` | captured failing output | No regression proof | DONE¹ |
| R-25 | Debugging | Passing test AFTER fix | M | `reports/bug_validation.md` → final in `before_after.md` | captured passing output | No fix proof | DONE¹ |
| R-26 | Tokens | Token counts or estimates | M | `reports/token_efficiency.md`, `docs/COSTS.md` | labeled measured/estimated/manual | Efficiency claim unsupported | PLANNED |
| R-27 | Tokens | Number of files / text units read | M | `reports/token_efficiency.md` | per-run counters | Incomplete comparison | PLANNED |
| R-28 | Tokens | Number of iterations | M | `reports/token_efficiency.md` | per-run iteration counts | Incomplete comparison | PLANNED |
| R-29 | Tokens | Token-efficiency comparison report | M | `reports/token_efficiency.md` | baseline vs graph-guided table | Key thesis missing | PLANNED |
| R-30 | Originality | Original extension beyond minimum | M | `README.md` + `reports/final_audit.md` | named, implemented extension | No distinction for top grade | PLANNED |
| R-31 | Evidence | Screenshots / diagrams | M | `artifacts/screenshots/`, `artifacts/diagrams/` | images embedded in README | Unconvincing evidence | PLANNED |
| R-32 | Docs | README with full explanation | M | `README.md` | sections: context, workflow, root cause, fix, extensions | Poor first impression | IN-PROGRESS |
| R-33 | Docs | AI workflow documentation | M | `docs/AI_WORKFLOW.md` | policy + workflow described | Process opacity | DONE (policy)² |
| R-34 | Docs | Prompts documentation | M | `docs/PROMPTS.md` | summarized prompts per stage | Reproducibility gap | DONE (to-date)² |
| R-35 | Docs | Decisions documentation | M | `docs/DECISIONS.md` | D-001…D-006 recorded | Rationale opacity | DONE (to-date)² |
| R-36 | Docs | Cost / resource awareness | M | `docs/COSTS.md` | cost policy + labeling rule | Ignores efficiency framing | DONE (policy)² |
| R-37 | Quality | Quality gates defined & runnable | M | `docs/QUALITY.md`, `pyproject.toml` | gates listed; later run in CI/local | Sloppy engineering marks | DONE (defined)² |
| R-38 | Quality | uv usage | M | `pyproject.toml`, `docs/QUALITY.md`, README | `uv --version`; `uv run …` later | Not following course toolchain | DONE (config) |
| R-39 | Quality | Ruff lint/format | M | `pyproject.toml` `[tool.ruff]` | `uv run ruff check/format` later | Style/quality marks | SKELETON |
| R-40 | Quality | pytest test suite | M | `tests/`, `pyproject.toml` | `uv run pytest` later | No automated tests | SKELETON |
| R-41 | Quality | 150-line Python file rule | M | `docs/QUALITY.md`, custom gate | line-count check ≤150 over `src/` | Violates course rule | PLANNED (gate) |
| R-42 | Security | No secrets / API keys committed | M | `.gitignore`, `.env.example`, secret scan | scan finds no secrets | Security/process penalty | DONE |
| R-43 | Validation | Docker / Python 3.8 validation documented | M | `reports/bug_validation.md`, `config/default.toml` | command + version recorded | Reproducibility gap | DONE |
| R-44 | Honesty | No overclaiming / no fake evidence | M | all docs; `docs/QUALITY.md` gate | audit cross-check; status labels | Integrity penalty (severe) | DONE (ongoing) |
| R-45 | Audit | Final audit of submission | M | `reports/final_audit.md` | full requirement re-check before submit | Avoidable missed reqs | PLANNED |

**Footnotes**
1. ¹ **R-23/R-24/R-25:** the fail→pass cycle was *validated in the temporary candidate repo* (see `reports/bug_validation.md`). It is **not yet reproduced inside this final repo**; final before/after evidence lands in `reports/before_after.md` and `artifacts/validation/` during the debugging stage. Marked accordingly to avoid overclaiming.
2. ² **R-33…R-37:** the *policy / to-date content* exists now; these documents are appended as later stages produce real data (prompts, costs, gate runs).

## Coverage summary (current stage)
- **DONE (skeleton-appropriate):** R-02, R-03, R-04, R-24/R-25 (in candidate repo only), R-33, R-34, R-35, R-36, R-37, R-38, R-42, R-43, R-44.
- **IN-PROGRESS:** R-21, R-23, R-32.
- **SKELETON / PLANNED:** all remaining (Graphify, Obsidian analysis, diagrams, agent, token efficiency, extension, final audit).

No requirement is marked `DONE` without in-repo (or clearly-scoped candidate-repo) evidence.
