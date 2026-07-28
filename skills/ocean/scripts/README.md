# OCEAN Tools and Scripts

[中文工具说明](README.zh-CN.md)

This directory contains OCEAN's executable helpers, source-packet adapters,
bioinformatics tool wrappers, and public database adapters.
The tool implementation lives under [`tools/`](tools/README.md).

## Read the status correctly

OCEAN distinguishes three different states:

| State | Meaning |
|---|---|
| **Covered** | OCEAN has a tool folder, routing metadata, examples, and a bounded wrapper contract |
| **Available** | The required executable, package, runtime, API, database, license, and compute are present in the current environment |
| **Executed** | A real command or query ran and its inputs, parameters, outputs, logs, versions, and environment were inspected |

A tool listed below is **covered**. It is not automatically available or
executed. A source packet records provenance and limitations; it does not by
itself validate a biological, causal, mechanistic, or clinical claim.

## What is included

| Tool layer | Current coverage | Main location |
|---|---:|---|
| Bioinformatics tool folders | 115 | [`tools/bioinformatics/`](tools/bioinformatics/README.md) |
| Public database adapters | 13 | [`tools/databases/`](tools/databases/) |
| Literature source adapter | 1 | [`tools/literature/`](tools/literature/) |
| ClinicalTrials.gov source adapter | 1 | [`tools/clinicaltrials/`](tools/clinicaltrials/) |
| Shared execution and packet helpers | 10+ | [`tools/common/`](tools/common/README.md) |
| Routing and wrapper-management scripts | repository utilities | this directory and [`tools/`](tools/README.md) |

## Public database adapters

These are bounded Reef adapters. They default to dry-run planning unless live
network execution is explicitly enabled.

| Adapter | Main use | Safe evidence boundary |
|---|---|---|
| **UniProt** | Protein accession, sequence, and annotation provenance | Annotation is not new functional or mechanistic proof |
| **PubMed** | PMID and citation metadata | Metadata or abstract is not full-text evidence |
| **Europe PMC** | Literature and preprint metadata | Search retrieval is not claim verification |
| **ChEMBL** | Compound, assay, activity, and target records | Database activity is not therapeutic efficacy |
| **Open Targets** | Target-disease association evidence | Association scores are not causal or clinical proof |
| **STRING** | Protein association network evidence | Predicted or aggregated association is not direct binding or mechanism |
| **Reactome** | Curated pathway membership | Pathway annotation is not context-specific activation |
| **QuickGO** | Gene Ontology annotations | Ontology annotation is not experimental confirmation in the study context |
| **ClinVar** | Variant assertions and review status | An assertion alone is not patient-specific treatment guidance |
| **gnomAD** | Population allele-frequency evidence | Population frequency is not pathogenicity or clinical actionability |
| **AlphaFold DB** | Predicted structure and confidence metadata | Prediction is not binding, function, mechanism, or efficacy proof |
| **ClinicalTrials.gov** | Trial registration, design, and status | Registration is not efficacy or safety evidence |
| **NCBI E-utilities** | Bounded NCBI record retrieval | Retrieved metadata must be inspected before downstream use |

Every adapter folder contains:

- `tool.json`: scope and evidence boundary;
- `api.json`: stable command contract;
- `examples/query.example.json`: example input;
- `scripts/query_packet.py`: dry-run or bounded live entry point.

Example:

```bash
cd skills/ocean/scripts/tools/databases/uniprot

python3 scripts/query_packet.py \
  --accession P04637 \
  --out outputs/uniprot-reef-packet.json
```

Add `--execute` only when public network access is appropriate. Inspect the
resulting packet before using it as Reef evidence.

## Literature and registry source adapters

| Adapter | Purpose | Important limitation |
|---|---|---|
| [`tools/literature/`](tools/literature/) | Turn PubMed, Europe PMC, DOI/PMID, abstract, or local literature records into source packets | Title/abstract packets remain title/abstract-level evidence |
| [`tools/clinicaltrials/`](tools/clinicaltrials/) | Turn ClinicalTrials.gov records into registry packets | Registry design/status does not prove efficacy or safety |
| [`tools/bioinformatics/alphafold_db/`](tools/bioinformatics/alphafold_db/) | Inspect AlphaFold DB-style metadata, PAE, mmCIF, and pLDDT evidence | Structural confidence does not prove biological function |

## Bioinformatics tools by scientific family

All 115 folders include `tool.json`, `api.json`, a wrapper configuration,
example run records, a usage reference, and bounded probe/plan or runner
entrypoints.

