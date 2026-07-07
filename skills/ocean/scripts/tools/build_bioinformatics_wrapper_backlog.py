#!/usr/bin/env python3
"""Build an implementation backlog from OCEAN wrapper-readiness plans.

This script does not install or run bioinformatics tools. It converts readiness
plans into an ordered engineering backlog so wrapper work can proceed without
confusing planning artifacts with scientific validation.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import sys
from typing import Any

from build_bioinformatics_wrapper_readiness_plan import PRIORITY_SLUGS, render_command


DEFAULT_PREFIX = "bioinformatics-wrapper-implementation-backlog-r1"
DEFAULT_PLANS = "bioinformatics-wrapper-readiness-all-r1-results.json"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backlog_group(plan: dict[str, Any]) -> str:
    slug = plan["tool"]["slug"]
    stage = plan["readiness_stage"]
    interface = plan["interface_layer"]
    if stage == "stage_2_local_smoke_executed":
        return "immediate_local_packetization"
    if slug in PRIORITY_SLUGS:
        return "priority_environment_setup"
    if "lightweight_cli" in interface:
        return "common_cli_wrappers"
    if interface.startswith("r_") or interface.startswith("python_"):
        return "python_r_package_wrappers"
    if "workflow" in interface:
        return "workflow_reproducibility_plans"
    if "heavy" in interface or "container" in interface:
        return "heavy_tool_launcher_plans"
    return "general_source_packet_scaffolds"


def priority_rank(plan: dict[str, Any]) -> tuple[int, int, str, str]:
    group_rank = {
        "immediate_local_packetization": 0,
        "priority_environment_setup": 1,
        "common_cli_wrappers": 2,
        "python_r_package_wrappers": 3,
        "workflow_reproducibility_plans": 4,
        "heavy_tool_launcher_plans": 5,
        "general_source_packet_scaffolds": 6,
    }
    group = backlog_group(plan)
    return (
        group_rank[group],
        -int(plan.get("readiness_score_0_10", 0)),
        plan["tool"]["family"],
        plan["tool"]["slug"],
    )


def next_action(plan: dict[str, Any]) -> str:
    stage = plan["readiness_stage"]
    interface = plan["interface_layer"]
    if stage == "stage_2_local_smoke_executed":
        return "Collect an inspected run record or minimal fixture, then create a software source packet with the shared packet helper."
    if "lightweight_cli" in interface:
        return "Verify/install the CLI or container, run the bounded version/help probe, then capture logs and file manifests before any analysis."
    if interface.startswith("r_"):
        return "Verify Rscript and package version, then run only a bounded package check or tiny fixture with sessionInfo before packetization."
    if interface.startswith("python_"):
        return "Verify the Python import path and package version, then capture environment and tiny-fixture output before packetization."
    if "workflow" in interface:
        return "Create a dry-run/test-profile plan with workflow version, config, container/environment manifest, and input manifest."
    if "heavy" in interface or "container" in interface:
        return "Create a non-executing launcher plan first; require license, compute, reference/database, privacy, and log-export boundaries before execution."
    return "Inspect official documentation, verify the interface, and fill the run-record/source-packet contract before execution."


def make_row(plan: dict[str, Any], index: int) -> dict[str, Any]:
    command = plan.get("smoke_command") or []
    return {
        "rank": index,
        "group": backlog_group(plan),
        "slug": plan["tool"]["slug"],
        "name": plan["tool"]["name"],
        "family": plan["tool"]["family"],
        "stage": plan["readiness_stage"],
        "score": plan["readiness_score_0_10"],
        "interface_layer": plan["interface_layer"],
        "smoke_command": render_command(command) if command else "",
        "handoff": plan["handoff"],
        "next_action": next_action(plan),
        "evidence_boundary": "Engineering backlog only; not installation, execution, benchmark, or biological validation.",
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, int] = {}
    families: dict[str, int] = {}
    for row in rows:
        groups[row["group"]] = groups.get(row["group"], 0) + 1
        families[row["family"]] = families.get(row["family"], 0) + 1
    return {
        "run_date": dt.date.today().isoformat(),
        "items": len(rows),
        "groups": dict(sorted(groups.items())),
        "families": dict(sorted(families.items())),
        "top_group": rows[0]["group"] if rows else "",
        "evidence_boundary": "Backlog generated from readiness plans only; no external software execution or scientific validation.",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any], top_n: int) -> str:
    lines = [
        "# OCEAN Bioinformatics Wrapper Implementation Backlog R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Backlog items: {summary['items']}",
        f"- Evidence boundary: {summary['evidence_boundary']}",
        "",
        "## Group Counts",
        "",
        "| Group | Items |",
        "|---|---:|",
    ]
    for group, count in summary["groups"].items():
        lines.append(f"| {group} | {count} |")
    lines.extend(
        [
            "",
            f"## Top {min(top_n, len(rows))} Items",
            "",
            "| Rank | Group | Tool | Family | Stage | Interface | Next action |",
            "|---:|---|---|---|---|---|---|",
        ]
    )
    for row in rows[:top_n]:
        lines.append(
            f"| {row['rank']} | {row['group']} | {row['name']} | {row['family']} | {row['stage']} | {row['interface_layer']} | {row['next_action']} |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This backlog orders implementation work only. It does not prove that a tool is installed, callable, benchmarked, biologically valid, clinically useful, or publication-ready.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
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
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build OCEAN bioinformatics wrapper implementation backlog.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--plans", type=Path)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--top-n", type=int, default=30)
    args = parser.parse_args(argv)

    plans_path = args.plans or args.outdir / DEFAULT_PLANS
    plans = read_json(plans_path)
    rows = [make_row(plan, index) for index, plan in enumerate(sorted(plans, key=priority_rank), start=1)]
    summary = summarize(rows)

    write_json(args.outdir / f"{args.prefix}-results.json", rows)
    write_json(args.outdir / f"{args.prefix}-summary.json", summary)
    write_csv(args.outdir / f"{args.prefix}-scorecard.csv", rows)
    (args.outdir / f"{args.prefix}-results.md").write_text(
        make_markdown(rows, summary, args.top_n),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
