# Harbor Module Contract

Active module: Harbor

Purpose: preserve reports, artifact ledgers, decision memory, collaboration records, and workspace state without inflating uncertain status into fact.

## Required artifact

- Decision Memo
- Evidence Boundary Ledger
- Contribution Boundary Record
- Next-action Register
- Reuse Note

## Collaboration/status rules

- Meeting note != authorship agreement.
- Discussion != commitment.
- Planned != submitted.
- Submitted/under review/revision/accepted requires an explicit record.
- Reviewer comment must be user-provided or source-traceable.

## Harbor ledger

| Item | Recorded fact | Source | Not recorded / cannot infer | Next action |
|---|---|---|---|---|

Harbor should preserve uncertainty so future OCEAN runs do not inherit inflated memory.

## Stop when

Stop before recording authorship, submission status, reviewer status, acceptance, or collaboration commitments unless an explicit traceable record is provided.
