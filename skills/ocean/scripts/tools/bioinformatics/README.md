# Bioinformatics Tool Scaffolds

This directory contains one folder per bioinformatics tool listed in OCEAN's bioinformatics resource map.

These folders are scaffolds, not claims that the tools are installed or executable in OCEAN. Use `../common/software_source_packet.py` for generic source-packet creation until a tool has a dedicated wrapper.

Each tool folder includes `examples/run-record.example.json`, a template for recording inspected tool runs before they are converted into OCEAN evidence packets.

Each tool folder also includes `api.json` and `scripts/create_source_packet.py`. These define a stable local wrapper contract for turning inspected run metadata into source packets; they do not install or execute external tools.

Each tool folder includes `references/tool_usage.md`, a science-skills-style operation guide with use/avoid rules, required local execution evidence, stop conditions, and OCEAN handoff guidance.

Shared execution layers live in `../common/`:

- `cli_subprocess_wrapper.py` for lightweight local CLI tools such as FastQC, MultiQC, cutadapt, fastp, samtools, bcftools, bedtools, BLAST, MAFFT, HMMER, and minimap2.
- `rscript_wrapper.py` for R/Bioconductor tools such as DESeq2, limma, edgeR, Seurat, WGCNA, and DADA2.
- `heavy_tool_launcher.py` for non-executing launcher plans for tools such as Cell Ranger, GATK, AlphaFold, MaxQuant, Galaxy, 3D Slicer, and ChimeraX.

Tool folders: 115
