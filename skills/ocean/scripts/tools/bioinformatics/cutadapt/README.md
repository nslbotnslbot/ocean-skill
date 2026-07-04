# cutadapt

OCEAN tool scaffold for `cutadapt`.

## Scope

- Family: `qc_preprocessing`
- Current maturity: `L0/L1 scaffold`
- Shared helper: `../../common/software_source_packet.py`

## Evidence Boundary

This folder does not mean OCEAN can run `cutadapt` automatically. It defines where tool-specific wrapper code, examples, and source-packet tests should live.

Before `cutadapt` output can be used as evidence, provide:

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
