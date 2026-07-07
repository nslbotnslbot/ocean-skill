# Reef API Resource Packet

## 一、Query Plan

- Adapter: ChEMBL (`chembl`)
- Official documentation: https://chembl.gitbook.io/chembl-interface-documentation/web-services
- Endpoint family: https://www.ebi.ac.uk/chembl/api/data/
- Executed: False
- Query date UTC: 2026-07-07T17:10:44+00:00
- Query target: `{"pref_name__icontains": "aspirin", "limit": 2}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Bioactive molecules, targets, assays, and drug-like compound metadata
- Query URL or endpoint: `https://www.ebi.ac.uk/chembl/api/data/molecule.json?pref_name__icontains=aspirin&limit=2&format=json`

## 四、Evidence Boundary

- Can support: Traceable molecule/target/assay metadata discovery.
- Cannot support: Efficacy, safety, clinical utility, or mechanism from database presence alone.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
