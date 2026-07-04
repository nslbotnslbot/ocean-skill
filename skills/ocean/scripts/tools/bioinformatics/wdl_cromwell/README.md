# WDL-Cromwell

OCEAN tool scaffold for `WDL-Cromwell`.

## Scope

- Family: `workflow_reproducibility`
- Current maturity: `L0/L1 scaffold`
- Shared helper: `../../common/software_source_packet.py`

## Evidence Boundary

This folder does not mean OCEAN can run `WDL-Cromwell` automatically. It defines where tool-specific wrapper code, examples, and source-packet tests should live.

Before `WDL-Cromwell` output can be used as evidence, provide:

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

Use the wrapper only after you have inspected a real `WDL-Cromwell` run record:

```bash
python3 scripts/create_source_packet.py \
  --input examples/run-record.example.json \
  --output /path/to/wdl_cromwell-source-packet.json
```

The wrapper converts provenance fields into an OCEAN software source packet. It does not install or execute `WDL-Cromwell`.

## Science-skills-style usage guide

See `references/tool_usage.md` for the tool-specific use/avoid rules, required local execution evidence, stop conditions, and OCEAN handoff path.

