# OCEAN Bioinformatics Wrapper Readiness Plan R1

- Run date: 2026-07-08
- Scope: all registered tools
- Tools planned: 115
- Mean readiness score: 8.05 / 10
- Local smoke already executed: 3
- Environment-missing but plan-ready: 112

## What This Adds

This R1 artifact turns the capability matrix into implementation plans for all registered tools. Each plan records the intended interface layer, a bounded smoke probe, candidate install/container routes, the minimal fixture needed, required run evidence, stop conditions, and OCEAN handoff.

It does not install or run the tools. Candidate install routes must be verified against current official documentation before use.

## Plan Table

| Tool | Family | Stage | Score | Interface | Smoke command | Handoff |
|---|---|---|---:|---|---|---|
| bcftools | alignment_file_operations | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bcftools --version` | Anchor |
| BEDTools | alignment_file_operations | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bedtools --version` | Anchor |
| HTSlib | alignment_file_operations | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bgzip --version` | Anchor |
| SAMtools | alignment_file_operations | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `samtools --version` | Anchor |
| DESeq2 | differential_expression | stage_2_local_smoke_executed | 10 | r_bioconductor_rscript | `Rscript -e "cat(as.character(utils::packageVersion('DESeq2')))"` | Anchor |
| edgeR | differential_expression | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_rscript | `Rscript -e "cat(as.character(utils::packageVersion('edgeR')))"` | Anchor |
| limma-voom | differential_expression | stage_2_local_smoke_executed | 10 | r_bioconductor_rscript | `Rscript -e "cat(as.character(utils::packageVersion('limma')))"` | Anchor |
| sleuth | differential_expression | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_or_rscript | `Rscript -e "cat(as.character(utils::packageVersion('sleuth')))"` | Anchor |
| deepTools | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import deeptools; print(getattr(deeptools, '__version__', 'version_not_exposed'))"` | Anchor |
| FIMO | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `fimo --version` | Anchor |
| HOMER | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `findMotifsGenome.pl --version` | Anchor |
| MACS2 | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `macs2 --version` | Anchor |
| MACS3 | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `macs3 --version` | Anchor |
| MEME | epigenomics_peak_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `meme --version` | Anchor |
| Bakta | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bakta --version` | Anchor |
| BUSCO | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `busco --version` | Anchor |
| Canu | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `canu --version` | Anchor |
| CheckM | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `checkm --version` | Anchor |
| eggNOG-mapper | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `emapper.py --version` | Anchor |
| Flye | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `flye --version` | Anchor |
| InterProScan | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `interproscan.sh --version` | Anchor |
| MEGAHIT | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `megahit --version` | Anchor |
| Prokka | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `prokka --version` | Anchor |
| QUAST | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `quast.py --version` | Anchor |
| Raven | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `raven --version` | Anchor |
| SPAdes | genome_assembly_annotation | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `spades.py --version` | Anchor |
| 3D Slicer | imaging_signal_ml | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `Slicer --version` | Anchor |
| ITK-SNAP | imaging_signal_ml | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `itksnap --version` | Anchor |
| MONAI | imaging_signal_ml | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import monai; print(getattr(monai, '__version__', 'version_not_exposed'))"` | Anchor |
| nnU-Net | imaging_signal_ml | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `nnUNetv2_train --version` | Anchor |
| SimpleITK | imaging_signal_ml | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import SimpleITK; print(getattr(SimpleITK, '__version__', 'version_not_exposed'))"` | Anchor |
| TorchIO | imaging_signal_ml | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import torchio; print(getattr(torchio, '__version__', 'version_not_exposed'))"` | Anchor |
| Bracken | microbiome_metagenomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bracken --version` | Anchor |
| DADA2 | microbiome_metagenomics | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_rscript | `Rscript -e "cat(as.character(utils::packageVersion('dada2')))"` | Anchor |
| HUMAnN | microbiome_metagenomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `humann --version` | Anchor |
| Kraken2 | microbiome_metagenomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `kraken2 --version` | Anchor |
| MetaPhlAn | microbiome_metagenomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `metaphlan --version` | Anchor |
| QIIME2 | microbiome_metagenomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `qiime --version` | Anchor |
| DIABLO | multi_omics_integration | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import mixomics; print(getattr(mixomics, '__version__', 'version_not_exposed'))"` | Anchor |
| mixOmics | multi_omics_integration | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_or_rscript | `Rscript -e "cat(as.character(utils::packageVersion('mixOmics')))"` | Anchor |
| MOFA | multi_omics_integration | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import mofapy2; print(getattr(mofapy2, '__version__', 'version_not_exposed'))"` | Anchor |
| MOFA+ | multi_omics_integration | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import mofapy2; print(getattr(mofapy2, '__version__', 'version_not_exposed'))"` | Anchor |
| WGCNA | multi_omics_integration | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_or_rscript | `Rscript -e "cat(as.character(utils::packageVersion('WGCNA')))"` | Anchor |
| Clustal Omega | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `clustalo --version` | Anchor |
| FastTree | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `FastTree --version` | Anchor |
| IQ-TREE | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `iqtree2 --version` | Anchor |
| MAFFT | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `mafft --version` | Anchor |
| MUSCLE | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `muscle --version` | Anchor |
| OrthoFinder | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `orthofinder --version` | Anchor |
| RAxML | phylogenetics_comparative_genomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `raxmlHPC --version` | Anchor |
| DIA-NN | proteomics_metabolomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `diann --version` | Anchor |
| FragPipe | proteomics_metabolomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `fragpipe --help` | Anchor |
| MaxQuant | proteomics_metabolomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `MaxQuantCmd --version` | Anchor |
| MS-DIAL | proteomics_metabolomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `MSDIAL --version` | Anchor |
| MZmine | proteomics_metabolomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `mzmine --help` | Anchor |
| Skyline | proteomics_metabolomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `SkylineCmd --version` | Anchor |
| XCMS | proteomics_metabolomics | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_or_rscript | `Rscript -e "cat(as.character(utils::packageVersion('xcms')))"` | Anchor |
| cutadapt | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `cutadapt --version` | Anchor |
| fastp | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `fastp --version` | Anchor |
| FastQC | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `fastqc --version` | Anchor |
| MultiQC | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `multiqc --version` | Anchor |
| Picard | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `picard --help` | Anchor |
| Qualimap | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `qualimap --version` | Anchor |
| Trim Galore | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `trim_galore --version` | Anchor |
| Trimmomatic | qc_preprocessing | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `trimmomatic --help` | Anchor |
| featureCounts | rna_seq_quantification | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `featureCounts --version` | Anchor |
| kallisto | rna_seq_quantification | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `kallisto --version` | Anchor |
| RSEM | rna_seq_quantification | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `rsem-calculate-expression --version` | Anchor |
| Salmon | rna_seq_quantification | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `salmon --version` | Anchor |
| StringTie | rna_seq_quantification | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `stringtie --version` | Anchor |
| BLAST | sequence_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `blastp -version` | Anchor |
| Bowtie2 | sequence_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bowtie2 --version` | Anchor |
| BWA | sequence_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `bwa --version` | Anchor |
| LAST | sequence_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `lastal --version` | Anchor |
| minimap2 | sequence_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `minimap2 --version` | Anchor |
| Alevin-fry | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `alevin-fry --version` | Anchor |
| Azimuth | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_or_rscript | `Rscript -e "cat(as.character(utils::packageVersion('Azimuth')))"` | Anchor |
| Cell Ranger | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `cellranger --version` | Anchor |
| CellTypist | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import celltypist; print(getattr(celltypist, '__version__', 'version_not_exposed'))"` | Anchor |
| Scanpy | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import scanpy; print(getattr(scanpy, '__version__', 'version_not_exposed'))"` | Anchor |
| scVI | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import scvi; print(getattr(scvi, '__version__', 'version_not_exposed'))"` | Anchor |
| Seurat | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | r_bioconductor_rscript | `Rscript -e "cat(as.character(utils::packageVersion('Seurat')))"` | Anchor |
| STARsolo | single_cell_analysis | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `STAR --version` | Anchor |
| cell2location | spatial_transcriptomics | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import cell2location; print(getattr(cell2location, '__version__', 'version_not_exposed'))"` | Anchor |
| Giotto | spatial_transcriptomics | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import giotto; print(getattr(giotto, '__version__', 'version_not_exposed'))"` | Anchor |
| Space Ranger | spatial_transcriptomics | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `spaceranger --version` | Anchor |
| Squidpy | spatial_transcriptomics | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import squidpy; print(getattr(squidpy, '__version__', 'version_not_exposed'))"` | Anchor |
| Stereoscope | spatial_transcriptomics | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import stereoscope; print(getattr(stereoscope, '__version__', 'version_not_exposed'))"` | Anchor |
| stLearn | spatial_transcriptomics | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import stlearn; print(getattr(stlearn, '__version__', 'version_not_exposed'))"` | Anchor |
| Tangram | spatial_transcriptomics | stage_1_plan_ready_environment_missing | 8 | python_import_or_subprocess | `python3 -c "import tangram; print(getattr(tangram, '__version__', 'version_not_exposed'))"` | Anchor |
| HISAT2 | spliced_rna_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `hisat2 --version` | Anchor |
| STAR | spliced_rna_alignment | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `STAR --version` | Anchor |
| AlphaFold | structure_modeling | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `run_alphafold.py --version` | Anchor |
| AlphaFold DB | structure_modeling | stage_2_local_smoke_executed | 10 | heavy_cli_api_or_container_launcher | `"alphafold db" --version` | Anchor |
| ChimeraX | structure_modeling | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `ChimeraX --version` | Anchor |
| ColabFold | structure_modeling | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `colabfold_batch --version` | Anchor |
| HH-suite | structure_modeling | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `hhsearch -h` | Anchor |
| HMMER | structure_modeling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `hmmsearch -h` | Anchor |
| MODELLER | structure_modeling | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `mod9.25 --version` | Anchor |
| PyMOL | structure_modeling | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `pymol --version` | Anchor |
| RoseTTAFold | structure_modeling | stage_1_plan_ready_environment_missing | 8 | heavy_cli_api_or_container_launcher | `rosettafold --version` | Anchor |
| DeepVariant | variant_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `run_deepvariant --version` | Anchor |
| FreeBayes | variant_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `freebayes --version` | Anchor |
| GATK | variant_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `gatk --help` | Anchor |
| Mutect2 | variant_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `gatk --help` | Anchor |
| Strelka2 | variant_calling | stage_1_plan_ready_environment_missing | 8 | lightweight_cli_subprocess | `configureStrelkaGermlineWorkflow.py --version` | Anchor |
| Conda | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_or_runtime_subprocess | `conda --version` | Harbor |
| CWL | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_or_runtime_subprocess | `cwltool --version` | Harbor |
| Docker | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `docker --version` | Harbor |
| Galaxy | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_or_runtime_subprocess | `galaxy --help` | Harbor |
| Nextflow | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `nextflow -version` | Harbor |
| nf-core | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_or_runtime_subprocess | `nf-core --version` | Harbor |
| Singularity-Apptainer | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `apptainer --version` | Harbor |
| Snakemake | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_reproducibility | `snakemake --version` | Harbor |
| WDL-Cromwell | workflow_reproducibility | stage_1_plan_ready_environment_missing | 8 | workflow_or_runtime_subprocess | `cromwell --version` | Harbor |

