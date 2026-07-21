# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[中文版本](README.zh-CN.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow-logo-v4.png)

OCEAN is a lightweight Codex-compatible external audit layer and skill for biomedical research claim-evidence navigation across medical and biological research. It is AI-aware, but not AI-only: it can support biomedical AI studies, biological AI studies, manuscripts, databases, knowledge graphs, clinical prediction work, journal positioning, validation planning, and collaboration boundary analysis. It includes a central Domain Lens and Data/Tool Router so medical, biological, omics, clinical, drug, KG/database, proposal, and collaboration tasks use different evidence standards instead of one generic checklist.

OCEAN is an independent open-source workflow project. Its evidence-discovery module is named **Sounding**: a source-packet workflow for scanning literature, evidence boundaries, and traceable review materials. OCEAN audits what existing sources can and cannot support; it does not manage the internal execution or release workflow of a research program.

## What this is

This package is designed for personal use inside Codex and for publishing as a small GitHub repository.

It provides two entry points:

1. `AGENTS.md` at the repository root, so Codex can automatically read project-level instructions.
2. `skills/ocean/SKILL.md`, so the same workflow can be used as a portable skill folder if your Codex interface supports Skills.

## Boundary, scope, and non-goals

OCEAN should be described as a **source-packet-based claim-evidence audit layer**. Its main objects are source packets, evidence gates, claim audit cards, safe rewrites, negative space, reviewer-risk tickets, and validation plans.

See [`docs/project-boundary.md`](docs/project-boundary.md) for the longer public positioning memo.

OCEAN is **biomedical first, AI-aware, and evidence-boundary centered**.

- Core scope: biomedical research.
- Main domains: medical research and biological research.
- Priority use cases today: medical AI research, biological AI research, bioinformatics, clinical prediction, knowledge graphs, databases, public review signals, manuscripts, and research planning.
- Out of scope: summary-only paper reading, unsupported clinical advice, invented data, or broad general-science claims without a biomedical evidence question.

OCEAN is not:

- an autonomous AI scientist;
- a system for executing experiments or generating discoveries;
- an internal evidence-ledger or project release workflow;
- a human-supervised execution-package-to-release-gate system;
- a discovery endpoint spectrum for one research program.

When presenting OCEAN publicly, prefer wording such as **external claim-evidence auditing**, **evidence-type gating**, **source-packet construction**, **safe claim rewriting**, and **public adversarial case matrices**. Avoid making evidence ledgers, paired non-claims, endpoint ladders, or release gates the central contribution.

## Best use cases

Use this when you ask Codex to review:

- manuscripts
- preprints
- system papers
- AI-agent / AI-for-Science projects
- biomedical AI studies
- bioinformatics studies
- database / knowledge graph / CTD-style evidence systems
- clinical prediction models
- collaboration contribution boundaries
- paper positioning and journal strategy
- reviewer-style critique and pre-submission stress testing

## Manuscript lifecycle modes

OCEAN now separates manuscript work by lifecycle instead of treating every manuscript request as a full audit:

| Mode | Use it for | Default output |
|---|---|---|
| **Design / Audit** | ideas, proposals, experiment design, early drafts, or explicit weakness finding | Relevant module artifacts; full-chain critique only when genuinely needed |
| **Manuscript Revision** | finished passages that need polishing, shortening, translation, or evidence-safe wording changes | Clean replacement text first; editorial notes and author queries remain separate |
| **Pre-submission Stress Test** | explicit reviewer simulation or full submission-readiness audit | Audit report plus separately isolated safe rewrites |
| **Reviewer Response** | reviewer/editor comments and manuscript revision | Separate response-letter text, revised manuscript text, and author-only notes |

A generic request to revise a finished paragraph defaults to **Manuscript Revision**. OCEAN may use Iceberg as a silent safety check, but module labels, reviewer criticism, deletion commands, risk tables, scores, and new placeholders must not appear in paste-ready manuscript prose. See [`skills/ocean/references/manuscript-revision-mode.md`](skills/ocean/references/manuscript-revision-mode.md).

## Real workflow tracker

OCEAN is also being tracked in real manuscript and submission workflows. See `docs/application-submission-tracker.md` for the public-safe application and submission tracker.

The first public-safe case note is the [whole-wheat broth project](docs/case-studies/whole-wheat-broth-project.md). It shows how all seven OCEAN modules were used in one fermentation, microbiome, metabolomics, toxicology-support, and manuscript-planning workflow without publishing raw data or private manuscript text.

## Project-start records

