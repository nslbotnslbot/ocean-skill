# OCEAN 证据控制层 CLI

[English version](evidence-control-plane.md)

OCEAN 的对话 skill 负责判断科研 claim 在现有证据下最多能安全地说到什么程度；
证据控制层 CLI 则把这个判断过程落实为可追踪的文件、工具运行、任务工作流和
长期项目记录。

它是控制层，不是科研结果生成器。命令成功只表示 OCEAN contract 被正确执行，
不代表生物学、临床、材料或工程结论已经成立。

## 核心 contract

| Contract | 用途 | 不能证明 |
|---|---|---|
| SourcePacket v2 | 保存来源身份、版本、checksum、locator、依赖和 claim 边界 | 来源内容真实或能够支持 claim |
| PaperBundle | 保存 page-grounded 或 structure-grounded 的正文、图表和 unresolved region | 图片型图表已被正确读取 |
| RunManifest | 保存命令、软件、输入、输出、环境和 checksum | 已经独立复现 |
| ValidationCard | 保存 claim 类型、所需证据、对照、pass criteria 和 stop condition | 验证已经完成 |
| Artifact Envelope | 为跨工具 artifact 提供 portable checksum 和 provenance | artifact 具有科学支持 |
| Harbor Ledger | 用 checksum 链保存项目事件、决定、失败和冲突 | 声明的事件一定真实发生 |

Schema 位于 [`skills/ocean/schemas/`](../skills/ocean/schemas/)。

## 环境

大多数控制层命令只使用 Python 标准库。PDF 提取可以选择使用 `pypdf` 或本地
`pdftotext`；开发检查使用 PyYAML。

```bash
uv sync --dev
python3 skills/ocean/scripts/ocean.py --help
```

如果没有 `uv`，请使用 Python 3.9 或更新版本，并按照 `pyproject.toml`
安装声明的依赖。

## 1. 检查环境

```bash
python3 skills/ocean/scripts/ocean.py doctor \
  --output outputs/ocean-doctor.json
```

Doctor 只报告 credential 环境变量和本地工具是否存在，不显示 secret 值，也不会
默认访问外部 API。

## 2. 建立有定位信息的来源

创建并验证 SourcePacket：

```bash
python3 skills/ocean/scripts/ocean.py source-packet create \
  --source-type primary_literature \
  --source-id YOUR_SOURCE_ID \
  --source-file path/to/source.pdf \
  --evidence-state inspected \
  --locator-mode page-grounded \
  --locators-json '[{"locator_id":"p1","locator_type":"page","value":"1"}]' \
  --output outputs/source-packet.json

python3 skills/ocean/scripts/ocean.py source-packet validate \
  --input outputs/source-packet.json
```

`queried_evidence` 必须有 checksum 和至少一个可以解析的 locator。如果内容没有
被检查，应保持为 `candidate` 或 `unavailable`。

准备论文：

```bash
python3 skills/ocean/scripts/ocean.py paper prepare \
  --input path/to/manuscript.pdf \
  --output outputs/paper-bundle.json
```

输出会说明 grounding 是 page-based、structure-based 还是 source-limited，
并保留提取失败或无法解析的区域。

## 3. 运行任务级工作流

目前包含三条 reference workflow：

```bash
python3 skills/ocean/scripts/ocean.py workflow variant \
  --input path/to/variant-task.json \
  --output outputs/variant-audit.json

python3 skills/ocean/scripts/ocean.py workflow target-disease \
  --input path/to/target-disease-task.json \
  --output outputs/target-disease-audit.json

python3 skills/ocean/scripts/ocean.py workflow manuscript \
  --input path/to/manuscript-task.json \
  --output outputs/manuscript-reliability.json
```

每条 workflow 都会同时写出 `.run-manifest.json`。缺失证据、部分独立来源、
循环验证、leakage 和 unresolved locator 会保留在结果中。Manuscript workflow
会把干净正文与 audit notes 分开。

## 4. 审核 claim 与研究设计

统一 CLI 提供以下 detector 和 audit：

```text
detect independence | circularity | leakage | claim-validation | diff
audit statistics-design | statistics-unit | statistics-multiplicity
audit statistics-figure | statistics-claim | data-availability
audit citation-link | citation-scope | citation-entailment | citation-metadata
```

查看具体命令的输入输出：

```bash
python3 skills/ocean/scripts/ocean.py audit statistics-unit --help
```

这些检查只基于已经提供的 metadata 与 locator，不会悄悄读取缺失全文、猜测
未报告的样本结构，也不会自动编写 accession 或 DOI。

## 5. 保存长期项目决定

建立并校验 checksum-linked Harbor ledger：

```bash
python3 skills/ocean/scripts/ocean.py ledger init \
  --project-id YOUR_PROJECT_ID \
  --title "Project title" \
  --output outputs/harbor-ledger.json

python3 skills/ocean/scripts/ocean.py ledger validate \
  --ledger outputs/harbor-ledger.json
```

每个新增事件必须包含 evidence boundary，也可以附加 SourcePacket 和 RunManifest
的 checksum。这样可以保留 negative result、冲突与决定变化，而不是把它们藏进
不透明的聊天总结。

使用 `detect diff` 比较新旧 evidence snapshot。证据发生变化只会触发人工复核，
不会自动升级或降级 claim。

## 6. 与其他工具互操作

Bridge 可以把 grounded reader artifact 转为 PaperBundle，把科学工具结果转为
SourcePacket + RunManifest，或把 artifact 包装为 portable envelope：

```bash
python3 skills/ocean/scripts/ocean.py bridge envelope \
  --input outputs/source-packet.json \
  --producer "your-tool" \
  --producer-version "1.0" \
  --access public \
  --license MIT \
  --output outputs/artifact-envelope.json
```

Envelope 保存身份和 provenance，但不会认证其中的科学结论。

## 7. 验证软件

仓库测试用于检查 schema、命令路由、证据边界和三个参考工作流：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

测试通过只表示已实现的软件 contract 按预期运行，不代表某项科学结论为真，
也不代表 OCEAN 优于某个模型、研究者或实验室流程。

## 公开仓库边界

公开仓库只保存稳定 schema、脚本、可合法再分发的测试 fixture、文档和简洁示例。
API key、private manuscript、patient-level data、raw model output、本地绝对路径、
内部审核材料和探索性日志都不应进入 GitHub。
