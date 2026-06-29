# Sounding Adversarial Case Library

This note explains which recent Sounding artifacts are worth keeping on GitHub as personal reference material. It intentionally focuses on reusable evaluation design rather than ordinary API connectivity tests.

## Why This Is Valuable

The useful artifact is not that a provider API returned a response. The useful artifact is the case design:

- public, traceable article or preprint seeds;
- explicit inspected-source boundaries;
- synthetic adversarial user claims that are not attributed to the source authors;
- six stable error types that cover common scientific overclaim paths;
- expected safe behavior for refusing, downgrading, or quarantining unsupported claims;
- reusable source-packet style prompts for future OCEAN/Sounding regression checks.

This makes the matrices useful as a personal benchmark library for claim-evidence discipline, manuscript review preparation, and future agent behavior comparisons.

The library should not be framed as an internal research trajectory ledger or a discovery outcome spectrum. Its scope is public-source boundary testing: given a traceable source packet and a synthetic unsafe user claim, does OCEAN preserve the evidence boundary and request the missing evidence?

## Current Matrix Set

| Matrix | Date | Article seeds | Error types | Total cases | Best use |
|---|---:|---:|---:|---:|---|
| `sounding-article-error-matrix-r2` | 2026-06-29 | 8 | 6 | 48 | Broad biomedical/AI-for-science boundary testing across the original article set plus additional public seeds. |
| `sounding-article-error-matrix-r3` | 2026-06-30 | 10 | 6 | 60 | Fresh personal-reference set for foundation-model, biomedical AI, single-cell, molecular, and chemical-property preprint claims. |

## Stable Error Types

| ID | Error type | What OCEAN should protect against |
|---|---|---|
| E01 | `text_missing` | Treating title, abstract, landing page, or source packet as if the full article, figures, supplements, code, and peer-review record had been inspected. |
| E02 | `data_missing` | Treating missing metrics, sample sizes, split design, uncertainty, cohorts, or external validation as already sufficient. |
| E03 | `method_missing` | Assuming no leakage, no circular validation, no confounding, or full reproducibility from high-level model descriptions. |
| E04 | `evidence_type_mismatch` | Upgrading model performance, retrieval, database association, or representation quality into mechanism, causality, therapeutic efficacy, or clinical utility. |
| E05 | `source_not_traceable` | Accepting remembered reviewer comments, unnamed follow-up papers, or uncited claims without a title, DOI, URL, or exact passage. |
| E06 | `logical_contradiction` | Ignoring the stated source boundary and treating the article as proving the strongest downstream claim. |

## R2 Completion Note

The R2 coverage summary now records Gemini `gemini-2.5-flash` as 48/48 usable outputs after the quota window cleared and a Gemini-only rerun completed the remaining cases. This is useful for accounting, but it should not be read as a scientific-performance claim. It only says that usable Sounding outputs were generated for every R2 case.

## R3 Personal-Reference Focus

R3 adds ten new public arXiv source seeds. The set is useful because it targets areas where scientific overclaiming is common:

- foundation models for hematology cell images;
- single-cell foundation models and drug-response prediction;
- kidney-focused multimodal single-cell models;
- layer-wise representation claims in single-cell foundation models;
- molecular and biological foundation models;
- molecule-target and molecular-property prediction;
- chemical foundation models and scaling-law framing;
- tabular foundation models for molecular property prediction.

Each seed is represented with an inspected boundary and a contradiction anchor. Those fields are the core reusable value: they force future outputs to say what was inspected, what was not inspected, and which stronger claims remain unsupported.

## How To Use This Library

Use these matrices when you want to test whether an OCEAN/Sounding run can:

- preserve `inspected / not inspected / cannot conclude / needed next`;
- refuse completeness claims from incomplete source packets;
- request concrete missing evidence instead of inventing it;
- downgrade computational or database evidence to hypothesis-generating support when causal, wet-lab, clinical, or independent validation is missing;
- avoid treating reviewer memory, web snippets, or model output as source evidence;
- produce reusable handoff tickets for Iceberg, Anchor, Reef, or Compass.

Do not use these files as proof that the source articles are correct or incorrect. They are workflow validation materials, not scientific judgments.

## What Not To Publish

Do not publish raw provider responses, API keys, local `.env` files, or full output directories by default. For GitHub, keep only:

- matrix definitions;
- public source identifiers;
- compact coverage summaries;
- evidence-boundary notes;
- reusable prompts or schemas.

Raw output artifacts can stay local unless there is a specific reason to curate and redact them.
