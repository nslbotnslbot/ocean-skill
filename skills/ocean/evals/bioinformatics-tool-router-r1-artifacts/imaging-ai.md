# OCEAN Bioinformatics Workflow Plan: imaging-ai

- Date: 2026-07-08
- Intent: medical/biological imaging annotation, segmentation, and ML workflow provenance plan
- Final handoff: Anchor

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | 3D Slicer | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 2 | ITK-SNAP | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 3 | SimpleITK | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 4 | TorchIO | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 5 | MONAI | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 6 | nnU-Net | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name '3D Slicer' --tool-slug three_d_slicer --command-template 'three-d-slicer <user-supplied arguments>' --output three_d_slicer-launch-plan.json`
2. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name ITK-SNAP --tool-slug itk_snap --command-template 'itk-snap <user-supplied arguments>' --output itk_snap-launch-plan.json`
3. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name SimpleITK --tool-slug simpleitk --output simpleitk-run-record.template.json`
4. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name TorchIO --tool-slug torchio --output torchio-run-record.template.json`
5. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name MONAI --tool-slug monai --output monai-run-record.template.json`
6. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name nnU-Net --tool-slug nnu_net --command-template 'nnu-net <user-supplied arguments>' --output nnu_net-launch-plan.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
