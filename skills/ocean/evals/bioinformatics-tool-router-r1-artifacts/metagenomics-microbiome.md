# OCEAN Bioinformatics Workflow Plan: metagenomics-microbiome

- Date: 2026-07-08
- Intent: microbiome/metagenomics QC, profiling, and compositional-analysis evidence plan
- Final handoff: Iceberg

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | FastQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 2 | MultiQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 3 | Kraken2 | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | Bracken | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 5 | MetaPhlAn | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 6 | HUMAnN | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 7 | QIIME2 | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 8 | DADA2 | r_bioconductor | scripts/tools/common/rscript_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name FastQC --tool-slug fastqc --command fastqc --probe-args=--version --output fastqc-probe.json`
2. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MultiQC --tool-slug multiqc --command multiqc --probe-args=--version --output multiqc-probe.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Kraken2 --tool-slug kraken2 --command kraken2 --probe-args=--version --output kraken2-probe.json`
4. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Bracken --tool-slug bracken --command bracken --probe-args=--version --output bracken-probe.json`
5. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MetaPhlAn --tool-slug metaphlan --command metaphlan --probe-args=--version --output metaphlan-probe.json`
6. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name HUMAnN --tool-slug humann --command humann --probe-args=--version --output humann-probe.json`
7. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name QIIME2 --tool-slug qiime2 --command qiime --probe-args=--version --output qiime2-probe.json`
8. `python3 skills/ocean/scripts/tools/common/rscript_wrapper.py check-package --tool-name DADA2 --tool-slug dada2 --package dada2 --output dada2-rscript-check.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
