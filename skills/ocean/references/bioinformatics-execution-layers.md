# Bioinformatics Execution Layers

OCEAN routes each covered tool through one of six bounded layers. The layer
describes what the wrapper may do; it does not state that the tool is installed
or that an analysis has run.

| Layer | Public behavior | Required before scientific use |
|---|---|---|
| `lightweight_cli` | Probe a local executable; run only explicit user-supplied argument lists | Version, command, parameters, inputs, outputs, references, logs, environment |
| `python_package` | Probe a Python import; run only an explicit user-supplied script | Package version, script, parameters, inputs/outputs, environment, logs |
| `r_bioconductor` | Probe `Rscript` and package version; run only an explicit R script | R/package versions, script, design/contrast, inputs/outputs, session information |
| `workflow_runtime` | Probe a workflow/container runtime; run only explicit runtime arguments | Workflow definition, lock/container, backend, inputs/outputs, logs, resume/cache state |
| `heavy_launcher_plan` | Create a non-executing environment and asset plan | License/terms, compute, database/index, command, inputs, logs, exported results |
| `source_packet_adapter` | Inspect bounded source files or adapter inputs | Identifiers/files, inspected fields, confidence metadata, source limitations |

## Safe Entry Point

Prefer the unified router:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  profile --tool deseq2

python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  check --tool deseq2 --output outputs/deseq2-check.json
```

Tool-specific runners remain available under:

`scripts/tools/bioinformatics/<tool>/scripts/`

- `run_cli.py`
- `run_package.py`
- `run_launcher.py`
- `probe_or_plan.py`
- `create_source_packet.py`

The applicable files depend on the tool's execution layer.

## Execution Rules

- Use argument lists with `subprocess.run`; never build a shell command from
  untrusted input.
- Never install tools, download databases, or upload private data
  automatically.
- A version/help probe is availability evidence, not an analysis.
- A successful command is not sufficient without inputs, parameters,
  references, outputs, logs, and environment provenance.
- GUI, licensed, GPU, and large-database tools require an explicit local plan
  and user approval.
- Create a source packet only from inspected run records or source-specific
  adapter outputs.

## Handoff

- Reef: tool/resource selection and provenance.
- Iceberg: whether the inspected output supports a claim.
- Anchor: validation, leakage, reproducibility, benchmark, and replication.
- Harbor: unresolved environment or provenance debt.
