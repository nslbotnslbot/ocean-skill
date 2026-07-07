# OCEAN Bioinformatics Launcher / Workflow Runner Eval R1

- Run date: 2026-07-08
- Launcher tools checked: 29
- Runtime probes checked: 8
- Checks: 37
- Pass: 37
- Needs review: 0

## Execution Status Counts

| Status | Count |
|---|---:|
| not_available_current_environment | 8 |
| planned_not_executed | 29 |

## Results

| Tool | Layer | Mode | Status | Verdict | Issues |
|---|---|---|---|---|---|
| AlphaFold | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| AlphaFold DB | source_packet_adapter | launcher-plan | planned_not_executed | pass |  |
| Cell Ranger | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| ChimeraX | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| ColabFold | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| Conda | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| Conda | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |
| CWL | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| CWL | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |
| DeepVariant | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| Docker | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| Docker | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |
| FragPipe | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| Galaxy | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| GATK | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| ITK-SNAP | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| MaxQuant | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| MODELLER | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| MS-DIAL | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| Mutect2 | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| MZmine | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| Nextflow | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| Nextflow | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |
| nf-core | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| nf-core | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |
| nnU-Net | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| PyMOL | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| RoseTTAFold | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| Singularity-Apptainer | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| Singularity-Apptainer | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |
| Skyline | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| Snakemake | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| Snakemake | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |
| Space Ranger | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| 3D Slicer | heavy_launcher_plan | launcher-plan | planned_not_executed | pass |  |
| WDL-Cromwell | workflow_runtime | launcher-plan | planned_not_executed | pass |  |
| WDL-Cromwell | workflow_runtime | runtime-probe | not_available_current_environment | pass |  |

## Evidence Boundary / 证据边界

Launcher plans are non-executing records for heavy, GUI, GPU, licensed, source-packet-adapter, or workflow tools. Runtime probes only check whether a workflow runtime command is locally available. This eval does not install software, download references, run workflows, process biological data, benchmark methods, or validate scientific claims.
