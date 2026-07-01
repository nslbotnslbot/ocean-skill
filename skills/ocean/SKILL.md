---
name: ocean
description: >-
  OCEAN: Orchestrated Claim-Evidence Analysis Navigator for biomedical research claim-evidence navigation across medical and biological research. Use it to scan evidence, build source packets, audit claims, check leakage/validation/benchmark fairness/reproducibility, review manuscripts, inspect biomedical AI or biological AI studies, evaluate database/KG evidence, plan validation, judge journal positioning, or clarify collaboration contribution boundaries. Do not use for summary-only reading or inventing missing data.
---

# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

Use OCEAN to judge whether biomedical research claims are supported by available evidence across medical and biological research. The goal is not to praise or summarize the work. The goal is to identify the real contribution, evidence gaps, overclaims, publication positioning, and the user's realistic contribution boundary.

## Operating Rules

- Respond in Chinese by default unless the user requests another language.
- Use only evidence present in the workspace, provided by the user, or explicitly obtained with available tools. Do not invent data, sample sizes, validation results, author roles, journal requirements, or experimental outcomes.
- State what was inspected, what was not inspected, and what cannot be concluded when evidence is incomplete.
- Separate hypothesis, association, database annotation, text-mining co-occurrence, model prediction, and causal mechanism.
- Prefer direct, critical wording over vague encouragement.

## Module Order

Use the OCEAN module order when the task spans multiple steps:

1. **Sounding**: scan literature, evidence, DOI/preprint/public review sources, and build traceable source packets.
2. **Current**: analyze field trends and direction flow.
3. **Reef**: organize knowledge graph, database, benchmark, cohort, and resource evidence.
4. **Iceberg**: audit claim support beneath surface-level conclusions.
5. **Anchor**: design validation, replication, benchmark, leakage, and reproducibility checks.
6. **Compass**: turn evidence into research plans, experiment design, idea prioritization, and journal strategy.
7. **Harbor**: preserve audit reports, decision notes, and collaboration boundary records.

## Resource Routing

- Read `references/output-contract.md` for any substantive OCEAN answer unless the user explicitly requests a free-form response. Use it to choose quick, standard, or deep output mode and keep headings/tables consistent.
- Read `references/sounding.md` when the user asks to scan literature or evidence, find sources for a claim, gather DOI/preprint/public review materials, build a source packet, or prepare evidence before claim audit, trend analysis, KG/resource organization, validation planning, or idea generation.
- Read `references/audit-lenses.md` when evaluating manuscripts, AI-agent systems, biomedical AI, knowledge graphs, databases, clinical prediction studies, or publication readiness.
- Read `references/claim-evidence-table.md` when extracting, rewriting, or scoring claims.
- Read `references/reviewer-lens.md` when the user asks for reviewer-style critique, pre-submission risk prediction, likely objections, response preparation, or journal-tier stress testing.
- Read `references/review-report.md` when the user needs a structured long-form review report or collaboration/journal-positioning memo.
- Use `evals/forward-test-cases.md` only for manual pre-release testing of this skill. Do not treat eval prompts as scientific evidence.
- Use `scripts/make_claim_table.py` to create a claim-audit CSV template when a file-based claim inventory would help.
- Use `scripts/check_claim_table.py` after the claim CSV is filled to summarize weak or high-risk claims.
- Use `scripts/make_review_skeleton.py` when the user wants a reusable markdown review skeleton.

## Workflow

1. Select the output mode from `references/output-contract.md`: quick for narrow questions, standard by default, deep for full manuscript/reviewer-style reports.
2. Establish the evidence boundary: list the files, passages, figures, tables, results, notes, or search sources inspected; mark missing or unreadable evidence.
3. If the task requires discovery, use Sounding first. Read `references/sounding.md`, define the search question, record source/search boundaries, triage source tiers, build source packets, map negative space, and create handoff tickets before making downstream claims.
4. Classify the request mode and evidence state: Sounding evidence scan, claim audit, manuscript/project review, reviewer-risk review, journal positioning, collaboration/authorship boundary, anti-hallucination boundary check, or idea extraction from reviews.
5. Classify the work as one or more of: methodology article, resource/database article, system/platform article, application validation article, scientific discovery article, review/perspective/commentary, or collaboration/pre-submission advisory case.
6. Extract central claims. For each major claim, record the evidence source, evidence type, support verdict, causal strength, missing validation, and overstatement risk. Use `references/claim-evidence-table.md` and `references/output-contract.md` for the table schema.
7. Audit reliability using the relevant lenses in `references/audit-lenses.md`: data clarity, label definition, leakage, validation, benchmark fairness, ablation, calibration/decision utility, database evidence hierarchy, AI-agent reproducibility, and biomedical causal caution.
8. Apply the reviewer lens when useful: identify the most likely major criticisms, what evidence would neutralize them, and which claims should be downgraded before submission.
9. Judge publication positioning realistically. Explain the stretch tier, realistic tier, backup tier, likely reviewer objections, and what would be needed to move up one tier.
10. Judge collaboration contribution as light, medium, deep, or authorship-level. Clarify which tasks are advisory and which could justify co-authorship.
11. Output in the selected fixed mode. Keep section order stable; write "不适用" with a reason instead of deleting standard sections.

## Default Output Contract

Use `references/output-contract.md` unless the user requests another format.

- **Quick mode** for narrow questions: conclusion, evidence boundary, key claim handling, next steps.
- **Standard mode** by default: audit card, evidence boundary, claim-evidence matrix, risks, missing evidence, contribution boundary, journal positioning, next actions, and 0-10 scores.
- **Deep mode** for full reports: standard mode plus reviewer concerns, claim rewrites, and decision memo.

Do not vary headings casually. Consistency is part of the skill.

## Scoring

Score each dimension from 0 to 10 and use low scores when evidence is missing:

- Scientific question clarity
- Novelty
- Methodological rigor
- Data reliability
- Validation strength
- Benchmark fairness
- Reproducibility
- Domain insight
- Publication readiness
- User contribution potential

Do not inflate scores to be polite. If a conclusion is unsupported, downgrade it to a hypothesis or recommendation.
