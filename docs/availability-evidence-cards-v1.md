# Availability Evidence Cards v1: Protocol Preview

## Current implementation status

The repository contains a fail-closed schema and an evidence-boundary contract
for a proposed 14-dimension Availability Evidence Card. It does **not** yet
ship a card generator that turns papers, JATS XML, or PaperBundles into that
schema. The current `audit data-availability` CLI checks only user-declared
asset metadata and unresolved placeholders.

Therefore OCEAN does not currently claim that it can generate a 14-dimension
card, resolve repositories or identifiers, verify accessibility or licenses,
assess FAIR compliance, establish reproducibility, or report a completed
corpus-level evaluation.

## Proposed card boundary

The future card will inspect these dimensions independently:

1. data availability statement;
2. code availability statement;
3. data repository;
4. persistent identifier or accession;
5. controlled access;
6. request-based access;
7. third-party restriction;
8. metadata or data dictionary;
9. license terms;
10. source data;
11. model weights;
12. prompt or configuration;
13. reproducibility environment; and
14. version or commit.

For each dimension, the only structural states will be
`explicit_textual_signal` and `not_explicitly_located`. Neither is a quality,
availability, FAIR, or scientific-validity verdict. URLs, DOIs, repository
names, and accessions must remain `not_verified` until an authorized lookup.

## Required release evidence before stronger claims

Before this page can report a reproducible evaluation, a release must include:

- a deterministic card generator with schema and checksum regression tests;
- a versioned corpus manifest that records source, license, selection rule,
  access date, and content checksums;
- runner configuration, per-run manifest, and aggregate-summary procedure;
- an explicit statement of which material was inspected and excluded;
- locked expert positive and negative examples for all 14 dimensions; and
- reported error rates, abstention behavior, and cross-domain review results.

Until then, this is a public protocol preview, not a validated FAIR,
availability, or reproducibility checker.
