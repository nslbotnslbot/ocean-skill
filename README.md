# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[中文版本](README.zh-CN.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow.jpg)

OCEAN is a lightweight Codex-compatible skill for biomedical research claim-evidence navigation and research design workflow across medical and biological research. It is AI-aware, but not AI-only: it can support biomedical AI studies, biological AI studies, manuscripts, databases, knowledge graphs, clinical prediction work, journal positioning, validation planning, and collaboration boundary analysis. It now includes a central Domain Lens and Data/Tool Router so medical, biological, omics, clinical, drug, KG/database, proposal, and collaboration tasks use different evidence standards instead of one generic checklist.

OCEAN is an independent open-source workflow project. Its evidence-discovery module is named **Sounding**: a source-packet workflow for scanning literature, evidence boundaries, and traceable review materials.

## What this is

This package is designed for personal use inside Codex and for publishing as a small GitHub repository.

It provides two entry points:

1. `AGENTS.md` at the repository root, so Codex can automatically read project-level instructions.
2. `skills/ocean/SKILL.md`, so the same workflow can be used as a portable skill folder if your Codex interface supports Skills.

## Scope

OCEAN is **biomedical first, AI-aware, and evidence-boundary centered**.

- Core scope: biomedical research.
- Main domains: medical research and biological research.
- Priority use cases today: medical AI research, biological AI research, bioinformatics, clinical prediction, knowledge graphs, databases, public review signals, manuscripts, and research planning.
- Out of scope: summary-only paper reading, unsupported clinical advice, invented data, or broad general-science claims without a biomedical evidence question.

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

## Module flow

OCEAN uses seven modules in order. Each module is meant to complete a different event and hand off a concrete artifact to the next step. See `docs/module-map.md` for the fuller public map.

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

By default, OCEAN uses a fixed output contract: audit card, evidence boundary, claim-evidence matrix, risk register, missing evidence/analysis, collaboration boundary, journal positioning, next actions, and scores. Use quick mode only for narrow questions and deep mode for full manuscript or reviewer-style reports.

## Repository layout

```text
.env.ocean.example
README.zh-CN.md
assets/
└── ocean-polar-workflow.jpg
docs/
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

Collaborative Workflow R1 adds a cross-module workflow stress test over proposal, trend, resource/API, claim downgrade, validation, reviewer-pressure-to-idea, benchmark fairness, and Harbor handoff cases.

Full-workflow protocol and case seeds are included to test whether one paper, one idea, one proposal, one review comment, or one resource/KG seed can move through the seven OCEAN modules with stable handoffs and evidence boundaries.

Research Design Workflow R1 tests whether OCEAN can turn uncertain ideas, proposals, resource requests, reviewer pressure, and workflow decisions into design gates, validation gates, research routes, and Harbor decision memory without claiming unsupported maturity. The first scored pass covered 42 usable outputs across six completed model lanes; one Kimi lane was runtime-blocked and is tracked separately.

Domain Router Big Experiment R1 tests the new central routing layer offline. It checks that the Domain Lens, Data/Tool Router, and Module Artifact Contract are connected to the skill entrypoint and cover representative biomedical inputs across medical AI, biological AI, omics, clinical research, drug/target hypotheses, KG/database resources, public-review pressure, collaboration boundaries, and stale Harbor reuse.

Domain Router Model R1 then tests the same central layer across Qwen, DeepSeek, Kimi fallback, MiniMax-M1, Gemini, Claude, and Perplexity retrieval control. The run completed 49/49 usable outputs with a 17.86/20 mean M3 score. The most important flagged issue was an endpoint-invention trap in a Reef/Open Targets case, which is now tracked as a data-router safety concern.

The earlier anti-hallucination and contamination-resistance tests exercise OCEAN's evidence-boundary behavior and claim-downgrade discipline. M1/M2 should still be read as coverage plus heuristic screening, not final scientific correctness validation or a model leaderboard.

These files show what was tested and what passed without copying private materials, long paper passages, or hidden-answer logs. The internal release log remains in `skills/ocean/evals/release-validation-log.md`.

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

Before release, run the manual forward tests in `skills/ocean/evals/forward-test-cases.md` using real user-provided or public, source-traceable materials. Use `skills/ocean/evals/anti-hallucination-cases.md` for incomplete, missing, contradictory, or non-traceable evidence tests. Use `skills/ocean/evals/public-source-protocol.md` to select DOI papers, bioRxiv/medRxiv preprints, and public peer review reports, track concrete candidates in `skills/ocean/evals/source-candidates.md`, use `skills/ocean/evals/sounding-multimodel-strict-eval.md` for model-robustness checks, use `skills/ocean/evals/full-ocean-workflow-protocol.md` for seven-module workflow checks, and summarize release validation outcomes in `skills/ocean/evals/release-validation-log.md`.

## License

MIT License. See `LICENSE`.
