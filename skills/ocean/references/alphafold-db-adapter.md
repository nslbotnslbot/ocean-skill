# AlphaFold DB Adapter

Use this reference when OCEAN needs to inspect AlphaFold Database predicted structures as bounded structural evidence.

## Purpose

The adapter turns AlphaFold DB files into an OCEAN source packet. It is a Reef/Anchor support tool, not a mechanism prover.

## Inputs

- UniProt accession ID for live fetch.
- Or local AlphaFold DB metadata JSON, PAE JSON, and optional mmCIF for offline analysis.

## Evidence Boundary

AlphaFold DB can support:

- predicted-structure availability;
- pLDDT confidence summary;
- low-confidence/disorder warning;
- PAE-based domain/flexibility hypothesis;
- residue or domain ranges for downstream inspection.

AlphaFold DB cannot by itself support:

- binding proof;
- enzymatic function;
- disease mechanism;
- druggability;
- clinical relevance;
- experimental validation;
- docking readiness for disordered regions.

## Required OCEAN Packet Fields

| Field | Requirement |
|---|---|
| resource | AlphaFold DB |
| source_type | predicted_structure_database |
| identifiers | UniProt accession and fetched file names if available |
| inspected_content | metadata, pLDDT summary, PAE summary, optional mmCIF B-factor pLDDT |
| supports_claims | only bounded structural-confidence claims |
| cannot_support | mechanism, function, binding, clinical or therapeutic claims |
| boundary_status | `queried_evidence` or `packet_evidence` only after local files are inspected |
| handoff | Reef, Iceberg, or Anchor |

## Workflow

1. If the user gives only a protein/gene name, ask for a UniProt accession or route to UniProt first.
2. Use `scripts/tools/bioinformatics/alphafold_db/source_packet.py fetch` only with explicit user intent to fetch public AFDB files.
3. Use `scripts/tools/bioinformatics/alphafold_db/source_packet.py analyze` on local metadata/PAE/mmCIF files.
4. Use `scripts/tools/bioinformatics/alphafold_db/source_packet.py packet` to create an OCEAN source packet.
5. Hand the packet to Iceberg for claim downgrade or Anchor for validation planning.

## Warnings to Preserve

- If mean pLDDT is low or a large fraction is below 50, warn that whole-protein structure-based interpretation is unsafe.
- If PAE suggests multiple flexible domains, avoid whole-protein rigid-body interpretations.
- If only metadata is available and no PAE/mmCIF was inspected, stop before domain-boundary or inter-domain flexibility claims.
