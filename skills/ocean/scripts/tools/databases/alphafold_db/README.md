# AlphaFold DB

OCEAN database adapter folder for `alphafold-db`.

## Scope

- Family: `structure_modeling`
- Required input: `--accession` or `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: predicted-structure metadata provenance by UniProt accession.

It cannot by itself support: experimental structure proof, binding, druggability, or function.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --accession "P04637" \
  --out outputs/alphafold_db-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --accession "P04637" \
  --execute \
  --out outputs/alphafold_db-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://alphafold.ebi.ac.uk/api-docs

## OCEAN Handoff

Reef -> Iceberg/Anchor. Do not treat database presence as primary experimental validation.
