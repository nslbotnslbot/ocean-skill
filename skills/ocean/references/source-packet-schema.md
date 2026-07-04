# Source Packet Schema

Use this reference when OCEAN converts literature, database, API, registry, cohort, knowledge graph, or artifact outputs into evidence that can be audited.

## Core rule

A source packet is not automatically proof. It is a traceable evidence container. OCEAN must still decide what claims it can and cannot support.

## Evidence states

| State | Meaning | Can support claims? |
|---|---|---|
| `candidate_route` | A resource that could be queried later | No |
| `retrieved_external_context` | Search/model/tool context not fully inspected | No, except as context to inspect |
| `queried_evidence` | A recorded query/API/search result with date, filters, identifiers, and inspected fields | Bounded source-level claims |
| `packet_evidence` | User-provided or tool-created packet with inspected content and limits | Bounded claim-evidence audit |

## Required JSON fields

```json
{
  "packet_id": "string",
  "created_at": "ISO-8601 timestamp",
  "source_type": "literature|database|api|kg|registry|cohort|artifact|other",
  "resource": "PubMed|OpenAlex|ChEMBL|GEO|ClinicalTrials|local_file|...",
  "query": "string or null",
  "filters": {},
  "date_accessed": "YYYY-MM-DD",
  "identifiers": [],
  "inspected_content": [],
  "supports_claims": [],
  "cannot_support": [],
  "license_or_terms_note": "string",
  "boundary_status": "candidate_route|retrieved_external_context|queried_evidence|packet_evidence",
  "handoff": "Sounding|Current|Reef|Iceberg|Anchor|Compass|Harbor|stop"
}
```

## Minimum evidence rules

- A packet without `resource`, `date_accessed`, and `boundary_status` is incomplete.
- `queried_evidence` requires a query or explicit identifiers plus inspected content.
- `packet_evidence` requires inspected content and a limitation statement in `cannot_support`.
- Empty `identifiers` are allowed only when the packet explicitly records that no identifiers were found.
- Do not infer sample size, cohort structure, assay values, validation status, or publication status from the packet metadata.

## Markdown summary format

When summarizing a packet, use:

| Field | Value |
|---|---|
| Packet ID |  |
| Resource |  |
| Boundary status |  |
| Query / identifiers |  |
| Inspected content |  |
| Can support |  |
| Cannot support |  |
| Handoff |  |

