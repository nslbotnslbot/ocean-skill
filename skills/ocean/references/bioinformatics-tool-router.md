# Bioinformatics Tool Router

Use this reference when a user asks which bioinformatics tool or workflow fits
a medical or biological research task.

The public entry point is:

`scripts/tools/bioinformatics_tool_router.py`

It reads each tool's `wrapper_config.json` and exposes five user-facing
operations:

- `list-tools`: list or search the 115 covered tools;
- `profile`: show one tool's layer, evidence requirements, stop conditions,
  and wrapper command;
- `list-workflows`: list common workflow templates;
- `workflow`: create a bounded multi-tool plan;
- `check`: probe current availability or create a non-executing plan.

## Commands

Run these from the repository root:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  list-tools --search rna
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  profile --tool fastqc
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-workflows
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  workflow \
  --workflow rna-seq-differential-expression \
  --output outputs/rna-seq-plan.json
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  check \
  --tool fastqc \
  --output outputs/fastqc-check.json
```

## What `check` Means

| Tool layer | `check` behavior |
|---|---|
| Lightweight CLI | Run the configured version/help probe |
| Python package | Check whether the configured module can be imported |
| R/Bioconductor | Check `Rscript` and the configured package version |
| Workflow runtime | Probe the configured runtime command |
| Heavy/license/GUI/GPU tool | Create a plan without launching the tool |
| Source-packet adapter | Create an adapter-input plan |

`check` never installs software, downloads a reference database, selects
private inputs, or runs a complete biological analysis.

## Workflow Seeds

- `fastq-qc`
- `rna-seq-differential-expression`
- `variant-calling-qc`
- `single-cell-rna-seq`
- `spatial-transcriptomics`
- `metagenomics-microbiome`
- `genome-assembly-annotation`
- `protein-structure`
- `epigenomics-peak-calling`
- `proteomics-metabolomics`
- `workflow-reproducibility`
- `imaging-ai`

## Evidence Boundary

A profile or workflow plan supports routing only. An availability probe supports
only the statement that a command/package/runtime was or was not observed in
the current environment. Neither one establishes biological validity,
mechanism, causality, clinical utility, benchmark superiority, or publication
readiness.

Use a real run record before creating a source packet. Send provenance and
resource selection to Reef, claim pressure to Iceberg, and reproducibility or
validation questions to Anchor.
