# OCEAN Evaluation

This folder contains public-facing evaluation notes for **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**.

These files are for GitHub transparency. They are not runtime instructions for the skill and should not be treated as scientific evidence.

## What Is Included

- `round-1-5-results.md`: concise public summary of strict validation rounds 1-5.
- `reference-materials/public-sources.md`: public DOI, arXiv, bioRxiv, and public-review source identifiers used or prepared for evals.
- `reference-materials/boundary-cases.md`: synthetic boundary-case categories used to test anti-hallucination behavior.

## What Is Not Included

- No private manuscripts.
- No patient data.
- No private peer-review text.
- No large copyrighted paper excerpts.
- No raw hidden-answer logs or contamination decoys from `outputs/`.

## Evaluation Boundary

The evaluation checks whether OCEAN preserves evidence boundaries when reviewing claims. It does **not** prove or disprove the scientific correctness of the source articles.

The key pass condition is behavioral:

- state what was inspected and not inspected;
- refuse or downgrade unsupported claims;
- avoid invented data, sample sizes, metrics, validations, reviewer comments, author roles, or clinical conclusions;
- separate model prediction, association, database evidence, text-mining evidence, mechanism, causality, and clinical utility.

For the full internal validation log, see `skills/ocean/evals/release-validation-log.md`.
