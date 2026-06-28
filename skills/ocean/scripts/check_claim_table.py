#!/usr/bin/env python3
"""Validate and summarize a scientific claim audit CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean

REQUIRED_COLUMNS = [
    "id",
    "claim",
    "claim_type",
    "evidence_source",
    "evidence_type",
    "directness_1_to_5",
    "causality_1_to_5",
    "support_1_to_5",
    "novelty_status",
    "validation_status",
    "missing_validation",
    "risk",
    "suggested_rewrite",
]

HIGH_RISK_KEYWORDS = [
    "causal",
    "causality",
    "overstatement",
    "leakage",
    "no external",
    "text mining",
    "database only",
    "unsupported",
    "circular",
    "association",
    "mechanism not validated",
]

def to_float(value: str) -> float | None:
    try:
        return float(str(value).strip())
    except Exception:
        return None

def score_issue(row_id: str, column: str, value: str) -> str | None:
    score = to_float(value)
    if score is None:
        return f"{row_id}: {column} is not numeric"
    if score < 1 or score > 5:
        return f"{row_id}: {column}={value} is outside 1-5"
    return None

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Claim audit CSV")
    parser.add_argument("--out", default="outputs/claim_table_summary.md", help="Output markdown summary")
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        rows = list(reader)

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    directness = [to_float(r["directness_1_to_5"]) for r in rows]
    causality = [to_float(r["causality_1_to_5"]) for r in rows]
    support = [to_float(r["support_1_to_5"]) for r in rows]
    directness = [x for x in directness if x is not None]
    causality = [x for x in causality if x is not None]
    support = [x for x in support if x is not None]

    high_risk_rows = []
    weak_rows = []
    score_issues = []
    for r in rows:
        row_id = r.get("id", "(missing id)") or "(missing id)"
        for column in ["directness_1_to_5", "causality_1_to_5", "support_1_to_5"]:
            issue = score_issue(row_id, column, r.get(column, ""))
            if issue:
                score_issues.append(issue)
        risk_text = " ".join([
            r.get("risk", ""),
            r.get("missing_validation", ""),
            r.get("evidence_type", ""),
        ]).lower()
        support_score = to_float(r.get("support_1_to_5", ""))
        causal_score = to_float(r.get("causality_1_to_5", ""))
        if any(k in risk_text for k in HIGH_RISK_KEYWORDS):
            high_risk_rows.append(r)
        if support_score is not None and support_score <= 2:
            weak_rows.append(r)
        if causal_score is not None and causal_score <= 2 and "mechanism" in r.get("claim_type", "").lower():
            if r not in high_risk_rows:
                high_risk_rows.append(r)

    def avg(xs: list[float]) -> str:
        return f"{mean(xs):.2f}" if xs else "NA"

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Claim Table Summary",
        "",
        f"- Total claims: {len(rows)}",
        f"- Mean directness: {avg(directness)} / 5",
        f"- Mean causality: {avg(causality)} / 5",
        f"- Mean support: {avg(support)} / 5",
        f"- High-risk claims: {len(high_risk_rows)}",
        f"- Weakly supported claims: {len(weak_rows)}",
        f"- Score issues: {len(score_issues)}",
        "",
        "## High-risk claims",
        "",
        "| ID | Claim | Risk | Suggested rewrite |",
        "|---|---|---|---|",
    ]
    for r in high_risk_rows:
        lines.append(
            f"| {r.get('id','')} | {r.get('claim','').replace('|','/')} | "
            f"{r.get('risk','').replace('|','/')} | {r.get('suggested_rewrite','').replace('|','/')} |"
        )
    lines.extend([
        "",
        "## Weakly supported claims",
        "",
        "| ID | Claim | Support | Missing validation |",
        "|---|---|---:|---|",
    ])
    for r in weak_rows:
        lines.append(
            f"| {r.get('id','')} | {r.get('claim','').replace('|','/')} | "
            f"{r.get('support_1_to_5','')} | {r.get('missing_validation','').replace('|','/')} |"
        )
    lines.extend([
        "",
        "## Score issues",
        "",
    ])
    if score_issues:
        lines.extend([f"- {issue}" for issue in score_issues])
    else:
        lines.append("- None")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
