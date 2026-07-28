# OCEAN Repository Instructions

## Scope

OCEAN is a biomedical claim-evidence workflow for medical and biological
research. Its canonical runtime instructions are:

- `skills/ocean/SKILL.md`
- `skills/ocean/references/`

Use the smallest set of OCEAN modules that can answer the user's request. Do
not force a full seven-module audit onto a focused writing, planning, or
evidence question.

## Language

Respond in Chinese by default unless the user requests another language. Keep
scientific judgments direct, specific, and evidence-bounded.

## Evidence Boundary

- Distinguish inspected evidence from uninspected or unavailable material.
- Do not invent data, source details, sample sizes, results, journal
  requirements, or author contributions.
- Separate association, prediction, database annotation, text-mined
  co-occurrence, and causal evidence.
- State what cannot be concluded and what evidence is needed next.
- Do not turn model output, a software probe, or a passing repository test into
  a scientific claim.

## Manuscript Work

Determine the manuscript stage before editing. For a finished manuscript,
return clean replacement prose separately from audit notes and author queries.
Do not insert reviewer-style criticism, placeholders, or unsupported
strengthening into paste-ready text.

## Public Repository

Keep reusable skill behavior, public documentation, concise owner-approved
project milestones, and deterministic tests in GitHub. Keep raw model
responses, experimental logs, internal scorecards, private strategy, local
paths, credentials, unpublished manuscripts, reviewer correspondence, and
controlled data outside the repository.

Generated work belongs in ignored `outputs/`.

## Quality Checks

Before publishing repository changes, run:

```bash
python3 tests/check_json_files.py
python3 tests/validate_skill.py
python3 tests/check_project_records.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 skills/ocean/scripts/check_ocean_contracts.py --out outputs/ocean-contract-check.md
python3 skills/ocean/scripts/check_manuscript_revision_mode.py --out outputs/manuscript-revision-check.md
```
