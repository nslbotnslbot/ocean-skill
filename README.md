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

## Real project progress

OCEAN is also tracked in real manuscript and research workflows through the canonical [`projects/`](projects/README.md) progress hub. Each project has its own public-safe status, evidence basis, OCEAN module record, dated progress log, next gate, and confidentiality boundary.

Current records cover the [whole-wheat fermented broth study](projects/whole-wheat-fermented-broth/README.md) and [Delirium AI ICU prediction transportability](projects/delirium-ai/README.md). Project tracking does not prove scientific validity, submission, acceptance, or clinical readiness.

## Project-start records

When a new OCEAN analysis becomes a traceable research project, Harbor can create a public-safe Project Start Card and GitHub Sync Ticket. This is meant to keep important research work from staying only in chat history. It does not publish raw data, private manuscripts, patient-level data, confidential review text, API keys, or unconfirmed submission outcomes.

The project-start gate is documented in `skills/ocean/references/project-start-gate.md`. A local record can be generated with:

```bash
python3 skills/ocean/scripts/create_project_start_record.py \
  --title "Example biomedical project" \
  --domain "Biological research" \
  --public-safe unclear \
  --outdir outputs/project-records \
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
skills/ocean/  installable skill, references, adapters, and tool wrappers
validation/    development cases, fixtures, scorecards, and regression records
docs/          public architecture, evaluation summaries, and case studies
projects/      public-safe progress records for real OCEAN research projects
examples/      small source-safe examples
assets/        logos and README media
outputs/       ignored local generated work
.github/       continuous integration
```

See [`docs/repository-layout.md`](docs/repository-layout.md) for ownership rules, canonical instruction sources, and generated-file policy. Installing `skills/ocean/` no longer copies the validation archive into the runtime skill.

## Evaluation summary

OCEAN keeps detailed validation evidence outside the installable skill. The main test layers are:

| Layer | Scope |
|---|---|
| Evidence-boundary evals | Missing, contradictory, non-traceable, and adversarial claims |
| Module evals | Artifact quality and handoffs across all seven modules |
| Multi-model evals | Workflow robustness across configured model providers |
| Tool and adapter evals | Dry-run/live API packets, local availability, provenance, and stop conditions |
| Repository regressions | Skill validation, JSON parsing, structural contracts, and wrapper boundary tests |

The deepest historical strict testing remains Sounding, with later rounds extending coverage to the full workflow, domain/data routing, research design, Reef, and Harbor. These are development checks, not proof of scientific correctness or a model leaderboard.

Start with [`docs/evaluation/README.md`](docs/evaluation/README.md) for the public index, [`validation/README.md`](validation/README.md) for archive policy, and [`validation/release-validation-log.md`](validation/release-validation-log.md) for the detailed record.

## Development checks

Run the sample scripts before publishing:

```bash
python3 -m pip install -r requirements-dev.txt
python3 skills/ocean/scripts/make_claim_table.py --out outputs/claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py examples/sample_claim_table.csv --out outputs/claim_table_summary.md
python3 skills/ocean/scripts/make_claim_table.py --empty --out outputs/empty_claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py outputs/empty_claim_table.csv --out outputs/empty_claim_table_summary.md
python3 skills/ocean/scripts/run_reef_api_adapter.py --adapter ncbi-eutils --database pubmed --query "BRCA1 breast cancer" --retmax 5 --out outputs/reef_api_packet.json
python3 skills/ocean/scripts/run_sounding_multimodel_eval.py --dry-run
python3 validation/scripts/check_json_files.py
python3 validation/scripts/validate_skill.py
python3 -m unittest discover -s validation/scripts -p 'test_*.py' -v
python3 skills/ocean/scripts/check_ocean_contracts.py --out outputs/ocean-contract-check.md
python3 skills/ocean/scripts/check_manuscript_revision_mode.py --out outputs/manuscript-revision-check.md
```

Before release, run the manual forward tests in `validation/forward-test-cases.md` using real user-provided or public, source-traceable materials. Use `validation/anti-hallucination-cases.md` for incomplete, missing, contradictory, or non-traceable evidence tests. Use `validation/public-source-protocol.md` to select DOI papers, bioRxiv/medRxiv preprints, and public peer review reports, track concrete candidates in `validation/source-candidates.md`, use `validation/sounding-multimodel-strict-eval.md` for model-robustness checks, use `validation/full-ocean-workflow-protocol.md` for seven-module workflow checks, and summarize validation-check outcomes in `validation/release-validation-log.md`.

## License

MIT License. See `LICENSE`.
