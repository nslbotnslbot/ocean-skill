# OCEAN Domain Lens

Use this reference before selecting evidence standards for biomedical and biological research tasks. The Domain Lens is a routing layer: it identifies the scientific lane, expected evidence types, forbidden overclaims, and the next OCEAN module to load.

The Domain Lens does not decide whether a claim is true. It decides which evidence standard should apply.

## Contents

- Purpose
- When To Load
- Domain Fingerprint
- Domain Lanes
- Evidence Standards
- Output Artifact
- Handoff Rules
- Stop Conditions

## Purpose

- Classify the research object before reviewing evidence.
- Avoid using one generic peer-review checklist for unlike domains.
- Prevent upgrades from database, model, abstract, or review evidence into mechanism, clinical utility, publication readiness, or authorship claims.
- Route the task to Sounding, Current, Reef, Iceberg, Anchor, Compass, or Harbor with the correct evidence expectations.

## When To Load

Read this file when:

- the user gives a paper, idea, proposal, review comment, sentence, dataset, database, KG, biomarker, model, clinical claim, or manuscript;
- the task spans more than one OCEAN module;
- the answer needs medical, biological, biomedical AI, omics, clinical, drug, KG/database, or proposal-specific evidence standards;
- the model is about to use a generic summary or generic review style.

## Domain Fingerprint

Before making a verdict, fill this internal routing fingerprint:

```markdown
Domain Lens Fingerprint
- Primary domain:
- Secondary domain:
- Research object:
- Claim target:
- Evidence needed:
- Evidence currently available:
- Highest safe claim level:
- Active OCEAN module:
- Next module or stop condition:
```

Use "unknown" rather than guessing when a field is not provided.

## Domain Lanes

| Domain lane | Typical inputs | Evidence needed before strong claims | Main overclaim risk | Preferred first modules |
|---|---|---|---|---|
| Medical AI / clinical prediction | model paper, benchmark, EHR cohort, imaging model, risk score | dataset provenance, split strategy, leakage checks, calibration, external validation, clinical utility boundary | benchmark improvement becomes clinical readiness | Sounding, Reef, Iceberg, Anchor |
| Biological AI / AI-for-biology | foundation model, protein model, perturbation model, agentic biology workflow | task definition, biological endpoint, benchmark independence, wet-lab or independent validation boundary | model output becomes biological truth | Sounding, Reef, Iceberg, Anchor |
| Clinical research | trial, registry, guideline, patient cohort, treatment/outcome claim | protocol/design, population, outcome definition, bias/confounding controls, posted results/publication | registry or retrospective association becomes treatment guidance | Sounding, Reef, Iceberg, Anchor |
| Molecular / cellular biology | mechanism claim, pathway, cell phenotype, perturbation, animal/cell evidence | experimental system, controls, perturbation, replication, orthogonal validation, species/context boundary | association becomes causal mechanism | Sounding, Iceberg, Anchor |
| Omics / single-cell / spatial | scRNA-seq, spatial transcriptomics, bulk omics, proteomics, metabolomics | accession/provenance, sample metadata, preprocessing, batch/confounder checks, cell/tissue annotation boundary | atlas expression becomes mechanism or disease specificity | Sounding, Reef, Iceberg, Anchor |
| Drug / target / therapeutic hypothesis | target prioritization, drug repurposing, ChEMBL/PubChem/Open Targets, clinical trial search | target evidence, bioactivity context, disease relevance, safety/regulatory boundary, validation plan | target association becomes therapy efficacy | Sounding, Reef, Iceberg, Anchor, Compass |
| Knowledge graph / database / resource | KG, ontology, curated database, benchmark, cohort, registry, resource paper | official provenance, identifier/version, curation method, source overlap, circularity/leakage check | database edge becomes mechanism or validation | Reef, Iceberg, Anchor |
| Manuscript / review / proposal | manuscript draft, abstract, reviewer comment, research plan, grant-like idea | provided sections, source packet, claim-evidence matrix, missing materials, feasibility route | polished narrative becomes evidence | Sounding, Iceberg, Compass, Harbor |
| Collaboration / authorship boundary | project notes, contribution proposal, advisory request, collaboration plan | concrete tasks, delivered artifacts, decision dates, evidence of intellectual/experimental contribution | light advice becomes authorship claim | Compass, Harbor |

## Evidence Standards

Use the strictest relevant standard when a task spans domains.

| Claim type | Minimum inspected evidence for a cautious claim | Stronger claim requires |
|---|---|---|
| Source exists | DOI, PMID, preprint ID, registry ID, accession, URL, or local file | full source inspection for specific evidence claims |
| Trend / novelty direction | bounded search log and multiple traceable sources | systematic search strategy, inclusion/exclusion boundary, recent-source coverage |
| Database/resource support | official resource page, record, identifier, or documented API packet | primary cited evidence, version/provenance, curation method, circularity check |
| Mechanism | direct experimental evidence in the inspected system | perturbation, orthogonal validation, replication, context/species boundary |
| Clinical utility | validation design, outcome, population, calibration/decision utility | prospective/external validation, implementation context, safety/benefit boundary |
| Therapeutic efficacy | trial/publication evidence with outcome and design inspected | randomized/prospective evidence or strong triangulation plus safety context |
| Publication positioning | inspected manuscript/source packet and reviewer-risk analysis | field trend, benchmark/context, claim rewrites, validation gaps |
| Authorship-level contribution | concrete intellectual/technical work and documented contribution | project-specific authorship criteria, team agreement, sustained substantive work |

## Output Artifact

Use this compact add-on when the domain standard affects the answer:

```markdown
Domain Lens
| Field | Value |
|---|---|
| Primary domain |  |
| Secondary domain |  |
| Research object |  |
| Highest safe claim level |  |
| Required evidence standard |  |
| Current evidence state |  |
| Module route |  |
| Stop condition |  |

Domain-specific cautions

```

## Handoff Rules

- To Sounding when sources are missing, partial, abstract-only, or need traceable packets.
- To Current when the user asks whether a direction is timely, crowded, new, incremental, or field-moving.
- To Reef when the claim depends on databases, KGs, cohorts, registries, benchmarks, omics resources, or official APIs.
- To Iceberg when there is a concrete claim that needs support, downgrade, contradiction, or safe rewrite.
- To Anchor when the next question is validation, leakage, reproducibility, benchmark fairness, replication, or clinical utility.
- To Compass when the task is research planning, experiment design, journal strategy, or idea prioritization after evidence gaps are known.
- To Harbor when the output should become a durable decision memo, contribution boundary, report, or project memory.

## Stop Conditions

Stop or downgrade when:

- the domain cannot be identified and the requested conclusion depends on domain-specific evidence;
- only a title, abstract, DOI page, search snippet, or user memory is available for a strong claim;
- the task asks for clinical, therapeutic, mechanism, novelty, or publication certainty from insufficient evidence;
- private patient data, unpublished data, private peer review, paid sources, or key-protected resources would be required without approval;
- the next step would require inventing a dataset, endpoint, source, reviewer comment, model result, validation result, or authorship agreement.
