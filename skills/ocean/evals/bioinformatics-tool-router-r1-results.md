# OCEAN Bioinformatics Tool Router Eval R1

- Run date: 2026-07-08
- Cases: 133
- Pass: 133
- Needs review: 0
- Tools profiled: 115
- Workflows planned: 12

## Execution Layer Coverage

| Layer | Count |
|---|---:|
| heavy_launcher_plan | 20 |
| lightweight_cli | 60 |
| python_package | 16 |
| r_bioconductor | 10 |
| source_packet_adapter | 1 |
| workflow_runtime | 8 |

## Workflow Cases

| Workflow | Verdict | Notes |
|---|---|---|
| fastq-qc | pass | {
  "workflow": "fastq-qc",
  "steps": 4,
  "missing": []
}
 |
| rna-seq-differential-expression | pass | {
  "workflow": "rna-seq-differential-expression",
  "steps": 8,
  "missing": []
}
 |
| variant-calling-qc | pass | {
  "workflow": "variant-calling-qc",
  "steps": 8,
  "missing": []
}
 |
| single-cell-rna-seq | pass | {
  "workflow": "single-cell-rna-seq",
  "steps": 8,
  "missing": []
}
 |
| spatial-transcriptomics | pass | {
  "workflow": "spatial-transcriptomics",
  "steps": 7,
  "missing": []
}
 |
| metagenomics-microbiome | pass | {
  "workflow": "metagenomics-microbiome",
  "steps": 8,
  "missing": []
}
 |
| genome-assembly-annotation | pass | {
  "workflow": "genome-assembly-annotation",
  "steps": 11,
  "missing": []
}
 |
| protein-structure | pass | {
  "workflow": "protein-structure",
  "steps": 9,
  "missing": []
}
 |
| epigenomics-peak-calling | pass | {
  "workflow": "epigenomics-peak-calling",
  "steps": 11,
  "missing": []
}
 |
| proteomics-metabolomics | pass | {
  "workflow": "proteomics-metabolomics",
  "steps": 7,
  "missing": []
}
 |
| workflow-reproducibility | pass | {
  "workflow": "workflow-reproducibility",
  "steps": 9,
  "missing": []
}
 |
| imaging-ai | pass | {
  "workflow": "imaging-ai",
  "steps": 6,
  "missing": []
}
 |

## Evidence Boundary / 证据边界

This eval checks routing/profile/workflow-plan behavior only. It does not install or run external bioinformatics tools, download references, process biological/clinical data, benchmark methods, or validate scientific claims.
