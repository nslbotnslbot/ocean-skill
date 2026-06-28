# Sonar Evidence Discovery

Use Sonar when the user asks OCEAN to scan literature, find evidence, gather DOI/preprint/public review sources, map evidence around a claim, or prepare a source packet before claim audit, trend analysis, knowledge graph organization, validation planning, or research idea generation.

Sonar is not a general summary mode. Its job is to build a traceable evidence packet that downstream OCEAN modules can inspect.

## Core Role

Sonar answers:

- What exactly are we looking for?
- Which sources were searched?
- Which sources were found and inspected?
- What evidence type does each source provide?
- Which claims can be checked from these sources?
- What remains missing before stronger conclusions are allowed?

## Safety Rules

- Do not invent papers, DOIs, URLs, sample sizes, datasets, reviewer comments, benchmark results, or publication status.
- Do not treat search-result snippets as full-paper evidence.
- Do not treat a DOI, title, abstract, or preprint page as proof of methods/results not inspected.
- If live search tools, web access, or source databases are unavailable, state that Sonar can only work from provided local materials.
- Keep a search log when performing discovery: query, source/database, filters, date, and inspected result count.
- Prefer primary sources for evidence claims: paper, preprint, protocol, dataset, code repository, registry, public peer review record, or official database entry.
- Use reviews and perspectives for context, not as direct evidence for a specific empirical claim unless the review itself is the object being audited.

## Source Tiers

| Tier | Source type | Use | Caution |
|---|---|---|---|
| S1 | Full paper, preprint, protocol, dataset, code, clinical registry, public peer review record | Primary evidence for claim audit | Must inspect relevant sections before making specific claims |
| S2 | Abstract, DOI page, PubMed/arXiv/bioRxiv/medRxiv page, publisher landing page | Initial source packet and triage | Abstract-level only; cannot support detailed methods/results claims |
| S3 | Review, perspective, editorial, benchmark overview | Context, terminology, competing framing | Do not use as direct validation for a specific study claim |
| S4 | Database/KG/text-mining record | Association, annotation, candidate evidence | Not mechanism, causality, or clinical utility by itself |
| S5 | News, blog, social media, non-traceable notes | Background only | Needs primary-source confirmation |

## Discovery Workflow

1. Parse the user's request into searchable units:
   - target claim;
   - disease/domain/task;
   - method/model/resource;
   - evidence type needed;
   - time range or journal/source constraints;
   - whether peer review reports should be included.
2. Build a query map. Use multiple query forms when needed:
   - exact title/DOI/preprint ID;
   - keyword query;
   - method + domain query;
   - dataset/benchmark query;
   - claim-specific query;
   - peer review / open review query.
3. Search using available tools or user-provided sources. Prefer source-specific tools when available, such as PubMed, Crossref, arXiv, Semantic Scholar, publisher pages, preprint servers, OpenReview, PubPeer, or journal public review pages.
4. Triage results by relevance and evidence tier. Exclude unrelated, duplicate, inaccessible, or non-primary sources unless they are useful for context.
5. Create a source packet for each retained source. Include title, identifier, URL, source tier, inspected sections, key claim/evidence, limitations, and downstream module handoff.
6. Summarize evidence coverage. State which claims can be audited now and which require full text, figures, methods, supplements, code, data, or external validation.
7. Hand off:
   - to Current for trend / direction-flow analysis;
   - to Reef for database/KG/resource organization;
   - to Iceberg for claim-evidence audit;
   - to Anchor for validation, replication, benchmark, and leakage checks;
   - to Compass for planning, experiment design, journal strategy, or idea prioritization;
   - to Harbor for report/workspace memory.

## Sonar Output Add-On

When Sonar is the main task, use this section before downstream OCEAN audit sections:

```markdown
一、Sonar检索任务定义
- 目标问题/claim:
- 检索范围:
- 需要的证据类型:
- 是否包含peer review/public review:
- 当前证据状态:

二、检索记录
| Query | Source/database | Filters | Date | Results inspected | Notes |
|---|---|---|---|---:|---|

三、候选来源表
| ID | Source | Identifier/URL | Tier | Why included | Inspected content | Main evidence | Main limitation | Downstream handoff |
|---|---|---|---|---|---|---|---|---|

四、证据覆盖与缺口
| Claim/question | Evidence found | Evidence tier | Coverage | Missing evidence | Next module |
|---|---|---|---|---|---|

五、Sonar边界
- 已检索:
- 已检查:
- 未检索/未检查:
- 不能判断:
- 下一步需要:
```

If Sonar is only a preparatory step inside a larger OCEAN answer, condense this into a short evidence-discovery note and then continue with the standard OCEAN output.

## Peer Review Discovery

When searching peer review material:

- Prefer public review records from journals, OpenReview, PubPeer, preprint commentary pages, or publisher-hosted peer review files.
- Record whether the review is public, user-provided/private, simulated, or inferred.
- Do not copy long review passages. Extract pressure signals and keep source anchors.
- Hand off to `reviewer-to-idea.md` only after Sonar has identified the review source and evidence boundary.

## Stop Conditions

Stop and ask for more sources or state limits when:

- only a vague topic is provided and no search tools are available;
- a source cannot be traced to a DOI, URL, title, or local file;
- the user asks for publication or novelty claims but only abstract-level evidence is available;
- the task requires current literature coverage but live search is unavailable;
- a source is behind access restrictions and no abstract/full text/metadata is available.
