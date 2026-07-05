# OCEAN Bioinformatics Workflow Plan: rna-seq-differential-expression

- Date: 2026-07-05
- Intent: bulk RNA-seq QC, alignment/quantification, and differential-expression evidence plan
- Final handoff: Iceberg

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | FastQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 2 | MultiQC | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 3 | STAR | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | Salmon | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 5 | featureCounts | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 6 | DESeq2 | r_bioconductor | scripts/tools/common/rscript_wrapper.py |
| 7 | limma-voom | r_bioconductor | scripts/tools/common/rscript_wrapper.py |
| 8 | edgeR | r_bioconductor | scripts/tools/common/rscript_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name FastQC --tool-slug fastqc --command fastqc --probe-args=--version --output fastqc-probe.json`
2. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MultiQC --tool-slug multiqc --command multiqc --probe-args=--version --output multiqc-probe.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name STAR --tool-slug star --command STAR --probe-args=--version --output star-probe.json`
4. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Salmon --tool-slug salmon --command salmon --probe-args=--version --output salmon-probe.json`
5. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name featureCounts --tool-slug featurecounts --command featureCounts --probe-args=--version --output featurecounts-probe.json`
6. `python3 skills/ocean/scripts/tools/common/rscript_wrapper.py check-package --tool-name DESeq2 --tool-slug deseq2 --package DESeq2 --output deseq2-rscript-check.json`
7. `python3 skills/ocean/scripts/tools/common/rscript_wrapper.py check-package --tool-name limma-voom --tool-slug limma_voom --package limma --output limma_voom-rscript-check.json`
8. `python3 skills/ocean/scripts/tools/common/rscript_wrapper.py check-package --tool-name edgeR --tool-slug edger --package edgeR --output edger-rscript-check.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
