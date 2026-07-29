#!/usr/bin/env python3
"""Check or store local environment variables without exposing secret values."""

from __future__ import annotations

import argparse
import getpass
import json
import os
from pathlib import Path
import re
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import now_utc, read_json, write_json


NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,127}$")


def configured_names(config: Path) -> list[str]:
    payload = read_json(config)
    names = payload.get("credential_names", [])
    if not isinstance(names, list) or not all(isinstance(item, str) for item in names):
        raise SystemExit("credential_names must be a JSON list of strings")
    return names


def check_names(names: list[str]) -> dict:
    return {
        "schema_version": "ocean-credential-status-v1",
        "checked_at": now_utc(),
        "credentials": [
            {"name": name, "present": bool(os.environ.get(name))}
            for name in names
        ],
        "secret_values_exposed": False,
        "evidence_boundary": "Presence only; no credential value or API access was inspected."
    }


def upsert_env(path: Path, name: str, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    replacement = f"{name}={value}"
    updated: list[str] = []
    replaced = False
    for line in lines:
        if line.startswith(f"{name}="):
            if not replaced:
                updated.append(replacement)
                replaced = True
            continue
        updated.append(line)
    if not replaced:
        updated.append(replacement)
    path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


def command_check(args: argparse.Namespace) -> int:
    names = args.names or configured_names(args.config)
    payload = check_names(names)
    if args.output:
        write_json(args.output, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def command_set(args: argparse.Namespace) -> int:
    if not NAME_RE.fullmatch(args.name):
        raise SystemExit("Credential name must use uppercase letters, digits, and underscores")
    value = getpass.getpass(f"Enter {args.name} (input hidden): ")
    if not value:
        raise SystemExit("No value entered; file was not changed")
    upsert_env(args.env_file.expanduser(), args.name, value)
    print(
        json.dumps(
            {
                "name": args.name,
                "stored": True,
                "path": str(args.env_file.expanduser()),
                "permissions": "0600 requested",
                "secret_value_exposed": False
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safely check or store local credentials.")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check")
    check.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).with_name("credentials.example.json"),
    )
    check.add_argument("--names", nargs="*")
    check.add_argument("--output", type=Path)
    check.set_defaults(func=command_check)

    store = sub.add_parser("set")
    store.add_argument("--name", required=True)
    store.add_argument("--env-file", type=Path, required=True)
    store.set_defaults(func=command_set)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
