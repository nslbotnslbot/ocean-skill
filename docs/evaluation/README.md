# OCEAN Evaluation

This folder contains public-facing evaluation notes for **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**.

These files are for GitHub transparency. They are not runtime instructions for the skill and should not be treated as scientific evidence.

For the broader public positioning boundary, see [`../project-boundary.md`](../project-boundary.md). In short, OCEAN evaluation files are source-boundary and behavior-regression materials, not internal research trajectory ledgers, discovery endpoint spectra, or publication-release records.

## What Is Included

- `round-1-5-results.md`: concise public summary of strict validation rounds 1-5.
- `sounding-adversarial-case-library.md`: personal-reference guide for using the Sounding article/error matrices as an evidence-boundary case library rather than as ordinary API test logs.
- `reference-materials/public-sources.md`: public DOI, arXiv, bioRxiv, and public-review source identifiers used or prepared for evals.
- `reference-materials/boundary-cases.md`: synthetic boundary-case categories used to test anti-hallucination behavior.
- `validation/sounding-multimodel-strict-eval.md`: protocol for model-robustness testing of the Sounding source-packet workflow.
- `validation/sounding-multimodel-r1-codex-slice-results.md`: first executed Codex/OpenAI slice of the Sounding multi-model strict eval.
- `validation/sounding-multimodel-r1-deepseek-gemini-results.md`: live API slice for DeepSeek and Gemini after local keys were configured.
- `validation/sounding-article-error-matrix-r2.md`: eight-article adversarial matrix with six error types per article.
- `validation/sounding-article-error-matrix-r3.md`: ten-article adversarial matrix focused on foundation-model and biomedical AI preprints.
- `validation/sounding-multimodel-r2-results.md`: coverage summary for the R2 multi-model execution, including the completed Gemini rerun after quota reset.
- `validation/sounding-multimodel-r3-results.md`: coverage summary for the R3 10-article x 6-error multi-model execution, including the completed Gemini rerun after the initial HTTP 429 stop.
- `docs/module-map.md`: public module responsibility and validation-status map.
- `validation/full-ocean-workflow-protocol.md`: protocol for testing whether one paper, idea, proposal, review comment, or resource seed can move through the seven-module workflow.
- `validation/full-ocean-workflow-cases.md`: reusable full-workflow case seeds.
- `validation/ocean-seven-module-coordination-r1-results.md`: deterministic structural check for Sounding -> Current -> Reef -> Iceberg -> Anchor -> Compass -> Harbor coordination, handoff continuity, downgrade gates, and Harbor closure.
- `validation/research-design-workflow-r1-cases.json`: workflow-design case seeds for testing design gates, validation gates, research routes, and Harbor decision memory from uncertain biomedical research inputs.
- `validation/research-design-workflow-r1-results.md`: first Research Design Workflow R1 model run over six completed model lanes, with Kimi recorded as runtime blocked.
- `validation/domain-router-big-experiment-r1-cases.json`: offline routing case seeds for Domain Lens, Data/Tool Router, and Module Artifact Contract coverage.
- `validation/domain-router-big-experiment-r1-results.md`: deterministic 33-check result file for the Domain Router Big Experiment R1 structural run.
- `validation/domain-router-model-r1-cases.json`: model-eval case seeds for the central routing layer across seven modules.
- `validation/domain-router-model-r1-results.md`: M3-scored model run over the Domain Lens / Data Tool Router / Module Artifact Contract prompt.
- `validation/project-start-gate-r1-results.md`: Harbor Project Start Gate smoke test for Project Start Card, Harbor Seed, GitHub Sync Ticket, and public-safe persistence boundaries.
- `validation/manuscript-revision-mode-r1-results.md`: deterministic lifecycle-routing regression for separating finished-text revision from design/full-audit behavior and keeping critique outside paste-ready manuscript prose.
- `skills/ocean/scripts/check_ocean_contracts.py`: deterministic structural check for required references, module artifact terms, and domain-router case coverage.
- `validation/ocean-module-m1-results.md`: first all-module coverage eval across Sounding, Current, Reef, Iceberg, Anchor, Compass, and Harbor.
- `validation/ocean-module-m2-rubric.md`: 12-point scoring rubric for first-pass content-quality screening.
- `validation/ocean-module-m2-results.md`: first heuristic M2 scoring screen over the 98 M1 all-module outputs.
- `validation/ocean-module-m2-needs-review-triage.md`: manual triage guide for the 11 M2 `needs_review` rows.
- `validation/ocean-module-m3-rubric.md`: 20-point OCEAN-10 rubric for module/model comparison, including task framing, source traceability, negative space, and output consistency.
- `validation/ocean-module-m3-results.md`: first M3 screen over the existing 98 M1 all-module outputs.
- `validation/harbor-focused-m3-r1-results.md`: Harbor-focused M3 run over five project-memory/collaboration-boundary cases across seven model lanes.
- `validation/idea-scout-m3-r1-results.md`: Current/Compass M3 run for evidence-bounded idea generation from trends, reviewer pressure, and one-sentence idea seeds.
- `validation/reef-strict-eval-r1-results.md`: first Reef-focused strict eval over resource provenance, API/database boundaries, KG association, cell atlas planning, and clinical registry metadata cases.
- `validation/collaborative-workflow-r1-results.md`: cross-module workflow eval covering proposal, trend, resource/API, claim downgrade, validation, reviewer-pressure-to-idea, benchmark fairness, and Harbor handoff cases.
- `validation/bioinformatics-real-tool-smoke-r1-results.md`: local availability/version smoke check for all 115 bioinformatics tool scaffolds in the current execution environment.
- `validation/bioinformatics-execution-layer-r1-results.md`: execution-layer check for lightweight CLI, R/Bioconductor, and heavy-tool launcher behavior.
- `validation/bioinformatics-tool-router-r1-results.md`: tool-router check for 115 execution profiles and common workflow plans.
- `validation/bioinformatics-capability-matrix-r1-results.md`: combined planning matrix joining the 115-tool registry, per-tool API/source-packet contracts, and real-tool smoke results.
- `validation/bioinformatics-wrapper-readiness-r1-results.md`: high-priority wrapper readiness plans for install/container/smoke/source-packet implementation work.
- `validation/bioinformatics-wrapper-readiness-r1-eval-results.md`: structural eval for wrapper-readiness plan completeness and evidence-boundary safeguards.
- `validation/bioinformatics-wrapper-readiness-all-r1-results.md`: all-tool wrapper readiness plans covering 115 registered bioinformatics tool scaffolds.
- `validation/bioinformatics-wrapper-readiness-all-r1-eval-results.md`: structural eval for the all-tool readiness-plan set.
- `validation/bioinformatics-wrapper-implementation-backlog-r1-results.md`: ordered implementation backlog generated from the all-tool readiness plans.
- `validation/bioinformatics-wrapper-implementation-backlog-r1-eval-results.md`: structural eval for backlog completeness, rank continuity, next actions, and evidence boundaries.
- `validation/bioinformatics-per-tool-wrapper-r1-results.md`: full execution check for the generated per-tool `probe_or_plan.py` entrypoints across all 115 tool folders.
- `validation/bioinformatics-tool-scaffold-r1-results.md`: scaffold completeness check, now including source-packet wrappers, per-tool probe/plan wrappers, wrapper configs, API commands, examples, and usage guides.
- `validation/bioinformatics-cli-runner-r1-results.md`: bounded local CLI runner probe eval for the 60 lightweight command-line tool folders with per-tool `scripts/run_cli.py` entrypoints.
- `validation/bioinformatics-package-runner-r1-results.md`: bounded Python/R package runner probe eval for 26 package-based tool folders with per-tool `scripts/run_package.py` entrypoints.
- `validation/bioinformatics-launcher-runner-r1-results.md`: non-executing launcher-plan and workflow-runtime probe eval for the remaining 29 heavy, workflow-runtime, and source-packet-adapter tool folders with per-tool `scripts/run_launcher.py` entrypoints.
- `validation/bioinformatics-code-coverage-r1-results.md`: structural all-tool code-coverage eval confirming all 115 bioinformatics tool folders have their generic wrappers and execution-layer-specific runner/API commands.
- `validation/database-tool-adapter-r1-dry-run-results.md`: per-resource database tool-folder eval for 13 Reef adapters without network calls.
- `validation/database-tool-adapter-r1-live-results.md`: bounded live public API eval for the same 13 database tool folders.

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

