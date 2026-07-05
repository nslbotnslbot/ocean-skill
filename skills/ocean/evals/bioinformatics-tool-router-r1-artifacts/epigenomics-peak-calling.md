# OCEAN Bioinformatics Workflow Plan: epigenomics-peak-calling

- Date: 2026-07-05
- Intent: epigenomic alignment, peak-calling, motif, and signal-track provenance plan
- Final handoff: Iceberg

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | FastQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 2 | MultiQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 3 | Bowtie2 | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | SAMtools | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 5 | BEDTools | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 6 | MACS2 | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 7 | MACS3 | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 8 | HOMER | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 9 | deepTools | python_package | scripts/tools/common/software_source_packet.py plus Python import/run record |
| 10 | FIMO | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 11 | MEME | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name FastQC --tool-slug fastqc --command fastqc --probe-args=--version --output fastqc-probe.json`
2. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MultiQC --tool-slug multiqc --command multiqc --probe-args=--version --output multiqc-probe.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Bowtie2 --tool-slug bowtie2 --command bowtie2 --probe-args=--version --output bowtie2-probe.json`
4. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name SAMtools --tool-slug samtools --command samtools --probe-args=--version --output samtools-probe.json`
5. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name BEDTools --tool-slug bedtools --command bedtools --probe-args=--version --output bedtools-probe.json`
6. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MACS2 --tool-slug macs2 --command macs2 --probe-args=--version --output macs2-probe.json`
7. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MACS3 --tool-slug macs3 --command macs3 --probe-args=--version --output macs3-probe.json`
8. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name HOMER --tool-slug homer --command findMotifsGenome.pl --probe-args=--version --output homer-probe.json`
9. `python3 skills/ocean/scripts/tools/common/software_source_packet.py template --tool-name deepTools --tool-slug deeptools --output deeptools-run-record.template.json`
10. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name FIMO --tool-slug fimo --command fimo --probe-args=--version --output fimo-probe.json`
11. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MEME --tool-slug meme --command meme --probe-args=--version --output meme-probe.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
