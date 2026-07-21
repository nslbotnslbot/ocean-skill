# Reef API Resource Packet

## 一、Query Plan

- Adapter: PubMed via NCBI E-utilities (`pubmed`)
- Official documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- Endpoint family: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- Executed: True
- Query date UTC: 2026-07-07T17:06:43+00:00
- Query target: `{"database": "pubmed", "term": "TP53", "retmax": 1}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: PubMed literature metadata
- Query URL or endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=TP53&retmode=json&retmax=1`

## 四、Evidence Boundary

- Can support: Traceable PubMed record discovery and public metadata retrieval planning.
- Cannot support: Full-paper evidence, mechanism, causality, clinical efficacy, or absence-of-evidence claims.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "reported_count": "39030",
  "returned_ids": [
    "42410294"
  ],
  "query_translation": "\"tp53 protein human\"[Supplementary Concept] OR \"tp53 protein human\"[All Fields] OR \"tp53\"[All Fields]",
  "inspected_fields": [
    "esearchresult.count",
    "esearchresult.idlist",
    "esearchresult.querytranslation"
  ]
}
```
