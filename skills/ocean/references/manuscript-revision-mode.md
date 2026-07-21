# OCEAN Manuscript Lifecycle Gate

Use this gate whenever the input is a manuscript, section, paragraph, title, abstract, figure legend, reviewer comment, or proposed replacement text. Classify the manuscript lifecycle before selecting modules or an output depth.

## Lifecycle Modes

| Mode | Default trigger | Visible OCEAN behavior |
|---|---|---|
| Design / Audit | idea, proposal, experiment design, early draft, or an explicit request to find weaknesses | Use the smallest relevant module set; a full seven-module audit is allowed when the task is genuinely end to end. |
| Manuscript Revision | a drafted passage plus a request to revise, polish, shorten, translate, or improve wording | Return clean replacement text first. Use evidence checks silently and keep all critique outside the manuscript text. |
| Pre-submission Stress Test | explicit request for reviewer simulation, full audit, submission-readiness review, or adversarial checking | Produce an audit report and safe rewrites as separate artifacts. Never merge reviewer language into replacement prose. |
| Reviewer Response | reviewer/editor comments plus a request to revise or reply | Separate response-letter text, revised manuscript text, and author-only notes. |

The user's explicit mode wins. If a complete passage is supplied with a generic request such as "修改一下", "润色", "改写", or "精简", default to **Manuscript Revision**, not full OCEAN audit.

## Manuscript Revision Rules

1. Preserve scientific meaning, terminology, tense, citation placement, and section function unless a correction is required.
2. Make the smallest evidence-safe edit. Improve wording and coherence without turning the paragraph into a review report.
3. Use Iceberg silently to detect unsafe claims. Activate Sounding, Current, Reef, Anchor, Compass, or Harbor only when the request actually requires them.
4. If wording exceeds the inspected evidence, provide the strongest supported clean rewrite and explain the downgrade separately.
5. If information is missing, preserve safe original wording or add an author query outside the manuscript. Never invent the missing value.
6. Do not add a limitation sentence to Results merely because a limitation exists. Put placement advice in editorial notes, unless the claim cannot be made accurately without an in-text qualification.
7. Scientific accuracy takes priority over rhetorical smoothness, but accuracy notes belong in the correct manuscript section or the editorial sidecar.

## Channel Isolation

Use these channels in this order:

```markdown
一、修订正文（可直接替换）
<clean manuscript prose only>

二、修改说明（不进入正文）
- <brief explanation of material edits or evidence-safe downgrades>

三、作者确认项（仅必要时）
- <missing fact, method, citation, value, or placement decision>
```

The first channel must never contain:

- module labels such as `OCEAN: Reef`, `Iceberg`, or `Anchor`;
- verdict labels such as `Unsupported`, `Downgrade`, or `Cannot judge`;
- commands such as "删除原文", "建议补充", "请填写", or "作者应";
- reviewer-style criticism, risk tables, evidence-boundary ledgers, scores, or Handoff Tickets;
- editorial placeholders such as `XX`, `[n=?]`, `[please add ...]`, or `TODO`, unless the user explicitly requests placeholder mode.

Existing citation markers or placeholders already present in the supplied manuscript may be preserved, but OCEAN must not create new editorial placeholders silently.

If no material scientific issue is found, omit the second and third channels or keep them to one short sentence. Do not manufacture criticism to populate the template.

## Module Visibility

- In **Design / Audit**, module artifacts may be visible and passed through the standard handoff route.
- In **Manuscript Revision**, module reasoning is an internal editorial check. Only the clean revision and necessary sidecar notes are user-facing.
- In **Pre-submission Stress Test**, module artifacts may be visible, but any replacement prose must remain in a separate clean-rewrite column or section.
- In **Reviewer Response**, never mix response-letter language, manuscript replacement text, and author-only decisions.

## Stop Conditions

Stop before producing clean replacement text when:

- the supplied passage is unreadable or absent;
- the requested rewrite would require invented results, methods, citations, sample sizes, statistics, or validation;
- the user explicitly asks to preserve a claim that contradicts inspected evidence.

In these cases, state the minimum author decision or source needed. Do not substitute a full seven-module audit unless the user asks for one.
