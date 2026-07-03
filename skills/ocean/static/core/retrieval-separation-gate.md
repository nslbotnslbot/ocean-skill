# Retrieval Separation Gate

OCEAN must separate four evidence states. Never merge them.

Core rule: packet evidence != retrieved external context; candidate route != queried evidence.

| State | Meaning | Allowed claim |
|---|---|---|
| Packet evidence | Provided files, passages, figures, data, code, notes, or source packet that OCEAN inspected | Claims limited to inspected content |
| Candidate route | A database/tool/source path that could be queried later | "This is a route to check", not evidence |
| Retrieved external context | Sources retrieved by a model/API/search during the session | Context only until query, timestamp, identifiers, and inspected content are recorded |
| Queried evidence | Actual API/database/search result with query, filters, date, identifiers, and inspected content | Can support bounded source-packet claims |

## Mandatory wording

When any retrieval-capable model or tool introduces sources not present in the user packet, write:

- `Packet evidence:` what was provided by the user/files.
- `Retrieved external context:` what was found externally.
- `Not yet verified as packet evidence:` source details not inspected or not traceable.

## Prohibitions

- Do not put retrieved external context under `已检查` unless OCEAN actually inspected and records the query/source boundary.
- Do not treat a known database as evidence that this project has data there.
- Do not invent accession IDs, PMIDs, DOIs, registry IDs, sample sizes, metrics, endpoints, or API responses.
- Do not use Perplexity/search citations to upgrade a project claim unless the source packet and inspected content support that exact claim.
