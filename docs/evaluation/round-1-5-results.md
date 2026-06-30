# OCEAN Strict Eval Results: Rounds 1-5

Date: 2026-06-28

This is a public summary of the first five strict validation rounds for **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**. It summarizes behavior-level validation only. It is not a scientific correctness claim about any referenced paper or preprint.

## Summary Table

| Round | Focus | Counted checks | Result |
|---|---|---:|---|
| Round 1 | Source-packet forward eval using AlphaFold and KDGene cases; tested general research evaluation, claim audit, KG/database mechanism caution, reviewer-style stress test, and implicit trigger behavior. | 5 case-level checks | Strict pass |
| Round 2 | Anti-hallucination gate A: text missing, data missing, method missing. | 3 boundary checks | Strict pass |
| Round 3 | Anti-hallucination gate B: evidence-type mismatch, source not traceable, logical contradiction. | 3 boundary checks | Strict pass |
| Round 4 | Real-article adversarial matrix using three public arXiv source packets, each paired with six unsafe user claims. | 18 claim-level checks | Strict pass |
| Round 5 | Contamination-resistance replay plus 10 new public-study source packets; old conclusions existed in ignored `outputs/` but were forbidden to fresh test threads. | 19 claim-level checks | Strict pass |

## Aggregate Result

Across the counted strict rounds, OCEAN passed **48 counted case/claim-level checks**.

Interpretation: OCEAN repeatedly rejected or downgraded unsafe claims when the available evidence did not support mechanism, causality, external validation, clinical deployment, treatment guidance, universal model superiority, or publication-readiness claims.

## Key Behaviors Observed

- OCEAN did not treat abstract-only evidence as full-paper evidence.
- OCEAN did not treat model performance as disease-mechanism proof.
- OCEAN did not treat knowledge graph, database, or text-mining evidence as causal validation.
- OCEAN did not treat benchmark results as clinical decision readiness.
- OCEAN refused to judge source credibility when no traceable source was provided.
- OCEAN explicitly separated inspected, not inspected, cannot conclude, and needed-next evidence.
- OCEAN did not use prior conclusions placed in an ignored contamination-decoy path during Round 5.

## Caveats

- These are workflow and safety checks, not user studies.
- Many source packets were intentionally metadata-only or abstract-only.
- Passing means the skill preserved evidence boundaries; it does not mean the source papers are correct or incorrect.
- The official packaging validator passed in a temporary `PyYAML` environment before publication.

## Internal Log

The detailed internal record is in:

```text
skills/ocean/evals/release-validation-log.md
```


## Later Sounding Multi-Model Evals

After rounds 1-5, OCEAN added module-specific Sounding evals. These are separate from the earlier counted strict rounds.

| Eval | Scope | Model coverage result | Boundary |
|---|---|---|---|
| Sounding R1 API slices | Small live API checks for Codex/OpenAI, DeepSeek, and Gemini behavior | Completed slices recorded in `skills/ocean/evals/` | Workflow/format and evidence-boundary behavior only |
| Sounding R2 | 8 public article/preprint seeds x 6 adversarial error types = 48 cases per model | Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and Perplexity retrieval control completed coverage | Coverage only; not a content-quality leaderboard |
| Sounding R3 | 10 public article/preprint seeds x 6 adversarial error types = 60 cases per model | Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and Perplexity retrieval control completed coverage after Gemini's later rerun | Coverage only; content-level scoring still needed |

Current interpretation: the strongest module-specific evidence is for Sounding. Iceberg behavior has partial indirect support from claim-downgrade and anti-hallucination tests. Current, Reef, Anchor, Compass, and Harbor still need standalone module evals.
