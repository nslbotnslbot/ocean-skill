# External Validation Protocol

This protocol defines the minimum evidence required before OCEAN reports an
external-laboratory or external-researcher validation result.

## Independence

- The validating group must not have created the evaluated output.
- Conflicts of interest and prior collaboration must be declared.
- The group receives a versioned task packet, rubric, and submission template.
- Condition labels remain blinded until independent scoring is locked.
- Local modifications to prompts, code, tools, and source material are recorded.

## Required record

Each validation submission must preserve:

- task and case identifiers;
- OCEAN, model, tool, and environment versions;
- input and output checksums;
- run status, including errors, timeouts, and no-hit results;
- elapsed time, token use, and provider-reported cost when available;
- two independent expert decisions per case;
- disagreement resolution;
- permission and license status for public release.

## Promotion gate

An external result is public only when:

1. all required case records are present;
2. the benchmark report checksum matches the reviewed report;
3. the evaluation used the pre-specified rubric;
4. blinding and conflicts are documented;
5. ambiguous cases remain marked ambiguous;
6. the validating group approves public attribution or an agreed anonymous label.

Repository CI, an internal rerun, or a collaborator reading a report does not
count as external validation.

## Evidence boundary

This file is a protocol, not proof that an external laboratory has run OCEAN.
No external performance result should be claimed until signed or otherwise
verifiable records are supplied and independently audited.
