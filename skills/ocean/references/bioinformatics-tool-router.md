# Bioinformatics Tool Router

Use this reference when a user asks which bioinformatics tools to use, how a tool should be executed, or how to turn a biological/medical research workflow into OCEAN source-packet evidence.

The router is implemented in `scripts/tools/bioinformatics_tool_router.py`. It does not execute external tools. It classifies tools, proposes wrapper commands, records required evidence, and creates workflow plans.

## What the router adds

- Tool profile: execution layer, primary entrypoint, wrapper, required evidence, stop conditions, and handoff.
- Tool catalog: one profile for every scaffolded bioinformatics tool.
- Workflow plan: ordered tool list for common biomedical and biological analysis workflows.
- Boundary discipline: every plan states what it cannot prove.

## Commands

Profile one tool:

```bash
python3 scripts/tools/bioinformatics_tool_router.py profile \
  --skill-dir . \
  --tool fastqc \
  --output fastqc-profile.json
```

Export all 115 profiles:

```bash
python3 scripts/tools/bioinformatics_tool_router.py catalog \
  --skill-dir . \
  --output bioinformatics-tool-catalog.json
```

Plan a workflow:

```bash
python3 scripts/tools/bioinformatics_tool_router.py workflow \
  --skill-dir . \
  --workflow rna-seq-differential-expression \
  --output rna-seq-plan.json \
  --markdown-output rna-seq-plan.md
```

List workflows:

```bash
python3 scripts/tools/bioinformatics_tool_router.py list-workflows \
  --output workflows.json
```

## Supported workflow seeds

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

## Execution-layer meaning

- `source_packet_adapter`: tool-specific adapter can inspect local/source metadata and create an OCEAN packet.
- `lightweight_cli`: use bounded local CLI subprocess probes/runs.
- `r_bioconductor`: use bounded `Rscript` package/script checks.
- `python_package`: record Python package/import/script provenance before source-packet creation.
- `workflow_runtime`: record workflow engine/container/run manifest before claims.
- `heavy_launcher_plan`: create launcher plan only; do not pretend the tool ran.
- `run_record_only`: use the generic software source-packet helper after a user supplies inspected run metadata.

## Evidence Boundary

Router output is planning evidence. It can support statements such as "this tool belongs in this workflow" or "this run requires these records before evidence use." It cannot support mechanism, causality, clinical utility, benchmark superiority, or publication readiness.

Handoff:

- Send selected tool profiles to Reef as a resource/provenance map.
- Send execution records to Anchor for reproducibility review.
- Send unsupported claim pressure to Iceberg for downgrade.
- Send missing tools, missing databases, license blocks, and run debts to Harbor.
