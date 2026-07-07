# NCBI E-utilities

OCEAN database adapter folder for `ncbi-eutils`.

## Scope

- Family: `entrez_metadata`
- Required input: `--database` and `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: Entrez record discovery and public metadata retrieval planning.

It cannot by itself support: full evidence, mechanism, causality, or absence-of-evidence claims.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --database "gene" --query "TP53" \
  --out outputs/ncbi_eutils-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --database "gene" --query "TP53" \
  --execute \
  --out outputs/ncbi_eutils-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://www.ncbi.nlm.nih.gov/books/NBK25501/

## OCEAN Handoff

Reef -> Sounding/Iceberg/Harbor. Do not treat database presence as primary experimental validation.
