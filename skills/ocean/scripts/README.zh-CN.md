# OCEAN 工具与脚本

[English version](README.md)

这个目录包含 OCEAN 的可执行辅助脚本、source-packet adapter、生物信息学工具
wrapper 和公共数据库 adapter。工具实现主要位于
[`tools/`](tools/README.md)。

## 正确理解工具状态

OCEAN 严格区分三种状态：

| 状态 | 含义 |
|---|---|
| **已覆盖（Covered）** | OCEAN 已有工具目录、路由元数据、示例和受约束的 wrapper contract |
| **当前可用（Available）** | 当前环境已经具备 executable、package、runtime、API、数据库、license 和计算资源 |
| **已经运行（Executed）** | 真实命令或查询已经执行，并检查了输入、参数、输出、日志、版本和环境 |

下面列出的工具表示 OCEAN **已经覆盖**，不代表当前机器一定已经安装或运行。
source packet 用来记录 provenance 和局限，不能单独验证生物学、因果、机制或
临床 claim。

## 当前包含的工具层

| 工具层 | 当前覆盖 | 主要位置 |
|---|---:|---|
| 生物信息学工具目录 | 115 | [`tools/bioinformatics/`](tools/bioinformatics/README.md) |
| 公共数据库 adapter | 13 | [`tools/databases/`](tools/databases/) |
| 文献 source adapter | 1 | [`tools/literature/`](tools/literature/) |
| ClinicalTrials.gov source adapter | 1 | [`tools/clinicaltrials/`](tools/clinicaltrials/) |
| 共享执行与 packet helper | 10+ | [`tools/common/`](tools/common/README.md) |
| 路由和 wrapper 管理脚本 | 仓库工具 | 当前目录和 [`tools/`](tools/README.md) |

## 公共数据库 adapter

这些是受约束的 Reef adapter。除非明确启用 live network execution，否则默认
只生成 dry-run 计划。

| Adapter | 主要用途 | 安全证据边界 |
|---|---|---|
| **UniProt** | 蛋白 accession、sequence 和 annotation provenance | annotation 不是新的功能或机制证据 |
| **PubMed** | PMID 和 citation metadata | metadata 或 abstract 不是全文证据 |
| **Europe PMC** | 文献和 preprint metadata | 检索到来源不等于完成 claim 验证 |
| **ChEMBL** | compound、assay、activity 和 target 记录 | database activity 不是治疗有效性 |
| **Open Targets** | target-disease association evidence | association score 不是因果或临床证据 |
| **STRING** | 蛋白关联网络证据 | 预测或聚合关联不是直接 binding 或 mechanism |
| **Reactome** | curated pathway membership | pathway annotation 不是特定研究情境中的通路激活 |
| **QuickGO** | Gene Ontology annotation | ontology annotation 不是研究情境中的实验确认 |
| **ClinVar** | variant assertion 和 review status | assertion 不能单独指导患者治疗 |
| **gnomAD** | population allele frequency | 人群频率不是 pathogenicity 或 clinical actionability |
| **AlphaFold DB** | predicted structure 和 confidence metadata | 预测不是 binding、function、mechanism 或 efficacy 证据 |
| **ClinicalTrials.gov** | trial registration、design 和 status | 注册记录不是 efficacy 或 safety 证据 |
| **NCBI E-utilities** | 受约束的 NCBI record retrieval | 下游使用前必须检查返回的 metadata |

每个 adapter 文件夹包含：

- `tool.json`：scope 和 evidence boundary；
- `api.json`：稳定的命令 contract；
- `examples/query.example.json`：示例输入；
- `scripts/query_packet.py`：dry-run 或受约束的 live entry point。

示例：

```bash
cd skills/ocean/scripts/tools/databases/uniprot

python3 scripts/query_packet.py \
  --accession P04637 \
  --out outputs/uniprot-reef-packet.json
```

只有适合访问公开网络时才添加 `--execute`。把结果作为 Reef evidence 之前，
必须检查生成的 packet。

## 文献与 registry source adapter

| Adapter | 作用 | 重要局限 |
|---|---|---|
| [`tools/literature/`](tools/literature/) | 把 PubMed、Europe PMC、DOI/PMID、abstract 或本地文献记录变成 source packet | title/abstract packet 仍然只是标题或摘要级证据 |
| [`tools/clinicaltrials/`](tools/clinicaltrials/) | 把 ClinicalTrials.gov 记录变成 registry packet | registry design/status 不能证明有效性或安全性 |
| [`tools/bioinformatics/alphafold_db/`](tools/bioinformatics/alphafold_db/) | 检查 AlphaFold DB 风格的 metadata、PAE、mmCIF 和 pLDDT | 结构置信度不能证明生物学功能 |

## 按科学任务划分的生物信息学工具

全部 115 个工具目录都包含 `tool.json`、`api.json`、wrapper configuration、
example run record、usage reference，以及受约束的 probe/plan 或 runner
entry point。

