# Reef API Resource Packet

## 一、Query Plan

- Adapter: STRING (`string`)
- Official documentation: https://string-db.org/help/api/
- Endpoint family: https://string-db.org/api/
- Executed: False
- Query date UTC: 2026-07-07T17:45:45+00:00
- Query target: `{"identifiers": "TP53", "species": "9606", "limit": "2"}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Protein identifier mapping and protein-protein association metadata
- Query URL or endpoint: `https://string-db.org/api/json/get_string_ids?identifiers=TP53&species=9606&limit=2`

## 四、Evidence Boundary

- Can support: Traceable STRING identifier mapping or association-resource provenance.
- Cannot support: Physical binding, direct mechanism, causality, or disease relevance from association scores alone.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
