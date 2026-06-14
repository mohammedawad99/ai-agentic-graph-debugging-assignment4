# Parameter Subsystem (meso)

The parameter class family around the bug, grounded in `graph.json` and `luigi/parameter.py`.
`luigi/parameter.py` contributes **111 code nodes** to the graph.

## Inheritance chain to the bug (grounded — EXTRACTED edges)
```
Parameter (luigi_parameter_parameter, L93)
   └── ListParameter (luigi_parameter_listparameter, L1006)
          └── TupleParameter (luigi_parameter_tupleparameter, L1066)   ← bug class
                   └── .parse()  (luigi_parameter_tupleparameter_parse, L1095)  ← bug method
```
- `TupleParameter` **inherits** `ListParameter` — EXTRACTED edge in `graph.json`.
- `ListParameter.parse` exists at L1046 (`luigi_parameter_listparameter_parse`); `TupleParameter.parse`
  overrides/extends parsing at L1095.

## Selected parameter nodes (grounded, from `luigi/parameter.py`)
| node id | label | line |
|---------|-------|-----:|
| `luigi_parameter_parameter` | `Parameter` | L93 |
| `luigi_parameter_listparameter` | `ListParameter` | L1006 |
| `luigi_parameter_listparameter_parse` | `.parse()` | L1046 |
| `luigi_parameter_tupleparameter` | `TupleParameter` | L1066 |
| `luigi_parameter_tupleparameter_parse` | `.parse()` | L1095 |
| `luigi_parameter_parametervisibility` | `ParameterVisibility` | L48 |
| `luigi_parameter_parameterexception` | `ParameterException` | L65 |

(Also present in the file: `DictParameter`, `IntParameter`, `FloatParameter`, `BoolParameter`,
`ChoiceParameter`, `_FrozenOrderedDict`, `_DictParamEncoder` — several appear in **Community 58**, see
[[graph-communities]].)

## Community placement (grounded)
- `ListParameter`, `DictParameter`, `_FrozenOrderedDict`, `_DictParamEncoder`, `JSONEncoder` appear in
  **Community 58** of `GRAPH_REPORT.md` (cohesion 0.06) — the serialization/parameter cluster.
- The bug node also has an INFERRED `uses` edge to `CmdlineParser` (**Community 1**), reflecting that
  parameter values can arrive from the command line.

## Why this subsystem matters for the bug
`TupleParameter.parse` round-trips serialized values back to tuples. The defect is in its exception
handling (see [[hot]]). Parsing also interacts with config/CLI inputs, which is why the graph links it to
the cmdline parser.

## Stage 7 finding (grounded)
`TupleParameter` **overrides `parse` only** and **inherits `ListParameter.serialize` (`json.dumps`)** —
there is no `serialize` node for it in `graph.json`. This serialize/parse **asymmetry** is the structural
root of the bug. `ListParameter.parse` (L1046) returns `list(json.loads(...))`; `TupleParameter.parse`
(L1095) wraps it as a tuple-of-tuples, which breaks on a flat list of ints. Full write-up:
[[reverse-engineering-analysis]].

## Source / links
- Source: `target_repo/luigi_buggy/luigi/parameter.py`
- [[reverse-engineering-analysis]] · [[hot]] · [[architecture-map]] · [[graph-communities]] · [[index]]

*Deeper call-path tracing (exact callers of `parse`, config readers) remains for Stage 8/9; the
parameter→CLI edge is INFERRED.*
