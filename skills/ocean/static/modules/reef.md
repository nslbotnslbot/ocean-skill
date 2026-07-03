# Reef Module Contract

Active module: Reef

Purpose: route biomedical resources, databases, KGs, registries, cohorts, benchmarks, and APIs without turning routes into evidence.

## Required artifact

- Resource Provenance Map
- Evidence Hierarchy
- API/Database Boundary
- Circularity Risk Notes
- Source Packet Audit

## Resource route examples

| Domain | Candidate routes |
|---|---|
| Literature | PubMed, OpenAlex, CrossRef, arXiv, bioRxiv, medRxiv |
| Omics | GEO, SRA, ENA, ArrayExpress, GTEx, ENCODE, MetaboLights |
| Spatial / multimodal atlases | HuBMAP, HCA, CZ CELLxGENE, Single Cell Portal |
| Epigenomics / regulatory | ENCODE, Cistrome DB, ReMap, JASPAR, UCSC Genome Browser |
| Protein/structure | UniProt, PDB, AlphaFold DB, InterPro, STRING |
| Variant/genetics | ClinVar, dbSNP, gnomAD, Ensembl/VEP |
| Drug/target | ChEMBL, OpenTargets, PubChem, OpenFDA |
| Clinical | ClinicalTrials, registries, MIMIC/eICU only when lawful and explicitly provided |
| Clinical imaging/signal | TCIA, PhysioNet, MIMIC-CXR only when lawful and explicitly provided, OpenNeuro |
| Regulatory/safety | OpenFDA, DailyMed, FDA labels, EMA public assessment reports, FAERS with caveats |
| Cancer genomics | TCGA/GDC, cBioPortal, ICGC, COSMIC |
| Pathways/gene sets | GO, Reactome, KEGG, WikiPathways, MSigDB |
| Proteomics/metabolomics | PRIDE, ProteomeXchange, MetaboLights, HMDB, MassIVE |
| Microbiome | MGnify, Qiita, Human Microbiome Project, SRA/ENA microbiome studies |
| Model organisms | MGI, FlyBase, WormBase, SGD, ZFIN, TAIR |
| Bioinformatics software | BLAST, LAST, BWA, Bowtie2, HISAT2, STAR, minimap2, SAMtools, BEDTools, GATK, bcftools, Salmon, kallisto, DESeq2, edgeR, Seurat, Scanpy, Cell Ranger, Snakemake, Nextflow |

## Hard distinctions

- Candidate route != queried evidence.
- Known database != this project has data there.
- Database annotation != mechanism proof.
- KG/text-mining association != causality.
- API capability != API response.
- Source packet exists != source packet supports the claim.
- Enrichment/pathway hit != mechanism proof.
- Registry entry != clinical outcome.
- Software output != valid analysis without version, parameters, reference/index, inputs, logs, and provenance.
- Imaging/signal benchmark != clinical utility without label definition, split provenance, external validation, and deployment boundary.
- Safety/adverse-event signal != causal safety conclusion without reporting-bias handling and denominator/context.

## Tool layer

Use `scripts/ocean_source_router.py` before treating database/API/tool outputs as evidence:

1. `route`: classify the question or claim into candidate resources.
2. `record-query`: record query, filters, identifiers, inspected fields, date, and terms notes.
3. `packetize`: convert an existing query result, tool output, or local file summary into OCEAN source-packet JSON.
4. `audit-packet`: check whether the packet is complete enough to hand off to Iceberg, Anchor, Compass, or Harbor.

Reef may produce candidate routes, but it must not upgrade them into evidence without a complete source packet.

## Stop when

Stop if the user asks for exact identifiers without a real query/API response or source packet.
