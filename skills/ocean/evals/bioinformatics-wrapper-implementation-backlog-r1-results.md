# OCEAN Bioinformatics Wrapper Implementation Backlog R1

- Run date: 2026-07-08
- Backlog items: 115
- Evidence boundary: Backlog generated from readiness plans only; no external software execution or scientific validation.

## Group Counts

| Group | Items |
|---|---:|
| common_cli_wrappers | 58 |
| heavy_tool_launcher_plans | 10 |
| immediate_local_packetization | 3 |
| priority_environment_setup | 18 |
| python_r_package_wrappers | 21 |
| workflow_reproducibility_plans | 5 |

## Top 30 Items

| Rank | Group | Tool | Family | Stage | Interface | Next action |
|---:|---|---|---|---|---|---|
| 1 | immediate_local_packetization | DESeq2 | differential_expression | stage_2_local_smoke_executed | r_bioconductor_rscript | Collect an inspected run record or minimal fixture, then create a software source packet with the shared packet helper. |
| 2 | immediate_local_packetization | limma-voom | differential_expression | stage_2_local_smoke_executed | r_bioconductor_rscript | Collect an inspected run record or minimal fixture, then create a software source packet with the shared packet helper. |
| 3 | immediate_local_packetization | AlphaFold DB | structure_modeling | stage_2_local_smoke_executed | heavy_cli_api_or_container_launcher | Collect an inspected run record or minimal fixture, then create a software source packet with the shared packet helper. |
| 4 | priority_environment_setup | bcftools | alignment_file_operations | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 5 | priority_environment_setup | BEDTools | alignment_file_operations | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 6 | priority_environment_setup | SAMtools | alignment_file_operations | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 7 | priority_environment_setup | edgeR | differential_expression | stage_1_plan_ready_environment_missing | r_bioconductor_rscript | Verify Rscript and package version, then run only a bounded package check or tiny fixture with sessionInfo before packetization. |
| 8 | priority_environment_setup | DADA2 | microbiome_metagenomics | stage_1_plan_ready_environment_missing | r_bioconductor_rscript | Verify Rscript and package version, then run only a bounded package check or tiny fixture with sessionInfo before packetization. |
| 9 | priority_environment_setup | MAFFT | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 10 | priority_environment_setup | cutadapt | qc_preprocessing | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 11 | priority_environment_setup | fastp | qc_preprocessing | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 12 | priority_environment_setup | FastQC | qc_preprocessing | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 13 | priority_environment_setup | MultiQC | qc_preprocessing | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 14 | priority_environment_setup | BLAST | sequence_alignment | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 15 | priority_environment_setup | minimap2 | sequence_alignment | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 16 | priority_environment_setup | Seurat | single_cell_analysis | stage_1_plan_ready_environment_missing | r_bioconductor_rscript | Verify Rscript and package version, then run only a bounded package check or tiny fixture with sessionInfo before packetization. |
| 17 | priority_environment_setup | HMMER | structure_modeling | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 18 | priority_environment_setup | Docker | workflow_reproducibility | stage_1_plan_ready_environment_missing | workflow_reproducibility | Create a dry-run/test-profile plan with workflow version, config, container/environment manifest, and input manifest. |
| 19 | priority_environment_setup | Nextflow | workflow_reproducibility | stage_1_plan_ready_environment_missing | workflow_reproducibility | Create a dry-run/test-profile plan with workflow version, config, container/environment manifest, and input manifest. |
| 20 | priority_environment_setup | Singularity-Apptainer | workflow_reproducibility | stage_1_plan_ready_environment_missing | workflow_reproducibility | Create a dry-run/test-profile plan with workflow version, config, container/environment manifest, and input manifest. |
| 21 | priority_environment_setup | Snakemake | workflow_reproducibility | stage_1_plan_ready_environment_missing | workflow_reproducibility | Create a dry-run/test-profile plan with workflow version, config, container/environment manifest, and input manifest. |
| 22 | common_cli_wrappers | HTSlib | alignment_file_operations | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 23 | common_cli_wrappers | FIMO | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 24 | common_cli_wrappers | HOMER | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 25 | common_cli_wrappers | MACS2 | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 26 | common_cli_wrappers | MACS3 | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 27 | common_cli_wrappers | MEME | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 28 | common_cli_wrappers | Bakta | genome_assembly_annotation | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 29 | common_cli_wrappers | BUSCO | genome_assembly_annotation | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |
| 30 | common_cli_wrappers | Canu | genome_assembly_annotation | stage_1_plan_ready_environment_missing | lightweight_cli_subprocess | Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis. |

## Evidence Boundary / 证据边界

This backlog orders implementation work only. It does not prove that a tool is installed, callable, benchmarked, biologically valid, clinically useful, or publication-ready.
