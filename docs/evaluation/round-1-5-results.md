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

Current interpretation: the strongest module-specific evidence is for Sounding. OCEAN Module M1 adds first-pass standalone coverage for Current, Reef, Iceberg, Anchor, Compass, and Harbor, but those modules still need content-level scoring before quality comparisons.


## OCEAN Module M1

OCEAN Module Strict Eval M1 is the first all-module coverage eval. It uses 14 cases, 2 per module, across the enabled model lanes. After targeted reruns for provider timeouts, the merged coverage record reaches 98/98 usable outputs. This validates that all seven modules can produce structured artifacts under a shared evidence-boundary contract, but content-level scoring is still required before claiming module quality rankings.


## OCEAN Module M2

OCEAN Module Strict Eval M2 adds a 12-point heuristic scoring screen over the 98 M1 outputs. The dimensions are evidence boundary correctness, unsupported-claim downgrade, no invented source/details, module-specific artifact quality, handoff correctness, and biomedical/biological research usefulness.

M2 scored 98/98 outputs with a mean score of 10.07/12: 64 strong, 23 developing, and 11 needs_review under the deterministic screen. This is a first-pass quality screen and a triage tool for manual review, not final scientific correctness validation or a model leaderboard.


## OCEAN Differentiation M3

After reviewing adjacent AI-for-science workflow framing, OCEAN was re-positioned more explicitly as external biomedical evidence navigation and claim-risk triage. The public guardrail is that OCEAN should not be described as an execution-ledger, release-gate, endpoint-calibration, or proof-object publishing workflow.

M3 scanned 50 public repository files and 98 saved M1 outputs. Result: 0 unqualified high-risk mentions; status pass. This is a positioning/similarity guardrail only, not legal clearance or scientific originality proof.
