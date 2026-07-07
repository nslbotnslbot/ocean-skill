#!/usr/bin/env python3
"""Validate OCEAN bioinformatics wrapper implementation backlog artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


DEFAULT_PREFIX = "bioinformatics-wrapper-implementation-backlog-r1"

REQUIRED_FIELDS = {
    "rank",
    "group",
    "slug",
    "name",
    "family",
    "stage",
    "score",
    "interface_layer",
    "smoke_command",
    "handoff",
    "next_action",
    "evidence_boundary",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_row(row: dict[str, Any], expected_rank: int) -> dict[str, Any]:
    missing = sorted(REQUIRED_FIELDS - set(row))
    boundary = str(row.get("evidence_boundary", "")).lower()
    next_action = str(row.get("next_action", ""))
    issues = []
    if missing:
        issues.append("missing_required_fields")
    if row.get("rank") != expected_rank:
        issues.append("rank_not_contiguous")
    if not row.get("slug") or not row.get("name"):
        issues.append("missing_tool_identity")
    if not row.get("group"):
        issues.append("missing_backlog_group")
    if not row.get("smoke_command"):
        issues.append("missing_smoke_command")
    if not next_action or len(next_action) < 40:
        issues.append("weak_next_action")
    if "not installation" not in boundary or "biological validation" not in boundary:
        issues.append("weak_evidence_boundary")
    return {
        "rank": row.get("rank"),
        "slug": row.get("slug", ""),
        "name": row.get("name", ""),
        "group": row.get("group", ""),
        "issues": issues,
        "verdict": "pass" if not issues else "needs_review",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Wrapper Backlog Eval R1",
        "",
        f"- Items checked: {summary['items_checked']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        "",
        "| Rank | Tool | Group | Verdict | Issues |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        issues = ", ".join(row["issues"])
        lines.append(f"| {row['rank']} | {row['name']} | {row['group']} | {row['verdict']} | {issues} |")
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval checks backlog artifact completeness only. It does not install software, execute tools, process data, benchmark wrappers, or validate scientific claims.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate OCEAN bioinformatics wrapper backlog artifacts.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--expected-items", type=int, default=115)
    args = parser.parse_args(argv)

    rows = read_json(args.outdir / f"{args.prefix}-results.json")
    checked = [check_row(row, index) for index, row in enumerate(rows, start=1)]
    duplicate_slugs = sorted({row["slug"] for row in checked if [item["slug"] for item in checked].count(row["slug"]) > 1})
    needs_review = sum(1 for row in checked if row["verdict"] != "pass")
    if len(rows) != args.expected_items:
        needs_review += 1
    if duplicate_slugs:
        needs_review += 1
    summary = {
        "items_checked": len(rows),
        "expected_items": args.expected_items,
        "pass": sum(1 for row in checked if row["verdict"] == "pass"),
        "needs_review": needs_review,
        "duplicate_slugs": duplicate_slugs,
        "evidence_boundary": "Backlog structure eval only; no software execution or scientific validation.",
    }
    write_json(args.outdir / f"{args.prefix}-eval-results.json", checked)
    write_json(args.outdir / f"{args.prefix}-eval-summary.json", summary)
    (args.outdir / f"{args.prefix}-eval-results.md").write_text(make_markdown(checked, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if needs_review == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
