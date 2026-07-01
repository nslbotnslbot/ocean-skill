# Anchor Validation Planning

Use Anchor when OCEAN needs to design or audit validation, replication, benchmark fairness, leakage checks, reproducibility, external validation, wet-lab validation, or clinical utility checks.

Anchor is not a claim that the work is valid. Its job is to define what would make the claim more reliable and what is currently missing.

## Contents

- Purpose
- Trigger
- Inputs
- Validation Lenses
- Safety Rules
- Workflow
- Output Artifact
- Stop Conditions
- Failure Modes

## Purpose

- Convert evidence gaps into validation and reproducibility checks.
- Identify leakage, benchmark unfairness, missing external validation, and reproducibility barriers.
- Define minimum evidence needed before stronger biological, clinical, or deployment claims.
- Produce a practical validation plan.

## Trigger

Read this file when the user asks about:

- validation, replication, reproducibility, benchmark fairness, leakage, external validation;
- clinical prediction model readiness;
- whether a model, biomarker, KG, database, or mechanism is reliable;
- what experiments or analyses are needed before publication or deployment;
- whether a claim can move from hypothesis to stronger evidence.

## Inputs

Anchor can start from:

- Iceberg claim-evidence gaps;
- Reef resource/provenance warnings;
- manuscript methods/results;
- model benchmark results;
- clinical prediction or biomedical AI proposal;
- reviewer concerns about validation.

## Validation Lenses

| Lens | Ask |
|---|---|
| Data provenance | Where did data come from and can it be independently traced? |
| Split integrity | Is there leakage across training, validation, test, patient, batch, time, center, or benchmark layers? |
| External validation | Does performance hold across independent datasets, centers, cohorts, labs, or time periods? |
| Calibration/utility | Are predictions calibrated and useful for decisions, not only statistically significant? |
| Benchmark fairness | Are baselines, data access, preprocessing, and metrics fair? |
| Reproducibility | Are code, data, environment, model weights, and protocols available enough to rerun? |
| Biological validation | Are mechanisms tested with perturbation, orthogonal assays, wet-lab, in vivo, or clinical evidence when needed? |

## Safety Rules

- Do not say a system is deployable from internal validation alone.
- Do not treat cross-validation as external validation.
- Do not invent AUROC, AUPRC, calibration, cohort size, event count, or benchmark rank.
- Do not assume code/data availability unless inspected.
- Do not design clinical use without safety, calibration, decision-impact, and prospective/external evidence.

## Workflow

1. **Validation target**
   - State the exact claim to validate and the evidence level required.
2. **Current evidence**
   - List inspected data, methods, results, code, supplement, benchmark, or protocol.
3. **Gap table**
   - Identify missing data, analysis, external validation, leakage checks, reproducibility artifacts, and biological/clinical checks.
4. **Minimum validation plan**
   - Define must-have checks before stronger claims.
5. **Tiered validation**
   - Internal technical check.
   - External or independent validation.
   - Biological or clinical relevance check.
   - Decision-impact or deployment check when applicable.
6. **Handoff**
   - To Compass for experiment design and project strategy.
   - To Harbor for final validation memo.

## Output Artifact

```markdown
一、Anchor任务定义
- Claim to validate:
- Current evidence:
- Required evidence level:
- Validation state:

二、验证缺口表
| Gap | Current evidence | Why it matters | Minimum check | Priority |
|---|---|---|---|---|

三、Leakage / benchmark / reproducibility audit
| Risk | Possible source | Evidence inspected | Needed check |
|---|---|---|---|

四、分层验证计划
| Tier | Validation task | Required input | Pass criterion | Stop condition |
|---|---|---|---|---|

五、Anchor边界
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

六、Handoff Ticket
| Next module | Reason | Input packet | Stop condition |
|---|---|---|---|
```

## Stop Conditions

Stop or downgrade when:

- validation target is undefined;
- only abstract/title evidence is available;
- model results are not provided but performance is requested;
- clinical deployment is requested without external/prospective validation, calibration, and utility evidence;
- code/data/protocol availability cannot be verified for reproducibility claims.

## Failure Modes

- Treating validation planning as validation completion.
- Upgrading cross-validation into deployment readiness.
- Ignoring leakage and benchmark overlap.
- Giving generic experiments that do not test the claim.
- Forgetting pass criteria and stop conditions.
