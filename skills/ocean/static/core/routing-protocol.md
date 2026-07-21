# OCEAN Routing Protocol

Use the smallest module set that fits the request. Do not run all modules unless the task is an end-to-end workflow. For manuscript inputs, classify the lifecycle before routing modules.

## Manuscript lifecycle gate

| Cue | Mode | Route |
|---|---|---|
| finished passage plus revise, polish, shorten, translate, or improve wording | Manuscript Revision | silent bounded Iceberg check; clean replacement text plus separate notes only when needed |
| idea, proposal, experiment design, early draft, or explicit weakness finding | Design / Audit | smallest relevant module set; full route only for genuine end-to-end work |
| explicit reviewer simulation, full audit, or submission-readiness stress test | Pre-submission Stress Test | visible audit artifacts; replacement prose remains separate |
| reviewer/editor comments plus reply or revision request | Reviewer Response | separate response letter, revised manuscript text, and author-only notes |

Use `references/manuscript-revision-mode.md` for the full channel-isolation rules. A generic manuscript revision request must not trigger the standard seven-module chain.

## Module order

1. Sounding
2. Current
3. Reef
4. Iceberg
5. Anchor
6. Compass
7. Harbor

## Routing cues

| Cue | Primary module |
|---|---|
| source packet, DOI, preprint, public review, evidence discovery | Sounding |
| trend, field maturity, recent direction, hype vs consensus | Current |
| database, API, KG, cohort, benchmark, registry, omics/protein/drug resource | Reef |
| claim support, overclaim, causal/mechanism downgrade | Iceberg |
| validation, reproducibility, leakage, benchmark, external check, clinical readiness | Anchor |
| research plan, experiment design, journal strategy, idea prioritization | Compass |
| project memory, collaboration record, artifact ledger, report/workspace | Harbor |

## Handoff rules

- Handoff targets must be one of: Sounding, Current, Reef, Iceberg, Anchor, Compass, Harbor.
- If the next module needs evidence that is missing, state a stop condition instead of pretending to hand off.
- For retrieval-capable workflows, run the Retrieval Separation Gate before Current/Reef/Iceberg conclusions.
- For artifacts/logs/code/figures, run the Artifact Ledger Gate before Anchor/Compass/Harbor conclusions.
- In Manuscript Revision mode, do not expose module handoffs, critique labels, or evidence ledgers inside clean replacement prose.
