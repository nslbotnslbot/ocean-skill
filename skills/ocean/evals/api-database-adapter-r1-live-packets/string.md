# Reef API Resource Packet

## 一、Query Plan

- Adapter: STRING (`string`)
- Official documentation: https://string-db.org/help/api/
- Endpoint family: https://string-db.org/api/
- Executed: True
- Query date UTC: 2026-07-04T15:41:59+00:00
- Query target: `{"identifiers": "TP53", "species": "9606", "limit": "1"}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Protein identifier mapping and protein-protein association metadata
- Query URL or endpoint: `https://string-db.org/api/json/get_string_ids?identifiers=TP53&species=9606&limit=1`

## 四、Evidence Boundary

- Can support: Traceable STRING identifier mapping or association-resource provenance.
- Cannot support: Physical binding, direct mechanism, causality, or disease relevance from association scores alone.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "records": [
    {
      "queryItem": "TP53",
      "stringId": "9606.ENSP00000269305",
      "preferredName": "TP53",
      "ncbiTaxonId": 9606,
      "annotation": "Cellular tumor antigen p53; Acts as a tumor suppressor in many tumor types; induces growth arrest or apoptosis depending on the physiological circumstances and cell type. Involved in cell cycle regulation as a trans-activator that acts to negatively regulate cell division by controlling a set of genes required for this process. One of the activated genes is an inhibitor of cyclin-dependent kinases. Apoptosis induction seems to be mediated either by stimulation of BAX and FAS antigen expression, or by repression of Bcl-2 expression. Its pro-apoptotic activity is activated via its intera [...] "
    }
  ],
  "inspected_fields": [
    "queryItem",
    "stringId",
    "preferredName",
    "ncbiTaxonId",
    "annotation"
  ]
}
```
