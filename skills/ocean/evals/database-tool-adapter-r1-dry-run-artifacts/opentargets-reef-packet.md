# Reef API Resource Packet

## 一、Query Plan

- Adapter: Open Targets Platform (`opentargets`)
- Official documentation: https://platform-docs.opentargets.org/data-access/graphql-api
- Endpoint family: https://api.platform.opentargets.org/api/v4/graphql
- Executed: False
- Query date UTC: 2026-07-07T17:34:51+00:00
- Query target: `{"ensembl_id": "ENSG00000141510"}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
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
{}
```