When a new OCEAN analysis becomes a traceable research project, Harbor can create a public-safe Project Start Card and GitHub Sync Ticket. This is meant to keep important research work from staying only in chat history. It does not publish raw data, private manuscripts, patient-level data, confidential review text, API keys, or unconfirmed submission outcomes.

The project-start gate is documented in `skills/ocean/references/project-start-gate.md`. A local record can be generated with:

```bash
python3 skills/ocean/scripts/create_project_start_record.py \
  --title "Example biomedical project" \
  --domain "Biological research" \
  --public-safe unclear \
  --remote-push "needs approval"
```

## Module flow

OCEAN uses seven modules as an external audit sequence, not as an experiment-execution loop. Each module is meant to complete a different event and hand off a concrete artifact to the next step. See `docs/module-map.md` for the fuller public map.

| Order | Module | Event it completes | Typical output | Current validation status |
|---:|---|---|---|---|
| 1 | **Sounding** | Evidence discovery and source-boundary setup | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket | Strict multi-model evals completed |
| 2 | **Current** | Field trend and direction-flow reading | Trend map, recent movement, opportunity/risk notes | M1 covered; M2 screened |
| 3 | **Reef** | Biomedical resource, clinical data, KG, and database organization | Resource provenance map, data-source routing, database/KG evidence table | M1 covered; M2 screened |
| 4 | **Iceberg** | Claim-evidence audit under the surface claim | Claim-evidence matrix, downgrade/rewrite notes | M1 covered; M2 screened |
| 5 | **Anchor** | Validation, replication, leakage, benchmark, and reproducibility planning | Validation checklist, benchmark/leakage plan, reproducibility risks | M1 covered; M2 screened |
| 6 | **Compass** | Research planning and strategic decision-making | Idea card, experiment plan, journal/collaboration strategy | M1 covered; M2 screened |
| 7 | **Harbor** | Review report preservation and collaboration boundary memory | Final audit report, decision note, contribution boundary record | M1 covered; M2 screened |

## Quick start

### Install From GitHub

Install the skill from this repository:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo nslbotnslbot/ocean-skill \
  --path skills/ocean \
  --ref main
```

Then restart Codex or open a new Codex session and test recognition:

```text
Use $ocean to audit this abstract-only claim.
State inspected / not inspected / cannot conclude / needed next.
```

If you only wanted a temporary test install, remove it after testing:

```bash
rm -rf ~/.codex/skills/ocean
```

### Local Copy

If you already cloned this repository, copy the skill folder into your Codex skills directory:

```bash
cp -R skills/ocean ~/.codex/skills/
```

Then ask Codex:

```text
Use $ocean to evaluate the uploaded manuscript.
Please output in Chinese.
Focus on scientific value, reliability, key risks, missing validation, collaboration contribution boundary, and journal positioning.
Use the standard OCEAN output format unless I ask for a quick or deep report.
```

For wording-only revision of an already drafted passage:

```text
Use $ocean in Manuscript Revision mode. Return clean replacement text first.
Keep audit notes and author queries outside the manuscript text.
```

For an empty review report skeleton:

```bash
python3 skills/ocean/scripts/make_review_skeleton.py \
  --title "My AI for Science Project" \
  --project-type "AI-agent system / biomedical evidence audit" \
  --out outputs/review_skeleton.md
```

For a claim table template:

```bash
python3 skills/ocean/scripts/make_claim_table.py \
  --out outputs/claim_table.csv
```

After filling the CSV, validate and summarize it:

```bash
python3 skills/ocean/scripts/check_claim_table.py \
  outputs/claim_table.csv \
  --out outputs/claim_table_summary.md
```

## Output principle

Default output language: Chinese.

The analysis must be direct, critical, and evidence-bound. Do not overstate novelty or validity. Always distinguish:

- hypothesis vs evidence
- association vs causality
- database co-occurrence vs mechanism
- internal validation vs external validation
- system demonstration vs scientific discovery
- light advice vs authorship-level contribution

For audits, OCEAN uses a fixed output contract: audit card, evidence boundary, claim-evidence matrix, risk register, missing evidence/analysis, collaboration boundary, journal positioning, next actions, and scores. Finished-text editing instead uses the Manuscript Revision contract: clean replacement text, separate change notes, and author queries only when necessary. Use deep mode only for an explicit full manuscript or reviewer-style audit.

## Repository layout

```text
.env.ocean.example
README.zh-CN.md
assets/
└── ocean-polar-workflow.jpg
docs/
├── project-boundary.md
├── application-submission-tracker.md
├── case-studies/
│   └── whole-wheat-broth-project.md
├── module-map.md
└── evaluation/
    ├── README.md
    ├── round-1-5-results.md
    ├── sounding-adversarial-case-library.md
    └── reference-materials/
        ├── boundary-cases.md
        └── public-sources.md
