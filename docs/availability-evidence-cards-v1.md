# Availability Evidence Cards v1

## Public validation snapshot

OCEAN's first Availability Evidence Card evaluation used 70 real Europe PMC
CC BY JATS papers represented as checksum-bound PaperBundles. The experiment
was offline and excluded reference sections and their descendants.

The workflow inspected:

- 70/70 PaperBundles;
- 1,850 non-reference sections;
- 3,893 paragraph locators;
- 3,841 unique paragraph texts after exact-checksum grouping;
- 52 duplicate locators retained across grouped text.

It produced one fixed 14-dimension card per paper. A separate clean rerun
reproduced all 70 card files and the aggregate summary byte-for-byte.

## Bounded trace coverage

| Signal class | Cards with an explicit textual signal |
|---|---:|
| Data availability statement | 17/70 |
| Code availability statement | 5/70 |
| Data repository | 33/70 |
| Persistent identifier or accession | 30/70 |
| Controlled access | 1/70 |
| Request-based access | 4/70 |
| Third-party restriction | 0/70 |
| Metadata or data dictionary | 2/70 |
| License terms | 1/70 |
| Source data | 10/70 |
| Model weights | 2/70 |
| Prompt or configuration | 1/70 |
| Reproducibility environment | 5/70 |
| Version or commit | 24/70 |

The run located 474 resource candidates and retained 470 under the fixed
per-card review cap. It did not resolve any candidate.

## Corrections made before freezing

Two development probes exposed false-positive traps:

1. generic `to be added` wording in ordinary methods text was initially
   mistaken for a release placeholder;
2. a statement that checkpoints were used for inference was initially
   mistaken for checkpoint availability.

The frozen rules require release-field context for placeholders and explicit
availability, release, provision, or deposition wording for model artifacts.
Common request-based wording such as `available from the corresponding author
on reasonable request` is handled separately.

## What the result means

The evaluation establishes deterministic structural extraction and traceable
unknown states under the frozen corpus, configuration, and implementation.

It does **not** establish:

- that a URL, DOI, accession, repository, code release, model artifact, or
  environment exists or resolves;
- that artifacts are complete, usable, immutable, or sufficient to reproduce
  the paper;
- FAIR compliance, accessibility, ownership, consent, or license
  compatibility;
- detector precision, recall, cross-domain validity, or expert utility;
- scientific validity.

All cards require expert review. A missing signal means only
`not_explicitly_located`, never that the full paper or supplement omitted the
artifact.

## Next validation

The next release gate is expert evaluation on locked positive and negative
examples for all 14 dimensions, followed by an independently authorized
resource-resolution layer. Until then, this is a public research-software
preview, not a validated FAIR or reproducibility checker.
