# HOMER

OCEAN tool scaffold for `HOMER`.

## Scope

- Family: `epigenomics_peak_calling`
- Current maturity: `L0/L1 scaffold`
- Shared helper: `../../common/software_source_packet.py`

## Evidence Boundary

This folder does not mean OCEAN can run `HOMER` automatically. It defines where tool-specific wrapper code, examples, and source-packet tests should live.

Before `HOMER` output can be used as evidence, provide:

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