| 科学任务 | 数量 | 已覆盖工具 |
|---|---:|---|
| 序列比对 | 5 | BLAST、Bowtie2、BWA、LAST、minimap2 |
| Alignment 文件处理 | 4 | bcftools、BEDTools、HTSlib、SAMtools |
| 剪接 RNA 比对 | 2 | HISAT2、STAR |
| 质控与预处理 | 8 | cutadapt、fastp、FastQC、MultiQC、Picard、Qualimap、Trim Galore、Trimmomatic |
| RNA-seq 定量 | 5 | featureCounts、kallisto、RSEM、Salmon、StringTie |
| 差异表达 | 4 | DESeq2、edgeR、limma-voom、sleuth |
| 单细胞分析 | 8 | Alevin-fry、Azimuth、Cell Ranger、CellTypist、Scanpy、scVI、Seurat、STARsolo |
| 空间转录组 | 7 | cell2location、Giotto、Space Ranger、Squidpy、Stereoscope、stLearn、Tangram |
| 表观组与 motif/peak 分析 | 6 | deepTools、FIMO、HOMER、MACS2、MACS3、MEME |
| 变异检测 | 5 | DeepVariant、FreeBayes、GATK、Mutect2、Strelka2 |
| 基因组组装与注释 | 12 | Bakta、BUSCO、Canu、CheckM、eggNOG-mapper、Flye、InterProScan、MEGAHIT、Prokka、QUAST、Raven、SPAdes |
| 微生物组与宏基因组 | 6 | Bracken、DADA2、HUMAnN、Kraken2、MetaPhlAn、QIIME2 |
| 系统发育与比较基因组 | 7 | Clustal Omega、FastTree、IQ-TREE、MAFFT、MUSCLE、OrthoFinder、RAxML |
| 蛋白结构与建模 | 9 | AlphaFold、AlphaFold DB、ChimeraX、ColabFold、HH-suite、HMMER、MODELLER、PyMOL、RoseTTAFold |
| 蛋白组与代谢组 | 7 | DIA-NN、FragPipe、MaxQuant、MS-DIAL、MZmine、Skyline、XCMS |
| 多组学整合 | 5 | DIABLO、mixOmics、MOFA、MOFA+、WGCNA |
| 医学影像与 signal ML | 6 | ITK-SNAP、MONAI、nnU-Net、SimpleITK、3D Slicer、TorchIO |
| Workflow 与可复现性 | 9 | Conda、CWL、Docker、Galaxy、Nextflow、nf-core、Singularity-Apptainer、Snakemake、WDL-Cromwell |

## 执行层

OCEAN 将覆盖的生物信息学工具路由到六种受约束的执行层：

| 执行层 | 工具数 | Wrapper 能做什么 |
|---|---:|---|
| `lightweight_cli` | 60 | 探测本地 executable，或记录用户明确提供的命令 |
| `python_package` | 16 | 探测 Python import，或记录已经检查的 Python script run |
| `r_bioconductor` | 10 | 探测 R package，或记录已经检查的 R script run |
| `heavy_launcher_plan` | 20 | 生成不执行的计划，记录 compute、database、license 和 evidence requirements |
| `workflow_runtime` | 8 | 探测 workflow runtime，或记录用户明确提供的 workflow invocation |
| `source_packet_adapter` | 1 | 检查受约束的来源文件并创建 provenance packet |

这些数量描述 wrapper 路由，不代表本地安装状态。

## 共享 helper

[`tools/common/`](tools/common/README.md) 提供可复用的受约束执行层：

- `software_source_packet.py`：把已检查的软件运行 metadata 变成 packet；
- `cli_subprocess_wrapper.py`：本地 CLI probe 和明确命令 provenance；
- `python_package_wrapper.py`：Python package probe 和已检查 script record；
- `rscript_wrapper.py`：R/Bioconductor probe 和已检查 script record；
- `heavy_tool_launcher.py`：不执行的重型工具计划；
- `database_adapter_entrypoint.py`：通用 database adapter entry point；
- per-tool CLI、package、launcher、probe 和 status helper。

这些 helper 不会安装依赖、选择私有输入、下载 reference database，也不会判断
生物学结论是否成立。

## 路由与检查

路由一个生物医学来源问题：

```bash
python3 skills/ocean/scripts/ocean_source_router.py route \
  --question "哪些公开证据可以支持这个 target-disease claim？" \
  --output outputs/source-route.json
```

查看可用的生物信息学 workflow：

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  list-workflows \
  --output outputs/bioinformatics-workflows.json
```

列出全部已覆盖工具，或按名称/类别搜索：

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py list-tools

python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  list-tools \
  --search alignment
```

检查一个工具的路由 profile：

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  profile \
  --tool last
```

运行受约束的 availability check，或为重型工具生成不执行的计划：

```bash
python3 skills/ocean/scripts/tools/bioinformatics_tool_router.py \
  check \
  --tool last \
  --output outputs/last-check.json
```

对于 CLI 和 package 工具，`check` 检查当前环境；对于重型工具，只创建
plan，不启动任务。结果不能证明科学分析有效。

## OCEAN 应该怎样使用工具输出

1. 记录科学问题，以及为什么需要这个工具或数据库。
2. 在能够检查时记录确切版本、query、command、parameters、references、
   inputs、outputs、logs、environment 和 date。
3. 明确标记未检查或缺失的字段。
4. 把已检查的 run 或 response 转成受约束的 source packet。
5. 交给 Reef 组织 provenance。
6. 用 Iceberg 判断这个 packet 是否支持拟议 claim。
7. 需要检查 validation、leakage、benchmark fairness、replication 或
   reproducibility 时交给 Anchor。

绝不能把工具可用性、dry-run plan、database hit 或未检查的输出升级成科学验证。
