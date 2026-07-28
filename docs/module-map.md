# OCEAN Module Map

OCEAN is scoped to biomedical research: medical research and biological research, with special attention to medical AI and biological AI workflows. The modules are ordered so that each one completes a distinct evidence-review event and produces a handoff artifact.

For research design tasks, the seven modules form a design loop: domain lens -> evidence boundary -> source/resource packet -> claim calibration -> validation gate -> research route -> decision memory.

## Module Responsibilities

| Order | Module | Event completed | Typical inputs | Typical outputs | Stop condition |
|---:|---|---|---|---|---|
| 1 | Sounding | Evidence discovery and source-boundary setup | DOI, preprint, paper title, manuscript, public review, database seed, claim | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket | No traceable source, no accessible evidence, or only abstract-level material for a stronger claim |
| 2 | Current | Field trend and direction-flow analysis | Source packets, recent papers, review signals, benchmark movement | Trend map, direction-flow notes, opportunity/risk map | Search coverage is insufficient for trend claims |
| 3 | Reef | Biomedical resource, clinical data, and KG/database organization | KG links, databases, ontologies, omics resources, cell atlases, cohorts, benchmarks, registries, clinical datasets | Resource provenance map, biological/clinical data-source routing, database/KG evidence table, circularity risks | Resource provenance, access boundary, or evidence type cannot be verified |
| 4 | Iceberg | Claim-evidence audit under the surface claim | Source packet, manuscript claims, figures/tables, review concerns | Claim-evidence matrix, support verdict, downgraded claim rewrites | Key evidence is missing or the claim requires unavailable validation |
| 5 | Anchor | Validation, replication, leakage, benchmark, and reproducibility planning | Claim-evidence gaps, model results, datasets, code/protocol notes | Validation checklist, benchmark/leakage plan, reproducibility risks | Validation target or available materials are not defined |
| 6 | Compass | Research planning and strategic decision-making | Evidence gaps, reviewer concerns, trend map, validation plan | Idea card, experiment plan, journal strategy, collaboration route | Evidence is too thin for strategy beyond next-source collection |
| 7 | Harbor | Review report preservation and collaboration boundary memory | Module outputs, decisions, contribution notes, final review notes | Final audit report, decision note, contribution boundary record | User does not want persistent reporting or collaboration record |

## Module Reference Files

Detailed execution rules live in `skills/ocean/references/`:

- `sounding.md`: evidence discovery and source packets.
- `domain-lens.md`: biomedical domain fingerprint, evidence standards, highest safe claim level, and module routing.
- `data-tool-router.md`: public data/resource/API source-class routing, data/tool packets, and access/privacy/licensing boundaries.
- `module-artifact-contract.md`: required artifacts and quality gates for each OCEAN module.
- `module-handoff.md`: explicit handoff tickets for full OCEAN workflows and multi-module routes.
- `project-start-gate.md`: project-start trigger rules, Project Start Card, Harbor seed, and GitHub Sync Ticket for persistent project records.
- `research-design-workflow.md`: design gates and research-route selection for idea, proposal, reviewer-pressure, resource, and collaboration workflow cases.
- `current.md`: field movement and trend-boundary scans.
- `reef.md`: resource, database, KG, benchmark, and provenance maps.
- `reef-biological-data-sources.md`: biological and clinical data-source routing with identifier, access, privacy, licensing, and evidence-level boundaries.
- `reef-api-adapters.md`: optional API adapter planning for official biomedical databases, registries, and resource tools.
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
