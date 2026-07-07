# Reef API Resource Packet

## 一、Query Plan

- Adapter: Europe PMC (`europepmc`)
- Official documentation: https://europepmc.org/RestfulWebService
- Endpoint family: https://www.ebi.ac.uk/europepmc/webservices/rest/
- Executed: False
- Query date UTC: 2026-07-07T17:06:25+00:00
- Query target: `{"query": "TP53", "pageSize": 2}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Literature metadata, abstracts, preprints, and publication identifiers
- Query URL or endpoint: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TP53&format=json&pageSize=2`

## 四、Evidence Boundary

- Can support: Traceable literature metadata and abstract-level source discovery.
- Cannot support: Full-paper methods/results quality, peer-review status, mechanism, or clinical efficacy unless source text is inspected.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
