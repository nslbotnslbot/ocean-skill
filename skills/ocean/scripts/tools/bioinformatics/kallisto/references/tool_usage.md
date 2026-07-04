# kallisto Usage Guide

This is an OCEAN tool-use guide inspired by science-skills-style wrappers. It is not a standalone Codex skill and it does not mean `kallisto` is installed locally.

## Use When

Use `kallisto` when quantifying transcript/gene abundance from RNA-seq with explicit reference and sample metadata.

## Do Not Use When

Do not use `kallisto` as standalone proof of differential expression, mechanism, or phenotype causality.

Do not infer uninspected sample sizes, databases, parameters, versions, benchmarks, effect sizes, or validation results.

## Before Running Or Trusting Output

Confirm and record:

- tool version and executable/package source;
- command line or workflow step;
- parameters and configuration files;
- reference/index/database and version;
- input files and sample metadata boundaries;
- output files and inspected result fields;
- logs, warnings, QC metrics, and failure messages;
- environment, container, OS, hardware if relevant, and run date;
- license/terms constraints when the tool or database requires them.

## OCEAN Packet Workflow

1. Run an availability smoke check before promising execution.
2. If the tool is unavailable, report `not_available_current_environment` and create an install/environment plan rather than inventing output.
3. If a real run exists, fill `examples/run-record.example.json` with inspected metadata.
4. Convert the inspected run record with `scripts/create_source_packet.py`.
5. Hand off the packet according to: Anchor for QC/replicate checks; Iceberg for expression-supported claims.

## Stop Conditions

Stop and ask for more evidence when:

- version, command, reference/index, inputs, outputs, or logs are missing;
- the run used private/clinical data without explicit access/privacy boundaries;
- the result is being used to claim mechanism, causality, clinical utility, or publication readiness without independent validation;
- the tool is unavailable in the current environment.

## Evidence Boundary

`kallisto` output can support bounded software-run provenance only after the run record is inspected. It cannot by itself prove biological mechanism, causal conclusion, clinical utility, reproducibility, or publication readiness.
