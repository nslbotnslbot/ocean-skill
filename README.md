
<img width="1672" height="941" alt="OCEAN" src="https://github.com/user-attachments/assets/942d67fb-5bce-46e1-8450-9dc8c4e01f23" />


# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

OCEAN is a lightweight Codex-compatible skill for scientific claim auditing, literature and evidence discovery, biomedical evidence review, AI-for-Science manuscript evaluation, journal positioning, collaboration boundary analysis, and evidence-bound idea extraction from peer review.

## What this is

This package is designed for personal use inside Codex and for publishing as a small GitHub repository.

It provides two entry points:

1. `AGENTS.md` at the repository root, so Codex can automatically read project-level instructions.
2. `skills/ocean/SKILL.md`, so the same workflow can be used as a portable skill folder if your Codex interface supports Skills.

## 中文说明

OCEAN 是一个轻量级、兼容 Codex 的 skill，用于科学 claim 审核、文献与证据扫描、生物医学证据评估、AI-for-Science manuscript 评价、期刊定位、合作边界分析，以及从 peer review / 审稿意见中反推可验证的研究 idea。

这个仓库提供两个入口：

1. 仓库根目录的 `AGENTS.md`，用于让 Codex 自动读取项目级说明。
2. `skills/ocean/SKILL.md`，用于把同一套工作流作为可移植的 Codex skill 使用。

OCEAN 的模块顺序是：

1. **Sonar**：先扫描文献、证据、DOI/preprint/public review 来源，并建立可追踪 source packet。
2. **Current**：看领域趋势和方向流动。
3. **Reef**：把知识图谱、数据库、benchmark、cohort 和资源证据组织起来。
4. **Iceberg**：审 claim 下面的证据支撑和隐藏风险。
5. **Anchor**：做验证、复现、benchmark、leakage 和 reproducibility 检查。
6. **Compass**：基于证据决定研究计划、实验设计、idea 优先级和投稿策略。
7. **Harbor**：沉淀成报告、工作区记忆和协作记录。

OCEAN 适合用来检查 manuscript、preprint、AI-agent / AI-for-Science 项目、生物医学 AI 研究、知识图谱或数据库证据系统、临床预测模型、合作贡献边界、投稿定位、reviewer-style 的预审稿压力测试，以及从真实或公开 peer review report 中抽取可做的补充实验、修稿路径和新项目 idea。

快速安装：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo nslbotnslbot/ocean-skill \
  --path skills/ocean \
  --ref main
```

安装后重启 Codex 或开启新的 Codex 会话，并测试 `$ocean` 是否能被识别：

```text
Use $ocean to audit this abstract-only claim.
State inspected / not inspected / cannot conclude / needed next.
```

如果只是临时测试，可以在测试后删除：

```bash
rm -rf ~/.codex/skills/ocean
```

默认输出语言是中文。OCEAN 的核心原则是保持证据边界清晰：必须区分假说与证据、相关性与因果、数据库共现与机制、内部验证与外部验证、系统展示与科学发现、轻量建议与可构成署名贡献的实质性参与。

Sonar 的检索结果只作为 discovery evidence，不等于全文证据。OCEAN 必须区分已检索、已检查、未检查、不能判断和下一步需要什么，然后才能进入 claim、novelty、publication、mechanism 或 clinical utility 判断。

当从审稿意见中反推 idea 时，OCEAN 会把 reviewer comments 当作 pressure signals，而不是论文事实、创新性证明或发表保证。真正的 idea 判断仍需要 manuscript/full text、相关文献、数据、方法和验证资源支持。

公开验证摘要位于 `docs/evaluation/`，简版结果在 `docs/evaluation/round-1-5-results.md`，发布记录在 `CHANGELOG.md`，内部 release validation log 位于 `skills/ocean/evals/release-validation-log.md`。

这些验证记录测试的是 OCEAN 的工作流行为：它是否能保持“已检查 / 未检查 / 不能判断 / 还需要什么”的边界，并避免 unsupported claims。它们不证明任何论文、preprint、benchmark、dataset、peer review report 或生物医学结论本身的科学正确性。

## Best use cases

Use this when you ask Codex to review:

- manuscripts
- preprints
- literature and evidence around a specific claim
- DOI/preprint/public review source packets
- system papers
- AI-agent / AI-for-Science projects
- biomedical AI studies
- bioinformatics studies
- database / knowledge graph / CTD-style evidence systems
- clinical prediction models
- collaboration contribution boundaries
- paper positioning and journal strategy
- reviewer-style critique and pre-submission stress testing
- peer review reports, reviewer comments, editor letters, and rebuttal exchanges
- review-to-idea extraction for repair ideas, extension ideas, new project ideas, and collaboration opportunities

## Quick start

### Install From GitHub

Install the skill from this repository:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo nslbotnslbot/ocean-skill \
  --path skills/ocean \
  --ref main
```

Then restart Codex or open a new Codex session and test recognition:

```text
Use $ocean to audit this abstract-only claim.
State inspected / not inspected / cannot conclude / needed next.
```

