# OCEAN Module Strict Eval M3 Results

Date: 2026-07-02T15:49:40

M3 applies the OCEAN-10 behavioral scoring screen to module outputs. It scores task framing, evidence boundary, source traceability, claim calibration, no invention, negative space, module artifact quality, handoff correctness, biomedical/biological usefulness, and output consistency.

## Boundary

This is a deterministic heuristic screen over existing outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.

## Overall

- Scored outputs: 98
- Mean score: 16.19/20
- Strong: 37
- Developing: 30
- Needs review: 31
- Critical-flag rows: 31

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Anchor | 14 | 16.43 | 6 | 2 | 6 | 6 |
| Compass | 14 | 16.79 | 6 | 5 | 3 | 3 |
| Current | 14 | 16.29 | 5 | 5 | 4 | 4 |
| Harbor | 14 | 16 | 5 | 4 | 5 | 5 |
| Iceberg | 14 | 16.07 | 5 | 5 | 4 | 4 |
| Reef | 14 | 16.29 | 6 | 6 | 2 | 2 |
| Sounding | 14 | 15.5 | 4 | 3 | 7 | 7 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 14 | 17.36 | 11 | 1 | 2 | 2 |
| deepseek-open-weight | 14 | 16.21 | 6 | 7 | 1 | 1 |
| gemini-frontier | 14 | 15.79 | 3 | 9 | 2 | 2 |
| kimi-moonshot-stable-fallback | 14 | 14.29 | 1 | 5 | 8 | 8 |
| minimax-open-weight | 14 | 15.86 | 0 | 0 | 14 | 14 |
| perplexity-retrieval-control | 14 | 16.86 | 8 | 3 | 3 | 3 |
| qwen-open-weight | 14 | 17 | 8 | 5 | 1 | 1 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| kimi-moonshot-stable-fallback | M1-ANCHOR-02 | Anchor | 12 | needs_review | critical_active_module_not_framed|weak_source_traceability|no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:AUPRC|active_module_not_mentioned |
| kimi-moonshot-stable-fallback | M1-CURRENT-01 | Current | 13 | needs_review | critical_active_module_not_framed|no_clear_unsupported_claim_downgrade|partial_negative_space|active_module_not_mentioned |
| kimi-moonshot-stable-fallback | M1-HARBOR-02 | Harbor | 13 | developing | generic_task_framing|weak_source_traceability|no_clear_unsupported_claim_downgrade|partial_negative_space|generic_or_missing_module_artifact |
| gemini-frontier | M1-SOUNDING-02 | Sounding | 13 | developing | generic_task_framing|no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量|partial_negative_space|generic_or_missing_module_artifact |
| kimi-moonshot-stable-fallback | M1-SOUNDING-02 | Sounding | 13 | developing | generic_task_framing|no_clear_unsupported_claim_downgrade|partial_negative_space|generic_or_missing_module_artifact|limited_research_usefulness |
| minimax-open-weight | M1-ANCHOR-02 | Anchor | 14 | needs_review | generic_task_framing|no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:AUROC,AUPRC,样本量,特异性,外部验证结果|critical_reasoning_leak_public_output |
| perplexity-retrieval-control | M1-ANCHOR-02 | Anchor | 14 | needs_review | generic_task_framing|critical_unsupported_claim_may_be_accepted:保证|detail_risk_requires_manual_review:AUROC,AUPRC,样本量|partial_module_artifact|partial_output_consistency |
| kimi-moonshot-stable-fallback | M1-CURRENT-02 | Current | 14 | needs_review | critical_active_module_not_framed|no_clear_unsupported_claim_downgrade|active_module_not_mentioned |
| gemini-frontier | M1-HARBOR-02 | Harbor | 14 | needs_review | generic_task_framing|critical_unsupported_claim_may_be_accepted:保证|detail_risk_requires_manual_review:样本量|partial_negative_space|partial_module_artifact |
| gemini-frontier | M1-ICEBERG-02 | Iceberg | 14 | developing | generic_task_framing|no_clear_unsupported_claim_downgrade|partial_negative_space|generic_or_missing_module_artifact |
| kimi-moonshot-stable-fallback | M1-ICEBERG-02 | Iceberg | 14 | needs_review | critical_active_module_not_framed|no_clear_unsupported_claim_downgrade|active_module_not_mentioned |
| kimi-moonshot-stable-fallback | M1-REEF-01 | Reef | 14 | developing | generic_task_framing|no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:队列大小|partial_negative_space|partial_module_artifact |
| deepseek-open-weight | M1-SOUNDING-02 | Sounding | 14 | developing | generic_task_framing|no_clear_unsupported_claim_downgrade|partial_negative_space|generic_or_missing_module_artifact |
| kimi-moonshot-stable-fallback | M1-ANCHOR-01 | Anchor | 15 | needs_review | critical_active_module_not_framed|active_module_not_mentioned |

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m3-rubric.md`
- Scorecard CSV: `skills/ocean/evals/ocean-module-m3-scorecard.csv`
- Summary JSON: `skills/ocean/evals/ocean-module-m3-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m3.py`
