# OCEAN Bioinformatics Capability Matrix R1

- Run date: 2026-07-06
- Tools indexed: 115
- Capability tiers: `{"source_packet_adapter": 1, "source_packet_scaffold": 114}`
- Local smoke status: `{"executed": 3, "not_available_current_environment": 112}`

## What This Matrix Means

This matrix joins OCEAN's static tool registry, per-tool API/source-packet contracts, and the latest local real-tool smoke results. It is a planning artifact for tool coverage and implementation priority.

It does not install software, run omics analyses, download databases, benchmark tools, or validate biological conclusions.

## Family Summary

| Family | Tools | Executed locally | Source-packet adapters | Scaffolds |
|---|---:|---:|---:|---:|
| alignment_file_operations | 4 | 0 | 0 | 4 |
| differential_expression | 4 | 2 | 0 | 4 |
| epigenomics_peak_calling | 6 | 0 | 0 | 6 |
| genome_assembly_annotation | 12 | 0 | 0 | 12 |
| imaging_signal_ml | 6 | 0 | 0 | 6 |
| microbiome_metagenomics | 6 | 0 | 0 | 6 |
| multi_omics_integration | 5 | 0 | 0 | 5 |
| phylogenetics_comparative_genomics | 7 | 0 | 0 | 7 |
| proteomics_metabolomics | 7 | 0 | 0 | 7 |
| qc_preprocessing | 8 | 0 | 0 | 8 |
| rna_seq_quantification | 5 | 0 | 0 | 5 |
| sequence_alignment | 5 | 0 | 0 | 5 |
| single_cell_analysis | 8 | 0 | 0 | 8 |
| spatial_transcriptomics | 7 | 0 | 0 | 7 |
| spliced_rna_alignment | 2 | 0 | 0 | 2 |
| structure_modeling | 9 | 1 | 1 | 8 |
| variant_calling | 5 | 0 | 0 | 5 |
| workflow_reproducibility | 9 | 0 | 0 | 9 |

## Practical Wrapper Priorities

These are high-utility tools where OCEAN should next add stronger install/container notes, focused smoke fixtures, or dedicated wrappers before claiming execution support.

| Tool | Family | Local status | Interface | Next action |
|---|---|---|---|---|
| bcftools | alignment_file_operations | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| BEDTools | alignment_file_operations | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| BLAST | sequence_alignment | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| cutadapt | qc_preprocessing | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| DADA2 | microbiome_metagenomics | not_available_current_environment | r_package | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| DESeq2 | differential_expression | executed | r_package | Create a real run record from inspected files, then convert it into an OCEAN software source packet. |
| Docker | workflow_reproducibility | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| edgeR | differential_expression | not_available_current_environment | r_package | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| fastp | qc_preprocessing | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| FastQC | qc_preprocessing | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| HMMER | structure_modeling | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| limma-voom | differential_expression | executed | r_package | Create a real run record from inspected files, then convert it into an OCEAN software source packet. |
| MAFFT | phylogenetics_comparative_genomics | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| minimap2 | sequence_alignment | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| MultiQC | qc_preprocessing | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| Nextflow | workflow_reproducibility | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| SAMtools | alignment_file_operations | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| Seurat | single_cell_analysis | not_available_current_environment | r_package | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| Singularity-Apptainer | workflow_reproducibility | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |
| Snakemake | workflow_reproducibility | not_available_current_environment | none_found | High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution. |

## Full Matrix

