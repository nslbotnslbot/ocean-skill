#!/usr/bin/env python3
"""Run bounded local CLI probes or commands for OCEAN tool wrappers.

This wrapper executes local commands only when the command is installed on PATH.
It never installs software, downloads reference databases, or treats a command
probe as scientific validation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from typing import Any

from probe_status import classify_probe_status
from software_source_packet import DEFAULT_CANNOT_SUPPORT, make_packet, write_json


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def today() -> str:
    return dt.date.today().isoformat()


def read_json_arg(value: str, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON argument: {exc}") from exc


def safe_text(text: str, limit: int = 4000) -> str:
    return text.replace("\r", "\n")[:limit]


def run_bounded(command: list[str], timeout: int) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        return proc.returncode, safe_text(proc.stdout or ""), safe_text(proc.stderr or "")
    except subprocess.TimeoutExpired as exc:
        stdout = safe_text(exc.stdout or "")
        stderr = safe_text((exc.stderr or "") + "\nTIMEOUT")
        return 124, stdout, stderr
    except OSError as exc:
        return 127, "", safe_text(str(exc))


def make_run_record(
    *,
    args: argparse.Namespace,
    command: list[str],
    status: str,
    returncode: int | None,
    stdout: str,
    stderr: str,
    resolved_path: str,
) -> dict[str, Any]:
    parameters = read_json_arg(getattr(args, "parameters_json", ""), {})
    if getattr(args, "probe_args", ""):
        parameters.setdefault("probe_args", args.probe_args)
    version_output = (stdout + "\n" + stderr).strip()
    return {
        "tool_name": args.tool_name,
        "tool_slug": args.tool_slug,
        "tool_version": version_output.splitlines()[0][:200] if status == "executed" and version_output else "",
        "task_intent": args.task_intent,
        "command_line": " ".join(shlex.quote(item) for item in command),
        "parameters": parameters,
        "reference_or_index": args.reference_or_index,
        "input_files": read_json_arg(getattr(args, "input_files_json", ""), []),
        "output_files": read_json_arg(getattr(args, "output_files_json", ""), []),
        "logs_or_qc": read_json_arg(getattr(args, "logs_or_qc_json", ""), []),
        "environment": args.environment,
        "date": today(),
        "supports_claims": [
            "local command availability and bounded execution metadata"
        ]
        if status == "executed"
        else [],
        "cannot_support": DEFAULT_CANNOT_SUPPORT,
        "boundary_status": "queried_evidence" if status == "executed" else "candidate_route",
        "handoff": "Anchor",
        "execution_status": status,
        "returncode": returncode,
        "resolved_path": resolved_path,
        "stdout_excerpt": stdout,
        "stderr_excerpt": stderr,
        "created_at": now_iso(),
    }


def emit_output(args: argparse.Namespace, payload: dict[str, Any]) -> None:
    write_json(args.output, payload)
    if getattr(args, "packet_output", None) and payload["execution_status"] == "executed":
        packet = make_packet(payload["software_record"])
        packet["filters"]["adapter"] = "scripts/tools/common/cli_subprocess_wrapper.py"
        packet["execution_status"] = payload["execution_status"]
        write_json(args.packet_output, packet)


def command_probe(args: argparse.Namespace) -> int:
    resolved = shutil.which(args.command)
    probe_args = shlex.split(args.probe_args)
    command = [resolved or args.command, *probe_args]
    if not resolved:
        record = make_run_record(
            args=args,
            command=command,
            status="not_available_current_environment",
            returncode=None,
            stdout="",
            stderr=f"{args.command} was not found on PATH.",
            resolved_path="",
        )
        emit_output(
            args,
            {
                "schema_version": "ocean-cli-wrapper-r1",
                "wrapper": "cli_subprocess_wrapper.py",
                "mode": "probe",
                "execution_status": record["execution_status"],
                "software_record": record,
                "evidence_boundary": "Availability/probe evidence only; not a biological analysis.",
            },
        )
        print(f"{args.tool_slug}: not available in current environment")
        return 0

    code, stdout, stderr = run_bounded(command, args.timeout)
    status = classify_probe_status(code, stdout, stderr)
    record = make_run_record(
        args=args,
        command=command,
        status=status,
        returncode=code,
        stdout=stdout,
        stderr=stderr,
        resolved_path=resolved,
    )
    emit_output(
        args,
        {
            "schema_version": "ocean-cli-wrapper-r1",
            "wrapper": "cli_subprocess_wrapper.py",
            "mode": "probe",
            "execution_status": record["execution_status"],
            "software_record": record,
            "evidence_boundary": "Availability/probe evidence only; not a biological analysis.",
        },
    )
    print(f"{args.tool_slug}: {status}")
    return 0 if status == "executed" else 1


def command_run(args: argparse.Namespace) -> int:
    resolved = shutil.which(args.command)
    run_args = read_json_arg(args.args_json, [])
    if not isinstance(run_args, list) or not all(isinstance(item, str) for item in run_args):
        raise SystemExit("--args-json must be a JSON list of strings")
    command = [resolved or args.command, *run_args]
    if not resolved:
        record = make_run_record(
            args=args,
            command=command,
            status="not_available_current_environment",
            returncode=None,
            stdout="",
            stderr=f"{args.command} was not found on PATH.",
            resolved_path="",
        )
        emit_output(
            args,
            {
                "schema_version": "ocean-cli-wrapper-r1",
                "wrapper": "cli_subprocess_wrapper.py",
                "mode": "run",
                "execution_status": record["execution_status"],
                "software_record": record,
                "evidence_boundary": "Command did not run because the executable is unavailable.",
            },
        )
        print(f"{args.tool_slug}: not available in current environment")
        return 2

    code, stdout, stderr = run_bounded(command, args.timeout)
    status = "executed" if code == 0 else "execution_failed"
    record = make_run_record(
        args=args,
        command=command,
        status=status,
        returncode=code,
        stdout=stdout,
        stderr=stderr,
        resolved_path=resolved,
    )
    emit_output(
        args,
        {
            "schema_version": "ocean-cli-wrapper-r1",
            "wrapper": "cli_subprocess_wrapper.py",
            "mode": "run",
            "execution_status": record["execution_status"],
            "software_record": record,
            "evidence_boundary": "Local command execution evidence only; downstream OCEAN audit is required.",
        },
    )
    print(f"{args.tool_slug}: {status}")
    return 0 if status == "executed" else 1


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tool-name", required=True)
    parser.add_argument("--tool-slug", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--task-intent", default="local software availability/version smoke")
    parser.add_argument("--reference-or-index", default="not applicable for version/help probe")
    parser.add_argument("--parameters-json", default="{}")
    parser.add_argument("--input-files-json", default="[]")
    parser.add_argument("--output-files-json", default="[]")
    parser.add_argument("--logs-or-qc-json", default="[]")
    parser.add_argument("--environment", default="current local PATH environment")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run bounded local CLI wrappers for OCEAN.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    probe = sub.add_parser("probe")
    add_common_arguments(probe)
    probe.add_argument("--probe-args", default="--version")
    probe.set_defaults(func=command_probe)

    run = sub.add_parser("run")
    add_common_arguments(run)
    run.add_argument("--args-json", required=True)
    run.set_defaults(func=command_run)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
