# OCEAN Database Tool Adapter Eval

- Run date: 2026-07-08
- Mode: live
- Cases: 13
- Pass: 13
- Needs review: 0

| Adapter | Family | Status | Records | Verdict | Notes |
|---|---|---|---:|---|---|
| alphafold-db | structure_modeling | executed | 1 | pass | None |
| chembl | drug_target | executed | 1 | pass | None |
| clinicaltrials | clinical_registry | executed | 1 | pass | None |
| clinvar | variant_clinical_annotation | executed | 1 | pass | None |
| europepmc | literature_metadata | executed | 1 | pass | None |
| gnomad | population_genetics | executed | 1 | pass | None |
| ncbi-eutils | entrez_metadata | executed | 1 | pass | None |
| opentargets | drug_target | executed | 1 | pass | None |
| pubmed | literature_metadata | executed | 1 | pass | None |
| quickgo | ontology | executed | 1 | pass | None |
| reactome | pathway | executed | 1 | pass | None |
| string | protein_interaction | executed | 1 | pass | None |
| uniprot | protein_annotation | executed | 1 | pass | None |

## Evidence Boundary

This eval checks database tool folder contracts and bounded Reef packet creation. Dry-run mode does not make network calls. Live mode is bounded and records API/network failures explicitly. Passing this eval does not validate biological mechanisms, clinical utility, therapeutic efficacy, diagnosis, or publication readiness.
