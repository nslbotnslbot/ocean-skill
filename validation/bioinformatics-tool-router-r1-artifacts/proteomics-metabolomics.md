# OCEAN Bioinformatics Workflow Plan: proteomics-metabolomics

- Date: 2026-07-08
- Intent: proteomics/metabolomics search, quantification, and feature-detection provenance plan
- Final handoff: Anchor

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | MaxQuant | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 2 | FragPipe | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 3 | DIA-NN | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | Skyline | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 5 | MS-DIAL | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 6 | MZmine | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 7 | XCMS | r_bioconductor | scripts/tools/common/rscript_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name MaxQuant --tool-slug maxquant --command-template 'maxquant <user-supplied arguments>' --output maxquant-launch-plan.json`
2. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name FragPipe --tool-slug fragpipe --command-template 'fragpipe <user-supplied arguments>' --output fragpipe-launch-plan.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name DIA-NN --tool-slug dia_nn --command diann --probe-args=--version --output dia_nn-probe.json`
4. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name Skyline --tool-slug skyline --command-template 'skyline <user-supplied arguments>' --output skyline-launch-plan.json`
5. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name MS-DIAL --tool-slug ms_dial --command-template 'ms-dial <user-supplied arguments>' --output ms_dial-launch-plan.json`
6. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name MZmine --tool-slug mzmine --command-template 'mzmine <user-supplied arguments>' --output mzmine-launch-plan.json`
7. `python3 skills/ocean/scripts/tools/common/rscript_wrapper.py check-package --tool-name XCMS --tool-slug xcms --package xcms --output xcms-rscript-check.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
