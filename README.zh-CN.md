# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[English README](README.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow-logo-v4.png)

OCEAN 是一个轻量级、兼容 Codex 的 biomedical claim-evidence skill，用于医学研究与生物学研究。它可以支持生物医学 AI、生物学 AI、manuscript、数据库、知识图谱、临床预测、验证规划、期刊定位和协作边界分析。Domain Lens 和 Data/Tool Router 会为 medical、biological、omics、clinical、drug、KG/database、proposal 和 collaboration 任务选择合适的证据标准。

它的证据发现模块命名为 **Sounding**：这是一个 source-packet 工作流，用于扫描文献、证据边界和可追踪的 review 材料。

**表面简单，底层严谨；当工作成为项目时，过程可以追踪。**

[中文详细使用指南](docs/usage-guide.zh-CN.md) |
[证据控制层 CLI](docs/evidence-control-plane.zh-CN.md) |
[Availability 审计验证](docs/availability-evidence-cards-v1.md) |
[English usage guide](docs/usage-guide.md)

## 这是什么

这个仓库提供位于 [`skills/ocean/`](skills/ocean/) 的可安装 skill，以及
简洁的中英文使用指南、可复用工具适配器和公开项目示例。

## 边界、范围和非目标

OCEAN 是一个 **基于 source packet 的 claim-evidence 科研工作流**。它的核心对象是 source packet、evidence gate、claim audit card、safe rewrite、negative space、reviewer-risk ticket 和 validation plan。

OCEAN 的定位是：**biomedical first, AI-aware, evidence-boundary centered**。

- 核心范围：生物医学研究。
- 两个主要方向：医学研究和生物学研究。
- 当前优先场景：medical AI research、biological AI research、生物信息学、临床预测、知识图谱、数据库、public review 信号、manuscript 和研究规划。
- 不适合：只做普通论文总结、无证据的临床建议、虚构数据，或没有生物医学证据问题的泛科学讨论。

机器可读的 Domain Lens 也为明确提出的 materials、chemistry 与 engineering
任务提供保守路由；这只是证据控制脚手架，不代表 OCEAN 的核心范围扩展到生物医学
之外，也不代表它在这些领域具备专家能力。

OCEAN 不是：

- autonomous AI scientist；
- 实验、领域专家或临床判断的替代品；
- 虚构证据或无依据临床建议的来源。

## 60 秒开始使用

使用者只需选择想完成的目标；OCEAN 会在内部选择最少且必要的模块。

| 模式 | 让 OCEAN 完成 | 默认可见结果 |
|---|---|---|
| **Explore** | 理解论文、idea、来源或领域 | 清楚解释，并说明证据边界 |
| **Design** | 把 idea、proposal 或缺口变成可行研究 | 研究路线、决定性对照、下一项实验 |
| **Audit** | 检查 claim、方法、验证或投稿准备度 | claim verdict、风险、缺失证据和修复方案 |
| **Revise** | 修改已经写好的正文 | 先给干净替换文本；说明与正文分离 |
| **Track** | 保存已确认的项目或投稿更新 | 当前状态、最近里程碑、下一步 |

```text
使用 $ocean 为组会解读这个 DOI。
使用 $ocean 的 Design 模式，把这一句话 idea 变成可行研究。
使用 $ocean 的 Audit 模式，检查这篇稿件的 claim 和验证。
使用 $ocean 的 Revise 模式，先返回可直接替换的干净正文。
使用 $ocean 的 Track 模式，记录这个已经确认的投稿更新。
```

不需要记住七个 module 名称。安装、提示词模板、输出深度、来源处理、
工具与 GitHub 安全规则见[中文详细使用指南](docs/usage-guide.zh-CN.md)；
也可以阅读 [English guide](docs/usage-guide.md)。

对于已经写完的稿件，**Revise** 会先返回可直接替换的干净正文，并将科学问题
或作者确认项放在正文之外。完整生命周期规则见
[中文使用指南](docs/usage-guide.zh-CN.md)。

## 模块流程

OCEAN 默认只选择最少且必要的模块，并隐藏模块名称。端到端对话工作流中，每个模块
都有文档化的产物与交接契约；只有已列出的控制层 CLI 命令和参考工作流会生成机器可读
artifact，模块名称本身不代表自动执行。更完整的说明见 `docs/module-map.md`。

