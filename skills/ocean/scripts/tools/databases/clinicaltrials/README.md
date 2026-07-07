# ClinicalTrials.gov

OCEAN database adapter folder for `clinicaltrials`.

## Scope

- Family: `clinical_registry`
- Required input: `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: trial registration, status, design, and registry-field provenance.

It cannot by itself support: treatment efficacy, safety superiority, or clinical guidance.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --query "melanoma" \
  --out outputs/clinicaltrials-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --query "melanoma" \
  --execute \
  --out outputs/clinicaltrials-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://clinicaltrials.gov/data-api/about-api

## OCEAN Handoff

Reef -> Iceberg/Anchor/Compass. Do not treat database presence as primary experimental validation.
