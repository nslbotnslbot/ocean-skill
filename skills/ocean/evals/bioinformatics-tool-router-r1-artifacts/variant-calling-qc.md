# OCEAN Bioinformatics Workflow Plan: variant-calling-qc

- Date: 2026-07-05
- Intent: variant calling, file-operation, and QC provenance plan
- Final handoff: Anchor

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | BWA | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 2 | SAMtools | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 3 | bcftools | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | GATK | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 5 | FreeBayes | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 6 | Strelka2 | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 7 | DeepVariant | heavy_launcher_plan | scripts/tools/common/heavy_tool_launcher.py |
| 8 | Picard | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name BWA --tool-slug bwa --command bwa --probe-args=--version --output bwa-probe.json`
2. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name SAMtools --tool-slug samtools --command samtools --probe-args=--version --output samtools-probe.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name bcftools --tool-slug bcftools --command bcftools --probe-args=--version --output bcftools-probe.json`
4. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name GATK --tool-slug gatk --command-template 'gatk <user-supplied arguments>' --output gatk-launch-plan.json`
5. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name FreeBayes --tool-slug freebayes --command freebayes --probe-args=--version --output freebayes-probe.json`
6. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Strelka2 --tool-slug strelka2 --command configureStrelkaGermlineWorkflow.py --probe-args=--help --output strelka2-probe.json`
7. `python3 skills/ocean/scripts/tools/common/heavy_tool_launcher.py plan --tool-name DeepVariant --tool-slug deepvariant --command-template 'deepvariant <user-supplied arguments>' --output deepvariant-launch-plan.json`
8. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Picard --tool-slug picard --command picard --probe-args=--version --output picard-probe.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
