# Sonar Evidence Discovery

Use Sonar when the user asks OCEAN to scan literature, find evidence, gather DOI/preprint/public review sources, map evidence around a claim, or prepare source packets before downstream claim audit, trend analysis, knowledge graph organization, validation planning, journal positioning, or idea generation.

Sonar is not a paper-summary mode or a citation manager. Its job is to produce traceable evidence coordinates: what was searched, what was inspected, what each source can and cannot support, what remains missing, and which OCEAN module should handle the next step.

## Core Questions

- What exact claim, object, method, dataset, disease, mechanism, or review signal is being searched?
- Which sources were searched or provided?
- Which sources were actually inspected?
- What evidence type does each source provide?
- What claims can be checked now?
- What remains missing before stronger scientific, mechanism, clinical, novelty, or publication conclusions are allowed?
- Which downstream module should receive the source packet?

## Safety Rules

- Treat user claims as audit targets, not facts.
- Do not invent papers, DOIs, URLs, sample sizes, datasets, reviewer comments, benchmark results, publication status, or validation outcomes.
- Do not treat search-result snippets as full-paper evidence.
- Do not treat a DOI, title, abstract, landing page, preprint page, or public review summary as proof of methods/results not inspected.
- Do not convert KG/database/text-mining/model-prediction evidence into mechanism, causality, clinical utility, or therapy guidance by itself.
- Do not treat peer review reports, eLife assessments, OpenReview comments, PubPeer comments, or reviewer opinions as experimental facts, novelty proof, publication guarantees, or clinical validation.
- If live search tools, web access, or source databases are unavailable, state that Sonar can only work from provided local materials.
- Keep a search log whenever discovery is performed: query or source seed, source/database, filters, date, inspected result count, and notes.
- Prefer primary sources for evidence claims: paper, preprint, protocol, dataset, code repository, registry, public peer review record, or official database entry.
- Use reviews and perspectives for context, not as direct evidence for a specific empirical claim unless the review itself is the object being audited.

## Source Tiers

| Tier | Source type | Use | Caution |
|---|---|---|---|
| S1 | Full paper, preprint PDF/full text, protocol, dataset, code, clinical registry, public peer review full record | Primary evidence for claim audit | Inspect relevant sections before making specific claims |
| S2 | Abstract, DOI page, PubMed/arXiv/bioRxiv/medRxiv page, publisher landing page, visible assessment metadata | Source packet and triage | Abstract/landing-level only; cannot support detailed methods/results claims |
| S3 | Review, perspective, editorial, benchmark overview | Context, terminology, competing framing | Do not use as direct validation for a specific study claim |
| S4 | Database, KG, text-mining, ontology, pathway, or association record | Association, annotation, candidate evidence | Not mechanism, causality, or clinical utility by itself |
| S5 | News, blog, social media, non-traceable notes | Background only | Needs primary-source confirmation |

## Sonar Workflow

1. **Mission framing**: Parse the request into searchable units:
   - target claim;
   - disease/domain/task;
   - method/model/resource;
   - evidence type needed;
   - source constraints or time range;
   - whether peer review/public review should be included.
2. **Query/source map**: Build one or more query forms:
   - exact DOI/title/preprint ID;
   - keyword query;
   - method + domain query;
   - dataset/benchmark query;
   - claim-specific query;
   - peer review / open review query.
3. **Source discovery**: Search using available tools or user-provided sources. Prefer source-specific tools when available, such as PubMed, Crossref, arXiv, Semantic Scholar, publisher pages, preprint servers, OpenReview, PubPeer, journal public review pages, clinical registries, or official databases.
4. **Source fingerprinting**: For each retained source, record title, identifier, URL, source tier, inspected content, evidence type, main limitation, and provenance concerns.
5. **Evidence radar mapping**: Map each source to evidence zones:
   - seed/landing page;
   - abstract;
   - full text;
   - methods/supplement;
   - figures/tables;
   - code/data/protocol;
   - review/assessment;
   - independent validation;
   - wet-lab/in vivo/clinical validation.
6. **Negative space audit**: Explicitly list what was not found, not inspected, inaccessible, contradicted, or insufficient to infer.
7. **Handoff ticket**:
   - to Current for trend / direction-flow analysis;
   - to Reef for database/KG/resource provenance;
   - to Iceberg for claim-evidence audit and safe rewrites;
   - to Anchor for validation, replication, benchmark, leakage, or reproducibility checks;
   - to Compass for planning, experiment design, journal strategy, or idea prioritization;
   - to Harbor for report/workspace memory.

## Output Format

Use this add-on when Sonar is the main task or a necessary preparation step:

```markdown
一、Sonar检索任务定义
- 目标问题/claim:
- 检索范围:
- 需要的证据类型:
- 是否包含peer review/public review:
- 当前证据状态:

二、检索记录
| Query/source seed | Source/database | Filters | Date | Results inspected | Notes |
|---|---|---|---|---:|---|

三、候选来源表
| ID | Source | Identifier/URL | Tier | Why included | Inspected content | Main evidence | Main limitation | Downstream handoff |
|---|---|---|---|---|---|---|---|---|

四、Evidence Radar Map
| Claim/question | Landing/abstract | Full text | Methods/supplement | Data/code | Review/assessment | Independent validation | Wet/clinical validation |
|---|---|---|---|---|---|---|---|

五、Negative Space
- 未检查:
- 未找到:
- 不可推出:
- 矛盾或过度外推:
- 需要补充:

六、Sonar边界
- 已检索:
- 已检查:
- 未检索/未检查:
- 不能判断:
- 下一步需要:

七、Handoff Ticket
| Next module | Reason | Input packet | Stop condition |
|---|---|---|---|
```

If Sonar is only a brief preparatory step, condense the tables but preserve the same logic: search/source boundary, candidate sources, negative space, and handoff.

## Strict Gate Labels

Use these labels when evaluating a source packet or a user claim:

- **Pass**: the current inspected evidence is sufficient for the stated limited claim.
- **Partial**: evidence supports a weaker or narrower version.
- **Reject/Downgrade**: the claim overstates what the inspected evidence supports.
- **Cannot judge**: key source material is missing or inaccessible.
- **Boundary fail**: Sonar could not establish a traceable source/evidence boundary.

Passing Sonar means the evidence boundary and source packet are usable. It does not mean the underlying science is true or publication-ready.

## Peer Review Discovery

When searching peer review material:

- Prefer public review records from journals, OpenReview, PubPeer, preprint commentary pages, publisher-hosted peer review files, or official assessment pages.
- Record whether the review is public, user-provided/private, simulated, or inferred.
- Do not copy long review passages. Extract pressure signals and keep source anchors.
- Treat reviewer comments as pressure signals, not as facts, novelty proof, mechanism proof, or publication guarantees.

## Stop Conditions

Stop and state limits when:

- only a vague topic is provided and no search tools are available;
- a source cannot be traced to a DOI, URL, title, local file, or official database record;
- publication, novelty, mechanism, or clinical claims are requested but only abstract-level evidence is available;
- current literature coverage is required but live search is unavailable;
- a source is behind access restrictions and no abstract/full text/metadata is available;
- search is expanding without improving evidence coverage.
