#!/usr/bin/env python3
"""Per-tool Python/R package runner bridge for OCEAN bioinformatics tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from python_package_wrapper import main as python_main
from rscript_wrapper import main as rscript_main


PACKAGE_LAYERS = {"python_package", "r_bioconductor"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_config(tool_dir: Path) -> dict[str, Any]:
    config_path = tool_dir / "wrapper_config.json"
    if not config_path.exists():
        raise SystemExit(f"Missing wrapper_config.json in {tool_dir}")
    config = read_json(config_path)
    if config.get("execution_layer") not in PACKAGE_LAYERS:
        raise SystemExit(
            f"{config.get('tool_slug', tool_dir.name)} is not configured as a Python/R package tool."
        )
    return config


def add_metadata_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task-intent", default="")
    parser.add_argument("--reference-or-index", default="not applicable for package probe")
    parser.add_argument("--parameters-json", default="{}")
    parser.add_argument("--input-files-json", default="[]")
    parser.add_argument("--output-files-json", default="[]")
    parser.add_argument("--logs-or-qc-json", default="[]")
    parser.add_argument("--environment", default="current local Python/R environment")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path)


def common_args(config: dict[str, Any], args: argparse.Namespace) -> list[str]:
    task_intent = args.task_intent or config.get("task_intent") or f"{config['tool_name']} package wrapper"
    return [
        "--tool-name",
        config["tool_name"],
        "--tool-slug",
        config["tool_slug"],
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


def packet_args(args: argparse.Namespace) -> list[str]:
    if args.packet_output is None:
        return []
    return ["--packet-output", str(args.packet_output)]


def command_probe(config: dict[str, Any], args: argparse.Namespace) -> int:
    if config.get("execution_layer") == "python_package":
        module = config.get("python_module") or config.get("entrypoint")
        return python_main(
            [
                "check-package",
                *common_args(config, args),
                *packet_args(args),
                "--module",
                str(module),
            ]
        )
    package = config.get("r_package") or config.get("entrypoint")
    return rscript_main(
        [
            "check-package",
            *common_args(config, args),
            *packet_args(args),
            "--package",
            str(package),
        ]
    )


def command_run_script(config: dict[str, Any], args: argparse.Namespace) -> int:
    if config.get("execution_layer") == "python_package":
        return python_main(
            [
                "run-script",
                *common_args(config, args),
                *packet_args(args),
                "--script",
                str(args.script),
                "--args-json",
                args.args_json,
            ]
        )
    return rscript_main(
        [
            "run-script",
            *common_args(config, args),
            *packet_args(args),
            "--script",
            str(args.script),
            "--args-json",
            args.args_json,
        ]
    )


def build_parser(config: dict[str, Any]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"Run bounded Python/R package wrapper for {config['tool_name']}."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    probe = sub.add_parser("probe", help="Run package availability/version probe.")
    add_metadata_args(probe)
    probe.set_defaults(func=command_probe)

    run = sub.add_parser("run-script", help="Run an explicit user-supplied script and record provenance.")
    add_metadata_args(run)
    run.add_argument("--script", type=Path, required=True)
    run.add_argument("--args-json", default="[]")
    run.set_defaults(func=command_run_script)
    return parser


def main_for_tool(tool_dir: Path, argv: list[str] | None = None) -> int:
    config = load_config(tool_dir.resolve())
    parser = build_parser(config)
    args = parser.parse_args(argv)
    return args.func(config, args)


if __name__ == "__main__":
    raise SystemExit(main_for_tool(Path.cwd()))
