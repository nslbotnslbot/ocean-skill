# Reef Biological and Clinical Data Sources

Use this reference when Reef needs to choose, compare, or route biological and clinical data resources for biomedical research evidence review.

This file is a data-source navigation catalog. It is not proof that any resource was queried. Before naming live endpoints, schema fields, counts, release versions, or API results, inspect the official documentation in the current run and record the evidence boundary.

## Contents

- Purpose
- Source Selection Principles
- Resource Map
- Clinical Data Boundaries
- Biological Data Boundaries
- Output Add-On
- Official Documentation Anchors
- Stop Conditions

## Purpose

- Help Reef identify which biological or clinical resources might be relevant to a claim, paper, proposal, or idea.
- Separate entity lookup, curated annotation, primary omics data, clinical registry metadata, cohort/EHR data, regulatory data, and knowledge-graph associations.
- Prevent unsupported upgrades from "resource contains a record" to "mechanism is proven", "therapy works", "clinical utility is established", or "the idea is novel".
- Produce a traceable resource provenance packet for Iceberg, Anchor, or Compass.

## Source Selection Principles

- Start from the research entity: gene/protein, variant, cell type, tissue, disease, drug, pathway, cohort, trial, imaging modality, model organism, or benchmark.
- Prefer official portals, official APIs, official bulk downloads, primary resource papers, and stable accessions.
- Record identifiers before interpretation: PMID/DOI, accession, Ensembl ID, UniProt ID, NCT ID, trial registry ID, dataset ID, variant ID, ontology ID, drug/compound ID.
- Treat public clinical resources as research metadata unless patient-level data and study design are actually inspected.
- Treat controlled-access clinical/EHR/cohort resources as privacy-sensitive. Do not send private patient data, private manuscripts, or protected health information to an external service without explicit user approval.
- Mark licensing and access restrictions when known or suspected. Some resources are open for browsing but restrict redistribution, commercial use, bulk download, or derived datasets.

## Resource Map

| Lane | Candidate resources | Best for | Cannot support alone | Traceability anchors |
|---|---|---|---|---|
| Literature and source identity | PubMed, PubMed Central, Europe PMC, Crossref, bioRxiv, medRxiv, arXiv | Literature/source discovery, PMID/DOI/preprint identity, citation trail | Full evidence support unless full text/methods/data are inspected | PMID, PMCID, DOI, preprint ID, URL |
| Gene and genome annotation | NCBI Gene, Ensembl, HGNC, RefSeq, UCSC Genome Browser | Gene IDs, coordinates, transcripts, nomenclature, genome context | Biological mechanism or disease causality | Entrez Gene ID, Ensembl ID, HGNC ID, RefSeq accession |
| Protein annotation | UniProt, InterPro, Pfam, PROSITE, AlphaFold DB, RCSB PDB | Protein function notes, domains, sequence, structure/model context | Wet-lab functional validation or drug efficacy | UniProt accession, PDB ID, InterPro/Pfam ID |
| Variant and population genetics | ClinVar, dbSNP, gnomAD, GWAS Catalog, dbGaP, Ensembl VEP | Variant identity, population frequency, clinical assertion, GWAS association | Diagnosis, penetrance, treatment decision, causal mechanism without study context | rsID, ClinVar Variation ID, HGVS, GWAS Catalog accession |
| Pathways and ontologies | Gene Ontology, Reactome, KEGG, WikiPathways, Disease Ontology, HPO, Cell Ontology, Uberon, OBO Foundry/BioPortal | Term normalization, pathway context, phenotype/cell/tissue mapping | Empirical proof that a pathway is active or causal in the user's system | GO/Reactome/HP/CL/UBERON/DOID IDs, pathway IDs |
| Single-cell and spatial atlases | CZ CELLxGENE Discover/Census, Human Cell Atlas, Single Cell Portal, HuBMAP, Human Protein Atlas, GEO/SRA/ENA, ArrayExpress/BioStudies | Cell/tissue context, scRNA-seq/spatial data discovery, atlas provenance | Validation of a new mechanism, disease specificity, or clinical actionability | Dataset ID, collection ID, accession, tissue/cell ontology terms |
| Bulk omics and functional genomics | GEO, SRA, ENA, ArrayExpress/BioStudies, Expression Atlas, PRIDE, PeptideAtlas, MetaboLights, DepMap | Expression, sequencing, proteomics, metabolomics, perturbation screens | General mechanism or treatment claim without design/metadata/validation | GEO/SRA/ENA accession, BioProject/BioSample, PRIDE/MTBLS IDs |
| Cancer genomics and oncology cohorts | NCI GDC/TCGA, cBioPortal, ICGC/ARGO, AACR Project GENIE, COSMIC | Tumor genomics, cohort-level alterations, cancer study metadata | Treatment recommendation, prospective clinical utility, real-world efficacy | GDC project/case/file UUID, cBioPortal study ID, mutation/gene IDs |
| Drug and chemical resources | ChEMBL, PubChem, DrugBank, DrugCentral, BindingDB, Open Targets, PharmGKB | Compound identity, target annotations, bioactivity, pharmacology, drug-gene context | Therapeutic efficacy, safety, indication expansion, clinical readiness | ChEMBL ID, CID, DrugBank ID, target ID, PharmGKB ID |
| Clinical trials and registries | ClinicalTrials.gov, EU Clinical Trials Register/CTIS, WHO ICTRP, ISRCTN | Trial existence, status, design metadata, arms/outcomes if posted | Efficacy unless results/publications are inspected; absence of trials as absence of evidence | NCT ID, registry ID, trial URL |
| Regulatory and safety data | FDA labels, openFDA, EMA EPAR, DailyMed, FAERS, MAUDE | Labels, adverse-event reports, recalls, device events, regulatory context | Causality from spontaneous reports; off-label recommendation | label ID, application number, event/report ID, product/device code |
| EHR and clinical research cohorts | MIMIC-IV, eICU-CRD, OMOP CDM datasets, All of Us Researcher Workbench, UK Biobank, SEER, NHANES | Retrospective clinical data, cohort feasibility, phenotype/outcome definitions | Prospective clinical utility, causal treatment effect, generalizability without design checks | dataset version, cohort definition, code list, access approval |
| Imaging and signals | The Cancer Imaging Archive, MIMIC-CXR, PhysioNet waveform datasets, ADNI, OASIS | Imaging/signal benchmark context and dataset provenance | Deployment safety, broad generalization, clinical utility | dataset ID, imaging collection ID, waveform record ID |
| Model organisms | MGI, ZFIN, FlyBase, WormBase, TAIR, SGD, RGD | Orthologs, phenotype annotations, organism-specific evidence | Human mechanism or clinical translation without bridging evidence | organism gene ID, allele ID, phenotype term |
| Microbiome and pathogen data | MGnify, NCBI Taxonomy, ENA/SRA, BV-BRC, GISAID, Nextstrain | Taxonomy, metagenomics, pathogen sequence context, surveillance lineage | Host mechanism, clinical outcome, or treatment guidance without study evidence | taxon ID, accession, lineage, sample metadata |

