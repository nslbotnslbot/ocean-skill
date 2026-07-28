# Using OCEAN

[中文使用指南](usage-guide.zh-CN.md)

OCEAN is a model-neutral biomedical research workflow for navigating claims,
evidence, study design, manuscript revision, and concise project records. You
do not need to learn its seven internal modules before using it.

The shortest rule is:

> Tell OCEAN what you are trying to accomplish and provide the evidence you
> actually have.

## 1. Install in 60 seconds

Install the skill from GitHub:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo nslbotnslbot/ocean-skill \
  --path skills/ocean \
  --ref main
```

Open a new Codex session so the skill list refreshes, then test it:

```text
Use $ocean to explore this research idea:
Can a microbiome-derived metabolite improve response to immunotherapy?
Give me the short Decision Card and state what cannot yet be concluded.
```

For a temporary installation, remove it after testing:

```bash
rm -rf ~/.codex/skills/ocean
```

If the repository is already cloned locally:

```bash
cp -R skills/ocean ~/.codex/skills/
```

## 2. What you can give OCEAN

OCEAN can start from:

- one sentence or an early research idea;
- a research question, hypothesis, or proposed claim;
- a DOI, PMID, URL, abstract, preprint, or PDF;
- a manuscript section or complete manuscript;
- a proposal, protocol, analysis plan, or model description;
- figures, tables, database records, or public tool outputs;
- reviewer or editor comments;
- a collaboration question;
- a confirmed project or submission-status update.

The smaller the input, the narrower the safe conclusion. OCEAN should proceed
with a bounded answer rather than inventing missing information.

## 3. Choose an outcome, not a module

OCEAN has five user-facing modes:

| Mode | Use it when you want to | Default result |
|---|---|---|
| **Explore** | understand a paper, idea, source, or field | clear explanation plus evidence limits |
| **Design** | turn an idea or gap into a feasible study | research route, decisive controls, next experiment |
| **Audit** | test claims, methods, validation, or submission readiness | claim verdicts, risks, missing evidence, fixes |
| **Revise** | improve finished manuscript text | clean replacement text; notes kept separate |
| **Track** | preserve a concise project or submission record | Status, Progress, Next, Public Boundary |

OCEAN selects the minimum internal modules needed. It should not run all seven
modules merely to display the framework.

You may name the mode explicitly:

```text
Use $ocean in Design mode...
```

Or state the task naturally:

```text
Use $ocean to explain this paper for a journal club.
```

Explicit `$ocean` invocation is recommended when testing installation or when
you want to ensure the workflow is used.

## 4. Ready-to-use prompts

### Explore a paper

```text
Use $ocean to explore the attached paper.
Audience: a graduate journal club.
Explain the research question, design, strongest result, main limitation,
and what the paper does not prove. Use the short Decision Card first.
```

### Explore a literature landscape

```text
Use $ocean to map recent evidence around this question:
<research question>.
Search public sources if tools are available. Separate inspected full text,
abstract-only evidence, and uninspected candidates. Do not invent citations.
```

### Design a study from one idea

```text
Use $ocean in Design mode for this idea:
<one-sentence idea>.
Define the highest safe claim, the minimum viable study, the decisive controls,
independent validation, likely failure points, and the next three actions.
```

### Review a proposal

```text
Use $ocean to assess this proposal.
Give me the overall decision first, then only the three issues most likely to
change feasibility or scientific value. Do not score unless it helps compare
alternatives.
```

### Audit a manuscript or model

```text
Use $ocean in Audit mode on the attached manuscript.
Check claim support, data leakage, benchmark fairness, external validation,
reproducibility, and whether association/prediction is overstated as mechanism
or clinical utility. Use Standard output.
```

### Revise finished manuscript text

```text
Use $ocean in Revise mode.
Return clean replacement text first. Keep audit findings, reviewer language,
and author questions outside the manuscript prose. Do not invent new data,
methods, citations, or results.

