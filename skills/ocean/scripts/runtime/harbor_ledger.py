#!/usr/bin/env python3
"""Maintain a checksum-linked Harbor decision and evidence ledger."""

from __future__ import annotations

import argparse
import json
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
    sha256_json,
    stable_id,
    write_json,
)


EVENT_TYPES = {
    "project_started",
    "source_added",
    "run_recorded",
    "decision_recorded",
    "claim_changed",
    "evidence_changed",
    "validation_requested",
    "validation_completed",
    "negative_result",
    "conflict_recorded",
    "handoff",
}


def base_ledger(project_id: str, title: str) -> dict:
    created_at = now_utc()
    return {
        "schema_version": "ocean-harbor-ledger-v1",
        "ledger_id": stable_id(
            "ledger",
            {"project_id": project_id, "title": title, "created_at": created_at},
        ),
        "project_id": project_id,
        "title": title,
        "created_at": created_at,
        "entries": [],
        "head_checksum": sha256_json([]),
        "evidence_boundary": evidence_boundary(
            inspected=["ledger structure and checksum chain"],
            not_inspected=["truth or scientific validity of entry contents"],
            cannot_conclude=[
                "that an event occurred solely because it was declared in the ledger"
            ],
            next_required=[
                "retain referenced SourcePackets, RunManifests, and human decisions"
            ],
        ),
    }


def entry_checksum(entry: dict) -> str:
    content = dict(entry)
    content.pop("entry_checksum", None)
    return sha256_json(content)


def validate_ledger(payload: dict) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != "ocean-harbor-ledger-v1":
        errors.append("unsupported schema_version")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        return errors + ["entries must be an array"]
    previous = sha256_json([])
    for index, entry in enumerate(entries):
        if entry.get("index") != index + 1:
            errors.append(f"entry {index + 1}: index mismatch")
        if entry.get("previous_entry_checksum") != previous:
            errors.append(f"entry {index + 1}: previous checksum mismatch")
        expected = entry_checksum(entry)
        if entry.get("entry_checksum") != expected:
            errors.append(f"entry {index + 1}: entry checksum mismatch")
        previous = expected
    if payload.get("head_checksum") != previous:
        errors.append("head_checksum mismatch")
    return errors


def append_entry(payload: dict, args: argparse.Namespace) -> dict:
    errors = validate_ledger(payload)
    if errors:
        raise SystemExit("Ledger validation failed before append: " + "; ".join(errors))
    boundary = parse_json_argument(
        args.evidence_boundary_json,
        dict,
        "--evidence-boundary-json",
    )
    for field in ("inspected", "not_inspected", "cannot_conclude", "next_required"):
        if field not in boundary or not isinstance(boundary[field], list):
            raise SystemExit(
                "--evidence-boundary-json must include list field: " + field
            )
    missing_references = [
        str(path)
        for path in [*args.source_packet, *args.run_manifest]
        if not path.is_file()
    ]
    if missing_references:
        raise SystemExit(
            "Refusing to append missing evidence references: "
            + ", ".join(missing_references)
        )
    entry = {
        "index": len(payload["entries"]) + 1,
        "event_id": stable_id(
            "event",
            {
                "ledger_id": payload["ledger_id"],
                "index": len(payload["entries"]) + 1,
                "event_type": args.event_type,
                "summary": args.summary,
            },
        ),
        "event_type": args.event_type,
        "created_at": now_utc(),
        "summary": args.summary,
        "source_packets": [file_record(path) for path in args.source_packet],
        "run_manifests": [file_record(path) for path in args.run_manifest],
        "decision": args.decision,
        "evidence_boundary": boundary,
        "previous_entry_checksum": payload["head_checksum"],
    }
    entry["entry_checksum"] = entry_checksum(entry)
    payload["entries"].append(entry)
    payload["head_checksum"] = entry["entry_checksum"]
    return payload


def command_init(args: argparse.Namespace) -> int:
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite existing ledger: {args.output}")
    payload = base_ledger(args.project_id, args.title)
    write_json(args.output, payload)
    print(
        json.dumps(
            {"ledger_id": payload["ledger_id"], "output": str(args.output)},
            indent=2,
        )
    )
    return 0


def command_append(args: argparse.Namespace) -> int:
    payload = append_entry(read_json(args.ledger), args)
    write_json(args.ledger, payload)
    print(
        json.dumps(
            {
                "ledger_id": payload["ledger_id"],
                "entries": len(payload["entries"]),
                "head_checksum": payload["head_checksum"],
            },
            indent=2,
        )
    )
    return 0


def command_validate(args: argparse.Namespace) -> int:
    errors = validate_ledger(read_json(args.ledger))
    print(
        json.dumps(
            {"valid": not errors, "errors": errors, "ledger": str(args.ledger)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Maintain a Harbor evidence ledger.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--project-id", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--output", type=Path, required=True)
    init.set_defaults(func=command_init)

    append = sub.add_parser("append")
    append.add_argument("--ledger", type=Path, required=True)
    append.add_argument("--event-type", choices=sorted(EVENT_TYPES), required=True)
    append.add_argument("--summary", required=True)
    append.add_argument("--source-packet", type=Path, action="append", default=[])
    append.add_argument("--run-manifest", type=Path, action="append", default=[])
    append.add_argument("--decision", default="")
    append.add_argument(
        "--evidence-boundary-json",
        required=True,
        help="JSON object with inspected/not_inspected/cannot_conclude/next_required arrays.",
    )
    append.set_defaults(func=command_append)

    validate = sub.add_parser("validate")
    validate.add_argument("--ledger", type=Path, required=True)
    validate.set_defaults(func=command_validate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
