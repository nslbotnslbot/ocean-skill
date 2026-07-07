#!/usr/bin/env python3
"""Evaluate generated launcher/workflow runner wrappers."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


DEFAULT_PREFIX = "bioinformatics-launcher-runner-r1"
LAUNCHER_LAYERS = {"heavy_launcher_plan", "workflow_runtime", "source_packet_adapter"}
VALID_PROBE_STATUSES = {
    "executed",
    "not_available_current_environment",
    "found_but_probe_failed",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_text(text: str, limit: int = 2500) -> str:
    return text.replace("\r", "\n")[:limit]


def run_command(command: list[str], timeout: int) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        return proc.returncode, safe_text(proc.stdout or ""), safe_text(proc.stderr or "")
    except subprocess.TimeoutExpired as exc:
        return 124, safe_text(exc.stdout or ""), safe_text((exc.stderr or "") + "\nTIMEOUT")
    except OSError as exc:
        return 127, "", safe_text(str(exc))


def launcher_tools(skill_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for config_path in sorted((skill_dir / "scripts" / "tools" / "bioinformatics").glob("*/wrapper_config.json")):
        config = read_json(config_path)
        if config.get("execution_layer") in LAUNCHER_LAYERS:
            rows.append(config)
    return rows


def evaluate_plan(config: dict[str, Any], skill_dir: Path, artifacts_dir: Path, timeout: int) -> dict[str, Any]:
    slug = config["tool_slug"]
    folder = skill_dir / "scripts" / "tools" / "bioinformatics" / slug
    runner = folder / "scripts" / "run_launcher.py"
    output = artifacts_dir / f"{slug}-launcher-plan.json"
    command = [sys.executable, str(runner), "plan", "--output", str(output), "--timeout", str(timeout)]
    code, stdout, stderr = run_command(command, timeout + 8)
    payload = read_json(output) if output.exists() else {}
    boundary = str(payload.get("evidence_boundary", "")).lower()
    issues = []
    if not runner.exists():
        issues.append("missing_launcher_runner")
    if not payload:
        issues.append("missing_plan_artifact")
    if payload.get("execution_status") != "planned_not_executed":
        issues.append("plan_not_marked_planned_not_executed")
    if "not" not in boundary or ("executed" not in boundary and "scientific" not in boundary):
        issues.append("weak_plan_boundary")
    if not payload.get("required_run_evidence_before_packet"):
        issues.append("missing_required_run_evidence")
    if not payload.get("stop_conditions"):
        issues.append("missing_stop_conditions")
    if code != 0:
        issues.append("plan_runner_failed")
    return {
        "slug": slug,
        "name": config["tool_name"],
        "family": config["tool_family"],
        "execution_layer": config["execution_layer"],
        "mode": "launcher-plan",
        "returncode": code,
        "execution_status": payload.get("execution_status", ""),
        "artifact": str(output),
        "stdout_excerpt": stdout,
        "stderr_excerpt": stderr,
        "issues": issues,
        "verdict": "pass" if not issues else "needs_review",
    }


def evaluate_runtime_probe(config: dict[str, Any], skill_dir: Path, artifacts_dir: Path, timeout: int) -> dict[str, Any] | None:
    if config.get("execution_layer") != "workflow_runtime":
        return None
    slug = config["tool_slug"]
    folder = skill_dir / "scripts" / "tools" / "bioinformatics" / slug
    runner = folder / "scripts" / "run_launcher.py"
    output = artifacts_dir / f"{slug}-runtime-probe.json"
    packet_output = artifacts_dir / f"{slug}-runtime-probe-source-packet.json"
    command = [
        sys.executable,
        str(runner),
        "probe-runtime",
        "--output",
        str(output),
        "--packet-output",
        str(packet_output),
        "--timeout",
        str(timeout),
    ]
    code, stdout, stderr = run_command(command, timeout + 8)
    payload = read_json(output) if output.exists() else {}
    status = payload.get("execution_status", "")
    software_record = payload.get("software_record", {})
    boundary = str(payload.get("evidence_boundary", "")).lower()
    issues = []
    if not payload:
        issues.append("missing_runtime_probe_artifact")
    if status not in VALID_PROBE_STATUSES:
        issues.append("invalid_runtime_probe_status")
    if "not" not in boundary or ("biological" not in boundary and "analysis" not in boundary):
        issues.append("weak_runtime_probe_boundary")
    if code not in {0, 1}:
        issues.append("runtime_probe_crashed_or_timed_out")
    if software_record.get("tool_slug") != slug:
        issues.append("tool_slug_mismatch")
    if status == "executed" and not packet_output.exists():
        issues.append("missing_source_packet_for_executed_runtime_probe")
    return {
        "slug": slug,
        "name": config["tool_name"],
        "family": config["tool_family"],
        "execution_layer": config["execution_layer"],
        "mode": "runtime-probe",
        "returncode": code,
        "execution_status": status,
        "artifact": str(output),
        "stdout_excerpt": stdout,
        "stderr_excerpt": stderr,
        "issues": issues,
        "verdict": "pass" if not issues else "needs_review",
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_status: dict[str, int] = {}
    by_layer: dict[str, int] = {}
    by_mode: dict[str, int] = {}
    for row in rows:
        by_status[row["execution_status"]] = by_status.get(row["execution_status"], 0) + 1
        by_layer[row["execution_layer"]] = by_layer.get(row["execution_layer"], 0) + 1
        by_mode[row["mode"]] = by_mode.get(row["mode"], 0) + 1
    plan_rows = [row for row in rows if row["mode"] == "launcher-plan"]
    runtime_rows = [row for row in rows if row["mode"] == "runtime-probe"]
    return {
        "run_date": dt.date.today().isoformat(),
        "checks": len(rows),
        "launcher_tools_checked": len(plan_rows),
        "runtime_probes_checked": len(runtime_rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "by_execution_status": dict(sorted(by_status.items())),
        "by_execution_layer": dict(sorted(by_layer.items())),
        "by_mode": dict(sorted(by_mode.items())),
        "evidence_boundary": "Launcher/workflow runner eval only; launcher plans are non-executing and runtime probes do not run biological workflows.",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Launcher / Workflow Runner Eval R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Launcher tools checked: {summary['launcher_tools_checked']}",
        f"- Runtime probes checked: {summary['runtime_probes_checked']}",
        f"- Checks: {summary['checks']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        "",
        "## Execution Status Counts",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in summary["by_execution_status"].items():
        lines.append(f"| {status} | {count} |")
    lines.extend(
        [
            "",
            "## Results",
            "",
            "| Tool | Layer | Mode | Status | Verdict | Issues |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        issues = ", ".join(row["issues"])
        lines.append(
            f"| {row['name']} | {row['execution_layer']} | {row['mode']} | {row['execution_status']} | {row['verdict']} | {issues} |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "Launcher plans are non-executing records for heavy, GUI, GPU, licensed, source-packet-adapter, or workflow tools. Runtime probes only check whether a workflow runtime command is locally available. This eval does not install software, download references, run workflows, process biological data, benchmark methods, or validate scientific claims.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "slug",
        "name",
        "family",
        "execution_layer",
        "mode",
        "returncode",
        "execution_status",
        "verdict",
        "issues",
        "artifact",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: ("; ".join(row["issues"]) if field == "issues" else row.get(field, "")) for field in fields})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate launcher/workflow runner wrappers.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--timeout", type=int, default=6)
    args = parser.parse_args(argv)

    artifacts_dir = args.outdir / f"{args.prefix}-artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for config in launcher_tools(args.skill_dir):
        rows.append(evaluate_plan(config, args.skill_dir, artifacts_dir, args.timeout))
        runtime_probe = evaluate_runtime_probe(config, args.skill_dir, artifacts_dir, args.timeout)
        if runtime_probe is not None:
            rows.append(runtime_probe)
    summary = summarize(rows)
    write_json(args.outdir / f"{args.prefix}-results.json", rows)
    write_json(args.outdir / f"{args.prefix}-summary.json", summary)
    write_csv(args.outdir / f"{args.prefix}-scorecard.csv", rows)
    (args.outdir / f"{args.prefix}-results.md").write_text(make_markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
