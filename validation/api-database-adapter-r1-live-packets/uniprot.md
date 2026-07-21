# Reef API Resource Packet

## 一、Query Plan

- Adapter: UniProt (`uniprot`)
- Official documentation: https://www.uniprot.org/help/api
- Endpoint family: https://rest.uniprot.org/
- Executed: True
- Query date UTC: 2026-07-07T17:06:41+00:00
- Query target: `{"accession": "P04637"}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Protein metadata, function, taxonomy, sequence, and cross-references
- Query URL or endpoint: `https://rest.uniprot.org/uniprotkb/P04637.json`

## 四、Evidence Boundary

- Can support: Traceable protein accession, reviewed/unreviewed status, sequence, and annotation metadata.
- Cannot support: New functional proof, mechanism, causality, or clinical utility without primary evidence.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "records": [
    {
      "primaryAccession": "P04637",
      "uniProtkbId": "P53_HUMAN",
      "reviewed": "UniProtKB reviewed (Swiss-Prot)",
      "proteinDescription": "Cellular tumor antigen p53",
      "genes": [
        "TP53"
      ],
      "organism": "Homo sapiens"
    }
  ],
  "inspected_fields": [
    "primaryAccession",
    "uniProtkbId",
    "entryType",
    "proteinDescription",
    "genes",
    "organism"
  ]
}
```
