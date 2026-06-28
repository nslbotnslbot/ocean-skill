# Public Source Protocol

Use this protocol to choose real, source-traceable materials for manual forward tests. Do not copy large passages of papers or peer review reports into the skill. Store only links, identifiers, short source notes, and the eval case each source supports.

Use `source-candidates.md` as the working candidate log. Keep this protocol generic and keep concrete source choices in that log.

## Acceptable Source Types

### DOI Paper

Use a published article with a DOI when testing:

- claim support
- journal positioning
- reviewer-style critique
- publication-readiness scoring

Record:

- title
- DOI
- journal
- article URL
- inspected sections, figures, or tables
- whether peer review material is available

### bioRxiv Or medRxiv Preprint

Use a preprint when testing:

- evidence-bound caution
- preprint vs peer-reviewed status
- overclaiming before validation
- "what is needed before submission" advice

Record:

- title
- preprint DOI or URL
- version/date inspected
- article type or subject area
- whether linked reviews, journal versions, or comments exist

Do not treat a preprint as peer-reviewed unless a linked journal version or public review source is explicitly inspected.

### Public Peer Review Report

Use public review material when testing:

- reviewer-lens behavior
- major/minor concern classification
- claim downgrade rules
- response-to-reviewer planning

Suitable sources include:

- Nature Portfolio transparent peer review files
- eLife reviewed preprints with public reviews and assessments
- BMC journals with open peer review or pre-publication history
- OpenReview conference reviews
- Review Commons or other preprint review services

Record:

- article or submission title
- review source URL
- associated DOI, preprint DOI, arXiv ID, or OpenReview forum URL
- review type: journal review, conference review, public preprint review, author response, editorial decision letter
- which eval case it supports

## Selection Criteria

Prefer sources that have at least one of:

- biomedical AI, bioinformatics, single-cell, clinical prediction, AI-agent, knowledge graph, database, or scientific discovery claims
- strong mechanism, causality, generalization, or clinical utility wording
- visible validation limitations or reviewer criticism
- public reviews with author responses

Avoid sources when:

- the review text is not public
- the license or page terms forbid reuse beyond reading/linking
- the article requires access that cannot be reproduced by another evaluator
- the material is too large to inspect within one eval session

## Candidate Log Template

| ID | Source type | Title | Identifier / URL | Why useful | Eval case | Inspected evidence | Status |
|---|---|---|---|---|---|---|---|
| S1 | DOI paper |  |  |  |  |  | candidate |
| S2 | bioRxiv/medRxiv |  |  |  |  |  | candidate |
| S3 | public peer review |  |  |  |  |  | candidate |

Concrete candidates live in `source-candidates.md`.

## Use Rules

- Read the source before using it in an eval.
- Cite the source URL in the eval notes.
- Do not infer uninspected figures, datasets, sample sizes, validation cohorts, or reviewer positions.
- When only abstract/title/review snippets are inspected, mark the evidence boundary clearly.
- Keep source notes short enough that the skill remains a workflow, not a dataset.
