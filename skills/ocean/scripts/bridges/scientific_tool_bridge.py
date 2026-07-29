#!/usr/bin/env python3
"""Convert a scientific-tool result plus provenance into OCEAN contracts."""

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


def convert(payload: dict) -> tuple[dict, dict]:
    source = payload.get("source", {})
    result = payload.get("result", {})
    provenance = payload.get("provenance", {})
    locators = payload.get("locators", [])
    evidence_state = "queried_evidence" if result and locators else "candidate"
    source_packet = {
        "schema_version": "ocean-source-packet-v2",
        "packet_id": stable_id("packet", {"source": source, "result": result}),
        "source": {
            "source_type": source.get("source_type", "external_science_tool"),
            "source_id": source.get("source_id", ""),
            "title": source.get("title", ""),
            "url": source.get("url", ""),
            "version": source.get("version", ""),
            "retrieved_at": provenance.get("retrieved_at", now_utc()),
            "checksum": provenance.get("checksum") or sha256_json(result),
            "access_mode": source.get("access_mode", "unknown"),
        },
        "evidence_state": evidence_state,
        "locator_mode": "source-limited",
        "locators": locators,
        "supports_claims": payload.get("supports_claims", []),
        "cannot_support": payload.get(
            "cannot_support",
            ["mechanism, causality, or clinical utility without independent validation"],
        ),
        "upstream_dependencies": payload.get("upstream_dependencies", []),
        "conflict_state": payload.get("conflict_state", "unknown"),
        "recheck_policy": payload.get(
            "recheck_policy",
            {"stale_after": "unspecified", "recheck_trigger": ["source version changes"]},
        ),
        "result_summary": result,
        "evidence_boundary": evidence_boundary(
            inspected=["supplied external result and provenance fields"],
            not_inspected=["external tool implementation and undeclared upstream sources"],
            cannot_conclude=["scientific correctness from successful transformation"],
            next_required=["inspect source-specific result fields and independence"],
        ),
    }
    run_manifest = {
        "schema_version": "ocean-run-manifest-v1",
        "run_id": stable_id("run", provenance),
        "task_intent": provenance.get("task_intent", "external science tool bridge"),
        "created_at": provenance.get("created_at", now_utc()),
        "status": provenance.get("status", "executed" if result else "partial"),
        "command": provenance.get("command", []),
        "software": {
            "name": provenance.get("software", "external-scientific-tool"),
            "version": provenance.get("software_version", "unknown"),
        },
        "parameters": provenance.get("parameters", {}),
        "inputs": provenance.get("inputs", []),
        "outputs": provenance.get("outputs", []),
        "environment": provenance.get(
            "environment",
            {"python": "unknown", "platform": "unknown"},
        ),
        "logs": provenance.get("logs", []),
        "evidence_boundary": evidence_boundary(
            inspected=["supplied run provenance"],
            not_inspected=["undeclared environment and execution details"],
            cannot_conclude=["reproducibility without an independent rerun"],
            next_required=["validate run manifest and inspect outputs"],
        ),
    }
    return source_packet, run_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bridge external scientific-tool output."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args(argv)
    packet, manifest = convert(read_json(args.input))
    packet_errors = validate_required_contract(
        packet,
        schema_path(__file__, "source_packet_v2.schema.json"),
    )
    manifest_errors = validate_required_contract(
        manifest,
        schema_path(__file__, "run_manifest.schema.json"),
    )
    errors = packet_errors + manifest_errors
    if errors:
        raise SystemExit("Bridge contract validation failed: " + "; ".join(errors))
    write_json(args.packet_output, packet)
    write_json(args.manifest_output, manifest)
    print(json.dumps({"packet_id": packet["packet_id"], "run_id": manifest["run_id"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
