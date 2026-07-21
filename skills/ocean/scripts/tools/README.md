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
| `databases/` | Per-resource Reef API/database tool folders for UniProt, PubMed, EuropePMC, ChEMBL, OpenTargets, STRING, Reactome, QuickGO, ClinVar, gnomAD, AlphaFold DB, ClinicalTrials.gov, and NCBI E-utilities |
| `../run_reef_api_adapter.py` | Executable Reef API/database adapters for UniProt, PubMed, EuropePMC, ChEMBL, OpenTargets, STRING, Reactome, QuickGO, ClinVar, gnomAD, AlphaFold DB, ClinicalTrials.gov, and NCBI E-utilities |
| `bioinformatics/` | Per-tool scaffolds for bioinformatics software listed in OCEAN's resource map |
| `bioinformatics_tool_router.py` | Route tools to execution layers and create workflow plans for common bioinformatics tasks |
| `build_bioinformatics_capability_matrix.py` | Join the bioinformatics registry, API/source-packet contracts, and real-tool smoke results into a planning matrix |
| `build_bioinformatics_wrapper_readiness_plan.py` | Turn priority or full matrix rows into install/container/smoke/source-packet readiness plans |
| `run_bioinformatics_wrapper_readiness_eval.py` | Validate readiness-plan completeness and evidence-boundary safeguards |
| `build_bioinformatics_wrapper_backlog.py` | Convert all-tool readiness plans into an ordered implementation backlog |
| `run_bioinformatics_wrapper_backlog_eval.py` | Validate backlog completeness, rank continuity, next actions, and evidence boundaries |
| `generate_bioinformatics_probe_wrappers.py` | Generate per-tool `wrapper_config.json` and `scripts/probe_or_plan.py` entrypoints |
| `run_bioinformatics_per_tool_wrapper_eval.py` | Execute generated per-tool probe/plan entrypoints and validate their artifacts |
| `generate_bioinformatics_cli_runners.py` | Generate per-tool `scripts/run_cli.py` entrypoints for lightweight CLI tools |
| `run_bioinformatics_cli_runner_eval.py` | Execute lightweight CLI runner probes and validate bounded provenance artifacts |
| `generate_bioinformatics_package_runners.py` | Generate per-tool `scripts/run_package.py` entrypoints for Python/R package tools |
| `run_bioinformatics_package_runner_eval.py` | Execute Python/R package runner probes and validate bounded provenance artifacts |
| `generate_bioinformatics_launcher_runners.py` | Generate per-tool `scripts/run_launcher.py` entrypoints for heavy, workflow-runtime, and source-packet-adapter tools |
| `run_bioinformatics_launcher_runner_eval.py` | Execute launcher-plan and workflow-runtime probe checks |
| `run_bioinformatics_code_coverage_eval.py` | Verify all 115 bioinformatics tool folders have generic wrappers and execution-layer-specific runner/API commands |
| `generate_database_adapter_scaffold.py` | Generate per-resource database adapter folders around the shared Reef API runner |
| `run_database_tool_adapter_eval.py` | Execute database adapter folder entrypoints in dry-run or bounded live mode |
| `common/` | Shared helpers for generic software source-packet creation, CLI subprocess probes, Rscript checks, and heavy-tool launcher plans |

Shared or cross-tool eval runners may live directly under `scripts/tools/`.

## Capability matrix

After running the scaffold and real-tool smoke evals, build a combined planning matrix:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_capability_matrix.py \
  --skill-dir skills/ocean \
  --outdir validation
```

The matrix records scaffold/adapter coverage and local availability. It is not evidence that a tool has completed a biological analysis.

## Wrapper readiness plans

After the capability matrix exists, generate high-priority wrapper readiness plans:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_wrapper_readiness_plan.py \
  --skill-dir skills/ocean \
  --outdir validation
```

To cover every registered bioinformatics scaffold, run the same builder with all-tool scope and a separate prefix:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_wrapper_readiness_plan.py \
  --skill-dir skills/ocean \
  --outdir validation \
  --scope all \
  --prefix bioinformatics-wrapper-readiness-all-r1
```

Then validate the generated plans:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_wrapper_readiness_eval.py \
  --outdir validation
```

For the all-tool run, validate the matching prefix:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_wrapper_readiness_eval.py \
  --outdir validation \
  --prefix bioinformatics-wrapper-readiness-all-r1
```

Readiness plans define candidate interface layers, smoke probes, install/container notes, minimal fixtures, run-record evidence, stop conditions, and OCEAN handoffs. They are not installation instructions and must not be treated as proof that a tool can run locally.

## Wrapper implementation backlog

After generating the all-tool readiness plans, build an ordered engineering backlog:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_wrapper_backlog.py \
  --outdir validation
```

