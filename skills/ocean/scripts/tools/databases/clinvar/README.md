# ClinVar

OCEAN database adapter folder for `clinvar`.

## Scope

- Family: `variant_clinical_annotation`
- Required input: `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: ClinVar record discovery and clinical-assertion metadata provenance.

It cannot by itself support: diagnosis, treatment guidance, or pathogenicity without inspected details.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --query "BRCA1" \
  --out outputs/clinvar-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --query "BRCA1" \
  --execute \
  --out outputs/clinvar-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://www.ncbi.nlm.nih.gov/clinvar/

## OCEAN Handoff

Reef -> Iceberg/Anchor. Do not treat database presence as primary experimental validation.
