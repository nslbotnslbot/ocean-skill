# OCEAN Data and Tool Router

Use this reference when OCEAN needs to decide which public data source, official API, registry, benchmark, literature source, or local artifact should be inspected before making a biomedical research claim.

The router is not a live-search guarantee. It defines what should be routed, what can be inferred, and when to stop.

## Contents

- Purpose
- Router Protocol
- Source Classes
- Route Matrix
- Data/Tool Packet
- API and Privacy Boundary
- Handoff Rules
- Stop Conditions

## Purpose

- Keep source discovery separate from source interpretation.
- Route evidence needs to the correct public resource class before Reef, Iceberg, Anchor, or Compass.
- Make API/database work optional, bounded, and provenance-preserving.
- Avoid making OCEAN dependent on a single model, API, paid service, or network condition.

## Router Protocol

1. Identify the entity or claim target:
   - paper/source;
   - gene/protein/variant;
   - disease/phenotype/cell type/tissue;
   - drug/compound/target;
   - dataset/benchmark/cohort/registry;
   - model/workflow/manuscript/proposal.
2. Select the source class and candidate official resources.
3. Record identifiers needed before interpretation.
4. State access, privacy, licensing, key, cost, and network boundaries.
5. Route the resulting packet to the next OCEAN module.

## Source Classes

| Source class | Examples | Can support | Cannot support alone |
|---|---|---|---|
| Literature identity | PubMed, PMC, Crossref, bioRxiv, medRxiv, arXiv | source existence, DOI/PMID/preprint identity, citation trail | detailed methods/results unless inspected |
| Public peer review / assessment | journal public review, eLife assessment, OpenReview, PubPeer | reviewer pressure signals, critique categories, revision opportunities | experimental fact, novelty proof, publication guarantee |
| Biological annotation | NCBI Gene, Ensembl, HGNC, UniProt, GO, Reactome | identifier mapping, annotation context, pathway vocabulary | mechanism or empirical validation |
| Omics and atlases | GEO, SRA, ENA, Expression Atlas, CELLxGENE, HCA, HuBMAP | data discovery, accession, tissue/cell context, provenance | disease mechanism or validation without study inspection |
| Variant/genetics | ClinVar, dbSNP, gnomAD, GWAS Catalog | variant identity, frequency, assertion, association signal | diagnosis, penetrance, treatment guidance |
| Cancer/cohort resources | GDC/TCGA, cBioPortal, GENIE, ICGC | cohort/resource context, alteration metadata | prospective utility or treatment efficacy |
| Drug/chemical resources | ChEMBL, PubChem, BindingDB, Open Targets, DrugCentral, PharmGKB | compound/target/bioactivity context, prioritization | efficacy, safety, clinical readiness |
| Clinical registry/regulatory | ClinicalTrials.gov, WHO ICTRP, FDA label/openFDA, DailyMed | study existence/status, label context, regulatory metadata | efficacy from registry metadata; causality from spontaneous reports |
| EHR/cohort/imaging/signal | MIMIC, PhysioNet, SEER, NHANES, All of Us, TCIA | cohort feasibility, phenotype/outcome planning, benchmark provenance | causal effect or deployment readiness |
| Bioinformatics workflow/software | FastQC, MultiQC, BLAST, LAST/LASTAL, minimap2, BWA, Bowtie2, HISAT2, STAR, SAMtools, BEDTools, bcftools, GATK, DeepVariant, Salmon, kallisto, DESeq2, edgeR, Seurat, Scanpy, Cell Ranger, QIIME2, MetaPhlAn, HUMAnN, AlphaFold, MaxQuant, XCMS, nnU-Net, MONAI, Snakemake, Nextflow, nf-core | tool identity, workflow routing, reproducibility requirements, software provenance | biological validity, mechanism, clinical utility, or benchmark superiority without inspected run details |
| Local manuscript/project files | uploaded manuscript, figures, tables, code, notes | inspected source-bound evidence | anything missing from provided material |

## Route Matrix

| User asks | First route | Then route | Stop if |
|---|---|---|---|
| "Does this paper support this claim?" | Sounding for source packet | Iceberg for claim audit | no traceable source or only abstract for a strong claim |
| "Is this direction hot/new?" | Sounding for source set | Current for trend boundary | search coverage too narrow |
| "Can this KG/database prove mechanism?" | Reef for provenance and evidence hierarchy | Iceberg/Anchor for downgrade and validation plan | resource provenance missing or KG evidence used as mechanism |
| "Which database/API should we use?" | Domain Lens + Data Router | Reef biological/API references | private, paid, key-protected, or endpoint details unverified |
| "Which bioinformatics tool/workflow should we use?" | Data Router + bioinformatics resource map | Reef/Anchor for provenance, run requirements, and reproducibility | version, command, inputs, database/index, parameters, or validation target are missing |
| "Can this guide treatment?" | Domain Lens + Sounding/Reef | Iceberg/Anchor | no clinical design/outcome evidence inspected |
| "What experiment should we do?" | Iceberg/Anchor if claim gaps exist | Compass for plan | evidence is too thin to choose beyond source collection |
| "How do I join this collaboration?" | Compass for contribution route | Harbor for boundary record | contribution facts are missing |

## Data/Tool Packet

When a task depends on data or tools, preserve this packet:

```markdown
Data/Tool Router Packet
| Field | Content |
|---|---|
| Entity or claim target |  |
| Source class |  |
| Candidate official resources |  |
| Identifier(s) needed |  |
| Access/privacy/licensing boundary |  |
| API/tool boundary |  |
| Evidence level |  |
| Next OCEAN module |  |
| Stop condition |  |
```

## API and Privacy Boundary

- Prefer dry-run planning before live public API calls.
- Use official APIs, official portals, documented bulk downloads, or local files.
- Do not invent endpoint paths, response fields, release versions, result counts, cohort sizes, or API status.
- Do not send patient data, private manuscripts, unpublished data, private peer review, credentials, or paid-account materials to external services without explicit user approval.
- If an adapter needs a key, costs money, changes remote state, or accesses controlled data, ask before running it.
- Treat failed/no-hit API calls as boundary information, not biological conclusions.
- Treat software routing as a reproducibility plan, not as proof that a tool ran correctly or that its output supports a biological or clinical claim.

## Handoff Rules

- Hand source identity and source packets to Sounding or Iceberg.
- Hand resource/data/API packets to Reef.
- Hand evidence gaps, leakage risks, or validation targets to Anchor.
- Hand bounded options, tradeoffs, and route choices to Compass.
- Hand decisions, unresolved risks, and contribution records to Harbor.

## Stop Conditions

Stop or downgrade when:

- no source class can be selected from the available input;
- the claim requires a data source that is private, controlled-access, paid, or key-protected and the user has not approved access;
- endpoint/source details would have to be invented;
- the evidence is only a search result, abstract, review comment, registry shell, database association, KG edge, or model prediction but the user asks for causal, clinical, or publication certainty;
- data licensing or privacy boundaries are unknown and the output would imply public reuse.
