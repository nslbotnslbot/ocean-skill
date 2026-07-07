# UniProt

OCEAN database adapter folder for `uniprot`.

## Scope

- Family: `protein_annotation`
- Required input: `--accession` or `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: protein accession, reviewed/unreviewed status, sequence/function annotation provenance.

It cannot by itself support: new function, mechanism, causality, or clinical utility without primary evidence.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --accession "P04637" \
  --out outputs/uniprot-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --accession "P04637" \
  --execute \
  --out outputs/uniprot-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://www.uniprot.org/help/license

## OCEAN Handoff

Reef -> Iceberg/Anchor. Do not treat database presence as primary experimental validation.