If you only wanted a temporary test install, remove it after testing:

```bash
rm -rf ~/.codex/skills/ocean
```

### Local Copy

If you already cloned this repository, copy the skill folder into your Codex skills directory:

```bash
cp -R skills/ocean ~/.codex/skills/
```

Then ask Codex:

```text
Use $ocean to evaluate the uploaded manuscript.
Please output in Chinese.
Focus on scientific value, reliability, key risks, missing validation, collaboration contribution boundary, and journal positioning.
Use the standard OCEAN output format unless I ask for a quick or deep report.
```

For Sonar evidence discovery:

```text
Use $ocean Sonar to scan literature and evidence for this claim.
Build a traceable source packet with DOI/URL, source tier, inspected content, main evidence, main limitation, and downstream handoff.
Do not treat search-result snippets as full-paper evidence.
```

For reviewer-to-idea extraction:

```text
Use $ocean on these reviewer comments.
Extract repair ideas, extension ideas, possible new project ideas, and my realistic contribution boundary.
Do not treat reviewer comments as facts; state inspected / not inspected / cannot conclude / needed next.
```

For an empty review report skeleton:

```bash
python3 skills/ocean/scripts/make_review_skeleton.py \
  --title "My AI for Science Project" \
  --project-type "AI-agent system / biomedical evidence audit" \
  --out outputs/review_skeleton.md
```

For a claim table template:

```bash
python3 skills/ocean/scripts/make_claim_table.py \
  --out outputs/claim_table.csv
```

After filling the CSV, validate and summarize it:

```bash
python3 skills/ocean/scripts/check_claim_table.py \
  outputs/claim_table.csv \
  --out outputs/claim_table_summary.md
```

## Output principle

Default output language: Chinese.

The analysis must be direct, critical, and evidence-bound. Do not overstate novelty or validity. Always distinguish:

- hypothesis vs evidence
- association vs causality
- database co-occurrence vs mechanism
- internal validation vs external validation
- system demonstration vs scientific discovery
- literature search result vs inspected source evidence
- light advice vs authorship-level contribution
- reviewer pressure signal vs verified manuscript fact

By default, OCEAN uses a fixed output contract: audit card, evidence boundary, claim-evidence matrix, risk register, missing evidence/analysis, collaboration boundary, journal positioning, next actions, and scores. Use quick mode only for narrow questions and deep mode for full manuscript or reviewer-style reports.

For Sonar tasks, OCEAN adds a search-task definition, search log, candidate source table, evidence coverage/gap table, and Sonar evidence boundary before downstream audit.

For review-to-idea tasks, OCEAN adds an idea pool, priority ranking, and overclaim boundary section so reviewer comments become testable next steps rather than unsupported conclusions.

## Repository layout

```text
docs/evaluation/
├── README.md
├── round-1-5-results.md
└── reference-materials/
    ├── boundary-cases.md
    └── public-sources.md
skills/ocean/
├── SKILL.md
├── agents/openai.yaml
├── evals/
│   ├── anti-hallucination-cases.md
│   ├── contamination-resistance-round5.md
│   ├── forward-test-cases.md
│   ├── public-source-protocol.md
│   ├── real-article-adversarial-cases.md
│   ├── release-validation-log.md
│   └── source-candidates.md
├── references/
│   ├── audit-lenses.md
│   ├── claim-evidence-table.md
│   ├── output-contract.md
│   ├── reviewer-lens.md
│   ├── reviewer-to-idea.md
│   ├── review-report.md
│   └── sonar.md
└── scripts/
    ├── make_claim_table.py
    ├── check_claim_table.py
    └── make_review_skeleton.py
```

## Evaluation summary

Public-facing validation notes are in `docs/evaluation/`. The concise summary is `docs/evaluation/round-1-5-results.md`, and public source identifiers are in `docs/evaluation/reference-materials/public-sources.md`.

These files show what was tested and what passed without copying private materials, long paper passages, or hidden-answer logs. The internal release log remains in `skills/ocean/evals/release-validation-log.md`.

Release notes are tracked in `CHANGELOG.md`.

## Development checks

Run the sample scripts before publishing:

```bash
python3 skills/ocean/scripts/make_claim_table.py --out outputs/claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py examples/sample_claim_table.csv --out outputs/claim_table_summary.md
python3 skills/ocean/scripts/make_claim_table.py --empty --out outputs/empty_claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py outputs/empty_claim_table.csv --out outputs/empty_claim_table_summary.md
```

Before release, run the manual forward tests in `skills/ocean/evals/forward-test-cases.md` using real user-provided or public, source-traceable materials. Use `skills/ocean/evals/anti-hallucination-cases.md` for incomplete, missing, contradictory, or non-traceable evidence tests. Use `skills/ocean/evals/public-source-protocol.md` to select DOI papers, bioRxiv/medRxiv preprints, and public peer review reports, track concrete candidates in `skills/ocean/evals/source-candidates.md`, and summarize release-gate outcomes in `skills/ocean/evals/release-validation-log.md`.

## License

MIT License. See `LICENSE`.
