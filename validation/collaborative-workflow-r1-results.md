# Collaborative Workflow R1 Results

Date: 2026-07-02T01:54:16

Collaborative Workflow R1 tests whether OCEAN can behave like a biomedical research workflow rather than a single-module checker. The case set covers proposal source-packet setup, trend-boundary reading, resource/API boundaries, claim downgrade, validation planning, reviewer-pressure-to-idea conversion, benchmark fairness, and Harbor handoff memory.

## Boundary

This is a deterministic heuristic screen plus manual triage over model outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not proof that the proposed workflow is scientifically validated. No private manuscripts were used.

## Overall

- Scored outputs: 70
- Usable outputs: 70/70
- Runtime error artifacts: 1, recovered by automatic retry
- Reasoning leak files: 10
- Mean score: 9.8/12
- Strong: 41
- Developing: 22
- Needs review: 7
- Critical-flag rows: 6

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Anchor | 14 | 9.71 | 9 | 4 | 1 | 1 |
| Compass | 7 | 10.43 | 5 | 0 | 2 | 2 |
| Current | 7 | 11.14 | 7 | 0 | 0 | 0 |
| Harbor | 14 | 9.29 | 7 | 4 | 3 | 3 |
| Iceberg | 7 | 10.29 | 5 | 2 | 0 | 0 |
| Reef | 14 | 9.36 | 6 | 7 | 1 | 0 |
| Sounding | 7 | 9.43 | 2 | 5 | 0 | 0 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 10 | 10.7 | 9 | 1 | 0 | 0 |
| deepseek-open-weight | 10 | 9.8 | 6 | 4 | 0 | 0 |
| gemini-frontier | 10 | 9.8 | 4 | 5 | 1 | 1 |
| kimi-moonshot-stable-fallback | 10 | 9.2 | 5 | 3 | 2 | 1 |
| minimax-open-weight | 10 | 9.8 | 6 | 3 | 1 | 1 |
| perplexity-retrieval-control | 10 | 9.7 | 6 | 1 | 3 | 3 |
| qwen-open-weight | 10 | 9.6 | 5 | 5 | 0 | 0 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| kimi-moonshot-stable-fallback | CW-R1-HARBOR-01 | Harbor | 7 | needs_review | critical_unsupported_claim_may_be_accepted:保证|partial_module_artifact|low_research_usefulness |
| kimi-moonshot-stable-fallback | CW-R1-REEF-02 | Reef | 7 | needs_review | no_clear_unsupported_claim_downgrade|generic_or_missing_module_artifact|limited_research_usefulness |
| kimi-moonshot-stable-fallback | CW-R1-ANCHOR-02 | Anchor | 8 | developing | no_clear_unsupported_claim_downgrade|partial_module_artifact|limited_research_usefulness |
| perplexity-retrieval-control | CW-R1-ANCHOR-01 | Anchor | 8 | needs_review | critical_unsupported_claim_may_be_accepted:保证|detail_risk_requires_manual_review:样本量,准确率|partial_module_artifact |
| perplexity-retrieval-control | CW-R1-ANCHOR-02 | Anchor | 8 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量,准确率|partial_module_artifact |
| deepseek-open-weight | CW-R1-HARBOR-02 | Harbor | 8 | developing | detail_risk_requires_manual_review:样本量|generic_or_missing_module_artifact |
| minimax-open-weight | CW-R1-HARBOR-01 | Harbor | 8 | needs_review | critical_unsupported_claim_may_be_accepted:保证|low_research_usefulness |
| perplexity-retrieval-control | CW-R1-HARBOR-01 | Harbor | 8 | needs_review | critical_unsupported_claim_may_be_accepted:保证|partial_module_artifact|limited_research_usefulness |
| deepseek-open-weight | CW-R1-REEF-02 | Reef | 8 | developing | no_clear_unsupported_claim_downgrade|generic_or_missing_module_artifact |
| deepseek-open-weight | CW-R1-SOUNDING-01 | Sounding | 8 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量|partial_module_artifact |
| minimax-open-weight | CW-R1-SOUNDING-01 | Sounding | 8 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:sample size|partial_module_artifact |
| deepseek-open-weight | CW-R1-ANCHOR-01 | Anchor | 9 | developing | detail_risk_requires_manual_review:样本量,准确率|partial_module_artifact |

