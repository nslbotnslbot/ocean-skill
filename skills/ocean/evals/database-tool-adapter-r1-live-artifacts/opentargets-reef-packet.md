# Reef API Resource Packet

## 一、Query Plan

- Adapter: Open Targets Platform (`opentargets`)
- Official documentation: https://platform-docs.opentargets.org/data-access/graphql-api
- Endpoint family: https://api.platform.opentargets.org/api/v4/graphql
- Executed: True
- Query date UTC: 2026-07-07T17:08:20+00:00
- Query target: `{"ensembl_id": "ENSG00000141510"}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Target, disease, drug, variant, and target-disease association context
- Query URL or endpoint: `https://api.platform.opentargets.org/api/v4/graphql`

## 四、Evidence Boundary

- Can support: Target annotation and association-resource provenance.
- Cannot support: Mechanism, therapeutic efficacy, or clinical readiness from association scores alone.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "target": {
    "id": "ENSG00000141510",
    "approvedSymbol": "TP53",
    "approvedName": "tumor protein p53",
    "biotype": "protein_coding"
  },
  "inspected_fields": [
    "target.id",
    "target.approvedSymbol",
    "target.approvedName",
    "target.biotype"
  ]
}
```
