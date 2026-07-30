# Availability Audit

Use this reference when the user asks whether a manuscript, project, dataset,
code repository, model, or analysis package is ready to share, submit, or
reproduce.

This is an evidence-boundary audit. It does not turn a repository name, URL,
DOI, accession, license token, or availability sentence into proof that an
artifact exists, resolves, is complete, is reusable, or satisfies FAIR
principles.

## When To Use

Use this contract for:

- data and code availability statements;
- repository and accession checks;
- controlled-access and request-based data routes;
- source-data and data-dictionary planning;
- model-weight, prompt, configuration, and environment availability;
- release placeholders such as unresolved DOI, URL, accession, or repository
  fields;
- pre-submission reproducibility packaging.

Use the minimum necessary OCEAN modules:

- **Reef** for repository, registry, identifier, access, provenance, and
  license routing;
- **Anchor** for reproducibility, environment, run-command, and rerun checks;
- **Iceberg** when an availability statement is being used to support a
  stronger reproducibility or transparency claim;
- **Harbor** for the final release checklist and unresolved author actions.

## Required Evidence Boundary

Start every audit by recording:

1. what files, statements, repository records, and identifiers were inspected;
2. what was not inspected, including supplements and controlled resources;
3. which candidates were only syntactically located and not resolved;
4. what cannot be concluded;
5. what author input or external verification is required next.

Never describe an unlocated artifact as absent from the full publication.
Never describe an unverified candidate as available.

## Fourteen Dimensions

Audit these dimensions independently:

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
13. reproducibility environment;
14. version or commit.

For each dimension, use only:

- `explicit_textual_signal`: the inspected material contains a traceable
  expression relevant to the dimension;
- `not_explicitly_located`: the configured inspection did not locate such an
  expression.

Neither state is a quality verdict. A signal does not establish correctness,
completeness, accessibility, or compliance.

## Candidate States

Repository names, URLs, DOIs, and accessions must remain:

```text
verification_state: not_verified
```

Unresolved release placeholders must remain:

```text
verification_state: requires_author_resolution
```

Each retained item should include a source locator, source-text checksum, and
bounded excerpt. Group exact duplicate text by checksum while preserving every
locator.

## Stop Conditions

Stop and ask for more evidence when:

- the full statement, supplement, or source-data package was not inspected;
- a repository or identifier has not been resolved through an authorized
  public lookup;
- access requires credentials, patient-level data, a data-use agreement, or
  institutional approval;
- ownership or license compatibility is unclear;
- the exact code, model, environment, version, run command, or expected output
  is not bound to the reported result;
- a placeholder remains unresolved.

Do not inspect private, controlled, patient-level, paid, or key-protected
resources without explicit authorization.

## Output Contract

Return:

1. **Availability Decision Card**: ready, conditionally ready, or not ready,
   with the evidence basis.
2. **Inspected / Not Inspected / Cannot Conclude**.
3. **Dimension Table**: state, source locator, unresolved risk, author action.
4. **Unverified Resource Candidates**.
5. **Unresolved Release Placeholders**.
6. **Submission-Ready Actions** ordered by blocking priority.

When a machine-readable artifact is useful, use
`../schemas/availability_evidence_card.schema.json`. The schema deliberately
fixes availability verification, FAIR compliance, repository identity,
license compatibility, and scientific-evidence claims to false until separate
authorized checks and expert review occur.
