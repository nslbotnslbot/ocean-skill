# Project Start Gate and GitHub Sync Ticket

Use this gate when an OCEAN conversation is no longer a casual question and has become a traceable research project, manuscript audit, proposal route, validation plan, or collaboration workflow.

This reference does not turn OCEAN into a project release framework. Its purpose is to make project-start decisions explicit, preserve public-safe boundaries, and create a GitHub-ready sync ticket when a new research analysis should be recorded.

## Contents

- Purpose
- Trigger Decision
- Project Classes
- Required Artifacts
- GitHub Sync Rules
- Output Template
- Stop Conditions

## Purpose

- Decide when a new OCEAN research analysis should become a tracked project record.
- Prevent important research work from remaining only in a chat transcript.
- Preserve the first evidence boundary before later claims drift.
- Create a public-safe GitHub sync ticket without publishing private data, raw manuscripts, patient data, collaborator-only decisions, or confidential review text.

## Trigger Decision

Open the Project Start Gate when at least three of these signals are present:

1. A concrete research object exists: project, manuscript, proposal, dataset, DOI/preprint, claim set, review comments, or collaboration case.
2. The user asks OCEAN to analyze, audit, design, validate, plan, compare, route, or preserve the work rather than only answer a narrow question.
3. The work will use one or more OCEAN modules and produce an artifact that should be reused later.
4. There is an expected next action: source packet, claim audit, validation plan, experiment route, manuscript strategy, or Harbor memo.
5. The privacy boundary can be stated: what may be public, what must stay local/private, and what is not yet confirmed.

Do not open the gate for:

- casual explanation, brainstorming, or one-off terminology questions;
- sensitive clinical or collaborator material with no safe boundary;
- user requests that explicitly say not to record, not to publish, or not to update GitHub;
- work whose only output is a private analysis with no reusable artifact.

If only one or two trigger signals are present, ask whether to create a tracked project record or keep the analysis temporary.

## Project Classes

| Class | Meaning | Default action |
|---|---|---|
| New tracked project | First serious OCEAN run for a project | Create Project Start Card, Harbor seed, and GitHub Sync Ticket |
| Continuation project | Follow-up on an existing OCEAN project | Update Harbor memo or add dated process entry |
| Public-safe application case | Project owner has approved public-safe tracking | Update public tracker or case note with confirmed facts only |
| Private-local project | Useful research record but not public-safe | Keep local/project-private record; do not push public details |
| Temporary analysis | Not enough evidence or user does not want persistence | Answer normally; no project record |

## Required Artifacts

When the gate opens, create these artifacts before or alongside the first substantive module output:

1. **Project Start Card**
   - project id, title, date, domain lane, project class, status, owner/user boundary, intended OCEAN modules, and current evidence state.
2. **Evidence Boundary Snapshot**
   - inspected, not inspected, cannot conclude, next evidence needed, and confidential material excluded from public records.
3. **Module Route**
   - starting module, expected module chain, stop condition, and first handoff ticket.
4. **Harbor Seed**
   - initial decision memo placeholder, unresolved risks, next-action register, and reuse warning.
5. **GitHub Sync Ticket**
   - target files, public-safe summary, excluded material, suggested branch, commit message, and whether remote push is approved.

## GitHub Sync Rules

- Public GitHub records must be public-safe summaries, not raw scientific evidence.
- Never commit API keys, patient-level data, unpublished raw data, private manuscript text, private peer review, journal correspondence, collaborator-only notes, or unconfirmed submission outcomes.
- When a repository is available and the user has requested GitHub updating, OCEAN should prepare commit-ready files and a sync ticket.
- Remote push should happen only when the user has approved the GitHub update for that project/session or the task explicitly asks to push/update GitHub.
- If push is not allowed, output the GitHub Sync Ticket and stop at local files.
- If the project is private-local, write local records only and mark `remote_push: not_allowed`.
- If public status is not confirmed, use `To be updated` or `OCEAN planning`; do not infer submission, review, revision, acceptance, or publication status.

## Output Template

```markdown
# OCEAN Project Start Card

| Field | Value |
|---|---|
| Project ID |  |
| Project title |  |
| Start date |  |
| Project class | New tracked project / Continuation / Public-safe application case / Private-local / Temporary |
| Domain lane | Medical research / Biological research / Medical AI / Biological AI / Omics / Clinical / KG/database / Other |
| Starting module |  |
| Expected module route |  |
| Status | OCEAN planning / OCEAN pre-submission audit / To be updated |
| Public-safe? | yes / no / unclear |

## Evidence Boundary Snapshot

- Inspected:
- Not inspected:
- Cannot conclude:
- Next evidence needed:
- Excluded from public record:

## Module Route

| Step | Module | Planned artifact | Stop condition |
|---:|---|---|---|

## Harbor Seed

- Current decision:
- Unresolved risks:
- Next-action register:
- Reuse warning:

## GitHub Sync Ticket

| Field | Value |
|---|---|
| Target repository |  |
| Suggested branch |  |
| Files to add/update |  |
| Commit message |  |
| Remote push | approved / needs approval / not allowed |
| Public-safe summary |  |
| Excluded material |  |
```

## Stop Conditions

Stop or mark incomplete when:

- the user has not approved persistence and the project boundary is unclear;
- the requested public record would expose confidential material;
- no evidence boundary can be stated;
- the analysis would require invented project status, source details, validation results, author roles, or publication outcomes;
- the repository state is dirty or behind and the update would mix unrelated changes.
