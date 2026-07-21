# Harbor Decision Memory

Use Harbor when OCEAN needs to preserve a final report, decision memo, collaboration boundary, handoff record, or reusable project memory from prior module outputs.

Harbor is not a place to invent missing conclusions. Its job is to store what has been checked, what remains uncertain, what decisions were made, and what should be done next.

## Contents

- Purpose
- Trigger
- Inputs
- Safety Rules
- Workflow
- Output Artifact
- Stop Conditions
- Failure Modes

## Purpose

- Convert module outputs into a stable audit report or decision memo.
- Preserve inspected/not-inspected boundaries for later work.
- Record collaboration contribution boundaries without promising authorship.
- Keep next actions traceable to evidence gaps.
- Prevent old conclusions from being reused without their evidence boundary.

## Trigger

Read this file when the user asks to:

- summarize or preserve an OCEAN run;
- create a final audit report, decision memo, or project memory;
- start a persistent OCEAN project record or decide whether a new analysis should be tracked;
- record collaboration roles, contribution boundaries, or authorship-related notes;
- prepare a reusable report from Sounding/Current/Reef/Iceberg/Anchor/Compass outputs;
- compare what has changed since an earlier run.

## Inputs

Harbor can start from:

- complete OCEAN module outputs;
- review report notes;
- claim-evidence matrix;
- validation plan;
- research strategy card;
- collaboration notes;
- user decision or next-action list.
- a Project Start Card, Evidence Boundary Snapshot, Module Route, or GitHub Sync Ticket from `project-start-gate.md`.

## Safety Rules

- Do not add new scientific evidence at Harbor unless explicitly inspected.
- Do not turn planned contribution into completed contribution.
- Do not infer authorship, acceptance, review outcome, or PI agreement.
- Preserve uncertainty and stop conditions.
- If prior outputs are stale, mark them as historical rather than current evidence.
- Keep decisions separate from evidence. A decision can be recorded as a user/project choice, but it must not be treated as new scientific support.
- For collaboration or authorship questions, record contribution evidence and boundary warnings; do not decide authorship from incomplete notes.
- For GitHub sync, record only public-safe project metadata, module route, evidence boundary, and next-action summaries. Do not publish raw manuscripts, patient-level data, unpublished raw data, private peer review, journal correspondence, collaborator-only notes, or API keys.
- Remote push requires user approval for that project/session or an explicit request to update GitHub. If approval is missing, create the sync ticket and stop at local records.

## Workflow

1. **Collect artifacts**
   - List which module outputs are being preserved.
2. **Project start gate**
   - If this is the first serious OCEAN run for a project, apply `project-start-gate.md` and create a Project Start Card, Evidence Boundary Snapshot, Module Route, Harbor Seed, and GitHub Sync Ticket.
3. **Normalize decisions**
   - Separate facts inspected, interpretations, decisions, recommendations, and open questions.
4. **Preserve evidence boundary**
   - Record inspected/not inspected/cannot conclude/needed next.
5. **Contribution boundary**
   - Record advisory, analysis, writing, validation, data, wet-lab, or authorship-relevant tasks only if provided.
6. **Next-action register**
   - Convert gaps into owners, priority, effort, and evidence required.
7. **GitHub sync ticket**
   - If the project should be persisted in GitHub, record target files, public-safe summary, excluded material, suggested branch, commit message, and remote-push status.
8. **Reuse warning**
   - State what must be rechecked before future reuse.

## Required Harbor Artifacts

Harbor outputs are considered complete only when they include these five artifacts:

1. **Decision memo**
   - What is decided now, what remains unresolved, and what cannot be claimed.
2. **Evidence boundary ledger**
   - A durable record of checked, unchecked, cannot-judge, and next-needed items.
3. **Contribution boundary record**
   - What contribution evidence exists, what is only planned, and what cannot justify authorship or role claims yet.
4. **Next-action register**
   - Concrete next steps tied to evidence gaps, with owner/role, priority, and required evidence.
5. **Reuse note**
   - What the memo can be reused for, what must be rechecked, and what it must not be used as evidence for.
6. **GitHub sync ticket** when the work is a new tracked project or a public-safe application case
   - Target repository/files, branch, commit message, public-safe summary, excluded material, and push approval state.
   - For public OCEAN projects, target the canonical `projects/<slug>/README.md` record and append a dated progress entry rather than creating a second tracker.

If one artifact cannot be filled because evidence is missing, keep the heading and write the missing boundary rather than deleting it.

## Output Artifact

```markdown
一、Harbor任务定义
- Report/memory target:
- Artifacts being preserved:
- Decision context:
- Evidence state:

二、Final audit / decision memo
- Main verdict:
- What can be claimed now:
- What must remain hypothesis:
- What should be removed or downgraded:
- What would justify stronger claims:

三、Evidence boundary ledger
| Item | Status | Evidence basis | Reuse warning |
|---|---|---|---|

四、Collaboration / contribution boundary
| Contribution area | Provided evidence | Current level | Authorship boundary warning | Next record needed |
|---|---|---|---|---|

五、Next-action register
| Action | Why needed | Owner/role | Priority | Evidence required |
|---|---|---|---|---|

六、GitHub sync ticket
| Field | Value |
|---|---|
| Target repository |  |
| Suggested branch |  |
| Files to add/update |  |
| Commit message |  |
| Remote push | approved / needs approval / not allowed |
| Public-safe summary |  |
| Excluded material |  |

七、Harbor边界
- 已检查:
- 未检查:
- 不能判断:
- 下一步需要:

八、Reuse note
- This memo can be reused for:
- Must be rechecked before reuse:
- Do not reuse as evidence for:
```

## Stop Conditions

Stop or mark incomplete when:

- no module outputs or source notes are available;
- the user asks Harbor to decide authorship or publication outcome from insufficient notes;
- prior conclusions lack evidence boundaries;
- the requested report would require new scientific evidence that has not been inspected.
- the requested GitHub update would expose private material or mix with unrelated dirty repository changes.

## Failure Modes

- Adding new claims during report preservation.
- Converting a plan into completed work.
- Forgetting uncertainty and missing evidence.
- Treating old outputs as current evidence without checking.
- Promising authorship, acceptance, or collaboration outcomes.
- Producing a generic summary without a decision memo, evidence ledger, contribution boundary, next-action register, and reuse note.
- Auto-pushing private project details to GitHub without a public-safe boundary and user approval.
