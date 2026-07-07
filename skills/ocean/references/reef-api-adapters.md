# Reef API Adapter Registry

Use this reference when Reef needs to plan or inspect live biomedical resources through public APIs, registries, knowledge graphs, or database tools.

Reef API adapters are optional. OCEAN must remain a workflow and output contract, not a dependency on any specific API, model, paid service, key, or network condition.

For broader biological or clinical data-source selection before live API planning, read `data-tool-router.md` and `reef-biological-data-sources.md` first.

## Contents

- Purpose
- Adapter Principles
- Candidate Adapter Registry
- Query Planning
- Output Artifact
- Evidence Boundaries
- Stop Conditions

## Purpose

- Turn external biomedical resources into traceable resource evidence.
- Record provenance, endpoint, version/date, inspected fields, and access boundary.
- Separate database annotation, registry metadata, KG association, benchmark artifact, and primary experimental evidence.
- Prepare API-derived resource packets for Iceberg, Anchor, or Compass without overstating what the API proves.

## Adapter Principles

- Treat every adapter as optional unless the user explicitly asks for live API/database work.
- Use `scripts/run_reef_api_adapter.py` for supported public starter adapters when a bounded query packet would help. The script defaults to dry-run and only performs live public API calls with `--execute`.
- Prefer official APIs, official bulk downloads, official data portals, or documented public endpoints.
- Record the exact source URL, endpoint family, query date, inspected fields, filters, and any failures.
- Do not name endpoint URLs, query paths, schema fields, release versions, or API result fields unless they were provided by the user or inspected from official documentation in the current run.
- Never write API keys, credentials, paid account details, private manuscript text, patient data, or raw sensitive outputs into public logs.
- If an API call costs money, uses a private key, accesses private data, or may submit unpublished material to a third party, ask the user before calling it.
- Treat API records as resource evidence. They can support provenance, annotation, association, or registry status; they do not alone prove mechanism, causality, treatment efficacy, clinical utility, or publication readiness.

## Starter Runner

Use the runner only after the Reef query plan is bounded:

```bash
python3 skills/ocean/scripts/run_reef_api_adapter.py \
  --adapter ncbi-eutils \
  --database pubmed \
  --query "BRCA1 breast cancer" \
  --retmax 5 \
  --out outputs/reef_ncbi_packet.json
```

Default mode is dry-run. Add `--execute` only for public, non-sensitive, no-key requests:

```bash
python3 skills/ocean/scripts/run_reef_api_adapter.py \
  --adapter opentargets \
  --ensembl-id ENSG00000012048 \
  --execute \
  --out outputs/reef_opentargets_packet.json
```

Supported starter adapters:

| Adapter flag | Live behavior | Required input |
|---|---|---|
| `ncbi-eutils` | Entrez search packet over a selected database | `--query`, optional `--database` |
| `pubmed` | PubMed search packet via NCBI E-utilities | `--query` |
| `europepmc` | Europe PMC search packet | `--query` |
| `chembl` | ChEMBL molecule search packet | `--query` |
| `uniprot` | UniProt accession or search packet | `--accession` or `--query` |
| `clinicaltrials` | ClinicalTrials.gov study search packet | `--query` |
| `opentargets` | Open Targets target lookup packet | `--ensembl-id` |
| `string` | STRING identifier mapping packet | `--identifier` or `--query`, explicit `--species` when relevant |
| `reactome` | Reactome content-service search packet | `--query` |
| `quickgo` | QuickGO ontology search packet | `--query` |
| `clinvar` | ClinVar search packet via NCBI E-utilities | `--query` |
| `gnomad` | gnomAD variant GraphQL packet | `--variant-id` |
| `alphafold-db` | AlphaFold DB prediction metadata packet | `--accession` or `--query` |

The runner output is a Reef resource packet, not a scientific conclusion. Hand it to Iceberg or Anchor before making claim-support or validation statements.

These adapters are also exposed as tool-library folders under `scripts/tools/databases/<adapter_slug>/`. Each folder has `README.md`, `api.json`, `tool.json`, `adapter_config.json`, an example query, and `scripts/query_packet.py`, while still delegating execution to the shared runner above.

## Candidate Adapter Registry

These adapters are starting points, not mandatory dependencies.

