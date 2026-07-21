# OCEAN Source Packet Boundary R2 Results

- Run date: 2026-07-04
- Cases: 6
- Pass: 6
- Needs review: 0

| Case | Expected | Actual | Verdict | Missing fields | Warnings |
|---|---|---|---|---|---|
| R2-PACKET-001 | pass | pass | pass | None | None |
| R2-PACKET-002 | fail | fail | pass | software field: tool_version; software field: command_line; software field: parameters; software field: reference_or_index; software field: input_files; software field: output_files; software field: logs_or_qc; software field: environment | None |
| R2-PACKET-003 | fail | fail | pass | software field: parameters; software field: reference_or_index; software field: input_files; software field: output_files; software field: logs_or_qc; software field: environment | None |
| R2-PACKET-004 | pass | pass | pass | None | None |
| R2-PACKET-005 | fail | fail | pass | candidate_route must not include supports_claims | candidate_route cannot support claims until a query/source is inspected |
| R2-PACKET-006 | fail | fail | pass | inspected_content for evidence-level packet | None |

## Interpretation

- Complete software evidence packets must include software-specific provenance fields.
- Candidate routes, missing inspected content, and software outputs without command/version/parameter provenance cannot be used as evidence.

## Evidence Boundary / 证据边界

This eval uses synthetic public-safe packets only. It does not inspect real software logs, private data, patient records, manuscripts, or live database/API responses.
