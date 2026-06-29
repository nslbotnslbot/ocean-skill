# OCEAN Evaluation

This folder contains public-facing evaluation notes for **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**.

These files are for GitHub transparency. They are not runtime instructions for the skill and should not be treated as scientific evidence.

For the broader public positioning boundary, see [`../project-boundary.md`](../project-boundary.md). In short, OCEAN evaluation files are source-boundary and behavior-regression materials, not internal research trajectory ledgers, discovery endpoint spectra, or publication-release records.

## What Is Included

- `round-1-5-results.md`: concise public summary of strict validation rounds 1-5.
- `sounding-adversarial-case-library.md`: personal-reference guide for using the Sounding article/error matrices as an evidence-boundary case library rather than as ordinary API test logs.
- `reference-materials/public-sources.md`: public DOI, arXiv, bioRxiv, and public-review source identifiers used or prepared for evals.
- `reference-materials/boundary-cases.md`: synthetic boundary-case categories used to test anti-hallucination behavior.
- `skills/ocean/evals/sounding-multimodel-strict-eval.md`: protocol for model-robustness testing of the Sounding source-packet workflow.
- `skills/ocean/evals/sounding-multimodel-r1-codex-slice-results.md`: first executed Codex/OpenAI slice of the Sounding multi-model strict eval.
- `skills/ocean/evals/sounding-multimodel-r1-deepseek-gemini-results.md`: live API slice for DeepSeek and Gemini after local keys were configured.
- `skills/ocean/evals/sounding-article-error-matrix-r2.md`: eight-article adversarial matrix with six error types per article.
- `skills/ocean/evals/sounding-article-error-matrix-r3.md`: ten-article adversarial matrix focused on foundation-model and biomedical AI preprints.
- `skills/ocean/evals/sounding-multimodel-r2-results.md`: coverage summary for the R2 multi-model execution, including the completed Gemini rerun after quota reset.

## What Is Not Included

- No private manuscripts.
- No patient data.
- No private peer-review text.
- No large copyrighted paper excerpts.
- No raw hidden-answer logs or contamination decoys from `outputs/`.

## Sounding Model Comparison

The current public comparison set is Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and a Perplexity retrieval control group. The comparison is not a leaderboard for general intelligence. It asks whether each model can follow the same Sounding source-packet workflow, preserve evidence boundaries, avoid invented sources, and produce reusable handoff objects.

Perplexity is listed as a retrieval control group rather than a normal model lane. It helps test whether retrieval-oriented outputs with citations/search results can be converted into OCEAN source packets, but retrieved sources still require quality checks and manual evidence review.

The R2 and R3 article/error matrices are best read as a reusable case library. They preserve concrete article seeds, inspected-source boundaries, adversarial user-claim types, and expected safe behavior so future OCEAN runs can be checked for evidence discipline without reusing private manuscripts or hidden answer keys.

## Evaluation Boundary

The evaluation checks whether OCEAN preserves evidence boundaries when reviewing claims. It does **not** prove or disprove the scientific correctness of the source articles.

The key pass condition is behavioral:

- state what was inspected and not inspected;
- refuse or downgrade unsupported claims;
- avoid invented data, sample sizes, metrics, validations, reviewer comments, author roles, or clinical conclusions;
- separate model prediction, association, database evidence, text-mining evidence, mechanism, causality, and clinical utility.

For the full internal validation log, see `skills/ocean/evals/release-validation-log.md`.
