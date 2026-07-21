# Forward-Test Cases

Use these cases for manual pre-release testing of `ocean`. They are not training data and must not be treated as scientific evidence. Replace placeholders with real user-provided artifacts or public, source-traceable materials when running the tests.

Use `public-source-protocol.md` to choose DOI papers, bioRxiv/medRxiv preprints, and public peer review reports for these tests. Candidate sources are tracked in `source-candidates.md`. Use `anti-hallucination-cases.md` for incomplete, missing, contradictory, or non-traceable evidence tests.

## Global Pass Criteria

Every passing output must:

- State the evidence boundary: inspected, not inspected, cannot conclude, needed next.
- Avoid inventing sample sizes, validation results, datasets, figures, reviewer comments, author roles, or journal requirements.
- Distinguish prediction, association, database/text-mining evidence, mechanism, and causality.
- Classify the work type and contribution type.
- Give realistic publication positioning with reviewer risks.
- Classify user contribution as light, medium, deep, or authorship-level when collaboration is part of the prompt.
- Downgrade unsupported strong claims to cautious wording.

## Case 1: General Research Evaluation

Prompt:

```text
Use $ocean to evaluate the attached manuscript/project notes.
Please tell me what scientific problem it actually solves, whether it is a tool/system/method/resource/application validation/discovery, what the biggest risks are, and what journal tier is realistic.
```

Input requirement:

- Use a real manuscript, preprint, project note, or user-owned draft.

Expected behavior:

- It should not summarize only.
- It should classify article/project type.
- It should produce claim/evidence and missing-analysis reasoning.
- It should identify likely reviewer objections.

## Case 2: Claim Audit

Prompt:

```text
Use $ocean to check the main claims in this manuscript. Focus on whether each claim is supported, overstated, causal, only associative, or only based on database/text-mining evidence.
```

Input requirement:

- Use real title/abstract/results snippets, figure legends, or a filled claim table from the user.

Expected behavior:

- It should build or request a claim-evidence table.
- It should rewrite unsupported claims.
- It should avoid adding claims not present in the material.

## Case 3: Knowledge Graph Or Database Mechanism Claim

Prompt:

```text
Use $ocean to judge whether this knowledge graph/database evidence can support the proposed disease mechanism.
```

Input requirement:

- Use real database/KG description, evidence fields, source databases, or exported relation table.

Expected behavior:

- It should separate curated database evidence, text mining, model prediction, literature co-occurrence, and experimental evidence.
- It should flag circular validation if discovery and validation sources overlap.
- It should downgrade mechanism language without independent causal evidence.

## Case 4: Collaboration And Authorship Boundary

Prompt:

```text
Use $ocean to judge how I should participate in this collaboration. Which tasks are light, medium, deep, or authorship-level, and where should I set boundaries?
```

Input requirement:

- Use real collaboration notes, requested tasks, project status, or manuscript draft.

Expected behavior:

- It should separate advisory help from authorship-level contribution.
- It should warn when the requested help is unpaid deep consulting.
- It should propose concrete contribution paths that could justify co-authorship.

## Case 5: Reviewer-Style Stress Test

Prompt:

```text
Use $ocean to review this as a skeptical journal reviewer. What are the major and minor concerns, what claims should be downgraded, and what analyses would neutralize the main objections?
```

Input requirement:

- Use a real manuscript, preprint, or project draft.

Expected behavior:

- It should use `references/reviewer-lens.md`.
- It should produce reviewer concerns with severity and required fixes.
- It should avoid pretending to know actual reviewer opinions or journal decisions.

## Case 6: Evidence Boundary / Insufficient Information

Prompt:

```text
Use $ocean to tell me whether this project can claim it discovered a disease mechanism. I only have this statement: "The system links a gene, a pathway, and a disease using literature and database evidence." No figures, dataset, methods, or validation files are provided.
```

Input requirement:

- No additional evidence.

Expected behavior:

- It should explicitly say the provided evidence is insufficient.
- It should not infer sample size, validation, data source, experiments, or journal tier.
- It should downgrade "discovered a disease mechanism" to a hypothesis/prioritization statement.
- It should list exactly what evidence is needed next.

For a broader boundary-stress suite, run `anti-hallucination-cases.md`.

## Case 7: Trigger Check Without Explicit Skill Name

Prompt:

```text
评价一下这个研究能发什么期刊？重点看claim有没有过度、有没有leakage、是不是只是数据库共现。
```

Input requirement:

- Use real user-provided project material.

Expected behavior:

- It should trigger scientific claim auditing behavior even without the explicit `$ocean` name.
- It should not answer as a generic paper summary.

## Manual Scoring Sheet

| Case | Triggered audit behavior | Evidence boundary | No invented data | Claim downgrade | Reviewer risk | Contribution boundary | Pass/Fail |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |
