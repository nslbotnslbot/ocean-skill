# Reef API Resource Packet

## 一、Query Plan

- Adapter: Reactome (`reactome`)
- Official documentation: https://reactome.org/dev/content-service
- Endpoint family: https://reactome.org/ContentService/
- Executed: False
- Query date UTC: 2026-07-07T17:24:54+00:00
- Query target: `{"query": "TP53", "pageSize": "2", "page": "1", "species": "Homo sapiens"}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Curated pathway and reaction metadata
- Query URL or endpoint: `https://reactome.org/ContentService/search/query?query=TP53&pageSize=2&page=1&species=Homo+sapiens`

## 四、Evidence Boundary

- Can support: Traceable pathway/resource discovery and pathway-context provenance.
- Cannot support: Pathway activity, causality, disease mechanism, or treatment effect without experimental support.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
