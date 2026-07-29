#!/usr/bin/env python3
"""Wrap a scientific artifact in an OCEAN interoperability envelope."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    evidence_boundary,
    now_utc,
    read_json,
    schema_path,
    sha256_json,
    stable_id,
    validate_required_contract,
    write_json,
)


KNOWN_ARTIFACTS = {
    "ocean-source-packet-v2": ("source_packet", "packet_id"),
    "ocean-run-manifest-v1": ("run_manifest", "run_id"),
    "ocean-paper-bundle-v1": ("paper_bundle", "paper_id"),
    "ocean-claim-card-v1": ("claim_card", "claim_id"),
    "ocean-validation-card-v1": ("validation_card", "validation_id"),
}


def wrap(payload: dict, args: argparse.Namespace) -> dict:
    artifact_schema = str(payload.get("schema_version", "unknown"))
    inferred_type, id_field = KNOWN_ARTIFACTS.get(
        artifact_schema,
        ("external_artifact", ""),
    )
    artifact_type = args.artifact_type or inferred_type
    artifact_id = args.artifact_id or (
        str(payload.get(id_field, "")) if id_field else ""
    )
    if not artifact_id:
        artifact_id = stable_id("artifact", payload)
    checksum = sha256_json(payload)
    return {
        "schema_version": "ocean-artifact-envelope-v1",
        "envelope_id": stable_id(
            "envelope",
            {
                "artifact_type": artifact_type,
                "artifact_id": artifact_id,
                "checksum": checksum,
            },
        ),
        "artifact_type": artifact_type,
        "artifact_schema_version": artifact_schema,
        "artifact_id": artifact_id,
        "producer": {"name": args.producer, "version": args.producer_version},
        "created_at": now_utc(),
        "content_checksum": checksum,
        "artifact": payload,
        "source_refs": args.source_ref,
        "run_ref": args.run_ref,
        "access": args.access,
        "license": args.license,
        "evidence_boundary": evidence_boundary(
            inspected=["artifact JSON structure and content checksum"],
            not_inspected=[
                "scientific truth of artifact content",
                "external source availability",
                "license compatibility",
            ],
            cannot_conclude=[
                "scientific support merely because an artifact is interoperable"
            ],
            next_required=[
                "validate the embedded artifact contract and inspect its source references"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an OCEAN artifact envelope.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--artifact-type",
        choices=[
            "source_packet",
            "run_manifest",
            "paper_bundle",
            "claim_card",
            "validation_card",
            "external_artifact",
        ],
    )
    parser.add_argument("--artifact-id", default="")
    parser.add_argument("--producer", required=True)
    parser.add_argument("--producer-version", default="unknown")
    parser.add_argument("--source-ref", action="append", default=[])
    parser.add_argument("--run-ref", default="")
    parser.add_argument(
        "--access",
        choices=["public", "controlled", "private", "local", "unknown"],
        default="unknown",
    )
    parser.add_argument("--license", default="unknown")
    args = parser.parse_args(argv)
    result = wrap(read_json(args.input), args)
    errors = validate_required_contract(
        result,
        schema_path(__file__, "artifact_envelope.schema.json"),
    )
    if errors:
        raise SystemExit("Artifact envelope validation failed: " + "; ".join(errors))
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "envelope_id": result["envelope_id"],
                "artifact_type": result["artifact_type"],
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
