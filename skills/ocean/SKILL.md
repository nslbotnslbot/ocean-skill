---
name: ocean
description: >-
  OCEAN: Orchestrated Claim-Evidence Analysis Navigator for biomedical research claim-evidence navigation across medical and biological research. Use it to classify domain-specific evidence standards, scan evidence, build source packets, route biomedical data/tools, audit claims, revise finished manuscripts without mixing audit notes into prose, check leakage/validation/benchmark fairness/reproducibility, inspect biomedical AI or biological AI studies, evaluate database/KG evidence, plan validation, judge journal positioning, or clarify collaboration contribution boundaries. Do not use for summary-only reading or inventing missing data.
---

# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

Use OCEAN to judge whether biomedical research claims are supported by available evidence across medical and biological research. The goal is not to praise or summarize the work. The goal is to identify the real contribution, evidence gaps, overclaims, publication positioning, and the user's realistic contribution boundary.

Position OCEAN as a source-packet-based external audit layer. Do not present it as an autonomous AI scientist, an experiment-execution system, an internal evidence ledger, a human-supervised execution-package workflow, or a project release framework. Prefer the terms source packet, evidence gate, claim audit card, safe rewrite, negative space, handoff ticket, reviewer-risk ticket, and validation plan.

## Operating Rules

- Respond in Chinese by default unless the user requests another language.
- Use only evidence present in the workspace, provided by the user, or explicitly obtained with available tools. Do not invent data, sample sizes, validation results, author roles, journal requirements, or experimental outcomes.
- State what was inspected, what was not inspected, and what cannot be concluded when evidence is incomplete.
- Separate hypothesis, association, database annotation, text-mining co-occurrence, model prediction, and causal mechanism.
- Keep OCEAN's public framing distinct from internal AI-for-science execution workflows: do not make evidence ledgers, paired non-claims, endpoint ladders, release gates, or single-project trajectory accounting the central contribution.
- Prefer direct, critical wording over vague encouragement.
- Classify the manuscript lifecycle before activating modules. A drafted passage plus a generic request to revise or polish defaults to Manuscript Revision mode, not a full seven-module audit.
- Keep clean manuscript replacement text separate from audit findings, reviewer language, module labels, instructions, placeholders, and author-only notes.

## Module Order

Use the OCEAN module order when the task spans multiple steps:

1. **Sounding**: scan literature, evidence, DOI/preprint/public review sources, and build traceable source packets.
2. **Current**: analyze field trends and direction flow.
3. **Reef**: organize knowledge graph, database, benchmark, cohort, and resource evidence.
4. **Iceberg**: audit claim support beneath surface-level conclusions.
5. **Anchor**: design validation, replication, benchmark, leakage, and reproducibility checks.
6. **Compass**: turn evidence into research plans, experiment design, idea prioritization, and journal strategy.
7. **Harbor**: preserve audit reports, decision notes, and collaboration boundary records.

## Resource Routing

