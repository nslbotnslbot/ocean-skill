# OCEAN Module Map

OCEAN is scoped to biomedical research: medical research and biological research, with special attention to medical AI and biological AI workflows. The modules are ordered so that each one completes a distinct evidence-review event and produces a handoff artifact.

## Module Responsibilities

| Order | Module | Event completed | Typical inputs | Typical outputs | Stop condition |
|---:|---|---|---|---|---|
| 1 | Sounding | Evidence discovery and source-boundary setup | DOI, preprint, paper title, manuscript, public review, database seed, claim | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket | No traceable source, no accessible evidence, or only abstract-level material for a stronger claim |
| 2 | Current | Field trend and direction-flow analysis | Source packets, recent papers, review signals, benchmark movement | Trend map, direction-flow notes, opportunity/risk map | Search coverage is insufficient for trend claims |
| 3 | Reef | Biomedical resource and KG/database organization | KG links, databases, ontologies, cohorts, benchmarks, registries | Resource provenance map, database/KG evidence table, circularity risks | Resource provenance or evidence type cannot be verified |
| 4 | Iceberg | Claim-evidence audit under the surface claim | Source packet, manuscript claims, figures/tables, review concerns | Claim-evidence matrix, support verdict, downgraded claim rewrites | Key evidence is missing or the claim requires unavailable validation |
| 5 | Anchor | Validation, replication, leakage, benchmark, and reproducibility planning | Claim-evidence gaps, model results, datasets, code/protocol notes | Validation checklist, benchmark/leakage plan, reproducibility risks | Validation target or available materials are not defined |
| 6 | Compass | Research planning and strategic decision-making | Evidence gaps, reviewer concerns, trend map, validation plan | Idea card, experiment plan, journal strategy, collaboration route | Evidence is too thin for strategy beyond next-source collection |
| 7 | Harbor | Review report preservation and collaboration boundary memory | Module outputs, decisions, contribution notes, final review notes | Final audit report, decision note, contribution boundary record | User does not want persistent reporting or collaboration record |

## Module Reference Files

Detailed execution rules live in `skills/ocean/references/`:

- `sounding.md`: evidence discovery and source packets.
- `current.md`: field movement and trend-boundary scans.
- `reef.md`: resource, database, KG, benchmark, and provenance maps.
- `iceberg.md`: claim-evidence audit and safe rewrites.
- `anchor.md`: validation, leakage, benchmark, and reproducibility planning.
- `compass.md`: research planning, idea cards, and strategy routes.
- `harbor.md`: final reports, decision memos, and collaboration-boundary memory.

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
| Sounding | Tested most heavily; M2 screened | R1 API slice, R2/R3 article-error matrices, M1 all-module coverage, and M2 heuristic scoring | Manual source-grounded review of flagged M2 rows |
| Iceberg | Initial standalone coverage plus M2 screen | Anti-hallucination rounds, M1 Iceberg cases, and M2 heuristic scoring | Full-paper/figure-level claim-evidence audit eval |
| Current | Initial standalone coverage plus M2 screen | M1 Current cases and M2 heuristic scoring using bounded source sets | Time-bounded trend eval with live/public search protocol |
| Reef | Initial standalone coverage plus M2 screen | M1 Reef cases and M2 heuristic scoring using resource/provenance traps | KG/database provenance eval with real resource records |
| Anchor | Initial standalone coverage plus M2 screen | M1 Anchor cases and M2 heuristic scoring using validation-plan prompts | Deeper validation-plan scoring for clinical and wet-lab follow-up |
| Compass | Initial standalone coverage plus M2 screen | M1 Compass cases and M2 heuristic scoring using review-to-idea and evidence-gap prompts | Review-to-idea scoring with real public review text |
| Harbor | Initial standalone coverage plus M2 screen | M1 Harbor cases and M2 heuristic scoring using report/memory and collaboration-boundary prompts | Report persistence and collaboration-boundary scoring |

## Practical Interpretation

At the current release stage, OCEAN should be presented as a biomedical claim-evidence workflow whose most heavily tested component remains Sounding. M1 adds initial coverage testing for all seven modules, and M2 adds a first-pass heuristic scoring screen over those outputs. This is still not final scientific correctness validation or a model leaderboard.
