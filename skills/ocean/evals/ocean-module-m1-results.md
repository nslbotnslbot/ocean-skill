# OCEAN Module Strict Eval M1 Results

Date: 2026-06-30 to 2026-07-01 (Asia/Tokyo)

This is the first all-module coverage eval for OCEAN. It tests whether each configured model can produce usable artifacts for all seven modules while preserving evidence boundaries. It does not claim final content-quality ranking or scientific correctness.

## Scope

- Modules: Sounding, Current, Reef, Iceberg, Anchor, Compass, Harbor.
- Cases: 14 total, 2 per module.
- Enabled model lanes: 7.
- Expected model-case outputs: 98.
- Source policy: public/source-traceable seeds and explicitly adversarial user requests; adversarial requests are test prompts, not source-author claims.

## Coverage Summary

| Model | Lane | Usable outputs | Auto-check files | Heading pass | Source packets | Notes |
|---|---|---:|---:|---:|---:|---|
| Qwen qwen3.7-max | open-weight reproducibility | 14/14 | 14 | 14 | 0 | 14/14 after targeted rerun. |
| DeepSeek deepseek-v4-pro | open-weight reproducibility | 14/14 | 14 | 14 | 0 | 14/14 after targeted rerun. |
| Kimi moonshot-v1-128k | open-weight reproducibility | 14/14 | 14 | 14 | 0 | 14/14 after targeted rerun. |
| MiniMax MiniMax-M1 | open-weight reproducibility | 14/14 | 14 | 13 | 0 | 14/14 main run. |
| Google Gemini gemini-2.5-flash | frontier ceiling | 14/14 | 14 | 14 | 0 | 14/14 main run. |
| Anthropic Claude claude-opus-4-8 | frontier ceiling | 14/14 | 14 | 14 | 0 | 14/14 main run. |
| Perplexity Retrieval API sonar-pro | retrieval control | 14/14 | 14 | 11 | 14 | 14/14 main run. Source packet saved for all cases. |

## Module Coverage

| Module | Usable outputs | Auto-check files | Heading pass | Source packets |
|---|---:|---:|---:|---:|
| Anchor | 14/14 | 14 | 13 | 2 |
| Compass | 14/14 | 14 | 14 | 2 |
| Current | 14/14 | 14 | 13 | 2 |
| Harbor | 14/14 | 14 | 14 | 2 |
| Iceberg | 14/14 | 14 | 13 | 2 |
| Reef | 14/14 | 14 | 13 | 2 |
| Sounding | 14/14 | 14 | 14 | 2 |

## Run Notes

- Initial full run produced 93/98 usable outputs and 5 provider error artifacts.
- The initial full run used `--timeout 240`; targeted reruns used a longer `--timeout 420`.
- Targeted reruns recovered all 5 missing outputs: Qwen M1-REEF-02 and M1-HARBOR-02; DeepSeek M1-SOUNDING-01; Kimi M1-REEF-01 and M1-COMPASS-02.
- Perplexity retrieval control produced source packets for all 14 cases.
- A pre-full-run Gemini smoke exposed a prompt-boundary issue: the model reconstructed abstract-like text when exact abstract text was not provided. The runner/case wording was tightened before the full run to require `未提供` for absent abstract/method/metric details.

## Error Recovery

| Model | Case | Module | Initial error | Rerun timeout | Result | Interpretation |
|---|---|---|---|---:|---|---|
| Qwen qwen3.7-max | M1-REEF-02 | Reef | `timeout('The read operation timed out')` | 420s | Recovered | Provider/API read timeout; not treated as a module failure. |
| Qwen qwen3.7-max | M1-HARBOR-02 | Harbor | `ConnectionResetError(54, 'Connection reset by peer')` | 420s | Recovered | Remote connection reset; not treated as a module failure. |
| DeepSeek deepseek-v4-pro | M1-SOUNDING-01 | Sounding | `timeout('The read operation timed out')` | 420s | Recovered | Provider/API read timeout; not treated as a module failure. |
| Kimi moonshot-v1-128k | M1-REEF-01 | Reef | `timeout('The read operation timed out')` | 420s | Recovered | Provider/API read timeout; not treated as a module failure. |
| Kimi moonshot-v1-128k | M1-COMPASS-02 | Compass | `timeout('The read operation timed out')` | 420s | Recovered | Provider/API read timeout; not treated as a module failure. |

Detailed recovery table: `skills/ocean/evals/ocean-module-m1-error-recovery.csv`.

## Evidence Boundary

M1 is a coverage and format-stability eval. It checks whether OCEAN can route each module, keep inspected/not-inspected/cannot-conclude/needed-next boundaries, and produce module-specific artifacts. It does not prove that every output is scientifically correct. Manual or programmatic content-level scoring is still required.

## Artifact Roots

- Main run: `outputs/ocean-module-eval-m1-full/20260630-225724`
- Rerun qwen-open-weight: `outputs/ocean-module-eval-m1-rerun-qwen/20260701-000444`
- Rerun deepseek-open-weight: `outputs/ocean-module-eval-m1-rerun-deepseek/20260701-000734`
- Rerun kimi-moonshot-stable-fallback: `outputs/ocean-module-eval-m1-rerun-kimi/20260701-000922`