## Clinical Data Boundaries

Use clinical resources conservatively:

- Registry records can establish that a study exists, what status/design metadata are posted, and whether results may be available. They do not by themselves prove efficacy.
- Spontaneous adverse-event databases can support signal exploration. They do not establish causality, incidence, comparative safety, or treatment guidance.
- EHR and claims data can support retrospective associations and cohort feasibility when definitions are inspected. They do not establish causal effects without design controls and bias assessment.
- Controlled-access cohorts require access terms, IRB/data-use conditions, privacy handling, and reproducible cohort definitions before evidence claims.
- Clinical labels and regulatory documents describe approved context and warnings. They do not prove new indications or new mechanisms beyond inspected regulatory evidence.

## Biological Data Boundaries

Use biological resources by evidence type:

- Annotation resources normalize entities and point to prior evidence; inspect the cited primary evidence before strong claims.
- Ontologies and pathways provide structure and vocabulary; they do not prove pathway activity.
- Atlases show where signals have been observed under specific sampling and processing; they do not prove mechanism or disease causality.
- Protein structure predictions and domain annotations are hypothesis support unless experimentally validated.
- Variant databases mix assertion levels, submitter evidence, population frequency, and prediction. Do not collapse them into a single "pathogenic/proven" label without inspecting review status and evidence.
- Knowledge-graph and drug-target association scores are prioritization signals, not biological truth.

## Output Add-On

Use this after the standard Reef artifact when biological or clinical data-source routing is needed:

```markdown
七、Biological / Clinical Data Source Routing
| Research entity/question | Candidate resource | Why this resource | Identifier needed | What it can support | What it cannot support | Access/licensing/privacy boundary |
|---|---|---|---|---|---|---|

八、Resource-to-Module Handoff
| Resource packet | Next module | Why | Stop condition |
|---|---|---|---|
```

## Official Documentation Anchors

These are starting anchors for official documentation or portals. Verify in the current run before using endpoint details.

| Resource | Official documentation or portal |
|---|---|
| NCBI E-utilities / Entrez | `https://www.ncbi.nlm.nih.gov/books/NBK25501/` |
| Ensembl REST | `https://rest.ensembl.org/` |
| UniProt API | `https://www.uniprot.org/help/api` |
| Open Targets Platform | `https://platform-docs.opentargets.org/data-access/graphql-api` |
| CZ CELLxGENE Census | `https://chanzuckerberg.github.io/cellxgene-census/` |
| ClinicalTrials.gov API | `https://clinicaltrials.gov/data-api/api` |
| NCI GDC API | `https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started/` |
| cBioPortal API | `https://docs.cbioportal.org/web-api-and-clients/` |
| ChEMBL API | `https://www.ebi.ac.uk/chembl/api/data/docs` |
| PubChem PUG-REST | `https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest` |
| openFDA API | `https://open.fda.gov/apis/` |
| MIMIC-IV on PhysioNet | `https://physionet.org/content/mimiciv/` |
| PhysioNet databases | `https://physionet.org/about/database/` |
| SEER data | `https://seer.cancer.gov/data/` |
| NHANES datasets | `https://wwwn.cdc.gov/nchs/nhanes/` |
| All of Us Researcher Workbench | `https://www.researchallofus.org/data-tools/workbench/` |

## Stop Conditions

Stop or downgrade when:

- the user asks for clinical recommendation, diagnosis, treatment choice, or patient-specific action from database/resource evidence alone;
- the resource is controlled-access, patient-level, private, or sensitive and the user has not approved the access route;
- the task would require live API calls, paid access, private keys, or data-use approval that has not been granted;
- the model is about to invent an endpoint, field, release version, dataset count, cohort size, label, or identifier;
- the resource's licensing/access boundary is unknown and the output would imply redistribution or public release;
- a clinical or biological conclusion depends on uninspected primary data, methods, supplementary tables, validation, or cited evidence.
