# Bioinformatics Resource Map

Use this reference when OCEAN needs to route biomedical, biological, bioinformatics, computational biology, omics, variant, pathway, protein, drug-target, clinical, or benchmark evidence.

## Core rule

Resource presence is not evidence. A named database is only a candidate route until OCEAN has a recorded query, identifiers, date, inspected fields, and source-packet limitations.

## Common resource families

| Family | Common resources | Best used for | Boundary warning |
|---|---|---|---|
| Literature and metadata | PubMed, EuropePMC, CrossRef, OpenAlex, Semantic Scholar, arXiv, bioRxiv, medRxiv | source discovery, citation graph, source corpus | title/abstract metadata is not full-text evidence |
| Sequence and raw reads | GenBank, RefSeq, ENA, DDBJ, SRA | sequence existence, raw read archives, accession routing | accession existence does not prove sample quality or analysis validity |
| Expression and functional genomics | GEO, ArrayExpress, Expression Atlas, GTEx, ENCODE, Human Cell Atlas, Single Cell Portal, CELLxGENE | transcriptomics, single-cell, tissue expression, regulatory assays | dataset availability does not prove cohort suitability or biological mechanism |
| Spatial / multimodal atlases | HuBMAP, Human Cell Atlas, CZ CELLxGENE, Single Cell Portal, Xenium/Visium-associated public portals when source-linked | spatial/multimodal tissue context, atlas comparison, cell-state hypotheses | atlas similarity or spatial proximity is not causal mechanism or clinical validation |
| Epigenomics and regulatory evidence | ENCODE, Cistrome DB, ReMap, JASPAR, UCSC Genome Browser, Roadmap Epigenomics | ChIP/ATAC peaks, motif scans, regulatory annotations | peak/motif evidence is candidate regulation, not direct binding or functional causality |
| Cancer genomics | TCGA/GDC, cBioPortal, ICGC, COSMIC | cancer mutations, copy number, expression, survival associations | retrospective association does not prove mechanism or treatment guidance |
| Variants and genetics | ClinVar, dbSNP, gnomAD, Ensembl/VEP, UCSC Genome Browser, GWAS Catalog, OMIM | variant annotation, population frequency, phenotype association, genome build checks | pathogenicity labels and GWAS hits are not causal proof without context |
| Protein and structure | UniProt, RCSB PDB, AlphaFold DB, InterPro, Pfam, STRING, BioGRID, IntAct | protein function, domains, structures, interactions | predicted structure or interaction annotation is not binding/functional proof |
| Pathways and gene sets | Gene Ontology, Reactome, KEGG, WikiPathways, MSigDB, GSEA resources | pathway enrichment, function categories, gene-set interpretation | enrichment is hypothesis-generating and sensitive to background/gene-set choice |
| Drug and target | ChEMBL, OpenTargets, PubChem, BindingDB, DrugBank, PharmGKB, DGIdb, OpenFDA | compounds, targets, assays, adverse events, target-disease links | bioactivity or target association is not therapeutic efficacy |
| Regulatory and safety | OpenFDA, DailyMed, FDA labels, EMA public assessment reports, FAERS with caveats | label context, adverse-event signal triage, safety annotation | spontaneous reports and label metadata do not prove causality or comparative safety |
| Proteomics and metabolomics | PRIDE, ProteomeXchange, PeptideAtlas, MetaboLights, HMDB, MassIVE | proteomics/metabolomics datasets and identifiers | detected molecule or protein is not necessarily causal or clinically actionable |
| Microbiome | MGnify, Qiita, Human Microbiome Project, SRA/ENA microbiome studies | microbiome datasets, taxonomic/functional profiles | compositional association is not mechanism or treatment response proof |
| Clinical and cohorts | ClinicalTrials.gov, WHO ICTRP, EU Clinical Trials Register, MIMIC/eICU when lawful, UK Biobank when authorized, SEER, NHANES, All of Us when authorized | trial registration, cohort context, clinical endpoints | registry existence is not trial result; controlled cohorts require access/ethics boundary |
| Clinical imaging and physiological signals | TCIA, PhysioNet, MIMIC-CXR when lawful, OpenNeuro, UK Biobank imaging when authorized | imaging/signal benchmark provenance, modality and label routing | dataset existence is not deployability, clinical utility, or prospective validation |
| Model organism databases | MGI, FlyBase, WormBase, SGD, ZFIN, TAIR | gene function and phenotype evidence in model organisms | organism evidence must be translated cautiously to human biology |
| Benchmarks and challenges | DREAM Challenges, OpenML where relevant, Kaggle only with caution, task-specific benchmark repositories | benchmark context, challenge tasks, baseline comparison | leaderboard performance is not biological validity or clinical deployment readiness |
| Bioinformatics software / workflows | FastQC, MultiQC, BLAST, LAST/LASTAL, minimap2, BWA, Bowtie2, HISAT2, STAR, SAMtools, BEDTools, GATK, bcftools, DeepVariant, Salmon, kallisto, featureCounts, DESeq2, edgeR, Seurat, Scanpy, Cell Ranger, QIIME2, MetaPhlAn, HUMAnN, AlphaFold, MaxQuant, XCMS, nnU-Net, MONAI, Snakemake, Nextflow, Galaxy | workflow provenance, method routing, reproducibility checks, software-generated artifacts | software use does not prove correct parameters, data quality, reproducibility, or biological interpretation |

