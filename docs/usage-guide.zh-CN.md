# OCEAN 使用指南

[English guide](usage-guide.md)

OCEAN 是一个模型中立的生物医学科研工作流，用于处理 claim、evidence、
研究设计、稿件修改和简洁的项目记录。使用者不需要先学会七个内部模块。

最短的使用原则是：

> 告诉 OCEAN 你想完成什么，并提供你真正拥有的证据。

## 1. 60 秒安装

从 GitHub 安装 skill：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo nslbotnslbot/ocean-skill \
  --path skills/ocean \
  --ref main
```

打开一个新的 Codex 会话，让 skill 列表刷新，然后测试：

```text
使用 $ocean 探索这个研究想法：
微生物组来源的代谢物能否改善免疫治疗应答？
先给简短的 Decision Card，并说明目前不能得出什么结论。
```

如果只是临时安装测试，结束后可以删除：

```bash
rm -rf ~/.codex/skills/ocean
```

如果已经在本地 clone 了仓库：

```bash
cp -R skills/ocean ~/.codex/skills/
```

## 2. 可以给 OCEAN 什么

OCEAN 可以从以下任意材料开始：

- 一句话或很早期的研究 idea；
- 研究问题、假设或拟议 claim；
- DOI、PMID、URL、abstract、preprint 或 PDF；
- 一个 manuscript section 或完整稿件；
- proposal、protocol、analysis plan 或模型说明；
- figure、table、数据库记录或公开工具输出；
- reviewer 或 editor comments；
- 一个合作问题；
- 已经确认的项目或投稿状态更新。

输入材料越少，能够安全得出的结论就越窄。OCEAN 应该在证据边界内继续回答，
而不是补造缺失信息。

## 3. 选择目标，不必选择模块

OCEAN 对使用者提供五种模式：

| 模式 | 你想完成的事 | 默认结果 |
|---|---|---|
| **Explore** | 理解论文、idea、来源或领域 | 清楚解释，并说明证据边界 |
| **Design** | 把 idea 或缺口变成可行研究 | 研究路线、决定性对照、下一项实验 |
| **Audit** | 检查 claim、方法、验证或投稿准备度 | claim verdict、风险、缺失证据和修复方案 |
| **Revise** | 修改已经写好的正文 | 先给干净替换文本；说明与正文分离 |
| **Track** | 保存简洁项目或投稿记录 | Status、Progress、Next、Public Boundary |

OCEAN 会在内部选择最少且必要的模块，不会为了展示框架而每次运行全部七个模块。

可以明确指定模式：

```text
使用 $ocean 的 Design 模式……
```

也可以直接说任务：

```text
使用 $ocean 给组会讲清楚这篇论文。
```

测试安装是否成功，或明确要求使用这套工作流时，建议显式写出 `$ocean`。

## 4. 可以直接使用的提示词

### 解读一篇论文

```text
使用 $ocean 探索附件中的论文。
听众是研究生组会。
解释研究问题、设计、最强结果、主要局限，以及论文没有证明什么。
先给简短的 Decision Card。
```

### 梳理一个文献方向

```text
使用 $ocean 梳理这个问题附近的近期证据：
<研究问题>。
如果工具可用，可以检索公开来源。请区分已经检查的全文、
只有摘要的证据和尚未检查的候选来源。不要虚构引用。
```

### 从一句 idea 设计研究

```text
使用 $ocean 的 Design 模式处理这个想法：
<一句话 idea>。
请确定最高安全 claim、最小可行研究、决定性对照、独立验证、
最可能失败的环节，以及接下来的三个行动。
```

### 评估 proposal

```text
使用 $ocean 评估这个 proposal。
先给总体判断，然后只保留最可能改变可行性或科学价值的三个问题。
除非有助于比较方案，否则不要评分。
```

### 审计 manuscript 或模型

```text
使用 $ocean 的 Audit 模式审查附件中的稿件。
检查 claim 支撑、数据泄漏、benchmark 公平性、外部验证、
可复现性，以及是否把 association/prediction 夸大为 mechanism
或 clinical utility。使用 Standard 输出。
```

### 修改已经写好的正文

```text
使用 $ocean 的 Revise 模式。
先给可以直接替换的干净正文。审计结论、reviewer 语言和作者确认项
不要进入正文。不要虚构新的数据、方法、引用或结果。

