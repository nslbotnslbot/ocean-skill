# OCEAN Project Progress Hub

This directory is the canonical public-safe progress area for real research projects that use **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**.

**中文上下文**: 这里记录 OCEAN 在真实科研项目中的使用进度，但不公开原始数据、未公开稿件正文、患者级信息、保密审稿意见或未经确认的投稿结果。

**English context**: These records show how OCEAN enters real research and manuscript workflows. They are project-level progress notes, not scientific validation, publication proof, or a substitute for the project repository.

## Project Index

| Project ID | Project | Domain | OCEAN phase | Project stage | Last verified | Record |
|---|---|---|---|---|---|---|
| OCEAN-PROJ-001 | Whole-Wheat Fermented Broth Study | Biological research | Pre-submission audit | Manuscript preparation | 2026-07-06 | [Project record](whole-wheat-fermented-broth/README.md) |
| OCEAN-PROJ-002 | Delirium AI: ICU Prediction Transportability | Medical AI | Pre-submission audit | Repository release preparation | 2026-07-20 | [Project record](delirium-ai/README.md) |

## Two Independent Statuses

Do not compress OCEAN activity and external publication status into one label.

| Field | Allowed meaning |
|---|---|
| `ocean_phase` | `planning`, `evidence-audit`, `validation-planning`, `manuscript-support`, `pre-submission-audit`, `reviewer-response`, or `archived` |
| `project_stage` | `idea`, `analysis`, `manuscript-preparation`, `repository-release-preparation`, `submitted`, `under-review`, `revision`, `accepted`, `published`, `paused`, or `to-be-confirmed` |
| `public_status` | `active`, `paused`, `completed`, `archived`, or `awaiting-owner-confirmation` |

`Submitted`, `under-review`, `revision`, `accepted`, and `published` may be recorded only after owner confirmation or inspection of a public/official record. An OCEAN audit does not prove scientific validity or journal status.

## Update Rules

1. Use [`PROJECT_TEMPLATE.md`](PROJECT_TEMPLATE.md) for each new project.
2. Keep one folder per project and append dated entries to its `Progress Log`.
3. Separate inspected evidence, owner-confirmed facts, local project records, and unverified plans.
4. Record what changed, what remains blocked, and the next public update gate.
5. Never publish secrets, local absolute paths, raw or row-level controlled data, private manuscripts, confidential correspondence, hidden eval answers, or collaborator-only decisions.
6. A repository-organization update must explicitly say that it does not change the scientific or submission status.

Run the project-record check before publishing:

```bash
python3 validation/scripts/check_project_records.py
```

After the project owner confirms that a new record is public-safe, the Harbor generator can create the folder and index entry:

```bash
python3 skills/ocean/scripts/create_project_start_record.py \
  --title "Public-safe project title" \
  --domain "biological-research" \
  --public-safe yes \
  --evidence-basis "owner-confirmed-public-safe-record" \
  --outdir projects
```

For unclear or private projects, generate into ignored local `outputs/project-records/` instead.

## Evidence Boundary

Project records are Harbor-style public memory. They document workflow use and decision boundaries. They do not establish that a biological mechanism is causal, a clinical model is deployable, a manuscript has been submitted, or a paper will be accepted.