## Minimum source-packet fields by family

| Family | Must record before evidence use |
|---|---|
| Literature | query, date, source, PMID/DOI/arXiv ID if returned, inspected title/abstract/full text boundary |
| Raw reads / omics | accession, organism, assay/platform, sample table, condition labels, inspected metadata fields |
| Cancer genomics | cohort, data type, endpoint definition, filters, version/access date, analysis boundary |
| Variants | variant ID, genome build/transcript, phenotype context, submitter/evidence status, date |
| Protein/structure | accession/structure ID, evidence level, organism/isoform, confidence/resolution limits |
| Pathway/gene set | gene list, background set, database version/date, enrichment method, multiple-testing handling |
| Drug/target | compound/target ID, assay type, endpoint, organism/cell line, concentration/unit, date |
| Clinical | registry/cohort ID, status/date, endpoint, population, access/ethics boundary |
| Artifact/benchmark | code/data version, inputs, parameters, environment, outputs, benchmark split |
| Software/workflow | tool name, version, command line, parameters, reference/index, input files, output files, logs, environment, date |
| Imaging/signal | dataset ID, modality, label definition, acquisition/preprocessing boundary, train/test split, privacy/access boundary |
| Regulatory/safety | product/drug ID, label/adverse-event field, date, reporter/source caveat, known reporting-bias limitations |

## Safe route language

Use:

- "Candidate resources to query include..."
- "This route could inspect..."
- "The current packet can support only..."
- "This database may provide identifiers, but no query has been inspected yet."

Avoid:

- "The database proves..."
- "This dataset confirms..."
- "The pathway analysis establishes a mechanism..."
- "The trial registry shows efficacy..."
- "The benchmark demonstrates clinical readiness..."

## Handoff guidance

| Situation | OCEAN handoff |
|---|---|
| Need to find source material | Sounding |
| Need to choose databases/resources | Reef |
| Need to judge trend/maturity from corpus | Current |
| Need to audit a claim using packet evidence | Iceberg |
| Need validation/reproducibility/benchmark gates | Anchor |
| Need experiment or research strategy | Compass |
| Need project memory or collaboration record | Harbor |

## Stop conditions

Stop or downgrade if:

- exact identifiers are requested but no query/API response is available;
- a route is being treated as evidence;
- a database annotation is being treated as mechanism proof;
- association/enrichment is being treated as causality;
- a registry record is being treated as trial result;
- controlled-access data is implied but not lawfully provided;
- tool output lacks date, version, filters, or inspected fields.
- software output lacks tool version, command line, parameters, reference/index, inputs, logs, or output provenance.

## Common bioinformatics software families