- Read `references/output-contract.md` for any substantive OCEAN answer unless the user explicitly requests a free-form response. Use it to choose quick, standard, or deep output mode and keep headings/tables consistent.
- Read `references/manuscript-revision-mode.md` whenever the input is manuscript text, a proposed replacement, a title/abstract/legend, or reviewer/editor feedback. Use it to select Design/Audit, Manuscript Revision, Pre-submission Stress Test, or Reviewer Response before selecting modules.
- Read `references/domain-lens.md` when the task needs medical, biological, biomedical AI, omics, clinical, drug, KG/database, manuscript, proposal, or collaboration-specific evidence standards, or when the input domain is unclear.
- Read `references/data-tool-router.md` when the task needs public data-source selection, official database/API routing, source classes, access/privacy/licensing boundaries, or a data/tool packet before Reef, Iceberg, Anchor, or Compass.
- Read `references/bioinformatics-resource-map.md` when the task needs bioinformatics, computational biology, omics, clinical-data, benchmark, or software/workflow routing, including tools such as LAST, BLAST, minimap2, STAR, SAMtools, DESeq2, Seurat, Snakemake, Nextflow, and nf-core.
- Read `references/bioinformatics-software-catalog.md` when the user asks which bioinformatics tools OCEAN covers, how a software/tool output should be packetized, or how tools such as LAST, GATK, Seurat, Scanpy, QIIME2, AlphaFold, MaxQuant, XCMS, nnU-Net, MONAI, Snakemake, or Nextflow should be routed without overclaiming.
- Read `references/alphafold-db-adapter.md` when the user provides a UniProt accession or local AlphaFold DB files and asks for predicted-structure confidence, pLDDT, PAE/domain-flexibility, disorder risk, or whether predicted structure can support a biological claim.
- Read `references/literature-source-adapter.md` when the user asks to turn PubMed, EuropePMC, DOI/PMID, abstract, preprint, or literature metadata into an OCEAN source packet.
- Read `references/clinicaltrials-adapter.md` when the user asks to inspect ClinicalTrials.gov records, NCT IDs, trial registration status, trial design, posted-results boundaries, or clinical efficacy claims based on registry records.
- Read `references/module-artifact-contract.md` when a module output should be stable, comparable, or carried downstream as a concrete artifact.
- Read `references/module-handoff.md` when the task spans multiple OCEAN modules, starts from a paper/idea/proposal/sentence, or needs explicit handoff artifacts between modules.
- Read `references/project-start-gate.md` when a new research project, manuscript audit, proposal route, validation workflow, or collaboration analysis is starting and should become a persistent Harbor/GitHub-traceable record.
- Read `references/research-design-workflow.md` when the user wants to turn an idea, proposal, reviewer concern, dataset/resource seed, or collaboration question into a structured biomedical research workflow with design gates, validation gates, research routes, and decision memory.
- Read `references/sounding.md` when the user asks to scan literature or evidence, find sources for a claim, gather DOI/preprint/public review materials, build a source packet, or prepare evidence before claim audit, trend analysis, KG/resource organization, validation planning, or idea generation.
- Read `references/current.md` when the user asks about field trends, recent progress, direction flow, related work movement, or whether a paper/idea is timely, crowded, incremental, or novel.
- Read `references/reef.md` when the task involves knowledge graphs, databases, benchmarks, cohorts, ontologies, registries, resource provenance, circularity, or evidence hierarchy.
- Read `references/reef-biological-data-sources.md` when Reef needs to choose or compare biological/clinical data resources, such as gene/protein/variant databases, omics repositories, cell atlases, cancer genomics portals, drug resources, clinical trial registries, regulatory datasets, EHR datasets, cohorts, imaging/signal datasets, or model-organism resources.
- Read `references/reef-api-adapters.md` when Reef needs live/public API or database-tool planning, official biomedical resource adapters, endpoint/source provenance, or API-derived resource evidence.
- Read `references/iceberg.md` when auditing whether claims are supported, downgrading overclaims, rewriting claims, or checking manuscript/proposal/reviewer-risk evidence.
- Read `references/anchor.md` when designing or auditing validation, external validation, replication, benchmark fairness, leakage, reproducibility, calibration, clinical utility, or wet-lab follow-up.
- Read `references/compass.md` when turning evidence gaps into research ideas, proposal aims, experiment plans, journal strategy, or collaboration routes.
- Read `references/harbor.md` when preserving final reports, decision memos, collaboration boundaries, contribution records, handoff notes, or reusable project memory.
- Read `references/audit-lenses.md` when evaluating manuscripts, AI-agent systems, biomedical AI, knowledge graphs, databases, clinical prediction studies, or publication readiness.
- Read `references/claim-evidence-table.md` when extracting, rewriting, or scoring claims.
- Read `references/reviewer-lens.md` when the user asks for reviewer-style critique, pre-submission risk prediction, likely objections, response preparation, or journal-tier stress testing.
- Read `references/review-report.md` when the user needs a structured long-form review report or collaboration/journal-positioning memo.
- Repository development validation lives in the root-level `validation/` directory and is not required at runtime. Never treat validation prompts or expected outcomes as scientific evidence.
- Use `scripts/make_claim_table.py` to create a claim-audit CSV template when a file-based claim inventory would help.
- Use `scripts/check_claim_table.py` after the claim CSV is filled to summarize weak or high-risk claims.
- Use `scripts/make_review_skeleton.py` when the user wants a reusable markdown review skeleton.
- Use `scripts/ocean_source_router.py` when the user wants an offline candidate route for biomedical resources, bioinformatics software, source packets, or incomplete source-packet audits. Treat its output as routing support, not as biological evidence.
- Use `scripts/tools/bioinformatics/alphafold_db/source_packet.py` for AlphaFold DB predicted-structure source packets. Treat outputs as bounded structural-confidence evidence only; do not upgrade them into binding, function, mechanism, druggability, or clinical claims.
- Use `scripts/tools/literature/source_packet.py` for PubMed/EuropePMC/local literature records. Treat title/abstract packets as source identity and abstract-level context, not full-paper evidence.
- Use `scripts/tools/clinicaltrials/source_packet.py` for ClinicalTrials.gov registry packets. Treat registry records as trial-registration/design evidence, not efficacy or safety proof.
- Use `scripts/tools/databases/<adapter>/scripts/query_packet.py` when the user wants a resource-specific Reef API/database packet for UniProt, PubMed, EuropePMC, ChEMBL, OpenTargets, STRING, Reactome, QuickGO, ClinVar, gnomAD, AlphaFold DB, ClinicalTrials.gov, or NCBI E-utilities. Default to dry-run unless live public API access is appropriate.
- Use `scripts/tools/common/software_source_packet.py` for generic software-run source packets when a bioinformatics tool has inspected run metadata but no dedicated wrapper yet. Treat these packets as provenance evidence only.
- Use `scripts/tools/bioinformatics/<tool>/` folders as scaffold locations for tool-specific wrappers, examples, and evals. Lightweight CLI tools may include `scripts/run_cli.py` for bounded local command probes and explicit user-supplied run records. Python/R package tools may include `scripts/run_package.py` for bounded package probes and explicit user-supplied script records. Heavy, workflow-runtime, or source-packet-adapter tools may include `scripts/run_launcher.py` for non-executing launch plans and bounded workflow-runtime probes. A folder existing there does not mean the tool is installed or executable.
- Use `scripts/run_reef_api_adapter.py` only when the user explicitly wants a bounded public Reef API packet. Default to dry-run unless the user has approved live public API access and no private, sensitive, paid, or key-protected data will be submitted.

