# OCEAN 研究包红队

研究包红队是 **Design** 与 **Audit** 下的可选专项：只有用户明确要求对一个可追溯的
biomedical AI、clinical prediction、database 或 knowledge-graph 研究包进行
Go / Rework / Stop 式决策辅助或最小验证分诊时才启用。

它不取代五种 OCEAN 模式，也不适用于普通 Audit、Explore、Revise 或 Track。

## 它检查什么

在材料可追溯且足够完整时，审查可检查研究框架、核心 claim 或计划、data/cohort 边界、
train/validation/test 设计、来源 provenance、benchmark/comparator 公平性、外部验证、
calibration 或决策效用边界，以及 claim、figure 与可用分析之间的关系。

## 前提与结果

用户需要提供或授权检查：研究目标、核心 claim 或计划、data/cohort 信息、验证设计，
以及至少一个可追溯 source packet 或 locator。缺任何关键项时，OCEAN 只能返回
**Cannot decide** 与最小缺失输入；不得臆造致命缺陷或发表预测。

完整审查可以给出最大证据瓶颈、研究有效性边界、最小补充验证包、
Go / Rework / Stop / Cannot decide、reviewer-risk ticket 和协作输入边界。它们是受证据
约束的审查辅助，不是科学真伪证明，也不是发表、临床、伦理或署名决定。

对于文件化研究包，`scripts/ocean.py red-team-gate` 只检查请求范围、最低组成与定位信息，
不会给出 Go / Rework / Stop。完整文件化审查可再用
`scripts/ocean.py red-team-review-check` 检查每项固定结论是否回链到已声明的
source-packet locator，或显式标为未知并说明下一条所需输入；它不验证被引材料本身的科学内容。

这一路径目前没有对外发布的性能宣称。未来评测必须遵循
[`research-package-red-team-evaluation-protocol.md`](research-package-red-team-evaluation-protocol.md)
中的锁定公开案例、裁定与工件要求。

唯一运行时规范是
[`skills/ocean/references/research-red-team.md`](../skills/ocean/references/research-red-team.md)；
紧凑输出模板是
[`skills/ocean/references/research-red-team-template.md`](../skills/ocean/references/research-red-team-template.md)。
本页仅作中文说明，不与运行时定义竞争。
