# Reactome

OCEAN database adapter folder for `reactome`.

## Scope

- Family: `pathway`
- Required input: `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: pathway/resource discovery and pathway-context provenance.

It cannot by itself support: pathway activity, causal disease mechanism, or treatment effect.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --query "TP53" --species-name "Homo sapiens" \
  --out outputs/reactome-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --query "TP53" --species-name "Homo sapiens" \
  --execute \
  --out outputs/reactome-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://reactome.org/license

## OCEAN Handoff

Reef -> Iceberg/Compass. Do not treat database presence as primary experimental validation.