| Adapter | Resource role | API/source style | Use when | Reef boundary |
|---|---|---|---|---|
| Open Targets Platform | Target-disease, drug, variant, study, credible-set evidence | GraphQL endpoint and downloads | Mapping gene/target, disease, drug, genetic evidence, tractability, or pharmacology context | Association or evidence score is not mechanism or clinical efficacy |
| CZ CELLxGENE Census | Single-cell and spatial dataset access | Python/R API over hosted Census object | Checking cell/gene metadata, tissue/cell-type context, dataset provenance, and slice availability | Dataset presence is not validation of a new claim; record release and `is_primary_data` handling |
| NCBI E-utilities | PubMed, Gene, GEO, SRA, Protein, PMC, and other Entrez records | Fixed URL server-side utilities | Retrieving public biomedical literature/data records and metadata | Metadata or abstract records are not full-paper evidence |
| Ensembl REST API | Gene, transcript, variant, sequence, homology, phenotype, ontology, and VEP context | REST endpoints | Mapping identifiers, variants, coordinates, homologs, and genome annotations | Annotation or predicted consequence is not experimental mechanism proof |
| MyGene.info | Gene annotation retrieval and identifier mapping | REST query and gene annotation endpoints | Normalizing gene symbols, Entrez/Ensembl IDs, RefSeq links, and common gene annotation fields | Convenience annotations need source confirmation for high-stakes claims |
| UniProt | Protein sequence/function annotation and cross-references | REST/web programmatic access | Checking reviewed/unreviewed protein records, function notes, domains, isoforms, and cross-references | Separate curated evidence, inferred annotation, and unreviewed records |
| ClinicalTrials.gov | Clinical study registry and results metadata | Official data API / registry records | Checking whether a clinical study exists, its status, arms, outcomes, and reported results availability | Registry status is not efficacy proof; absence of a trial is not absence of evidence |
| BioThings / federated KG tools | Federated gene/drug/disease API discovery | REST/federated query tools | Exploring candidate multi-hop resource links before formal evidence audit | Multi-hop links are hypotheses until original sources are checked |
| NCI GDC / cBioPortal | Cancer genomics and oncology cohort records | Official APIs, portals, and downloads | Checking tumor genomics study provenance, alteration context, and cancer cohort resource boundaries | Cohort/resource records are not treatment guidance or prospective clinical utility |
| openFDA / FDA labels / DailyMed | Regulatory labels, adverse events, recalls, and product metadata | Official public APIs and label portals | Checking label/regulatory/safety context and public adverse-event signal boundaries | Spontaneous reports and labels do not prove new causality, efficacy, or indication expansion |
| PhysioNet / MIMIC-IV-style clinical datasets | Credentialed EHR, ICU, waveform, imaging, and clinical datasets | Official dataset portals, credentialed access, and documented data-use rules | Planning retrospective clinical data provenance, access boundaries, and cohort feasibility checks | EHR data alone does not prove causal treatment effect or deployment readiness |
| SEER / NHANES / All of Us | Population, cancer registry, survey, and controlled cohort resources | Official data portals and workbench access routes | Checking epidemiology/cohort feasibility, phenotype/outcome definitions, and access restrictions | Cohort availability is not causal evidence; controlled-access data must respect data-use/privacy rules |

## Official Documentation Anchors

Use official documentation or data portals before writing an adapter:

| Adapter | Documentation/source URL |
|---|---|
| Open Targets Platform | `https://platform-docs.opentargets.org/data-access/graphql-api` |
| CZ CELLxGENE Census | `https://chanzuckerberg.github.io/cellxgene-census/` |
| NCBI E-utilities | `https://www.ncbi.nlm.nih.gov/books/NBK25501/` |
| Ensembl REST API | `https://rest.ensembl.org/` |
| MyGene.info | `https://docs.mygene.info/en/latest/` |
| UniProt | `https://www.uniprot.org/help/api` |
| ClinicalTrials.gov | `https://clinicaltrials.gov/data-api/api` |
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

## Query Planning

Before any API call, create a small query plan:

```markdown
一、Reef API Query Plan
- User question:
- Claim/resource seed:
- Adapter(s):
- Why these adapters:
- Public/private boundary:
- Cost/key/network boundary:
- Stop condition:
```

Prefer narrow queries over broad harvesting. For example:

- one gene + one disease;
- one DOI/PMID + linked records;
- one dataset accession;
- one cell type + tissue + disease context;
- one benchmark/dataset provenance chain.

## Output Artifact

Use this add-on after `reef.md` when API/database work is involved:

```markdown
一、Reef API Adapter Plan
| Adapter | Query target | Endpoint/source | Why used | Boundary |
|---|---|---|---|---|

二、API Query Log
| Adapter | Query/filter | Date | Status | Records inspected | Failure/limit |
|---|---|---|---|---:|---|

三、Resource Provenance Map
| Resource/entity | Identifier | Source adapter | Inspected fields | Provenance status | Version/date | Limit |
|---|---|---|---|---|---|---|

四、Evidence Hierarchy
| Resource/entity | Evidence type | Supports | Does not support | Claim risk |
|---|---|---|---|---|

五、Circularity / leakage / dependency check
| Risk | Source | Why it matters | Needed check |
|---|---|---|---|

六、Boundary and Handoff
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:
- Next module:
```

## Evidence Boundaries

- A database record can show that a relationship, entity, identifier, or annotation exists in that resource.
- A curated database can point to prior evidence, but the primary evidence still needs inspection before strong claim support.
- A KG edge can support a candidate association or hypothesis route.
- A registry record can support study existence, status, design metadata, or posted results availability.
- A benchmark record can support benchmark provenance, but not broad deployment claims.
- An API failure, missing record, or no-hit result must be reported as such and not converted into a biological conclusion.

## Stop Conditions

Stop or downgrade when:

- the adapter source is unofficial or undocumented;
- the result cannot be traced to an identifier, endpoint, query, or date;
- a private key, paid quota, private manuscript, patient data, or unpublished data would be exposed without user approval;
- the user asks Reef to infer mechanism, causality, therapy guidance, or clinical utility from API/resource evidence alone;
- query coverage is too narrow for a trend, novelty, or absence-of-evidence claim.
