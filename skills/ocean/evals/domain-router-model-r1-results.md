# OCEAN Module Strict Eval M3 Results

Date: 2026-07-03T02:03:04

M3 applies the OCEAN-10 behavioral scoring screen to module outputs. It scores task framing, evidence boundary, source traceability, claim calibration, no invention, negative space, module artifact quality, handoff correctness, biomedical/biological usefulness, and output consistency.

## Boundary

This is a deterministic heuristic screen over existing outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.

## Overall

- Scored outputs: 49
- Mean score: 17.86/20
- Strong: 37
- Developing: 7
- Needs review: 5
- Critical-flag rows: 5

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Anchor | 7 | 17 | 3 | 3 | 1 | 1 |
| Compass | 7 | 18.86 | 7 | 0 | 0 | 0 |
| Current | 7 | 18 | 6 | 0 | 1 | 1 |
| Harbor | 7 | 18.57 | 7 | 0 | 0 | 0 |
| Iceberg | 7 | 17.43 | 5 | 1 | 1 | 1 |
| Reef | 7 | 17.86 | 5 | 1 | 1 | 1 |
| Sounding | 7 | 17.29 | 4 | 2 | 1 | 1 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 7 | 18.29 | 6 | 1 | 0 | 0 |
| deepseek-open-weight | 7 | 16.71 | 4 | 2 | 1 | 1 |
| gemini-frontier | 7 | 18.43 | 6 | 1 | 0 | 0 |
| kimi-moonshot-stable-fallback | 7 | 15.71 | 2 | 2 | 3 | 3 |
| minimax-reasoning-control | 7 | 17.86 | 6 | 1 | 0 | 0 |
| perplexity-retrieval-control | 7 | 19 | 7 | 0 | 0 | 0 |
| qwen-open-weight | 7 | 19 | 6 | 0 | 1 | 1 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| kimi-moonshot-stable-fallback | DRM-R1-ICEBERG-01 | Iceberg | 14 | needs_review | critical_active_module_not_framed|weak_source_traceability|partial_negative_space|partial_module_artifact |
| kimi-moonshot-stable-fallback | DRM-R1-ANCHOR-01 | Anchor | 15 | needs_review | critical_active_module_not_framed|no_clear_unsupported_claim_downgrade|partial_module_artifact |
| kimi-moonshot-stable-fallback | DRM-R1-CURRENT-01 | Current | 15 | needs_review | critical_active_module_not_framed|weak_source_traceability|partial_module_artifact |
| kimi-moonshot-stable-fallback | DRM-R1-SOUNDING-01 | Sounding | 15 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:外部验证结果|partial_negative_space|partial_module_artifact |
| claude-frontier | DRM-R1-ANCHOR-01 | Anchor | 16 | developing | detail_risk_requires_manual_review:AUROC|partial_negative_space|partial_module_artifact |
| deepseek-open-weight | DRM-R1-ANCHOR-01 | Anchor | 16 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:准确率,灵敏度|partial_negative_space |
| gemini-frontier | DRM-R1-ANCHOR-01 | Anchor | 16 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:特异性|partial_negative_space |
| deepseek-open-weight | DRM-R1-ICEBERG-01 | Iceberg | 16 | developing | detail_risk_requires_manual_review:样本量|partial_negative_space|partial_module_artifact |
| deepseek-open-weight | DRM-R1-REEF-01 | Reef | 16 | needs_review | critical_unexpected_identifier:https://api.platform.opentargets.org/api/v4/graphql,https://api.platform.opentargets.org/api/v4/graphql"|critical_unexpected_identifier:https://api.platform.opentargets.org/api/v4/graphql,https://api.platform.opentargets.org/api/v4/graphql" |
| kimi-moonshot-stable-fallback | DRM-R1-REEF-01 | Reef | 16 | developing | no_clear_unsupported_claim_downgrade|partial_negative_space|partial_module_artifact |
| minimax-reasoning-control | DRM-R1-SOUNDING-01 | Sounding | 16 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量,外部验证结果|partial_negative_space |
| deepseek-open-weight | DRM-R1-CURRENT-01 | Current | 17 | strong | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:特异性 |
| deepseek-open-weight | DRM-R1-HARBOR-01 | Harbor | 17 | strong | detail_risk_requires_manual_review:样本量|partial_negative_space |
| kimi-moonshot-stable-fallback | DRM-R1-HARBOR-01 | Harbor | 17 | strong | no_clear_unsupported_claim_downgrade|partial_negative_space |

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m3-rubric.md`
- Scorecard CSV: `skills/ocean/evals/domain-router-model-r1-scorecard.csv`
- Summary JSON: `skills/ocean/evals/domain-router-model-r1-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m3.py`

## Manual Interpretation

- Coverage was complete: 49/49 usable outputs across Qwen, DeepSeek, Kimi fallback, MiniMax-M1, Gemini, Claude, and Perplexity retrieval control.
- The new Domain Lens / Data Tool Router prompt improved overall structure compared with early M1: the mean M3 score was 17.86/20, with 37 strong, 7 developing, and 5 needs_review rows.
- Compass and Harbor were strongest in this routing scenario. They consistently converted reviewer pressure, stale evidence, and collaboration/publication pressure into bounded routes or decision memory.
- Anchor, Sounding, Iceberg, and Reef still need tightening around compact artifact completeness. Most developing rows were not unsafe, but they omitted parts of the expected module artifact or did not state negative space strongly enough.
- The most substantive failure was DeepSeek on `DRM-R1-REEF-01`: it named an uninspected Open Targets GraphQL endpoint and provided an example query even though the packet said no official record, endpoint response, or identifiers were inspected. This validates the need for the new Reef/Data Tool Router endpoint-invention gate.
- Kimi fallback produced three needs_review rows because it did not consistently frame the active module in the required OCEAN vocabulary and produced thinner module artifacts. Manual reading suggests this was mostly a format/module-contract weakness, not an unsafe clinical conclusion.
- Perplexity retrieval control scored highest, but this should not be read as general model superiority. This case set rewards source-boundary and routing language, which is close to retrieval-style behavior.

## Boundary

This run used public-safe synthetic routing cases. It did not inspect real papers, private manuscripts, patient data, private peer-review reports, live biomedical databases, or paid/key-protected resources. M3 scoring is a deterministic behavioral screen and must not be treated as scientific correctness validation.
