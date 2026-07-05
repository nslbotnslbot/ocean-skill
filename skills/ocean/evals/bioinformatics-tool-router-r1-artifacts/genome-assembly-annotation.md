# OCEAN Bioinformatics Workflow Plan: genome-assembly-annotation

- Date: 2026-07-05
- Intent: genome assembly, assembly QC, and annotation provenance plan
- Final handoff: Anchor

| Step | Tool | Layer | Wrapper |
|---:|---|---|---|
| 1 | Flye | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 2 | Canu | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 3 | Raven | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 4 | SPAdes | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 5 | MEGAHIT | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 6 | QUAST | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 7 | BUSCO | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 8 | Bakta | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 9 | Prokka | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 10 | eggNOG-mapper | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |
| 11 | InterProScan | lightweight_cli | scripts/tools/common/cli_subprocess_wrapper.py |

## Wrapper Commands

1. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Flye --tool-slug flye --command flye --probe-args=--version --output flye-probe.json`
2. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Canu --tool-slug canu --command canu --probe-args=--version --output canu-probe.json`
3. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Raven --tool-slug raven --command raven --probe-args=--version --output raven-probe.json`
4. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name SPAdes --tool-slug spades --command spades.py --probe-args=--version --output spades-probe.json`
5. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name MEGAHIT --tool-slug megahit --command megahit --probe-args=--version --output megahit-probe.json`
6. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name QUAST --tool-slug quast --command quast.py --probe-args=--version --output quast-probe.json`
7. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name BUSCO --tool-slug busco --command busco --probe-args=--version --output busco-probe.json`
8. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Bakta --tool-slug bakta --command bakta --probe-args=--version --output bakta-probe.json`
9. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name Prokka --tool-slug prokka --command prokka --probe-args=--version --output prokka-probe.json`
10. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name eggNOG-mapper --tool-slug eggnog_mapper --command emapper.py --probe-args=--version --output eggnog_mapper-probe.json`
11. `python3 skills/ocean/scripts/tools/common/cli_subprocess_wrapper.py probe --tool-name InterProScan --tool-slug interproscan --command interproscan.sh --probe-args=--version --output interproscan-probe.json`

## Negative Space

- No tool execution has happened from this plan alone.
- No reference database/index has been inspected unless a run record says so.
- No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.

## Evidence Boundary

Workflow plan only; execute tools locally and inspect run records before making scientific claims.
