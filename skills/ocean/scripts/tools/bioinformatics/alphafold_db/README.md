# AlphaFold DB

OCEAN source-packet adapter for AlphaFold DB predicted-structure evidence.

## Scope

- Family: `structure_modeling`
- Current maturity: `L2/L3 source-packet adapter`
- Main script: `source_packet.py`
- Eval script: `run_eval.py`

## What This Adapter Does

- Fetches or imports AlphaFold DB-style metadata, PAE, and mmCIF files.
- Analyzes pLDDT and PAE confidence summaries from inspected files.
- Creates an OCEAN source packet for downstream Iceberg or Anchor review.

## Evidence Boundary

AlphaFold DB output can support bounded predicted-structure confidence statements.

It cannot by itself prove:

- binding;
- experimental function;
- disease mechanism;
- druggability;
- clinical relevance;
- treatment efficacy.

## Example

```bash
python3 source_packet.py analyze \
  --metadata metadata.json \
  --pae pae.json \
  --uniprot P12345 \
  --output analysis.json

python3 source_packet.py packet \
  --analysis analysis.json \
  --output source-packet.json
```

## API / Python Wrapper

- API contract: `api.json`
- Python wrapper: `scripts/create_source_packet.py`
- Example input: `examples/run-record.example.json`

Use the wrapper only after you have inspected a real `AlphaFold DB` run record:

```bash
python3 scripts/create_source_packet.py \
  --input examples/run-record.example.json \
  --output /path/to/alphafold_db-source-packet.json
```

The wrapper converts provenance fields into an OCEAN software source packet. It does not install or execute `AlphaFold DB`.

## Science-skills-style usage guide

See `references/tool_usage.md` for the tool-specific use/avoid rules, required local execution evidence, stop conditions, and OCEAN handoff path.

## Probe / Plan Wrapper

Use `scripts/probe_or_plan.py` to run the bounded per-tool availability probe or to create a launcher/source-packet plan:

```bash
python3 scripts/probe_or_plan.py \
  --output /path/to/alphafold_db-probe-or-plan.json
```

This wrapper records availability or planning evidence only. It does not install the tool, download databases, run biological analyses, benchmark methods, or validate scientific claims.

## Launcher / Workflow Runner Wrapper

Use `scripts/run_launcher.py` to create a bounded non-executing launch/source-packet plan:

```bash
python3 scripts/run_launcher.py plan \
  --output /path/to/alphafold_db-launcher-plan.json
```

This runner does not install software, download references, choose private input files, launch GUI/GPU/HPC jobs, complete workflows, benchmark methods, or validate scientific claims.

