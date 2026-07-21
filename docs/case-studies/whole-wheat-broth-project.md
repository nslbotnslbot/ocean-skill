# Whole-Wheat Broth Project: OCEAN Seven-Module Case Note

This is a public-safe Harbor case note for a real whole-wheat broth / probiotic-fermented whole-wheat medicinal diet project that used OCEAN during manuscript planning, evidence calibration, figure routing, and claim-boundary review.

中文说明：这不是论文结果正文，也不是投稿状态证明。它只记录 OCEAN 在这个真实项目里如何使用七个模块，以及哪些结论被保留为直接证据、探索性解释或待验证假设。

## Source Basis

This note was reconstructed from local project records and the Codex project thread for the whole-wheat broth study.

Public-safe inspected material categories included:

- manuscript QA and figure-review records;
- publication/submission figure package manifests and source-data organization notes;
- fermentation-liquid 16S and ITS analysis records;
- targeted SCFA and untargeted metabolomics analysis records;
- 29-sample mouse diarrhea-model 16S analysis records;
- multi-omics integration records;
- toxicology screening and network-toxicology support records;
- OCEAN staging notes for the seven-module workflow and Harbor memory.

Confidential raw data, unpublished manuscript text, collaborator-only notes, private journal correspondence, and raw source tables are not published in this repository.

## Evidence Boundary

This case note records workflow usage and evidence boundaries. It does not claim that OCEAN independently discovered the biological mechanism, validated the experiment, or proved clinical usefulness.

The main boundary decisions were:

- exploratory microbiome-metabolome associations were not upgraded into mechanism proof;
- database or toxicity-routing outputs were not treated as validated toxic mechanisms;
- fermentation-liquid metabolomics and mouse fecal 16S were not merged into fake individual-level sample-wise correlations;
- manuscript and figure decisions were recorded as project workflow decisions, not as acceptance or peer-review outcomes.

## OCEAN Seven-Module Use

| OCEAN module | What it did in this project | Boundary kept |
|---|---|---|
| **Sounding** | Built local evidence packets from manuscript drafts, figure PDFs, OTU/abundance tables, metabolomics tables, SCFA tables, and downstream figure exports. | Distinguished inspected local files from oral/project-memory claims and unverified claims. |
| **Current** | Helped position the work as fermentation-driven metabolite remodeling plus gut-microbiome response, rather than a simple single-strain function story. | Journal-fit and trend reasoning were not converted into proof of novelty or acceptance likelihood. |
| **Reef** | Organized heterogeneous evidence layers: mouse fecal 16S, fermentation-liquid 16S, ITS, targeted SCFA, untargeted metabolomics, and toxicology-support outputs. | Resource routing was kept separate from mechanistic validation. |
| **Iceberg** | Downgraded over-strong claims around beta-diversity interpretation, direct microbiome-metabolome correlation, and toxicity radar interpretation. | Association was not written as causality; unmatched systems were not treated as paired sample evidence. |
| **Anchor** | Rechecked statistical and validation logic, including p-value/FDR framing, correlation thresholds, PERMANOVA wording, and main-versus-supplement recalculation rules. | Figures were required to be recomputed when analysis sets changed; unstable groups were not hidden without an audit trail. |
| **Compass** | Built the manuscript route: fermentation remodels the broth metabolome, candidate exposure features emerge, mouse microbiome responses move in rescue-like directions, and mechanism remains cautiously framed. | A promising narrative was kept separate from causal mechanism proof. |
| **Harbor** | Preserved group-label decisions, source-data packaging logic, main/supplement figure routing, and why some analyses stayed exploratory or supplementary. | Unconfirmed submission or review status was not recorded as fact. |

## Project-Specific Decisions

### Mouse 29-Sample 16S Layer

The mouse 16S group map was stabilized for project memory:

| Label | Project meaning |
|---|---|
| `D` | target-drug low dose |
| `G` | target-drug high dose |
| `K` | blank |
| `M` | E. coli model |
| `Y` | positive control |
| `Z` | tentative medium-dose group, moved out of the main figure set |

OCEAN kept the `Z` group as a documented supplement-oriented layer rather than silently deleting it. Main beta-diversity figures had to be recomputed after removing `Z`, not merely redrawn after hiding points.

