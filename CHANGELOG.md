# Changelog

## Unreleased

- Added full OCEAN workflow protocol/case seeds for paper, idea, proposal, review-comment, and resource/KG inputs.
- Added module handoff rules so multi-module runs preserve explicit evidence packets, unresolved risks, and stop conditions.
- Added optional Reef API adapter registry for official biomedical databases, registries, and resource tools without making OCEAN dependent on any API.
- Added manual triage notes for the 11 M2 `needs_review` rows.
- Added Reef Strict Eval R1 with 35/35 usable outputs across seven enabled model lanes and manual triage of three needs-review rows.
- Tightened Reef/API and eval-output instructions to avoid uninspected endpoint invention and `<think>`/private-reasoning blocks.
- Added standalone module reference files for Current, Reef, Iceberg, Anchor, Compass, and Harbor, and wired them into OCEAN resource routing.
- Added OCEAN Module Strict Eval M2 scoring: a 12-point heuristic rubric, scorecard CSV, summary JSON, results note, and scorer script for 98 M1 all-module outputs.
- Added OCEAN Module Strict Eval M1 covering all seven modules with 14 cases across enabled model lanes; merged coverage reached 98/98 usable outputs after targeted timeout reruns.
- Clarified OCEAN's public scope as biomedical research across medical and biological research, with medical AI and biological AI as priority use cases.
- Added a public module responsibility and validation-status map in `docs/module-map.md`.
- Clarified in README and evaluation docs that Sounding remains the most heavily tested module while M1/M2 now add first all-module coverage and heuristic scoring; final source-grounded content review is still needed.
- Updated public evaluation notes for Sounding R3, including Gemini's completed 60/60 rerun after the initial HTTP 429 stop.
- Clarified the Sounding model-comparison set: Qwen, DeepSeek, Kimi, MiniMax, Gemini, Claude, and a Perplexity retrieval control group.
- Added Perplexity retrieval-control smoke support with raw response and source-packet capture.
- Added DeepSeek and Gemini live API slice results for Sounding Multi-Model Strict Eval R1.
- Renamed the OCEAN literature/evidence discovery module to **Sounding** across public docs, skill routing, references, eval protocols, runner names, and README artwork.
- Kept public OCEAN module naming centered on **Sounding** while treating Perplexity only as a retrieval control group.
- Updated Sounding multi-model strict eval filenames and runner paths to use the `sounding-multimodel-*` naming pattern.

## v0.1.0

- Initial public OCEAN skill release with claim-evidence auditing, fixed output contract, evidence-boundary rules, validation logs, sample scripts, and installation instructions.