skills/ocean/
├── SKILL.md
├── agents/openai.yaml
├── evals/
│   ├── anti-hallucination-cases.md
│   ├── collaborative-workflow-r1-results.md
│   ├── contamination-resistance-round5.md
│   ├── full-ocean-workflow-cases.md
│   ├── full-ocean-workflow-protocol.md
│   ├── ocean-module-m1-results.md
│   ├── ocean-module-m2-results.md
│   ├── ocean-module-m2-needs-review-triage.md
│   ├── forward-test-cases.md
│   ├── public-source-protocol.md
│   ├── real-article-adversarial-cases.md
│   ├── reef-strict-eval-r1-cases.json
│   ├── reef-strict-eval-r1-coverage.json
│   ├── reef-strict-eval-r1-results.md
│   ├── domain-router-big-experiment-r1-cases.json
│   ├── domain-router-model-r1-cases.json
│   ├── domain-router-model-r1-results.md
│   ├── release-validation-log.md
│   ├── sounding-multimodel-cases.json
│   ├── sounding-multimodel-models.example.json
│   ├── sounding-multimodel-r1-codex-slice-results.md
│   ├── sounding-multimodel-strict-eval.md
│   └── source-candidates.md
├── references/
│   ├── audit-lenses.md
│   ├── anchor.md
│   ├── claim-evidence-table.md
│   ├── compass.md
│   ├── current.md
│   ├── data-tool-router.md
│   ├── domain-lens.md
│   ├── harbor.md
│   ├── iceberg.md
│   ├── module-handoff.md
│   ├── module-artifact-contract.md
│   ├── output-contract.md
│   ├── reef-biological-data-sources.md
│   ├── reef.md
│   ├── reef-api-adapters.md
│   ├── research-design-workflow.md
│   ├── reviewer-lens.md
│   ├── review-report.md
│   └── sounding.md
└── scripts/
    ├── make_claim_table.py
    ├── check_claim_table.py
    ├── make_review_skeleton.py
    ├── check_ocean_contracts.py
    ├── run_reef_api_adapter.py
    └── run_sounding_multimodel_eval.py
