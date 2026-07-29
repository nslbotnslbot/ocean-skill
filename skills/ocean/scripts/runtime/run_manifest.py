#!/usr/bin/env python3
"""Create or validate an OCEAN RunManifest."""

from __future__ import annotations

import argparse
import json
import os
import platform
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    evidence_boundary,
    file_record,
    now_utc,
    parse_json_argument,
    read_json,
    schema_path,
    stable_id,
    validate_required_contract,
    write_json,
)


def create_manifest(args: argparse.Namespace) -> dict:
    command = parse_json_argument(args.command_json, list, "--command-json")
    parameters = parse_json_argument(args.parameters_json, dict, "--parameters-json")
    inputs = [file_record(path) for path in args.input]
    outputs = [file_record(path) for path in args.expected_output]
    unresolved_inputs = [item["path"] for item in inputs if not item["exists"]]
    manifest_seed = {
        "task": args.task,
        "command": command,
        "created_at": now_utc(),
        "inputs": inputs,
    }
    return {
        "schema_version": "ocean-run-manifest-v1",
        "run_id": stable_id("run", manifest_seed),
        "task_intent": args.task,
        "created_at": manifest_seed["created_at"],
        "status": args.status,
        "command": command,
        "software": {"name": args.software, "version": args.software_version},
        "parameters": parameters,
        "inputs": inputs,
        "outputs": outputs,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "working_directory": os.getcwd(),
            "container": args.container,
            "environment_lock": args.environment_lock,
        },
        "logs": [str(path) for path in args.log],
        "evidence_boundary": evidence_boundary(
            inspected=["input file identity/checksum when files exist", "declared command and parameters"],
            not_inspected=["scientific correctness of outputs", "undeclared environment state"],
            cannot_conclude=[
                "reproducibility from a manifest alone",
                "biological or clinical validity from command success",
            ],
            next_required=(
                [f"provide missing input: {path}" for path in unresolved_inputs]
                or ["execute or independently rerun the declared workflow and inspect outputs"]
            ),
        ),
    }


def command_create(args: argparse.Namespace) -> int:
    payload = create_manifest(args)
    errors = validate_required_contract(
        payload,
        schema_path(__file__, "run_manifest.schema.json"),
    )
    if errors:
        raise SystemExit("RunManifest validation failed: " + "; ".join(errors))
    write_json(args.output, payload)
    print(json.dumps({"run_id": payload["run_id"], "status": payload["status"], "output": str(args.output)}, indent=2))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    payload = read_json(args.input)
    errors = validate_required_contract(
        payload,
        schema_path(__file__, "run_manifest.schema.json"),
    )
    result = {"valid": not errors, "errors": errors, "input": str(args.input)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create or validate an OCEAN RunManifest.")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--task", required=True)
    create.add_argument("--command-json", default="[]")
    create.add_argument("--software", default="unspecified")
    create.add_argument("--software-version", default="unknown")
    create.add_argument("--parameters-json", default="{}")
    create.add_argument("--input", type=Path, action="append", default=[])
    create.add_argument("--expected-output", type=Path, action="append", default=[])
    create.add_argument("--log", type=Path, action="append", default=[])
    create.add_argument(
        "--status",
        choices=["planned", "executed", "failed", "partial", "not_available"],
        default="planned",
    )
    create.add_argument("--container", default="")
    create.add_argument("--environment-lock", default="")
    create.add_argument("--output", type=Path, required=True)
    create.set_defaults(func=command_create)

    validate = sub.add_parser("validate")
    validate.add_argument("--input", type=Path, required=True)
    validate.set_defaults(func=command_validate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
