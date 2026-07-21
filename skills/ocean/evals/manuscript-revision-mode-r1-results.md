# Manuscript Revision Mode R1 Results

This is a deterministic structural and lifecycle-routing regression check. It does not evaluate scientific correctness or reproduce private manuscript text.

- Checks: 17
- Pass: 17
- Fail: 0

| Check | Target | Status | Detail |
|---|---|---|---|
| contract | revision_reference | pass | all required terms present |
| contract | skill_entrypoint | pass | all required terms present |
| contract | output_contract | pass | all required terms present |
| contract | routing_protocol | pass | all required terms present |
| contract | iceberg_isolation | pass | all required terms present |
| contract | manifest_always_load | pass | all required terms present |
| lifecycle_case | MR-R1-01 | pass | expected=Manuscript Revision; predicted=Manuscript Revision; channels=['修订正文（可直接替换）'] |
| lifecycle_case | MR-R1-02 | pass | expected=Manuscript Revision; predicted=Manuscript Revision; channels=['修订正文（可直接替换）'] |
| lifecycle_case | MR-R1-03 | pass | expected=Manuscript Revision; predicted=Manuscript Revision; channels=['修订正文（可直接替换）'] |
| lifecycle_case | MR-R1-04 | pass | expected=Manuscript Revision; predicted=Manuscript Revision; channels=['修订正文（可直接替换）', '修改说明（不进入正文）'] |
| lifecycle_case | MR-R1-05 | pass | expected=Manuscript Revision; predicted=Manuscript Revision; channels=['修订正文（可直接替换）', '作者确认项（仅必要时）'] |
| lifecycle_case | MR-R1-06 | pass | expected=Pre-submission Stress Test; predicted=Pre-submission Stress Test; channels=['audit_report', 'separate_safe_rewrites'] |
| lifecycle_case | MR-R1-07 | pass | expected=Design / Audit; predicted=Design / Audit; channels=['module_artifacts'] |
| lifecycle_case | MR-R1-08 | pass | expected=Reviewer Response; predicted=Reviewer Response; channels=['response_letter', 'revised_manuscript_text', 'author_only_notes'] |
| lifecycle_case | MR-R1-09 | pass | expected=Design / Audit; predicted=Design / Audit; channels=['module_artifacts'] |
| lifecycle_case | MR-R1-10 | pass | expected=Manuscript Revision; predicted=Manuscript Revision; channels=['修订正文（可直接替换）'] |
| forbidden_clean_tokens | forbidden_token_registry | pass | registered=13 |

## Evidence Boundary

Passing means the public skill files contain the lifecycle gate and the public-safe case router selects the expected mode. It does not prove that every model will obey the contract, that any manuscript claim is correct, or that private manuscript material was inspected in this regression run.