```

## Evaluation summary

Public-facing validation notes are in `docs/evaluation/`. The concise summary is `docs/evaluation/round-1-5-results.md`, and public source identifiers are in `docs/evaluation/reference-materials/public-sources.md`.

Current module-specific strict testing is still deepest for **Sounding**. R2 and R3 test the Sounding source-packet workflow across Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and a Perplexity retrieval control group. M1 adds all-module coverage, and M2 adds first-pass heuristic scoring over the 98 M1 outputs. Perplexity is treated as a retrieval-oriented control because it markets itself around answer/search grounding; it is not an OCEAN dependency.

Reef now includes a biological/clinical data-source routing catalog for genes, proteins, variants, omics repositories, cell atlases, cancer genomics portals, drug resources, clinical registries, regulatory/safety data, EHR/cohort resources, imaging/signal datasets, model organisms, and microbiome/pathogen resources. Reef-R1 adds the first dedicated Reef strict eval, focused on resource provenance, API/database evidence boundaries, KG association overclaims, cell atlas planning boundaries, and clinical registry metadata boundaries.

Bioinformatics Real-Tool Smoke R1 checks all 115 scaffolded bioinformatics tools against the current local execution environment. In this local run, 3 tools/adapters executed at smoke level and 112 were not available on PATH, Python, or R in the current environment. This is an availability check, not an end-to-end biological analysis.

Bioinformatics Execution Layer R1 adds shared wrappers for lightweight CLI tools, R/Bioconductor tools, and heavy/license/GUI/GPU/large-database tools. Missing local software is recorded as an environment boundary rather than a fake successful run.

Bioinformatics Tool Router R1 profiles all 115 scaffolded tools into execution layers and creates workflow plans for common biomedical and biological analysis tasks, including FASTQ QC, RNA-seq, variant calling, single-cell, spatial, metagenomics, genome assembly, protein structure, epigenomics, proteomics/metabolomics, workflow reproducibility, and imaging AI.

Each bioinformatics tool folder now also includes a science-skills-style `references/tool_usage.md` guide. These guides define use/avoid rules, required local execution evidence, stop conditions, and OCEAN handoff paths without claiming the external tool is installed.

Lightweight CLI bioinformatics tools now have generated per-tool `scripts/run_cli.py` entrypoints. These can record bounded availability probes or explicit user-supplied command run records, while preserving environment-missing boundaries when software is not installed.

Python/R package bioinformatics tools now have generated per-tool `scripts/run_package.py` entrypoints. These can record bounded Python import or R package-version probes and explicit user-supplied script run records, without treating package availability as biological validation.

Heavy, workflow-runtime, and source-packet-adapter bioinformatics tools now have generated per-tool `scripts/run_launcher.py` entrypoints. These create non-executing launch/source-packet plans and, for workflow runtimes, bounded availability probes.

Reef now has executable API/database adapters for UniProt, PubMed, EuropePMC, ChEMBL, OpenTargets, STRING, Reactome, QuickGO, ClinVar, gnomAD, and AlphaFold DB. These wrappers can run dry, or make bounded live public API requests with `--execute`, then write OCEAN packets with explicit evidence boundaries.

Collaborative Workflow R1 adds a cross-module workflow stress test over proposal, trend, resource/API, claim downgrade, validation, reviewer-pressure-to-idea, benchmark fairness, and Harbor handoff cases.

Full-workflow protocol and case seeds are included to test whether one paper, one idea, one proposal, one review comment, or one resource/KG seed can move through the seven OCEAN modules with stable handoffs and evidence boundaries.

Seven-Module Coordination R1 adds the first deterministic full-chain structural check over paper-source-packet, proposal, and one-sentence-idea seeds, testing artifact coverage, handoff continuity, downgrade gates, and Harbor closure.

Research Design Workflow R1 tests whether OCEAN can turn uncertain ideas, proposals, resource requests, reviewer pressure, and workflow decisions into design gates, validation gates, research routes, and Harbor decision memory without claiming unsupported maturity. The first scored pass covered 42 usable outputs across six completed model lanes; one Kimi lane was runtime-blocked and is tracked separately.

Domain Router Big Experiment R1 tests the new central routing layer offline. It checks that the Domain Lens, Data/Tool Router, and Module Artifact Contract are connected to the skill entrypoint and cover representative biomedical inputs across medical AI, biological AI, omics, clinical research, drug/target hypotheses, KG/database resources, public-review pressure, collaboration boundaries, and stale Harbor reuse.

Domain Router Model R1 then tests the same central layer across Qwen, DeepSeek, Kimi fallback, MiniMax-M1, Gemini, Claude, and Perplexity retrieval control. The run completed 49/49 usable outputs with a 17.86/20 mean M3 score. The most important flagged issue was an endpoint-invention trap in a Reef/Open Targets case, which is now tracked as a data-router safety concern.

The earlier anti-hallucination and contamination-resistance tests exercise OCEAN's evidence-boundary behavior and claim-downgrade discipline. M1/M2 should still be read as coverage plus heuristic screening, not final scientific correctness validation or a model leaderboard.

These files show what was tested and what passed without copying private materials, long paper passages, or hidden-answer logs. The public evaluation materials are designed as reusable source-boundary checks, not as internal research trajectory records or discovery claims. The internal release log remains in `skills/ocean/evals/release-validation-log.md`.

## Development checks

Run the sample scripts before publishing:

```bash
python3 skills/ocean/scripts/make_claim_table.py --out outputs/claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py examples/sample_claim_table.csv --out outputs/claim_table_summary.md
python3 skills/ocean/scripts/make_claim_table.py --empty --out outputs/empty_claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py outputs/empty_claim_table.csv --out outputs/empty_claim_table_summary.md
python3 skills/ocean/scripts/run_reef_api_adapter.py --adapter ncbi-eutils --database pubmed --query "BRCA1 breast cancer" --retmax 5 --out outputs/reef_api_packet.json
python3 skills/ocean/scripts/run_sounding_multimodel_eval.py --dry-run
python3 skills/ocean/scripts/check_ocean_contracts.py
```

Before release, run the manual forward tests in `skills/ocean/evals/forward-test-cases.md` using real user-provided or public, source-traceable materials. Use `skills/ocean/evals/anti-hallucination-cases.md` for incomplete, missing, contradictory, or non-traceable evidence tests. Use `skills/ocean/evals/public-source-protocol.md` to select DOI papers, bioRxiv/medRxiv preprints, and public peer review reports, track concrete candidates in `skills/ocean/evals/source-candidates.md`, use `skills/ocean/evals/sounding-multimodel-strict-eval.md` for model-robustness checks, use `skills/ocean/evals/full-ocean-workflow-protocol.md` for seven-module workflow checks, and summarize validation-check outcomes in `skills/ocean/evals/release-validation-log.md`.

## License

MIT License. See `LICENSE`.