Bioinformatics Execution Layer R1 checks the shared execution wrappers for three tool classes: lightweight CLI subprocess tools, R/Bioconductor tools through `Rscript`, and heavy/license/GUI/GPU/large-database tools through non-executing launcher plans. It records unavailable local dependencies instead of pretending tools ran.

Bioinformatics Tool Router R1 checks whether all 115 tools receive an execution profile and whether common biomedical/biological workflows can be converted into ordered tool plans with evidence boundaries and stop conditions.

Bioinformatics Capability Matrix R1 joins registry, API/source-packet contract, and real-tool smoke results into a single implementation-planning artifact. It separates source-packet adapters, source-packet scaffolds, locally executed smoke results, environment gaps, and high-priority practical wrapper candidates.

Bioinformatics Wrapper Readiness R1 turns the capability matrix into per-tool implementation plans for high-priority tools. It records candidate interface layers, smoke probes, install/container notes, minimal fixtures, required run evidence, stop conditions, and OCEAN handoffs. It does not install or execute the tools.

Bioinformatics Wrapper Readiness Eval R1 checks that readiness plans remain structurally complete and evidence-bound. It verifies required fields, run-evidence markers, route verification language, smoke commands, stop conditions, stages, scores, and per-tool artifacts.

Bioinformatics Wrapper Readiness All-Tool R1 extends the same readiness planning pattern from the 20 priority tools to all 115 registered bioinformatics tool folders. It is still a planning and source-packet contract artifact: 112 tools remain environment-missing in the current local smoke results, and the all-tool plans do not claim installation, execution, benchmarking, or scientific validation.

