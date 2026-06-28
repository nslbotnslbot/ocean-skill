# Audit Lenses

Use only the lenses relevant to the user's artifact. Do not treat this checklist as evidence; it is a guide for what to inspect.

## General Scientific Reliability

- Are data sources clearly defined?
- Are inclusion and exclusion criteria explicit?
- Is sample size sufficient for the claim being made?
- Are labels, endpoints, gold standards, or outcome definitions clear?
- Are training, validation, and test splits appropriate?
- Is there leakage risk through duplicate samples, temporal overlap, patient overlap, feature leakage, preprocessing leakage, or database overlap?
- Is there external validation?
- Are ablation studies included?
- Are benchmarks fair and comparable?
- Are statistical tests appropriate?
- Are limitations explicit?
- Are conclusions supported by the inspected evidence?

## AI, Agent, And LLM Reliability

- Is the task definition clear and reproducible?
- Are baselines appropriate?
- Are prompts, models, temperatures, tool permissions, retrieval settings, and versions reported?
- Are agent tools and permissions documented?
- Is there a deterministic verifier or independent evaluator?
- Are failure cases reported?
- Is there an ablation of tools, memory, RAG, critic, multi-agent components, or retrieval sources?
- Is there human expert evaluation when the task requires domain judgment?
- Are cost, latency, stability, and hallucination rates reported when relevant?
- Is the system reproducible outside the authors' environment?

## Biomedical, Database, And Knowledge Graph Caution

- Separate human, animal, cell-line, computational, database, and literature-mining evidence.
- Do not treat text-mined relations as validated mechanisms.
- Do not treat database co-occurrence as causality.
- Check whether disease, gene, drug, protein, variant, and phenotype identifiers are standardized.
- Flag circular validation when discovery and validation rely on overlapping databases.
- Require independent experimental, clinical, or external-data validation for strong biological or clinical claims.

## Clinical Prediction And Medical AI

- Check cohort definition, site count, dates, inclusion criteria, exclusion criteria, endpoint timing, and missing-data handling.
- Check train/validation/test split, patient-level separation, temporal validation, site-level validation, and true external validation.
- Require calibration, decision-curve analysis, subgroup performance, and clinical utility discussion for deployment claims.
- Downgrade claims when the work reports only AUROC or accuracy without calibration, external validation, or decision impact.

## Publication Positioning

Classify realistic positioning as one or more of:

- top general journal
- Nature Communications / Science Advances / Cell Reports / iScience level
- Communications Biology / Medicine / Engineering / Materials / Chemistry
- AI/computational/data science journal
- biomedical AI / bioinformatics journal
- database/resource journal
- software/application journal
- ordinary application journal
- not ready for submission

For each likely tier, explain why it fits, why it may fail, what must be added to move up one tier, and the likely reviewer objections.

## Contribution Boundary

Classify the user's role:

- Light participation: reliability assessment, journal positioning, key risks, article logic, broad strengthening suggestions.
- Medium participation: article structure, result reorganization, figure strategy, critical analysis design, reviewer risk prediction.
- Deep participation: data reanalysis, benchmark design, external validation, ablation experiments, case-study design, major result interpretation, major writing.
- Authorship-level contribution: substantial impact on research question, analysis design, key results, figures, validation, manuscript writing, or interpretation.

Warn when a request is becoming unpaid deep consulting without a clear authorship or collaboration boundary.