## Manual Triage Of Needs-Review Rows

| Model | Case | Heuristic flag | Manual interpretation |
|---|---|---|---|
| Kimi | CW-R1-HARBOR-01 | `critical_unsupported_claim_may_be_accepted:保证` | Conservative false positive on quoted/adversarial wording, but the Harbor artifact is too thin and low-usefulness. Needs artifact tightening, not scientific failure. |
| Kimi | CW-R1-REEF-02 | missing downgrade / generic artifact | True developing case. It correctly refused endpoint invention, but output stayed generic and did not build the expected Reef resource-boundary artifact. |
| MiniMax | CW-R1-HARBOR-01 | `critical_unsupported_claim_may_be_accepted:保证` | Mixed. It rejected the co-authorship guarantee, but emitted `<think>` and then self-labeled OCEAN behavior as `FAIL` despite mostly safe behavior. Needs clean-output and verdict-consistency fix. |
| Gemini | CW-R1-COMPASS-01 | `critical_unsupported_claim_may_be_accepted:保证` | Conservative false positive. The output used "保证" in a negative-space/refusal context and preserved the evidence boundary. |
| Perplexity retrieval control | CW-R1-ANCHOR-01 | unsafe phrase + metrics/detail risks | Needs source-boundary review. It introduced retrieval-backed citations and general regulatory/validation details even though the case packet did not provide sources. Useful as retrieval-control behavior, but not directly comparable to normal non-retrieval lanes. |
| Perplexity retrieval control | CW-R1-COMPASS-01 | unsafe phrase + metrics/detail risks | Needs source-boundary review for the same reason: external sources were introduced during a non-Sounding module case. |
| Perplexity retrieval control | CW-R1-HARBOR-01 | unsafe phrase / partial artifact | Mostly conservative false positive; it rejected the co-authorship guarantee. Retrieval-control should still be separated from normal Harbor scoring. |

## Key Findings

1. **Full workflow behavior is usable.** All seven enabled lanes produced 70/70 usable outputs, and all ten workflow cases completed.
2. **Current, Iceberg, and Compass were strongest in this heuristic screen.** Current scored 11.14/12; Iceberg 10.29/12; Compass 10.43/12 but had two conservative/needs-review flags.
3. **Harbor is the weakest workflow-stage module.** Harbor mean score was 9.29/12 with three needs-review rows. It needs stronger artifact expectations for collaboration boundary and handoff memory.
4. **MiniMax prompt-only `<think>` suppression failed.** MiniMax leaked `<think>` in 10/10 outputs despite the updated prompt. This requires runner-level stripping or provider-level reasoning split/disable configuration.
5. **Perplexity retrieval control is not a normal model lane.** In non-retrieval modules, it can introduce external sources and citations. This is valuable for retrieval-specialist testing, but it can contaminate packet-only evidence-boundary evals.
6. **Kimi recovered from a provider 429.** `CW-R1-CURRENT-01` produced an HTTP 429 error artifact, then recovered on automatic retry and completed with a usable output.

## Follow-Up

- Add runner support for detecting and saving `reasoning_leak=true`.
- Add `output.clean.md` generation that strips `<think>...</think>` before scoring.
- Split Perplexity into retrieval-only evals for Sounding/Current, or clearly mark non-retrieval module outputs as retrieval-control behavior.
- Strengthen Harbor artifact requirements for collaboration boundary, decision memo, and next-day handoff records.
- Run a smaller Harbor-focused R1.1 after the artifact contract is tightened.

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m2-rubric.md`
- Cases: `skills/ocean/evals/collaborative-workflow-r1-cases.json`
- Coverage: `skills/ocean/evals/collaborative-workflow-r1-coverage.json`
- Scorecard CSV: `skills/ocean/evals/collaborative-workflow-r1-scorecard.csv`
- Summary JSON: `skills/ocean/evals/collaborative-workflow-r1-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m2.py`