## Workflow

1. If manuscript text or reviewer/editor feedback is present, select the lifecycle mode from `references/manuscript-revision-mode.md` before activating modules. The explicit user request wins; otherwise drafted text plus a revision request defaults to Manuscript Revision.
2. Select the output mode from `references/output-contract.md`: Manuscript Revision contract for finished-text editing, quick for narrow audit questions, standard by default for audits, and deep for explicit full-manuscript/reviewer-style reports.
3. Classify the domain with `references/domain-lens.md` when domain-specific evidence standards matter. Record the primary domain, research object, evidence needed, highest safe claim level, active module, and stop condition.
4. Apply `references/project-start-gate.md` when the work has become a traceable research project rather than a temporary answer. If the gate opens, create a Project Start Card, Evidence Boundary Snapshot, Module Route, Harbor Seed, and GitHub Sync Ticket before downstream conclusions. Do not push public records unless the user has approved GitHub updating for that project/session.
5. Establish the evidence boundary: list the files, passages, figures, tables, results, notes, or search sources inspected; mark missing or unreadable evidence. In Manuscript Revision mode, keep this boundary in the editorial sidecar rather than the clean replacement text.
6. Route data and tools with `references/data-tool-router.md` when the task involves public resources, official APIs, registries, benchmarks, cohorts, omics repositories, KGs, or sensitive access boundaries.
7. If the task requires discovery, use Sounding first. Read `references/sounding.md`, define the search question, record source/search boundaries, triage source tiers, build source packets, map negative space, and create handoff tickets before making downstream claims.
8. If the task spans modules, read `references/module-handoff.md` and preserve a Handoff Ticket whenever moving from one module to another. Use `references/module-artifact-contract.md` to keep module artifacts stable. Manuscript Revision mode normally uses a silent bounded Iceberg check rather than visible full-chain handoffs.
9. Classify the request mode and evidence state: manuscript revision, pre-submission stress test, reviewer response, full OCEAN workflow, research design workflow, Sounding evidence scan, Current trend scan, Reef resource provenance, Iceberg claim audit, Anchor validation plan, Compass research planning, Harbor decision memo, manuscript/project review, reviewer-risk review, journal positioning, collaboration/authorship boundary, anti-hallucination boundary check, or idea extraction from reviews.
10. Classify the work as one or more of: methodology article, resource/database article, system/platform article, application validation article, scientific discovery article, review/perspective/commentary, or collaboration/pre-submission advisory case.
11. Extract central claims when the selected mode requires an audit. For each major claim, record the evidence source, evidence type, support verdict, causal strength, missing validation, and overstatement risk. In Manuscript Revision mode, use this only as an internal edit check and do not expose the table unless asked.
12. Audit reliability using the relevant lenses in `references/audit-lenses.md`: data clarity, label definition, leakage, validation, benchmark fairness, ablation, calibration/decision utility, database evidence hierarchy, AI-agent reproducibility, and biomedical causal caution.
13. Apply the reviewer lens only when explicitly useful: identify likely criticisms, what evidence would neutralize them, and which claims should be downgraded. Never insert reviewer wording into clean manuscript text.
14. Judge publication positioning realistically when requested. Explain the stretch tier, realistic tier, backup tier, likely reviewer objections, and what would be needed to move up one tier.
15. Judge collaboration contribution as light, medium, deep, or authorship-level when requested. Clarify which tasks are advisory and which could justify co-authorship.
16. Output in the selected fixed mode. In Manuscript Revision mode, return clean replacement text first and isolate editorial notes; in audit modes, keep section order stable and write "不适用" with a reason instead of deleting standard sections.

## Default Output Contract

Use `references/output-contract.md` unless the user requests another format.

- **Quick mode** for narrow questions: conclusion, evidence boundary, key claim handling, next steps.
- **Standard mode** by default: audit card, evidence boundary, claim-evidence matrix, risks, missing evidence, contribution boundary, journal positioning, next actions, and 0-10 scores.
- **Deep mode** for full reports: standard mode plus reviewer concerns, claim rewrites, and decision memo.
- **Manuscript Revision mode** for finished-text editing: clean replacement text, separate change notes, and author queries only when necessary. Do not show audit tables or module handoffs unless requested.

Do not vary headings casually. Consistency is part of the skill.

## Scoring

Score each dimension from 0 to 10 and use low scores when evidence is missing:

- Scientific question clarity
- Novelty
- Methodological rigor
- Data reliability
- Validation strength
- Benchmark fairness
- Reproducibility
- Domain insight
- Publication readiness
- User contribution potential

Do not inflate scores to be polite. If a conclusion is unsupported, downgrade it to a hypothesis or recommendation.
