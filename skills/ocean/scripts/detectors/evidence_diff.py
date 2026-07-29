#!/usr/bin/env python3
"""Compare two OCEAN evidence snapshots without silently upgrading claims."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


STATE_RANK = {
    "unavailable": 0,
    "candidate": 1,
    "inspected": 2,
    "queried_evidence": 3,
    "conflicting": 1,
}


def packet_map(payload: dict) -> dict[str, dict]:
    if payload.get("schema_version") == "ocean-source-packet-v2":
        packets = [payload]
    else:
        packets = payload.get("packets", [])
    return {
        packet.get("packet_id") or packet.get("source", {}).get("source_id", ""): packet
        for packet in packets
        if packet.get("packet_id") or packet.get("source", {}).get("source_id")
    }


def compare(old_payload: dict, new_payload: dict) -> dict:
    old = packet_map(old_payload)
    new = packet_map(new_payload)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = []
    upgrades = []
    weakened = []
    review = []
    for packet_id in sorted(set(old) & set(new)):
        before = old[packet_id]
        after = new[packet_id]
        fields = {}
        before_source = before.get("source", {})
        after_source = after.get("source", {})
        for field, left, right in [
            ("checksum", before_source.get("checksum"), after_source.get("checksum")),
            ("version", before_source.get("version"), after_source.get("version")),
            ("evidence_state", before.get("evidence_state"), after.get("evidence_state")),
            ("conflict_state", before.get("conflict_state"), after.get("conflict_state")),
        ]:
            if left != right:
                fields[field] = {"old": left, "new": right}
        if fields:
            changed.append({"packet_id": packet_id, "changes": fields})
        old_rank = STATE_RANK.get(before.get("evidence_state", "candidate"), 0)
        new_rank = STATE_RANK.get(after.get("evidence_state", "candidate"), 0)
        if new_rank > old_rank:
            upgrades.append(packet_id)
        if new_rank < old_rank or after.get("conflict_state") in {"possible", "confirmed"}:
            weakened.append(packet_id)
        if fields.get("checksum") or fields.get("version") or fields.get("conflict_state"):
            review.append(packet_id)
    return {
        "schema_version": "ocean-evidence-diff-v1",
        "new_evidence": added,
        "removed_evidence": removed,
        "changed_packets": changed,
        "claims_eligible_for_upgrade_review": sorted(set(upgrades)),
        "previously_supported_claims_may_be_weakened": sorted(set(removed + weakened)),
        "required_human_review": sorted(set(review + removed + upgrades + weakened)),
        "evidence_boundary": evidence_boundary(
            inspected=["packet identity, checksum, version, evidence state, and conflict state"],
            not_inspected=["semantic meaning of changed source content", "downstream claim dependencies"],
            cannot_conclude=[
                "that a claim should be automatically upgraded or downgraded",
                "that unchanged metadata means unchanged scientific evidence",
            ],
            next_required=["inspect changed content and re-run claim-to-source audits"],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare two OCEAN evidence snapshots.")
    parser.add_argument("--old", type=Path, required=True)
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = compare(read_json(args.old), read_json(args.new))
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "new": len(result["new_evidence"]),
                "removed": len(result["removed_evidence"]),
                "changed": len(result["changed_packets"]),
                "human_review": len(result["required_human_review"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
