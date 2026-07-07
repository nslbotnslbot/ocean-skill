# Reef API Resource Packet

## 一、Query Plan

- Adapter: QuickGO (`quickgo`)
- Official documentation: https://www.ebi.ac.uk/QuickGO/api/index.html
- Endpoint family: https://www.ebi.ac.uk/QuickGO/services/
- Executed: False
- Query date UTC: 2026-07-07T17:24:54+00:00
- Query target: `{"query": "apoptosis", "limit": "2", "page": "1"}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Gene Ontology term and annotation metadata
- Query URL or endpoint: `https://www.ebi.ac.uk/QuickGO/services/ontology/go/search?query=apoptosis&limit=2&page=1`

## 四、Evidence Boundary

- Can support: Traceable GO term or annotation metadata discovery.
- Cannot support: Direct molecular mechanism, causality, or phenotype proof from annotation presence alone.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
