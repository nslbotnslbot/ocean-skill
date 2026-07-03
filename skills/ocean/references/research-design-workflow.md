# Research Design Workflow

Use this reference when OCEAN needs to turn an idea, paper, proposal, reviewer concern, dataset seed, or collaboration question into an evidence-bounded research workflow.

OCEAN is a research process skill. It should help design the next reliable scientific step, not merely summarize papers, aggregate databases, or produce attractive but unsupported ideas.

## Contents

- Purpose
- Trigger
- Design Loop
- Design Gates
- Output Artifact
- Module Responsibilities
- Stop Conditions
- Failure Modes

## Purpose

- Convert uncertain biomedical research inputs into a traceable workflow.
- Keep the workflow grounded in inspected evidence, missing evidence, and explicit stop conditions.
- Make research design decisions auditable: why this aim, why this validation, why this resource, why this handoff.
- Preserve the user's contribution boundary and next actions.

## Trigger

Read this file when the user asks about:

- designing a research project, proposal, study, validation plan, or manuscript revision route;
- turning a one-sentence idea into a research workflow;
- deciding what evidence is needed before a claim, experiment, or collaboration can move forward;
- making OCEAN more like a structured scientific workflow rather than a single-module answer;
- coordinating Sounding, Current, Reef, Iceberg, Anchor, Compass, and Harbor around one project.

## Design Loop

Use this loop for research design cases:

1. **Question Frame**
   - Define the biological, medical, methodological, or collaboration question.
   - Separate completed evidence from planned work.
2. **Evidence Boundary**
   - State inspected sources, missing sources, cannot-conclude items, and needed next evidence.
3. **Source / Resource Packet**
   - Use Sounding for literature/source packets.
   - Use Reef for data resources, databases, KGs, registries, cohorts, benchmarks, and optional API packets.
4. **Claim Calibration**
   - Use Iceberg to downgrade unsupported mechanism, causal, clinical, benchmark, novelty, authorship, or publication claims.
5. **Validation Gate**
   - Use Anchor to define minimum checks, pass criteria, leakage controls, replication, and external/biological/clinical validation requirements.
6. **Research Route**
   - Use Compass to choose conservative, balanced, ambitious, or rescue/revision routes based on evidence state.
7. **Decision Memory**
   - Use Harbor to preserve the decision memo, assumptions, unresolved risks, contribution boundary, and next-action register.

## Design Gates

Every research design answer should include gate logic:

| Gate | Must answer | Failure state |
|---|---|---|
| Source gate | What sources or materials were inspected? | Stop if only title/idea evidence is available for a strong claim. |
| Resource gate | Which data/database/KG/registry resources are relevant and traceable? | Stop if provenance, identifier, access, or evidence type is unclear. |
| Claim gate | What can be claimed now, and what must be downgraded? | Stop if downstream planning depends on an unsupported claim. |
| Validation gate | What minimum check would strengthen the claim? | Stop if validation target, input, or pass criterion is undefined. |
| Feasibility gate | What data, code, collaborator, time, or ethics condition is required? | Stop if feasibility depends on unavailable or private resources. |
| Decision gate | What route is chosen, rejected, or deferred? | Stop if no evidence-bounded route can be selected. |

## Output Artifact

Use this compact artifact when the main task is research design:

```markdown
一、Research Design任务定义
- Starting input:
- Research question:
- Evidence state:
- Desired decision:

二、OCEAN Design Loop
| Step | Module | Artifact | Evidence boundary | Stop condition |
|---|---|---|---|---|

三、Design Gates
| Gate | Current state | Pass / needs work / stop | What is needed next |
|---|---|---|---|

四、Recommended Research Route
| Route | Evidence basis | What it tests | Required resources | Main risk | Verdict |
|---|---|---|---|---|---|

五、Claim and Validation Boundary
- What can be claimed now:
- What must remain hypothesis:
- Minimum validation before stronger claims:
- What not to say:

六、Contribution and Workflow Boundary
- User's possible role:
- Work that is advisory only:
- Work that could become substantive contribution:
- Authorship/collaboration caveat:

七、Handoff Ticket
| Next module | Reason | Input packet | Stop condition |
|---|---|---|---|
```

## Module Responsibilities

| Module | Research-design responsibility |
|---|---|
| Sounding | Build the source packet and Negative Space before novelty or evidence claims. |
| Current | Bound field movement and trend claims; do not infer dominance from sparse search. |
| Reef | Route data resources and API packets; separate resource metadata from biological/clinical proof. |
| Iceberg | Calibrate claims and produce safe rewrites before validation or planning. |
| Anchor | Convert gaps into validation tasks with inputs, pass criteria, and stop conditions. |
| Compass | Select evidence-bounded research routes and experiment/proposal strategy. |
| Harbor | Preserve final decision memory, contribution boundary, stale-evidence flags, and next actions. |

## Stop Conditions

Stop or route backward when:

- the user asks for a research plan from an unsupported mechanism, clinical, or novelty claim;
- a proposal claims completed evidence but only planned work is provided;
- a database/API/resource record is needed but no traceable identifier or official source is available;
- validation pass criteria cannot be defined;
- patient-level, private, paid, or unpublished data would need external submission without explicit approval;
- the task is only a summary and does not require OCEAN workflow.

## Failure Modes

- Producing generic brainstorming instead of a module-by-module workflow.
- Treating research design as evidence that the research already works.
- Skipping claim downgrade before experiment design.
- Treating API/database output as mechanism or clinical proof.
- Forgetting contribution boundary and decision memory.
