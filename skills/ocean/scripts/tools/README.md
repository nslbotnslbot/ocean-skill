# OCEAN Tool Adapters

[Complete tool index](../README.md) |
[中文工具总览](../README.zh-CN.md)

This directory contains bounded adapters and wrappers that turn inspected
sources or tool runs into OCEAN source packets.

## Layout

| Folder | Purpose |
|---|---|
| [`bioinformatics/`](bioinformatics/README.md) | 115 bioinformatics tool folders with per-tool metadata, examples, and bounded runners |
| [`databases/`](databases/) | 13 public Reef database adapters |
| [`literature/`](literature/) | Literature metadata and local-record source packets |
| [`clinicaltrials/`](clinicaltrials/) | ClinicalTrials.gov registry source packets |
| [`common/`](common/README.md) | Shared CLI, Python, R, launcher, database, and provenance helpers |

The parent [tool index](../README.md) lists every covered tool and explains the
six execution layers.

## Evidence boundary

Tool coverage, local availability, and real execution are different states.

- A folder means OCEAN can route the tool.
- A successful probe means an executable or package was observed.
- A run record means a command or query was executed and recorded.
- Only inspected inputs, parameters, outputs, logs, versions, and environment
  can support a provenance packet.

None of these states alone proves biological mechanism, causality, clinical
utility, benchmark superiority, or publication readiness.

## Database example

Database adapters default to a dry-run packet:

```bash
cd skills/ocean/scripts/tools/databases/uniprot

python3 scripts/query_packet.py \
  --accession P04637 \
  --out outputs/uniprot-reef-packet.json
```

Add `--execute` only for an approved public network call. Inspect the returned
packet before handing it to Reef or Iceberg.

## Bioinformatics example

Probe one lightweight CLI wrapper from its tool folder:

```bash
cd skills/ocean/scripts/tools/bioinformatics/last

python3 scripts/run_cli.py probe \
  --output outputs/last-cli-probe.json
```

An unavailable command is an environment boundary, not a scientific failure.
For an actual run, provide explicit inspected arguments and preserve the
resulting run record and source packet.

## Generated work

Write generated packets, probes, plans, scorecards, and logs to the repository
root `outputs/` directory or another ignored local workspace. Do not commit raw
provider responses, local execution artifacts, credentials, private data, or
internal evaluation logs.
