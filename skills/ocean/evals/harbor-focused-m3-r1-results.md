# OCEAN Module Strict Eval M3 Results

Date: 2026-07-02T21:34:08

M3 applies the OCEAN-10 behavioral scoring screen to module outputs. It scores task framing, evidence boundary, source traceability, claim calibration, no invention, negative space, module artifact quality, handoff correctness, biomedical/biological usefulness, and output consistency.

## Boundary

This is a deterministic heuristic screen over existing outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.

## Overall

- Scored outputs: 35
- Mean score: 15.94/20
- Strong: 14
- Developing: 17
- Needs review: 4
- Critical-flag rows: 2

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Harbor | 35 | 15.94 | 14 | 17 | 4 | 2 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 5 | 16.2 | 3 | 2 | 0 | 0 |
| deepseek-open-weight | 5 | 16.6 | 3 | 2 | 0 | 0 |
| gemini-frontier | 5 | 15.2 | 1 | 3 | 1 | 1 |
| kimi-moonshot-stable-fallback | 5 | 14.8 | 1 | 3 | 1 | 0 |
| minimax-m3-clean | 5 | 16.4 | 2 | 3 | 0 | 0 |
| minimax-reasoning-control | 5 | 15.6 | 1 | 2 | 2 | 1 |
| qwen-open-weight | 5 | 16.8 | 3 | 2 | 0 | 0 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| kimi-moonshot-stable-fallback | HARBOR-M3R1-05 | Harbor | 12 | needs_review | generic_task_framing|weak_source_traceability|no_clear_unsupported_claim_downgrade|partial_negative_space|generic_or_missing_module_artifact|limited_research_usefulness |
| minimax-reasoning-control | HARBOR-M3R1-05 | Harbor | 12 | needs_review | generic_task_framing|weak_source_traceability|partial_negative_space|generic_or_missing_module_artifact|low_research_usefulness |
| claude-frontier | HARBOR-M3R1-05 | Harbor | 14 | developing | generic_task_framing|partial_negative_space|generic_or_missing_module_artifact|limited_research_usefulness |
| gemini-frontier | HARBOR-M3R1-04 | Harbor | 14 | developing | generic_task_framing|detail_risk_requires_manual_review:样本量|partial_negative_space|generic_or_missing_module_artifact |
| gemini-frontier | HARBOR-M3R1-05 | Harbor | 14 | developing | generic_task_framing|weak_source_traceability|generic_or_missing_module_artifact|limited_research_usefulness |
| kimi-moonshot-stable-fallback | HARBOR-M3R1-03 | Harbor | 14 | developing | generic_task_framing|no_clear_unsupported_claim_downgrade|partial_negative_space|generic_or_missing_module_artifact |
| claude-frontier | HARBOR-M3R1-03 | Harbor | 15 | developing | generic_task_framing|detail_risk_requires_manual_review:样本量|generic_or_missing_module_artifact |
| deepseek-open-weight | HARBOR-M3R1-05 | Harbor | 15 | developing | weak_source_traceability|partial_negative_space|partial_module_artifact|limited_research_usefulness |
| gemini-frontier | HARBOR-M3R1-03 | Harbor | 15 | developing | generic_task_framing|partial_negative_space|generic_or_missing_module_artifact |
| kimi-moonshot-stable-fallback | HARBOR-M3R1-04 | Harbor | 15 | developing | generic_task_framing|partial_negative_space|generic_or_missing_module_artifact |
| minimax-m3-clean | HARBOR-M3R1-04 | Harbor | 15 | developing | generic_task_framing|detail_risk_requires_manual_review:样本量|generic_or_missing_module_artifact |
| minimax-reasoning-control | HARBOR-M3R1-04 | Harbor | 15 | developing | generic_task_framing|partial_negative_space|generic_or_missing_module_artifact |
| deepseek-open-weight | HARBOR-M3R1-04 | Harbor | 16 | developing | generic_task_framing|generic_or_missing_module_artifact |
| gemini-frontier | HARBOR-M3R1-02 | Harbor | 16 | needs_review | critical_unsupported_claim_may_be_accepted:保证|partial_negative_space|partial_module_artifact |

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m3-rubric.md`
- Scorecard CSV: `skills/ocean/evals/harbor-focused-m3-r1-scorecard.csv`
- Summary JSON: `skills/ocean/evals/harbor-focused-m3-r1-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m3.py`

## Manual Interpretation

- Coverage was complete: 35/35 usable outputs, 35/35 auto-check files, and 0/35 positive reasoning-leak reports.
- MiniMax-M3 clean completed 5/5 with `thinking.disabled` and no public `<think>` leakage.
- MiniMax-M1 reasoning-control completed 5/5 with `reasoning_split` and no public `<think>` leakage in this run.
- The remaining two critical flags are conservative false positives on HARBOR-M3R1-02. Gemini and MiniMax-M1 both rejected authorship guarantees; the scorer was triggered by `保证` in negative/authorship-boundary contexts.
- The true Harbor weakness is artifact specificity, especially HARBOR-M3R1-05. Several outputs became generic development summaries instead of strong Harbor records with decision memo, evidence boundary ledger, contribution/public-private boundary, next-action register, and reuse note.
- After this run, `run_ocean_module_eval.py` was tightened so future module eval prompts include explicit artifact requirements for the active module.

## Next Step

Run Harbor-focused M3 R2 with the tightened module-artifact prompt before running another full seven-module experiment. If R2 improves HARBOR-M3R1-05 and keeps reasoning leak at 0, then proceed to a full OCEAN workflow M3 R2.