Interpretation boundary: incomplete separation on PCoA was not treated as experimental failure; it was treated as partial community-level differentiation.

### Fermentation Multi-Omics Layer

The fermentation-side integration involved matched DH samples and multiple evidence layers:

- fermentation-liquid 16S;
- fermentation-liquid ITS;
- targeted SCFA;
- untargeted metabolomics;
- curated metabolite co-variation modules;
- selected exploratory microbe-metabolite associations.

The important Iceberg boundary was:

> Fermentation-liquid metabolite measurements and mouse fecal 16S measurements are not the same sample layer, so they cannot be written as strict individual-level metabolite-taxon correlations across systems.

Safe framing:

- direct sample-wise association can be discussed only within the matched fermentation-side panel;
- cross-system links should be phrased as exposure-feature / response-feature alignment;
- causal mechanism requires direct validation beyond these records.

### Deep Metabolite Modules

The project used six metabolite co-variation modules in the deep DH integration. These are not the same as the seven OCEAN workflow modules.

| Deep metabolite module | Practical role in the project | Evidence boundary |
|---|---|---|
| `Module_1` | Main DH signature module and center of the curated interpretation chain. Representative themes included lactate/acidification, carbohydrate-release context, fermentation-aroma context, newly emerged DH features, aromatic-acid context, and organic-acid context. | Strongest narrative module, but still not single-metabolite causal proof. |
| `Module_2` | Small auxiliary mixed-direction module. | Not suitable as a headline mechanism. |
| `Module_3` | Very small mixed module. | Too small for a major claim. |
| `Module_4` | Secondary mixed module with modest support. | Supportive only. |
| `Module_5` | Small secondary module. | Supportive only. |
| `Module_6` | Balanced-direction module. | Not a strong narrative anchor. |

The key memory rule is:

> OCEAN has seven workflow modules; this project's metabolomics integration had six metabolite modules. Do not confuse the two.

### Toxicology Support Layer

OCEAN kept toxicology outputs as screening support.

Safe wording:

- candidate compounds;
- in silico toxicity watchlist;
- route-level or endpoint-level predicted activity;
- follow-up validation needed.

Unsafe wording avoided:

- proven toxic mechanism;
- confirmed intestinal-toxic target;
- validated compound-level harm from prediction alone.

## Public Outcome

This project became an OCEAN application case because it exercised all seven modules on one real biomedical/biological research workflow:

- food-fermentation evidence organization;
- microbiome analysis interpretation;
- metabolomics integration boundary-setting;
- toxicology support calibration;
- main-versus-supplement figure routing;
- manuscript story control;
- Harbor memory for future revision or submission work.

The public lesson is not that OCEAN proves the whole-wheat broth mechanism. The lesson is that OCEAN can help keep a complex multi-omics manuscript workflow evidence-bound, auditable, and harder to overclaim.

## Workflow Lesson: Audit Is Not Line Editing

A later manuscript-revision pass exposed an important usability boundary. The seven-module critique was useful while the evidence structure, analysis route, claim strength, and manuscript story were still being designed. It was not an appropriate default for sentence-level editing after the manuscript text had already been drafted.

The failure pattern was channel mixing: module labels, deletion or supplementation instructions, evidence limitations, and author-only decisions could appear beside proposed replacement prose and become easy to paste into the manuscript itself.

OCEAN now separates this work by lifecycle:

- **Design / Audit** keeps the relevant critical modules visible while experiments, analyses, and claims are still being shaped.
- **Manuscript Revision** returns clean replacement prose first and keeps audit notes or author queries outside the manuscript.
- **Pre-submission Stress Test** can reopen adversarial multi-module critique, but safe rewrites remain isolated from the audit report.
- **Reviewer Response** separates response-letter language, revised manuscript text, and author-only decisions.

This change preserves critical claim checking without turning a finished manuscript paragraph into an audit worksheet.

## What Is Not Published Here

This repository does not publish:

- raw OTU tables, metabolomics tables, or SCFA tables;
- raw figure packages or unpublished manuscript files;
- collaborator-only notes;
- private submission records;
- reviewer comments or journal correspondence;
- exact unpublished claim wording from manuscript drafts.

Future updates should add dated process notes only when the project owner confirms the manuscript stage, public artifact boundary, and release-safe wording.
