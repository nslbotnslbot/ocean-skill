#!/usr/bin/env python3
"""Evaluate generated lightweight CLI runner wrappers.

The eval runs each `scripts/run_cli.py probe` entrypoint. It records whether the
tool is installed in the current environment, but does not process biological
data or benchmark tools.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


DEFAULT_PREFIX = "bioinformatics-cli-runner-r1"
VALID_STATUSES = {
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


def lightweight_tools(skill_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for config_path in sorted((skill_dir / "scripts" / "tools" / "bioinformatics").glob("*/wrapper_config.json")):
        config = read_json(config_path)
        if config.get("execution_layer") == "lightweight_cli":
            rows.append(config)
    return rows


def evaluate_tool(config: dict[str, Any], skill_dir: Path, artifacts_dir: Path, timeout: int) -> dict[str, Any]:
    slug = config["tool_slug"]
    folder = skill_dir / "scripts" / "tools" / "bioinformatics" / slug
    runner = folder / "scripts" / "run_cli.py"
    output = artifacts_dir / f"{slug}-cli-probe.json"
    packet_output = artifacts_dir / f"{slug}-cli-probe-source-packet.json"
    command = [
        sys.executable,
        str(runner),
        "probe",
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
    if not runner.exists():
        issues.append("missing_cli_runner")
    if status not in VALID_STATUSES:
        issues.append("invalid_execution_status")
    if not payload:
        issues.append("missing_output_artifact")
    if "not" not in boundary or ("biological" not in boundary and "analysis" not in boundary):
        issues.append("weak_evidence_boundary")
    if code not in {0, 1}:
        issues.append("runner_crashed_or_timed_out")
    if software_record.get("tool_slug") != slug:
        issues.append("tool_slug_mismatch")
    if status == "executed" and not packet_output.exists():
        issues.append("missing_source_packet_for_executed_probe")
    return {
        "slug": slug,
        "name": config["tool_name"],
        "family": config["tool_family"],
        "command": " ".join(config.get("command", [])),
        "returncode": code,
        "execution_status": status,
        "artifact": str(output),
        "source_packet": str(packet_output) if packet_output.exists() else "",
        "stdout_excerpt": stdout,
        "stderr_excerpt": stderr,
        "issues": issues,
        "verdict": "pass" if not issues else "needs_review",
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_status: dict[str, int] = {}
    by_family: dict[str, int] = {}
    for row in rows:
        by_status[row["execution_status"]] = by_status.get(row["execution_status"], 0) + 1
        by_family[row["family"]] = by_family.get(row["family"], 0) + 1
    return {
        "run_date": dt.date.today().isoformat(),
        "tools_checked": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "by_execution_status": dict(sorted(by_status.items())),
        "by_family": dict(sorted(by_family.items())),
        "evidence_boundary": "Lightweight CLI runner probe eval only; no installation, biological analysis, benchmark, or scientific validation.",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Lightweight CLI Runner Eval R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Tools checked: {summary['tools_checked']}",
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
            "## Tool Results",
            "",
            "| Tool | Command | Family | Status | Verdict | Issues |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        issues = ", ".join(row["issues"])
        lines.append(
            f"| {row['name']} | `{row['command']}` | {row['family']} | {row['execution_status']} | {row['verdict']} | {issues} |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval executes only bounded CLI probe entrypoints. An `executed` status means the local command produced probe output. It does not mean OCEAN processed biological data, selected valid parameters, completed a workflow, benchmarked a method, or validated any scientific claim.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["slug", "name", "family", "command", "returncode", "execution_status", "verdict", "issues", "artifact", "source_packet"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: ("; ".join(row["issues"]) if field == "issues" else row.get(field, "")) for field in fields})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate lightweight CLI runner wrappers.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--timeout", type=int, default=6)
    args = parser.parse_args(argv)

    artifacts_dir = args.outdir / f"{args.prefix}-artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    rows = [evaluate_tool(config, args.skill_dir, artifacts_dir, args.timeout) for config in lightweight_tools(args.skill_dir)]
    summary = summarize(rows)
    write_json(args.outdir / f"{args.prefix}-results.json", rows)
    write_json(args.outdir / f"{args.prefix}-summary.json", summary)
    write_csv(args.outdir / f"{args.prefix}-scorecard.csv", rows)
    (args.outdir / f"{args.prefix}-results.md").write_text(make_markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
