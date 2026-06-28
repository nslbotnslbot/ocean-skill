# Changelog

## Unreleased

### Added

- Added `skills/ocean/references/reviewer-to-idea.md`, a workflow for turning peer review reports, reviewer comments, editor letters, rebuttal exchanges, or public review histories into evidence-bound repair ideas, extension ideas, independent project ideas, and collaboration opportunities.
- Wired the reviewer-to-idea workflow into `skills/ocean/SKILL.md`, `references/output-contract.md`, and `agents/openai.yaml`.

### Evidence Boundary

Reviewer comments are treated as pressure signals, not facts, novelty proof, publication guarantees, or scientific validation. OCEAN must still check manuscript evidence and external literature before calling an idea supported, novel, or publishable.

## v0.1.0 - 2026-06-28

Initial public release candidate for **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**, a Codex-compatible skill for scientific claim auditing, biomedical evidence review, AI-for-Science manuscript evaluation, journal positioning, and collaboration boundary analysis.

### Added

- Codex skill entry point at `skills/ocean/SKILL.md`.
- Repository-level `AGENTS.md` for project instructions.
- OCEAN module map: Sonar, Current, Reef, Iceberg, Anchor, Compass, Harbor.
- Standard OCEAN output contract for evidence-bound reports.
- Helper scripts for claim-table generation/checking and review skeleton generation.
- Public evaluation materials and release-validation log under `skills/ocean/evals/`.
- MIT `LICENSE`.

### Validation Summary

- Strict Forward Eval Round 1 passed for Cases 1, 2, 3, 5, and implicit-trigger Case 7 using source-traceable AlphaFold and KDGene packets.
- Anti-Hallucination Gate Rounds 2-3 passed six insufficient/unsafe-material scenarios: text missing, data missing, method missing, evidence-type mismatch, source not traceable, and logical contradiction.
- Strict Forward Eval Round 4 passed a real-article adversarial matrix: three public article packets paired with six unsafe user claims each.
- Strict Forward Eval Round 5 passed contamination-resistance replay plus 10 new public-study packets, with 19 counted checks rejecting or downgrading 19 unsafe claims.
- Packaging gate passed script execution, manual frontmatter validation, `agents/openai.yaml` parsing, `.gitignore` output protection, MIT license presence, and official `quick_validate.py` in a temporary PyYAML environment.
- Post-release GitHub install recognition test passed: `skills/ocean` installed from `nslbotnslbot/ocean-skill` and `$ocean` was recognized in a fresh Codex session, then the temporary install was removed.

### Evidence Boundary

These validation records test OCEAN's workflow behavior: whether it preserves inspected / not inspected / cannot conclude / needed-next boundaries and avoids unsupported claims. They do not prove the scientific correctness of any cited paper, preprint, benchmark, dataset, peer review report, or biomedical conclusion.

### Known Limits

- Many evaluation packets are abstract-level or source-packet-level rather than full-paper audits.
- OCEAN should continue to request full text, figures, methods, supplementary materials, code, datasets, external validation, peer review reports, and provenance records when those materials are needed for stronger conclusions.
- The release-validation log is a workflow validation record, not a scientific evidence database.
