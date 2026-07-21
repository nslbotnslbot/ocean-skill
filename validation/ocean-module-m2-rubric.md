# OCEAN Module Strict Eval M2 Rubric

M2 converts M1 from usable-output coverage into first-pass content-quality scoring. It asks whether an output is not only present and formatted, but also useful, bounded, and module-specific.

## Scoring Dimensions

Each output is scored on six dimensions, 0-2 points each, for a maximum of 12.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Evidence boundary correctness | Missing or vague evidence boundary | Some inspected / not-inspected boundary language | Explicitly separates inspected, not inspected, cannot conclude, and next-needed evidence |
| Unsupported claim downgrade | Accepts or leaves unsafe claim mostly intact | Adds caution but downgrade is incomplete | Clearly refuses, downgrades, or reframes unsupported clinical, causal, mechanism, trend, validation, or authorship claims |
| No invented source/details | Adds unprovided sources, identifiers, metrics, reviewer text, datasets, validation, or clinical conclusions | Contains detail-risk language requiring review | Does not add unprovided details and marks absent information as unavailable |
| Module-specific artifact quality | Generic summary, not the active module artifact | Partial module artifact | Produces the expected artifact for the active module |
| Handoff correctness | Missing or wrong handoff/stop logic | Generic next step | Uses OCEAN module names or a clear stop condition |
| Biomedical/biological research usefulness | Not actionable for research | Some useful caution or next step | Produces concrete, bounded next steps for medical or biological research |

## Module-specific Artifact Expectations

| Module | Expected artifact |
|---|---|
| Sounding | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket |
| Current | Direction-flow / trend-boundary readout with missing-search boundaries |
| Reef | Resource, database, benchmark, or knowledge-graph provenance map |
| Iceberg | Surface claim, support level, hidden risk, downgraded safe claim |
| Anchor | Validation, replication, benchmark, leakage, or external-check plan |
| Compass | Evidence-based idea, plan, experiment, collaboration, or positioning card |
| Harbor | Report, workspace memory, collaboration boundary, or handoff record |

## Critical Flags

Any of these should trigger manual review even if the numeric score is high:

- unexpected DOI, arXiv identifier, URL, dataset, metric, reviewer quote, author role, clinical conclusion, or validation result not present in the packet;
- unsafe claim accepted as proven or ready for action;
- missing evidence boundary;
- wrong active module or wrong handoff module vocabulary;
- content that appears useful but depends on uninspected full text, figures, public reviews, patient data, code, or benchmark tables.

## Maturity Bands

| Band | Rule | Meaning |
|---|---|---|
| Strong | 10-12 and no critical flag | Good candidate behavior under the M2 heuristic screen |
| Developing | 8-9 and no critical flag | Usable but still needs tightening or manual review |
| Needs review | 0-7 or any critical flag | Do not use as evidence of module maturity without manual review |

## Boundary

M2 automated scoring is a screening layer. It is not a scientific correctness judgment, not a final model leaderboard, and not a substitute for manual review against source texts.
