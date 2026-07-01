# Reef Resource Provenance

Use Reef when OCEAN needs to inspect biomedical resources beneath a claim: databases, knowledge graphs, ontologies, cohorts, benchmarks, registries, datasets, annotations, curated relationships, or text-mined associations.

Reef is not a generic database summary. Its job is to map resource provenance, evidence hierarchy, circularity, leakage, and whether a resource can support the claim being made.

## Contents

- Purpose
- Trigger
- Inputs
- Evidence Hierarchy
- Safety Rules
- Workflow
- Output Artifact
- Stop Conditions
- Failure Modes

## Purpose

- Identify what resources a paper, idea, or claim depends on.
- Separate curated evidence, primary data, model prediction, text mining, ontology, and benchmark artifacts.
- Detect circularity, leakage, duplicated provenance, or overclaiming from database/KG evidence.
- Prepare resource evidence for Iceberg, Anchor, or Compass.

## Trigger

Read this file when the user asks about:

- knowledge graphs, databases, benchmarks, cohorts, registries, ontologies, or resources;
- whether a KG/database supports a mechanism claim;
- whether a benchmark is fair, independent, or leakage-prone;
- resource/database article evaluation;
- biomedical AI work using external databases or annotation resources;
- live/public API or official database-tool planning. For API-specific boundaries and adapter planning, also read `reef-api-adapters.md`.

## Inputs

Reef can start from:

- Sounding source packet;
- paper methods/resource section;
- dataset, KG, database, or benchmark name;
- list of genes, drugs, diseases, pathways, cell types, cohorts, or ontologies;
- reviewer concern about data provenance or circular evidence.

## Evidence Hierarchy

| Evidence type | Can support | Cannot support alone |
|---|---|---|
| Primary experimental data | Observed association under inspected design | General mechanism or clinical utility without validation |
| Curated database entry | Prior reported relationship or annotation | New causal claim unless source evidence is inspected |
| Text-mined relation | Candidate association or signal | Mechanism, causality, or therapeutic conclusion |
| KG prediction/embedding | Hypothesis or prioritization | Biological truth or clinical readiness |
| Benchmark dataset | Comparative model behavior under that benchmark | Real-world deployment or broad generalization |
| Ontology/pathway annotation | Term mapping or structured context | Empirical validation of a new claim |

## Safety Rules

- Do not convert database co-occurrence into mechanism.
- Do not treat KG prediction as causal evidence.
- Do not assume benchmark independence without checking dataset provenance and split strategy.
- Do not invent dataset size, cohort origin, curation rules, benchmark version, or ontology mappings.
- If a resource cannot be traced to an official page, paper, registry, or data record, label it non-traceable.

## Workflow

1. **Resource inventory**
   - Extract every dataset, benchmark, KG, ontology, registry, cohort, database, annotation source, and code/resource URL mentioned or needed.
2. **Provenance check**
   - Record official source, identifier/version, primary paper, curation method, update status if inspected, and access boundary.
   - If live/public API or database-tool work is needed, use `reef-api-adapters.md` to plan adapters, endpoint/source boundaries, query logs, and API-derived resource evidence.
3. **Evidence classification**
   - Classify each resource as primary data, curated annotation, text-mined relation, KG prediction, benchmark, ontology, registry, or review context.
4. **Circularity and leakage audit**
   - Check whether the same source contributes to training, validation, benchmark, KG construction, and evidence interpretation.
5. **Claim support mapping**
   - Map each resource to the strongest claim it can support and the claims it cannot support.
6. **Handoff**
   - To Iceberg for claim-evidence downgrade.
   - To Anchor for validation, leakage, benchmark, and reproducibility checks.
   - To Compass for resource-driven idea design.

## Output Artifact

```markdown
一、Reef任务定义
- Resource/KG/database seed:
- Claim being evaluated:
- Resource scope:
- Evidence state:

二、资源清单与provenance
| Resource | Type | Official source/identifier | Inspected content | Provenance status | Version/date if known | Limit |
|---|---|---|---|---|---|---|

三、证据等级表
| Resource | Evidence type | Supports | Does not support | Claim risk |
|---|---|---|---|---|

四、Circularity / leakage / dependency map
| Risk | Where it appears | Why it matters | Needed check |
|---|---|---|---|

五、Reef边界
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

六、Handoff Ticket
| Next module | Reason | Input packet | Stop condition |
|---|---|---|---|
```

## Stop Conditions

Stop or downgrade when:

- resource provenance is not traceable;
- the resource type is unknown;
- KG/database evidence is being used to claim mechanism or causality;
- benchmark independence cannot be established;
- the user asks for clinical or therapeutic conclusions from resource evidence alone.

## Failure Modes

- Treating "present in database" as "experimentally proven".
- Ignoring that a KG may be built from the same literature later used for validation.
- Treating benchmark performance as biological insight.
- Using ontology/pathway labels as causal evidence.
- Failing to distinguish curated, predicted, and text-mined relationships.
