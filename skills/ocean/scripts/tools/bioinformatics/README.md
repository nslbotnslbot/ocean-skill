# Bioinformatics Tool Scaffolds

This directory contains one folder per bioinformatics tool listed in OCEAN's bioinformatics resource map.

These folders are scaffolds, not claims that the tools are installed or executable in OCEAN. Use `../common/software_source_packet.py` for generic source-packet creation until a tool has a dedicated wrapper.

Each tool folder includes `examples/run-record.example.json`, a template for recording inspected tool runs before they are converted into OCEAN evidence packets.

Each tool folder also includes `api.json`, `wrapper_config.json`, `scripts/create_source_packet.py`, and `scripts/probe_or_plan.py`. These define a stable local wrapper contract for bounded availability/plan probes and for turning inspected run metadata into source packets; they do not install or execute biological analyses.

Each tool folder includes `references/tool_usage.md`, a science-skills-style operation guide with use/avoid rules, required local execution evidence, stop conditions, and OCEAN handoff guidance.

Shared execution layers live in `../common/`:

- `cli_subprocess_wrapper.py` for lightweight local CLI tools such as FastQC, MultiQC, cutadapt, fastp, samtools, bcftools, bedtools, BLAST, MAFFT, HMMER, and minimap2.
- `rscript_wrapper.py` for R/Bioconductor tools such as DESeq2, limma, edgeR, Seurat, WGCNA, and DADA2.
- `heavy_tool_launcher.py` for non-executing launcher plans for tools such as Cell Ranger, GATK, AlphaFold, MaxQuant, Galaxy, 3D Slicer, and ChimeraX.

Tool folders: 115

## Capability matrix

Use the cross-tool capability matrix to summarize which folders are only scaffolds, which have source-packet adapters, and which tools are actually available in the current local environment:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_capability_matrix.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals
```

The matrix is a planning artifact. It must not be treated as biological validation, benchmark evidence, or proof that unavailable tools can run locally.

## Wrapper readiness plans

Once a capability matrix exists, build the next implementation plan for high-priority tools:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_wrapper_readiness_plan.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals
```

To generate bounded readiness plans for all 115 tool folders:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_wrapper_readiness_plan.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals \
  --scope all \
  --prefix bioinformatics-wrapper-readiness-all-r1
```

This produces per-tool readiness plans for practical wrapper work. Each plan records the intended execution layer, a bounded smoke probe, candidate install/container notes, required run evidence, and stop conditions. These plans do not install software or validate biological conclusions.

## Implementation backlog

After generating the all-tool readiness plans, build and validate the wrapper backlog:

```bash
python3 skills/ocean/scripts/tools/build_bioinformatics_wrapper_backlog.py \
  --outdir skills/ocean/evals

python3 skills/ocean/scripts/tools/run_bioinformatics_wrapper_backlog_eval.py \
  --outdir skills/ocean/evals
```

The backlog orders engineering work by current evidence and execution layer. It is useful for deciding which wrappers to implement next, but it is not installation, local execution, benchmarking, or biological validation.

## Per-tool probe/plan wrappers

Every tool folder has a generated `scripts/probe_or_plan.py` entrypoint backed by `wrapper_config.json`:

```bash
python3 scripts/probe_or_plan.py \
  --output /path/to/<tool>-probe-or-plan.json
```

From the repository root, regenerate and evaluate the full set with:

```bash
python3 skills/ocean/scripts/tools/generate_bioinformatics_probe_wrappers.py \
  --skill-dir skills/ocean

python3 skills/ocean/scripts/tools/run_bioinformatics_per_tool_wrapper_eval.py \
  --skill-dir skills/ocean \
  --outdir skills/ocean/evals
```

The wrapper records local availability/import/version evidence where safe, or creates a launcher/source-packet plan for heavy, GUI, license, GPU, workflow, or adapter-style tools. It is not a claim that the tool is installed, a workflow ran, or a biological conclusion is valid.
