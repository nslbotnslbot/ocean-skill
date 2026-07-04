# OCEAN Reef Bioinformatics Router R4 Results

- Run date: 2026-07-04
- Cases: 20
- Pass: 20
- Needs review: 0
- Mean score: 11.95/12

## Case Summary

| Case | Score | Verdict | Expected routes | Returned routes | Misses |
|---|---:|---|---|---|---|
| R4-REEF-001 | 12/12 | pass | bioinformatics_software, protein_structure | bioinformatics_software, protein_structure | None |
| R4-REEF-002 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R4-REEF-003 | 12/12 | pass | bioinformatics_software, variant_genetics | bioinformatics_software, variant_genetics | None |
| R4-REEF-004 | 12/12 | pass | bioinformatics_software, clinical, variant_genetics | bioinformatics_software, clinical, variant_genetics | None |
| R4-REEF-005 | 12/12 | pass | bioinformatics_software, variant_genetics | bioinformatics_software, variant_genetics | None |
| R4-REEF-006 | 12/12 | pass | bioinformatics_software, omics, pathway_gene_set | bioinformatics_software, omics, pathway_gene_set | None |
| R4-REEF-007 | 12/12 | pass | bioinformatics_software, omics | bioinformatics_software, omics | None |
| R4-REEF-008 | 12/12 | pass | bioinformatics_software, omics | bioinformatics_software, omics | None |
| R4-REEF-009 | 11/12 | pass | bioinformatics_software, omics | bioinformatics_software, omics | bayspace |
| R4-REEF-010 | 12/12 | pass | bioinformatics_software, epigenomics_regulatory | bioinformatics_software, epigenomics_regulatory | None |
| R4-REEF-011 | 12/12 | pass | bioinformatics_software | bioinformatics_software, clinical_imaging_signal | None |
| R4-REEF-012 | 12/12 | pass | bioinformatics_software, microbiome | bioinformatics_software, clinical, microbiome | None |
| R4-REEF-013 | 12/12 | pass | bioinformatics_software, clinical, proteomics_metabolomics | bioinformatics_software, clinical, protein_structure, proteomics_metabolomics | None |
| R4-REEF-014 | 12/12 | pass | bioinformatics_software, proteomics_metabolomics | bioinformatics_software, proteomics_metabolomics | None |
| R4-REEF-015 | 12/12 | pass | bioinformatics_software, protein_structure | bioinformatics_software, protein_structure | None |
| R4-REEF-016 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R4-REEF-017 | 12/12 | pass | bioinformatics_software, clinical, clinical_imaging_signal | bioinformatics_software, clinical, clinical_imaging_signal | None |
| R4-REEF-018 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R4-REEF-019 | 12/12 | pass | benchmark, bioinformatics_software | benchmark, bioinformatics_software | None |
| R4-REEF-020 | 12/12 | pass | bioinformatics_software, omics, pathway_gene_set | bioinformatics_software, omics, pathway_gene_set | None |

## Interpretation

- This is a deterministic router eval, not a scientific correctness eval.
- Passing means the local OCEAN router selected expected candidate route classes, kept outputs at `candidate_route`, and attached minimum source-packet fields.
- `needs_review` means the route vocabulary or expected route map should be refined before using the case as a stable regression check.

## Evidence Boundary / 证据边界

This run did not query PubMed, GEO, TCGA/GDC, ClinVar, ChEMBL, ClinicalTrials.gov, OpenFDA, TCIA, PhysioNet, or any external software. It did not run LAST, STAR, SAMtools, DESeq2, Seurat, Snakemake, Nextflow, or other tools. It only tested local routing behavior and evidence-boundary scaffolding.
