# OCEAN Bioinformatics Wrapper Readiness Plan R1

- Run date: 2026-07-07
- Priority tools planned: 20
- Mean readiness score: 8.20 / 10
- Local smoke already executed: 2
- Environment-missing but plan-ready: 18

## What This Adds

This R1 artifact turns the capability matrix into implementation plans for high-priority tools. Each plan records the intended interface layer, a bounded smoke probe, candidate install/container routes, the minimal fixture needed, required run evidence, stop conditions, and OCEAN handoff.

It does not install or run the tools. Candidate install routes must be verified against current official documentation before use.

## Priority Plan Table

| Tool | Family | Stage | Score | Interface | Smoke command | Handoff |
|---|---|---|---:|---|---|---|
| FastQC | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `fastqc --version` | Anchor |
| MultiQC | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `multiqc --version` | Anchor |
| cutadapt | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `cutadapt --version` | Anchor |
| fastp | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `fastp --version` | Anchor |
| SAMtools | alignment_file_operations | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `samtools --version` | Anchor |
| bcftools | alignment_file_operations | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bcftools --version` | Anchor |
| BEDTools | alignment_file_operations | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bedtools --version` | Anchor |
| BLAST | sequence_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `blastp -version` | Anchor |
| MAFFT | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `mafft --version` | Anchor |
| HMMER | structure_modeling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `hmmsearch -h` | Anchor |
| minimap2 | sequence_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `minimap2 --version` | Anchor |
| DESeq2 | differential_expression | stage_2_local_smoke_executed | 10 | r_bioconductor_rscript | `Rscript -e cat(as.character(utils::packageVersion('DESeq2')))` | Anchor |
| edgeR | differential_expression | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_rscript | `Rscript -e cat(as.character(utils::packageVersion('edgeR')))` | Anchor |
| limma-voom | differential_expression | stage_2_local_smoke_executed | 10 | r_bioconductor_rscript | `Rscript -e cat(as.character(utils::packageVersion('limma')))` | Anchor |
| Seurat | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_rscript | `Rscript -e cat(as.character(utils::packageVersion('Seurat')))` | Anchor |
| DADA2 | microbiome_metagenomics | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_rscript | `Rscript -e cat(as.character(utils::packageVersion('dada2')))` | Anchor |
| Snakemake | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `snakemake --version` | Harbor |
| Nextflow | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `nextflow -version` | Harbor |
| Docker | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `docker --version` | Harbor |
| Singularity-Apptainer | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `apptainer --version` | Harbor |

## Next Implementation Order

1. **DESeq2**: stage_2_local_smoke_executed; next step is to collect a real run record or verify/install the environment, then create a source packet.
2. **limma-voom**: stage_2_local_smoke_executed; next step is to collect a real run record or verify/install the environment, then create a source packet.
3. **bcftools**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
4. **BEDTools**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
5. **BLAST**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
6. **cutadapt**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
7. **DADA2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
8. **Docker**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
9. **edgeR**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
10. **fastp**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
11. **FastQC**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
12. **HMMER**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
13. **MAFFT**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
14. **minimap2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
15. **MultiQC**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
16. **Nextflow**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
17. **SAMtools**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
18. **Seurat**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
19. **Singularity-Apptainer**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
20. **Snakemake**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.

## Evidence Boundary / 证据边界

- `stage_2_local_smoke_executed` means a bounded local version/package probe existed in the capability matrix, not a biological analysis.
- `stage_1_plan_ready_environment_missing` means OCEAN has a plan, but local execution is unavailable until the environment/tool/container is supplied.
- Candidate install routes are planning notes and must be verified against official/current documentation before use.
- These plans cannot support mechanism, causality, clinical utility, reproducibility, or publication readiness without inspected run records and downstream OCEAN audit.
