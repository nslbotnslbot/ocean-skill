# Research-Package Red-Team

Use this conditional contract only when all of the following are true:

1. the user explicitly requests a Go / Rework / Stop-style decision, a
   package-level pre-submission stress test, or minimum-validation triage;
2. the user-facing mode is **Design** or **Audit**;
3. the object is a biomedical AI, clinical-prediction, knowledge-graph, or
   database research package rather than a narrow claim, wording edit, or
   status update; and
4. the available material can identify the study framing, central claims or
   plan, data/cohort boundary, validation design, and at least one traceable
   source packet or locator.

This is an optional Audit/Design specialization. It does not replace Explore,
ordinary Audit, Revise, or Track, and it must not be activated merely because a
request is scientific or mentions publication.

## Purpose and Boundary

The red-team asks which documented evidence problem most limits the current
study package and what minimum additional validation could change that status.
It is a structured human-and-model review aid, not an automated validity,
publishability, authorship, ethics, or clinical-decision system.

Every bottleneck, verdict, and recommendation must be linked to inspected
material, a source packet, a locator, or an explicit unknown. A complete
package gate only establishes that a human red-team review can begin; it does
not establish that any scientific claim is true.

## Entry Gate

Before using the full template, record:

- study aim and intended claim ceiling;
- central claims, manuscript, or a sufficiently concrete study plan;
- data/cohort and train/validation/test boundary where applicable;
- validation, comparator, calibration, or reproducibility plan where
  applicable; and
- at least one traceable source packet or source locator.

For a file-based package, `scripts/ocean.py red-team-gate` can check this
declared minimum structure. Its output is only one of:

- `not_requested`: retain the selected normal OCEAN mode;
- `not_applicable`: the request is outside Design/Audit or the supported
  package domains;
- `cannot_decide`: the evidence package is incomplete or not traceable; or
- `ready_for_human_red_team`: the declared inputs are sufficient to start a
  human-and-model review.

The gate never emits Go, Rework, or Stop.

## Decision Semantics

- **Cannot decide**: required material is missing, non-traceable, contradictory
  without resolution, or too incomplete to identify a defensible bottleneck.
  State the smallest missing input instead of guessing.
- **Go**: no documented fatal bottleneck remains for the *stated limited
  claim* after the available validation package is inspected. It never means
  publication acceptance, clinical readiness, ethical approval, or a general
  scientific-validity guarantee.
- **Rework**: a documented, remediable bottleneck limits the stated claim and
  a minimum validation package can be specified.
- **Stop**: a documented blocker makes the current stated route unsuitable
  within its declared scope or constraints. State whether the conclusion,
  data access, ethics, or validation route causes the stop; do not use this
  label as an unsupported prediction of project or publication failure.

## Required Output

Use `research-red-team-template.md` only after the entry gate. The full review
contains:

1. evidence boundary and package-input completeness;
2. Fatal Evidence Bottleneck, or an explicit statement that none can be
   identified from the material;
3. study-validity verdict at the strongest supported claim level;
4. a minimum validation package with pass criteria;
5. Go / Rework / Stop / Cannot decide with its evidence basis;
6. reviewer-risk ticket; and
7. collaboration-input boundary.

For incomplete packages, return only the bounded Cannot-decide form and the
next required materials. Do not manufacture a fatal flaw, cost estimate,
reviewer objection, journal tier, author role, or publication probability.

For a file-based full review record, `scripts/ocean.py red-team-review-check`
validates that every required conclusion has either a declared source-packet
locator or an explicit-unknown label with its next required input. It verifies
the record structure only; a passing check does not establish that the cited
source proves the conclusion.

## Stop Conditions

Stop the full red-team route when:

- the request is Explore, Revise, Track, or ordinary Audit;
- the object is a title, abstract, isolated sentence, or untraceable memory;
- source locators, data/cohort boundaries, or validation information required
  for the requested conclusion are unavailable;
- the next step would expose private, patient-level, paid, key-protected, or
  unpublished material without authorization; or
- the user asks for a guarantee of publication, deployment, authorship, or
  clinical benefit.
