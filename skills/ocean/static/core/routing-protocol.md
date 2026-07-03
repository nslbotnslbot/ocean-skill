# OCEAN Routing Protocol

Use the smallest module set that fits the request. Do not run all modules unless the task is an end-to-end workflow.

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
