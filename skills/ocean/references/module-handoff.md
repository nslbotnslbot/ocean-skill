# OCEAN Module Handoff

Use this reference when more than one OCEAN module is active or when a task should move from domain classification to evidence discovery, trend analysis, resource organization, claim audit, validation, planning, or report preservation.

The goal is to make each module produce a concrete artifact instead of a loose paragraph.

## Contents

- Handoff Object
- Domain and Data Router Placement
- Standard Route
- Module-by-Module Handoffs
- Input Shapes
- Stop Conditions

## Handoff Object

Every module handoff should contain:

```markdown
### Handoff Ticket
| Field | Content |
|---|---|
| Source module |  |
| Next module |  |
| Evidence packet |  |
| Domain lens |  |
| Data/tool packet |  |
| What was inspected |  |
| What was not inspected |  |
| Claim/resource boundary |  |
| Unresolved risk |  |
| Stop condition |  |
```

If the next module should not run, set `Next module` to `Stop` and explain why.

## Standard Route

Use this order for full OCEAN cases:

0. Domain Lens and Data/Tool Router: identify the biomedical domain, evidence standard, source classes, and stop conditions.
1. Sounding: find and bound sources.
2. Current: place the source in field movement.
3. Reef: organize resource/KG/database/cohort/benchmark evidence.
4. Iceberg: audit claims under the surface conclusion.
5. Anchor: design validation, leakage, benchmark, and reproducibility checks.
6. Compass: choose evidence-based research, experiment, journal, or collaboration route.
7. Harbor: preserve the final report and decision memory.

Skipping is allowed only when the evidence boundary makes a module irrelevant or impossible. Record skipped modules and the reason.

For research design workflows, use `research-design-workflow.md` to add design gates before selecting a Compass route. The handoff should preserve which gates passed, which need work, and which require a stop condition.

## Domain and Data Router Placement

Use `domain-lens.md` before module execution when the domain standard affects the answer. Use `data-tool-router.md` before Reef or any API/database/resource work. Use `module-artifact-contract.md` whenever the output is intended to be compared, scored, reused, or passed downstream.

## Module-by-Module Handoffs

| From | To | Pass forward | Main boundary |
|---|---|---|---|
| Domain Lens | Sounding/Reef/Iceberg/Anchor/Compass | Primary domain, research object, highest safe claim level, evidence standard | Domain routing is not scientific proof |
| Data/Tool Router | Reef | Source class, candidate resources, identifiers needed, access/privacy/licensing boundary | Candidate resources are not inspected evidence unless queried or provided |
| Sounding | Current | Source packet, inspected search boundary, candidate sources, Negative Space | Search coverage may be too narrow for trend claims |
| Sounding | Reef | Source packet, database/KG/resource names, identifiers, resource URLs | Source finding does not verify resource provenance |
| Current | Reef | Direction-flow nodes, benchmark/resource signals, recurring entities | Trend signals do not prove resource quality |
| Reef | Iceberg | Resource provenance map, evidence hierarchy, circularity risks | Database/KG evidence does not equal mechanism |
| Iceberg | Anchor | Claim-evidence matrix, downgraded claims, missing validation | Unsupported claims should not become validation targets without rewrite |
| Anchor | Compass | Validation plan, benchmark/leakage risks, feasibility notes | Validation plan is not proof of future success |
| Compass | Harbor | Chosen route, alternatives rejected, assumptions, next actions | Strategy must preserve evidence boundary and decision date |
| Harbor | Any earlier module | Persistent report, unresolved questions, stale evidence flags | Re-opening requires fresh source boundary if evidence changed |

## Input Shapes

OCEAN can start from different input sizes:

| Input | First module | Full-route behavior |
|---|---|---|
| One sentence or claim | Sounding or Iceberg | Treat as a hypothesis until sources are supplied or found |
| One idea | Sounding | Build a source packet before novelty or feasibility claims |
| One proposal | Sounding, Current, Reef | Separate planned work from evidence already available |
| One paper/preprint | Sounding | Inspect source boundary, then route through Current/Reef/Iceberg as needed |
| One review comment | Iceberg or Compass | Convert critique into claim/evidence gap and testable next action |
| One database/KG seed | Reef | Establish provenance before any claim audit |
| One clinical/therapeutic request | Domain Lens, Sounding, Reef | Establish clinical evidence standard before any utility or therapy statement |
| One data/API/tool request | Data/Tool Router, Reef | Plan official source class, identifier, access, privacy, and stop boundary before live access |

## Stop Conditions

Stop the full route when:

- only a title, abstract, DOI page, or search snippet is available for a strong claim;
- the source cannot be traced;
- the Domain Lens cannot identify a safe evidence standard for the requested conclusion;
- a database/KG/resource claim lacks official provenance;
- the next module would require private data, paid API calls, or unpublished material without user approval;
- the user requested a narrow module-only answer.
