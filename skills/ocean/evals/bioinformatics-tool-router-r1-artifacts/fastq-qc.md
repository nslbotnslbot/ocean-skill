# OCEAN Bioinformatics Workflow Plan: fastq-qc

- Date: 2026-07-05
- Intent: raw FASTQ quality control and preprocessing evidence plan
- Final handoff: Anchor

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | FastQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 2 | fastp | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 3 | cutadapt | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | MultiQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name FastQC --tool-slug fastqc --command fastqc --probe-args=--version --output fastqc-probe.json`
2. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name fastp --tool-slug fastp --command fastp --probe-args=--version --output fastp-probe.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name cutadapt --tool-slug cutadapt --command cutadapt --probe-args=--version --output cutadapt-probe.json`
4. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MultiQC --tool-slug multiqc --command multiqc --probe-args=--version --output multiqc-probe.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
