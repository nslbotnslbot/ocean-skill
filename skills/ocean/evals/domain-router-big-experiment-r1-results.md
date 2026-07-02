# OCEAN Contract Check

- Total checks: 33
- Pass: 33
- Review: 0
- Fail: 0

| Check | Target | Status | Detail |
|---|---|---|---|
| required_reference | domain-lens.md | pass | exists=True<br>mentioned=True |
| required_reference | data-tool-router.md | pass | exists=True<br>mentioned=True |
| required_reference | module-artifact-contract.md | pass | exists=True<br>mentioned=True |
| required_reference | output-contract.md | pass | exists=True<br>mentioned=True |
| required_reference | module-handoff.md | pass | exists=True<br>mentioned=True |
| required_reference | sounding.md | pass | exists=True<br>mentioned=True |
| required_reference | current.md | pass | exists=True<br>mentioned=True |
| required_reference | reef.md | pass | exists=True<br>mentioned=True |
| required_reference | reef-biological-data-sources.md | pass | exists=True<br>mentioned=True |
| required_reference | reef-api-adapters.md | pass | exists=True<br>mentioned=True |
| required_reference | iceberg.md | pass | exists=True<br>mentioned=True |
| required_reference | anchor.md | pass | exists=True<br>mentioned=True |
| required_reference | compass.md | pass | exists=True<br>mentioned=True |
| required_reference | harbor.md | pass | exists=True<br>mentioned=True |
| module_artifact_contract | Sounding | pass |  |
| module_artifact_contract | Current | pass |  |
| module_artifact_contract | Reef | pass |  |
| module_artifact_contract | Iceberg | pass |  |
| module_artifact_contract | Anchor | pass |  |
| module_artifact_contract | Compass | pass |  |
| module_artifact_contract | Harbor | pass |  |
| domain_router_case | DRR1-001 | pass | expected_domain=Medical AI / clinical prediction<br>predicted_domain=Medical AI / clinical prediction<br>expected_first_module=Sounding<br>expected_stop_condition=Only abstract/landing-level evidence cannot support treatment guidance. |
| domain_router_case | DRR1-002 | pass | expected_domain=Omics / single-cell / spatial<br>predicted_domain=Omics / single-cell / spatial<br>expected_first_module=Reef<br>expected_stop_condition=Atlas expression alone cannot prove mechanism. |
| domain_router_case | DRR1-003 | pass | expected_domain=Drug / target / therapeutic hypothesis<br>predicted_domain=Drug / target / therapeutic hypothesis<br>expected_first_module=Reef<br>expected_stop_condition=Target association is not therapeutic efficacy. |
| domain_router_case | DRR1-004 | pass | expected_domain=Clinical research<br>predicted_domain=Clinical research<br>expected_first_module=Reef<br>expected_stop_condition=Registry metadata alone cannot prove efficacy. |
| domain_router_case | DRR1-005 | pass | expected_domain=Knowledge graph / database / resource<br>predicted_domain=Knowledge graph / database / resource<br>expected_first_module=Reef<br>expected_stop_condition=KG prediction is hypothesis support, not causality. |
| domain_router_case | DRR1-006 | pass | expected_domain=Manuscript / review / proposal<br>predicted_domain=Manuscript / review / proposal<br>expected_first_module=Iceberg<br>expected_stop_condition=Reviewer text is pressure signal, not experimental fact. |
| domain_router_case | DRR1-007 | pass | expected_domain=Biological AI / AI-for-biology<br>predicted_domain=Biological AI / AI-for-biology<br>expected_first_module=Sounding<br>expected_stop_condition=Novelty cannot be claimed without bounded Current search. |
| domain_router_case | DRR1-008 | pass | expected_domain=Collaboration / authorship boundary<br>predicted_domain=Collaboration / authorship boundary<br>expected_first_module=Compass<br>expected_stop_condition=Authorship cannot be decided without concrete contribution records and team criteria. |
| domain_router_case | DRR1-009 | pass | expected_domain=Omics / single-cell / spatial<br>predicted_domain=Omics / single-cell / spatial<br>expected_first_module=Reef<br>expected_stop_condition=Dataset presence/expression association does not prove disease-specific mechanism. |
| domain_router_case | DRR1-010 | pass | expected_domain=Medical AI / clinical prediction<br>predicted_domain=Medical AI / clinical prediction<br>expected_first_module=Reef<br>expected_stop_condition=Benchmark rank alone cannot prove deployment readiness. |
| domain_router_case | DRR1-011 | pass | expected_domain=Clinical research<br>predicted_domain=Clinical research<br>expected_first_module=Reef<br>expected_stop_condition=Variant assertion alone cannot support patient-specific treatment guidance. |
| domain_router_case | DRR1-012 | pass | expected_domain=Manuscript / review / proposal<br>predicted_domain=Manuscript / review / proposal<br>expected_first_module=Harbor<br>expected_stop_condition=Stale evidence needs a fresh source boundary before current positioning. |