Bioinformatics Wrapper Implementation Backlog R1 converts the all-tool readiness set into an ordered engineering queue. It groups tools into immediate local packetization, priority environment setup, common CLI wrappers, Python/R package wrappers, workflow plans, and heavy-tool launcher plans. It passed 115/115 structural checks, but remains an implementation-planning artifact rather than a scientific result.

Bioinformatics Per-Tool Wrapper R1 executes every generated `scripts/probe_or_plan.py` entrypoint. It checks that all 115 tool folders now have callable code paths that produce bounded availability, import, or launcher-plan artifacts. The current environment produced 2 executed probes, 92 environment-missing records, and 21 planned-not-executed records; all 115 wrapper entrypoints passed structurally.

Bioinformatics Tool Usage Guide R1 adds science-skills-style `references/tool_usage.md` files to every bioinformatics tool folder. The scaffold eval now verifies these usage guides alongside `tool.json`, README, example run records, API contracts, and Python wrappers.

Bioinformatics Lightweight CLI Runner R1 adds per-tool `scripts/run_cli.py` entrypoints for 60 lightweight command-line tools. In the current local environment, all 60 probes correctly recorded `not_available_current_environment`; this is an environment boundary, not a biological analysis failure. The eval verifies that each runner writes bounded provenance artifacts and stops cleanly without pretending unavailable software ran.

Bioinformatics Python/R Package Runner R1 adds per-tool `scripts/run_package.py` entrypoints for 26 Python-package and R/Bioconductor tools. In the current local environment, DESeq2 and limma-voom package probes executed, while 24 package/module probes recorded `not_available_current_environment`. The eval verifies package-probe and source-packet behavior only; it does not validate scripts, workflows, biological analyses, or scientific claims.

Bioinformatics Launcher / Workflow Runner R1 adds per-tool `scripts/run_launcher.py` entrypoints for 29 heavy, workflow-runtime, and source-packet-adapter tools. It creates 29 non-executing launcher/source-packet plans and probes 8 workflow runtimes. In the current local environment, all workflow runtime probes recorded `not_available_current_environment`; this is an environment boundary, not a workflow failure.

Bioinformatics Code Coverage R1 checks the current all-tool code surface. It confirms 115/115 bioinformatics tool folders have generic source-packet/probe wrappers plus their execution-layer-specific runner/API commands: 60 CLI runners, 26 Python/R package runners, and 29 launcher/workflow/source-adapter runners.

API/Database Adapter R1 adds executable Reef wrappers for UniProt, PubMed, EuropePMC, ChEMBL, OpenTargets, STRING, Reactome, QuickGO, ClinVar, gnomAD, AlphaFold DB, ClinicalTrials.gov, and NCBI E-utilities. Dry-run eval checks packet construction without network calls; bounded live eval performs public API requests and passed 13/13 adapters.

Database Tool Adapter R1 exposes those public resource adapters as per-resource tool folders under `scripts/tools/databases/`, adding ClinicalTrials.gov and generic NCBI E-utilities to the tool-library layer. Dry-run and bounded live evals both passed 13/13. These are Reef resource-packet adapters, not biological or clinical validation.

Harbor-focused M3 R1 adds the first dedicated Harbor test. It focuses on decision memos, contribution boundaries, stale evidence reuse, stop-condition handoffs, public/private development memory, and MiniMax clean-output handling.

Idea Scout M3 R1 tests whether Current and Compass can turn trend/reviewer-pressure/idea seeds into bounded research directions without claiming proven novelty, field dominance, or publication readiness.

Research Design Workflow R1 tests whether OCEAN behaves as a research process workflow: source boundary first, resource routing second, claim calibration before validation planning, and decision memory at the end. The first completed scoring pass covered 42 usable outputs across six model lanes; Kimi was runtime-blocked and should be retried separately before content-quality comparison.

Domain Router Big Experiment R1 is an offline structural experiment. It does not call external model APIs. It checks whether OCEAN's new central routing layer covers representative biomedical inputs across medical AI, biological AI, omics, clinical research, drug/target hypotheses, KG/database resources, public-review pressure, collaboration boundaries, and stale Harbor reuse.

Domain Router Model R1 is the first model-based run focused on the new central routing layer. It completed 49/49 usable outputs across seven enabled model/control lanes and surfaced one substantive data-router issue: an uninspected Open Targets endpoint/query invented in a Reef case.

Project Start Gate R1 tests the Harbor persistence mechanism for new traceable OCEAN projects. It is a structural workflow test only: it checks project-card and GitHub-sync-ticket generation, not scientific validity, public-release readiness, or repository push behavior.

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

For the full internal validation log, see `validation/release-validation-log.md`.
