# Reviewer-To-Idea Workflow

Use this reference when the user wants to extract research opportunities, repair paths, collaboration entry points, or new project ideas from peer review reports, reviewer comments, editor letters, public review histories, rebuttal exchanges, or pre-submission reviewer-style critiques.

Do not treat reviewer comments as facts. Treat them as pressure signals that point to missing evidence, unclear claims, weak validation, or unresolved scientific questions.

## Core Safety Rules

- Do not copy long peer review reports into the answer. Paraphrase the review logic and quote only short necessary fragments if the user provided them.
- Do not infer paper details, author responses, hidden data, reviewer identity, acceptance odds, or journal policy unless explicitly inspected.
- Do not claim an idea is novel only because a reviewer asked for it. Novelty requires literature search and evidence mapping.
- Separate reviewer opinion, manuscript evidence, author rebuttal, and external evidence.
- If only reviewer comments are provided without the manuscript or response, mark the output as review-signal-only.
- If the review report is public, preserve the source URL/DOI and inspected sections. If it is user-provided/private, do not expose sensitive content beyond the user's task.

## Input Classification

Before extracting ideas, classify the source:

| Field | Options / notes |
|---|---|
| Review source | public peer review; journal decision letter; reviewer report; rebuttal exchange; user notes; simulated reviewer critique |
| Manuscript evidence | full manuscript; abstract only; figures/tables; response letter; not provided |
| Review status | pre-submission; rejected; major revision; minor revision; accepted with review history; unknown |
| Use goal | repair current paper; generate new project idea; plan collaboration; design validation; journal strategy |
| Evidence state | sufficient; partial; minimal; non-traceable; contradictory |

## Workflow

1. Establish the evidence boundary: list which review comments, manuscript sections, figures, response letters, and external sources were inspected.
2. Extract reviewer pressure points. Classify each as claim support, method, data, validation, benchmark, mechanism, clinical utility, reproducibility, writing/framing, or scope.
3. Convert each pressure point into an underlying gap. Avoid preserving reviewer wording if it is vague or emotional; normalize it into a testable missing-evidence statement.
4. Generate idea seeds from gaps:
   - Repair idea: directly fixes the current manuscript.
   - Extension idea: expands the current study with new validation, data, or analysis.
   - Independent project idea: turns a repeated review gap into a standalone research question.
   - Collaboration idea: identifies where the user could contribute with analysis, experiment design, data curation, validation, or writing.
5. Audit each idea with OCEAN claim-evidence rules. State what evidence would be needed before the idea could support a strong claim.
6. Prioritize ideas by feasibility, evidence availability, risk reduction, publication value, and contribution boundary.
7. State what must be searched next. Use literature search before calling anything novel, saturated, or publishable.

## Pressure-Point Map

| Reviewer signal | Underlying gap | Useful idea direction | Evidence needed |
|---|---|---|---|
| Claim is too broad | Claim-evidence mismatch | Narrow claim or add external validation | Direct support for generalized claim |
| Missing baseline | Benchmark fairness gap | Re-run with strong/current baselines | Baseline choice, tuning, identical data splits |
| Possible leakage | Validation design gap | Leakage audit or time/site/entity split | Split protocol, leakage tests, negative controls |
| Mechanism not proven | Evidence-type mismatch | Mechanistic validation or hypothesis reframing | Perturbation, causal design, wet-lab or strong causal evidence |
| Clinical utility unclear | Translation gap | Calibration, decision curve, subgroup and deployment analysis | External cohort, calibration, decision utility, safety analysis |
| Resource usefulness unclear | Adoption/utility gap | User study, benchmark task, API/workflow evaluation | Task definition, expert evaluation, usage metrics |
| Contribution incremental | Novelty/framing gap | Reframe contribution or add new dataset/method/insight | Comparative literature and clear delta over prior work |

## Output Add-On

When the user's main request is idea extraction from reviews, use OCEAN Standard or Deep Mode, then add this section after the risk table or in Deep Mode after reviewer concerns:

```markdown
十、从reviewer意见反推的idea池
| ID | Review signal | Evidence anchor | Underlying gap | Idea seed | Idea type | Needed evidence | Feasibility | Main risk | Contribution boundary |
|---|---|---|---|---|---|---|---|---|---|

十一、优先级排序
| Priority | Idea | Why now | First concrete step | Stop condition |
|---|---|---|---|---|

十二、不能过度声称的地方
- 不能说已经证明:
- 不能说有创新性，除非:
- 不能说可发表，除非:
- 下一步必须检索/补充:
```

If the review material is the only source, keep the conclusion conservative:

```markdown
这是从 reviewer pressure signals 反推出的 idea pool，不是对论文事实、领域空白或创新性的最终判断。下一步需要用 manuscript/full text、相关文献、数据和验证资源来确认。
```

## Collaboration Boundary

For each idea, classify the user's possible contribution:

- Light: framing, claim rewrite, reviewer response wording, checklist.
- Medium: literature/evidence mapping, benchmark table, validation plan, error taxonomy.
- Deep: running analyses, designing experiments, building evaluation datasets, leakage audit, reproducibility package.
- Authorship-level: producing new data, new experiments, substantial analysis, new method, or core revision that materially changes the scientific contribution.

Do not promise authorship. State what work would be needed before authorship-level contribution is plausible.
