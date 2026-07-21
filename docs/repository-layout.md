# Repository Layout

OCEAN separates the installable skill from development evidence and public documentation.

| Region | Ownership | Publish policy |
|---|---|---|
| `skills/ocean/` | Installable runtime skill, references, adapters, and bounded tool wrappers | Required for skill releases |
| `validation/` | Cases, protocols, fixtures, scorecards, generated eval artifacts, and regression scripts | Public-safe development evidence only |
| `docs/` | User-facing architecture, evaluation summaries, and case studies | No private research strategy or hidden answer keys |
| `examples/` | Small reusable examples | Source-traceable and redistribution-safe |
| `assets/` | Logos and README media | Optimized public assets only |
| `outputs/` | Local generated work | Ignored except `.gitkeep` |
| `.github/` | CI and repository automation | Deterministic checks only |

## Canonical instruction sources

`skills/ocean/SKILL.md` is the runtime entrypoint. Files under `skills/ocean/references/` are the canonical module and contract instructions. `skills/ocean/manifest.yaml` is a human-readable inventory; Codex does not auto-load it.

The `skills/ocean/static/` tree is retained temporarily for compatibility with existing structural checks. Do not add new behavior there. New or changed behavior belongs in `SKILL.md` and `references/` until the compatibility tree is removed in a separately tested cleanup.

## Generated tool wrappers

The bioinformatics tool catalog contains many generated per-tool entrypoints. Shared behavior belongs in `skills/ocean/scripts/tools/common/`; per-tool files should contain configuration or a thin dispatcher only. Consolidating duplicate dispatchers is planned as a compatibility-sensitive follow-up, because existing public command paths must not disappear without migration aliases and tests.

## Validation policy

Keep historical validation records reproducible and append-only where practical. New generated result sets should live under a named subdirectory rather than expanding the validation root. Never commit secrets, local model configuration, private manuscripts, patient-level data, or licensed full text.
