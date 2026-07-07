# OCEAN Tool Adapters

This directory contains tool-specific source-packet adapters.

Each tool adapter should stay narrow:

- fetch or import source material;
- analyze only inspected files or API responses;
- create an OCEAN source packet;
- preserve what the packet cannot support.

Adapters do not decide scientific truth. OCEAN modules audit the resulting packet.

## Current layout

| Folder | Purpose |
|---|---|
| `bioinformatics/alphafold_db/` | AlphaFold DB predicted-structure confidence and PAE source packets |
| `literature/` | PubMed, EuropePMC, or local literature metadata source packets |
| `clinicaltrials/` | ClinicalTrials.gov registry source packets |
| `../run_reef_api_adapter.py` | Executable Reef API/database adapters for UniProt, PubMed, EuropePMC, ChEMBL, OpenTargets, STRING, Reactome, QuickGO, ClinVar, gnomAD, and AlphaFold DB |
| `bioinformatics/` | Per-tool scaffolds for bioinformatics software listed in OCEAN's resource map |
| `bioinformatics_tool_router.py` | Route tools to execution layers and create workflow plans for common bioinformatics tasks |
| `build_bioinformatics_capability_matrix.py` | Join the bioinformatics registry, API/source-packet contracts, and real-tool smoke results into a planning matrix |
| `build_bioinformatics_wrapper_readiness_plan.py` | Turn high-priority matrix rows into install/container/smoke/source-packet readiness plans |
| `run_bioinformatics_wrapper_readiness_eval.py` | Validate readiness-plan completeness and evidence-boundary safeguards |
| `common/` | Shared helpers for generic software source-packet creation, CLI subprocess probes, Rscript checks, and heavy-tool launcher plans |

Shared or cross-tool eval runners may live directly under `scripts/tools/`.

## Capability matrix

After running the scaffold and real-tool smoke evals, build a combined planning matrix:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_capability_matrix.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals
```

The matrix records scaffold/adapter coverage and local availability. It is not evidence that a tool has completed a biological analysis.

## Wrapper readiness plans

After the capability matrix exists, generate high-priority wrapper readiness plans:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_wrapper_readiness_plan.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals
```

Then validate the generated plans:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_wrapper_readiness_eval.py \
  --outdir skills/ocean/evals
```

Readiness plans define candidate interface layers, smoke probes, install/container notes, minimal fixtures, run-record evidence, stop conditions, and OCEAN handoffs. They are not installation instructions and must not be treated as proof that a tool can run locally.

## Naming pattern

Prefer:

```text
scripts/tools/<tool_or_resource>/source_packet.py
scripts/tools/<tool_or_resource>/run_eval.py
```

Use tool-specific names only when a directory contains multiple independent adapters.

## Scaffold vs executable adapter

Most `bioinformatics/<tool>/` folders start as L0/L1 scaffolds. They provide a stable place for:

- tool metadata;
- source-packet requirements;
- examples;
- future wrappers;
- future evals.

They do not mean that OCEAN installs or runs that tool. Use `common/software_source_packet.py` to packetize inspected run metadata until a dedicated wrapper exists. Use `common/cli_subprocess_wrapper.py`, `common/rscript_wrapper.py`, or `common/heavy_tool_launcher.py` when a tool should follow the shared CLI, R/Bioconductor, or heavy-tool execution layer.
