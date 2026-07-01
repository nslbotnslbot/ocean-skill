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

## Safety Rules

- Do not add new scientific evidence at Harbor unless explicitly inspected.
- Do not turn planned contribution into completed contribution.
- Do not infer authorship, acceptance, review outcome, or PI agreement.
- Preserve uncertainty and stop conditions.
- If prior outputs are stale, mark them as historical rather than current evidence.

## Workflow

1. **Collect artifacts**
   - List which module outputs are being preserved.
2. **Normalize decisions**
   - Separate facts inspected, interpretations, decisions, recommendations, and open questions.
3. **Preserve evidence boundary**
   - Record inspected/not inspected/cannot conclude/needed next.
4. **Contribution boundary**
   - Record advisory, analysis, writing, validation, data, wet-lab, or authorship-relevant tasks only if provided.
5. **Next-action register**
   - Convert gaps into owners, priority, effort, and evidence required.
6. **Reuse warning**
   - State what must be rechecked before future reuse.

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

六、Harbor边界
- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

七、Reuse note
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

## Failure Modes

- Adding new claims during report preservation.
- Converting a plan into completed work.
- Forgetting uncertainty and missing evidence.
- Treating old outputs as current evidence without checking.
- Promising authorship, acceptance, or collaboration outcomes.
