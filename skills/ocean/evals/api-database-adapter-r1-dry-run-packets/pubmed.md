# Reef API Resource Packet

## 一、Query Plan

- Adapter: PubMed via NCBI E-utilities (`pubmed`)
- Official documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- Endpoint family: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- Executed: False
- Query date UTC: 2026-07-07T17:06:25+00:00
- Query target: `{"database": "pubmed", "term": "TP53", "retmax": 2}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: PubMed literature metadata
- Query URL or endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=TP53&retmode=json&retmax=2`

## 四、Evidence Boundary

- Can support: Traceable PubMed record discovery and public metadata retrieval planning.
- Cannot support: Full-paper evidence, mechanism, causality, clinical efficacy, or absence-of-evidence claims.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
