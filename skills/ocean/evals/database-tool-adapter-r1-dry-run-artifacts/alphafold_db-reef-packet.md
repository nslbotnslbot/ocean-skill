# Reef API Resource Packet

## 一、Query Plan

- Adapter: AlphaFold DB (`alphafold-db`)
- Official documentation: https://alphafold.ebi.ac.uk/api-docs
- Endpoint family: https://alphafold.ebi.ac.uk/api/prediction/
- Executed: False
- Query date UTC: 2026-07-07T17:10:44+00:00
- Query target: `{"uniprot_accession": "P04637"}`

## 二、Query Log

- Status: dry-run
- Records inspected: 0
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Predicted protein structure metadata and confidence files by UniProt accession
- Query URL or endpoint: `https://alphafold.ebi.ac.uk/api/prediction/P04637`

## 四、Evidence Boundary

- Can support: Traceable predicted-structure metadata lookup by UniProt accession.
- Cannot support: Experimental structure proof, binding proof, mechanism, druggability, or functional rescue.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{}
```