Then validate the backlog artifact:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_wrapper_backlog_eval.py \
  --outdir validation
```

The backlog groups work into immediate local packetization, priority environment setup, common CLI wrappers, Python/R package wrappers, workflow plans, and heavy-tool launcher plans. It is still an engineering-planning artifact, not proof that a tool ran or that a biological result is valid.

## Per-tool probe/plan wrappers

Generate concrete per-tool wrapper entrypoints:

```bash
python3 skills/ocean/scripts/tools/generate_bioinformatics_probe_wrappers.py \
  --skill-dir skills/ocean
```

Then execute the generated entrypoints in bounded probe/plan mode:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_per_tool_wrapper_eval.py \
  --skill-dir skills/ocean \
  --outdir validation
```

Each tool folder receives `wrapper_config.json` and `scripts/probe_or_plan.py`. The generated entrypoint either records a local availability/version/import probe or emits a launcher/source-packet plan. It does not install tools, download databases, run biological analyses, benchmark methods, or validate scientific claims.

## Lightweight CLI runners

For tools whose execution layer is `lightweight_cli`, generate per-tool runner entrypoints:

```bash
python3 skills/ocean/scripts/tools/generate_bioinformatics_cli_runners.py \
  --skill-dir skills/ocean
```

Then run the bounded probe eval:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_cli_runner_eval.py \
  --skill-dir skills/ocean \
  --outdir validation
```

Each lightweight CLI folder receives `scripts/run_cli.py` plus `cli-probe` and `cli-run-record` API commands. The runner delegates to `common/cli_subprocess_wrapper.py`, records executable availability and command provenance, and requires explicit user-supplied arguments for non-probe runs. It does not install tools, choose private inputs, download references, complete workflows, benchmark methods, or validate biological claims.

## Python/R package runners

For Python-package and R/Bioconductor tools, generate per-tool package runner entrypoints:

```bash
python3 skills/ocean/scripts/tools/generate_bioinformatics_package_runners.py \
  --skill-dir skills/ocean
```

Then run the bounded package probe eval:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_package_runner_eval.py \
  --skill-dir skills/ocean \
  --outdir validation
```

Each Python/R package folder receives `scripts/run_package.py` plus `package-probe` and `package-run-record` API commands. The runner records package/module availability and can record explicit user-supplied Python/R script execution provenance. It does not install packages, choose private inputs, design analyses, validate scripts, complete workflows, benchmark methods, or validate biological claims.

## Launcher and workflow runners

For heavy, workflow-runtime, and source-packet-adapter tools, generate per-tool launcher entrypoints:

```bash
python3 skills/ocean/scripts/tools/generate_bioinformatics_launcher_runners.py \
  --skill-dir skills/ocean
```

Then run the bounded launcher/workflow eval:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_launcher_runner_eval.py \
  --skill-dir skills/ocean \
  --outdir validation
```

Each relevant tool folder receives `scripts/run_launcher.py` and a `launcher-plan` API command. Workflow runtimes also receive `runtime-probe` and `runtime-run-record` commands. Launcher plans are intentionally non-executing; they record required assets, stop conditions, compute/privacy/license notes, and run evidence needed before any source packet can support downstream OCEAN review.

## All-tool code coverage

After generating CLI, package, and launcher runners, run the structural coverage check:

```bash
python3 skills/ocean/scripts/tools/run_bioinformatics_code_coverage_eval.py \
  --skill-dir skills/ocean \
  --outdir validation
```

This confirms that every bioinformatics tool folder has the generic source-packet/probe wrappers plus the execution-layer-specific runner and API commands. It is a code-surface check, not a local installation check or biological workflow validation.

## Database tool adapters

Generate per-resource database adapter folders:

```bash
python3 skills/ocean/scripts/tools/generate_database_adapter_scaffold.py \
  --skill-dir skills/ocean
```

Validate the generated folders without network access:

```bash
python3 skills/ocean/scripts/tools/run_database_tool_adapter_eval.py \
  --skill-dir skills/ocean \
  --outdir validation
```

Run bounded live public API checks only when public network access is appropriate:

```bash
python3 skills/ocean/scripts/tools/run_database_tool_adapter_eval.py \
  --skill-dir skills/ocean \
  --outdir validation \
  --execute-live \
  --retmax 1
```

These database folders make public resources scriptable as OCEAN Reef packet adapters. They do not make OCEAN dependent on any live API and do not convert database metadata into biological, causal, or clinical proof.

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
