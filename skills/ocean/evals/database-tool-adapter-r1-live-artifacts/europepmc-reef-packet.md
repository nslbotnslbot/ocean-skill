# Reef API Resource Packet

## 一、Query Plan

- Adapter: Europe PMC (`europepmc`)
- Official documentation: https://europepmc.org/RestfulWebService
- Endpoint family: https://www.ebi.ac.uk/europepmc/webservices/rest/
- Executed: True
- Query date UTC: 2026-07-07T17:08:19+00:00
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
  "hit_count": 154709,
  "records": [
    {
      "id": "41980118",
      "source": "MED",
      "pmid": "41980118",
      "doi": "10.1093/jjco/hyag056",
      "title": "TP53 mutation landscape and patient survival in oral squamous cell carcinoma.",
      "journalTitle": "Jpn J Clin Oncol",
      "pubYear": "2026",
      "authorString": "Ichikawa M, Kondo Y, Carreras J, Sasaki M, Nagase S, Hoshimoto Y, Tamura M, Uchibori M, Aoki T, Nakamura N, Masugi Y, Ota Y."
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
