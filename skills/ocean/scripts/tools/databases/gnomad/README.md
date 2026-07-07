# gnomAD

OCEAN database adapter folder for `gnomad`.

## Scope

- Family: `population_genetics`
- Required input: `--variant-id`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: population-frequency or constraint-resource provenance.

It cannot by itself support: pathogenicity, diagnosis, treatment actionability, or mechanism.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --variant-id "11-5227002-T-A" --gnomad-dataset "gnomad_r4" \
  --out outputs/gnomad-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --variant-id "11-5227002-T-A" --gnomad-dataset "gnomad_r4" \
  --execute \
  --out outputs/gnomad-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://gnomad.broadinstitute.org/help/terms

## OCEAN Handoff

Reef -> Iceberg/Anchor. Do not treat database presence as primary experimental validation.
