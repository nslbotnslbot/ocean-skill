# Iceberg Module Contract

Active module: Iceberg

Purpose: audit what lies under a surface claim: support level, hidden risks, unsupported leaps, and safer wording.

## Required artifact

- Surface Claim
- Support Level
- Hidden Risk
- Downgraded Safe Claim

## Claim downgrade rules

- Prediction -> hypothesis unless validated.
- Association -> association, not mechanism.
- Database/KG/text-mining hit -> candidate evidence, not proof.
- Docking/predicted structure -> structural hypothesis, not binding proof.
- Internal validation -> internal validation, not external/clinical readiness.
- Retrospective single-center model -> development/internal validation, not deployment.

## Output table

| Surface claim | Evidence inspected | Support level | Hidden risk | Safe rewrite |
|---|---|---|---|---|

If no evidence supports the surface claim, state `Unsupported` and provide a hypothesis-level rewrite.

## Manuscript revision boundary

When the lifecycle mode is Manuscript Revision, run this audit silently. Return the safe rewrite in `修订正文（可直接替换）` and put the support verdict or hidden risk only in `修改说明（不进入正文）`. Never insert `Iceberg`, `Unsupported`, `Downgrade`, editing commands, reviewer language, or newly created placeholders into clean manuscript prose.

## Stop when

Stop before causal, mechanistic, clinical, or publication-ready conclusions if the inspected evidence only supports association, prediction, database annotation, or hypothesis.
