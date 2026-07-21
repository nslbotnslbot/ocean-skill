# Iceberg Claim-Evidence Audit

Use Iceberg when OCEAN needs to inspect the evidence beneath a surface claim. Iceberg turns claims into audit units, compares them against inspected evidence, and rewrites overstatements into safer claims.

Iceberg is not a full paper summary. Its job is to find the hidden risk below the visible claim.

## Contents

- Purpose
- Trigger
- Inputs
- Claim Types
- Safety Rules
- Workflow
- Output Artifact
- Stop Conditions
- Failure Modes

## Purpose

- Extract major claims from a paper, manuscript, proposal, idea, review comment, or source packet.
- Determine what inspected evidence can and cannot support.
- Downgrade unsupported mechanism, causality, clinical, novelty, validation, benchmark, or authorship claims.
- Produce claim-evidence matrices and safer wording.

## Trigger

Read this file when the user asks to:

- check manuscript or paper claims;
- audit whether evidence supports a conclusion;
- find overclaims, hidden reviewer risks, or unsafe wording;
- rewrite claims more safely;
- evaluate mechanism, causality, clinical utility, validation, or publication readiness.

## Inputs

Iceberg can start from:

- Sounding source packet;
- paper abstract/full text/figures/tables/supplement;
- manuscript draft;
- proposal aims;
- reviewer comments;
- Current direction map or Reef resource map.

## Claim Types

| Claim type | Typical risk |
|---|---|
| Descriptive | Overstating scope or sample coverage |
| Association | Framed as mechanism or causality |
| Mechanism | Lacks perturbation, time ordering, or experimental validation |
| Benchmark | Overstated as general superiority or clinical utility |
| Clinical | Lacks external/prospective validation, calibration, utility, or safety evidence |
| Resource/KG | Database co-occurrence treated as experimental proof |
| Novelty | Ignores related work or prior art |
| Authorship/contribution | Infers role or credit not supported by records |

## Safety Rules

- Never audit a claim without stating what evidence was inspected.
- Do not infer figure/table results that were not provided.
- Do not treat abstract-level wording as full-paper evidence.
- Downgrade strong claims when key evidence is missing.
- Separate "supports a weaker claim" from "supports the original claim".
- In Manuscript Revision mode, keep the claim audit internal and isolate clean replacement prose from module labels, verdicts, reviewer language, editing commands, and author queries.

## Workflow

1. **Claim inventory**
   - Extract central claims and label claim type.
   - Split compound claims into auditable fragments.
2. **Evidence binding**
   - Attach each claim to inspected evidence: passage, figure, table, method, dataset, source packet, or resource record.
3. **Support verdict**
   - Use Supported, Partially supported, Downgrade, Unsupported, Contradicted, Cannot judge, or Needs source.
4. **Risk diagnosis**
   - Identify hidden assumptions, missing validation, causal leap, benchmark leap, resource leap, or clinical leap.
5. **Safe rewrite**
   - Rewrite each risky claim into the strongest version supported by inspected evidence.
6. **Handoff**
   - To Anchor when validation or reproducibility is needed.
   - To Compass when claim gaps imply research plans or idea opportunities.
   - To Harbor when final report memory is needed.

For finished-text revision, replace the visible artifact below with the Manuscript Revision contract in `references/manuscript-revision-mode.md`. The Claim-Evidence Matrix may inform the edit but must not be mixed into the paste-ready paragraph.

## Output Artifact

```markdown
一、Iceberg任务定义
- Surface claim / manuscript section:
- Evidence inspected:
- Claim scope:
- Evidence state:

二、Claim inventory
| ID | Surface claim | Claim type | Strength requested | Evidence needed |
|---|---|---|---|---|

三、Claim-evidence matrix
| ID | Evidence inspected | Support verdict | Main gap | Hidden risk | Safe rewrite |
|---|---|---|---|---|---|

四、Overclaim map
| Overclaim pattern | Where it appears | Why unsupported | Downgrade |
|---|---|---|---|

五、Iceberg边界
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

六、Handoff Ticket
| Next module | Reason | Input packet | Stop condition |
|---|---|---|---|
```

## Stop Conditions

Stop or mark Cannot judge when:

- the claim has no traceable source;
- figures/tables/supplements needed for the claim were not provided;
- methods or datasets are unavailable for validation claims;
- clinical or mechanism claims are requested from association, benchmark, KG, or abstract-only evidence.

## Failure Modes

- Summarizing instead of auditing.
- Keeping unsafe claim wording because the work sounds promising.
- Treating missing evidence as neutral rather than a gap.
- Collapsing Partially supported and Supported.
- Failing to provide safe rewrites.
