# OCEAN Bioinformatics Lightweight CLI Runner Eval R1

- Run date: 2026-07-08
- Tools checked: 60
- Pass: 60
- Needs review: 0

## Execution Status Counts

| Status | Count |
|---|---:|
| not_available_current_environment | 60 |

## Tool Results

| Tool | Command | Family | Status | Verdict | Issues |
|---|---|---|---|---|---|
| Alevin-fry | `alevin-fry` | single_cell_analysis | not_available_current_environment | pass |  |
| Bakta | `bakta` | genome_assembly_annotation | not_available_current_environment | pass |  |
| bcftools | `bcftools` | alignment_file_operations | not_available_current_environment | pass |  |
| BEDTools | `bedtools` | alignment_file_operations | not_available_current_environment | pass |  |
| BLAST | `blastp` | sequence_alignment | not_available_current_environment | pass |  |
| Bowtie2 | `bowtie2` | sequence_alignment | not_available_current_environment | pass |  |
| Bracken | `bracken` | microbiome_metagenomics | not_available_current_environment | pass |  |
| BUSCO | `busco` | genome_assembly_annotation | not_available_current_environment | pass |  |
| BWA | `bwa` | sequence_alignment | not_available_current_environment | pass |  |
| Canu | `canu` | genome_assembly_annotation | not_available_current_environment | pass |  |
| CheckM | `checkm` | genome_assembly_annotation | not_available_current_environment | pass |  |
| Clustal Omega | `clustalo` | phylogenetics_comparative_genomics | not_available_current_environment | pass |  |
| cutadapt | `cutadapt` | qc_preprocessing | not_available_current_environment | pass |  |
| DIA-NN | `diann` | proteomics_metabolomics | not_available_current_environment | pass |  |
| eggNOG-mapper | `emapper.py` | genome_assembly_annotation | not_available_current_environment | pass |  |
| fastp | `fastp` | qc_preprocessing | not_available_current_environment | pass |  |
| FastQC | `fastqc` | qc_preprocessing | not_available_current_environment | pass |  |
| FastTree | `FastTree` | phylogenetics_comparative_genomics | not_available_current_environment | pass |  |
| featureCounts | `featureCounts` | rna_seq_quantification | not_available_current_environment | pass |  |
| FIMO | `fimo` | epigenomics_peak_calling | not_available_current_environment | pass |  |
| Flye | `flye` | genome_assembly_annotation | not_available_current_environment | pass |  |
| FreeBayes | `freebayes` | variant_calling | not_available_current_environment | pass |  |
| HH-suite | `hhsearch` | structure_modeling | not_available_current_environment | pass |  |
| HISAT2 | `hisat2` | spliced_rna_alignment | not_available_current_environment | pass |  |
| HMMER | `hmmsearch` | structure_modeling | not_available_current_environment | pass |  |
| HOMER | `findMotifsGenome.pl` | epigenomics_peak_calling | not_available_current_environment | pass |  |
| HTSlib | `bgzip` | alignment_file_operations | not_available_current_environment | pass |  |
| HUMAnN | `humann` | microbiome_metagenomics | not_available_current_environment | pass |  |
| InterProScan | `interproscan.sh` | genome_assembly_annotation | not_available_current_environment | pass |  |
| IQ-TREE | `iqtree2` | phylogenetics_comparative_genomics | not_available_current_environment | pass |  |
| kallisto | `kallisto` | rna_seq_quantification | not_available_current_environment | pass |  |
| Kraken2 | `kraken2` | microbiome_metagenomics | not_available_current_environment | pass |  |
| LAST | `lastal` | sequence_alignment | not_available_current_environment | pass |  |
| MACS2 | `macs2` | epigenomics_peak_calling | not_available_current_environment | pass |  |
| MACS3 | `macs3` | epigenomics_peak_calling | not_available_current_environment | pass |  |
| MAFFT | `mafft` | phylogenetics_comparative_genomics | not_available_current_environment | pass |  |
| MEGAHIT | `megahit` | genome_assembly_annotation | not_available_current_environment | pass |  |
| MEME | `meme` | epigenomics_peak_calling | not_available_current_environment | pass |  |
| MetaPhlAn | `metaphlan` | microbiome_metagenomics | not_available_current_environment | pass |  |
| minimap2 | `minimap2` | sequence_alignment | not_available_current_environment | pass |  |
| MultiQC | `multiqc` | qc_preprocessing | not_available_current_environment | pass |  |
| MUSCLE | `muscle` | phylogenetics_comparative_genomics | not_available_current_environment | pass |  |
| OrthoFinder | `orthofinder` | phylogenetics_comparative_genomics | not_available_current_environment | pass |  |
| Picard | `picard` | qc_preprocessing | not_available_current_environment | pass |  |
| Prokka | `prokka` | genome_assembly_annotation | not_available_current_environment | pass |  |
| QIIME2 | `qiime` | microbiome_metagenomics | not_available_current_environment | pass |  |
| Qualimap | `qualimap` | qc_preprocessing | not_available_current_environment | pass |  |
| QUAST | `quast.py` | genome_assembly_annotation | not_available_current_environment | pass |  |
| Raven | `raven` | genome_assembly_annotation | not_available_current_environment | pass |  |
| RAxML | `raxml-ng` | phylogenetics_comparative_genomics | not_available_current_environment | pass |  |
| RSEM | `rsem-calculate-expression` | rna_seq_quantification | not_available_current_environment | pass |  |
| Salmon | `salmon` | rna_seq_quantification | not_available_current_environment | pass |  |
| SAMtools | `samtools` | alignment_file_operations | not_available_current_environment | pass |  |
| SPAdes | `spades.py` | genome_assembly_annotation | not_available_current_environment | pass |  |
| STAR | `STAR` | spliced_rna_alignment | not_available_current_environment | pass |  |
| STARsolo | `STAR` | single_cell_analysis | not_available_current_environment | pass |  |
| Strelka2 | `configureStrelkaGermlineWorkflow.py` | variant_calling | not_available_current_environment | pass |  |
| StringTie | `stringtie` | rna_seq_quantification | not_available_current_environment | pass |  |
| Trim Galore | `trim_galore` | qc_preprocessing | not_available_current_environment | pass |  |
| Trimmomatic | `trimmomatic` | qc_preprocessing | not_available_current_environment | pass |  |

## Evidence Boundary / 证据边界

This eval executes only bounded CLI probe entrypoints. An `executed` status means the local command produced probe output. It does not mean OCEAN processed biological data, selected valid parameters, completed a workflow, benchmarked a method, or validated any scientific claim.
