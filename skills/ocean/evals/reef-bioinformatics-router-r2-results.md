# OCEAN Reef Bioinformatics Router R2 Results

- Run date: 2026-07-04
- Cases: 21
- Pass: 21
- Needs review: 0
- Mean score: 11.95/12

## Case Summary

| Case | Score | Verdict | Expected routes | Returned routes | Misses |
|---|---:|---|---|---|---|
| R2-REEF-001 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R2-REEF-002 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R2-REEF-003 | 12/12 | pass | bioinformatics_software, omics | bioinformatics_software, clinical, omics | None |
| R2-REEF-004 | 12/12 | pass | omics | cancer_genomics, omics | None |
| R2-REEF-005 | 12/12 | pass | epigenomics_regulatory | epigenomics_regulatory, omics | None |
| R2-REEF-006 | 12/12 | pass | clinical, variant_genetics | cancer_genomics, clinical, variant_genetics | None |
| R2-REEF-007 | 12/12 | pass | cancer_genomics, pathway_gene_set | cancer_genomics, clinical, pathway_gene_set | None |
| R2-REEF-008 | 12/12 | pass | drug_target | drug_target | None |
| R2-REEF-009 | 12/12 | pass | clinical | clinical | None |
| R2-REEF-010 | 12/12 | pass | drug_target, regulatory_safety | drug_target, regulatory_safety | None |
| R2-REEF-011 | 11/12 | pass | clinical, clinical_imaging_signal | clinical, clinical_imaging_signal | imaging |
| R2-REEF-012 | 12/12 | pass | bioinformatics_software, microbiome | bioinformatics_software, clinical, microbiome | None |
| R2-REEF-013 | 12/12 | pass | bioinformatics_software, proteomics_metabolomics | bioinformatics_software, proteomics_metabolomics | None |
| R2-REEF-014 | 12/12 | pass | bioinformatics_software, proteomics_metabolomics | bioinformatics_software, proteomics_metabolomics | None |
| R2-REEF-015 | 12/12 | pass | bioinformatics_software, protein_structure | bioinformatics_software, protein_structure | None |
| R2-REEF-016 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R2-REEF-017 | 12/12 | pass | model_organism | model_organism | None |
| R2-REEF-018 | 12/12 | pass | benchmark | benchmark, clinical | None |
| R2-REEF-019 | 12/12 | pass | bioinformatics_software | bioinformatics_software | None |
| R2-REEF-020 | 12/12 | pass | clinical, literature | clinical, literature | None |
| R2-REEF-021 | 12/12 | pass | clinical | artifact, clinical, clinical_imaging_signal | None |

## Interpretation

- This is a deterministic router eval, not a scientific correctness eval.
- Passing means the local OCEAN router selected expected candidate route classes, kept outputs at `candidate_route`, and attached minimum source-packet fields.
- `needs_review` means the route vocabulary or expected route map should be refined before using the case as a stable regression check.

## Evidence Boundary / 证据边界

This run did not query PubMed, GEO, TCGA/GDC, ClinVar, ChEMBL, ClinicalTrials.gov, OpenFDA, TCIA, PhysioNet, or any external software. It did not run LAST, STAR, SAMtools, DESeq2, Seurat, Snakemake, Nextflow, or other tools. It only tested local routing behavior and evidence-boundary scaffolding.
