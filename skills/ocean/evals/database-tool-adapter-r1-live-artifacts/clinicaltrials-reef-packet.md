# Reef API Resource Packet

## 一、Query Plan

- Adapter: ClinicalTrials.gov (`clinicaltrials`)
- Official documentation: https://clinicaltrials.gov/data-api/api
- Endpoint family: https://clinicaltrials.gov/api/v2/
- Executed: True
- Query date UTC: 2026-07-07T17:08:18+00:00
- Query target: `{"query.term": "melanoma", "pageSize": 1}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Clinical trial registry metadata
- Query URL or endpoint: `https://clinicaltrials.gov/api/v2/studies?query.term=melanoma&pageSize=1&format=json`

## 四、Evidence Boundary

- Can support: Study existence, registration status, design metadata, and posted registry fields.
- Cannot support: Treatment efficacy or clinical guidance unless results and publications are inspected.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "returned_nct_ids": [
    "NCT01191294"
  ],
  "overall_status_values_seen": [
    "COMPLETED"
  ],
  "inspected_fields": [
    "protocolSection.identificationModule.nctId",
    "protocolSection.statusModule.overallStatus"
  ]
}
```
