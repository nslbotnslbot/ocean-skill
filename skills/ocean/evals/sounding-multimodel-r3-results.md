# Sounding Multi-Model Strict Eval R3 Results

Date: 2026-06-30

This run uses ten new public, traceable article/preprint seeds. Each article receives six adversarial error types. The adversarial claims are synthetic test inputs and are not claims made by source authors.

## Scope

- Articles: 10
- Error types per article: 6
- Total cases per model: 60
- Gemini was tested first as requested, but the first R3 Gemini attempt returned HTTP 429 and was stopped. The non-Gemini model set was then run on the same R3 matrix.

## Article Seeds

| ID | Title | URL |
|---|---|---|
| R3A01 | DinoBloom: A Foundation Model for Generalizable Cell Embeddings in Hematology | https://arxiv.org/abs/2404.05022 |
| R3A02 | scDrugMap: Benchmarking Large Foundation Models for Drug Response Prediction | https://arxiv.org/abs/2505.05612 |
| R3A03 | Nephrobase Cell+: Multimodal Single-Cell Foundation Model for Decoding Kidney Biology | https://arxiv.org/abs/2509.26223 |
| R3A04 | Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models | https://arxiv.org/abs/2604.14838 |
| R3A05 | UBio-MolFM: A Universal Molecular Foundation Model for Bio-Systems | https://arxiv.org/abs/2602.17709 |
| R3A06 | MultiPUFFIN: A Multimodal Domain-Constrained Foundation Model for Molecular Property Prediction of Small Molecules | https://arxiv.org/abs/2603.00857 |
| R3A07 | BioMatrix: Towards a Comprehensive Biological Foundation Model Spanning the Modality Matrix of Sequences, Structures, and Language | https://arxiv.org/abs/2606.22138 |
| R3A08 | Multi-view biomedical foundation models for molecule-target and property prediction | https://arxiv.org/abs/2410.19704 |
| R3A09 | ChemFM as a Scaling Law Guided Foundation Model Pre-trained on Informative Chemicals | https://arxiv.org/abs/2410.21422 |
| R3A10 | Tabular foundation models for in-context prediction of molecular properties | https://arxiv.org/abs/2604.16123 |

## Coverage Summary

| Model | Lane | Usable outputs | Coverage | Auto-check files | Source packets | Notes |
|---|---|---:|---:|---:|---:|---|
| Qwen qwen3.7-max | open-weight reproducibility | 60/60 | 100.0% | 60 | 0 | 57/60 main run plus 3 successful timeout reruns. |
| DeepSeek deepseek-v4-pro | open-weight reproducibility | 60/60 | 100.0% | 60 | 0 | 60/60 main run. |
| Kimi moonshot-v1-128k fallback | open-weight reproducibility | 60/60 | 100.0% | 60 | 0 | 54/60 main run plus 6 successful connection-reset/timeout reruns. |
| MiniMax MiniMax-M1 | open-weight reproducibility | 60/60 | 100.0% | 60 | 0 | 60/60 main run. |
| Claude claude-opus-4-8 | frontier ceiling | 60/60 | 100.0% | 60 | 0 | 60/60 main run. |
| Perplexity retrieval control sonar-pro | retrieval control | 60/60 | 100.0% | 60 | 60 | 60/60 main run; source_packet.json saved for all cases. |
| Gemini gemini-2.5-flash | frontier ceiling | 0/60 | 0.0% | 0 | 0 | 0/60 for R3; initial Gemini-first attempt returned HTTP 429 RESOURCE_EXHAUSTED because prepayment credits are depleted; stopped to avoid wasting requests. |

## Interpretation

Coverage means the model/API produced a usable raw Sounding output for that case. It does not by itself prove content-level scientific correctness. Manual or programmatic content scoring should be run on the saved artifacts before claiming model-quality rankings.

## Output Artifact Roots

- Qwen qwen3.7-max: outputs/sounding-article-error-matrix-r3-full-qwen/20260630-001150/qwen-open-weight; outputs/sounding-article-error-matrix-r3-rerun-qwen/20260630-012513/qwen-open-weight
- DeepSeek deepseek-v4-pro: outputs/sounding-article-error-matrix-r3-full-deepseek/20260630-001150/deepseek-open-weight
- Kimi moonshot-v1-128k fallback: outputs/sounding-article-error-matrix-r3-full-kimi/20260630-001150/kimi-moonshot-stable-fallback; outputs/sounding-article-error-matrix-r3-rerun-kimi/20260630-012513/kimi-moonshot-stable-fallback
- MiniMax MiniMax-M1: outputs/sounding-article-error-matrix-r3-full-minimax/20260630-001150/minimax-open-weight
- Claude claude-opus-4-8: outputs/sounding-article-error-matrix-r3-full-claude/20260630-001247/claude-frontier
- Perplexity retrieval control sonar-pro: outputs/sounding-article-error-matrix-r3-full-perplexity/20260630-001247/perplexity-retrieval-control
- Gemini gemini-2.5-flash: outputs/sounding-article-error-matrix-r3-gemini-first/20260630-000618/gemini-frontier
