# Repository Layout

OCEAN keeps the public repository small enough to understand from the first
screen.

| Region | Purpose |
|---|---|
| `skills/ocean/` | Installable skill, runtime references, adapters, and bounded tool wrappers |
| `docs/` | Public architecture and bilingual usage guides |
| `projects/` | Concise, owner-approved public project milestones |
| `tests/` | Small deterministic CI checks and non-sensitive fixtures |
| `examples/` | Reusable source-safe examples |
| `assets/` | Logos and README media |
| `outputs/` | Ignored local reports, experiments, logs, scorecards, and generated packets |
| `.github/` | Continuous integration |

## Public boundary

The repository should contain reusable product behavior, not internal working
history.

Keep out of GitHub:

- raw model responses and provider-by-provider run logs;
- generated evaluation artifacts and manual working notes;
- local availability probes and generated tool artifacts;
- private development and decision materials;
- unpublished manuscript text, reviewer correspondence, and collaborator notes;
- patient-level or controlled data;
- API keys, local paths, credentials, and private environment files.

The installable behavior is defined by `skills/ocean/SKILL.md` and
`skills/ocean/references/`. Generated work belongs in `outputs/`, which is
ignored by Git.

## Tests

`tests/` contains only the compact checks needed to keep the public package
usable:

- JSON and skill-package validation;
- concise public project-record validation;
- software evidence-boundary regressions;
- bilingual tool-index coverage;
- small routing and manuscript-channel fixtures.

Passing these tests means the repository contract is intact. It does not prove
scientific correctness, model superiority, or clinical validity.