| 顺序 | Module | 完成的事件 | 典型产物 |
|---:|---|---|---|
| 1 | **Sounding** | 证据发现和 source boundary 建立 | Source packet、Evidence Radar Map、Negative Space、Handoff Ticket |
| 2 | **Current** | 领域趋势和方向流动分析 | Trend map、近期流动、机会/风险说明 |
| 3 | **Reef** | 生物医学资源、临床数据、KG、数据库证据组织 | Resource provenance map、data-source routing、database/KG evidence table |
| 4 | **Iceberg** | 审核表面 claim 下面的证据支撑 | Claim-evidence matrix、降级/改写建议 |
| 5 | **Anchor** | 验证、复现、leakage、benchmark、reproducibility 规划 | Validation checklist、benchmark/leakage plan、复现风险 |
| 6 | **Compass** | 研究计划和策略决策 | Idea card、实验计划、期刊/合作策略 |
| 7 | **Harbor** | 报告沉淀和协作边界记忆 | Final report、decision note、贡献边界记录 |

## 可选的研究包红队

只有用户在 **Design** 或 **Audit** 中明确要求决策，并提供可追溯的 biomedical AI、
clinical prediction、database 或 knowledge-graph 研究包时，OCEAN 才可启用研究包红队。
它不是普通 Audit、Explore、Revise 或 Track 的默认路径。

研究包至少要能说明 study aim、核心 claim 或研究计划、data/cohort 边界、验证设计，
以及至少一个可追溯 SourcePacket 或 locator。否则 OCEAN 只能返回 **Cannot decide**
和最小补充材料。合格的审查可以给出最大证据瓶颈、研究有效性边界、最小补充验证包、
Go / Rework / Stop / Cannot decide、reviewer-risk ticket 与合作投入边界；它们只是有
边界的审查辅助，不是发表、临床、伦理或署名决定。

中文说明见 [`docs/research-red-team.zh-CN.md`](docs/research-red-team.zh-CN.md)，运行时规范见
[`skills/ocean/references/research-red-team.md`](skills/ocean/references/research-red-team.md)。

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
使用 $ocean 探索这个只有摘要的 claim。
先给简短 Decision Card，并说明目前不能得出什么结论。
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
使用 $ocean 的 Audit 模式评估上传的 manuscript。
请用中文输出，关注科学价值、可靠性、主要风险、缺失验证、
合作贡献边界和期刊定位。因为这是明确的多部分审计，请使用 Standard 输出。
```

如果只是修改已经完成的正文措辞：

```text
使用 $ocean 的 Manuscript Revision 模式。先返回可直接替换的干净正文；
审计说明和作者确认项不要写进正文。
```

浏览已覆盖的 bioinformatics 工具：

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py profile --tool last
```

数据库 adapter、workflow template、执行层和证据边界见
[中文工具总览](skills/ocean/scripts/README.zh-CN.md)。

## 输出原则

默认输出语言：中文。

普通首轮问题和范围较窄的问题默认先给简短 Decision Card：结论、依据、
目前不能判断、主要风险和下一步。只有明确要求或任务确实需要时才使用
Standard / Deep 审计。Manuscript Revision 先给干净替换正文；Track 只记录
已经确认的状态、最近里程碑和下一步。

所有模式都必须受证据边界约束。不要夸大 novelty 或 validity。始终区分：

- hypothesis vs evidence
- association vs causality
- database co-occurrence vs mechanism
- internal validation vs external validation
- system demonstration vs scientific discovery
- light advice vs authorship-level contribution

明确要求审计时，OCEAN 可以使用完整 claim-evidence contract。评分、期刊定位、
署名分析和七模块叙述，只有用户要求或确实有决策价值时才出现。

### 数据、代码与模型可用性

OCEAN 当前提供有证据边界的 availability-audit contract，以及一个拟议中的固定
14 维 Availability Evidence Card schema。已发布 CLI 只检查用户声明的 asset metadata
和未解决 placeholder；它**尚不能**从论文生成 14 维 card，也不会核验 repository、
identifier、license、FAIR 合规、可访问性或可复现性。URL、DOI、accession 和
repository name 在单独授权核验前始终只是 `not_verified` 候选；没有命中只表示
`not_explicitly_located`，不能写成“全文中不存在”。

公开工作流见
[`availability-audit.md`](skills/ocean/references/availability-audit.md)，
机器可读 schema 见
[`availability_evidence_card.schema.json`](skills/ocean/schemas/availability_evidence_card.schema.json)，
当前实现状态与后续评测 protocol 见
[`docs/availability-evidence-cards-v1.md`](docs/availability-evidence-cards-v1.md)。

## 项目示例

简洁的 [`projects/`](projects/README.md) 页面展示 OCEAN 在全麦发酵菌汤研究和
Delirium AI ICU 预测项目中的使用情况，只呈现已经确认的公开进度。

## 仓库导航

- [`skills/ocean/`](skills/ocean/)：可安装 skill、references、adapters 与工具 wrappers
- [`docs/`](docs/)：中英文使用指南与可执行证据控制层 CLI
- [`projects/`](projects/)：简洁的公开项目示例
- [`examples/`](examples/)：可复用的入门文件
- [`assets/`](assets/)：OCEAN 插图与图标

## License

MIT License。见 `LICENSE`。
