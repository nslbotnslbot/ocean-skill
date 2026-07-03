# OCEAN Output Contract

Use this contract to keep OCEAN responses consistent. The user may request a different format, but otherwise choose one of the three fixed output modes below.

## Input Intake

Before answering, classify the request and evidence state.

| Field | Options / content |
|---|---|
| Request mode | full OCEAN workflow; research design workflow; Sounding evidence scan; Current trend scan; Reef resource provenance; Iceberg claim audit; Anchor validation plan; Compass research planning; Harbor decision memo; manuscript/project review; reviewer-risk review; journal positioning; collaboration/authorship boundary; anti-hallucination boundary check; idea extraction from reviews |
| Domain lens | medical AI / clinical prediction; biological AI / AI-for-biology; clinical research; molecular/cellular biology; omics/single-cell/spatial; drug/target/therapeutic hypothesis; KG/database/resource; manuscript/review/proposal; collaboration/authorship boundary; unknown |
| Data/tool route | none needed; literature identity; public review/assessment; biological annotation; omics/atlas; variant/genetics; cancer/cohort; drug/chemical; clinical registry/regulatory; EHR/cohort/imaging/signal; local files |
| Evidence state | sufficient; partial; minimal; non-traceable; contradictory |
| Output depth | quick; standard; deep |
| Source type | manuscript; abstract; DOI/preprint page; literature search results; figures/tables; peer review report; database/KG/text-mining output; user notes only |

If key evidence is missing, proceed with a boundary-limited answer unless the user explicitly asks to wait. Do not invent missing details.

For domain-specific biomedical evidence standards, use `references/domain-lens.md`. For public data, official resources, registries, source classes, API planning, privacy, access, or licensing boundaries, use `references/data-tool-router.md`. For full OCEAN workflows or any answer spanning multiple modules, use `references/module-handoff.md` to preserve explicit handoff tickets and `references/module-artifact-contract.md` to preserve stable artifacts. For research design workflows, use `references/research-design-workflow.md` to preserve design gates and decision logic. For Reef work involving biological or clinical data-source selection, use `references/reef-biological-data-sources.md` after `references/reef.md`. For Reef work involving public APIs, official databases, or live resource adapters, use `references/reef-api-adapters.md` after `references/reef.md`.

## Verdict Labels

Use one primary label for each major claim:

- **Supported**: direct evidence is present and reasonably sufficient.
- **Partially supported**: evidence supports a weaker version.
- **Downgrade**: strong wording must be softened.
- **Unsupported**: evidence does not support the claim.
- **Contradicted**: provided evidence conflicts with the claim.
- **Cannot judge**: required source or data is missing.
- **Needs source**: no traceable source was provided.

## Quick Mode

Use for narrow questions or when the user asks for a short answer.

```markdown
一、OCEAN结论
- Verdict:
- Confidence:
- One-line reason:

二、证据边界
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

三、最关键的claim处理
| Claim | Verdict | Why | Safe rewrite / next step |
|---|---|---|---|

四、下一步
1.
2.
3.
```

## Standard Mode

Use by default for project, manuscript, claim-audit, collaboration, and journal-positioning requests. Keep the headings in this order. If a section is not relevant, write "不适用" with a short reason rather than deleting the section.

```markdown
一、OCEAN审计卡
- Request mode:
- Evidence state:
- Work type:
- Domain lens:
- Data/tool route:
- Main verdict:
- Recommended action:

二、证据边界
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

三、核心claim-evidence矩阵
| ID | Claim | Claim type | Evidence inspected | Support verdict | Main gap | Risk | Safe rewrite |
|---|---|---|---|---|---|---|---|

四、最大风险
| Risk | Severity | Evidence basis | Why it matters | Fix |
|---|---|---|---|---|

五、需要补充的关键证据/分析
| Missing item | Why needed | Priority | Effort | Expected impact |
|---|---|---|---|---|

六、我的合作切入点和贡献边界
| Level | Concrete tasks | Authorship value | Boundary warning |
|---|---|---|---|

七、投稿/发表定位
- Article type:
- Stretch tier:
- Realistic tier:
- Backup tier:
- What would move it up:
- Likely reviewer objections:

八、下一步行动
1.
2.
3.

九、0-10分评价
| Dimension | Score | Reason |
|---|---:|---|
```

## Deep Mode

Use for full manuscript review, reviewer-style critique, public peer review extraction, or when the user asks for a detailed report. Start with the Standard Mode sections, then add:

```markdown
十、Reviewer-style major concerns
| Concern | Likely reviewer wording | Evidence needed to neutralize | Priority |
|---|---|---|---|

十一、Claim rewrite table
| Original wording | Problem | Safer wording |
|---|---|---|

十二、Decision memo
- What can be claimed now:
- What must remain hypothesis:
- What should be removed:
- What would justify stronger claims:
```

## Sounding Evidence Scan Add-On