| Family | Count | Covered tools |
|---|---:|---|
| Sequence alignment | 5 | BLAST, Bowtie2, BWA, LAST, minimap2 |
| Alignment-file operations | 4 | bcftools, BEDTools, HTSlib, SAMtools |
| Spliced RNA alignment | 2 | HISAT2, STAR |
| QC and preprocessing | 8 | cutadapt, fastp, FastQC, MultiQC, Picard, Qualimap, Trim Galore, Trimmomatic |
| RNA-seq quantification | 5 | featureCounts, kallisto, RSEM, Salmon, StringTie |
| Differential expression | 4 | DESeq2, edgeR, limma-voom, sleuth |
| Single-cell analysis | 8 | Alevin-fry, Azimuth, Cell Ranger, CellTypist, Scanpy, scVI, Seurat, STARsolo |
| Spatial transcriptomics | 7 | cell2location, Giotto, Space Ranger, Squidpy, Stereoscope, stLearn, Tangram |
| Epigenomics and motif/peak analysis | 6 | deepTools, FIMO, HOMER, MACS2, MACS3, MEME |
| Variant calling | 5 | DeepVariant, FreeBayes, GATK, Mutect2, Strelka2 |
| Genome assembly and annotation | 12 | Bakta, BUSCO, Canu, CheckM, eggNOG-mapper, Flye, InterProScan, MEGAHIT, Prokka, QUAST, Raven, SPAdes |
| Microbiome and metagenomics | 6 | Bracken, DADA2, HUMAnN, Kraken2, MetaPhlAn, QIIME2 |
| Phylogenetics and comparative genomics | 7 | Clustal Omega, FastTree, IQ-TREE, MAFFT, MUSCLE, OrthoFinder, RAxML |
| Protein structure and modeling | 9 | AlphaFold, AlphaFold DB, ChimeraX, ColabFold, HH-suite, HMMER, MODELLER, PyMOL, RoseTTAFold |
| Proteomics and metabolomics | 7 | DIA-NN, FragPipe, MaxQuant, MS-DIAL, MZmine, Skyline, XCMS |
| Multi-omics integration | 5 | DIABLO, mixOmics, MOFA, MOFA+, WGCNA |
| Imaging and signal ML | 6 | ITK-SNAP, MONAI, nnU-Net, SimpleITK, 3D Slicer, TorchIO |
| Workflow and reproducibility | 9 | Conda, CWL, Docker, Galaxy, Nextflow, nf-core, Singularity-Apptainer, Snakemake, WDL-Cromwell |

## Execution layers

OCEAN routes each covered bioinformatics tool to one of six bounded execution
layers:

| Layer | Tools | What the wrapper can do |
|---|---:|---|
| `lightweight_cli` | 60 | Probe a local executable or record an explicit user-supplied command |
| `python_package` | 16 | Probe an import or record an inspected Python script run |
| `r_bioconductor` | 10 | Probe an R package or record an inspected R script run |
| `heavy_launcher_plan` | 20 | Produce a non-executing plan with compute, database, license, and evidence requirements |
| `workflow_runtime` | 8 | Probe workflow runtime availability or record an explicit workflow invocation |
| `source_packet_adapter` | 1 | Inspect bounded source files and create a provenance packet |

The counts describe wrapper routing, not local installation.

## Shared helpers

[`tools/common/`](tools/common/README.md) provides reusable bounded layers:

- `software_source_packet.py`: packetize inspected software-run metadata;
- `cli_subprocess_wrapper.py`: local CLI probe and explicit command provenance;
- `python_package_wrapper.py`: Python package probe and inspected script record;
- `rscript_wrapper.py`: R/Bioconductor probe and inspected script record;
- `heavy_tool_launcher.py`: non-executing heavy-tool plan;
- `database_adapter_entrypoint.py`: common database-adapter entry point;
- per-tool CLI, package, launcher, probe, and status helpers.

These helpers do not install dependencies, choose private inputs, download
reference databases, or decide whether a biological conclusion is valid.

## Routing and inspection

Route a biomedical source question:

```bash
python3 skills/ocean/scripts/ocean_source_router.py route \
  --question "What public evidence can support this target-disease claim?" \
  --output outputs/source-route.json
```

Inspect available bioinformatics workflows:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  list-workflows \
  --output outputs/bioinformatics-workflows.json
```

List all covered tools, or search by name/family:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools

python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  list-tools \
  --search alignment
```

Inspect one tool's routing profile:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  profile \
  --tool last
```

Run a bounded availability check or create a non-executing plan:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  check \
  --tool last \
  --output outputs/last-check.json
```

For CLI and package tools, `check` probes the current environment. For heavy
tools it creates a plan without launching a job. The result never proves that a
scientific analysis was valid.

## How OCEAN should use tool output

1. Record the scientific question and why the tool or database is relevant.
2. Record the exact version, query, command, parameters, references, inputs,
   outputs, logs, environment, and date when available.
3. Mark uninspected or missing fields explicitly.
4. Convert the inspected run or response into a bounded source packet.
5. Hand the packet to Reef for provenance organization.
6. Use Iceberg to test whether the packet supports the proposed claim.
7. Use Anchor when validation, leakage, benchmark fairness, replication, or
   reproducibility must be checked.

Never upgrade tool availability, a dry-run plan, a database hit, or an
uninspected output into scientific validation.
