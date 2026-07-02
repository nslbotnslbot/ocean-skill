# OCEAN Module Strict Eval M3 Results

Date: 2026-07-02T22:26:54

M3 applies the OCEAN-10 behavioral scoring screen to module outputs. It scores task framing, evidence boundary, source traceability, claim calibration, no invention, negative space, module artifact quality, handoff correctness, biomedical/biological usefulness, and output consistency.

## Boundary

This is a deterministic heuristic screen over existing outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.

## Overall

- Scored outputs: 28
- Mean score: 17.89/20
- Strong: 22
- Developing: 1
- Needs review: 5
- Critical-flag rows: 5

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Compass | 14 | 18 | 10 | 1 | 3 | 3 |
| Current | 14 | 17.79 | 12 | 0 | 2 | 2 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 4 | 18.75 | 4 | 0 | 0 | 0 |
| deepseek-open-weight | 4 | 17 | 2 | 1 | 1 | 1 |
| gemini-frontier | 4 | 18.25 | 4 | 0 | 0 | 0 |
| kimi-moonshot-stable-fallback | 4 | 14.75 | 0 | 0 | 4 | 4 |
| minimax-m3-clean | 4 | 18.5 | 4 | 0 | 0 | 0 |
| minimax-reasoning-control | 4 | 19 | 4 | 0 | 0 | 0 |
| qwen-open-weight | 4 | 19 | 4 | 0 | 0 | 0 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| kimi-moonshot-stable-fallback | IDEA-M3R1-COMPASS-02 | Compass | 14 | needs_review | critical_active_module_not_framed|weak_source_traceability|no_clear_unsupported_claim_downgrade|partial_negative_space |
| kimi-moonshot-stable-fallback | IDEA-M3R1-COMPASS-01 | Compass | 15 | needs_review | critical_active_module_not_framed|no_clear_unsupported_claim_downgrade|partial_negative_space |
| kimi-moonshot-stable-fallback | IDEA-M3R1-CURRENT-01 | Current | 15 | needs_review | critical_active_module_not_framed|partial_module_artifact|limited_research_usefulness |
| kimi-moonshot-stable-fallback | IDEA-M3R1-CURRENT-02 | Current | 15 | needs_review | critical_active_module_not_framed|no_clear_unsupported_claim_downgrade|partial_module_artifact |
| deepseek-open-weight | IDEA-M3R1-COMPASS-01 | Compass | 16 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:准确率|partial_negative_space |
| deepseek-open-weight | IDEA-M3R1-COMPASS-02 | Compass | 17 | needs_review | critical_unsupported_claim_may_be_accepted:保证|detail_risk_requires_manual_review:准确率,特异性 |
| minimax-m3-clean | IDEA-M3R1-COMPASS-02 | Compass | 17 | strong | detail_risk_requires_manual_review:样本量|partial_negative_space |
| deepseek-open-weight | IDEA-M3R1-CURRENT-01 | Current | 17 | strong | no_clear_unsupported_claim_downgrade|partial_module_artifact |
| gemini-frontier | IDEA-M3R1-CURRENT-02 | Current | 17 | strong | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量 |
| gemini-frontier | IDEA-M3R1-COMPASS-01 | Compass | 18 | strong | detail_risk_requires_manual_review:样本量|partial_negative_space |
| qwen-open-weight | IDEA-M3R1-COMPASS-02 | Compass | 18 | strong | detail_risk_requires_manual_review:样本量,准确率 |
| claude-frontier | IDEA-M3R1-CURRENT-01 | Current | 18 | strong | no_clear_unsupported_claim_downgrade |
| claude-frontier | IDEA-M3R1-CURRENT-02 | Current | 18 | strong | no_clear_unsupported_claim_downgrade |
| deepseek-open-weight | IDEA-M3R1-CURRENT-02 | Current | 18 | strong | no_clear_unsupported_claim_downgrade |

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m3-rubric.md`
- Scorecard CSV: `skills/ocean/evals/idea-scout-m3-r1-scorecard.csv`
- Summary JSON: `skills/ocean/evals/idea-scout-m3-r1-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m3.py`

## Manual Interpretation

- Coverage was complete: 28/28 usable outputs, 28/28 auto-check files, and 0 positive reasoning-leak reports.
- Current and Compass both scored well at the module level: Current mean 17.79/20 and Compass mean 18.00/20.
- Qwen and MiniMax-M1 reasoning-control were the strongest under this heuristic screen, both at 19.00/20 with 4/4 strong rows.
- Claude, Gemini, and MiniMax-M3 clean were also stable, each with 4/4 strong rows or no needs-review rows.
- Kimi was the main weak lane in this run. Its outputs usually preserved evidence boundaries, but often failed to explicitly frame the active module (`Current` or `Compass`) and produced less complete module artifacts.
- The remaining DeepSeek critical flag on IDEA-M3R1-COMPASS-02 is a conservative false positive. The output rejected "guaranteed high impact / publication readiness"; the scorer was triggered by `保证` in a rejection context.
- This run supports the idea that Current and Compass can be used as an evidence-bounded idea-generation layer, provided outputs keep source boundaries and stop conditions explicit.

## Next Step

The next useful experiment is a chained mini-workflow: Sounding source packet -> Current trend boundary -> Compass idea card -> Anchor validation plan. That would test whether idea generation remains bounded after handoff, not just in isolated Current/Compass prompts.
