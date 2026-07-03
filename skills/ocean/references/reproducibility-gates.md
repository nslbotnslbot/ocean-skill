# Reproducibility Gates

Use these gates when a project, figure, analysis, AI model, or manuscript claims reproducibility, validation, benchmark strength, or clinical readiness.

## Minimum reproducibility gate

| Gate | Pass condition | Fail / cannot judge condition |
|---|---|---|
| Data identity | accession/path/checksum/version recorded | file name only or undocumented data |
| Code identity | script/notebook inspected with commit/version | code name only |
| Environment | package versions, OS/container/conda/pip lock available | no version record |
| Parameters | preprocessing/model/plot parameters recorded | implicit defaults or missing settings |
| Randomness | seeds and stochastic steps recorded | no seed or nondeterministic pipeline |
| Execution | log/status plus warnings/errors inspected | completion line only |
| Output lineage | figure/table linked to code and data | figure exists without provenance |
| External validation | independent cohort/site/task inspected | mentioned but not inspected |

## Clinical AI readiness gate

Clinical readiness requires more than retrospective performance:

- label definition;
- temporal and site split;
- leakage audit;
- calibration;
- subgroup/fairness analysis;
- external validation;
- decision utility;
- implementation context;
- prospective or workflow evaluation;
- safety and failure-mode analysis.

If these are absent, use: "development/internal validation only" or "planning stage".

## Structure/mechanism gate

Predicted structure, docking, or model confidence can support a hypothesis, not mechanism proof. Stronger claims require:

- confidence metrics and model file;
- interface/uncertainty inspection;
- binding or perturbation assay;
- mutagenesis or orthogonal validation;
- functional phenotype;
- disease/context relevance.
