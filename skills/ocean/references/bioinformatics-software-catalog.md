# Bioinformatics Software Catalog

Use this reference when OCEAN needs to route bioinformatics, computational biology, biomedical AI, omics, clinical-data, or workflow-tool requests.

This catalog is a routing and source-packet contract. It does not mean OCEAN has run the tool, installed the tool, validated tool output, or verified that a tool is appropriate for a specific dataset.

## Core rule

Tool presence is not evidence. A tool name becomes evidence only after OCEAN has a source packet containing tool version, command line, parameters, reference/index, input files, output files, logs/QC, environment, date, and inspected result fields.

## Required software source packet

| Field | Required content |
|---|---|
| Tool identity | name, version, official URL or citation if available |
| Task intent | QC, alignment, quantification, variant calling, clustering, enrichment, prediction, visualization, workflow orchestration, or other |
| Input files | file names, formats, sample identifiers, privacy/access boundary |
| Reference/index/database | genome build, transcriptome, protein database, library, panel, ontology, or model checkpoint |
| Command line | exact command, config, workflow file, or notebook cell |
| Parameters | thresholds, filters, seeds, threads, memory, scoring scheme, model options |
| Environment | OS/container, package manager, dependency versions, hardware if relevant |
| Output files | paths, formats, checksums if available, inspected fields |
| Logs/QC | warnings, failure modes, runtime errors, quality metrics |
| Interpretation boundary | what the output can and cannot support |
| Next OCEAN module | Reef for resource provenance, Anchor for reproducibility/validation, Iceberg for claim audit, Compass for experiment design |

## Common software families

