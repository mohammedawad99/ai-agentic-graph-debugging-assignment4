# PRD — Product Requirements (PLACEHOLDER)

> Status: **placeholder**. Drafted and approved before implementation (see `docs/DECISIONS.md` D-006).

## Problem
Investigating and fixing a bug in an unfamiliar large Python codebase is token-expensive when done
naively. This project tests whether a **Graphify-derived code graph** makes an AI agent's bug
investigation more **token-efficient** and reliable.

## Goal (to be detailed)
Demonstrate, on **Luigi bug 3**, that a **graph-guided** agent locates and fixes the defect using
fewer tokens / files / iterations than a **baseline naive** agent, with verifiable before/after tests.

## Users
- Course graders; future engineers studying graph-guided debugging.

## In scope (to expand)
- Graphify graph of Luigi; Obsidian vault; LangGraph agent (baseline + graph-guided); real fix; token comparison.

## Out of scope (to expand)
- Fixing other Luigi bugs; modifying Luigi's architecture; production hardening.

## Success metrics (to finalize)
- Fix makes `TestSerializeTupleParameter::testSerialize` pass.
- Graph-guided run shows measurable reduction vs baseline (tokens / files read / iterations), labeled by provenance.

_To be completed in the PRD stage._
