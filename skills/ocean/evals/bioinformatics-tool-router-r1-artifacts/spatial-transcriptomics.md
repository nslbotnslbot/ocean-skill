# OCEAN Bioinformatics Workflow Plan: spatial-transcriptomics

- Date: 2026-07-05
- Intent: spatial transcriptomics alignment, annotation, deconvolution, and mapping plan
- Final handoff: Iceberg

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | Space Ranger | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 2 | Squidpy | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 3 | stLearn | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 4 | cell2location | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 5 | Tangram | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 6 | Stereoscope | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 7 | Giotto | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name 'Space Ranger' --tool-slug space_ranger --command-template 'space-ranger <user-supplied arguments>' --output space_ranger-launch-plan.json`
2. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name Squidpy --tool-slug squidpy --output squidpy-run-record.template.json`
3. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name stLearn --tool-slug stlearn --output stlearn-run-record.template.json`
4. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name cell2location --tool-slug cell2location --output cell2location-run-record.template.json`
5. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name Tangram --tool-slug tangram --output tangram-run-record.template.json`
6. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name Stereoscope --tool-slug stereoscope --output stereoscope-run-record.template.json`
7. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name Giotto --tool-slug giotto --output giotto-run-record.template.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
