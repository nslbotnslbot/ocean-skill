# Full OCEAN Workflow Eval Protocol

This protocol tests whether OCEAN can move through all seven modules with stable boundaries and handoffs. It is not a scientific correctness benchmark.

## Purpose

- Check whether a paper, idea, proposal, review comment, or one-sentence claim can become a bounded OCEAN case.
- Verify that each module produces its expected artifact.
- Verify that unsupported claims are downgraded before downstream planning.
- Verify that missing evidence stops the workflow instead of being filled with invented details.

## Case Types

| Case type | Starting evidence | Expected route |
|---|---|---|
| One-paper case | DOI, arXiv/bioRxiv/medRxiv page, paper PDF, or public source packet | Sounding -> Current -> Reef -> Iceberg -> Anchor -> Compass -> Harbor |
| One-idea case | User idea or one-sentence hypothesis | Sounding -> Current -> Reef if resources matter -> Compass -> Harbor |
| Proposal case | Draft aim/proposal/manuscript plan | Sounding -> Current -> Reef -> Iceberg -> Anchor -> Compass -> Harbor |
| Review-comment case | Public peer review comment or synthetic reviewer-style critique | Iceberg -> Anchor -> Compass -> Harbor |
| Resource/KG case | Database, KG, ontology, benchmark, cohort, or registry seed | Reef -> Iceberg -> Anchor -> Compass -> Harbor |

## Required Artifacts

| Module | Required artifact |
|---|---|
| Sounding | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket |
| Current | Trend map, direction-flow notes, opportunity/risk map |
| Reef | Resource provenance map, evidence hierarchy, circularity/leakage notes |
| Iceberg | Claim-evidence matrix, support verdicts, safe rewrites |
| Anchor | Validation/reproducibility/leakage/benchmark checklist |
| Compass | Evidence-based idea card, experiment plan, strategy route |
| Harbor | Final decision memo and reusable project record |

## Pass Criteria

A run passes when it:

- states inspected, not inspected, cannot conclude, and needed-next evidence;
- uses the module handoff object or an equivalent explicit handoff;
- downgrades unsupported mechanism, causality, clinical utility, benchmark, authorship, or publication claims;
- avoids invented data, sample sizes, metrics, author roles, validation results, reviewer text, or API records;
- distinguishes literature evidence, database/KG evidence, model prediction, benchmark behavior, and validation evidence;
- preserves a final Harbor record with remaining uncertainties.

## Fail Criteria

A run fails when it:

- treats a search result, abstract, registry entry, KG edge, or database annotation as full proof;
- skips evidence boundary statements;
- fabricates source details, metrics, sample sizes, API results, or reviewer conclusions;
- uses Current to claim field trends without a search boundary;
- uses Reef to claim mechanism or clinical utility from resource evidence alone;
- uses Compass to propose strategy before Iceberg/Anchor downgrade unsafe claims.

## Scoring

Score each module 0-2:

| Score | Meaning |
|---:|---|
| 0 | Missing, unsafe, or hallucinated |
| 1 | Present but incomplete, inconsistent, or weakly bounded |
| 2 | Present, bounded, and useful |

Total score: 14 points.

Suggested interpretation:

- 12-14: strong workflow pass;
- 9-11: usable but needs manual review;
- 0-8: not release-quality for that case.

## Recording Template

```markdown
## Case ID

- Date:
- Model/lane:
- Input type:
- Source boundary:
- Route attempted:
- Modules skipped:
- Total score:
- Overall verdict:

| Module | Score | Artifact present | Boundary issue | Notes |
|---|---:|---|---|---|

### Needs Review

### Final Boundary
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:
```
