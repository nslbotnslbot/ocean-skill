# ClinicalTrials.gov Adapter

Use this reference when OCEAN needs to inspect ClinicalTrials.gov registry records as bounded registry evidence.

## Purpose

ClinicalTrials.gov adapter outputs registry source packets. Registry records can describe trial existence, design, status, eligibility, arms, interventions, outcomes, and sometimes posted results. A registry record is not the same as clinical efficacy evidence.

## Can Support

- Trial registration existence.
- NCT identifier and registry status.
- Study phase/type/design if inspected.
- Conditions, interventions, outcomes, eligibility, sponsor metadata.
- Whether results appear to be posted, if the field was inspected.

## Cannot Support Alone

- Treatment efficacy.
- Safety superiority.
- Clinical guideline readiness.
- Completed peer-reviewed trial interpretation.
- Causal treatment effect.

## Required Fields

| Field | Requirement |
|---|---|
| resource | ClinicalTrials.gov |
| identifiers | NCT ID |
| inspected_content | status, design, conditions, interventions, outcomes, results flag if available |
| boundary_status | `queried_evidence` after local registry fields are inspected |
| handoff | Reef, Iceberg, Anchor, or Compass |

## Workflow

1. Use `scripts/clinicaltrials_source_packet.py fetch` only when live public registry retrieval is intended.
2. Use `analyze` on a local ClinicalTrials.gov v2-style JSON record.
3. Use `packet` to generate an OCEAN source packet.
4. Hand off to Iceberg for claim downgrade or Anchor for clinical validation planning.

## Hard Warning

Do not treat `COMPLETED`, `RECRUITING`, or a registry entry as proof of efficacy. Even posted results require endpoint, population, statistical analysis, adverse events, and publication/context inspection before clinical claims.
