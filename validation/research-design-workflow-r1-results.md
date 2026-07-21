# Research Design Workflow R1 Results

Date: 2026-07-03T00:34:01

M3 applies the OCEAN-10 behavioral scoring screen to module outputs. It scores task framing, evidence boundary, source traceability, claim calibration, no invention, negative space, module artifact quality, handoff correctness, biomedical/biological usefulness, and output consistency.

## Boundary

This is a deterministic heuristic screen over existing outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.

## Overall

- Scored outputs: 42
- Mean score: 18.38/20
- Strong: 42
- Developing: 0
- Needs review: 0
- Critical-flag rows: 0
- Runtime-blocked model lanes: 1 (`kimi-moonshot-stable-fallback`)
- Positive reasoning-leak reports: 0

## Runtime Boundary

The initial full run completed Qwen and DeepSeek, then stalled on the first Kimi request. That run was manually interrupted to avoid one provider blocking the experiment. A follow-up run completed MiniMax, Gemini, Claude, and Perplexity across all seven cases.

Kimi is recorded as runtime blocked for this R1, not as a content-quality failure. It should be retried separately with a shorter timeout or provider-specific settings before comparing content quality.

## Interpretation

Research Design Workflow R1 passed as a scaffold-to-behavior test. Across 42 scored outputs, models generally preserved the core process shape: source boundary first, resource routing without proof inflation, claim calibration before validation, staged research route selection, and Harbor-style decision memory.

The strongest module means were Current and Iceberg, suggesting the workflow is good at refusing field-trend and completed-evidence overclaims when input evidence is sparse. Anchor and Reef were still strong but lower, which is useful: those are the modules most likely to become too specific when asked for validation thresholds or database routes.

Manual review of the lowest-scoring rows found mostly conservative scorer flags. Terms such as sample size, accuracy, specificity, sensitivity, and external validation were usually used as future validation criteria, not as invented completed results. The remaining improvement target is to make Anchor avoid arbitrary hard thresholds unless the user supplied domain constraints or the output clearly labels them as illustrative examples.

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Anchor | 6 | 17.5 | 6 | 0 | 0 | 0 |
| Compass | 6 | 18.83 | 6 | 0 | 0 | 0 |
| Current | 6 | 19.17 | 6 | 0 | 0 | 0 |
| Harbor | 6 | 18 | 6 | 0 | 0 | 0 |
| Iceberg | 6 | 19 | 6 | 0 | 0 | 0 |
| Reef | 6 | 17.83 | 6 | 0 | 0 | 0 |
| Sounding | 6 | 18.33 | 6 | 0 | 0 | 0 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 7 | 18.57 | 7 | 0 | 0 | 0 |
| deepseek-open-weight | 7 | 18.43 | 7 | 0 | 0 | 0 |
| gemini-frontier | 7 | 17.71 | 7 | 0 | 0 | 0 |
| minimax-reasoning-control | 7 | 18.57 | 7 | 0 | 0 | 0 |
| perplexity-retrieval-control | 7 | 18.71 | 7 | 0 | 0 | 0 |
| qwen-open-weight | 7 | 18.29 | 7 | 0 | 0 | 0 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| deepseek-open-weight | RDW-R1-ANCHOR-01 | Anchor | 17 | strong | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量,准确率,外部验证结果 |
| gemini-frontier | RDW-R1-ANCHOR-01 | Anchor | 17 | strong | detail_risk_requires_manual_review:准确率|partial_negative_space |
| minimax-reasoning-control | RDW-R1-ANCHOR-01 | Anchor | 17 | strong | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:准确率 |
| perplexity-retrieval-control | RDW-R1-ANCHOR-01 | Anchor | 17 | strong | no_clear_unsupported_claim_downgrade|partial_negative_space |
| qwen-open-weight | RDW-R1-CURRENT-01 | Current | 17 | strong | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量 |
| gemini-frontier | RDW-R1-HARBOR-01 | Harbor | 17 | strong | detail_risk_requires_manual_review:样本量|partial_negative_space |
| deepseek-open-weight | RDW-R1-REEF-01 | Reef | 17 | strong | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量 |
| gemini-frontier | RDW-R1-REEF-01 | Reef | 17 | strong | detail_risk_requires_manual_review:特异性|partial_negative_space |
| gemini-frontier | RDW-R1-SOUNDING-01 | Sounding | 17 | strong | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量 |
| qwen-open-weight | RDW-R1-ANCHOR-01 | Anchor | 18 | strong | no_clear_unsupported_claim_downgrade |
| claude-frontier | RDW-R1-COMPASS-01 | Compass | 18 | strong | detail_risk_requires_manual_review:样本量 |
| gemini-frontier | RDW-R1-COMPASS-01 | Compass | 18 | strong | partial_negative_space |
| perplexity-retrieval-control | RDW-R1-COMPASS-01 | Compass | 18 | strong | detail_risk_requires_manual_review:样本量,准确率,灵敏度|partial_negative_space |
| claude-frontier | RDW-R1-HARBOR-01 | Harbor | 18 | strong | partial_negative_space |

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m3-rubric.md`
- Scorecard CSV: `skills/ocean/evals/research-design-workflow-r1-scorecard.csv`
- Summary JSON: `skills/ocean/evals/research-design-workflow-r1-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m3.py`
