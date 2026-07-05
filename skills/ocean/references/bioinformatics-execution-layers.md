# Bioinformatics Execution Layers

Use this reference when Reef routes a software request from a biological or medical research task to local bioinformatics tools.

OCEAN distinguishes three execution layers. This prevents the skill from pretending that unavailable tools, licensed tools, large databases, or GPU workflows have run.

## Layer 1: Lightweight CLI Subprocess Tools

Use `scripts/tools/common/cli_subprocess_wrapper.py` for tools such as FastQC, MultiQC, cutadapt, fastp, samtools, bcftools, bedtools, BLAST, MAFFT, HMMER, and minimap2.

Required behavior:

- call commands with `subprocess.run([...])`, not shell strings;
- record command, version/probe output, return code, stdout/stderr excerpts, PATH resolution, date, and environment;
- stop cleanly when a command is not installed;
- never install tools or download references automatically;
- never treat a version/help probe as an end-to-end biological analysis.

Example:

```bash
python3 scripts/tools/common/cli_subprocess_wrapper.py probe \
  --tool-name FastQC \
  --tool-slug fastqc \
  --command fastqc \
  --probe-args=--version \
  --output fastqc-probe.json
```

## Layer 2: R/Bioconductor Rscript Tools

Use `scripts/tools/common/rscript_wrapper.py` for tools such as DESeq2, limma, edgeR, Seurat, WGCNA, and DADA2.

Required behavior:

- check `Rscript` availability before using a package;
- check package versions with `utils::packageVersion`;
- run user-supplied R scripts only through explicit file paths and argument lists;
- record Rscript path, package version or error, script path, parameters, input/output manifests, and logs/QC;
- stop when `Rscript` or the package is unavailable.

Example:

```bash
python3 scripts/tools/common/rscript_wrapper.py check-package \
  --tool-name DESeq2 \
  --tool-slug deseq2 \
  --package DESeq2 \
  --output deseq2-package-check.json
```

## Layer 3: Heavy / Licensed / GUI / Large-Database Tools

Use `scripts/tools/common/heavy_tool_launcher.py` for tools such as Cell Ranger, GATK, AlphaFold, MaxQuant, Galaxy, 3D Slicer, and ChimeraX.

This layer creates a launcher plan and run-record checklist only. It does not execute the tool.

Required behavior:

- record command template, required assets, container/environment, license/terms note, compute requirements, and stop conditions;
- require explicit run evidence before any result becomes a source packet;
- stop if license, reference database/index, GPU/HPC/container runtime, GUI logs, or data-safety requirements are missing.

Example:

```bash
python3 scripts/tools/common/heavy_tool_launcher.py plan \
  --tool-name AlphaFold \
  --tool-slug alphafold \
  --command-template 'run_alphafold.py --fasta_paths <input.fasta> --data_dir <database_dir> --output_dir <outdir>' \
  --required-assets-json '["AlphaFold databases", "model parameters", "FASTA input", "GPU/container environment"]' \
  --output alphafold-launch-plan.json
```

## Evidence Boundary

These wrappers can support statements about local availability, command provenance, package availability, or planned execution requirements. They cannot support biological mechanism, causality, clinical utility, benchmark superiority, or publication readiness without downstream OCEAN review.

Handoff:

- send executed command records to Anchor for validation/reproducibility review;
- send missing-tool or missing-package records to Harbor as environment setup debt;
- send heavy-tool launch plans to Compass or Anchor before execution;
- send completed and audited source packets back to Iceberg only when evaluating claims.
