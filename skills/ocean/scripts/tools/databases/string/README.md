# STRING

OCEAN database adapter folder for `string`.

## Scope

- Family: `protein_interaction`
- Required input: `--identifier` or `--query`, plus explicit `--species`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: identifier mapping and protein association-resource provenance.

It cannot by itself support: direct physical binding, mechanism, causality, or disease relevance.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --identifier "TP53" --species 9606 \
  --out outputs/string-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --identifier "TP53" --species 9606 \
  --execute \
  --out outputs/string-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://string-db.org/cgi/access

## OCEAN Handoff

Reef -> Iceberg/Compass. Do not treat database presence as primary experimental validation.
