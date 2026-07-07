# Reef API Resource Packet

## 一、Query Plan

- Adapter: QuickGO (`quickgo`)
- Official documentation: https://www.ebi.ac.uk/QuickGO/api/index.html
- Endpoint family: https://www.ebi.ac.uk/QuickGO/services/
- Executed: True
- Query date UTC: 2026-07-07T17:06:50+00:00
- Query target: `{"query": "apoptosis", "limit": "1", "page": "1"}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Gene Ontology term and annotation metadata
- Query URL or endpoint: `https://www.ebi.ac.uk/QuickGO/services/ontology/go/search?query=apoptosis&limit=1&page=1`

## 四、Evidence Boundary

- Can support: Traceable GO term or annotation metadata discovery.
- Cannot support: Direct molecular mechanism, causality, or phenotype proof from annotation presence alone.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "records": [
    {
      "id": "GO:0097194",
      "name": "execution phase of apoptosis",
      "definition": {
        "text": "A stage of the apoptotic process that starts with the controlled breakdown of the cell through the action of effector caspases or other effector molecules (e.g. cathepsins, calpains etc.). Key steps of the execution phase are rounding-up of the cell, retraction of pseudopodes, reduction of cellular volume (pyknosis), chromatin condensation, nuclear fragmentation (karyorrhexis), plasma membrane blebbing and fragmentation of the cell into apoptotic bodies. When the execution phase is completed, the cell has died."
      },
      "aspect": "biological_process",
      "isObsolete": false
    }
  ],
  "inspected_fields": [
    "id",
    "name",
    "definition",
    "aspect",
    "isObsolete"
  ]
}
```
