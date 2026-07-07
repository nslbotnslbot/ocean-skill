# QuickGO

OCEAN database adapter folder for `quickgo`.

## Scope

- Family: `ontology`
- Required input: `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: GO term metadata and annotation-resource provenance.

It cannot by itself support: direct molecular mechanism, causality, or phenotype proof.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --query "apoptosis" \
  --out outputs/quickgo-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --query "apoptosis" \
  --execute \
  --out outputs/quickgo-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://www.ebi.ac.uk/QuickGO/api/index.html

## OCEAN Handoff

Reef -> Iceberg/Harbor. Do not treat database presence as primary experimental validation.
