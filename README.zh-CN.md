# OCEAN: Orchestrated Claim-Evidence Analysis Navigator

[English README](README.md)

![OCEAN polar workflow infographic](assets/ocean-polar-workflow-logo-v4.png)

OCEAN 是一个轻量级、兼容 Codex 的 biomedical claim-evidence skill，用于医学研究与生物学研究。它可以支持生物医学 AI、生物学 AI、manuscript、数据库、知识图谱、临床预测、验证规划、期刊定位和协作边界分析。Domain Lens 和 Data/Tool Router 会为 medical、biological、omics、clinical、drug、KG/database、proposal 和 collaboration 任务选择合适的证据标准。

它的证据发现模块命名为 **Sounding**：这是一个 source-packet 工作流，用于扫描文献、证据边界和可追踪的 review 材料。

**表面简单，底层严谨；当工作成为项目时，过程可以追踪。**

[中文详细使用指南](docs/usage-guide.zh-CN.md) |
[证据控制层 CLI](docs/evidence-control-plane.zh-CN.md) |
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
| **Track** | 保存简洁项目或投稿状态 | Status、Progress、Next、Public Boundary |

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

OCEAN 默认只选择最少且必要的模块，并隐藏模块名称。需要端到端处理时，每个模块完成不同事件并交付具体产物。更完整的说明见 `docs/module-map.md`。

| 顺序 | Module | 完成的事件 | 典型产物 |
|---:|---|---|---|
| 1 | **Sounding** | 证据发现和 source boundary 建立 | Source packet、Evidence Radar Map、Negative Space、Handoff Ticket |
| 2 | **Current** | 领域趋势和方向流动分析 | Trend map、近期流动、机会/风险说明 |
| 3 | **Reef** | 生物医学资源、临床数据、KG、数据库证据组织 | Resource provenance map、data-source routing、database/KG evidence table |
| 4 | **Iceberg** | 审核表面 claim 下面的证据支撑 | Claim-evidence matrix、降级/改写建议 |
| 5 | **Anchor** | 验证、复现、leakage、benchmark、reproducibility 规划 | Validation checklist、benchmark/leakage plan、复现风险 |
| 6 | **Compass** | 研究计划和策略决策 | Idea card、实验计划、期刊/合作策略 |
| 7 | **Harbor** | 报告沉淀和协作边界记忆 | Final report、decision note、贡献边界记录 |

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
Standard / Deep 审计。Manuscript Revision 先给干净替换正文；Track 只保留
Status、Progress、Next 和 Public Boundary。

所有模式都必须受证据边界约束。不要夸大 novelty 或 validity。始终区分：

- hypothesis vs evidence
- association vs causality
- database co-occurrence vs mechanism
- internal validation vs external validation
- system demonstration vs scientific discovery
- light advice vs authorship-level contribution

明确要求审计时，OCEAN 可以使用完整 claim-evidence contract。评分、期刊定位、
署名分析和七模块叙述，只有用户要求或确实有决策价值时才出现。

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
