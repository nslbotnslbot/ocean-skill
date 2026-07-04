# Anchor Module Contract

Active module: Anchor

Purpose: design validation, reproducibility, leakage, benchmark, external-check, and clinical-readiness gates.

## Required artifact

- Validation Checklist
- Leakage/Benchmark/Reproducibility Plan
- External-check Boundary
- Passed-vs-Planned Gate Table

## Gate table

| Gate | Planned? | Evidence passed? | Evidence inspected | Missing item | Stop condition |
|---|---|---|---|---|---|

## Hard rules

- Planned validation != passed validation.
- Slurm completed != analysis valid.
- Notebook exists != reproducible pipeline.
- Figure exists != traceable artifact.
- Benchmark reported != fair benchmark.
- External validation mentioned != external validation inspected.
- Clinical readiness requires prospective/implementation evidence, calibration, decision utility, safety, and deployment context.

## Reproducibility minimum

Require data ID/checksum, code, parameters, environment versions, random seed, execution log, and output artifact lineage before calling an analysis reproducible.

## Stop when

Stop before declaring validation passed, reproducibility achieved, clinical readiness, or benchmark fairness if the required artifacts are planned, named, or claimed but not inspected.
