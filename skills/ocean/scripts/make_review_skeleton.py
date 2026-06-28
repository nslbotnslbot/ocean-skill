#!/usr/bin/env python3
"""Create a markdown skeleton for a scientific project review."""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import date

TEMPLATE = """# OCEAN Standard Review Report

Date: {today}
Title: {title}
Project type: {project_type}

## 一、OCEAN审计卡

- Request mode:
- Evidence state:
- Work type: {project_type}
- Main verdict:
- Recommended action:

## 二、证据边界

- 已检查:
- 未检查:
- 不能判断:
- 需要补充:

## 三、核心claim-evidence矩阵

| ID | Claim | Claim type | Evidence inspected | Support verdict | Main gap | Risk | Safe rewrite |
|---|---|---|---|---|---|---|---|
| C1 |  |  |  |  |  |  |  |

## 四、最大风险

| Risk | Severity | Evidence basis | Why it matters | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## 五、需要补充的关键证据/分析

| Missing item | Why needed | Priority | Effort | Expected impact |
|---|---|---|---|---|
| External validation |  | High | Medium/High | High |
| Ablation study |  | High | Medium | High |
| Expert evaluation |  | Medium | Medium | Medium |
| Failure case analysis |  | High | Low/Medium | High |

## 六、我的合作切入点和贡献边界

| Level | Concrete tasks | Authorship value | Boundary warning |
|---|---|---|---|
| Light | reliability assessment, journal positioning | Low | advisory only |
| Medium | structure, result logic, figure design | Medium | clarify scope |
| Deep | reanalysis, benchmark, validation, writing | High | discuss authorship |
| Authorship-level | key analysis, validation, major writing | High | should be explicit |

## 七、投稿定位

- Best article type:
- Best direction:
- Stretch tier:
- Realistic tier:
- Backup tier:
- Not suitable for:
- Needed to move up one tier:
- Likely reviewer objections:

## 八、下一步怎么做

1.
2.
3.

## 九、0-10分评价

| Dimension | Score | Reason |
|---|---:|---|
| Scientific question clarity |  |  |
| Novelty |  |  |
| Methodological rigor |  |  |
| Data reliability |  |  |
| Validation strength |  |  |
| Benchmark fairness |  |  |
| Reproducibility |  |  |
| Domain insight |  |  |
| Publication readiness |  |  |
| User contribution potential |  |  |
"""

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True, help="Project or manuscript title")
    parser.add_argument("--project-type", default="unknown", help="Project/article type")
    parser.add_argument("--out", default="outputs/review_skeleton.md", help="Output markdown path")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        TEMPLATE.format(
            today=date.today().isoformat(),
            title=args.title,
            project_type=args.project_type,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