| Family | Tools to route | Typical outputs | Cannot support alone |
|---|---|---|---|
| Raw-read QC and trimming | FastQC, MultiQC, fastp, cutadapt, Trimmomatic, Trim Galore, BBTools/BBduk, seqkit, seqtk, Picard, Qualimap | QC reports, trimmed reads, duplication/quality summaries | biological validity, correct study design, absence of batch effects |
| Sequence search and alignment | BLAST, LAST/LASTAL, minimap2, BWA, Bowtie2, HISAT2, STAR, BBMap, DIAMOND, MMseqs2, GraphMap | alignments, mapping stats, homology hits, SAM/BAM/PAF/MAF | function, mechanism, orthology, or clinical relevance without downstream evidence |
| File operations and intervals | SAMtools, bcftools, BEDTools, HTSlib, BEDOPS, UCSC command-line utilities, CrossMap, liftOver | sorted/indexed files, VCF/BED operations, coordinate conversion | biological interpretation, genome-build correctness unless checked |
| Variant calling and annotation | GATK, HaplotypeCaller, Mutect2, bcftools, FreeBayes, DeepVariant, Strelka2, VarScan, VarDict, Manta, Delly, LUMPY, CNVkit, Control-FREEC, FACETS, PureCN, VEP, ANNOVAR, SnpEff, SnpSift, PLINK, BOLT-LMM, SAIGE, REGENIE | VCF, CNV/SV calls, annotations, GWAS outputs | pathogenicity, clonality, treatment guidance, or causal genetics by itself |
| RNA-seq quantification and DE | STAR, HISAT2, Salmon, kallisto, RSEM, StringTie, featureCounts, HTSeq-count, DESeq2, edgeR, limma-voom, sleuth, tximport, fgsea | count matrices, transcript estimates, DE tables, enrichment tables | causality, mechanism, cell-type specificity, or clinical utility |
| Single-cell analysis | Cell Ranger, STARsolo, Alevin-fry, kallisto bustools, Seurat, Scanpy, scVI, scANVI, scArches, Harmony, LIGER, BBKNN, SoupX, Scrublet, DoubletFinder, CellTypist, SingleR, Azimuth, scPred | matrices, embeddings, clusters, annotations, integration outputs | validated cell identity, causal biology, clinical marker readiness |
| Spatial and multimodal omics | Space Ranger, Squidpy, Giotto, Seurat spatial, Scanpy spatial, cell2location, Tangram, Stereoscope, SPOTlight, BayesSpace, SpaGCN, SpatialDE, stLearn, MOFA/MOFA+, WNN workflows | spatial clusters, deconvolution, neighborhood statistics, modality integration | physical interaction, causal communication, therapeutic mechanism |
| Epigenomics and regulation | MACS2/MACS3, deepTools, HOMER, MEME/FIMO, Bismark, methylKit, ChromHMM, DiffBind, ChIPseeker, ATACseqQC, HINT-ATAC, TOBIAS, ArchR, Signac | peaks, motifs, coverage tracks, methylation calls, chromatin states | direct binding, functional regulation, or causal gene control without validation |
| Genome assembly and annotation | Flye, Canu, Raven, SPAdes, MEGAHIT, metaSPAdes, QUAST, BUSCO, CheckM/CheckM2, GTDB-Tk, Prokka, Bakta, eggNOG-mapper, InterProScan, Roary, Panaroo | assemblies, bins, annotations, pangenomes, completeness/contamination reports | pathogenicity, function, or evolutionary conclusion without support |
| Microbiome and metagenomics | QIIME2, DADA2, mothur, VSEARCH, MetaPhlAn, HUMAnN, Kraken2, Bracken, Kaiju, Centrifuge, Sourmash, Mash, PICRUSt2, phyloseq, ANCOM-BC, MaAsLin2 | ASV/OTU tables, taxonomic profiles, functional profiles, diversity stats | treatment mechanism, causality, host-response proof |
| Proteomics | MaxQuant, FragPipe, MSFragger, DIA-NN, Skyline, OpenMS, Proteome Discoverer, Spectronaut, Perseus | peptide/protein IDs, quantification tables, FDR/QC reports | protein causality, pathway mechanism, clinical biomarker readiness |
| Metabolomics and lipidomics | XCMS, MZmine, MS-DIAL, OpenMS, GNPS, MetaboAnalyst, LipidSearch, Skyline | feature tables, putative IDs, pathway summaries, spectral matches | definitive metabolite identity, pathway causality, intervention effect |
| Structure and protein modeling | AlphaFold, AlphaFold DB, ColabFold, RoseTTAFold, ESMFold, HH-suite, HMMER, MODELLER, Rosetta, FoldX, PyMOL, ChimeraX, Mol*, AutoDock Vina, HADDOCK | predicted structures, confidence, alignments, visualizations, docking poses | binding proof, function, mechanism, druggability, clinical relevance |
| Phylogenetics and comparative genomics | MAFFT, MUSCLE, Clustal Omega, IQ-TREE, RAxML, FastTree, BEAST, OrthoFinder, OrthoMCL, HyPhy, PAML, ClonalFrameML | MSAs, trees, orthogroups, selection tests | evolutionary conclusion without sampling/model/support checks |
| Imaging and signal analysis | nnU-Net, MONAI, TorchIO, SimpleITK, ITK-SNAP, 3D Slicer, QuPath, CellProfiler, Fiji/ImageJ, napari, ilastik, MNE, WFDB tools | segmentations, features, preprocessing outputs, model metrics | clinical utility, prospective performance, deployment readiness |
| Workflow and reproducibility | Snakemake, Nextflow, nf-core, CWL, WDL/Cromwell, Galaxy, Docker, Singularity/Apptainer, Conda, Mamba, Bioconda, renv, workflowr | pipelines, DAGs, containers, lock files, reports | successful execution, valid parameters, biological correctness |
| Statistical and ML frameworks | R/Bioconductor, Python/scikit-learn, PyTorch, TensorFlow, XGBoost, LightGBM, tidymodels, mlr3, caret | model outputs, statistics, notebooks, fitted objects | leakage-free validation, causal inference, or external generalization by itself |

## LAST-specific handling

LAST/LASTAL should be routed as sequence search/alignment. Required extra fields are:

- scoring matrix or scoring scheme;
- database/index build command if available;
- alignment threshold/filter;
- MAF/tabular output fields inspected;
- repeat/masking strategy when relevant.

LAST output can support alignment evidence and candidate homology. It cannot by itself prove function, mechanism, pathogen attribution, clinical relevance, or evolutionary conclusion.

## Safe wording

Use:

- "This tool is a candidate route for..."
- "A valid software packet would need..."
- "The current evidence is only software-routing support."
- "The output could be handed to Anchor for reproducibility checks."

Avoid:

- "Running this tool proves..."
- "The tool confirms the mechanism..."
- "The workflow is reproducible" without logs/environment/output checks.
- "The model is clinically useful" from software metrics alone.

