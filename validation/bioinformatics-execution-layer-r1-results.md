# OCEAN Bioinformatics Execution Layer Eval R1

- Run date: 2026-07-06
- Cases: 24
- Pass: 24
- Needs review: 0
- Executed local probes/packages: 2
- Unavailable in current environment: 15
- Launcher plans created without execution: 7

| Layer | Tool | Status | Verdict |
|---|---|---|---|
| lightweight_cli_subprocess | FastQC | not_available_current_environment | pass |
| lightweight_cli_subprocess | MultiQC | not_available_current_environment | pass |
| lightweight_cli_subprocess | cutadapt | not_available_current_environment | pass |
| lightweight_cli_subprocess | fastp | not_available_current_environment | pass |
| lightweight_cli_subprocess | samtools | not_available_current_environment | pass |
| lightweight_cli_subprocess | bcftools | not_available_current_environment | pass |
| lightweight_cli_subprocess | BEDTools | not_available_current_environment | pass |
| lightweight_cli_subprocess | BLAST | not_available_current_environment | pass |
| lightweight_cli_subprocess | MAFFT | not_available_current_environment | pass |
| lightweight_cli_subprocess | HMMER | not_available_current_environment | pass |
| lightweight_cli_subprocess | minimap2 | not_available_current_environment | pass |
| r_bioconductor_rscript | DESeq2 | executed | pass |
| r_bioconductor_rscript | limma | executed | pass |
| r_bioconductor_rscript | edgeR | not_available_current_environment | pass |
| r_bioconductor_rscript | Seurat | not_available_current_environment | pass |
| r_bioconductor_rscript | WGCNA | not_available_current_environment | pass |
| r_bioconductor_rscript | DADA2 | not_available_current_environment | pass |
| heavy_tool_launcher_plan | Cell Ranger | planned_not_executed | pass |
| heavy_tool_launcher_plan | GATK | planned_not_executed | pass |
| heavy_tool_launcher_plan | AlphaFold | planned_not_executed | pass |
| heavy_tool_launcher_plan | MaxQuant | planned_not_executed | pass |
| heavy_tool_launcher_plan | Galaxy | planned_not_executed | pass |
| heavy_tool_launcher_plan | 3D Slicer | planned_not_executed | pass |
| heavy_tool_launcher_plan | ChimeraX | planned_not_executed | pass |

## Evidence Boundary / 证据边界

This eval checks execution-layer behavior only. It does not install missing tools, download references, run full omics pipelines, process biological or clinical datasets, benchmark software, or validate scientific claims. Unavailable CLI/R tools are environment gaps, not failures of those tools. Heavy-tool cases must remain `planned_not_executed` until the user supplies installation, license, reference/database, compute, and run-record evidence.
