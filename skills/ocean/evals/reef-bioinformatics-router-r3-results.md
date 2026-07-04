# OCEAN Reef Bioinformatics Router R3 Results

- Run date: 2026-07-04
- Cases: 12
- Pass: 12
- Needs review: 0
- Mean score: 12.00/12

## Case Summary

| Case | Score | Verdict | Expected routes | Returned routes | Misses |
|---|---:|---|---|---|---|
| R3-REEF-001 | 12/12 | pass | bioinformatics_software | bioinformatics_software, clinical, omics | None |
| R3-REEF-002 | 12/12 | pass | bioinformatics_software | bioinformatics_software, omics | None |
| R3-REEF-003 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R3-REEF-004 | 12/12 | pass | bioinformatics_software, protein_structure | bioinformatics_software, protein_structure | None |
| R3-REEF-005 | 12/12 | pass | bioinformatics_software, omics | bioinformatics_software, omics | None |
| R3-REEF-006 | 12/12 | pass | bioinformatics_software, omics, pathway_gene_set | bioinformatics_software, omics, pathway_gene_set | None |
| R3-REEF-007 | 12/12 | pass | bioinformatics_software, clinical, clinical_imaging_signal | bioinformatics_software, clinical, clinical_imaging_signal | None |
| R3-REEF-008 | 12/12 | pass | benchmark, clinical, clinical_imaging_signal | benchmark, clinical, clinical_imaging_signal | None |
| R3-REEF-009 | 12/12 | pass | benchmark, clinical, clinical_imaging_signal | benchmark, bioinformatics_software, clinical, clinical_imaging_signal | None |
| R3-REEF-010 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R3-REEF-011 | 12/12 | pass | clinical, clinical_imaging_signal | clinical, clinical_imaging_signal | None |
| R3-REEF-012 | 12/12 | pass | bioinformatics_software, omics | bioinformatics_software, epigenomics_regulatory, omics | None |

## Interpretation

- This is a deterministic router eval, not a scientific correctness eval.
- Passing means the local OCEAN router selected expected candidate route classes, kept outputs at `candidate_route`, and attached minimum source-packet fields.
- `needs_review` means the route vocabulary or expected route map should be refined before using the case as a stable regression check.

## Evidence Boundary / 证据边界

This run did not query PubMed, GEO, TCGA/GDC, ClinVar, ChEMBL, ClinicalTrials.gov, OpenFDA, TCIA, PhysioNet, or any external software. It did not run LAST, STAR, SAMtools, DESeq2, Seurat, Snakemake, Nextflow, or other tools. It only tested local routing behavior and evidence-boundary scaffolding.
