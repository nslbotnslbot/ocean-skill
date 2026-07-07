# MAFFT

OCEAN tool scaffold for `MAFFT`.

## Scope

- Family: `phylogenetics_comparative_genomics`
- Current maturity: `L0/L1 scaffold`
- Shared helper: `../../common/software_source_packet.py`

## Evidence Boundary

This folder does not mean OCEAN can run `MAFFT` automatically. It defines where tool-specific wrapper code, examples, and source-packet tests should live.

Before `MAFFT` output can be used as evidence, provide:

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

Use the wrapper only after you have inspected a real `MAFFT` run record:

```bash
python3 scripts/create_source_packet.py \
  --input examples/run-record.example.json \
  --output /path/to/mafft-source-packet.json
```

The wrapper converts provenance fields into an OCEAN software source packet. It does not install or execute `MAFFT`.

## Science-skills-style usage guide

See `references/tool_usage.md` for the tool-specific use/avoid rules, required local execution evidence, stop conditions, and OCEAN handoff path.

## Probe / Plan Wrapper

Use `scripts/probe_or_plan.py` to run the bounded per-tool availability probe or to create a launcher/source-packet plan:

```bash
python3 scripts/probe_or_plan.py \
  --output /path/to/mafft-probe-or-plan.json
```

This wrapper records availability or planning evidence only. It does not install the tool, download databases, run biological analyses, benchmark methods, or validate scientific claims.

