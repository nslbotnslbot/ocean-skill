#!/usr/bin/env python3
"""Evaluate generated OCEAN database tool adapter folders."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def discover_tools(base_dir: Path) -> list[Path]:
    return sorted(path for path in base_dir.iterdir() if (path / "adapter_config.json").exists())


def validate_static_files(tool_dir: Path) -> tuple[bool, list[str]]:
    required = [
        "README.md",
        "api.json",
        "tool.json",
        "adapter_config.json",
        "examples/query.example.json",
        "scripts/query_packet.py",
    ]
    missing = [name for name in required if not (tool_dir / name).exists()]
    return not missing, missing


def evaluate_tool(tool_dir: Path, args: argparse.Namespace, artifact_dir: Path) -> dict[str, Any]:
    config = read_json(tool_dir / "adapter_config.json")
    out = artifact_dir / f"{config['slug']}-reef-packet.json"
    md = artifact_dir / f"{config['slug']}-reef-packet.md"
    static_ok, missing = validate_static_files(tool_dir)
    command = [
        sys.executable,
        str(tool_dir / "scripts" / "query_packet.py"),
        "--out",
        str(out),
        "--markdown-out",
        str(md),
        "--retmax",
        str(args.retmax),
        "--timeout",
        str(args.timeout),
    ]
    if args.execute_live:
        command.append("--execute")
    proc = subprocess.run(command, capture_output=True, text=True, check=False, timeout=args.subprocess_timeout)
    packet = read_json(out) if out.exists() else {}
    boundary = packet.get("evidence_boundary", {})
    query_log = packet.get("query_log", {})
    mode = "live" if args.execute_live else "dry-run"
    status = query_log.get("status", "")
    status_ok = status in {"executed", "error"} if args.execute_live else status == "dry-run"
    packet_ok = (
        packet.get("ocean_module") == "Reef"
        and packet.get("adapter") == config["adapter"]
        and bool(packet.get("query"))
        and all(key in boundary for key in ["can_support", "cannot_support", "privacy_or_access", "handoff"])
        and status_ok
    )
    notes = []
    if missing:
        notes.append("missing=" + ",".join(missing))
    if proc.returncode != 0:
        notes.append((proc.stderr or proc.stdout).strip().replace("\n", " ")[:200])
    if query_log.get("failure_or_limit"):
        notes.append(str(query_log["failure_or_limit"])[:200])
    verdict = "pass" if static_ok and proc.returncode == 0 and packet_ok else "needs_review"
    if args.execute_live and status == "error":
        verdict = "needs_review"
    return {
        "slug": config["slug"],
        "adapter": config["adapter"],
        "label": config["label"],
        "family": config["family"],
        "mode": mode,
        "static_ok": static_ok,
        "query_status": status,
        "records_inspected": query_log.get("records_inspected", 0),
        "packet_ok": packet_ok,
        "verdict": verdict,
        "artifact": str(out),
        "notes": " | ".join(note for note in notes if note),
    }


def markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Database Tool Adapter Eval",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Mode: {summary['mode']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        "",
        "| Adapter | Family | Status | Records | Verdict | Notes |",
        "|---|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['adapter']} | {row['family']} | {row['query_status']} | {row['records_inspected']} | {row['verdict']} | {row['notes'] or 'None'} |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary",
            "",
            "This eval checks database tool folder contracts and bounded Reef packet creation. Dry-run mode does not make network calls. Live mode is bounded and records API/network failures explicitly. Passing this eval does not validate biological mechanisms, clinical utility, therapeutic efficacy, diagnosis, or publication readiness.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["slug", "adapter", "label", "family", "mode", "static_ok", "query_status", "records_inspected", "packet_ok", "verdict", "artifact", "notes"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate database tool adapter folders.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--execute-live", action="store_true")
    parser.add_argument("--retmax", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--subprocess-timeout", type=int, default=45)
    parser.add_argument("--prefix", default="")
    args = parser.parse_args(argv)

    mode = "live" if args.execute_live else "dry-run"
    prefix = args.prefix or f"database-tool-adapter-r1-{mode}"
    base_dir = args.skill_dir / "scripts" / "tools" / "databases"
    artifact_dir = args.outdir / f"{prefix}-artifacts"
    rows = [evaluate_tool(tool_dir, args, artifact_dir) for tool_dir in discover_tools(base_dir)]
    summary = {
        "run_date": dt.date.today().isoformat(),
        "mode": mode,
        "cases": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "adapters": [row["adapter"] for row in rows],
        "boundary": "Database tool packet creation only; not scientific validation.",
    }
    write_json(args.outdir / f"{prefix}-results.json", rows)
    write_json(args.outdir / f"{prefix}-summary.json", summary)
    write_csv(args.outdir / f"{prefix}-scorecard.csv", rows)
    (args.outdir / f"{prefix}-results.md").write_text(markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
