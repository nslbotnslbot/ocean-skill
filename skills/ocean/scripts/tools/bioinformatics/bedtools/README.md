# BEDTools

OCEAN tool scaffold for `BEDTools`.

## Scope

- Family: `alignment_file_operations`
- Current maturity: `L0/L1 scaffold`
- Shared helper: `../../common/software_source_packet.py`

## Evidence Boundary

This folder does not mean OCEAN can run `BEDTools` automatically. It defines where tool-specific wrapper code, examples, and source-packet tests should live.

Before `BEDTools` output can be used as evidence, provide:

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
