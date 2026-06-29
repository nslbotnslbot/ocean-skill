# Changelog

## Unreleased

- Clarified the Sounding model-comparison set: Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and a Perplexity retrieval control group.
- Added Perplexity retrieval-control smoke support with raw response and source-packet capture.
- Added DeepSeek and Gemini live API slice results for Sounding Multi-Model Strict Eval R1.
- Renamed the OCEAN literature/evidence discovery module to **Sounding** across public docs, skill routing, references, eval protocols, runner names, and README artwork.
- Kept public OCEAN module naming centered on **Sounding** while treating Perplexity only as a retrieval control group.
- Updated Sounding multi-model strict eval filenames and runner paths to use the `sounding-multimodel-*` naming pattern.

## v0.1.0

- Initial public OCEAN skill release with claim-evidence auditing, fixed output contract, evidence-boundary rules, validation logs, sample scripts, and installation instructions.
