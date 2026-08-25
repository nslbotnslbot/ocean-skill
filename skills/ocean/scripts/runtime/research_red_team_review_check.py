#!/usr/bin/env python3
"""Validate evidence traceability in a completed OCEAN red-team review.

The checker validates a review record's declared links. It does not inspect the
scientific content behind those links and does not make a research decision.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    evidence_boundary,
    read_json,
    schema_path,
    stable_id,
    validate_required_contract,
    write_json,
)


REQUIRED_KINDS = {
    "bottleneck",
    "validity_verdict",
    "minimum_validation",
    "decision",
    "reviewer_risk",
    "collaboration_boundary",
}
DECISIONS = {"Go", "Rework", "Stop", "Cannot decide"}
EVIDENCE_STATES = {"located", "explicit_unknown"}


def validate_structure(payload: dict) -> list[str]:
    """Validate nested fields and the cross-reference rules for a review."""

    errors: list[str] = []
    allowed_root = {
        "schema_version",
        "package_gate_id",
        "package_gate_status",
        "source_packet_ids",
        "conclusions",
    }
    unexpected_root = set(payload) - allowed_root
    if unexpected_root:
        errors.append(
            "review record has unsupported fields: " + ", ".join(sorted(unexpected_root))
        )
    if not isinstance(payload.get("package_gate_id"), str) or not payload["package_gate_id"].strip():
        errors.append("package_gate_id must be non-empty")
    packet_ids = payload.get("source_packet_ids")
    if not isinstance(packet_ids, list) or not packet_ids or not all(
        isinstance(packet_id, str) and packet_id for packet_id in packet_ids
    ):
        return ["source_packet_ids must be a non-empty list of strings"]
    if len(set(packet_ids)) != len(packet_ids):
        errors.append("source_packet_ids must be unique")
    known_packets = set(packet_ids)

    conclusions = payload.get("conclusions")
    if not isinstance(conclusions, list) or not conclusions:
        return errors + ["conclusions must be a non-empty array"]

    ids: set[str] = set()
    kinds: set[str] = set()
    for index, conclusion in enumerate(conclusions):
        location = f"conclusions[{index}]"
        if not isinstance(conclusion, dict):
            errors.append(f"{location} must be an object")
            continue
        allowed = {
            "conclusion_id",
            "kind",
            "statement",
            "decision",
            "evidence_state",
            "evidence",
            "next_required",
        }
        unexpected = set(conclusion) - allowed
        if unexpected:
            errors.append(f"{location} has unsupported fields: {', '.join(sorted(unexpected))}")
        conclusion_id = conclusion.get("conclusion_id")
        if not isinstance(conclusion_id, str) or not conclusion_id:
            errors.append(f"{location}.conclusion_id must be non-empty")
        elif conclusion_id in ids:
            errors.append(f"duplicate conclusion_id: {conclusion_id}")
        else:
            ids.add(conclusion_id)

        kind = conclusion.get("kind")
        if kind not in REQUIRED_KINDS:
            errors.append(f"{location}.kind is invalid")
        else:
            kinds.add(kind)
        statement = conclusion.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            errors.append(f"{location}.statement must be non-empty")
        evidence_state = conclusion.get("evidence_state")
        if evidence_state not in EVIDENCE_STATES:
            errors.append(f"{location}.evidence_state is invalid")
        evidence = conclusion.get("evidence")
        if not isinstance(evidence, list):
            errors.append(f"{location}.evidence must be an array")
            evidence = []
        for evidence_index, item in enumerate(evidence):
            evidence_location = f"{location}.evidence[{evidence_index}]"
            if not isinstance(item, dict):
                errors.append(f"{evidence_location} must be an object")
                continue
            if item.get("packet_id") not in known_packets:
                errors.append(f"{evidence_location}.packet_id must be listed in source_packet_ids")
            if not isinstance(item.get("locator"), str) or not item["locator"].strip():
                errors.append(f"{evidence_location}.locator must be non-empty")

        next_required = conclusion.get("next_required")
        if not isinstance(next_required, list) or not all(
            isinstance(item, str) and item.strip() for item in next_required
        ):
            errors.append(f"{location}.next_required must be a string list")
            next_required = []
        if evidence_state == "located" and not evidence:
            errors.append(f"{location} marked located requires at least one evidence locator")
        if evidence_state == "explicit_unknown":
            if evidence:
                errors.append(f"{location} marked explicit_unknown must not cite unsupported evidence")
            if not next_required:
                errors.append(f"{location} marked explicit_unknown requires a next_required item")

        decision = conclusion.get("decision")
        if kind == "decision" and decision not in DECISIONS:
            errors.append(f"{location}.decision must be Go, Rework, Stop, or Cannot decide")
        if kind != "decision" and decision is not None:
            errors.append(f"{location}.decision is allowed only for kind=decision")

    missing_kinds = REQUIRED_KINDS - kinds
    if missing_kinds:
        errors.append("missing required conclusion kinds: " + ", ".join(sorted(missing_kinds)))
    return errors


def summary(payload: dict) -> dict:
    conclusions = payload["conclusions"]
    return {
        "schema_version": "ocean-research-red-team-review-check-v1",
        "review_check_id": stable_id("red-team-review-check", payload),
        "status": "valid",
        "package_gate_id": payload["package_gate_id"],
        "source_packet_ids": payload["source_packet_ids"],
        "traceable_conclusion_count": sum(
            conclusion["evidence_state"] == "located" for conclusion in conclusions
        ),
        "explicit_unknown_conclusion_count": sum(
            conclusion["evidence_state"] == "explicit_unknown" for conclusion in conclusions
        ),
        "evidence_boundary": evidence_boundary(
            inspected=[
                "declared source-packet identifiers and conclusion-to-locator references"
            ],
            not_inspected=[
                "scientific content, authority, or completeness of the linked sources",
                "whether the stated research decision is scientifically correct",
            ],
            cannot_conclude=[
                "scientific validity, publishability, clinical utility, ethics, or authorship",
                "whether a cited locator supports more than the review record declares",
            ],
            next_required=[
                "human review of each cited source packet and locator before relying on the conclusion"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate evidence links in a completed research red-team review."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = read_json(args.input)
    errors = validate_required_contract(
        payload,
        schema_path(__file__, "research_red_team_review.schema.json"),
    )
    errors.extend(validate_structure(payload))
    if errors:
        raise SystemExit("Research red-team review contract failed: " + "; ".join(errors))
    result = summary(payload)
    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
