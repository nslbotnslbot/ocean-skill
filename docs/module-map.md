# OCEAN Module Map

OCEAN is scoped to biomedical research: medical research and biological research, with special attention to medical AI and biological AI workflows. The modules are ordered so that each one completes a distinct event and produces a handoff artifact.

## Module Responsibilities

| Order | Module | Event completed | Typical inputs | Typical outputs | Stop condition |
|---:|---|---|---|---|---|
| 1 | Sounding | Evidence discovery and source-boundary setup | DOI, preprint, paper title, manuscript, public review, database seed, claim | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket | No traceable source, no accessible evidence, or only abstract-level material for a stronger claim |
| 2 | Current | Field trend and direction-flow analysis | Source packets, recent papers, review signals, benchmark movement | Trend map, direction-flow notes, opportunity/risk map | Search coverage is insufficient for trend claims |
| 3 | Reef | Biomedical resource and KG/database organization | KG links, databases, ontologies, cohorts, benchmarks, registries | Resource provenance map, database/KG evidence table, circularity risks | Resource provenance or evidence type cannot be verified |
| 4 | Iceberg | Claim-evidence audit under the surface claim | Source packet, manuscript claims, figures/tables, review concerns | Claim-evidence matrix, support verdict, downgraded claim rewrites | Key evidence is missing or the claim requires unavailable validation |
| 5 | Anchor | Validation, replication, leakage, benchmark, and reproducibility planning | Claim-evidence gaps, model results, datasets, code/protocol notes | Validation checklist, benchmark/leakage plan, reproducibility risks | Validation target or available materials are not defined |
| 6 | Compass | Research planning and strategic decision-making | Evidence gaps, reviewer concerns, trend map, validation plan | Idea card, experiment plan, journal strategy, collaboration route | Evidence is too thin for strategy beyond next-source collection |
| 7 | Harbor | Report preservation and collaboration memory | Module outputs, decisions, contribution records, final notes | Final report, workspace log, contribution boundary record | User does not want persistent reporting or collaboration record |

## Biomedical Claim Types

OCEAN should be especially careful with these biomedical claim transitions:

- Benchmark improvement does not by itself prove clinical utility.
- Database or KG association does not by itself prove mechanism.
- Foundation-model embeddings do not by themselves prove biological causality.
- Retrospective internal validation does not by itself prove deployment readiness.
- Public review, peer review, or assessment language is a pressure signal, not experimental evidence.
- Omics association requires additional evidence before mechanism, perturbation, or therapeutic claims.

## Current Validation Status

| Module | Current status | Evidence in repository | Next recommended eval |
|---|---|---|---|
| Sounding | Tested most heavily | R1 API slice, R2 8-article x 6-error matrix, R3 10-article x 6-error matrix, multi-model coverage files | Add content-level scoring beyond coverage |
| Iceberg | Partially and indirectly tested | Anti-hallucination, claim downgrade, contamination-resistance rounds | Standalone claim-evidence audit eval with full papers/figures |
| Current | Designed only | Module routing in `SKILL.md`; no standalone eval yet | Trend-analysis eval using a time-bounded biomedical topic |
| Reef | Designed only | Module routing in `SKILL.md`; KG/database cautions in eval prompts | KG/database provenance eval with known circularity traps |
| Anchor | Designed only | Module routing in `SKILL.md`; validation/leakage language in output contract | Validation-plan eval for clinical prediction and wet-lab follow-up |
| Compass | Designed only | Module routing in `SKILL.md`; planning/journal strategy output contract | Review-to-idea and experiment-planning eval |
| Harbor | Designed only | Module routing in `SKILL.md`; report skeleton scripts | Report persistence and collaboration-boundary eval |

## Practical Interpretation

At the current release stage, OCEAN should be presented as a biomedical claim-evidence workflow whose strongest tested component is Sounding. The rest of the module sequence is intentional product structure and should be expanded with module-specific evals before making strong claims about those modules.
