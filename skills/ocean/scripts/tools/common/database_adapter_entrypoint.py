#!/usr/bin/env python3
"""Shared entrypoint for OCEAN database adapter folders.

The per-database folders under scripts/tools/databases/ keep their own
configuration and examples, while this helper delegates bounded query-packet
creation to scripts/run_reef_api_adapter.py. It does not interpret API results
as scientific proof.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ARG_FLAGS = {
    "query": "--query",
    "database": "--database",
    "accession": "--accession",
    "identifier": "--identifier",
    "ensembl_id": "--ensembl-id",
    "variant_id": "--variant-id",
    "gnomad_dataset": "--gnomad-dataset",
    "species": "--species",
    "species_name": "--species-name",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_scripts_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "run_reef_api_adapter.py").exists():
            return parent
    raise RuntimeError("Could not find skills/ocean/scripts/run_reef_api_adapter.py")


def load_config(tool_dir: Path) -> dict[str, Any]:
    config_path = tool_dir / "adapter_config.json"
    if not config_path.exists():
        raise SystemExit(f"Missing adapter_config.json in {tool_dir}")
    return read_json(config_path)


def build_parser(config: dict[str, Any], tool_dir: Path) -> argparse.ArgumentParser:
    adapter = config["adapter"]
    parser = argparse.ArgumentParser(
        description=f"Create a bounded OCEAN Reef packet for {config['label']} ({adapter})."
    )
    parser.add_argument("--query")
    parser.add_argument("--database")
    parser.add_argument("--accession")
    parser.add_argument("--identifier")
    parser.add_argument("--ensembl-id", dest="ensembl_id")
    parser.add_argument("--variant-id", dest="variant_id")
    parser.add_argument("--gnomad-dataset", dest="gnomad_dataset")
    parser.add_argument("--species", type=int)
    parser.add_argument("--species-name", dest="species_name")
    parser.add_argument("--retmax", type=int)
    parser.add_argument("--timeout", type=int)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument(
        "--out",
        type=Path,
        default=tool_dir / "outputs" / f"{adapter.replace('-', '_')}-reef-packet.json",
    )
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument(
        "--no-example-defaults",
        action="store_true",
        help="Do not fill missing query arguments from adapter_config.json example defaults.",
    )
    return parser


def value_with_default(args: argparse.Namespace, defaults: dict[str, Any], key: str) -> Any:
    value = getattr(args, key)
    if value not in (None, ""):
        return value
    if args.no_example_defaults:
        return None
    return defaults.get(key)


def build_runner_command(
    scripts_root: Path,
    config: dict[str, Any],
    args: argparse.Namespace,
) -> list[str]:
    defaults = config.get("default_arguments", {})
    command = [
        sys.executable,
        str(scripts_root / "run_reef_api_adapter.py"),
        "--adapter",
        config["adapter"],
        "--retmax",
        str(args.retmax if args.retmax is not None else defaults.get("retmax", 2)),
        "--timeout",
        str(args.timeout if args.timeout is not None else defaults.get("timeout", 20)),
        "--out",
        str(args.out),
    ]
    if args.markdown_out is not None:
        command.extend(["--markdown-out", str(args.markdown_out)])
    if args.execute:
        command.append("--execute")
    for key, flag in ARG_FLAGS.items():
        value = value_with_default(args, defaults, key)
        if value not in (None, ""):
            command.extend([flag, str(value)])
    return command


def main_for_adapter(tool_dir: Path, argv: list[str] | None = None) -> int:
    tool_dir = tool_dir.resolve()
    config = load_config(tool_dir)
    scripts_root = find_scripts_root(tool_dir)
    parser = build_parser(config, tool_dir)
    args = parser.parse_args(argv)
    command = build_runner_command(scripts_root, config, args)
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main_for_adapter(Path.cwd()))
