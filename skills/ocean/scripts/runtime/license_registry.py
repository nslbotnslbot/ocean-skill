#!/usr/bin/env python3
"""Inspect resource notices and record local user acknowledgements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import now_utc, read_json, write_json


DEFAULT_REGISTRY = SCRIPT_ROOT.parent / "licenses" / "registry.yaml"


def load_registry(path: Path) -> dict:
    # The checked-in YAML files use JSON syntax, which is valid YAML and keeps
    # this installed skill dependency-free.
    return read_json(path)


def load_acknowledgements(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": "ocean-license-ack-v1", "acknowledgements": []}
    return read_json(path)


def command_list(args: argparse.Namespace) -> int:
    registry = load_registry(args.registry)
    print(json.dumps(registry, ensure_ascii=False, indent=2))
    return 0


def command_status(args: argparse.Namespace) -> int:
    registry = load_registry(args.registry)
    acknowledgements = load_acknowledgements(args.ack_file)
    acknowledged = {
        item["resource_id"]: item
        for item in acknowledgements.get("acknowledgements", [])
    }
    rows = []
    for resource in registry.get("resources", []):
        required = bool(resource.get("acknowledgement_required"))
        rows.append(
            {
                "resource_id": resource["resource_id"],
                "name": resource["name"],
                "acknowledgement_required": required,
                "acknowledged": resource["resource_id"] in acknowledged,
                "terms_url": resource.get("terms_url", ""),
            }
        )
    payload = {
        "schema_version": "ocean-license-status-v1",
        "checked_at": now_utc(),
        "resources": rows,
        "evidence_boundary": registry.get("evidence_boundary", ""),
    }
    if args.output:
        write_json(args.output, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def command_ack(args: argparse.Namespace) -> int:
    registry = load_registry(args.registry)
    resources = {
        item["resource_id"]: item for item in registry.get("resources", [])
    }
    if args.resource not in resources:
        raise SystemExit(f"Unknown resource: {args.resource}")
    payload = load_acknowledgements(args.ack_file)
    rows = [
        item
        for item in payload.get("acknowledgements", [])
        if item.get("resource_id") != args.resource
    ]
    rows.append(
        {
            "resource_id": args.resource,
            "acknowledged_at": now_utc(),
            "terms_url": resources[args.resource].get("terms_url", ""),
            "statement": "User confirmed that the current upstream notice was displayed.",
        }
    )
    payload["acknowledgements"] = rows
    payload["evidence_boundary"] = (
        "Acknowledgement is not legal advice, a license grant, or proof of compliance."
    )
    write_json(args.ack_file, payload)
    print(f"Recorded local acknowledgement for {args.resource}: {args.ack_file}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OCEAN resource notice registry.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    sub = parser.add_subparsers(dest="command", required=True)

    listing = sub.add_parser("list")
    listing.set_defaults(func=command_list)

    status = sub.add_parser("status")
    status.add_argument("--ack-file", type=Path, required=True)
    status.add_argument("--output", type=Path)
    status.set_defaults(func=command_status)

    ack = sub.add_parser("ack")
    ack.add_argument("--resource", required=True)
    ack.add_argument("--ack-file", type=Path, required=True)
    ack.set_defaults(func=command_ack)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
