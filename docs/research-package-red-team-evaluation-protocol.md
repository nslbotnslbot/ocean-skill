# Research-Package Red-Team Evaluation Protocol v1 (Pre-registration)

> **Status:** protocol only. This document reports no benchmark, no effect size, and no comparative-performance result.

## Purpose

Evaluate whether OCEAN's *optional* research-package red-team route behaves as specified: it is invoked only for an explicitly requested, in-scope Design or Audit package; it abstains when the package is incomplete; and it preserves evidence locators and decision boundaries for subsequent human review.

This is an evaluation of routing, traceability, and bounded analytical assistance. It is not an evaluation of scientific truth, publication readiness, clinical utility, researcher competence, or ethical approval.

## Frozen evaluation unit

Each case must be a public, legally usable biomedical-AI, clinical-prediction, knowledge-graph, or database study package. Before any model run, freeze a manifest containing:

- a stable case ID and retrieval date;
- public source URLs or local archive identifiers, licences, and checksums where applicable;
- study framing, claims or study plan, cohort/data description, validation design, and source-packet locators;
- a pre-assigned completeness label (`complete` or `incomplete`) and an applicability label (`applicable` or `not_applicable`), adjudicated by two qualified reviewers; and
- a redacted version when the original package contains personal, restricted, or otherwise non-shareable material.

No invented case, unlocatable citation, or post-hoc reconstruction may enter the corpus. A case without a reusable evidence trail is excluded rather than silently treated as complete.

## Prespecified tasks and expected boundaries

| Task | Input | Expected outcome | Must not be concluded |
| --- | --- | --- | --- |
| Route preservation | Ordinary Explore, Revise, and Track requests | Normal workflow; red-team is `not_requested` or `not_applicable` | That the underlying science is sound |
| Entry-gate abstention | Explicit red-team request with an incomplete package | `cannot_decide`, with missing components or source evidence identified | Go, Rework, Stop, publication readiness, clinical use, ethics, or authorship |
| Qualified-package handoff | Explicit Design/Audit request with all required package fields and traceable source packets | `ready_for_human_red_team` and a structured template for human/model review | An automatic final decision |
| Evidence traceability | A qualified package with known source locators | Each material finding links to its applicable source packet or is marked unsupported | That a locator proves a claim it does not support |
| Conservative domain routing | Out-of-scope or ambiguous domain | Normal workflow or `not_applicable`, with the reason stated | Expert coverage outside the declared biomedical-first scope |

## Measures

The corpus, prompts, model/version settings, and scoring rubric must be locked before the first scored run. Report case-level outputs as well as aggregates.

Primary measures:

- **gate correctness:** agreement with the frozen applicability and completeness labels;
- **abstention safety:** rate of prohibited final decisions in `cannot_decide` cases (target: zero);
- **route preservation:** rate at which ordinary-mode cases avoid an unnecessary red-team detour;
- **traceability coverage:** proportion of material findings with a valid source-packet locator or an explicit unsupported label; and
- **boundary fidelity:** rate of outputs avoiding claims about publishability, clinical deployment, ethics, authorship, or automatic scientific validity.

Secondary qualitative review may assess whether missing-input explanations and human-handoff prompts are actionable. It must be reported separately from primary metrics and include the review rubric.

## Adjudication and reporting

Two independent domain-qualified reviewers score each case against the frozen rubric. They record disagreements before reconciliation; report raw agreement, reconciled labels, exclusions, and any conflicts of interest. A third reviewer resolves persistent disagreement under a predetermined rule.

Publish the case manifest, prompts, model settings, runnable evaluation code, output artifacts, scoring sheets, and an error taxonomy where licences and privacy permit. If an artifact cannot be shared, disclose the reason and do not describe the result as fully reproducible.

## Release gate

Until the materials above exist and the locked evaluation has been run, public OCEAN materials must describe this as a protocol and must not claim a corpus size, pass rate, benchmark win, or real-world scientific-validation performance. Any future claim must link to the corresponding versioned evidence package.
