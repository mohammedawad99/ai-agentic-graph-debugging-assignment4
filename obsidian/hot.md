# Hot — Bug Context: `TupleParameter.parse`

The focused (micro) context for Luigi bug 3. All facts below are grounded in the vendored source and
`artifacts/graphify/graph.json`.

## Target
- **File:** `target_repo/luigi_buggy/luigi/parameter.py`
- **Class / method:** `TupleParameter.parse` (class `TupleParameter` @ **L1066**, method `.parse()` @ **L1095**)
- **Graph node:** `luigi_parameter_tupleparameter` (label `TupleParameter`); method node
  `luigi_parameter_tupleparameter_parse` (label `.parse()`).

## Buggy code (still present — NOT fixed)
From `luigi/parameter.py` (≈L1115–L1118):
```python
try:
    # loop required to parse tuple of tuples
    return tuple(tuple(x) for x in json.loads(x, object_pairs_hook=_FrozenOrderedDict))
except ValueError:                       # <-- buggy guard (too narrow)
    return literal_eval(x)               # <-- not wrapped in tuple(...)
```
- **Buggy pattern present:** `except ValueError:`
- **Fixed pattern must remain ABSENT in this repo:** `except (ValueError, TypeError)` — confirmed not applied.

## Known failing symptom (from earlier validation — candidate repo, Docker/Python 3.8.20)
- `TypeError: 'int' object is not iterable`
- Cause (validated earlier): `serialize((1,2,3))` → `"[1, 2, 3]"`; on parse, `json.loads` returns
  `[1,2,3]`, and `tuple(tuple(x) for x in …)` does `tuple(1)` → `TypeError`. The narrow `except ValueError`
  does not catch it, so it escapes.
- **Known fix (NOT applied here; reserved for Stage 10):** `except (ValueError, TypeError):` and
  `return tuple(literal_eval(x))`.

## Graph neighborhood (from `graph.json`, edges of the bug node)
- `TupleParameter` **inherits** `ListParameter` (`luigi_parameter_listparameter` @ L1006) — EXTRACTED
- `TupleParameter` **method** `.parse()` (`..._tupleparameter_parse` @ L1095) — EXTRACTED
- `TupleParameter` **uses** `CmdlineParser` (`luigi_cmdline_parser_cmdlineparser`) — INFERRED
- `luigi_parameter` (module) **contains** `TupleParameter` — EXTRACTED
- `luigi/__init__` **imports** `TupleParameter` — EXTRACTED

## Why the guard fails (Stage 7)
`serialize` (inherited from `ListParameter` = `json.dumps`) turns `(1,2,3)` into `"[1, 2, 3]"`; `parse`
then `json.loads` → `[1,2,3]` and runs `tuple(1)` on an int → `TypeError`. The `except ValueError:` is too
narrow to catch it. Full analysis: [[reverse-engineering-analysis]].

## Related pages
- [[reverse-engineering-analysis]] — Stage 7 macro→meso→micro.
- [[parameter-subsystem]] — the parameter class family (meso).
- [[bug-investigation-seed]] — what still needs proving in-repo.
- [[graphify-overview]] · [[architecture-map]] · [[index]]

> Reminder: the bug is **not** fixed in this repository. Before/after proof is a later, Docker-based stage.
