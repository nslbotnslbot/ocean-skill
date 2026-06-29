# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[English README](README.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow.jpg)

OCEAN 是一个轻量级、兼容 Codex 的外部审计层，用于科学 claim 审核、生物医学证据审查、AI-for-Science 稿件评估、期刊定位，以及协作边界分析。

OCEAN 是一个独立的开源工作流项目。它的证据发现模块命名为 **Sounding**：这是一个 source-packet 工作流，用于扫描文献、证据边界和可追踪的 review 材料。OCEAN 审计的是已有来源能支持什么、不能支持什么；它不管理某个研究项目的内部执行或发布流程。

## 这是什么

这个 package 设计用于在 Codex 中个人使用，也可以作为一个小型 GitHub 仓库发布。

它提供两个入口：

1. 仓库根目录的 `AGENTS.md`，让 Codex 自动读取项目级指令。
2. `skills/ocean/SKILL.md`，如果你的 Codex 界面支持 Skills，同一个工作流也可以作为可移植的 skill 文件夹使用。

## 边界和非目标

OCEAN 应该被描述为一个 **基于 source packet 的 claim-evidence 外部审计层**。它的核心对象是 source packet、evidence gate、claim audit card、safe rewrite、negative space、reviewer-risk ticket 和 validation plan。

更完整的公开定位说明见 [`docs/project-boundary.md`](docs/project-boundary.md)。

OCEAN 不是：

- autonomous AI scientist；
- 执行实验或生成发现的系统；
- 内部 evidence ledger 或项目发布工作流；
- human-supervised execution-package-to-release-gate 系统；
- 面向单一研究项目的 discovery endpoint spectrum。

公开介绍 OCEAN 时，优先使用 **external claim-evidence auditing**、**evidence-type gating**、**source-packet construction**、**safe claim rewriting** 和 **public adversarial case matrices**。不要把 evidence ledger、paired non-claim、endpoint ladder 或 release gate 写成中心贡献。

## 适用场景

当你让 Codex 审查以下内容时，可以使用 OCEAN：

- manuscript
- preprint
- system paper
- AI-agent / AI-for-Science 项目
- 生物医学 AI 研究
- 生物信息学研究
- database / knowledge graph / CTD 风格的证据系统
- 临床预测模型
- 合作贡献边界
- 论文定位与期刊策略
- reviewer 风格批判和投稿前压力测试

## 模块流程

OCEAN 按顺序使用七个模块；这是一个外部审计序列，不是实验执行循环：

1. **Sounding**：扫描文献、证据、DOI/preprint/public review 来源，并建立可追踪 source packet。
2. **Current**：分析领域趋势和研究方向流动。
3. **Reef**：整理知识图谱、数据库、benchmark、cohort 和资源证据。
4. **Iceberg**：审核表面结论之下的 claim 支撑。
5. **Anchor**：设计 validation、replication、benchmark、leakage 和 reproducibility 检查。
6. **Compass**：把证据转化为研究计划、实验设计、idea 优先级和期刊策略。
7. **Harbor**：保存报告、工作区记忆和协作记录。

## 快速开始

### 从 GitHub 安装

从这个仓库安装 skill：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo nslbotnslbot/ocean-skill \
  --path skills/ocean \
  --ref main
```

然后重启 Codex，或打开新的 Codex session，并测试识别：

```text
Use $ocean to audit this abstract-only claim.
State inspected / not inspected / cannot conclude / needed next.
```

如果只是临时测试安装，测试后可以删除：

```bash
rm -rf ~/.codex/skills/ocean
```

### 本地复制

如果你已经 clone 了这个仓库，可以把 skill 文件夹复制到 Codex skills 目录：

```bash
cp -R skills/ocean ~/.codex/skills/
```

然后向 Codex 提问：

```text
Use $ocean to evaluate the uploaded manuscript.
Please output in Chinese.
Focus on scientific value, reliability, key risks, missing validation, collaboration contribution boundary, and journal positioning.
Use the standard OCEAN output format unless I ask for a quick or deep report.
```

生成空的 review report skeleton：

```bash
python3 skills/ocean/scripts/make_review_skeleton.py \
  --title "My AI for Science Project" \
  --project-type "AI-agent system / biomedical evidence audit" \
  --out outputs/review_skeleton.md
