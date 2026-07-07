# OCEAN Bioinformatics Code Coverage Eval R1

- Run date: 2026-07-08
- Tools checked: 115
- Pass: 115
- Needs review: 0

## Execution Layer Counts

| Layer | Count |
|---|---:|
| heavy_launcher_plan | 20 |
| lightweight_cli | 60 |
| python_package | 16 |
| r_bioconductor | 10 |
| source_packet_adapter | 1 |
| workflow_runtime | 8 |

## Tool Results

| Tool | Layer | Runner | Verdict | Issues |
|---|---|---|---|---|
| alevin_fry | lightweight_cli | `scripts/run_cli.py` | pass |  |
| alphafold | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| alphafold_db | source_packet_adapter | `scripts/run_launcher.py` | pass |  |
| azimuth | r_bioconductor | `scripts/run_package.py` | pass |  |
| bakta | lightweight_cli | `scripts/run_cli.py` | pass |  |
| bcftools | lightweight_cli | `scripts/run_cli.py` | pass |  |
| bedtools | lightweight_cli | `scripts/run_cli.py` | pass |  |
| blast | lightweight_cli | `scripts/run_cli.py` | pass |  |
| bowtie2 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| bracken | lightweight_cli | `scripts/run_cli.py` | pass |  |
| busco | lightweight_cli | `scripts/run_cli.py` | pass |  |
| bwa | lightweight_cli | `scripts/run_cli.py` | pass |  |
| canu | lightweight_cli | `scripts/run_cli.py` | pass |  |
| cell2location | python_package | `scripts/run_package.py` | pass |  |
| cell_ranger | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| celltypist | python_package | `scripts/run_package.py` | pass |  |
| checkm | lightweight_cli | `scripts/run_cli.py` | pass |  |
| chimerax | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| clustal_omega | lightweight_cli | `scripts/run_cli.py` | pass |  |
| colabfold | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| conda | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| cutadapt | lightweight_cli | `scripts/run_cli.py` | pass |  |
| cwl | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| dada2 | r_bioconductor | `scripts/run_package.py` | pass |  |
| deeptools | python_package | `scripts/run_package.py` | pass |  |
| deepvariant | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| deseq2 | r_bioconductor | `scripts/run_package.py` | pass |  |
| dia_nn | lightweight_cli | `scripts/run_cli.py` | pass |  |
| diablo | python_package | `scripts/run_package.py` | pass |  |
| docker | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| edger | r_bioconductor | `scripts/run_package.py` | pass |  |
| eggnog_mapper | lightweight_cli | `scripts/run_cli.py` | pass |  |
| fastp | lightweight_cli | `scripts/run_cli.py` | pass |  |
| fastqc | lightweight_cli | `scripts/run_cli.py` | pass |  |
| fasttree | lightweight_cli | `scripts/run_cli.py` | pass |  |
| featurecounts | lightweight_cli | `scripts/run_cli.py` | pass |  |
| fimo | lightweight_cli | `scripts/run_cli.py` | pass |  |
| flye | lightweight_cli | `scripts/run_cli.py` | pass |  |
| fragpipe | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| freebayes | lightweight_cli | `scripts/run_cli.py` | pass |  |
| galaxy | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| gatk | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| giotto | python_package | `scripts/run_package.py` | pass |  |
| hh_suite | lightweight_cli | `scripts/run_cli.py` | pass |  |
| hisat2 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| hmmer | lightweight_cli | `scripts/run_cli.py` | pass |  |
| homer | lightweight_cli | `scripts/run_cli.py` | pass |  |
| htslib | lightweight_cli | `scripts/run_cli.py` | pass |  |
| humann | lightweight_cli | `scripts/run_cli.py` | pass |  |
| interproscan | lightweight_cli | `scripts/run_cli.py` | pass |  |
| iq_tree | lightweight_cli | `scripts/run_cli.py` | pass |  |
| itk_snap | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| kallisto | lightweight_cli | `scripts/run_cli.py` | pass |  |
| kraken2 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| last | lightweight_cli | `scripts/run_cli.py` | pass |  |
| limma_voom | r_bioconductor | `scripts/run_package.py` | pass |  |
| macs2 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| macs3 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| mafft | lightweight_cli | `scripts/run_cli.py` | pass |  |
| maxquant | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| megahit | lightweight_cli | `scripts/run_cli.py` | pass |  |
| meme | lightweight_cli | `scripts/run_cli.py` | pass |  |
| metaphlan | lightweight_cli | `scripts/run_cli.py` | pass |  |
| minimap2 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| mixomics | r_bioconductor | `scripts/run_package.py` | pass |  |
| modeller | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| mofa | python_package | `scripts/run_package.py` | pass |  |
| mofaplus | python_package | `scripts/run_package.py` | pass |  |
| monai | python_package | `scripts/run_package.py` | pass |  |
| ms_dial | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| multiqc | lightweight_cli | `scripts/run_cli.py` | pass |  |
| muscle | lightweight_cli | `scripts/run_cli.py` | pass |  |
| mutect2 | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| mzmine | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| nextflow | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| nf_core | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| nnu_net | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| orthofinder | lightweight_cli | `scripts/run_cli.py` | pass |  |
| picard | lightweight_cli | `scripts/run_cli.py` | pass |  |
| prokka | lightweight_cli | `scripts/run_cli.py` | pass |  |
| pymol | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| qiime2 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| qualimap | lightweight_cli | `scripts/run_cli.py` | pass |  |
| quast | lightweight_cli | `scripts/run_cli.py` | pass |  |
| raven | lightweight_cli | `scripts/run_cli.py` | pass |  |
| raxml | lightweight_cli | `scripts/run_cli.py` | pass |  |
| rosettafold | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| rsem | lightweight_cli | `scripts/run_cli.py` | pass |  |
| salmon | lightweight_cli | `scripts/run_cli.py` | pass |  |
| samtools | lightweight_cli | `scripts/run_cli.py` | pass |  |
| scanpy | python_package | `scripts/run_package.py` | pass |  |
| scvi | python_package | `scripts/run_package.py` | pass |  |
| seurat | r_bioconductor | `scripts/run_package.py` | pass |  |
| simpleitk | python_package | `scripts/run_package.py` | pass |  |
| singularity_apptainer | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| skyline | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| sleuth | r_bioconductor | `scripts/run_package.py` | pass |  |
| snakemake | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| space_ranger | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| spades | lightweight_cli | `scripts/run_cli.py` | pass |  |
| squidpy | python_package | `scripts/run_package.py` | pass |  |
| star | lightweight_cli | `scripts/run_cli.py` | pass |  |
| starsolo | lightweight_cli | `scripts/run_cli.py` | pass |  |
| stereoscope | python_package | `scripts/run_package.py` | pass |  |
| stlearn | python_package | `scripts/run_package.py` | pass |  |
| strelka2 | lightweight_cli | `scripts/run_cli.py` | pass |  |
| stringtie | lightweight_cli | `scripts/run_cli.py` | pass |  |
| tangram | python_package | `scripts/run_package.py` | pass |  |
| three_d_slicer | heavy_launcher_plan | `scripts/run_launcher.py` | pass |  |
| torchio | python_package | `scripts/run_package.py` | pass |  |
| trim_galore | lightweight_cli | `scripts/run_cli.py` | pass |  |
| trimmomatic | lightweight_cli | `scripts/run_cli.py` | pass |  |
| wdl_cromwell | workflow_runtime | `scripts/run_launcher.py` | pass |  |
| wgcna | r_bioconductor | `scripts/run_package.py` | pass |  |
| xcms | r_bioconductor | `scripts/run_package.py` | pass |  |

## Boundary

This eval checks whether each bioinformatics tool folder has the required code files, API commands, generic source-packet wrapper, per-tool probe/plan wrapper, and execution-layer-specific runner. It does not prove local tool installation, workflow execution, benchmark validity, or scientific claim support.
