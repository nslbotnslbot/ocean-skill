# AlphaFold DB

OCEAN source-packet adapter for AlphaFold DB predicted-structure evidence.

## Scope

- Family: `structure_modeling`
- Current maturity: `L2/L3 source-packet adapter`
- Main script: `source_packet.py`
- Eval script: `run_eval.py`

## What This Adapter Does

- Fetches or imports AlphaFold DB-style metadata, PAE, and mmCIF files.
- Analyzes pLDDT and PAE confidence summaries from inspected files.
- Creates an OCEAN source packet for downstream Iceberg or Anchor review.

## Evidence Boundary

AlphaFold DB output can support bounded predicted-structure confidence statements.

It cannot by itself prove:

- binding;
- experimental function;
- disease mechanism;
- druggability;
- clinical relevance;
- treatment efficacy.

## Example

```bash
python3 source_packet.py analyze \
  --metadata metadata.json \
  --pae pae.json \
  --uniprot P12345 \
  --output analysis.json

python3 source_packet.py packet \
  --analysis analysis.json \
  --output source-packet.json
```

