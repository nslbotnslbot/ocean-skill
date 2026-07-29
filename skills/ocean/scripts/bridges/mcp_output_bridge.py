#!/usr/bin/env python3
"""Convert an inspected MCP/app tool response into a bounded SourcePacket v2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, now_utc, read_json, sha256_json, stable_id, write_json


def convert(payload: dict) -> dict:
    response = payload.get("response")
    inspected_fields = payload.get("inspected_fields", [])
    source_id = payload.get("source_id", "")
    return {
        "schema_version": "ocean-source-packet-v2",
        "packet_id": stable_id("packet", {"source_id": source_id, "response": response}),
        "source": {
            "source_type": "mcp_or_app_tool_response",
            "source_id": source_id,
            "title": payload.get("title", ""),
            "url": payload.get("url", ""),
            "version": payload.get("source_version", ""),
            "retrieved_at": payload.get("retrieved_at", now_utc()),
            "checksum": sha256_json(response),
            "access_mode": payload.get("access_mode", "unknown"),
        },
        "evidence_state": "inspected" if inspected_fields else "candidate",
        "locator_mode": "source-limited",
        "locators": payload.get("locators", []),
        "supports_claims": payload.get("supports_claims", []),
        "cannot_support": payload.get(
            "cannot_support",
            ["claims outside the inspected response fields"],
        ),
        "upstream_dependencies": payload.get("upstream_dependencies", []),
        "conflict_state": payload.get("conflict_state", "unknown"),
        "recheck_policy": payload.get(
            "recheck_policy",
            {"stale_after": "unspecified", "recheck_trigger": ["upstream response changes"]},
        ),
        "response": response,
        "evidence_boundary": evidence_boundary(
            inspected=[f"response field: {field}" for field in inspected_fields],
            not_inspected=payload.get("not_inspected", ["undeclared response fields and upstream source implementation"]),
            cannot_conclude=payload.get(
                "cannot_conclude",
                ["scientific validity from tool transport alone"],
            ),
            next_required=payload.get(
                "next_required",
                ["inspect source provenance and claim relevance"],
            ),
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bridge an MCP/app response to SourcePacket v2.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    packet = convert(read_json(args.input))
    write_json(args.output, packet)
    print(json.dumps({"packet_id": packet["packet_id"], "evidence_state": packet["evidence_state"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
