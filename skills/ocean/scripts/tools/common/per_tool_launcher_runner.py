#!/usr/bin/env python3
"""Per-tool launcher/workflow runner bridge for OCEAN bioinformatics tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from cli_subprocess_wrapper import main as cli_main
from heavy_tool_launcher import main as launcher_main


LAUNCHER_LAYERS = {"heavy_launcher_plan", "workflow_runtime", "source_packet_adapter"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(tool_dir: Path) -> dict[str, Any]:
    config_path = tool_dir / "wrapper_config.json"
    if not config_path.exists():
        raise SystemExit(f"Missing wrapper_config.json in {tool_dir}")
    config = read_json(config_path)
    if config.get("execution_layer") not in LAUNCHER_LAYERS:
        raise SystemExit(
            f"{config.get('tool_slug', tool_dir.name)} is not configured as a launcher/workflow tool."
        )
    return config


def add_metadata_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task-intent", default="")
    parser.add_argument("--reference-or-index", default="not applicable for launcher/workflow probe")
    parser.add_argument("--parameters-json", default="{}")
    parser.add_argument("--input-files-json", default="[]")
    parser.add_argument("--output-files-json", default="[]")
    parser.add_argument("--logs-or-qc-json", default="[]")
    parser.add_argument("--environment", default="current local workflow/container/launcher environment")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path)


def common_cli_args(config: dict[str, Any], args: argparse.Namespace) -> list[str]:
    task_intent = args.task_intent or config.get("task_intent") or f"{config['tool_name']} workflow runtime probe"
    command = config.get("command") or []
    if not command:
        smoke = config.get("smoke_command") or []
        command = smoke[:1]
    if not command:
        raise SystemExit(f"{config['tool_slug']} has no workflow runtime command configured.")
    return [
        "--tool-name",
        config["tool_name"],
        "--tool-slug",
        config["tool_slug"],
        "--command",
        str(command[0]),
        "--task-intent",
        task_intent,
        "--reference-or-index",
        args.reference_or_index,
        "--parameters-json",
        args.parameters_json,
        "--input-files-json",
        args.input_files_json,
        "--output-files-json",
        args.output_files_json,
        "--logs-or-qc-json",
        args.logs_or_qc_json,
        "--environment",
        args.environment,
        "--timeout",
        str(args.timeout),
        "--output",
        str(args.output),
    ]


def maybe_packet_args(args: argparse.Namespace) -> list[str]:
    if args.packet_output is None:
        return []
    return ["--packet-output", str(args.packet_output)]


def launcher_required_assets(config: dict[str, Any]) -> list[str]:
    assets = []
    if config.get("minimal_fixture"):
        assets.append(f"minimal_fixture: {config['minimal_fixture']}")
    for item in config.get("expected_outputs", []):
        assets.append(f"expected_output: {item}")
    for item in config.get("required_run_evidence", []):
        assets.append(f"required_run_evidence: {item}")
    return assets


def command_plan(config: dict[str, Any], args: argparse.Namespace) -> int:
    run_mode = config.get("wrapper_mode") or config.get("execution_layer") or "launcher_plan"
    return launcher_main(
        [
            "plan",
            "--tool-name",
            config["tool_name"],
            "--tool-slug",
            config["tool_slug"],
            "--run-mode",
            run_mode,
            "--command-template",
            config.get("command_template") or f"{config.get('entrypoint', config['tool_slug'])} <user-supplied arguments>",
            "--container-or-environment",
            args.environment or config.get("environment_note", "to be supplied by user"),
            "--required-assets-json",
            json.dumps(launcher_required_assets(config), ensure_ascii=False),
            "--stop-conditions-json",
            json.dumps(config.get("stop_conditions", []), ensure_ascii=False),
            "--output",
            str(args.output),
        ]
    )


def command_probe_runtime(config: dict[str, Any], args: argparse.Namespace) -> int:
    if config.get("execution_layer") != "workflow_runtime":
        raise SystemExit("probe-runtime is only available for workflow_runtime tools.")
    probe_args = args.probe_args
    if not probe_args:
        probe_args = " ".join(str(item) for item in config.get("probe_args", []))
    argv = [
        "probe",
        *common_cli_args(config, args),
        *maybe_packet_args(args),
        f"--probe-args={probe_args}",
    ]
    return cli_main(argv)


def command_run_runtime(config: dict[str, Any], args: argparse.Namespace) -> int:
    if config.get("execution_layer") != "workflow_runtime":
        raise SystemExit("run-runtime is only available for workflow_runtime tools.")
    argv = [
        "run",
        *common_cli_args(config, args),
        *maybe_packet_args(args),
        "--args-json",
        args.args_json,
    ]
    return cli_main(argv)


def build_parser(config: dict[str, Any]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"Run bounded launcher/workflow wrapper for {config['tool_name']}."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Create a non-executing launcher/source-packet plan.")
    add_metadata_args(plan)
    plan.set_defaults(func=command_plan)

    probe = sub.add_parser("probe-runtime", help="Probe workflow runtime availability/version.")
    add_metadata_args(probe)
    probe.add_argument("--probe-args", default="")
    probe.set_defaults(func=command_probe_runtime)

    run = sub.add_parser("run-runtime", help="Run explicit user-supplied workflow-runtime arguments and record provenance.")
    add_metadata_args(run)
    run.add_argument("--args-json", required=True)
    run.set_defaults(func=command_run_runtime)
    return parser


def main_for_tool(tool_dir: Path, argv: list[str] | None = None) -> int:
    config = load_config(tool_dir.resolve())
    parser = build_parser(config)
    args = parser.parse_args(argv)
    return args.func(config, args)


if __name__ == "__main__":
    raise SystemExit(main_for_tool(Path.cwd()))
