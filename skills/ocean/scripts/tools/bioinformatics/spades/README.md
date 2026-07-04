# SPAdes

OCEAN tool scaffold for `SPAdes`.

## Scope

- Family: `genome_assembly_annotation`
- Current maturity: `L0/L1 scaffold`
- Shared helper: `../../common/software_source_packet.py`

## Evidence Boundary

This folder does not mean OCEAN can run `SPAdes` automatically. It defines where tool-specific wrapper code, examples, and source-packet tests should live.

Before `SPAdes` output can be used as evidence, provide:

- tool version;
- command line or workflow step;
- parameters;
- reference/index/database;
- input files;
- output files;
- logs/QC;
- environment;
- date;
- inspected result fields.

The output cannot by itself prove biological mechanism, causality, clinical utility, reproducibility, or publication readiness.

## API / Python Wrapper

- API contract: `api.json`
- Python wrapper: `scripts/create_source_packet.py`
- Example input: `examples/run-record.example.json`

Use the wrapper only after you have inspected a real `SPAdes` run record:

```bash
python3 scripts/create_source_packet.py \
  --input examples/run-record.example.json \
  --output /path/to/spades-source-packet.json
```

The wrapper converts provenance fields into an OCEAN software source packet. It does not install or execute `SPAdes`.

