# Changelog

## Unreleased

- Clarified OCEAN's public scope as biomedical research across medical and biological research, with medical AI and biological AI as priority use cases.
- Added a public module responsibility and validation-status map in `docs/module-map.md`.
- Clarified in README and evaluation docs that current strict module-specific testing is concentrated on Sounding; other modules are designed but still need standalone evals.
- Updated public evaluation notes for Sounding R3, including Gemini's completed 60/60 rerun after the initial HTTP 429 stop.
- Clarified the Sounding model-comparison set: Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and a Perplexity retrieval control group.
- Added Perplexity retrieval-control smoke support with raw response and source-packet capture.
- Added DeepSeek and Gemini live API slice results for Sounding Multi-Model Strict Eval R1.
- Renamed the OCEAN literature/evidence discovery module to **Sounding** across public docs, skill routing, references, eval protocols, runner names, and README artwork.
- Kept public OCEAN module naming centered on **Sounding** while treating Perplexity only as a retrieval control group.
- Updated Sounding multi-model strict eval filenames and runner paths to use the `sounding-multimodel-*` naming pattern.

## v0.1.0

- Initial public OCEAN skill release with claim-evidence auditing, fixed output contract, evidence-boundary rules, validation logs, sample scripts, and installation instructions.
