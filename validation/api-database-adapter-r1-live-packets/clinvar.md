# Reef API Resource Packet

## 一、Query Plan

- Adapter: ClinVar via NCBI E-utilities (`clinvar`)
- Official documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- Endpoint family: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- Executed: True
- Query date UTC: 2026-07-07T17:06:51+00:00
- Query target: `{"database": "clinvar", "term": "BRCA1", "retmax": 1}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Public variant clinical-significance records and ClinVar metadata
- Query URL or endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1&retmode=json&retmax=1`

## 四、Evidence Boundary

- Can support: Traceable ClinVar record discovery and public metadata retrieval planning.
- Cannot support: Clinical diagnosis, treatment guidance, or variant pathogenicity without inspected record details and expert interpretation.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "reported_count": "84925",
  "returned_ids": [
    "4857230"
  ],
  "query_translation": "BRCA1[All Fields]",
  "inspected_fields": [
    "esearchresult.count",
    "esearchresult.idlist",
    "esearchresult.querytranslation"
  ]
}
```