Text:
<paste text>
```

### Critique and revise without mixing channels

```text
Use $ocean to audit and revise this Discussion section.
Output three separate blocks:
1. audit findings;
2. clean revised text;
3. author-only decisions.
Never put critique labels or editing instructions into the revised prose.
```

### Prepare a reviewer response

```text
Use $ocean to handle these reviewer comments.
For each comment, separate:
1. response-letter text;
2. revised manuscript text;
3. author-only action or missing evidence.
Do not claim that an experiment or analysis was completed unless I provide it.
```

### Track a project

```text
Use $ocean in Track mode.
Confirmed status: submitted to medRxiv and awaiting screening.
Update only Status, Progress, Next, and Public Boundary.
Do not describe it as posted, under review, accepted, or published.
Ask before any public GitHub update.
```

## 5. Output depth

### Decision Card

This is the default for ordinary first-turn and narrow questions:

1. Conclusion
2. Basis
3. What cannot currently be judged
4. Main risk
5. Next step

It intentionally hides module names, large matrices, journal tiers, and scores.

### Standard

Use Standard for explicit multi-claim audits, structured research plans,
collaboration analysis, or journal-positioning decisions. It may include an
evidence boundary, claim-evidence matrix, priority risks, missing evidence, and
next actions.

### Deep

Use Deep only for an explicit full manuscript review, reviewer simulation, or
detailed report. Deep output may add reviewer concerns, safe claim rewrites,
and a decision memo.

### Revision

Finished-text editing uses a separate contract:

1. clean replacement text;
2. change notes that do not enter the manuscript;
3. author questions only when necessary.

## 6. Make the evidence boundary explicit

For high-stakes or incomplete material, ask OCEAN to state:

- what was inspected;
- what was not inspected;
- what cannot be concluded;
- what source, file, control, or analysis is needed next.

Useful wording:

```text
Treat the abstract as abstract-level evidence only.
Do not infer full methods, sample size, external validation, or clinical
utility unless those details are inspected.
```

OCEAN should distinguish:

- hypothesis from evidence;
- association from causality;
- database co-occurrence from mechanism;
- model prediction from experimental validation;
- internal validation from external validation;
- technical performance from clinical utility;
- submission from posting, review, acceptance, or publication.

## 7. Files, sources, and web search

For the strongest answer:

1. Attach the relevant PDF, manuscript, figures, tables, or notes.
2. Provide a DOI, PMID, registry identifier, or official URL when available.
3. Say whether public web search is allowed or desired.
4. State whether OCEAN may inspect only supplied material or gather additional
   public sources.
5. Identify confidential, patient-level, unpublished, or embargoed material.

A search result, title, abstract, API response, or database record is not
automatically full scientific evidence. OCEAN records source provenance and
stops at the highest claim level the inspected evidence supports.

## 8. Tools and APIs

OCEAN's core workflow does not require a specific model or paid API. Database
adapters and bioinformatics wrappers are optional routes.

- A wrapper can create a dry-run query, provenance packet, or launch plan.
- Live calls require the relevant public endpoint, API key, local software,
  database, license, reference index, compute, and user approval when needed.
- A tool folder does not prove that the tool is installed or executable.
- Tool output is provenance or analysis evidence only after the actual run and
  relevant files have been inspected.
- Never commit API keys or private `.env` files.

## 9. Project tracking and GitHub safety

Use Track only when the work has become a real, traceable project. Keep the
public page concise:

1. Status
2. Progress
3. Next
4. Public Boundary

Do not publish raw data, patient-level information, confidential manuscripts,
private reviewer reports, API keys, unconfirmed submission outcomes, or claims
stronger than the inspected evidence.

OCEAN may prepare a local update, but a public GitHub push requires explicit
user approval.

## 10. Common questions

### Do I need to know the seven modules?

No. Modes are the user interface; modules are the internal scientific engine.
Ask for a module-by-module explanation only when it helps you inspect the
workflow.

### Can OCEAN start from one sentence?

Yes. It should label the result as an early design or evidence-bounded
hypothesis, not as a validated conclusion.

### Does OCEAN always criticize everything?

No. Explore explains, Design plans, Audit criticizes, Revise rewrites cleanly,
and Track records status. A normal revision request should not become a full
reviewer report.

### Can OCEAN execute every listed bioinformatics tool?

No. Coverage in the resource map means OCEAN can route or packetize the tool.
Execution depends on installation, runtime, databases, licenses, compute, and
input files.

### What if `$ocean` is not recognized?

Confirm that `~/.codex/skills/ocean/SKILL.md` exists, then open a new Codex
session. Reinstall from `main` if the folder is incomplete.

### Does OCEAN provide clinical advice?

No. It may assess biomedical evidence and clinical-study claims, but it must not
replace medical judgment or provide unsupported diagnosis or treatment advice.