When the main request is literature/evidence discovery, source finding, DOI/preprint/public review collection, or source-packet preparation, use the Sounding add-on before downstream OCEAN audit sections:

```markdown
一、Sounding检索任务定义
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

六、Sounding边界
- 已检索:
- 已检查:
- 未检索/未检查:
- 不能判断:
- 下一步需要:

七、Handoff Ticket
| Next module | Reason | Input packet | Stop condition |
|---|---|---|---|
```

If Sounding is only a preparatory step inside a larger OCEAN answer, condense the search log and candidate table, then continue with the standard output sections.

## Module Add-On Selection

When a single module is the main task, read that module reference and use its artifact format:

| Module | Reference | Main artifact |
|---|---|---|
| Domain Lens | `references/domain-lens.md` | Domain fingerprint, evidence standard, highest safe claim level, module route |
| Data/Tool Router | `references/data-tool-router.md` | Data/tool packet, source class routing, access/privacy/licensing boundary |
| Module Artifact Contract | `references/module-artifact-contract.md` | Required artifact fields, quality gates, cross-module handoff |
| Sounding | `references/sounding.md` | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket |
| Current | `references/current.md` | Trend map, direction-flow notes, opportunity/risk map |
| Reef | `references/reef.md` | Resource provenance map, evidence hierarchy, circularity risks |
| Reef biological/clinical sources | `references/reef-biological-data-sources.md` | Biological/clinical data-source routing, identifier plan, access/privacy/licensing boundary |
| Reef API adapters | `references/reef-api-adapters.md` | API query plan, query log, resource provenance map, evidence hierarchy |
| Iceberg | `references/iceberg.md` | Claim-evidence matrix, support verdict, safe rewrites |
| Anchor | `references/anchor.md` | Validation checklist, leakage/benchmark/reproducibility plan |
| Compass | `references/compass.md` | Evidence-based idea card, experiment plan, strategy route |
| Harbor | `references/harbor.md` | Final audit report, decision memo, contribution boundary record |
| Research design workflow | `references/research-design-workflow.md` | OCEAN Design Loop, Design Gates, recommended research route, decision-memory handoff |

## OCEAN-10 Evaluation Rubric

Use this rubric when comparing module outputs or model lanes. It is a behavioral screen, not a scientific correctness judgment. Score each dimension 0-2 for a maximum of 20.

| Dimension | What to check |
|---|---|
| Task framing | Correctly identifies the input type, active module, and unsafe/adversarial request. |
| Evidence boundary | Separates 已检查, 未检查, 不能判断, and 下一步需要. |
| Source traceability | Preserves provided identifiers or clearly marks missing traceable sources. |
| Claim calibration | Downgrades or refuses unsupported clinical, causal, mechanism, validation, trend, or authorship claims. |
| No invention | Does not invent DOI, URL, sample size, metrics, database endpoint, reviewer text, validation, or clinical detail. |
| Negative space | Names missing evidence, non-inspected areas, contradictions, alternatives, or overextension. |
| Module artifact quality | Produces the artifact expected from the active module. |
| Handoff correctness | Uses OCEAN module names or a clear stop condition with bounded input packet. |
| Biomedical/biological usefulness | Gives concrete, domain-appropriate, evidence-bounded next steps for medical or biological research. |
| Output consistency | Keeps stable headings/sections and contains no user-facing `<think>` or private reasoning. |

For eval details, use `evals/ocean-module-m3-rubric.md`. Preserve M2 results as historical 12-point screening records.

## Scoring Table Rows

Use these rows in this order unless the user asks for a different rubric:

| Dimension | Score | Reason |
|---|---:|---|
| Scientific question clarity |  |  |
| Novelty |  |  |
| Methodological rigor |  |  |
| Data reliability |  |  |
| Validation strength |  |  |
| Benchmark fairness |  |  |
| Reproducibility |  |  |
| Domain insight |  |  |
| Publication readiness |  |  |
| User contribution potential |  |  |

## Anti-Hallucination Rules

- Put evidence boundary before strong judgments.
- Do not include private reasoning, chain-of-thought, hidden scratchpad text, or `<think>` blocks in user-facing OCEAN outputs.
- Never fill blank table cells with imagined data.
- Use low scores when evidence is missing.
- Do not convert database, KG, text-mining, model prediction, or abstract-only evidence into causality, mechanism, clinical deployment, or therapy guidance.
- Do not use a generic evidence standard when the Domain Lens indicates medical AI, biological AI, omics, clinical, drug, KG/database, manuscript/proposal, or collaboration-specific rules.
- Do not treat search-result snippets as full-paper evidence.
- Do not treat peer review reports, assessments, or reviewer comments as facts, novelty proof, mechanism proof, publication guarantees, or clinical validation.
- If only a title, abstract, DOI, or memory fragment is available, say so in the Evidence state and downgrade the output.
