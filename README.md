# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[中文版本](README.zh-CN.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow-logo-v4.png)

OCEAN is a lightweight Codex-compatible skill for biomedical claim-evidence navigation across medical and biological research. It can support biomedical AI studies, biological AI studies, manuscripts, databases, knowledge graphs, clinical prediction work, journal positioning, validation planning, and collaboration boundary analysis. A Domain Lens and Data/Tool Router apply evidence standards suited to medical, biological, omics, clinical, drug, KG/database, proposal, and collaboration tasks.

Its evidence-discovery module is named **Sounding**: a source-packet workflow for scanning literature, evidence boundaries, and traceable review materials.

**Simple at the surface, rigorous underneath, and traceable when the work becomes a project.**

[Detailed usage guide](docs/usage-guide.md) |
[Evidence-control CLI](docs/evidence-control-plane.md) |
[Availability audit validation](docs/availability-evidence-cards-v1.md) |
[中文使用指南](docs/usage-guide.zh-CN.md)

## What this is

This repository provides the installable skill at
[`skills/ocean/`](skills/ocean/) together with concise user guides, reusable
tool adapters, and public project examples.

## Boundary, scope, and non-goals

OCEAN is a **source-packet-based claim-evidence workflow**. Its main objects are source packets, evidence gates, claim audit cards, safe rewrites, negative space, reviewer-risk tickets, and validation plans.

OCEAN is **biomedical first, AI-aware, and evidence-boundary centered**.

- Core scope: biomedical research.
- Main domains: medical research and biological research.
- Priority use cases today: medical AI research, biological AI research, bioinformatics, clinical prediction, knowledge graphs, databases, public review signals, manuscripts, and research planning.
- Out of scope: summary-only paper reading, unsupported clinical advice, invented data, or broad general-science claims without a biomedical evidence question.

OCEAN is not:

- an autonomous AI scientist;
- a substitute for experiments, domain experts, or clinical judgment;
- a source of invented evidence or unsupported clinical advice.

## Use OCEAN in 60 seconds

Users choose the outcome they need; OCEAN chooses the minimum required modules.

| Mode | Ask OCEAN to | Default visible result |
|---|---|---|
| **Explore** | understand a paper, idea, source, or field | clear explanation plus evidence limits |
| **Design** | turn an idea, proposal, or gap into a feasible study | research route, decisive controls, next experiment |
| **Audit** | test claims, methods, validation, or submission readiness | claim verdicts, risks, missing evidence, fixes |
| **Revise** | improve finished manuscript text | clean replacement text; notes kept separate |
| **Track** | preserve a confirmed project or submission update | current status, latest milestone, next step |

```text
Use $ocean to explore this DOI for a journal club.
Use $ocean in Design mode to turn this one-sentence idea into a feasible study.
Use $ocean in Audit mode to check this manuscript's claims and validation.
Use $ocean in Revise mode and return clean replacement text first.
Use $ocean in Track mode to record this confirmed submission update.
```

You do not need to know the seven module names. See the
[detailed English guide](docs/usage-guide.md) or
[Chinese guide](docs/usage-guide.zh-CN.md) for installation, prompt templates,
output depth, source handling, tools, and GitHub safety.

For finished manuscript text, **Revise** returns clean replacement prose first
and keeps scientific concerns or author questions separate. Full lifecycle
rules are in the [usage guide](docs/usage-guide.md).

## Module flow

OCEAN selects only the modules needed for the request and hides module names by default. For end-to-end work, each module completes a distinct event and hands off a concrete artifact. See `docs/module-map.md` for the fuller map.

| Order | Module | Event it completes | Typical output |
|---:|---|---|---|
| 1 | **Sounding** | Evidence discovery and source-boundary setup | Source packet, Evidence Radar Map, Negative Space, Handoff Ticket |
| 2 | **Current** | Field trend and direction-flow reading | Trend map, recent movement, opportunity/risk notes |
| 3 | **Reef** | Biomedical resource, clinical data, KG, and database organization | Resource provenance map, data-source routing, database/KG evidence table |
| 4 | **Iceberg** | Claim-evidence audit under the surface claim | Claim-evidence matrix, downgrade/rewrite notes |
| 5 | **Anchor** | Validation, replication, leakage, benchmark, and reproducibility planning | Validation checklist, benchmark/leakage plan, reproducibility risks |
| 6 | **Compass** | Research planning and strategic decision-making | Idea card, experiment plan, journal/collaboration strategy |
| 7 | **Harbor** | Report preservation and collaboration boundary memory | Final report, decision note, contribution boundary record |

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
Use $ocean to explore this abstract-only claim.
Give me the short Decision Card and state what cannot yet be concluded.
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
Use $ocean in Audit mode to evaluate the uploaded manuscript.
Please output in Chinese.
Focus on scientific value, reliability, key risks, missing validation, collaboration contribution boundary, and journal positioning.
Use Standard output because this is an explicit multi-part audit.
```

For wording-only revision of an already drafted passage:

```text
Use $ocean in Manuscript Revision mode. Return clean replacement text first.
Keep audit notes and author queries outside the manuscript text.
```

To browse the biomedical tool catalog:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py profile --tool last
```

See the [bilingual tool index](skills/ocean/scripts/README.md) for database
adapters, workflow templates, execution layers, and evidence boundaries.

## Output principle

Default output language: Chinese.

For ordinary first-turn and narrow questions, OCEAN begins with a short Decision Card: conclusion, basis, what cannot currently be judged, the main risk, and the next action. Standard and Deep audits are used only when explicitly requested or genuinely needed. Manuscript Revision returns clean replacement prose first. Track records only confirmed status, the latest milestone, and the next step.

Every mode remains evidence-bound. Do not overstate novelty or validity. Always distinguish:

- hypothesis vs evidence
- association vs causality
- database co-occurrence vs mechanism
- internal validation vs external validation
- system demonstration vs scientific discovery
- light advice vs authorship-level contribution

For explicit audits, OCEAN can use the full claim-evidence contract. Scores, journal positioning, authorship analysis, and seven-module narratives are omitted unless requested or materially useful.

### Data, code, and model availability

OCEAN can now produce a fixed 14-dimension Availability Evidence Card for
data, code, repositories, identifiers, access conditions, metadata, licenses,
source data, model weights, prompts/configuration, environments, and versions.
It treats URLs, DOIs, accessions, and repository names as unverified candidates
until a separate authorized check is performed. A no-hit result means only
`not_explicitly_located`, never that the artifact is absent.

The public contract is in
[`availability-audit.md`](skills/ocean/references/availability-audit.md), the
machine-readable schema is in
[`availability_evidence_card.schema.json`](skills/ocean/schemas/availability_evidence_card.schema.json),
and the bounded 70-paper validation snapshot is in
[`docs/availability-evidence-cards-v1.md`](docs/availability-evidence-cards-v1.md).

## Project examples

The concise [`projects/`](projects/README.md) hub shows how OCEAN is being used
in the whole-wheat fermented broth study and the Delirium AI ICU prediction
project. Only confirmed public milestones are shown.

## Repository map

- [`skills/ocean/`](skills/ocean/): installable skill, references, adapters, and tool wrappers
- [`docs/`](docs/): usage guides and the executable evidence-control CLI
- [`projects/`](projects/): concise public project examples
- [`examples/`](examples/): reusable starter files
- [`assets/`](assets/): OCEAN artwork and icons

## License

MIT License. See `LICENSE`.
