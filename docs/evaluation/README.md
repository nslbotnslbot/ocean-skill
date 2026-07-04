# OCEAN Evaluation

This folder contains public-facing evaluation notes for **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**.

These files are for GitHub transparency. They are not runtime instructions for the skill and should not be treated as scientific evidence.

For the broader public positioning boundary, see [`../project-boundary.md`](../project-boundary.md). In short, OCEAN evaluation files are source-boundary and behavior-regression materials, not internal research trajectory ledgers, discovery endpoint spectra, or publication-release records.

## What Is Included

- `round-1-5-results.md`: concise public summary of strict validation rounds 1-5.
- `sounding-adversarial-case-library.md`: personal-reference guide for using the Sounding article/error matrices as an evidence-boundary case library rather than as ordinary API test logs.
- `reference-materials/public-sources.md`: public DOI, arXiv, bioRxiv, and public-review source identifiers used or prepared for evals.
- `reference-materials/boundary-cases.md`: synthetic boundary-case categories used to test anti-hallucination behavior.
- `skills/ocean/evals/sounding-multimodel-strict-eval.md`: protocol for model-robustness testing of the Sounding source-packet workflow.
- `skills/ocean/evals/sounding-multimodel-r1-codex-slice-results.md`: first executed Codex/OpenAI slice of the Sounding multi-model strict eval.
- `skills/ocean/evals/sounding-multimodel-r1-deepseek-gemini-results.md`: live API slice for DeepSeek and Gemini after local keys were configured.
- `skills/ocean/evals/sounding-article-error-matrix-r2.md`: eight-article adversarial matrix with six error types per article.
- `skills/ocean/evals/sounding-article-error-matrix-r3.md`: ten-article adversarial matrix focused on foundation-model and biomedical AI preprints.
- `skills/ocean/evals/sounding-multimodel-r2-results.md`: coverage summary for the R2 multi-model execution, including the completed Gemini rerun after quota reset.
- `skills/ocean/evals/sounding-multimodel-r3-results.md`: coverage summary for the R3 10-article x 6-error multi-model execution, including the completed Gemini rerun after the initial HTTP 429 stop.
- `docs/module-map.md`: public module responsibility and validation-status map.
- `skills/ocean/evals/full-ocean-workflow-protocol.md`: protocol for testing whether one paper, idea, proposal, review comment, or resource seed can move through the seven-module workflow.
- `skills/ocean/evals/full-ocean-workflow-cases.md`: reusable full-workflow case seeds.
- `skills/ocean/evals/ocean-seven-module-coordination-r1-results.md`: deterministic structural check for Sounding -> Current -> Reef -> Iceberg -> Anchor -> Compass -> Harbor coordination, handoff continuity, downgrade gates, and Harbor closure.
- `skills/ocean/evals/research-design-workflow-r1-cases.json`: workflow-design case seeds for testing design gates, validation gates, research routes, and Harbor decision memory from uncertain biomedical research inputs.
- `skills/ocean/evals/research-design-workflow-r1-results.md`: first Research Design Workflow R1 model run over six completed model lanes, with Kimi recorded as runtime blocked.
- `skills/ocean/evals/domain-router-big-experiment-r1-cases.json`: offline routing case seeds for Domain Lens, Data/Tool Router, and Module Artifact Contract coverage.
- `skills/ocean/evals/domain-router-big-experiment-r1-results.md`: deterministic 33-check result file for the Domain Router Big Experiment R1 structural run.
- `skills/ocean/evals/domain-router-model-r1-cases.json`: model-eval case seeds for the central routing layer across seven modules.
- `skills/ocean/evals/domain-router-model-r1-results.md`: M3-scored model run over the Domain Lens / Data Tool Router / Module Artifact Contract prompt.
- `skills/ocean/scripts/check_ocean_contracts.py`: deterministic structural check for required references, module artifact terms, and domain-router case coverage.
- `skills/ocean/evals/ocean-module-m1-results.md`: first all-module coverage eval across Sounding, Current, Reef, Iceberg, Anchor, Compass, and Harbor.
- `skills/ocean/evals/ocean-module-m2-rubric.md`: 12-point scoring rubric for first-pass content-quality screening.
- `skills/ocean/evals/ocean-module-m2-results.md`: first heuristic M2 scoring screen over the 98 M1 all-module outputs.
- `skills/ocean/evals/ocean-module-m2-needs-review-triage.md`: manual triage guide for the 11 M2 `needs_review` rows.
- `skills/ocean/evals/ocean-module-m3-rubric.md`: 20-point OCEAN-10 rubric for module/model comparison, including task framing, source traceability, negative space, and output consistency.
- `skills/ocean/evals/ocean-module-m3-results.md`: first M3 screen over the existing 98 M1 all-module outputs.
- `skills/ocean/evals/harbor-focused-m3-r1-results.md`: Harbor-focused M3 run over five project-memory/collaboration-boundary cases across seven model lanes.
- `skills/ocean/evals/idea-scout-m3-r1-results.md`: Current/Compass M3 run for evidence-bounded idea generation from trends, reviewer pressure, and one-sentence idea seeds.
- `skills/ocean/evals/reef-strict-eval-r1-results.md`: first Reef-focused strict eval over resource provenance, API/database boundaries, KG association, cell atlas planning, and clinical registry metadata cases.
- `skills/ocean/evals/collaborative-workflow-r1-results.md`: cross-module workflow eval covering proposal, trend, resource/API, claim downgrade, validation, reviewer-pressure-to-idea, benchmark fairness, and Harbor handoff cases.
- `skills/ocean/evals/bioinformatics-real-tool-smoke-r1-results.md`: local availability/version smoke check for all 115 bioinformatics tool scaffolds in the current execution environment.

