# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[中文版本](README.zh-CN.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow.jpg)

OCEAN is a lightweight Codex-compatible skill for scientific claim auditing, biomedical evidence review, AI-for-Science manuscript evaluation, journal positioning, and collaboration boundary analysis.

OCEAN is an independent open-source workflow project. Its evidence-discovery module is named **Sounding**: a source-packet workflow for scanning literature, evidence boundaries, and traceable review materials.

## What this is

This package is designed for personal use inside Codex and for publishing as a small GitHub repository.

It provides two entry points:

1. `AGENTS.md` at the repository root, so Codex can automatically read project-level instructions.
2. `skills/ocean/SKILL.md`, so the same workflow can be used as a portable skill folder if your Codex interface supports Skills.

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

OCEAN uses seven modules in order:

1. **Sounding**: scan literature, evidence, DOI/preprint/public review sources, and build traceable source packets.
2. **Current**: analyze field trends and direction flow.
3. **Reef**: organize knowledge graph, database, benchmark, cohort, and resource evidence.
4. **Iceberg**: audit claim support beneath surface-level conclusions.
5. **Anchor**: design validation, replication, benchmark, leakage, and reproducibility checks.
6. **Compass**: turn evidence into research plans, experiment design, idea prioritization, and journal strategy.
7. **Harbor**: preserve reports, workspace memory, and collaboration records.

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
docs/evaluation/
├── README.md
├── round-1-5-results.md
└── reference-materials/
    ├── boundary-cases.md
    └── public-sources.md
skills/ocean/
├── SKILL.md
├── agents/openai.yaml
├── evals/
│   ├── anti-hallucination-cases.md
│   ├── contamination-resistance-round5.md
│   ├── forward-test-cases.md
│   ├── public-source-protocol.md
│   ├── real-article-adversarial-cases.md
│   ├── release-validation-log.md
│   ├── sounding-multimodel-cases.json
│   ├── sounding-multimodel-models.example.json
│   ├── sounding-multimodel-r1-codex-slice-results.md
│   ├── sounding-multimodel-strict-eval.md
│   └── source-candidates.md
├── references/
│   ├── audit-lenses.md
│   ├── claim-evidence-table.md
│   ├── output-contract.md
│   ├── reviewer-lens.md
│   ├── review-report.md
│   └── sounding.md
└── scripts/
    ├── make_claim_table.py
    ├── check_claim_table.py
    ├── make_review_skeleton.py
    └── run_sounding_multimodel_eval.py
```

## Evaluation summary

Public-facing validation notes are in `docs/evaluation/`. The concise summary is `docs/evaluation/round-1-5-results.md`, and public source identifiers are in `docs/evaluation/reference-materials/public-sources.md`.

The current Sounding model-comparison plan includes Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and a Perplexity retrieval control group. Perplexity is treated as a retrieval-oriented control because it markets itself around answer/search grounding; it is not an OCEAN dependency. The goal is to compare how consistently different models execute the same Sounding workflow, output contract, evidence boundary, and source-packet handoff.

These files show what was tested and what passed without copying private materials, long paper passages, or hidden-answer logs. The internal release log remains in `skills/ocean/evals/release-validation-log.md`.

## Development checks

Run the sample scripts before publishing:

```bash
python3 skills/ocean/scripts/make_claim_table.py --out outputs/claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py examples/sample_claim_table.csv --out outputs/claim_table_summary.md
python3 skills/ocean/scripts/make_claim_table.py --empty --out outputs/empty_claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py outputs/empty_claim_table.csv --out outputs/empty_claim_table_summary.md
python3 skills/ocean/scripts/run_sounding_multimodel_eval.py --dry-run
```

Before release, run the manual forward tests in `skills/ocean/evals/forward-test-cases.md` using real user-provided or public, source-traceable materials. Use `skills/ocean/evals/anti-hallucination-cases.md` for incomplete, missing, contradictory, or non-traceable evidence tests. Use `skills/ocean/evals/public-source-protocol.md` to select DOI papers, bioRxiv/medRxiv preprints, and public peer review reports, track concrete candidates in `skills/ocean/evals/source-candidates.md`, use `skills/ocean/evals/sounding-multimodel-strict-eval.md` for model-robustness checks, and summarize release-gate outcomes in `skills/ocean/evals/release-validation-log.md`.

## License

MIT License. See `LICENSE`.
