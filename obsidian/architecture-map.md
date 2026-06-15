# Architecture Map

A macro map of the Luigi codebase, grounded in `graph.json` node counts and source paths. It is the
orientation layer of the vault; the full analysis is in [[reverse-engineering-analysis]] /
`reports/reverse_engineering.md`.

## Where the code mass is (grounded — top code files by node count in `graph.json`)
| nodes | source file | role (from path/source) |
|------:|-------------|--------------------------|
| 207 | `test/scheduler_api_test.py` | scheduler API tests |
| 185 | `luigi/static/visualiser/lib/d3/d3.min.js` | vendored JS lib (web UI) |
| 180 | `test/parameter_test.py` | **parameter tests (incl. the bug's regression test)** |
| 163 | `test/worker_test.py` | worker tests |
| 135 | `luigi/scheduler.py` | **scheduler core** |
| 111 | `luigi/parameter.py` | **parameter system — bug lives here** |
| 108 | `test/range_test.py` | range tests |
| 83 | `luigi/format.py` | I/O formats |
| 79 | `luigi/worker.py` | **worker core** |

> Reading: the runtime core clusters around **`scheduler.py`**, **`worker.py`**, **`parameter.py`**, and
> `task.py` (the DAG/scheduling engine), while a large share of nodes are **tests** and vendored web-UI JS.

## Core runtime subsystems
- **Parameters** → [[parameter-subsystem]] (`luigi/parameter.py`) — **bug location**.
- **Tasks / registry** (`luigi/task.py`, `luigi/task_register.py`) — task model & registration — INFERRED from module grouping.
- **Scheduler** (`luigi/scheduler.py`) — DAG scheduling core (high degree, see [[graph-communities]]) — EXTRACTED.
- **Worker / execution** (`luigi/worker.py`) — task execution — EXTRACTED.
- **CLI / cmdline** (`luigi/cmdline_parser.py`) — connected to the bug node via an INFERRED `uses` edge.
- **Web UI / static** (`luigi/static/…`) — non-core assets; mostly excluded from the bug analysis.

## Hub reading
A degree-based hub ranking (see [[graph-communities]]) shows the runtime center is the
**scheduler/worker** core (`scheduler` deg≈137), while the very top God-nodes are **vendored d3 JS libs**
(a measurement artifact, not core logic). Full analysis: [[reverse-engineering-analysis]]. The block
diagram for this map is `artifacts/diagrams/architecture_block.mmd`.

## Pointers
- Full reverse-engineering analysis: [[reverse-engineering-analysis]]
- Community/hub view: [[graph-communities]]
- Bug context: [[hot]]
- How the graph was built: [[graphify-overview]]
- Provenance: [[sources]]

*Every claim above is tagged EXTRACTED (from `graph.json`/source) or INFERRED (reasoned from those facts).*
