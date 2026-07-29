# Blinded Human Adjudication Protocol

## Purpose

Determine whether an output is scientifically safer and still useful without
letting reviewers know which model, prompt, or workflow produced it.

## Review design

1. Two domain experts independently review every case.
2. Output order and system identity are randomized and blinded.
3. Reviewers use the versioned rubric in `../rubrics/`.
4. They record `accepted`, `rejected`, `modified`, or
   `genuinely_ambiguous`.
5. A third expert resolves disagreements when a deterministic consensus rule
   does not apply.
6. Conflicts of interest and relevant expertise are recorded before review.
7. Original outputs are immutable; adjudication is stored as a separate record.

## Required fields

- case ID and rubric version;
- reviewer pseudonymous ID and expertise;
- blinding state;
- decision for each criterion;
- severity and rationale;
- accepted/rejected/modified recommendation;
- review time;
- uncertainty;
- disagreement resolution;
- source locators inspected.

Use `schemas/adjudication_record.schema.json`. Do not include reviewer names,
private correspondence, or manuscript text in the public repository.

## Agreement reporting

Report raw agreement and a chance-adjusted measure appropriate to the data.
For sparse severe errors, report Gwet's AC1 or Krippendorff's alpha alongside
the contingency table. Do not choose a statistic solely because it appears more
favorable.

## Prospective manuscript case

A real manuscript may be evaluated as:

```text
original AI-assisted draft
→ OCEAN audit
→ two blinded independent expert reviews
→ author decision for each suggestion
→ final submitted text
```

One manuscript is a case study, not a benchmark. Submission, posting, review,
acceptance, and publication remain distinct states.
