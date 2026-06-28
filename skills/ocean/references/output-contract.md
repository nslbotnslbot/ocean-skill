# OCEAN Output Contract

Use this contract to keep OCEAN responses consistent. The user may request a different format, but otherwise choose one of the three fixed output modes below.

## Input Intake

Before answering, classify the request and evidence state.

| Field | Options / content |
|---|---|
| Request mode | claim audit; manuscript/project review; reviewer-risk review; journal positioning; collaboration/authorship boundary; anti-hallucination boundary check; idea extraction from reviews |
| Evidence state | sufficient; partial; minimal; non-traceable; contradictory |
| Output depth | quick; standard; deep |
| Source type | manuscript; abstract; DOI/preprint page; figures/tables; peer review report; database/KG/text-mining output; user notes only |

If key evidence is missing, proceed with a boundary-limited answer unless the user explicitly asks to wait. Do not invent missing details.

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
- Never fill blank table cells with imagined data.
- Use low scores when evidence is missing.
- Do not convert database, KG, text-mining, model prediction, or abstract-only evidence into causality, mechanism, clinical deployment, or therapy guidance.
- If only a title, abstract, DOI, or memory fragment is available, say so in the Evidence state and downgrade the output.
