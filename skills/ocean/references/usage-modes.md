# OCEAN User-Facing Modes

Use this reference before selecting modules. OCEAN should feel simple at the
surface, rigorous underneath, and traceable when the work becomes a project.

Users choose the outcome they need. OCEAN chooses the minimum necessary modules
internally.

## Mode Router

| Mode | User intent | Default visible output | Typical module route |
|---|---|---|---|
| **Explore** | Understand a paper, DOI, idea, field, or source landscape | OCEAN Decision Card plus a clear evidence-bounded explanation | Sounding; add Current or Reef only when needed |
| **Design** | Turn an idea, proposal, dataset, or reviewer concern into a study | Research route, decisive controls, main risks, next experiment | Compass + Anchor; add Sounding, Reef, or Iceberg as needed |
| **Audit** | Test claims, methods, validation, reproducibility, or submission readiness | Claim verdicts, evidence gaps, priority fixes | Iceberg + Anchor; add source/resource modules as needed |
| **Revise** | Polish, shorten, translate, or safely rewrite finished text | Clean replacement text first; notes and author queries separate | Silent bounded Iceberg check plus Manuscript Revision contract |
| **Track** | Record concise project status, decisions, next gate, or public boundary | Status, Progress, Next, Public Boundary | Harbor |

The explicit user request wins. Do not force a request into Audit merely
because the input is scientific.

## Classification Cues

### Explore

Choose Explore when the user asks to:

- explain or interpret a paper, abstract, figure, DOI, or research idea;
- prepare a journal club, student explanation, or field overview;
- find related evidence or understand what a source does and does not show;
- compare nearby literature without requesting a formal critique.

Use plain teaching language when the audience is a student or non-specialist.
Retain the evidence boundary without turning the answer into a reviewer report.

### Design

Choose Design when the user asks to:

- develop an idea, proposal, experiment, computational pipeline, or validation
  strategy;
- identify the most decisive control or the next highest-value analysis;
- turn evidence gaps, peer-review concerns, or available data into a feasible
  research route;
- distinguish an analysis-only study from a validation-free study.

Lead with the decision that changes the study. Do not produce an exhaustive
tool list when a small number of decisive controls would answer the question.

### Audit

Choose Audit when the user explicitly asks to:

- criticize, stress-test, review, score, or check claims;
- assess model leakage, benchmark fairness, external validation, mechanism,
  causality, clinical utility, or reproducibility;
- simulate reviewers or judge submission readiness;
- inspect whether database, knowledge-graph, omics, or model evidence supports
  a stronger conclusion.

Use Standard or Deep output only when the scope justifies it. Keep unsupported
claims at the safest level: hypothesis, association, prediction, mechanism, or
clinical benefit.

### Revise

Choose Revise when finished text is supplied for:

- polishing, shortening, translation, restructuring, or clarity;
- evidence-safe wording changes;
- title, abstract, Results, Discussion, figure legend, cover letter, or
  response-letter revision.

Return paste-ready prose without module labels, reviewer criticism, scores,
commands, or risk tables. Keep scientific caveats in the most appropriate
manuscript location and keep author-only questions outside the prose.

If the user asks both for critique and revision, separate the channels:

1. audit findings;
2. clean revised text;
3. author-only decisions, if any.

### Track

Choose Track when the user asks to:

- record project status, submission state, decisions, or the next gate;
- create or update a concise project page;
- preserve a public-safe project memory.

Use only:

1. Status
2. Progress
3. Next
4. Public Boundary

Distinguish submitted, awaiting screening, posted, under review, revised,
accepted, and published. Never infer a stronger state. Public GitHub updates
require user approval.

## Minimum Route Rules

- Paper explanation: Explore with Sounding only; add Current for field movement.
- Literature landscape: Explore with Sounding + Current.
- Database or knowledge-graph question: Explore or Audit with Reef; add Iceberg
  only for a scientific claim.
- New study or proposal: Design with Compass + Anchor; add source modules only
  when the design depends on literature or public resources.
- Finished manuscript wording: Revise with a silent evidence check.
- Explicit manuscript review: Audit with Iceberg + Anchor.
- Submission or project status: Track with Harbor.
- End-to-end research workflow: use several modules only when the handoffs are
  materially needed.

Never run all seven modules merely to demonstrate OCEAN.

## Visibility Rules

- Hide module names by default.
- Show a module name when the user asks how OCEAN reasoned, requests a
  module-by-module workflow, or needs to inspect a handoff artifact.
- Prefer one direct conclusion over a framework tour.
- Do not score unless the user asks or a comparative decision genuinely needs
  a rubric.
- Do not add journal positioning, authorship analysis, or project tracking to
  an unrelated request.

## Output Depth

- **Decision Card**: default for first-turn, narrow, learning, and ordinary
  evidence questions.
- **Standard**: explicit multi-claim audit, structured research plan,
  collaboration analysis, or journal-positioning decision.
- **Deep**: explicit full manuscript review, reviewer simulation, or detailed
  public report.
- **Manuscript Revision**: finished-text editing, regardless of audit depth.
- **Track Card**: project status using the four Track headings.

## Boundary Rules Across All Modes

- State what was inspected and what remains uninspected when it affects the
  conclusion.
- Never invent data, sample sizes, metrics, identifiers, citations, validation
  results, author roles, submission outcomes, or tool availability.
- A title or abstract is not full-text evidence.
- A registry record is not proof of efficacy or safety.
- A database association is not a mechanism.
- A prediction is not experimental validation.
- Matched measurements are required for sample-level correlation; separate
  experiments may support only group-level coordinated patterns.
- Analysis-only research can be valid; lack of independent validation remains
  a limitation that must be stated.
- A tool folder, wrapper, or API route shows orchestration capability, not that
  the tool is installed, licensed, executable, or scientifically appropriate.

## Examples

| User request | Mode | Visible behavior |
|---|---|---|
| "Explain this paper for an undergraduate journal club." | Explore | Clear explanation and evidence limits; no reviewer report |
| "Does this result prove a mechanism?" | Audit | Direct claim downgrade and the missing decisive evidence |
| "How should I test this idea?" | Design | Minimal research route and decisive controls |
| "Polish this Results paragraph." | Revise | Clean replacement text first; critique kept out |
| "Update the project after medRxiv submission." | Track | Precise status, progress, next step, public boundary |
