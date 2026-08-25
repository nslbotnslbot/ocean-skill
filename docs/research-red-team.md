# OCEAN Research-Package Red-Team

Research-package red-team is an **optional specialization under Design and
Audit**. It is used only when a user explicitly requests a package-level
Go / Rework / Stop-style decision or minimum-validation triage for a
biomedical AI, clinical-prediction, database, or knowledge-graph study.

It does not replace the five OCEAN modes and must not be used for ordinary
Explore, ordinary Audit, Revise, or Track requests.

## What it checks

When the supplied material is traceable and sufficiently complete, the review
can inspect the study framing, claims or plan, data/cohort boundary,
train/validation/test design, source provenance, comparator and benchmark
fairness, external validation, calibration or decision-utility boundary, and
the relation between claims, figures, and available analyses.

## Preconditions and outcomes

The user must supply, or authorize inspection of, a research package with a
study aim, central claims or plan, data/cohort information, validation design,
and at least one traceable source packet or locator. Otherwise OCEAN returns
**Cannot decide** and states the smallest missing input; it must not invent a
fatal flaw or a publication forecast.

A full red-team output contains a Fatal Evidence Bottleneck, study-validity
verdict, Minimum Validation Package, Go / Rework / Stop / Cannot decide,
reviewer-risk ticket, and collaboration-input boundary. These are bounded
review aids, not proof of scientific validity, publishability, clinical
readiness, ethics approval, or authorship.

There are no published performance claims for this route. A preregisterable
release protocol for any future evaluation is in
[`research-package-red-team-evaluation-protocol.md`](research-package-red-team-evaluation-protocol.md).

The canonical runtime rules are in
[`skills/ocean/references/research-red-team.md`](../skills/ocean/references/research-red-team.md)
and the compact output layout is in
[`skills/ocean/references/research-red-team-template.md`](../skills/ocean/references/research-red-team-template.md).