正文：
<粘贴文本>
```

### 同时批判和修改，但不混在一起

```text
使用 $ocean 审核并修改这个 Discussion section。
分成三个独立区域输出：
1. 审计发现；
2. 干净修订正文；
3. 仅供作者决定的事项。
任何批判标签或编辑指令都不能写进修订正文。
```

### 处理 reviewer response

```text
使用 $ocean 处理这些 reviewer comments。
每一条都分开：
1. response letter 文本；
2. 修改后的 manuscript 文本；
3. 作者内部行动或缺失证据。
如果我没有提供完成证据，不要声称实验或分析已经完成。
```

### 记录项目状态

```text
使用 $ocean 的 Track 模式。
已确认状态：已经提交 medRxiv，正在等待平台筛查。
只更新 Status、Progress、Next 和 Public Boundary。
不要写成已经 posted、under review、accepted 或 published。
任何公开 GitHub 更新之前都要先询问我。
```

## 5. 输出深度

### Decision Card

普通首轮问题和范围较窄的问题默认使用：

1. 结论
2. 依据
3. 目前不能判断
4. 主要风险
5. 下一步

它会主动隐藏模块名、大表格、期刊档次和评分。

### Standard

明确要求多 claim 审计、结构化研究计划、合作分析或期刊定位时使用。
可能包括 evidence boundary、claim-evidence matrix、优先风险、缺失证据和
下一步行动。

### Deep

只有明确要求完整 manuscript review、模拟审稿人或详细报告时使用。
可以增加 reviewer concerns、安全 claim 改写和 decision memo。

### Revision

已经写完的正文使用独立格式：

1. 可以直接替换的干净正文；
2. 不进入正文的修改说明；
3. 仅在必要时出现的作者确认项。

## 6. 明确证据边界

处理高风险问题或不完整材料时，可以要求 OCEAN 明确写出：

- 已检查什么；
- 未检查什么；
- 不能得出什么结论；
- 下一步还需要哪个来源、文件、对照或分析。

可以直接这样写：

```text
只能把 abstract 当作摘要级证据。
除非已经检查到相应内容，不要推断完整方法、样本量、外部验证
或 clinical utility。
```

OCEAN 应该始终区分：

- hypothesis 和 evidence；
- association 和 causality；
- database co-occurrence 和 mechanism；
- model prediction 和 experimental validation；
- internal validation 和 external validation；
- technical performance 和 clinical utility；
- submission、posting、review、acceptance 和 publication。

## 7. 文件、来源和网络检索

为了得到更强的结果：

1. 附上相关 PDF、manuscript、figures、tables 或研究笔记。
2. 如果有 DOI、PMID、registry identifier 或官方 URL，请一并提供。
3. 说明是否允许或希望检索公开网络。
4. 说明只能检查已有材料，还是可以补充公开来源。
5. 标出保密、患者级、未公开或 embargoed 的材料。

搜索结果、标题、abstract、API response 或 database record 不会自动变成完整
科学证据。OCEAN 应记录来源 provenance，并停在已检查证据所能支持的最高
claim level。

## 8. 工具和 API

OCEAN 核心工作流不依赖特定模型，也不强制使用付费 API。数据库 adapter 和
生物信息学 wrapper 都是可选路线。

- wrapper 可以生成 dry-run query、provenance packet 或 launch plan。
- live call 可能需要公开 endpoint、API key、本地软件、数据库、license、
  reference index、计算资源，以及必要的用户授权。
- 存在工具文件夹不等于工具已经安装或可以运行。
- 只有真实运行并检查相关文件后，工具输出才可能成为 provenance 或分析证据。
- 不要把 API key 或私有 `.env` 文件提交到 GitHub。

在仓库根目录使用统一 bioinformatics router：

```bash
# 列出或搜索已覆盖工具。
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools --search rna

# 查看工具 profile，但不声称已经安装。
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py profile --tool deseq2

# 列出或生成受证据边界约束的 workflow plan。
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-workflows
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  workflow \
  --workflow rna-seq-differential-expression \
  --output outputs/rna-seq-plan.json

# 检查 CLI/package/runtime，或为重型工具创建不执行的 plan。
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  check \
  --tool deseq2 \
  --output outputs/deseq2-check.json
```

check 结果会明确写出工具已找到、未找到，或只是生成了 plan；它不会自动运行
完整的生物学分析。

## 9. 项目记录与 GitHub 安全

只有当工作已经变成真实、可追踪的项目时才使用 Track。公开页面保持四部分：

1. Status
2. Progress
3. Next
4. Public Boundary

不要公开原始数据、患者级信息、保密稿件、私有审稿报告、API key、未经确认的
投稿状态，或超过已检查证据的 claim。

OCEAN 可以先准备本地更新，但公开 push 到 GitHub 必须获得用户明确授权。

## 10. 常见问题

### 我需要记住七个模块吗？

不需要。五种模式是用户界面，七个模块提供科学工作流。只有当你希望检查
OCEAN 的工作路径时，才需要要求逐模块解释。

### OCEAN 可以从一句话开始吗？

可以。它应把结果标记为早期设计或受证据边界约束的 hypothesis，而不是
已经验证的结论。

### OCEAN 会不会每次都批判所有内容？

不会。Explore 负责解释，Design 负责设计，Audit 负责批判，Revise 负责干净
修改，Track 负责记录状态。普通润色请求不应该自动变成完整 reviewer report。

### OCEAN 能执行资源表里的全部生物信息工具吗？

不能直接这样理解。资源表中的覆盖意味着 OCEAN 能够路由或生成 source packet。
能否执行还取决于安装、runtime、数据库、license、计算资源和输入文件。规划分析前，
可以先用统一 router 的 `check` 命令检查当前环境。

### `$ocean` 没有被识别怎么办？

确认 `~/.codex/skills/ocean/SKILL.md` 存在，然后打开新的 Codex 会话。
如果文件夹不完整，从 `main` 重新安装。

### OCEAN 会提供临床建议吗？

不会。它可以评估生物医学证据和临床研究 claim，但不能替代医学判断，也不能
给出无证据的诊断或治疗建议。
