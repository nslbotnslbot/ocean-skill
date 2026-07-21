# Project Start Gate R1 Results

Run date: 2026-07-10

## Purpose

Test the first Harbor Project Start Gate implementation. The goal was to check whether OCEAN can create a persistent, public-safe project-start record and GitHub Sync Ticket without publishing private scientific materials.

## Case

Smoke case: `Example biomedical project`

Input boundary:

- Inspected: project title, user intent
- Not inspected: raw data, manuscript
- Cannot conclude: scientific validity, publication status
- Next evidence needed: source packet, claim table
- Excluded from public record: raw data, private manuscript, API keys

## Results

| Check | Result | Notes |
|---|---|---|
| `create_project_start_record.py` smoke run | pass | Generated Project Start Card, Harbor Seed, GitHub Sync Ticket, and JSON state under `/private/tmp/ocean-project-start-smoke/`. |
| GitHub Sync Ticket boundary | pass | Remote push was marked `needs approval`; excluded material was preserved. |
| `check_ocean_contracts.py` | pass | 34/34 checks passed after wiring `project-start-gate.md` into the skill and artifact contract. |
| `git diff --check` | pass | No whitespace errors. |
| Python compile | pass after cache rerun | First compile attempt was blocked by sandboxed macOS pycache path; rerun with `PYTHONPYCACHEPREFIX=/private/tmp/ocean-project-sync-pycache` passed. |

## Boundary

This was a structural and workflow smoke test only. It did not test whether a real scientific project should be made public, did not inspect raw data, and did not push generated project records to GitHub.

## Decision

Project Start Gate R1 is usable as a Harbor-level persistence mechanism for new OCEAN research projects. Remote GitHub updates remain gated by public-safe boundaries and user approval.
