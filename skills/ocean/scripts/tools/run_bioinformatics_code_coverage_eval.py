#!/usr/bin/env python3
"""Check per-tool code coverage across all OCEAN bioinformatics tool folders."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
from typing import Any


DEFAULT_PREFIX = "bioinformatics-code-coverage-r1"
LAYER_REQUIREMENTS = {
    "lightweight_cli": {
        "runner": "scripts/run_cli.py",
        "api_commands": {"cli-probe", "cli-run-record"},
    },
    "python_package": {
        "runner": "scripts/run_package.py",
        "api_commands": {"package-probe", "package-run-record"},
    },
    "r_bioconductor": {
        "runner": "scripts/run_package.py",
        "api_commands": {"package-probe", "package-run-record"},
    },
    "heavy_launcher_plan": {
        "runner": "scripts/run_launcher.py",
        "api_commands": {"launcher-plan"},
    },
    "workflow_runtime": {
        "runner": "scripts/run_launcher.py",
        "api_commands": {"launcher-plan", "runtime-probe", "runtime-run-record"},
    },
    "source_packet_adapter": {
        "runner": "scripts/run_launcher.py",
        "api_commands": {"launcher-plan"},
    },
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_names(api: dict[str, Any]) -> set[str]:
    return {str(command.get("name")) for command in api.get("commands", [])}


def evaluate_tool(folder: Path) -> dict[str, Any]:
    config = read_json(folder / "wrapper_config.json") if (folder / "wrapper_config.json").exists() else {}
    api = read_json(folder / "api.json") if (folder / "api.json").exists() else {}
    layer = config.get("execution_layer", "")
    req = LAYER_REQUIREMENTS.get(layer, {})
    issues: list[str] = []
    required_files = [
        "README.md",
        "tool.json",
        "api.json",
        "wrapper_config.json",
        "examples/run-record.example.json",
        "references/tool_usage.md",
        "scripts/create_source_packet.py",
        "scripts/probe_or_plan.py",
    ]
    for relpath in required_files:
        if not (folder / relpath).exists():
            issues.append(f"missing:{relpath}")
    if layer not in LAYER_REQUIREMENTS:
        issues.append("unknown_execution_layer")
    runner = req.get("runner")
    if runner and not (folder / runner).exists():
        issues.append(f"missing_layer_runner:{runner}")
    names = command_names(api)
    for command in {"create-source-packet", "probe-or-plan"}:
        if command not in names:
            issues.append(f"missing_api_command:{command}")
    for command in req.get("api_commands", set()):
        if command not in names:
            issues.append(f"missing_api_command:{command}")
    return {
        "slug": folder.name,
        "tool_name": config.get("tool_name", ""),
        "execution_layer": layer,
        "layer_runner": runner or "",
        "api_commands": sorted(names),
        "issues": issues,
        "verdict": "pass" if not issues else "needs_review",
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_layer: dict[str, int] = {}
    for row in rows:
        by_layer[row["execution_layer"]] = by_layer.get(row["execution_layer"], 0) + 1
    return {
        "run_date": dt.date.today().isoformat(),
        "tools_checked": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "by_execution_layer": dict(sorted(by_layer.items())),
        "coverage_boundary": "Structural code-coverage check only; it does not execute biological workflows or validate scientific claims.",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Code Coverage Eval R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Tools checked: {summary['tools_checked']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        "",
        "## Execution Layer Counts",
        "",
        "| Layer | Count |",
        "|---|---:|",
    ]
    for layer, count in summary["by_execution_layer"].items():
        lines.append(f"| {layer} | {count} |")
    lines.extend(
        [
            "",
            "## Tool Results",
            "",
            "| Tool | Layer | Runner | Verdict | Issues |",
            "|---|---|---|---|---|",
        ]
    )
    for row in rows:
        issues = ", ".join(row["issues"])
        lines.append(
            f"| {row['slug']} | {row['execution_layer']} | `{row['layer_runner']}` | {row['verdict']} | {issues} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This eval checks whether each bioinformatics tool folder has the required code files, API commands, generic source-packet wrapper, per-tool probe/plan wrapper, and execution-layer-specific runner. It does not prove local tool installation, workflow execution, benchmark validity, or scientific claim support.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["slug", "tool_name", "execution_layer", "layer_runner", "verdict", "issues"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: ("; ".join(row["issues"]) if field == "issues" else row.get(field, "")) for field in fields})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check all bioinformatics tool code coverage.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    args = parser.parse_args(argv)

    bio_root = args.skill_dir / "scripts" / "tools" / "bioinformatics"
    rows = [evaluate_tool(folder) for folder in sorted(path for path in bio_root.iterdir() if path.is_dir())]
    summary = summarize(rows)
    write_json(args.outdir / f"{args.prefix}-results.json", rows)
    write_json(args.outdir / f"{args.prefix}-summary.json", summary)
    write_csv(args.outdir / f"{args.prefix}-scorecard.csv", rows)
    (args.outdir / f"{args.prefix}-results.md").write_text(make_markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
