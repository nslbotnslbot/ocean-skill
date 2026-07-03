# Sounding Module Contract

Active module: Sounding

Purpose: build a traceable source packet and evidence scan before downstream claims are made.

## Required artifact

- Source packet
- Evidence Radar Map
- Negative Space
- Handoff Ticket

## Source packet fields

| Field | Required content |
|---|---|
| Source seed | DOI, title, file, URL, user note, tool output, or query seed |
| Source tier | full text/data/code/registry; abstract/landing; review/context; database/KG; untraceable note |
| Inspected content | exact material inspected |
| Claim coverage | which claim/question this source can inspect |
| Main limitation | what it cannot support |
| Downstream handoff | Current/Reef/Iceberg/Anchor/Compass/Harbor or stop |

## Rules

- Sounding does not prove a claim; it prepares the evidence coordinates.
- A search result, title, abstract, or tool summary is not full-paper evidence.
- If a retrieval API returns sources, label them as retrieved external context until query and inspected content are recorded.
- If no traceable source exists, stop with a source-packet failure.

## Stop when

Stop before downstream Current, Reef, Iceberg, Anchor, Compass, or Harbor claims if the source packet is untraceable or only contains uninspected retrieval snippets.
