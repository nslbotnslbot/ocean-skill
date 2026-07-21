# OCEAN Bioinformatics Workflow Plan: single-cell-rna-seq

- Date: 2026-07-08
- Intent: single-cell RNA-seq preprocessing, annotation, and latent-model provenance plan
- Final handoff: Iceberg

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | Cell Ranger | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 2 | Alevin-fry | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 3 | STARsolo | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | Scanpy | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 5 | Seurat | r_bioconductor | scripts/tools/common/rscript_wrapper.py |
| 6 | scVI | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 7 | CellTypist | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 8 | Azimuth | r_bioconductor | scripts/tools/common/rscript_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name 'Cell Ranger' --tool-slug cell_ranger --command-template 'cell-ranger <user-supplied arguments>' --output cell_ranger-launch-plan.json`
2. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Alevin-fry --tool-slug alevin_fry --command alevin-fry --probe-args=--version --output alevin_fry-probe.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name STARsolo --tool-slug starsolo --command STAR --probe-args=--version --output starsolo-probe.json`
4. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name Scanpy --tool-slug scanpy --output scanpy-run-record.template.json`
5. `python3 skills/ocean/scripts/tools/common/rscript_wrapper.py check-package --tool-name Seurat --tool-slug seurat --package Seurat --output seurat-rscript-check.json`
6. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name scVI --tool-slug scvi --output scvi-run-record.template.json`
7. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name CellTypist --tool-slug celltypist --output celltypist-run-record.template.json`
8. `python3 skills/ocean/scripts/tools/common/rscript_wrapper.py check-package --tool-name Azimuth --tool-slug azimuth --package Azimuth --output azimuth-rscript-check.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
