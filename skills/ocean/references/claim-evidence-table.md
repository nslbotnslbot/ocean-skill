# Claim-Evidence Table

Use this schema to audit every important scientific claim. Include direct claims from the manuscript and implied claims from titles, abstracts, figures, highlights, graphical summaries, and cover letters.

| ID | Claim | Claim type | Evidence source | Evidence type | Directness | Causality level | Support level | Novelty status | Validation status | Missing validation | Risk | Suggested rewrite |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|
| C1 | Example: Model X discovers mechanism Y in disease Z | mechanism / discovery | Fig. 3, Table S2 | computational + literature | 3/5 | 2/5 | 2/5 | unclear | not externally validated | independent experiment, external data | causal overstatement | Model X prioritizes a hypothesis linking Y to disease Z |

## Claim Type Options

- mechanism
- performance
- generalization
- clinical utility
- resource coverage
- database evidence
- workflow/system capability
- biological discovery
- benchmark superiority
- reproducibility
- collaboration contribution

## Evidence Type Options

- experimental human
- experimental animal
- cell line
- clinical cohort
- external validation dataset
- internal validation
- retrospective database
- curated database
- text mining
- literature review
- model prediction
- expert annotation
- case study
- user study
- code/demo only

## Score Meaning

- Directness: 1 means indirect or proxy-only evidence; 5 means the evidence directly tests the claim.
- Causality level: 1 means association or prediction only; 5 means causal mechanism is directly tested with appropriate intervention or experimental support.
- Support level: 1 means unsupported or anecdotal; 5 means strong, independently validated, reproducible support.

## Rewrite Rule

When support or causality is weak, rewrite strong claims as cautious claims:

- "discovers a mechanism" -> "prioritizes a hypothesis"
- "generalizes clinically" -> "shows internal validation and needs external validation"
- "proves therapeutic effect" -> "suggests a candidate relationship requiring experimental validation"
- "database confirms" -> "database records or literature-mining evidence are consistent with"
