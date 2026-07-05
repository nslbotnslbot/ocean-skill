#!/usr/bin/env python3
"""Run bounded Rscript probes or scripts for OCEAN R/Bioconductor tools."""

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


def make_record(
    *,
    args: argparse.Namespace,
    command: list[str],
    status: str,
    returncode: int | None,
    stdout: str,
    stderr: str,
    resolved_path: str,
) -> dict[str, Any]:
    return {
        "tool_name": args.tool_name,
        "tool_slug": args.tool_slug,
        "tool_version": stdout.splitlines()[0][:200] if status == "executed" and stdout.strip() else "",
        "task_intent": args.task_intent,
        "command_line": " ".join(shlex.quote(item) for item in command),
        "parameters": read_json_arg(args.parameters_json, {}),
        "reference_or_index": args.reference_or_index,
        "input_files": read_json_arg(args.input_files_json, []),
        "output_files": read_json_arg(args.output_files_json, []),
        "logs_or_qc": read_json_arg(args.logs_or_qc_json, []),
        "environment": args.environment,
        "date": today(),
        "supports_claims": [
            "R/Bioconductor package availability or bounded Rscript execution metadata"
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
        packet["filters"]["adapter"] = "scripts/tools/common/rscript_wrapper.py"
        packet["execution_status"] = payload["execution_status"]
        write_json(args.packet_output, packet)


def command_check_package(args: argparse.Namespace) -> int:
    rscript = shutil.which("Rscript")
    command = [rscript or "Rscript", "-e", f"cat(as.character(utils::packageVersion('{args.package}')))"]
    if not rscript:
        record = make_record(
            args=args,
            command=command,
            status="not_available_current_environment",
            returncode=None,
            stdout="",
            stderr="Rscript is not available on PATH.",
            resolved_path="",
        )
        emit_output(
            args,
            {
                "schema_version": "ocean-rscript-wrapper-r1",
                "wrapper": "rscript_wrapper.py",
                "mode": "check-package",
                "package": args.package,
                "execution_status": record["execution_status"],
                "software_record": record,
                "evidence_boundary": "Package availability evidence only; not an analysis.",
            },
        )
        print(f"{args.tool_slug}: Rscript unavailable")
        return 0

    code, stdout, stderr = run_bounded(command, args.timeout)
    status = "executed" if code == 0 and stdout.strip() else "not_available_current_environment"
    record = make_record(
        args=args,
        command=command,
        status=status,
        returncode=code,
        stdout=stdout,
        stderr=stderr,
        resolved_path=rscript,
    )
    emit_output(
        args,
        {
            "schema_version": "ocean-rscript-wrapper-r1",
            "wrapper": "rscript_wrapper.py",
            "mode": "check-package",
            "package": args.package,
            "execution_status": record["execution_status"],
            "software_record": record,
            "evidence_boundary": "Package availability evidence only; not an analysis.",
        },
    )
    print(f"{args.tool_slug}: {status}")
    return 0


def command_run_script(args: argparse.Namespace) -> int:
    rscript = shutil.which("Rscript")
    script = args.script.resolve()
    if not script.exists():
        raise SystemExit(f"R script does not exist: {script}")
    script_args = read_json_arg(args.args_json, [])
    if not isinstance(script_args, list) or not all(isinstance(item, str) for item in script_args):
        raise SystemExit("--args-json must be a JSON list of strings")
    command = [rscript or "Rscript", str(script), *script_args]
    if not rscript:
        record = make_record(
            args=args,
            command=command,
            status="not_available_current_environment",
            returncode=None,
            stdout="",
            stderr="Rscript is not available on PATH.",
            resolved_path="",
        )
        emit_output(
            args,
            {
                "schema_version": "ocean-rscript-wrapper-r1",
                "wrapper": "rscript_wrapper.py",
                "mode": "run-script",
                "execution_status": record["execution_status"],
                "software_record": record,
                "evidence_boundary": "R script did not run because Rscript is unavailable.",
            },
        )
        print(f"{args.tool_slug}: Rscript unavailable")
        return 2

    code, stdout, stderr = run_bounded(command, args.timeout)
    status = "executed" if code == 0 else "execution_failed"
    record = make_record(
        args=args,
        command=command,
        status=status,
        returncode=code,
        stdout=stdout,
        stderr=stderr,
        resolved_path=rscript,
    )
    emit_output(
        args,
        {
            "schema_version": "ocean-rscript-wrapper-r1",
            "wrapper": "rscript_wrapper.py",
            "mode": "run-script",
            "execution_status": record["execution_status"],
            "software_record": record,
            "evidence_boundary": "Rscript execution evidence only; downstream OCEAN audit is required.",
        },
    )
    print(f"{args.tool_slug}: {status}")
    return 0 if status == "executed" else 1


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tool-name", required=True)
    parser.add_argument("--tool-slug", required=True)
    parser.add_argument("--task-intent", default="R/Bioconductor availability/version smoke")
    parser.add_argument("--reference-or-index", default="not applicable for package version probe")
    parser.add_argument("--parameters-json", default="{}")
    parser.add_argument("--input-files-json", default="[]")
    parser.add_argument("--output-files-json", default="[]")
    parser.add_argument("--logs-or-qc-json", default="[]")
    parser.add_argument("--environment", default="current local Rscript environment")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run bounded Rscript wrappers for OCEAN.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check-package")
    add_common_arguments(check)
    check.add_argument("--package", required=True)
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
