#!/usr/bin/env python3
"""Execute generated per-tool bioinformatics probe/plan wrappers.

This eval invokes each `bioinformatics/<tool>/scripts/probe_or_plan.py` entrypoint
with a bounded output path. It checks that generated per-tool code is callable
and produces an evidence-bound artifact. It does not install tools, process
biological data, benchmark methods, or validate scientific claims.
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


DEFAULT_PREFIX = "bioinformatics-per-tool-wrapper-r1"
VALID_STATUSES = {
    "executed",
    "not_available_current_environment",
    "found_but_probe_failed",
    "planned_not_executed",
    "adapter_available",
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


def evaluate_tool(tool: dict[str, Any], skill_dir: Path, artifacts_dir: Path, timeout: int) -> dict[str, Any]:
    slug = tool["slug"]
    folder = skill_dir / "scripts" / "tools" / "bioinformatics" / slug
    wrapper = folder / "scripts" / "probe_or_plan.py"
    config = folder / "wrapper_config.json"
    output = artifacts_dir / f"{slug}-probe-or-plan.json"
    command = [
        sys.executable,
        str(wrapper),
        "--output",
        str(output),
        "--timeout",
        str(timeout),
    ]
    code, stdout, stderr = run_command(command, timeout + 8)
    artifact_exists = output.exists()
    payload = read_json(output) if artifact_exists else {}
    status = payload.get("execution_status", "")
    boundary = str(payload.get("evidence_boundary", "")).lower()
    issues = []
    if not wrapper.exists():
        issues.append("missing_probe_or_plan_wrapper")
    if not config.exists():
        issues.append("missing_wrapper_config")
    if not artifact_exists:
        issues.append("missing_output_artifact")
    if status not in VALID_STATUSES:
        issues.append("invalid_execution_status")
    if "not" not in boundary or ("biological" not in boundary and "scientific" not in boundary):
        issues.append("weak_evidence_boundary")
    if code not in {0, 1}:
        issues.append("wrapper_crashed_or_timed_out")
    return {
        "slug": slug,
        "name": tool["name"],
        "family": tool["family"],
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
        "evidence_boundary": "Per-tool wrapper entrypoint eval only; no installation, biological analysis, benchmark, or scientific validation.",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Per-Tool Wrapper Eval R1",
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
            "| Tool | Family | Status | Verdict | Issues |",
            "|---|---|---|---|---|",
        ]
    )
    for row in rows:
        issues = ", ".join(row["issues"])
        lines.append(f"| {row['name']} | {row['family']} | {row['execution_status']} | {row['verdict']} | {issues} |")
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval executes per-tool OCEAN wrapper entrypoints only. A status of `executed` means a bounded availability/version/import probe produced output, not that an analysis ran. A status of `planned_not_executed` means OCEAN created a launcher/source-packet plan. It does not install software, process data, benchmark tools, or validate scientific claims.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["slug", "name", "family", "returncode", "execution_status", "verdict", "issues", "artifact"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: ("; ".join(row["issues"]) if field == "issues" else row.get(field, "")) for field in fields})


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run generated OCEAN per-tool bioinformatics wrapper entrypoint eval.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--timeout", type=int, default=6)
    args = parser.parse_args(argv)

    registry = read_json(args.skill_dir / "scripts" / "tools" / "bioinformatics" / "registry.json")
    artifacts_dir = args.outdir / f"{args.prefix}-artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    rows = [evaluate_tool(tool, args.skill_dir, artifacts_dir, args.timeout) for tool in registry]
    summary = summarize(rows)

    write_json(args.outdir / f"{args.prefix}-results.json", rows)
    write_json(args.outdir / f"{args.prefix}-summary.json", summary)
    write_csv(args.outdir / f"{args.prefix}-scorecard.csv", rows)
    (args.outdir / f"{args.prefix}-results.md").write_text(make_markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
