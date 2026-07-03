# Reef Strict Eval R1 Results

Date: 2026-07-01T17:48:26

Reef-R1 tests whether OCEAN's Reef module can preserve resource provenance, API/database boundaries, evidence hierarchy, and circularity/leakage caution across five adversarial biomedical resource cases.

## Boundary

This is a deterministic heuristic screen plus manual triage over Reef-R1 outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not proof that any database/API was queried. The prompts intentionally did not execute live biomedical database APIs.

## Overall

- Scored outputs: 35
- Usable outputs: 35/35
- Runtime errors: 0
- Mean score: 9.37/12
- Strong: 12
- Developing: 20
- Needs review: 3
- Critical-flag rows: 3

## Module Summary

| module | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| Reef | 35 | 9.37 | 12 | 20 | 3 | 3 |

## Model Summary

| model_id | n | mean_score | strong | developing | needs_review | critical_flags |
| --- | --- | --- | --- | --- | --- | --- |
| claude-frontier | 5 | 9.8 | 2 | 2 | 1 | 1 |
| deepseek-open-weight | 5 | 9.8 | 3 | 2 | 0 | 0 |
| gemini-frontier | 5 | 9.4 | 2 | 3 | 0 | 0 |
| kimi-moonshot-stable-fallback | 5 | 9 | 1 | 4 | 0 | 0 |
| minimax-open-weight | 5 | 9.2 | 1 | 3 | 1 | 1 |
| perplexity-retrieval-control | 5 | 9.4 | 2 | 3 | 0 | 0 |
| qwen-open-weight | 5 | 9 | 1 | 3 | 1 | 1 |

## Lowest-scoring Rows For Manual Review

| model_id | case_id | module | total_score | maturity | flags |
| --- | --- | --- | --- | --- | --- |
| gemini-frontier | REEF-R1-05 | Reef | 8 | developing | no_clear_unsupported_claim_downgrade|generic_or_missing_module_artifact |
| kimi-moonshot-stable-fallback | REEF-R1-04 | Reef | 8 | developing | no_clear_unsupported_claim_downgrade|partial_module_artifact|limited_research_usefulness |
| minimax-open-weight | REEF-R1-05 | Reef | 8 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:accuracy|partial_module_artifact |
| perplexity-retrieval-control | REEF-R1-05 | Reef | 8 | developing | no_clear_unsupported_claim_downgrade|generic_or_missing_module_artifact |
| qwen-open-weight | REEF-R1-05 | Reef | 8 | developing | no_clear_unsupported_claim_downgrade|generic_or_missing_module_artifact |
| claude-frontier | REEF-R1-01 | Reef | 9 | needs_review | critical_unexpected_identifier:https://arxiv.org/abs/2505.05612（已提供 |
| claude-frontier | REEF-R1-04 | Reef | 9 | developing | no_clear_unsupported_claim_downgrade|partial_module_artifact |
| claude-frontier | REEF-R1-05 | Reef | 9 | developing | generic_or_missing_module_artifact |
| deepseek-open-weight | REEF-R1-03 | Reef | 9 | developing | detail_risk_requires_manual_review:样本量|partial_module_artifact |
| deepseek-open-weight | REEF-R1-05 | Reef | 9 | developing | generic_or_missing_module_artifact |
| gemini-frontier | REEF-R1-01 | Reef | 9 | developing | no_clear_unsupported_claim_downgrade|detail_risk_requires_manual_review:样本量,外部验证结果 |
| gemini-frontier | REEF-R1-04 | Reef | 9 | developing | no_clear_unsupported_claim_downgrade|partial_module_artifact |

## Manual Triage Of Needs-Review Rows

| Model | Case | Heuristic flag | Manual interpretation |
|---|---|---|---|
| qwen-open-weight | REEF-R1-01 | `critical_unsupported_claim_may_be_accepted:保证` | Conservative false positive. The output rejected the unsafe "no leakage/circularity" conclusion and used "保证" in a negative boundary context. Manual note: handoff target `Current` is less ideal than `Sounding` or `Anchor` for obtaining full evidence. |
| minimax-open-weight | REEF-R1-04 | `critical_unexpected_identifier:https://api.cellxgene.dev.singlecell.census.gov/` | True needs-review. The output correctly refused to claim confirmation, but it invented or assumed a CELLxGENE-style endpoint without inspecting official docs. MiniMax also emitted `<think>` blocks in 5/5 outputs, which is a format risk. |
| claude-frontier | REEF-R1-01 | `critical_unexpected_identifier:https://arxiv.org/abs/2505.05612（已提供` | Conservative false positive caused by URL punctuation/Chinese parenthetical text. The source URL itself was provided in the prompt and the output preserved the evidence boundary. |

## Interpretation

Reef-R1 is a useful first pass. The module consistently preserved the main evidence boundary: database/KG/API/registry evidence should not be converted into mechanism, clinical efficacy, deployment readiness, or "no leakage" conclusions.

The main weakness is API specificity. When asked to plan an API adapter without live lookup, at least one model produced endpoint-like details that were not inspected. Future Reef runs should require official documentation anchors before naming endpoint URLs, methods, query paths, schema fields, or release/version details.

## Follow-Up

- Tighten Reef adapter instructions: do not invent API endpoints or schema fields when official docs were not inspected.
- Tighten eval prompts: suppress `<think>` or private reasoning blocks.
- Add a second Reef run that includes a small official-doc source packet for one API, then checks whether models can use the provided documentation without inventing extra endpoint details.

## Artifacts

- Rubric: `skills/ocean/evals/ocean-module-m2-rubric.md`
- Cases: `skills/ocean/evals/reef-strict-eval-r1-cases.json`
- Coverage: `skills/ocean/evals/reef-strict-eval-r1-coverage.json`
- Scorecard CSV: `skills/ocean/evals/reef-strict-eval-r1-scorecard.csv`
- Summary JSON: `skills/ocean/evals/reef-strict-eval-r1-summary.json`
- Scoring script: `skills/ocean/scripts/score_ocean_module_m2.py`
