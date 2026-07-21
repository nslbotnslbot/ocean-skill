# OCEAN Database Tool Adapter Eval

- Run date: 2026-07-08
- Mode: dry-run
- Cases: 13
- Pass: 13
- Needs review: 0

| Adapter | Family | Status | Records | Verdict | Notes |
|---|---|---|---:|---|---|
| alphafold-db | structure_modeling | dry-run | 0 | pass | None |
| chembl | drug_target | dry-run | 0 | pass | None |
| clinicaltrials | clinical_registry | dry-run | 0 | pass | None |
| clinvar | variant_clinical_annotation | dry-run | 0 | pass | None |
| europepmc | literature_metadata | dry-run | 0 | pass | None |
| gnomad | population_genetics | dry-run | 0 | pass | None |
| ncbi-eutils | entrez_metadata | dry-run | 0 | pass | None |
| opentargets | drug_target | dry-run | 0 | pass | None |
| pubmed | literature_metadata | dry-run | 0 | pass | None |
| quickgo | ontology | dry-run | 0 | pass | None |
| reactome | pathway | dry-run | 0 | pass | None |
| string | protein_interaction | dry-run | 0 | pass | None |
| uniprot | protein_annotation | dry-run | 0 | pass | None |

## Evidence Boundary

This eval checks database tool folder contracts and bounded Reef packet creation. Dry-run mode does not make network calls. Live mode is bounded and records API/network failures explicitly. Passing this eval does not validate biological mechanisms, clinical utility, therapeutic efficacy, diagnosis, or publication readiness.
