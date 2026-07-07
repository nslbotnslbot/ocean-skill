# Open Targets

OCEAN database adapter folder for `opentargets`.

## Scope

- Family: `drug_target`
- Required input: `--ensembl-id`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: target metadata and target-resource provenance.

It cannot by itself support: mechanism, therapeutic efficacy, or clinical readiness from association scores.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --ensembl-id "ENSG00000141510" \
  --out outputs/opentargets-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --ensembl-id "ENSG00000141510" \
  --execute \
  --out outputs/opentargets-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://platform-docs.opentargets.org/data-access

## OCEAN Handoff

Reef -> Iceberg/Compass. Do not treat database presence as primary experimental validation.
