#!/usr/bin/env python3
"""Dispatch per-tool OCEAN bioinformatics probe or launcher-plan wrappers.

This module is used by generated `bioinformatics/<tool>/scripts/probe_or_plan.py`
entrypoints. It records bounded availability evidence or launcher plans only.
It does not install tools, download references, process biological data,
benchmark methods, or validate scientific claims.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def shell_join(command: list[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in command)


def base_record(
    *,
    config: dict[str, Any],
    status: str,
    command_line: str,
    version: str = "",
    stdout: str = "",
    stderr: str = "",
    resolved_path: str = "",
    returncode: int | None = None,
) -> dict[str, Any]:
    return {
        "tool_name": config["tool_name"],
        "tool_slug": config["tool_slug"],
        "tool_version": version,
        "task_intent": config.get("task_intent", "bounded local availability probe"),
        "command_line": command_line,
        "parameters": {
            "wrapper_mode": config.get("wrapper_mode", ""),
            "interface_layer": config.get("execution_layer", ""),
        },
        "reference_or_index": "not applicable for availability probe or launcher plan",
        "input_files": [],
        "output_files": [],
        "logs_or_qc": [],
        "environment": config.get("environment_note", "current local environment"),
        "date": today(),
        "supports_claims": [
            "local availability or launcher-plan provenance only"
        ]
        if status in {"executed", "planned_not_executed", "adapter_available"}
        else [],
        "cannot_support": DEFAULT_CANNOT_SUPPORT,
        "boundary_status": "queried_evidence" if status == "executed" else "candidate_route",
        "handoff": config.get("handoff", "Anchor"),
        "execution_status": status,
        "returncode": returncode,
        "resolved_path": resolved_path,
        "stdout_excerpt": stdout,
        "stderr_excerpt": stderr,
        "created_at": now_iso(),
    }


def emit(args: argparse.Namespace, payload: dict[str, Any]) -> None:
    write_json(args.output, payload)
    record = payload.get("software_record")
    if args.packet_output and record and payload.get("execution_status") == "executed":
        packet = make_packet(record)
        packet["filters"]["adapter"] = "scripts/tools/common/per_tool_probe_or_plan.py"
        packet["execution_status"] = payload["execution_status"]
        write_json(args.packet_output, packet)


def cli_probe(config: dict[str, Any], args: argparse.Namespace) -> int:
    command = config.get("command") or config.get("smoke_command", [])[:1]
    probe_args = config.get("probe_args", [])
    if not command:
        command = [config.get("entrypoint", "")]
    executable = str(command[0])
    resolved = shutil.which(executable)
    full_command = [resolved or executable, *[str(item) for item in probe_args]]
    if not resolved:
        record = base_record(
            config=config,
            status="not_available_current_environment",
            command_line=shell_join(full_command),
            stderr=f"{executable} was not found on PATH.",
        )
        payload = {
            "schema_version": "ocean-per-tool-probe-r1",
            "wrapper": "per_tool_probe_or_plan.py",
            "mode": "cli_probe",
            "execution_status": record["execution_status"],
            "software_record": record,
            "candidate_install_routes": config.get("candidate_install_routes", []),
            "stop_conditions": config.get("stop_conditions", []),
            "evidence_boundary": "CLI availability probe only; not a biological analysis.",
        }
        emit(args, payload)
        print(f"{config['tool_slug']}: not_available_current_environment")
        return 0
    code, stdout, stderr = run_bounded(full_command, args.timeout)
    output = (stdout + "\n" + stderr).strip()
    status = "executed" if code in {0, 1, 2} and output else "found_but_probe_failed"
    version = output.splitlines()[0][:200] if status == "executed" and output else ""
    record = base_record(
        config=config,
        status=status,
        command_line=shell_join(full_command),
        version=version,
        stdout=stdout,
        stderr=stderr,
        resolved_path=resolved,
        returncode=code,
    )
    payload = {
        "schema_version": "ocean-per-tool-probe-r1",
        "wrapper": "per_tool_probe_or_plan.py",
        "mode": "cli_probe",
        "execution_status": status,
        "software_record": record,
        "candidate_install_routes": config.get("candidate_install_routes", []),
        "stop_conditions": config.get("stop_conditions", []),
        "evidence_boundary": "CLI availability/version probe only; not a biological analysis.",
    }
    emit(args, payload)
    print(f"{config['tool_slug']}: {status}")
    return 0 if status == "executed" else 1


def r_package_check(config: dict[str, Any], args: argparse.Namespace) -> int:
    package = config.get("r_package") or config.get("entrypoint")
    rscript = shutil.which("Rscript")
    command = [rscript or "Rscript", "-e", f"cat(as.character(utils::packageVersion('{package}')))"]
    if not rscript:
        record = base_record(
            config=config,
            status="not_available_current_environment",
            command_line=shell_join(command),
            stderr="Rscript is not available on PATH.",
        )
        payload = {
            "schema_version": "ocean-per-tool-probe-r1",
            "wrapper": "per_tool_probe_or_plan.py",
            "mode": "r_package_check",
            "execution_status": record["execution_status"],
            "software_record": record,
            "candidate_install_routes": config.get("candidate_install_routes", []),
            "stop_conditions": config.get("stop_conditions", []),
            "evidence_boundary": "R package availability probe only; not a biological analysis.",
        }
        emit(args, payload)
        print(f"{config['tool_slug']}: Rscript unavailable")
        return 0
    code, stdout, stderr = run_bounded(command, args.timeout)
    status = "executed" if code == 0 and stdout.strip() else "not_available_current_environment"
    record = base_record(
        config=config,
        status=status,
        command_line=shell_join(command),
        version=stdout.strip()[:200] if status == "executed" else "",
        stdout=stdout,
        stderr=stderr,
        resolved_path=rscript,
        returncode=code,
    )
    payload = {
        "schema_version": "ocean-per-tool-probe-r1",
        "wrapper": "per_tool_probe_or_plan.py",
        "mode": "r_package_check",
        "execution_status": status,
        "software_record": record,
        "candidate_install_routes": config.get("candidate_install_routes", []),
        "stop_conditions": config.get("stop_conditions", []),
        "evidence_boundary": "R package availability/version probe only; not a biological analysis.",
    }
    emit(args, payload)
    print(f"{config['tool_slug']}: {status}")
    return 0


def python_import_check(config: dict[str, Any], args: argparse.Namespace) -> int:
    module = config.get("python_module") or config.get("entrypoint")
    python_expr = f"import {module}; print(getattr({module}, '__version__', 'version_not_exposed'))"
    command_line = f"python3 -c {shlex.quote(python_expr)}"
    try:
        imported = importlib.import_module(str(module))
        version = str(getattr(imported, "__version__", "version_not_exposed"))
        status = "executed"
        stderr = ""
    except Exception as exc:  # noqa: BLE001 - bounded environment diagnostic
        version = ""
        status = "not_available_current_environment"
        stderr = safe_text(str(exc))
    record = base_record(
        config=config,
        status=status,
        command_line=command_line,
        version=version,
        stderr=stderr,
        resolved_path=sys.executable,
        returncode=0 if status == "executed" else 1,
    )
    payload = {
        "schema_version": "ocean-per-tool-probe-r1",
        "wrapper": "per_tool_probe_or_plan.py",
        "mode": "python_import_check",
        "execution_status": status,
        "software_record": record,
        "candidate_install_routes": config.get("candidate_install_routes", []),
        "stop_conditions": config.get("stop_conditions", []),
        "evidence_boundary": "Python package import/version probe only; not a biological analysis.",
    }
    emit(args, payload)
    print(f"{config['tool_slug']}: {status}")
    return 0


def launcher_plan(config: dict[str, Any], args: argparse.Namespace) -> int:
    record = base_record(
        config=config,
        status="planned_not_executed",
        command_line=config.get("command_template", ""),
    )
    payload = {
        "schema_version": "ocean-per-tool-launcher-plan-r1",
        "wrapper": "per_tool_probe_or_plan.py",
        "mode": config.get("wrapper_mode", "launcher_plan"),
        "execution_status": "planned_not_executed",
        "software_record": record,
        "tool_name": config["tool_name"],
        "tool_slug": config["tool_slug"],
        "command_template": config.get("command_template", ""),
        "candidate_install_routes": config.get("candidate_install_routes", []),
        "minimal_fixture": config.get("minimal_fixture", ""),
        "expected_outputs": config.get("expected_outputs", []),
        "required_run_evidence": config.get("required_run_evidence", []),
        "stop_conditions": config.get("stop_conditions", []),
        "handoff": config.get("handoff", "Anchor"),
        "evidence_boundary": "Launcher/source-packet plan only; not an executed software run or scientific result.",
    }
    emit(args, payload)
    print(f"{config['tool_slug']}: planned_not_executed")
    return 0


def dispatch(config: dict[str, Any], args: argparse.Namespace) -> int:
    mode = args.mode if args.mode != "auto" else config.get("wrapper_mode", "launcher_plan")
    if mode == "cli_probe":
        return cli_probe(config, args)
    if mode == "r_package_check":
        return r_package_check(config, args)
    if mode == "python_import_check":
        return python_import_check(config, args)
    if mode in {"heavy_launcher_plan", "workflow_launcher_plan", "source_packet_adapter_plan", "run_record_template"}:
        return launcher_plan(config, args)
    raise SystemExit(f"Unsupported wrapper mode: {mode}")


def main_for_tool(tool_dir: Path, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a bounded OCEAN per-tool probe or launcher plan.")
    parser.add_argument("--mode", choices=["auto", "cli_probe", "r_package_check", "python_import_check", "heavy_launcher_plan", "workflow_launcher_plan", "source_packet_adapter_plan", "run_record_template"], default="auto")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args(argv)

    config_path = tool_dir / "wrapper_config.json"
    if not config_path.exists():
        raise SystemExit(f"Missing wrapper config: {config_path}")
    config = read_json(config_path)
    return dispatch(config, args)
