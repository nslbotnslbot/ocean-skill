# Tool Adapter Contract

Use this reference when adding or using OCEAN tool adapters for literature, biomedical databases, clinical registries, omics resources, protein/structure resources, drug-target databases, knowledge graphs, or local artifacts.

## OCEAN adapter role

Adapters fetch, normalize, cache, and packetize evidence. They do not decide scientific truth.

OCEAN modules decide:

- whether the packet is complete enough to use;
- what claims the packet can support;
- what must be downgraded;
- whether to hand off to Iceberg, Anchor, Compass, or Harbor.

## Required adapter behavior

Every adapter must:

- write outputs to files;
- use JSON for machine-readable outputs;
- record query, filters, date, resource, identifiers, and inspected fields;
- respect API terms, rate limits, and credential boundaries;
- expose missing fields instead of filling them with guesses;
- preserve source errors and HTTP response bodies when available;
- separate `candidate_route`, `retrieved_external_context`, `queried_evidence`, and `packet_evidence`;
- produce or accept OCEAN source packets.

Every adapter must not:

- fabricate PMIDs, DOIs, accession IDs, registry IDs, ChEMBL IDs, UniProt IDs, sample sizes, p values, assay values, or endpoints;
- treat a database name as evidence;
- treat a route as a completed query;
- treat a query result as clinical, causal, mechanistic, or publication-ready proof without OCEAN audit;
- hide failed or empty queries.

## Recommended CLI pattern

Use one script with subcommands and explicit `--output`:

```bash
python3 scripts/ocean_source_router.py route --question "EGFR inhibitor resistance" --output route.json
python3 scripts/ocean_source_router.py record-query --resource PubMed --query "EGFR resistance" --output query.json
python3 scripts/ocean_source_router.py packetize --input query.json --output packet.json
python3 scripts/ocean_source_router.py audit-packet --input packet.json --output packet_audit.md
```

When a future live API adapter is added, prefer this shape:

```bash
python3 scripts/ocean_pubmed_adapter.py search --query "..." --limit 20 --output pubmed_search.json
python3 scripts/ocean_pubmed_adapter.py fetch --ids "..." --output pubmed_fetch.json
python3 scripts/ocean_source_router.py packetize --input pubmed_fetch.json --output source_packet.json
```

## Error handling

- Exit nonzero on invalid input.
- Write no success output when a command fails.
- Include the missing field or invalid state in error messages.
- On external APIs, record rate-limit and license/terms notes separately from evidence.

## Adapter maturity levels

| Level | Meaning |
|---|---|
| L0 route only | Suggest candidate resources; no live query |
| L1 record/import | Record query metadata or import existing JSON |
| L2 live query | Query a resource through a wrapper with rate limits |
| L3 packet audit | Produce source packets plus completeness checks |
| L4 cross-resource | Link literature, database, registry, and artifact packets |

