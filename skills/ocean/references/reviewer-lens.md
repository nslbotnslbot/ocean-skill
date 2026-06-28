# Reviewer Lens

Use this reference for reviewer-style critique, pre-submission stress testing, journal fit, and likely-objection prediction. Do not copy peer review reports into the final answer. Extract the review logic and apply it only to evidence the user provided or that was explicitly inspected.

## Reviewer Stance

Read as a skeptical but fair reviewer:

- Identify the central claim before judging details.
- Ask whether the strongest conclusion is directly supported by the strongest evidence.
- Penalize ambiguity in data source, cohort definition, labels, splits, and validation.
- Treat broad wording in the title, abstract, highlights, and conclusion as claims even when the results section is more cautious.
- Separate novelty of engineering integration from novelty of scientific insight.
- Separate useful tool demos from validated discovery, mechanism, or clinical utility.
- Prefer specific repair paths over generic criticism.

## Major-Criticism Patterns

### Contribution And Novelty

- The work may be useful but incremental because it combines known tools without a new method, dataset, discovery, or validation logic.
- The paper may overstate novelty if the contribution is a workflow, interface, or integration rather than a new scientific finding.
- The central research question may be unclear if the manuscript alternates between method paper, resource paper, and discovery paper.

### Evidence Support

- Strong claims need direct evidence, not only plausibility, examples, or selected case studies.
- A claim should be downgraded when evidence is indirect, internal-only, database-derived, text-mined, or based on model prediction without independent validation.
- A result shown in one disease, cohort, dataset, or benchmark should not be generalized to broad biomedical or clinical settings without external evidence.

### Validation And Leakage

- Internal validation is not external validation.
- Cross-validation does not prove generalization if there is patient, sample, site, time, preprocessing, feature, database, or literature leakage.
- Benchmarks are weak when baselines are under-tuned, outdated, evaluated on different data, or missing standard methods.
- Ablations are necessary when the manuscript claims that a pipeline component, agent tool, memory, retrieval source, or model choice drives performance.

### Causality And Mechanism

- Association, co-occurrence, database annotation, enrichment, literature mining, and model ranking do not establish mechanism.
- Mechanistic language requires perturbation, experimental intervention, longitudinal evidence, or strong causal design.
- Database overlap between discovery and validation should be flagged as circular validation.

### Clinical Or Translational Claims

- Clinical utility requires more than discrimination metrics.
- Ask for calibration, decision-curve analysis, subgroup performance, missing-data handling, temporal/site validation, and deployment consequences.
- Claims about patient benefit, diagnosis, prognosis, or treatment should be downgraded without human clinical evidence.

### AI-Agent And LLM Systems

- Require task definition, model/version, prompts, retrieval corpus, tool permissions, temperature/settings, and reproducible environment.
- Require hallucination/failure analysis when the system generates scientific claims or evidence summaries.
- Require expert evaluation when outputs require domain judgment.
- Require cost, latency, stability, and failure-mode reporting when the system is proposed as infrastructure.

## Reviewer Output Template

When the user asks for reviewer-style critique, include:

| Reviewer concern | Why it matters | Evidence inspected | Severity | Required fix |
|---|---|---|---:|---|

Use severity as:

- High: likely rejection or major revision issue.
- Medium: important but fixable with analysis, writing, or additional validation.
- Low: clarity, presentation, or framing issue.

## Claim Downgrade Rules

- "discovers" -> "prioritizes" unless independently validated.
- "mechanism" -> "hypothesis" unless causal evidence exists.
- "generalizes" -> "shows internal performance" unless external data exist.
- "clinically useful" -> "potentially relevant" unless clinical utility is tested.
- "validated by database" -> "supported by database records" unless independent validation exists.

## Response-To-Reviewer Preparation

For each major risk, classify the response strategy:

- Add evidence: new validation, ablation, benchmark, calibration, external dataset, expert evaluation, or failure analysis.
- Reframe claim: downgrade causal, clinical, generalization, or novelty language.
- Clarify methods: document data sources, splits, prompts, versions, preprocessing, and reproducibility.
- Limit scope: state boundaries explicitly rather than defending unsupported breadth.

Do not fabricate planned experiments, reviewer identities, acceptance odds, or journal policies.
