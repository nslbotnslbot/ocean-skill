# ChEMBL

OCEAN database adapter folder for `chembl`.

## Scope

- Family: `drug_target`
- Required input: `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: compound/target/assay metadata and ChEMBL identifier provenance.

It cannot by itself support: therapeutic efficacy, safety, mechanism, or clinical readiness.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --query "aspirin" \
  --out outputs/chembl-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --query "aspirin" \
  --execute \
  --out outputs/chembl-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://chembl.gitbook.io/chembl-interface-documentation/about

## OCEAN Handoff

Reef -> Iceberg/Compass. Do not treat database presence as primary experimental validation.
