# Artifact Ledger Gate

OCEAN should connect claims to artifacts, not only to prose.

Core rule: Artifact exists != artifact supports the claim.

Use this gate when the user provides or mentions code, notebooks, figures, tables, logs, data files, manuscripts, reviewer comments, database/API outputs, or collaboration notes.

## Artifact ledger fields

| Artifact | Type | Provided? | Inspected? | Version/ID/checksum | Supports which claim? | Missing link |
|---|---|---|---|---|---|---|

## Reproducibility rules

- A file name is not an inspected artifact.
- A notebook file is not a reproducible analysis unless code, inputs, environment, parameters, and execution path are inspectable.
- A Slurm/HPC job completion log is not a validation result.
- A figure is not traceable unless the data source and figure-generation code/parameters are known.
- A database output is not evidence unless the query, timestamp, identifiers, and inspected fields are recorded.
- A meeting note is not an authorship or submission record unless it explicitly says so.

## Claim-to-artifact rule

For each major claim, identify:

- supporting artifact;
- inspected content;
- support level;
- missing artifact;
- safe rewrite or stop condition.
