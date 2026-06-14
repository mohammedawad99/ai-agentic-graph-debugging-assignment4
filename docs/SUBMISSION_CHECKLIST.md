# Submission Checklist — Assignment 04 (MaRs-777)

Tick only when real, in-repo evidence exists. Mirrors `docs/REQUIREMENTS_AUDIT.md`.

## Identity & submission
- [ ] Public GitHub repo created and pushed (R-01)
- [x] Group code `MaRs-777` present in README/docs (R-02)
- [ ] Final submission link recorded

## Selection & validation
- [x] Luigi bug 3 selected with justification (R-03)
- [x] Size / grade-100 interpretation documented (R-04)
- [x] Docker / Python 3.8 validation documented (R-43)
- [x] Failing-before captured in candidate repo (R-24)¹
- [x] Passing-after captured in candidate repo (R-25)¹
- [ ] Before/after reproduced inside final repo (R-23)

## Graphify
- [ ] Graphify run produced outputs (R-06)
- [ ] `graph.json` present (R-07)
- [ ] `GRAPH_REPORT.md` present (R-08)

## Obsidian vault
- [ ] `index.md` complete (R-10)
- [ ] `hot.md` complete (R-11)
- [ ] Linked analysis pages, macro/meso/micro (R-12, R-14)

## Reverse engineering & diagrams
- [ ] RE write-up (R-05, R-13)
- [ ] Block architecture diagram (R-15)
- [ ] OOP / class diagram (R-16)

## Agent workflow & debugging
- [ ] Agent workflow (LangGraph/CrewAI) runs (R-17)
- [ ] Graph-guided path (R-18)
- [ ] Baseline naive path (R-19)
- [ ] Bug detection + root cause (R-20, R-21)
- [ ] Real fix applied (R-22)
- [ ] Before/after proof in repo (R-23)

## Token efficiency
- [x] Token counts (labeled `estimated` via chars/4) (R-26) — baseline 24,482 vs graph-guided 3,631
- [x] Files/text units read (R-27) — baseline 4/4 vs graph-guided 5/7
- [x] Iteration counts (R-28) — baseline 5 rounds vs graph-guided 8 states
- [x] Comparison report (R-29) — `reports/token_efficiency.md` (+ JSON/CSV) — commit `dad0413`

## Polish & integrity
- [x] Original extension (R-30) — centrality-based suspect ranking (`reports/original_extension.md`); commit pending
- [ ] Screenshots/diagrams embedded (R-31)
- [x] README scaffold with required sections (R-32, in progress)
- [x] AI workflow doc (R-33)
- [x] Prompts doc (R-34)
- [x] Decisions doc (R-35)
- [x] Costs doc (R-36)
- [x] Quality gates defined (R-37)
- [x] uv configured (R-38)
- [ ] Ruff clean (R-39)
- [ ] pytest green (R-40)
- [ ] 150-line rule enforced (R-41)
- [x] No secrets committed (R-42)
- [x] No overclaiming (R-44, ongoing)
- [ ] Final audit complete (R-45)

¹ Validated in the temporary candidate repo only; final-repo reproduction still pending (no overclaiming).