| Family | Common tools | OCEAN route use | Boundary warning |
|---|---|---|---|
| QC and preprocessing | FastQC, MultiQC, cutadapt, fastp, Trimmomatic, Trim Galore, Picard, Qualimap | raw/read-level QC, trimming, duplication, mapping-quality and batch-warning route | clean-looking QC is not biological validity or absence of bias |
| General sequence search/alignment | BLAST, LAST, minimap2, BWA, Bowtie2 | read/sequence alignment route, homology search, mapping provenance | alignment output depends on reference, index, scoring, thresholds, and filtering |
| Spliced RNA-seq alignment | STAR, HISAT2, minimap2 splice modes | RNA-seq mapping route and BAM/SJ artifact provenance | mapping rate or splice junction output is not differential expression or mechanism proof |
| Alignment/file operations | SAMtools, bcftools, BEDTools, HTSlib | BAM/CRAM/VCF/BED manipulation, interval overlap, indexing, QC route | file manipulation output is not biological interpretation without upstream/downstream context |
| Variant calling | GATK, bcftools, FreeBayes, DeepVariant, Strelka2, Mutect2 | variant-calling workflow route and VCF provenance | variant call is not pathogenicity, clonality, or treatment relevance by itself |
| RNA-seq quantification | Salmon, kallisto, RSEM, featureCounts, StringTie | gene/transcript count matrix provenance | counts require normalization, design matrix, batch/confounder handling |
| Differential expression | DESeq2, edgeR, limma-voom, sleuth | statistical comparison route | differential expression is association, not causal mechanism |
| Single-cell analysis | Cell Ranger, STARsolo, Alevin-fry, Seurat, Scanpy, scVI, CellTypist, Azimuth | cell-level matrix, clustering, annotation, integration route | cluster labels and marker genes need validation and annotation boundary |
| Spatial transcriptomics | Space Ranger, Squidpy, Giotto, cell2location, Tangram, Stereoscope, stLearn | spatial preprocessing, neighborhood analysis, deconvolution, mapping route | spatial proximity or cell-type deconvolution is not causal interaction proof |
| Epigenomics / peak calling | BWA/Bowtie2, MACS2/MACS3, deepTools, HOMER, MEME/FIMO | ChIP/ATAC peak and motif workflow route | peak/motif enrichment is candidate regulatory evidence, not direct binding proof |
| Genome assembly / annotation | Flye, Canu, Raven, SPAdes, MEGAHIT, QUAST, BUSCO, CheckM, Prokka, Bakta, eggNOG-mapper, InterProScan | assembly quality, completeness, contamination, genome/protein annotation route | assembly completeness or annotation similarity is not function, pathogenicity, or mechanism proof |
| Metagenomics / microbiome | QIIME2, DADA2, MetaPhlAn, HUMAnN, Kraken2, Bracken, MEGAHIT, SPAdes | taxonomic/functional profiling and assembly route | compositional profiles and taxa associations are not treatment mechanisms |
| Proteomics / metabolomics software | MaxQuant, FragPipe, DIA-NN, Skyline, MS-DIAL, XCMS, MZmine | peptide/protein/metabolite identification and quantification route | identification/quantification depends on library, FDR, calibration, and preprocessing |
| Structural / protein modeling | AlphaFold, ColabFold, RoseTTAFold, HH-suite, HMMER, MODELLER, PyMOL, ChimeraX | structure prediction, domain search, visualization route | predicted structure or visualization does not prove binding, function, or mechanism |
| Biomedical imaging / signal ML | nnU-Net, MONAI, TorchIO, SimpleITK, ITK-SNAP, 3D Slicer, Neuroimaging tools when source-linked | segmentation, preprocessing, annotation, model-evaluation route | image/signal model performance is not clinical utility without external/prospective validation |
| Phylogenetics / comparative genomics | MAFFT, MUSCLE, Clustal Omega, IQ-TREE, RAxML, FastTree, OrthoFinder | multiple alignment, tree, orthology route | tree topology depends on model, alignment quality, sampling, and support |
| Multi-omics integration | WGCNA, MOFA/MOFA+, mixOmics/DIABLO, network enrichment workflows | correlation modules, latent factors, feature integration, hypothesis prioritization route | integration patterns are not causality and require modality-specific validation |
| Workflow and reproducibility | Snakemake, Nextflow, CWL, WDL/Cromwell, Galaxy, Docker, Singularity/Apptainer, Conda, nf-core | pipeline provenance and reproducibility route | workflow existence is not successful execution or valid analysis |

For a fuller tool list and per-family packet rules, read `bioinformatics-software-catalog.md`.

Each tool listed in the software families now has a scaffold folder under `scripts/tools/bioinformatics/<tool_slug>/`. These folders define where tool-specific wrappers, examples, evals, and source-packet metadata should live. Folder presence is still only a scaffold; it does not mean the tool is installed, executable, or validated.

## LAST-specific note

LAST, associated with Martin Frith's `last` project, belongs to the sequence alignment/search route. In OCEAN, LAST output should be treated as alignment evidence only after recording tool version, database/index, scoring scheme, command line, input sequences, filters, and inspected alignments. It cannot by itself prove homology function, mechanism, clinical relevance, or evolutionary conclusion.
