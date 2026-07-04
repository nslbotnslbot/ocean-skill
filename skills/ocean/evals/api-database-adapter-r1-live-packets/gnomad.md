# Reef API Resource Packet

## 一、Query Plan

- Adapter: gnomAD (`gnomad`)
- Official documentation: https://gnomad.broadinstitute.org/help/api
- Endpoint family: https://gnomad.broadinstitute.org/api
- Executed: True
- Query date UTC: 2026-07-04T15:42:04+00:00
- Query target: `{"variant_id": "11-5227002-T-A", "dataset": "gnomad_r4"}`

## 二、Query Log

- Status: executed
- Records inspected: 1
- Failure/limit: None

## 三、Resource Provenance

- Resource role: Population variant frequency and constraint metadata
- Query URL or endpoint: `https://gnomad.broadinstitute.org/api`

## 四、Evidence Boundary

- Can support: Population-frequency or constraint-resource provenance for specified variants/genes.
- Cannot support: Pathogenicity, diagnosis, treatment, or clinical actionability from frequency alone.
- Privacy/access: Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.
- Handoff: Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.

## 五、Result Summary

```json
{
  "variant": {
    "variant_id": "11-5227002-T-A",
    "reference_genome": "GRCh38",
    "chrom": "11",
    "pos": 5227002,
    "ref": "T",
    "alt": "A",
    "exome": {
      "ac": 2335,
      "an": 1458356,
      "af": 0.001601117971194962
    },
    "genome": {
      "ac": 1937,
      "an": 152294,
      "af": 0.012718820176763365
    }
  },
  "inspected_fields": [
    "variant_id",
    "reference_genome",
    "chrom",
    "pos",
    "ref",
    "alt",
    "exome.ac/an/af",
    "genome.ac/an/af"
  ]
}
```
