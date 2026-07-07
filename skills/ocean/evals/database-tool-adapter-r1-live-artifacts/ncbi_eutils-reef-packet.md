# Reef API Resource Packet

## 一、Query Plan

- Adapter: NCBI E-utilities (`ncbi-eutils`)
- Official documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- Endpoint family: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- Executed: True
- Query date UTC: 2026-07-07T17:08:20+00:00
- Query target: `{"database": "gene", "term": "TP53", "retmax": 1}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: PubMed, Gene, GEO, SRA, Protein, PMC, and other Entrez metadata
- Query URL or endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=TP53&retmode=json&retmax=1`

## 四、Evidence Boundary

- Can support: Traceable Entrez record search and public metadata retrieval planning.
- Cannot support: Full-paper evidence, mechanism, causality, clinical efficacy, or absence-of-evidence claims.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "reported_count": "12586",
  "returned_ids": [
    "146679144"
  ],
  "query_translation": "TP53[All Fields]",
  "inspected_fields": [
    "esearchresult.count",
    "esearchresult.idlist",
    "esearchresult.querytranslation"
  ]
}
```
