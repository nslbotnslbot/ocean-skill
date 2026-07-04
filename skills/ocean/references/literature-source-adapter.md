# Literature Source Adapter

Use this reference when OCEAN needs to turn PubMed or EuropePMC records into bounded source packets for Sounding, Current, Iceberg, or Harbor.

## Purpose

Literature adapter outputs are source identity and abstract/full-text boundary packets. They are not full-paper audits unless the full text, figures, tables, supplement, and methods are inspected.

## Can Support

- Source existence and identifiers.
- Title/abstract-level claim framing.
- Publication metadata.
- A source packet for downstream claim audit.

## Cannot Support Alone

- Full methods/results quality.
- Figure/table-level evidence.
- Peer-review outcome unless explicitly included.
- Data/code availability.
- Causal, clinical, or publication-readiness claims.

## Required Fields

| Field | Requirement |
|---|---|
| resource | PubMed, EuropePMC, or local literature record |
| identifiers | PMID, DOI, PMCID, preprint ID if available |
| inspected_content | title, abstract, metadata, full text if actually inspected |
| boundary_status | `queried_evidence` only after local record fields are inspected |
| handoff | Sounding, Current, Iceberg, or Harbor |

## Workflow

1. Use `scripts/literature_source_packet.py fetch-pubmed` or `fetch-europepmc` only when live public retrieval is intended.
2. Use `analyze` on local JSON records.
3. Use `packet` to generate an OCEAN source packet.
4. If only title/abstract was inspected, downgrade downstream claims to abstract-level only.
