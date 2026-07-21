# OCEAN Validation

This directory contains repository-development evidence. It is intentionally outside `skills/ocean/` so installing the skill does not copy historical eval artifacts into the runtime package.

## What belongs here

- reusable adversarial cases and evaluation protocols;
- public-safe result summaries, scorecards, and coverage records;
- bounded adapter fixtures and generated test artifacts;
- the append-only release validation log;
- repository regression scripts under `scripts/`.

## What does not belong here

- API keys, private model configuration, unpublished manuscripts, private patient or participant data;
- downloaded papers or copyrighted full text that cannot be redistributed;
- outputs presented as scientific evidence without source and provenance boundaries.

Historical files remain at this directory root to preserve existing links. New evaluation families should use a named subdirectory when they produce multiple artifacts. Runtime instructions must live in `skills/ocean/SKILL.md` or `skills/ocean/references/`, not here.

Validation prompts, expected outcomes, and scorer outputs are test material. OCEAN must never treat them as biomedical evidence.
