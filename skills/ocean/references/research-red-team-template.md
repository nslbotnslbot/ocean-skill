# Research Red-Team Audit Template

Use this template only after the entry conditions in
`research-red-team.md` are met. It is for explicit package-level
pre-submission review or minimum-validation triage of biomedical AI, clinical
prediction, database, or knowledge-graph projects. It is not the default for
ordinary Audit, Explore, Revise, or Track.

## 一、研究红队任务定义

- 输入类型：`<可追溯的 manuscript / proposal / project packet>`
- 目标域：`<medical AI / clinical prediction / KG / database>`
- 证据状态：`<sufficient / partial / minimal / non-traceable / contradictory>`
- 当前任务：`<Explore / Design / Audit / Revise / Track>`
- 入口门禁：`<ready_for_human_red_team / Cannot decide；缺失项>`
- 已检查的 SourcePacket / locator：`<packet ID 与定位信息>`
- 结论：`<Go / Rework / Stop / Cannot decide>`

若入口门禁不是 `ready_for_human_red_team`，不要填写下列完整审计表；仅输出
`Cannot decide`、已检查/未检查边界和最小补充材料。

## 二、固定审计对象检查（Research Package）

逐项判定是否可追溯、是否可复核：

1. study aim / problem framing
2. manuscript logic 与 claim-figure 一致性
3. dataset 与 cohort 定义
4. train/validation/test 划分
5. code 与运行环境可复现性
6. 数据库 / KG /资源来源与 provenance
7. benchmark 与 baseline 的可比性
8. 外部验证与泛化策略
9. 校准与决策效用边界
10. 过度结论风险（机制、临床价值、因果、出版定位）

## 三、完整红队输出（仅在入口门禁通过后）

### 1) Fatal Evidence Bottleneck

- 主体句：`<最致命证据短板>`
- 为什么致命：`<证据链断裂或可致命偏差来源>`
- 若不修复会如何失败：`<潜在审稿/复现风险>`

### 2) Study-validity verdict

- 当前结论可支持范围：`<可支持 / 边界支持 / 不支持 / 不能判断>`
- 最直接结论：`<一句话>`

### 3) Minimum Validation Package

| 条目 | 目标 | 最小补充动作 | 通过标准 | 估计成本 |
|---|---|---|---|---|
| `<缺口 1>` | `<验证目标>` | `<复用已有资源/新增最小实验>` | `<通过标准>` | `<高 / 中 / 低>` |

### 4) Go / Rework / Stop / Cannot decide

- 决策：`<Go / Rework / Stop / Cannot decide>`
- 决策理由：`<证据充分性与风险控制理由>`
- 结论边界：`<该决定不代表发表保证、临床可用、伦理批准或作者贡献结论>`

### 5) Reviewer-risk ticket

| Reviewer 视角风险 | 严重性 | 证据依据 | 缓解措施 |
|---|---:|---|---|
| `<泄漏/循环验证/外部验证缺失/...>` | `<1-5>` | `<当前证据边界>` | `<优先修正动作>` |

### 6) 合作与贡献边界

- 可直接承接任务：`<哪些工作可以明确推进>`
- 保守边界：`<不能作承诺的部分>`
- 需要用户/合作方确认：`<隐私、资源、临床伦理、版权、时间>`

## 四、最小下一步

1. `<最高优先修正>`
2. `<次优先修正>`
3. `<可否发布版本条件>`

## 五、文件化审计记录（可选）

若把完整审计保存为 JSON，使用
`schemas/research_red_team_review.schema.json`，并以
`scripts/ocean.py red-team-review-check` 检查。每一个固定结论都必须有：

- 已定位的 `packet_id + locator`；或
- `explicit_unknown` 与下一条必需输入。

该检查只验证回链结构，不能证明引用内容、科学有效性、发表可行性、临床价值、伦理或作者贡献。
