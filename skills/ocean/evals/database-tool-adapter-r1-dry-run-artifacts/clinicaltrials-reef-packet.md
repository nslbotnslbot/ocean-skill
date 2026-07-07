# Reef API Resource Packet

## 一、Query Plan

- Adapter: ClinicalTrials.gov (`clinicaltrials`)
- Official documentation: https://clinicaltrials.gov/data-api/api
- Endpoint family: https://clinicaltrials.gov/api/v2/
- Executed: False
- Query date UTC: 2026-07-07T17:45:44+00:00
- Query target: `{"query.term": "melanoma", "pageSize": 2}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Clinical trial registry metadata
- Query URL or endpoint: `https://clinicaltrials.gov/api/v2/studies?query.term=melanoma&pageSize=2&format=json`

## 四、Evidence Boundary

- Can support: Study existence, registration status, design metadata, and posted registry fields.
- Cannot support: Treatment efficacy or clinical guidance unless results and publications are inspected.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
