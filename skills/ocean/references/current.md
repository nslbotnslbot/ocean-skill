# Current Field Movement

Use Current when OCEAN needs to understand how a biomedical research direction is moving around a paper, idea, source packet, reviewer concern, benchmark, disease area, or method family.

Current is not a general literature review. Its job is to produce a bounded direction-flow readout: what was searched, which nearby works or review signals were inspected, what movement can be stated, what cannot be stated, and which opportunity or risk should be handed downstream.

## Contents

- Purpose
- Trigger
- Inputs
- Safety Rules
- Workflow
- Output Artifact
- Stop Conditions
- Failure Modes

## Purpose

- Position a seed paper, idea, claim, benchmark, or proposal inside a recent biomedical research landscape.
- Identify nearby, competing, converging, or diverging work.
- Distinguish local evidence from field-wide trend claims.
- Detect whether a direction looks emerging, crowded, fragmented, challenged, or under-validated.

## Trigger

Read this file when the user asks about:

- field trends, recent progress, direction flow, or "where this field is going";
- whether a paper or idea is novel, crowded, incremental, or timely;
- related work around a Sounding source packet;
- public review pressure signals that imply a field-level gap;
- benchmark movement, task movement, or model-family movement.

## Inputs

Current can start from:

- Sounding source packet;
- paper title, DOI, arXiv/bioRxiv/medRxiv ID, PubMed record, or manuscript;
- user idea or research proposal;
- reviewer comments;
- benchmark, dataset, disease, method, or KG/database seed.

## Safety Rules

- Do not claim a field-wide trend without reporting the search boundary.
- Do not treat a few papers as consensus.
- Do not treat citation count, preprint status, social attention, or reviewer language as scientific validation.
- Do not invent related papers, dates, venues, benchmark movement, or reviewer opinions.
- When live search is unavailable, state that Current can only reason from provided source packets.
- Use recent papers and reviews for direction mapping, not as proof that a specific empirical claim is true.

## Workflow

1. **Scope the direction**
   - Define disease/domain, method/model/resource, task, modality, and time window.
   - Decide whether the scan is local, recent, benchmark-focused, review-focused, or full-field.
2. **Build search lanes**
   - Seed paper neighborhood: exact title/identifier, references, citations if available.
   - Method lane: model family, assay, computational method, validation style.
   - Domain lane: disease, tissue, omics modality, clinical task, biological mechanism.
   - Benchmark/resource lane: datasets, leaderboards, registries, databases.
   - Review lane: recent reviews, public review records, guidelines, consensus papers.
3. **Record the search boundary**
   - Query/source seed, database/tool, filters, date, inspected count, and reason for stopping.
4. **Classify movement**
   - Emerging: few but recent papers, unstable benchmark, high uncertainty.
   - Consolidating: multiple groups, shared benchmark, repeated validation pattern.
   - Crowded: many similar methods with thin distinction.
   - Challenged: public concerns, failed replications, leakage, contradictory findings.
   - Translating: movement from benchmark to external validation or clinical/wet-lab testing.
5. **Map direction flow**
   - What the seed work inherits.
   - What it adds or claims to add.
   - What parallel works are doing.
   - What evidence gap remains open.
6. **Prepare handoff**
   - To Reef for resources, datasets, KG, benchmark, or provenance issues.
   - To Iceberg for claim-risk audit.
   - To Anchor for validation or benchmark design.
   - To Compass for research planning or idea prioritization.

## Output Artifact

```markdown
一、Current任务定义
- Direction seed:
- Scope:
- Time window:
- Search boundary:
- Current evidence state:

二、检索/来源边界
| Lane | Query/source seed | Source/database | Filters | Inspected | Boundary note |
|---|---|---|---|---:|---|

三、方向流动图
| Direction node | Evidence inspected | Movement type | Why it matters | Confidence | Limit |
|---|---|---|---|---|---|

四、邻近工作/压力信号
| Source | Relationship to seed | What it supports | What it does not support | Downstream use |
|---|---|---|---|---|

五、机会与风险
| Opportunity/risk | Basis | Missing evidence | Suggested next module |
|---|---|---|---|

六、Current边界
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

七、Handoff Ticket
| Next module | Reason | Input packet | Stop condition |
|---|---|---|---|
```

## Stop Conditions

Stop or downgrade trend claims when:

- the scan only inspected one paper, one abstract, or one search snippet;
- search tools are unavailable and no source packets were provided;
- the time window is undefined but the user asks for "latest" or "current";
- related papers cannot be traced to identifiers or URLs;
- the observed literature is too sparse to support field movement claims.

## Failure Modes

- Turning a local paper neighborhood into a field-wide trend.
- Calling a direction "hot" without time-bounded search evidence.
- Treating reviews as direct empirical proof.
- Treating public review pressure as ground truth.
- Ignoring contradictory or negative findings.
