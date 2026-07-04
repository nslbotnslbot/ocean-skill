# Reef API Resource Packet

## 一、Query Plan

- Adapter: Europe PMC (`europepmc`)
- Official documentation: https://europepmc.org/RestfulWebService
- Endpoint family: https://www.ebi.ac.uk/europepmc/webservices/rest/
- Executed: True
- Query date UTC: 2026-07-04T15:41:56+00:00
- Query target: `{"query": "TP53", "pageSize": 1}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Literature metadata, abstracts, preprints, and publication identifiers
- Query URL or endpoint: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TP53&format=json&pageSize=1`

## 四、Evidence Boundary

- Can support: Traceable literature metadata and abstract-level source discovery.
- Cannot support: Full-paper methods/results quality, peer-review status, mechanism, or clinical efficacy unless source text is inspected.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "hit_count": 154698,
  "records": [
    {
      "id": "42399724",
      "source": "MED",
      "pmid": "42399724",
      "doi": "10.1186/s40478-026-02369-w",
      "title": "Molecular characteristics of isocitrate dehydrogenase 1 R132C-mutant diffuse gliomas: association with TP53 alterations and Li-Fraumeni syndrome. ",
      "journalTitle": "Acta Neuropathol Commun",
      "pubYear": "2026",
      "authorString": "Yamashita S, Matsumoto F, Saito K, Hidaka M, Arikawa S, Kawano T, Kawano T, Tamura M, Okuyama H, Higa N, Hanaya R, Akahane T, Tanimoto A, Sato Y, Okita Y."
    }
  ],
  "inspected_fields": [
    "id",
    "source",
    "pmid",
    "pmcid",
    "doi",
    "title",
    "journalTitle",
    "pubYear",
    "authorString"
  ]
}
```
