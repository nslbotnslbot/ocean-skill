#!/usr/bin/env python3
"""Per-tool CLI runner bridge for OCEAN bioinformatics tools.

Tool folders keep a tiny `scripts/run_cli.py` entrypoint. This shared helper
loads `wrapper_config.json` and delegates bounded probe/run-record behavior to
`cli_subprocess_wrapper.py`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from cli_subprocess_wrapper import main as cli_main


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(tool_dir: Path) -> dict[str, Any]:
    config_path = tool_dir / "wrapper_config.json"
    if not config_path.exists():
        raise SystemExit(f"Missing wrapper_config.json in {tool_dir}")
    config = read_json(config_path)
    if config.get("execution_layer") != "lightweight_cli":
        raise SystemExit(
            f"{config.get('tool_slug', tool_dir.name)} is not configured as a lightweight CLI tool."
        )
    command = config.get("command") or []
    if not command:
        raise SystemExit(f"{config.get('tool_slug', tool_dir.name)} has no CLI command configured.")
    return config


def json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def add_metadata_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task-intent", default="")
    parser.add_argument("--reference-or-index", default="not applicable for CLI probe")
    parser.add_argument("--parameters-json", default="{}")
    parser.add_argument("--input-files-json", default="[]")
    parser.add_argument("--output-files-json", default="[]")
    parser.add_argument("--logs-or-qc-json", default="[]")
    parser.add_argument("--environment", default="current local PATH environment")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path)


def common_cli_args(config: dict[str, Any], args: argparse.Namespace) -> list[str]:
    task_intent = args.task_intent or config.get("task_intent") or f"{config['tool_name']} bounded CLI wrapper"
    return [
        "--tool-name",
        config["tool_name"],
        "--tool-slug",
        config["tool_slug"],
        "--command",
        str(config["command"][0]),
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


def command_probe(config: dict[str, Any], args: argparse.Namespace) -> int:
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


def command_run(config: dict[str, Any], args: argparse.Namespace) -> int:
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
        description=f"Run bounded local CLI wrapper for {config['tool_name']}."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    probe = sub.add_parser("probe", help="Run only the configured availability/version/help probe.")
    add_metadata_args(probe)
    probe.add_argument("--probe-args", default="")
    probe.set_defaults(func=command_probe)

    run = sub.add_parser("run", help="Run a user-supplied local command argument list and record provenance.")
    add_metadata_args(run)
    run.add_argument(
        "--args-json",
        required=True,
        help="JSON list of command arguments. OCEAN never supplies private data paths automatically.",
    )
    run.set_defaults(func=command_run)
    return parser


def main_for_tool(tool_dir: Path, argv: list[str] | None = None) -> int:
    config = load_config(tool_dir.resolve())
    parser = build_parser(config)
    args = parser.parse_args(argv)
    return args.func(config, args)


if __name__ == "__main__":
    raise SystemExit(main_for_tool(Path.cwd()))
