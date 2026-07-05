#!/usr/bin/env python3
"""Create bounded launcher/run-plan records for heavy OCEAN tools.

Heavy tools can require licenses, GPUs, large reference databases, containers,
GUI sessions, or protected clinical data. This script records how a run should
be launched and what evidence is required, but it does not execute the tool.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from software_source_packet import DEFAULT_CANNOT_SUPPORT, write_json


def today() -> str:
    return dt.date.today().isoformat()


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def read_json_arg(value: str, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON argument: {exc}") from exc


def command_plan(args: argparse.Namespace) -> int:
    required_assets = read_json_arg(args.required_assets_json, [])
    stop_conditions = read_json_arg(args.stop_conditions_json, [])
    plan = {
        "schema_version": "ocean-heavy-tool-launcher-r1",
        "wrapper": "heavy_tool_launcher.py",
        "tool_name": args.tool_name,
        "tool_slug": args.tool_slug,
        "execution_status": "planned_not_executed",
        "run_mode": args.run_mode,
        "command_template": args.command_template,
        "container_or_environment": args.container_or_environment,
        "required_assets": required_assets,
        "license_or_terms_note": args.license_or_terms_note,
        "compute_note": args.compute_note,
        "data_safety_note": args.data_safety_note,
        "stop_conditions": stop_conditions
        or [
            "missing license or unavailable terms",
            "missing reference database/index",
            "missing GPU/HPC/container runtime",
            "private patient data or unpublished data without explicit local handling plan",
            "GUI-only workflow without exportable logs/run record",
        ],
        "required_run_evidence_before_packet": [
            "exact command or GUI action log",
            "tool version/build",
            "container/image or environment export",
            "reference database/index version and path",
            "input manifest",
            "output manifest",
            "logs/QC",
            "date and operator/context",
        ],
        "cannot_support": DEFAULT_CANNOT_SUPPORT
        + [
            "tool successfully ran",
            "result quality",
            "method benchmark superiority",
        ],
        "handoff": "Anchor",
        "created_at": now_iso(),
        "date": today(),
        "evidence_boundary": "Launcher plan only; this is not an executed software run or scientific result.",
    }
    write_json(args.output, plan)
    print(f"{args.tool_slug}: planned_not_executed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create non-executing launch plans for heavy tools.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("--tool-name", required=True)
    plan.add_argument("--tool-slug", required=True)
    plan.add_argument("--run-mode", default="launcher_plan")
    plan.add_argument("--command-template", required=True)
    plan.add_argument("--container-or-environment", default="to be supplied by user")
    plan.add_argument("--required-assets-json", default="[]")
    plan.add_argument("--license-or-terms-note", default="Check license, EULA, citation, and institutional terms before execution.")
    plan.add_argument("--compute-note", default="May require large references, GPU, HPC, or substantial local storage.")
    plan.add_argument("--data-safety-note", default="Do not submit PHI, patient data, or unpublished data to external services.")
    plan.add_argument("--stop-conditions-json", default="[]")
    plan.add_argument("--output", type=Path, required=True)
    plan.set_defaults(func=command_plan)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
