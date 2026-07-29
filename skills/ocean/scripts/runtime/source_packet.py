#!/usr/bin/env python3
"""Create or validate a versioned OCEAN SourcePacket."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    OCEAN_VERSION,
    evidence_boundary,
    now_utc,
    parse_json_argument,
    read_json,
    schema_path,
    sha256_file,
    stable_id,
    validate_required_contract,
    write_json,
)


def create_packet(args: argparse.Namespace) -> dict:
    locators = parse_json_argument(args.locators_json, list, "--locators-json")
    dependencies = parse_json_argument(
        args.dependencies_json,
        list,
        "--dependencies-json",
    )
    if args.source_file:
        if not args.source_file.is_file():
            raise SystemExit(f"Source file not found: {args.source_file}")
        checksum = sha256_file(args.source_file)
    else:
        checksum = args.checksum
    if not checksum:
        if args.evidence_state in {"inspected", "queried_evidence", "conflicting"}:
            raise SystemExit(
                "Inspected or queried evidence requires --source-file or --checksum"
            )
        checksum = "unverified:" + stable_id(
            "source",
            {"source_type": args.source_type, "source_id": args.source_id},
        )

    retrieved_at = args.retrieved_at or now_utc()
    source = {
        "source_type": args.source_type,
        "source_id": args.source_id,
        "title": args.title,
        "url": args.url,
        "version": args.source_version,
        "retrieved_at": retrieved_at,
        "checksum": checksum,
        "access_mode": args.access_mode,
    }
    packet_seed = {
        "source": source,
        "evidence_state": args.evidence_state,
        "locators": locators,
    }
    inspected = ["declared source identity, version, retrieval time, and checksum"]
    if locators:
        inspected.append("declared source locators")
    if args.source_file:
        inspected.append("local source-file bytes for checksum generation")
    cannot_conclude = [
        "that the source supports any claim beyond the declared support list",
        "scientific validity from source identity or retrieval alone",
    ]
    if args.evidence_state in {"candidate", "unavailable"}:
        cannot_conclude.append("source content because it was not declared as inspected")

    return {
        "schema_version": "ocean-source-packet-v2",
        "packet_id": stable_id("packet", packet_seed),
        "producer": {"name": "OCEAN SourcePacket builder", "version": OCEAN_VERSION},
        "source": source,
        "evidence_state": args.evidence_state,
        "locator_mode": args.locator_mode,
        "locators": locators,
        "supports_claims": args.supports_claim,
        "cannot_support": args.cannot_support,
        "upstream_dependencies": dependencies,
        "conflict_state": args.conflict_state,
        "recheck_policy": {
            "stale_after": args.stale_after,
            "recheck_trigger": args.recheck_trigger,
            "supersedes": args.supersedes,
        },
        "evidence_boundary": evidence_boundary(
            inspected=inspected,
            not_inspected=[
                "undeclared source content or upstream dependencies",
                "semantic entailment between the source and declared claims",
            ],
            cannot_conclude=cannot_conclude,
            next_required=(
                ["inspect source content and add resolvable locators"]
                if not locators
                else ["review claim-to-source entailment and evidence independence"]
            ),
        ),
    }


def validate_packet(payload: dict) -> list[str]:
    errors = validate_required_contract(
        payload,
        schema_path(__file__, "source_packet_v2.schema.json"),
    )
    checksum = payload.get("source", {}).get("checksum", "")
    if payload.get("evidence_state") in {
        "inspected",
        "queried_evidence",
        "conflicting",
    } and str(checksum).startswith("unverified:"):
        errors.append("$.source.checksum: inspected evidence cannot use an unverified checksum")
    if payload.get("evidence_state") == "queried_evidence" and not payload.get("locators"):
        errors.append("$.locators: queried evidence requires at least one locator")
    return errors


def command_create(args: argparse.Namespace) -> int:
    packet = create_packet(args)
    errors = validate_packet(packet)
    if errors:
        raise SystemExit("SourcePacket validation failed: " + "; ".join(errors))
    write_json(args.output, packet)
    print(
        json.dumps(
            {
                "packet_id": packet["packet_id"],
                "evidence_state": packet["evidence_state"],
                "locators": len(packet["locators"]),
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def command_validate(args: argparse.Namespace) -> int:
    errors = validate_packet(read_json(args.input))
    result = {"valid": not errors, "errors": errors, "input": str(args.input)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create or validate SourcePacket v2.")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create")
    create.add_argument("--source-type", required=True)
    create.add_argument("--source-id", required=True)
    create.add_argument("--title", default="")
    create.add_argument("--url", default="")
    create.add_argument("--source-version", default="unknown")
    create.add_argument("--retrieved-at", default="")
    create.add_argument(
        "--access-mode",
        choices=["public", "controlled", "private", "local", "unknown"],
        default="unknown",
    )
    create.add_argument(
        "--evidence-state",
        choices=[
            "candidate",
            "inspected",
            "queried_evidence",
            "conflicting",
            "unavailable",
        ],
        default="candidate",
    )
    create.add_argument(
        "--locator-mode",
        choices=["page-grounded", "structure-grounded", "source-limited"],
        default="source-limited",
    )
    create.add_argument("--locators-json", default="[]")
    create.add_argument("--dependencies-json", default="[]")
    create.add_argument("--supports-claim", action="append", default=[])
    create.add_argument("--cannot-support", action="append", default=[])
    create.add_argument(
        "--conflict-state",
        choices=["none_observed", "possible", "confirmed", "unknown"],
        default="unknown",
    )
    create.add_argument("--stale-after", default="P30D")
    create.add_argument("--recheck-trigger", action="append", default=[])
    create.add_argument("--supersedes", action="append", default=[])
    create.add_argument("--source-file", type=Path)
    create.add_argument("--checksum", default="")
    create.add_argument("--output", type=Path, required=True)
    create.set_defaults(func=command_create)

    validate = sub.add_parser("validate")
    validate.add_argument("--input", type=Path, required=True)
    validate.set_defaults(func=command_validate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