```

生成 claim table 模板：

```bash
python3 skills/ocean/scripts/make_claim_table.py \
  --out outputs/claim_table.csv
```

填写 CSV 后，验证并总结：

```bash
python3 skills/ocean/scripts/check_claim_table.py \
  outputs/claim_table.csv \
  --out outputs/claim_table_summary.md
```

## 输出原则

默认输出语言：中文。

分析必须直接、批判，并且受证据边界约束。不要夸大 novelty 或 validity。始终区分：

- hypothesis vs evidence
- association vs causality
- database co-occurrence vs mechanism
- internal validation vs external validation
- system demonstration vs scientific discovery
- light advice vs authorship-level contribution

默认情况下，OCEAN 使用固定 output contract：audit card、evidence boundary、claim-evidence matrix、risk register、missing evidence/analysis、collaboration boundary、journal positioning、next actions 和 scores。只有在窄问题中使用 quick mode；完整 manuscript 或 reviewer-style report 使用 deep mode。

## 仓库结构

```text
.env.ocean.example
README.zh-CN.md
assets/
└── ocean-polar-workflow.jpg
docs/
├── project-boundary.md
└── evaluation/
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
│   ├── sounding-multimodel-cases.json
│   ├── sounding-multimodel-models.example.json
│   ├── sounding-multimodel-r1-codex-slice-results.md
│   ├── sounding-multimodel-strict-eval.md
│   └── source-candidates.md
├── references/
│   ├── audit-lenses.md
│   ├── claim-evidence-table.md
│   ├── output-contract.md
│   ├── reviewer-lens.md
│   ├── review-report.md
│   └── sounding.md
└── scripts/
    ├── make_claim_table.py
    ├── check_claim_table.py
    ├── make_review_skeleton.py
    └── run_sounding_multimodel_eval.py
```

## 评估总结

面向公开发布的 validation notes 位于 `docs/evaluation/`。简洁总结在 `docs/evaluation/round-1-5-results.md`，公开来源标识符在 `docs/evaluation/reference-materials/public-sources.md`。

当前 Sounding model-comparison 计划包括 Qwen、DeepSeek、Kimi、MiniMax、Gemini、Claude，以及一个 Perplexity retrieval control group。Perplexity 被作为 retrieval-oriented control 处理，因为它的产品定位强调 answer/search grounding；它不是 OCEAN 的依赖。这个比较的目标，是测试不同模型能否稳定遵循同一个 Sounding workflow、output contract、evidence boundary 和 source-packet handoff。

这些文件说明测试了什么、哪些通过了，同时不会复制 private materials、长篇论文段落或 hidden-answer logs。公开 evaluation materials 被设计为可复用的 source-boundary checks，不是内部研究轨迹记录，也不是 discovery claim。内部 release log 保留在 `skills/ocean/evals/release-validation-log.md`。

## 开发检查

发布前运行示例脚本：

```bash
python3 skills/ocean/scripts/make_claim_table.py --out outputs/claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py examples/sample_claim_table.csv --out outputs/claim_table_summary.md
python3 skills/ocean/scripts/make_claim_table.py --empty --out outputs/empty_claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py outputs/empty_claim_table.csv --out outputs/empty_claim_table_summary.md
python3 skills/ocean/scripts/run_sounding_multimodel_eval.py --dry-run
```

发布前，请使用真实用户提供的、或公开且 source-traceable 的材料，运行 `skills/ocean/evals/forward-test-cases.md` 中的 manual forward tests。使用 `skills/ocean/evals/anti-hallucination-cases.md` 测试 incomplete、missing、contradictory 或 non-traceable evidence。使用 `skills/ocean/evals/public-source-protocol.md` 选择 DOI papers、bioRxiv/medRxiv preprints 和 public peer review reports；在 `skills/ocean/evals/source-candidates.md` 中追踪具体候选；使用 `skills/ocean/evals/sounding-multimodel-strict-eval.md` 进行 model-robustness checks；并在 `skills/ocean/evals/release-validation-log.md` 中总结 validation-check outcomes。

## License

MIT License。见 `LICENSE`。
