#!/usr/bin/env python3
"""Run bounded Python package probes or explicit scripts for OCEAN tools."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any

from software_source_packet import DEFAULT_CANNOT_SUPPORT, make_packet, write_json


def today() -> str:
    return dt.date.today().isoformat()


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def safe_text(text: str, limit: int = 4000) -> str:
    return text.replace("\r", "\n")[:limit]


def read_json_arg(value: str, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON argument: {exc}") from exc


def run_bounded(command: list[str], timeout: int) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        return proc.returncode, safe_text(proc.stdout or ""), safe_text(proc.stderr or "")
    except subprocess.TimeoutExpired as exc:
        return 124, safe_text(exc.stdout or ""), safe_text((exc.stderr or "") + "\nTIMEOUT")
    except OSError as exc:
        return 127, "", safe_text(str(exc))


def shell_join(command: list[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in command)


def make_record(
    *,
    args: argparse.Namespace,
    command: list[str],
    status: str,
    returncode: int | None,
    stdout: str,
    stderr: str,
) -> dict[str, Any]:
    return {
        "tool_name": args.tool_name,
        "tool_slug": args.tool_slug,
        "tool_version": stdout.splitlines()[0][:200] if status == "executed" and stdout.strip() else "",
        "task_intent": args.task_intent,
        "command_line": shell_join(command),
        "parameters": read_json_arg(args.parameters_json, {}),
        "reference_or_index": args.reference_or_index,
        "input_files": read_json_arg(args.input_files_json, []),
        "output_files": read_json_arg(args.output_files_json, []),
        "logs_or_qc": read_json_arg(args.logs_or_qc_json, []),
        "environment": args.environment,
        "date": today(),
        "supports_claims": [
            "Python package availability or bounded script execution metadata"
        ]
        if status == "executed"
        else [],
        "cannot_support": DEFAULT_CANNOT_SUPPORT,
        "boundary_status": "queried_evidence" if status == "executed" else "candidate_route",
        "handoff": "Anchor",
        "execution_status": status,
        "returncode": returncode,
        "resolved_path": sys.executable,
        "stdout_excerpt": stdout,
        "stderr_excerpt": stderr,
        "created_at": now_iso(),
    }


def emit_output(args: argparse.Namespace, payload: dict[str, Any]) -> None:
    write_json(args.output, payload)
    if getattr(args, "packet_output", None) and payload["execution_status"] == "executed":
        packet = make_packet(payload["software_record"])
        packet["filters"]["adapter"] = "scripts/tools/common/python_package_wrapper.py"
        packet["execution_status"] = payload["execution_status"]
        write_json(args.packet_output, packet)


def command_check_package(args: argparse.Namespace) -> int:
    probe_code = (
        "import importlib\n"
        f"mod = importlib.import_module({args.module!r})\n"
        "print(getattr(mod, '__version__', 'version_not_exposed'))\n"
    )
    command = [sys.executable, "-c", probe_code]
    code, stdout, stderr = run_bounded(command, args.timeout)
    status = "executed" if code == 0 and stdout.strip() else "not_available_current_environment"
    record = make_record(
        args=args,
        command=command,
        status=status,
        returncode=code,
        stdout=stdout,
        stderr=stderr,
    )
    payload = {
        "schema_version": "ocean-python-package-wrapper-r1",
        "wrapper": "python_package_wrapper.py",
        "mode": "check-package",
        "module": args.module,
        "execution_status": status,
        "software_record": record,
        "evidence_boundary": "Python package import/version probe only; not an analysis.",
    }
    emit_output(args, payload)
    print(f"{args.tool_slug}: {status}")
    return 0


def command_run_script(args: argparse.Namespace) -> int:
    script = args.script.resolve()
    if not script.exists():
        raise SystemExit(f"Python script does not exist: {script}")
    script_args = read_json_arg(args.args_json, [])
    if not isinstance(script_args, list) or not all(isinstance(item, str) for item in script_args):
        raise SystemExit("--args-json must be a JSON list of strings")
    command = [sys.executable, str(script), *script_args]
    code, stdout, stderr = run_bounded(command, args.timeout)
    status = "executed" if code == 0 else "execution_failed"
    record = make_record(
        args=args,
        command=command,
        status=status,
        returncode=code,
        stdout=stdout,
        stderr=stderr,
    )
    payload = {
        "schema_version": "ocean-python-package-wrapper-r1",
        "wrapper": "python_package_wrapper.py",
        "mode": "run-script",
        "execution_status": status,
        "software_record": record,
        "evidence_boundary": "Python script execution evidence only; downstream OCEAN audit is required.",
    }
    emit_output(args, payload)
    print(f"{args.tool_slug}: {status}")
    return 0 if status == "executed" else 1


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tool-name", required=True)
    parser.add_argument("--tool-slug", required=True)
    parser.add_argument("--task-intent", default="Python package availability/version smoke")
    parser.add_argument("--reference-or-index", default="not applicable for Python package import probe")
    parser.add_argument("--parameters-json", default="{}")
    parser.add_argument("--input-files-json", default="[]")
    parser.add_argument("--output-files-json", default="[]")
    parser.add_argument("--logs-or-qc-json", default="[]")
    parser.add_argument("--environment", default="current local Python environment")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run bounded Python package wrappers for OCEAN.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check-package")
    add_common_arguments(check)
    check.add_argument("--module", required=True)
    check.set_defaults(func=command_check_package)

    run = sub.add_parser("run-script")
    add_common_arguments(run)
    run.add_argument("--script", type=Path, required=True)
    run.add_argument("--args-json", default="[]")
    run.set_defaults(func=command_run_script)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
