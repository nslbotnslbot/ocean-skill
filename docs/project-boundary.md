# OCEAN Project Boundary

This note defines the public positioning boundary for **OCEAN: Orchestrated Claim-Evidence Analysis Navigator**.

## 中文上下文

OCEAN 的公开定位是 **基于 source packet 的外部 claim-evidence 审计层**。它用于审计论文、预印本、数据库、知识图谱、模型预测、AI-agent 输出和协作材料中的科学 claim 是否被已检查证据支持。

OCEAN 不应被包装成某个研究项目的内部执行账本、实验执行系统、自动科学家或发布审批流程。它的价值在于把已有来源拆成可追踪的证据边界，并判断哪些 claim 可以保留、哪些必须降级、哪些需要补充验证。

## English context

OCEAN's public positioning is a **source-packet-based external claim-evidence audit layer**. It audits whether scientific claims in manuscripts, preprints, databases, knowledge graphs, model predictions, AI-agent outputs, and collaboration materials are supported by inspected evidence.

OCEAN should not be framed as an internal execution ledger, experiment-execution system, autonomous scientist, or publication release workflow for one research program. Its value is to convert inspected sources into traceable evidence boundaries and decide which claims are allowed, which claims must be downgraded, and which claims require additional validation.

## Scope / 影响范围

This boundary applies to public README wording, figure captions, GitHub documentation, manuscript outlines, slide decks, and future module descriptions.

Affected project objects:

- `SourcePacket`: inspected-source record with explicit boundaries.
- `EvidenceGate`: rule for what an evidence type can and cannot support.
- `ClaimAuditCard`: claim-level verdict and risk record.
- `SafeRewrite`: supported weaker wording for an overextended claim.
- `NegativeSpace`: what was not inspected, not found, inaccessible, or insufficient.
- `HandoffTicket`: downstream route to Iceberg, Anchor, Reef, Compass, Current, or Harbor.
- `ReviewerRiskTicket`: likely reviewer objection and evidence needed to neutralize it.

## Evidence boundary / 证据边界

This file records a naming, positioning, and presentation decision. It is not scientific validation evidence, not a claim of benchmark performance, and not a discovery result.

## Preferred framing

Use these phrases when presenting OCEAN:

- source-packet-based claim-evidence auditing
- external audit layer for scientific agent outputs
- evidence-type gating
- safe claim rewriting
- public adversarial case matrices
- source-boundary regression checks
- reviewer-risk and validation-planning support

## Non-goals

Do not present OCEAN as:

- an autonomous AI scientist;
- an experiment-execution or discovery-generation system;
- an internal evidence ledger for one research program;
- a human-supervised execution-package workflow;
- a project release or publication-approval gate;
- a discovery endpoint spectrum;
- a replacement for domain experts, wet-lab validation, clinical validation, or independent replication.

## Terms to avoid as central contributions

These terms can appear only when discussing what OCEAN is **not**. They should not be the main contribution language:

- evidence ledger
- paired non-claim
- endpoint ladder or endpoint spectrum
- execution package
- guidance-reviewed record
- human-supervised release gate
- manuscript-facing release record
- six-case outcome spectrum

## Figure guidance

OCEAN figures should emphasize:

```text
External sources -> SourcePacket -> EvidenceGate -> ClaimAuditCard -> SafeRewrite / ReviewerRisk / ValidationPlan
```

They should not emphasize:

```text
AI execution -> human supervisor -> scientific guidance -> reviewed ledger -> release gate
```

## Public evaluation boundary

OCEAN public evaluation materials should remain public-source and benchmark-like:

- DOI, arXiv, bioRxiv, medRxiv, database, or public-review source seeds;
- explicit inspected-source boundaries;
- synthetic adversarial user claims;
- expected safe behavior;
- compact coverage summaries.

They should not publish private manuscripts, private collaborator notes, raw hidden-answer logs, private peer-review text, local execution transcripts, or private source routes.