| Tool | Family | Tier | Local status | Interface | Handoff |
|---|---|---|---|---|---|
| Alevin-fry | single_cell_analysis | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| AlphaFold | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| AlphaFold DB | structure_modeling | source_packet_adapter | executed | ocean_local_adapter | Anchor |
| Azimuth | single_cell_analysis | source_packet_scaffold | not_available_current_environment | r_package | Anchor |
| Bakta | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| bcftools | alignment_file_operations | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| BEDTools | alignment_file_operations | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| BLAST | sequence_alignment | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Bowtie2 | sequence_alignment | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Bracken | microbiome_metagenomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| BUSCO | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| BWA | sequence_alignment | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Canu | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| cell2location | spatial_transcriptomics | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| Cell Ranger | single_cell_analysis | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| CellTypist | single_cell_analysis | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| CheckM | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| ChimeraX | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Clustal Omega | phylogenetics_comparative_genomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| ColabFold | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Conda | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| cutadapt | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| CWL | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| DADA2 | microbiome_metagenomics | source_packet_scaffold | not_available_current_environment | r_package | Anchor |
| deepTools | epigenomics_peak_calling | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| DeepVariant | variant_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| DESeq2 | differential_expression | source_packet_scaffold | executed | r_package | Anchor |
| DIA-NN | proteomics_metabolomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| DIABLO | multi_omics_integration | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| Docker | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| edgeR | differential_expression | source_packet_scaffold | not_available_current_environment | r_package | Anchor |
| eggNOG-mapper | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| fastp | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| FastQC | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| FastTree | phylogenetics_comparative_genomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| featureCounts | rna_seq_quantification | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| FIMO | epigenomics_peak_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Flye | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| FragPipe | proteomics_metabolomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| FreeBayes | variant_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Galaxy | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| GATK | variant_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Giotto | spatial_transcriptomics | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| HH-suite | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| HISAT2 | spliced_rna_alignment | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| HMMER | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| HOMER | epigenomics_peak_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| HTSlib | alignment_file_operations | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| HUMAnN | microbiome_metagenomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| InterProScan | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| IQ-TREE | phylogenetics_comparative_genomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| ITK-SNAP | imaging_signal_ml | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| kallisto | rna_seq_quantification | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Kraken2 | microbiome_metagenomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| LAST | sequence_alignment | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| limma-voom | differential_expression | source_packet_scaffold | executed | r_package | Anchor |
| MACS2 | epigenomics_peak_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MACS3 | epigenomics_peak_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MAFFT | phylogenetics_comparative_genomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MaxQuant | proteomics_metabolomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MEGAHIT | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MEME | epigenomics_peak_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MetaPhlAn | microbiome_metagenomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| minimap2 | sequence_alignment | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| mixOmics | multi_omics_integration | source_packet_scaffold | not_available_current_environment | r_package | Anchor |
| MODELLER | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MOFA | multi_omics_integration | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| MOFA+ | multi_omics_integration | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| MONAI | imaging_signal_ml | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| MS-DIAL | proteomics_metabolomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MultiQC | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MUSCLE | phylogenetics_comparative_genomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Mutect2 | variant_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| MZmine | proteomics_metabolomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Nextflow | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| nf-core | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| nnU-Net | imaging_signal_ml | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| OrthoFinder | phylogenetics_comparative_genomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Picard | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Prokka | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| PyMOL | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| QIIME2 | microbiome_metagenomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Qualimap | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| QUAST | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Raven | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| RAxML | phylogenetics_comparative_genomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| RoseTTAFold | structure_modeling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| RSEM | rna_seq_quantification | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Salmon | rna_seq_quantification | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| SAMtools | alignment_file_operations | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Scanpy | single_cell_analysis | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| scVI | single_cell_analysis | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| Seurat | single_cell_analysis | source_packet_scaffold | not_available_current_environment | r_package | Anchor |
| SimpleITK | imaging_signal_ml | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| Singularity-Apptainer | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Skyline | proteomics_metabolomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| sleuth | differential_expression | source_packet_scaffold | not_available_current_environment | r_package | Anchor |
| Snakemake | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Space Ranger | spatial_transcriptomics | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| SPAdes | genome_assembly_annotation | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Squidpy | spatial_transcriptomics | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| STAR | spliced_rna_alignment | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| STARsolo | single_cell_analysis | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Stereoscope | spatial_transcriptomics | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| stLearn | spatial_transcriptomics | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| Strelka2 | variant_calling | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| StringTie | rna_seq_quantification | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Tangram | spatial_transcriptomics | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| 3D Slicer | imaging_signal_ml | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| TorchIO | imaging_signal_ml | source_packet_scaffold | not_available_current_environment | python_import | Anchor |
| Trim Galore | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| Trimmomatic | qc_preprocessing | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| WDL-Cromwell | workflow_reproducibility | source_packet_scaffold | not_available_current_environment | none_found | Anchor |
| WGCNA | multi_omics_integration | source_packet_scaffold | not_available_current_environment | r_package | Anchor |
| XCMS | proteomics_metabolomics | source_packet_scaffold | not_available_current_environment | r_package | Anchor |

## Evidence Boundary / 证据边界

- `executed` means the current local environment produced a bounded smoke result only.
- `not_available_current_environment` means the scaffold may be useful, but local execution is not available until the tool/package/container is installed.
- `source_packet_scaffold` means OCEAN can packetize inspected run metadata, not run the underlying scientific tool.
- `source_packet_adapter` means a narrower adapter exists, but its outputs still need source-specific evidence boundaries.
- This matrix must not be used as evidence of mechanism, causality, clinical utility, reproducibility, or publication readiness.
