# OCEAN Bioinformatics Workflow Plan: workflow-reproducibility

- Date: 2026-07-05
- Intent: workflow, environment, and container reproducibility plan
- Final handoff: Harbor

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | Conda | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 2 | Docker | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 3 | Singularity-Apptainer | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 4 | Snakemake | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 5 | Nextflow | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 6 | nf-core | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 7 | CWL | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 8 | WDL-Cromwell | workflow_runtime | scripts/tools/common/heavy_tool_launcher.py or workflow run record |
| 9 | Galaxy | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name Conda --tool-slug conda --command-template 'conda <user-supplied arguments>' --output conda-launch-plan.json`
2. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name Docker --tool-slug docker --command-template 'docker <user-supplied arguments>' --output docker-launch-plan.json`
3. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name Singularity-Apptainer --tool-slug singularity_apptainer --command-template 'apptainer <user-supplied arguments>' --output singularity_apptainer-launch-plan.json`
4. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name Snakemake --tool-slug snakemake --command-template 'snakemake <user-supplied arguments>' --output snakemake-launch-plan.json`
5. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name Nextflow --tool-slug nextflow --command-template 'nextflow <user-supplied arguments>' --output nextflow-launch-plan.json`
6. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name nf-core --tool-slug nf_core --command-template 'nf-core <user-supplied arguments>' --output nf_core-launch-plan.json`
7. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name CWL --tool-slug cwl --command-template 'cwltool <user-supplied arguments>' --output cwl-launch-plan.json`
8. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name WDL-Cromwell --tool-slug wdl_cromwell --command-template 'cromwell <user-supplied arguments>' --output wdl_cromwell-launch-plan.json`
9. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name Galaxy --tool-slug galaxy --command-template 'galaxy <user-supplied arguments>' --output galaxy-launch-plan.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
