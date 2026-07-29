# OCEAN Evidence-Control CLI

[中文版本](evidence-control-plane.zh-CN.md)

OCEAN's conversational skill decides what a research claim may safely say. The
evidence-control CLI makes that decision process traceable across files, tool
runs, task workflows, and long-running projects.

It is a control layer, not a scientific result generator. A successful command
means that an OCEAN contract was executed, not that a biological, clinical, or
engineering conclusion is true.

## Core contracts

| Contract | Purpose | What it does not prove |
|---|---|---|
| SourcePacket v2 | Source identity, version, checksum, locators, dependencies, and claim boundary | Source truth or claim entailment |
| PaperBundle | Page- or structure-grounded paper blocks, figures, tables, and unresolved regions | Correct extraction of image-only content |
| RunManifest | Command, software, inputs, outputs, environment, and checksums | Independent reproducibility |
| ValidationCard | Claim type, required evidence, controls, pass criteria, and stop conditions | That validation was performed |
| Artifact Envelope | Portable checksum and provenance wrapper for cross-tool artifacts | Scientific support |
| Harbor Ledger | Checksum-linked project events, decisions, failures, and conflicts | That a declared event occurred |

Schemas live in [`skills/ocean/schemas/`](../skills/ocean/schemas/).

## Requirements

Most control-plane commands use only the Python standard library. PDF extraction
can optionally use `pypdf` or the local `pdftotext` executable. Development
checks use PyYAML.

```bash
uv sync --dev
python3 skills/ocean/scripts/ocean.py --help
```

If `uv` is unavailable, use a Python 3.9 or newer environment and install the
declared dependencies from `pyproject.toml`.

## 1. Check the environment

```bash
python3 skills/ocean/scripts/ocean.py doctor \
  --output outputs/ocean-doctor.json
```

The doctor reports whether credential variables and local tools are present. It
does not print secret values and does not contact external APIs by default.

## 2. Create a grounded source

Create and validate a SourcePacket:

```bash
python3 skills/ocean/scripts/ocean.py source-packet create \
  --source-type primary_literature \
  --source-id YOUR_SOURCE_ID \
  --source-file path/to/source.pdf \
  --evidence-state inspected \
  --locator-mode page-grounded \
  --locators-json '[{"locator_id":"p1","locator_type":"page","value":"1"}]' \
  --output outputs/source-packet.json

python3 skills/ocean/scripts/ocean.py source-packet validate \
  --input outputs/source-packet.json
```

Queried evidence requires a checksum and at least one resolvable locator. When
content has not been inspected, keep the evidence state as `candidate` or
`unavailable`.

Prepare a paper:

```bash
python3 skills/ocean/scripts/ocean.py paper prepare \
  --input path/to/manuscript.pdf \
  --output outputs/paper-bundle.json
```

The result states whether grounding is page-based, structure-based, or
source-limited and records unresolved extraction regions.

## 3. Run a task workflow

Three reference workflows are included:

```bash
python3 skills/ocean/scripts/ocean.py workflow variant \
  --input path/to/variant-task.json \
  --output outputs/variant-audit.json

python3 skills/ocean/scripts/ocean.py workflow target-disease \
  --input path/to/target-disease-task.json \
  --output outputs/target-disease-audit.json

python3 skills/ocean/scripts/ocean.py workflow manuscript \
  --input path/to/manuscript-task.json \
  --output outputs/manuscript-reliability.json
```

Each workflow writes a `.run-manifest.json` sidecar. Missing evidence,
partially independent sources, circular validation, leakage, and unresolved
source locators remain visible. The manuscript workflow keeps clean replacement
text separate from audit notes.

## 4. Audit a claim or research design

The unified CLI exposes detectors and audits:

```text
detect independence | circularity | leakage | claim-validation | diff
audit statistics-design | statistics-unit | statistics-multiplicity
audit statistics-figure | statistics-claim | data-availability
audit citation-link | citation-scope | citation-entailment | citation-metadata
```

Use `--help` on a command to inspect its input and output arguments:

```bash
python3 skills/ocean/scripts/ocean.py audit statistics-unit --help
```

These checks are bounded by supplied metadata and locators. They do not silently
read missing full text, infer unreported sample structure, or fill repository
accessions and DOIs.

## 5. Preserve long-running decisions

Initialize and append to a checksum-linked Harbor ledger:

```bash
python3 skills/ocean/scripts/ocean.py ledger init \
  --project-id YOUR_PROJECT_ID \
  --title "Project title" \
  --output outputs/harbor-ledger.json

python3 skills/ocean/scripts/ocean.py ledger validate \
  --ledger outputs/harbor-ledger.json
```

Every appended event requires an explicit evidence boundary. SourcePacket and
RunManifest files can be attached by checksum. This preserves negative results,
conflicts, and changed decisions without turning them into hidden narrative
memory.

Use `detect diff` to compare old and new evidence snapshots. A changed source
does not automatically upgrade or downgrade a claim; it creates a human-review
requirement.

## 6. Interoperate with other tools

Bridges can convert a grounded reader artifact into a PaperBundle, convert a
scientific-tool result into a SourcePacket plus RunManifest, or wrap an artifact
in a portable envelope:

```bash
python3 skills/ocean/scripts/ocean.py bridge envelope \
  --input outputs/source-packet.json \
  --producer "your-tool" \
  --producer-version "1.0" \
  --access public \
  --license MIT \
  --output outputs/artifact-envelope.json
```

An envelope preserves identity and provenance; it does not certify the embedded
science.

## 7. Evaluate without overstating results

OCEAN-Bench currently includes 30 formal contract cases:

```bash
python3 skills/ocean/scripts/ocean.py benchmark run \
  --cases skills/ocean/evals/cases/golden_contract_cases.json \
  --output outputs/formal-contract-report.json
```

The cases contain no real patient records, experiments, or scientific
measurements and set `scientific_evidence: false`. They verify logic and
regression behavior only.

Research-level performance claims require at least 100 traceable cases, repeated
multi-model runs, pre-specified ablations, token/time/cost records, two blinded
experts per case, disagreement resolution, and external validation. The case
intake and leaderboard commands enforce these gates; they do not manufacture
missing evidence.

See [`BENCHMARK.md`](../skills/ocean/evals/BENCHMARK.md) and the
[human review protocol](../skills/ocean/evals/human_review/PROTOCOL.md).

## Public repository boundary

Commit stable schemas, scripts, fixtures that are safe to redistribute, public
protocols, and concise examples. Keep API keys, private manuscripts,
patient-level data, raw model outputs, local paths, internal review transcripts,
and exploratory logs outside the public repository.