## What Is Not Included

- No private manuscripts.
- No patient data.
- No private peer-review text.
- No large copyrighted paper excerpts.
- No raw hidden-answer logs or contamination decoys from `outputs/`.

## Module Coverage Boundary

The strongest strict module-specific validation is still concentrated on **Sounding**. M1 adds initial all-module coverage testing for Current, Reef, Iceberg, Anchor, Compass, and Harbor. M2 adds a deterministic 12-point heuristic scoring screen over those 98 outputs. M3 introduces the 20-point OCEAN-10 rubric for future module/model comparison. These should be read as coverage and first-pass behavioral scoring, not final source-grounded content-quality judgment.

Reef-R1 adds the first dedicated Reef strict eval. It focuses on resource provenance, API/database boundary control, KG association overclaim prevention, and clinical registry metadata boundaries.

Collaborative Workflow R1 adds a broader cross-module workflow stress test. It checks whether OCEAN can preserve evidence boundaries while moving from proposal/source packet setup to resource mapping, claim downgrade, validation planning, idea planning, and Harbor records.

Seven-Module Coordination R1 adds a deterministic full-chain structural check over paper-source-packet, proposal, and one-sentence-idea seeds. It tests whether the seven modules remain connected through concrete artifacts and Handoff Tickets before any model-based content evaluation.

Bioinformatics Real-Tool Smoke R1 checks whether the 115 scaffolded bioinformatics tools are actually callable in the current local environment. It is an availability/version/import smoke test, not an end-to-end biological analysis.

Bioinformatics Tool Usage Guide R1 adds science-skills-style `references/tool_usage.md` files to every bioinformatics tool folder. The scaffold eval now verifies these usage guides alongside `tool.json`, README, example run records, API contracts, and Python wrappers.

API/Database Adapter R1 adds executable Reef wrappers for UniProt, PubMed, EuropePMC, ChEMBL, OpenTargets, STRING, Reactome, QuickGO, ClinVar, gnomAD, and AlphaFold DB. Dry-run eval checks packet construction without network calls; bounded live eval performs public API requests and passed 11/11 adapters.

Harbor-focused M3 R1 adds the first dedicated Harbor test. It focuses on decision memos, contribution boundaries, stale evidence reuse, stop-condition handoffs, public/private development memory, and MiniMax clean-output handling.

Idea Scout M3 R1 tests whether Current and Compass can turn trend/reviewer-pressure/idea seeds into bounded research directions without claiming proven novelty, field dominance, or publication readiness.

Research Design Workflow R1 tests whether OCEAN behaves as a research process workflow: source boundary first, resource routing second, claim calibration before validation planning, and decision memory at the end. The first completed scoring pass covered 42 usable outputs across six model lanes; Kimi was runtime-blocked and should be retried separately before content-quality comparison.

Domain Router Big Experiment R1 is an offline structural experiment. It does not call external model APIs. It checks whether OCEAN's new central routing layer covers representative biomedical inputs across medical AI, biological AI, omics, clinical research, drug/target hypotheses, KG/database resources, public-review pressure, collaboration boundaries, and stale Harbor reuse.

Domain Router Model R1 is the first model-based run focused on the new central routing layer. It completed 49/49 usable outputs across seven enabled model/control lanes and surfaced one substantive data-router issue: an uninspected Open Targets endpoint/query invented in a Reef case.

See `docs/module-map.md` for the current module responsibility and validation-status map.

## Sounding Model Comparison

The current public comparison set is Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and a Perplexity retrieval control group. The comparison is not a leaderboard for general intelligence. It asks whether each model can follow the same Sounding source-packet workflow, preserve evidence boundaries, avoid invented sources, and produce reusable handoff objects.

Perplexity is listed as a retrieval control group rather than a normal model lane. It helps test whether retrieval-oriented outputs with citations/search results can be converted into OCEAN source packets, but retrieved sources still require quality checks and manual evidence review.

The R2 and R3 article/error matrices are best read as a reusable case library. They preserve concrete article seeds, inspected-source boundaries, adversarial user-claim types, and expected safe behavior so future OCEAN runs can be checked for evidence discipline without reusing private manuscripts or hidden answer keys.

As of 2026-06-30, R2 and R3 coverage records show Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and the Perplexity retrieval control all reached complete usable-output coverage for their respective matrices. Coverage means the model/API produced usable Sounding artifacts; it is not a final content-quality ranking.

## Evaluation Boundary

The evaluation checks whether OCEAN preserves evidence boundaries when reviewing claims. It does **not** prove or disprove the scientific correctness of the source articles.

The key pass condition is behavioral:

- state what was inspected and not inspected;
- refuse or downgrade unsupported claims;
- avoid invented data, sample sizes, metrics, validations, reviewer comments, author roles, or clinical conclusions;
- separate model prediction, association, database evidence, text-mining evidence, mechanism, causality, and clinical utility.

For the full internal validation log, see `skills/ocean/evals/release-validation-log.md`.
