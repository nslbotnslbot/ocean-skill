# OCEAN Bioinformatics Workflow Plan: protein-structure

- Date: 2026-07-08
- Intent: protein structure prediction, structure search, and confidence-boundary plan
- Final handoff: Iceberg

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | AlphaFold DB | source_packet_adapter | tool-specific source_packet.py |
| 2 | AlphaFold | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 3 | ColabFold | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 4 | RoseTTAFold | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 5 | HH-suite | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 6 | HMMER | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 7 | MODELLER | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 8 | PyMOL | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 9 | ChimeraX | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/bioinformatics/alphafold_db/source_packet.py --help`
2. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name AlphaFold --tool-slug alphafold --command-template 'alphafold <user-supplied arguments>' --output alphafold-launch-plan.json`
3. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name ColabFold --tool-slug colabfold --command-template 'colabfold <user-supplied arguments>' --output colabfold-launch-plan.json`
4. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name RoseTTAFold --tool-slug rosettafold --command-template 'rosettafold <user-supplied arguments>' --output rosettafold-launch-plan.json`
5. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name HH-suite --tool-slug hh_suite --command hhsearch --probe-args=--version --output hh_suite-probe.json`
6. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name HMMER --tool-slug hmmer --command hmmsearch --probe-args=-h --output hmmer-probe.json`
7. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name MODELLER --tool-slug modeller --command-template 'modeller <user-supplied arguments>' --output modeller-launch-plan.json`
8. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name PyMOL --tool-slug pymol --command-template 'pymol <user-supplied arguments>' --output pymol-launch-plan.json`
9. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name ChimeraX --tool-slug chimerax --command-template 'chimerax <user-supplied arguments>' --output chimerax-launch-plan.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
