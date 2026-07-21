# OCEAN Module Strict Eval M2 Results

Date: 2026-07-01T00:48:30

M2 applies the first content-quality scoring screen to the M1 all-module outputs. It scores evidence boundary correctness, unsupported-claim downgrade, absence of invented source details, module-specific artifact quality, handoff correctness, and biomedical/biological research usefulness.

## Boundary

This is a deterministic heuristic screen over existing M1 outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.

## Overall

- Scored outputs: 98
- Mean score: 10.07/12
- Strong: 64
- Developing: 23
- Needs review: 11
- Critical-flag rows: 10

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Anchor | 14 | 9.79 | 7 | 4 | 3 | 2 |
| Compass | 14 | 10.5 | 11 | 3 | 0 | 0 |
| Current | 14 | 10.29 | 11 | 3 | 0 | 0 |
| Harbor | 14 | 10.43 | 9 | 2 | 3 | 3 |
| Iceberg | 14 | 9.93 | 10 | 4 | 0 | 0 |
| Reef | 14 | 10 | 10 | 4 | 0 | 0 |
| Sounding | 14 | 9.57 | 6 | 3 | 5 | 5 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 14 | 10.43 | 12 | 0 | 2 | 2 |
| deepseek-open-weight | 14 | 9.79 | 8 | 5 | 1 | 1 |
| gemini-frontier | 14 | 9.71 | 7 | 5 | 2 | 2 |
| kimi-moonshot-stable-fallback | 14 | 8.93 | 4 | 8 | 2 | 1 |
| minimax-open-weight | 14 | 10.86 | 13 | 1 | 0 | 0 |
| perplexity-retrieval-control | 14 | 10.43 | 9 | 2 | 3 | 3 |
| qwen-open-weight | 14 | 10.36 | 11 | 2 | 1 | 1 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| kimi-moonshot-stable-fallback | M1-ANCHOR-02 | Anchor | 7 | needs_review | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:AUPRC|active_module_not_mentioned |
| perplexity-retrieval-control | M1-ANCHOR-02 | Anchor | 8 | needs_review | critical_unsupported_claim_may_be_accepted:保证|detail_risk_requires_manual_review:AUROC,AUPRC,样本量|partial_module_artifact |
| kimi-moonshot-stable-fallback | M1-CURRENT-01 | Current | 8 | developing | no_clear_unsupported_claim_downgrade|active_module_not_mentioned |
| kimi-moonshot-stable-fallback | M1-CURRENT-02 | Current | 8 | developing | no_clear_unsupported_claim_downgrade|active_module_not_mentioned |
| gemini-frontier | M1-HARBOR-02 | Harbor | 8 | needs_review | critical_unsupported_claim_may_be_accepted:保证|detail_risk_requires_manual_review:样本量|partial_module_artifact |
| kimi-moonshot-stable-fallback | M1-HARBOR-02 | Harbor | 8 | developing | no_clear_unsupported_claim_downgrade|generic_or_missing_module_artifact |
| gemini-frontier | M1-ICEBERG-02 | Iceberg | 8 | developing | no_clear_unsupported_claim_downgrade|generic_or_missing_module_artifact |
| kimi-moonshot-stable-fallback | M1-ICEBERG-02 | Iceberg | 8 | developing | no_clear_unsupported_claim_downgrade|active_module_not_mentioned |
| deepseek-open-weight | M1-SOUNDING-01 | Sounding | 8 | needs_review | critical_unsupported_claim_may_be_accepted:直接指导|detail_risk_requires_manual_review:样本量|partial_module_artifact |
| gemini-frontier | M1-SOUNDING-02 | Sounding | 8 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量|partial_module_artifact |
| kimi-moonshot-stable-fallback | M1-SOUNDING-02 | Sounding | 8 | developing | no_clear_unsupported_claim_downgrade|partial_module_artifact|limited_research_usefulness |
| gemini-frontier | M1-ANCHOR-02 | Anchor | 9 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:AUROC,AUPRC |

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m2-rubric.md`
- Scorecard CSV: `skills/ocean/evals/ocean-module-m2-scorecard.csv`
- Summary JSON: `skills/ocean/evals/ocean-module-m2-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m2.py`
