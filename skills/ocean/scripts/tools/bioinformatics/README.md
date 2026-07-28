# Bioinformatics Tool Wrappers

[All OCEAN tools](../../README.md) |
[中文工具总览](../../README.zh-CN.md)

This directory contains 115 tool-specific folders covering common
bioinformatics, computational biology, omics, imaging, and workflow tasks.

The complete grouped list is in the parent [tool index](../../README.md).

## Per-tool contract

Each tool folder contains:

- `tool.json`: scientific family and evidence boundary;
- `api.json`: stable command descriptions;
- `wrapper_config.json`: execution-layer routing;
- `examples/run-record.example.json`: provenance template;
- `references/tool_usage.md`: use, avoid, stop, and handoff rules;
- `scripts/create_source_packet.py`: convert an inspected run record;
- `scripts/probe_or_plan.py`: bounded availability probe or execution plan;
- an execution-layer runner when appropriate.

## Execution layers

| Layer | Behavior |
|---|---|
| `lightweight_cli` | Probe a local command or record explicit user-supplied arguments |
| `python_package` | Probe a Python import or record an inspected Python script |
| `r_bioconductor` | Probe an R package or record an inspected R script |
| `heavy_launcher_plan` | Create a non-executing environment and evidence plan |
| `workflow_runtime` | Probe a workflow runtime or record an explicit invocation |
| `source_packet_adapter` | Inspect bounded source files and create a packet |

These wrappers do not install software, download databases, choose private
inputs, design an analysis, or validate scientific conclusions.

## One entry point

From the repository root, use the router instead of browsing 115 folders:

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools --search rna
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py profile --tool deseq2
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-workflows
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  workflow \
  --workflow rna-seq-differential-expression \
  --output outputs/rna-seq-plan.json
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  check \
  --tool deseq2 \
  --output outputs/deseq2-check.json
```

`check` records current availability for CLI/package/workflow tools and creates
a non-executing plan for heavy tools. It never installs software or processes a
private dataset automatically.

## Probe a tool

From a tool folder:

```bash
python3 scripts/probe_or_plan.py \
  --output outputs/tool-probe-or-plan.json
```

For a lightweight CLI:

```bash
python3 scripts/run_cli.py probe \
  --output outputs/tool-cli-probe.json
```

For a Python or R package:

```bash
python3 scripts/run_package.py probe \
  --output outputs/tool-package-probe.json
```

For a heavy tool or workflow:

```bash
python3 scripts/run_launcher.py plan \
  --output outputs/tool-launcher-plan.json
```

The exact runner depends on `wrapper_config.json`. A missing runner usually
means that execution layer is not appropriate for that tool.

## Record an actual run

Only use a run command when inputs and arguments are explicitly supplied and
approved. Preserve:

- tool name and version;
- exact command or script;
- parameters;
- input and output manifests;
- reference database or index;
- logs and QC;
- environment and date;
- return code and relevant stdout/stderr.

Then create a source packet and route it through Reef for provenance, Iceberg
for claim support, or Anchor for validation and reproducibility.

## Safety

A successful command does not establish mechanism, causality, clinical
benefit, or publication readiness. Generated files belong in ignored
`outputs/`; never commit private data, credentials, local paths, or raw
execution logs.
