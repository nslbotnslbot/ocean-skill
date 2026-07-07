# Europe PMC

OCEAN database adapter folder for `europepmc`.

## Scope

- Family: `literature_metadata`
- Required input: `--query`
- Shared runner: `../../../run_reef_api_adapter.py`
- Entry point: `scripts/query_packet.py`

## What This Adapter Does

- Creates a bounded Reef API/database packet.
- Records query target, official resource family, inspected fields, and evidence boundary.
- Can run in dry-run mode without network access, or in bounded live mode with `--execute`.

## Evidence Boundary

This adapter can support: literature metadata, abstract-level discovery, DOI/PMID/PMCID provenance.

It cannot by itself support: full methods/results quality or publication outcome unless inspected.

## Example

Dry-run query packet:

```bash
python3 scripts/query_packet.py --query "TP53" \
  --out outputs/europepmc-reef-packet.json
```

Bounded live query packet:

```bash
python3 scripts/query_packet.py --query "TP53" \
  --execute \
  --out outputs/europepmc-reef-packet.json
```

## Terms Boundary

Check the source terms before reuse: https://europepmc.org/RestfulWebService

## OCEAN Handoff

Sounding/Reef -> Current/Iceberg. Do not treat database presence as primary experimental validation.
