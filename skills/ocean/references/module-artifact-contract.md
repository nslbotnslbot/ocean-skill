# OCEAN Module Artifact Contract

Use this contract when OCEAN needs stable outputs across the seven modules. Each module should produce a concrete artifact, not a loose paragraph.

## Contents

- Contract Principles
- Required Module Artifacts
- Artifact Quality Gates
- Compact Artifact Templates
- Cross-Module Handoff
- Stop Conditions

## Contract Principles

- Keep module outputs stable enough for later comparison and evaluation.
- State evidence boundaries before conclusions.
- Preserve identifiers, inspected source types, missing evidence, and stop conditions.
- Do not invent missing sources, data, endpoints, sample sizes, metrics, validations, reviewer comments, author roles, or publication outcomes.
- If a module is skipped, record why.

## Required Module Artifacts

| Module | Required artifact | Must include | Must not do |
|---|---|---|---|
| Sounding | Source Packet | search/source boundary, candidate sources, source tier, inspected content, Evidence Radar Map, Negative Space, Handoff Ticket | treat search snippets or abstracts as full evidence |
| Current | Direction-Flow Map | domain/method/resource lanes, bounded search notes, trend signals, consensus-vs-hype, opportunity/risk, missing-search boundary | claim field dominance or novelty without search coverage |
| Reef | Resource Provenance Map | resource inventory, official identifier/source, evidence hierarchy, access/privacy boundary, circularity/leakage risks, data/tool packet if needed | turn database/KG/resource records into mechanism, validation, or clinical utility |
| Iceberg | Claim-Evidence Matrix | surface claim, evidence inspected, support verdict, hidden assumption, missing validation, safe rewrite | keep unsupported strong wording |
| Anchor | Validation Plan | validation target, current evidence, minimum check, leakage/benchmark/reproducibility risks, feasibility boundary | imply planned validation has already succeeded |
| Compass | Research Route Card | evidence driver, route options, experiment/design plan, decision gates, journal/collaboration strategy, stop condition | brainstorm free-floating ideas without evidence anchors |
| Harbor | Decision Memory / Project Start Card | final memo, evidence boundary ledger, contribution boundary record, next-action register, stale-evidence flags, reuse note, GitHub Sync Ticket when a new tracked project starts | add new evidence, publish private project material, auto-push without approval, or decide authorship/publication from missing records |

## Artifact Quality Gates

Score an artifact as usable only if it passes all five gates:

1. **Boundary gate**: includes inspected, not inspected, cannot judge, and next-needed evidence.
2. **Traceability gate**: preserves provided identifiers or explicitly marks missing traceable sources.
3. **Calibration gate**: downgrades unsupported causal, clinical, mechanism, validation, novelty, publication, or authorship claims.
4. **Artifact gate**: produces the expected module artifact fields.
5. **Handoff gate**: names the next OCEAN module or a stop condition with an input packet.

## Compact Artifact Templates

### Sounding Source Packet

```markdown
Sounding Source Packet
| Source | Identifier/URL | Tier | Inspected content | Can support | Cannot support | Handoff |
|---|---|---|---|---|---|---|
```

### Current Direction-Flow Map

```markdown
Current Direction-Flow Map
| Lane | Signal inspected | Movement observed | Confidence | Missing search | Downstream risk/opportunity |
|---|---|---|---|---|---|
```

### Reef Resource Provenance Map

```markdown
Reef Resource Provenance Map
| Resource | Type | Identifier/source | Evidence level | Access/privacy boundary | Circularity/leakage risk | Cannot support |
|---|---|---|---|---|---|---|
```

### Iceberg Claim-Evidence Matrix

```markdown
Iceberg Claim-Evidence Matrix
| Claim | Evidence inspected | Support verdict | Hidden assumption | Missing validation | Safe rewrite |
|---|---|---|---|---|---|
```

### Anchor Validation Plan

```markdown
Anchor Validation Plan
| Validation target | Current evidence | Minimum check | Leakage/benchmark/reproducibility risk | Priority | Stop condition |
|---|---|---|---|---|---|
```

### Compass Research Route Card

```markdown
Compass Research Route Card
| Route | Evidence driver | Experiment/design move | Feasibility boundary | What would change decision | Next module |
|---|---|---|---|---|---|
```

### Harbor Decision Memory

```markdown
Harbor Decision Memory
| Decision / record | Evidence basis | Date/context | Unresolved risk | Next action | Reuse warning |
|---|---|---|---|---|---|
```

### Harbor Project Start Card

```markdown
Harbor Project Start Card
| Project ID | Title | Domain lane | Project class | Status | Public-safe boundary | First module | GitHub sync |
|---|---|---|---|---|---|---|---|
```

### GitHub Sync Ticket

```markdown
GitHub Sync Ticket
| Target repository | Files to add/update | Suggested branch | Commit message | Remote push | Excluded material |
|---|---|---|---|---|---|
```

## Cross-Module Handoff

Every artifact that moves downstream should include:

```markdown
Handoff Ticket
| Source module | Next module | Input packet | Boundary | Unresolved risk | Stop condition |
|---|---|---|---|---|---|
```

## Stop Conditions

Stop or downgrade when:

- the active module cannot produce its required artifact from the available input;
- the next module would require unapproved private, paid, key-protected, or sensitive data;
- the model would need to invent source details, data fields, validation results, reviewer text, or author roles;
- a strong claim depends on evidence that is not inspected.
