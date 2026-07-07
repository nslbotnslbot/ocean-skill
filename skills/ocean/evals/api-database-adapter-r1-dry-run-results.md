# OCEAN API/Database Adapter Eval R1

- Run date: 2026-07-08
- Mode: dry-run
- Cases: 13
- Pass: 13
- Needs review: 0

| Case | Adapter | Status | Records | Verdict | Notes |
|---|---|---|---:|---|---|
| API-R1-UNIPROT | uniprot | dry-run | 0 | pass |  |
| API-R1-PUBMED | pubmed | dry-run | 0 | pass |  |
| API-R1-EUROPEPMC | europepmc | dry-run | 0 | pass |  |
| API-R1-CHEMBL | chembl | dry-run | 0 | pass |  |
| API-R1-OPENTARGETS | opentargets | dry-run | 0 | pass |  |
| API-R1-STRING | string | dry-run | 0 | pass |  |
| API-R1-REACTOME | reactome | dry-run | 0 | pass |  |
| API-R1-QUICKGO | quickgo | dry-run | 0 | pass |  |
| API-R1-CLINVAR | clinvar | dry-run | 0 | pass |  |
| API-R1-GNOMAD | gnomad | dry-run | 0 | pass |  |
| API-R1-ALPHAFOLDDB | alphafold-db | dry-run | 0 | pass |  |
| API-R1-CLINICALTRIALS | clinicaltrials | dry-run | 0 | pass |  |
| API-R1-NCBI-EUTILS | ncbi-eutils | dry-run | 0 | pass |  |

## Evidence Boundary / 证据边界

This eval checks that OCEAN can construct bounded Reef packets for API/database resources. Dry-run mode validates query construction and packet contracts without network calls. Live mode performs bounded public API requests, records failures as failures or needs-review, and still does not claim biological mechanism, clinical utility, or scientific validity.