## Next Implementation Order

1. **AlphaFold DB**: stage_2_local_smoke_executed; next step is to collect a real run record or verify/install the environment, then create a source packet.
2. **DESeq2**: stage_2_local_smoke_executed; next step is to collect a real run record or verify/install the environment, then create a source packet.
3. **limma-voom**: stage_2_local_smoke_executed; next step is to collect a real run record or verify/install the environment, then create a source packet.
4. **Alevin-fry**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
5. **AlphaFold**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
6. **Azimuth**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
7. **Bakta**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
8. **bcftools**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
9. **BEDTools**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
10. **BLAST**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
11. **Bowtie2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
12. **Bracken**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
13. **BUSCO**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
14. **BWA**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
15. **Canu**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
16. **cell2location**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
17. **Cell Ranger**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
18. **CellTypist**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
19. **CheckM**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
20. **ChimeraX**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
21. **Clustal Omega**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
22. **ColabFold**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
23. **Conda**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
24. **cutadapt**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
25. **CWL**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
26. **DADA2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
27. **deepTools**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
28. **DeepVariant**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
29. **DIA-NN**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
30. **DIABLO**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
31. **Docker**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
32. **edgeR**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
33. **eggNOG-mapper**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
34. **fastp**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
35. **FastQC**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
36. **FastTree**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
37. **featureCounts**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
38. **FIMO**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
39. **Flye**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
40. **FragPipe**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
41. **FreeBayes**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
42. **Galaxy**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
43. **GATK**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
44. **Giotto**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
45. **HH-suite**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
46. **HISAT2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
47. **HMMER**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
48. **HOMER**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
49. **HTSlib**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
50. **HUMAnN**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
51. **InterProScan**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
52. **IQ-TREE**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
53. **ITK-SNAP**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
54. **kallisto**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
55. **Kraken2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
56. **LAST**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
57. **MACS2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
58. **MACS3**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
59. **MAFFT**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
60. **MaxQuant**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
61. **MEGAHIT**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
62. **MEME**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
63. **MetaPhlAn**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
64. **minimap2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
65. **mixOmics**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
66. **MODELLER**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
67. **MOFA**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
68. **MOFA+**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
69. **MONAI**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
70. **MS-DIAL**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
71. **MultiQC**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
72. **MUSCLE**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
73. **Mutect2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
74. **MZmine**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
75. **Nextflow**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
76. **nf-core**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
77. **nnU-Net**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
78. **OrthoFinder**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
79. **Picard**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
80. **Prokka**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
81. **PyMOL**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
82. **QIIME2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
83. **Qualimap**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
84. **QUAST**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
85. **Raven**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
86. **RAxML**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
87. **RoseTTAFold**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
88. **RSEM**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
89. **Salmon**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
90. **SAMtools**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
91. **Scanpy**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
92. **scVI**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
93. **Seurat**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
94. **SimpleITK**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
95. **Singularity-Apptainer**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
96. **Skyline**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
97. **sleuth**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
98. **Snakemake**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
99. **Space Ranger**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
100. **SPAdes**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
101. **Squidpy**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
102. **STAR**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
103. **STARsolo**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
104. **Stereoscope**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
105. **stLearn**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
106. **Strelka2**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
107. **StringTie**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
108. **Tangram**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
109. **3D Slicer**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
110. **TorchIO**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
111. **Trim Galore**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
112. **Trimmomatic**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
113. **WDL-Cromwell**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
114. **WGCNA**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.
115. **XCMS**: stage_1_plan_ready_environment_missing; next step is to collect a real run record or verify/install the environment, then create a source packet.

## Evidence Boundary / 证据边界

- `stage_2_local_smoke_executed` means a bounded local version/package probe existed in the capability matrix, not a biological analysis.
- `stage_1_plan_ready_environment_missing` means OCEAN has a plan, but local execution is unavailable until the environment/tool/container is supplied.
- Candidate install routes are planning notes and must be verified against official/current documentation before use.
- These plans cannot support mechanism, causality, clinical utility, reproducibility, or publication readiness without inspected run records and downstream OCEAN audit.
