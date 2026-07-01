# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[English README](README.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow.jpg)

OCEAN 是一个轻量级、兼容 Codex 的技能工作流，用于医学研究与生物学研究中的 claim-evidence 导航。它关注 biomedical research，理解 AI 研究场景，但不只服务于 AI 论文：也可以支持生物医学 AI、生物学 AI、manuscript、数据库、知识图谱、临床预测、期刊定位和协作边界分析。

OCEAN 是一个独立的开源工作流项目。它的证据发现模块命名为 **Sounding**：这是一个 source-packet 工作流，用于扫描文献、证据边界和可追踪的 review 材料。

## 这是什么

这个 package 设计用于在 Codex 中个人使用，也可以作为一个小型 GitHub 仓库发布。

它提供两个入口：

1. 仓库根目录的 `AGENTS.md`，让 Codex 自动读取项目级指令。
2. `skills/ocean/SKILL.md`，如果你的 Codex 界面支持 Skills，同一个工作流也可以作为可移植的 skill 文件夹使用。

## 范围

OCEAN 的定位是：**biomedical first, AI-aware, evidence-boundary centered**。

- 核心范围：生物医学研究。
- 两个主要方向：医学研究和生物学研究。
- 当前优先场景：medical AI research、biological AI research、生物信息学、临床预测、知识图谱、数据库、public review 信号、manuscript 和研究规划。
- 不适合：只做普通论文总结、无证据的临床建议、虚构数据，或没有生物医学证据问题的泛科学讨论。

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

OCEAN 按顺序使用七个模块。每个模块应该完成不同的事件，并把一个具体产物交给下一步。更完整的公开说明见 `docs/module-map.md`。

| 顺序 | Module | 完成的事件 | 典型产物 | 当前验证状态 |
|---:|---|---|---|---|
| 1 | **Sounding** | 证据发现和 source boundary 建立 | Source packet、Evidence Radar Map、Negative Space、Handoff Ticket | 已完成 strict multi-model eval |
| 2 | **Current** | 领域趋势和方向流动分析 | Trend map、近期流动、机会/风险说明 | M1 已覆盖；M2 已筛查 |
| 3 | **Reef** | 生物医学资源、KG、数据库证据组织 | Resource provenance map、database/KG evidence table | M1 已覆盖；M2 已筛查 |
| 4 | **Iceberg** | 审核表面 claim 下面的证据支撑 | Claim-evidence matrix、降级/改写建议 | M1 已覆盖；M2 已筛查 |
| 5 | **Anchor** | 验证、复现、leakage、benchmark、reproducibility 规划 | Validation checklist、benchmark/leakage plan、复现风险 | M1 已覆盖；M2 已筛查 |
| 6 | **Compass** | 研究计划和策略决策 | Idea card、实验计划、期刊/合作策略 | M1 已覆盖；M2 已筛查 |
| 7 | **Harbor** | 审计报告沉淀和协作边界记忆 | Final audit report、decision note、贡献边界记录 | M1 已覆盖；M2 已筛查 |

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
├── module-map.md
└── evaluation/
    ├── README.md
    ├── round-1-5-results.md
    ├── sounding-adversarial-case-library.md
    └── reference-materials/
        ├── boundary-cases.md
        └── public-sources.md
skills/ocean/
├── SKILL.md
├── agents/openai.yaml
├── evals/
│   ├── anti-hallucination-cases.md
│   ├── contamination-resistance-round5.md
│   ├── full-ocean-workflow-cases.md
│   ├── full-ocean-workflow-protocol.md
│   ├── ocean-module-m1-results.md
│   ├── ocean-module-m2-results.md
│   ├── ocean-module-m2-needs-review-triage.md
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
│   ├── anchor.md
│   ├── claim-evidence-table.md
│   ├── compass.md
│   ├── current.md
│   ├── harbor.md
│   ├── iceberg.md
│   ├── module-handoff.md
│   ├── output-contract.md
│   ├── reef.md
│   ├── reef-api-adapters.md
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

目前最深入的 module-specific strict testing 仍然集中在 **Sounding**。R2 和 R3 测试的是 Sounding source-packet workflow，模型包括 Qwen、DeepSeek、Kimi、MiniMax、Gemini、Claude，以及一个 Perplexity retrieval control group。M1 增加了七个 module 的全覆盖测试，M2 对 98 个 M1 输出做了第一轮 heuristic scoring。Perplexity 被作为 retrieval-oriented control 处理，因为它的产品定位强调 answer/search grounding；它不是 OCEAN 的依赖。

仓库也包含 full-workflow protocol 和 case seeds，用于测试一篇论文、一个 idea、一段 proposal、一条 review comment 或一个 resource/KG seed 是否能通过七个 OCEAN module，并保持稳定的 handoff 和 evidence boundary。

更早的 anti-hallucination 和 contamination-resistance 测试覆盖了 OCEAN 的 evidence-boundary 行为和 claim downgrade 纪律。M1/M2 仍然应被理解为 coverage + heuristic screening，而不是最终科学正确性验证或模型排行榜。

这些文件说明测试了什么、哪些通过了，同时不会复制 private materials、长篇论文段落或 hidden-answer logs。内部 release log 保留在 `skills/ocean/evals/release-validation-log.md`。

## 开发检查

发布前运行示例脚本：

```bash
python3 skills/ocean/scripts/make_claim_table.py --out outputs/claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py examples/sample_claim_table.csv --out outputs/claim_table_summary.md
python3 skills/ocean/scripts/make_claim_table.py --empty --out outputs/empty_claim_table.csv
python3 skills/ocean/scripts/check_claim_table.py outputs/empty_claim_table.csv --out outputs/empty_claim_table_summary.md
python3 skills/ocean/scripts/run_sounding_multimodel_eval.py --dry-run
```

发布前，请使用真实用户提供的、或公开且 source-traceable 的材料，运行 `skills/ocean/evals/forward-test-cases.md` 中的 manual forward tests。使用 `skills/ocean/evals/anti-hallucination-cases.md` 测试 incomplete、missing、contradictory 或 non-traceable evidence。使用 `skills/ocean/evals/public-source-protocol.md` 选择 DOI papers、bioRxiv/medRxiv preprints 和 public peer review reports；在 `skills/ocean/evals/source-candidates.md` 中追踪具体候选；使用 `skills/ocean/evals/sounding-multimodel-strict-eval.md` 进行 model-robustness checks；使用 `skills/ocean/evals/full-ocean-workflow-protocol.md` 进行七模块 workflow 检查；并在 `skills/ocean/evals/release-validation-log.md` 中总结 release validation outcomes。

## License

MIT License。见 `LICENSE`。
