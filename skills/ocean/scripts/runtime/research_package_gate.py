#!/usr/bin/env python3
"""Gate a declared research package before a human red-team review.

This program checks only the supplied package structure and traceability.  It
does not evaluate scientific validity and never emits Go, Rework, or Stop.
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


SUPPORTED_DOMAINS = {
    "biomedical_ai",
    "clinical_prediction",
    "knowledge_graph",
    "database",
}
REQUIRED_COMPONENTS = (
    "study_framing",
    "claims_or_study_plan",
    "data_or_cohort",
    "validation_design",
)
TRACEABLE_PACKET_STATES = {"inspected", "queried_evidence"}
COMPONENT_STATUSES = {"inspected", "partial", "missing", "not_applicable"}
PACKET_STATES = TRACEABLE_PACKET_STATES | {"candidate", "unavailable"}


def validate_structure(payload: dict) -> list[str]:
    """Validate the nested subset that the dependency-free schema helper omits."""

    errors: list[str] = []
    components = payload.get("components")
    if not isinstance(components, dict):
        return ["components must be an object"]
    for name in REQUIRED_COMPONENTS:
        component = components.get(name)
        if not isinstance(component, dict):
            errors.append(f"components.{name} must be an object")
            continue
        if component.get("status") not in COMPONENT_STATUSES:
            errors.append(f"components.{name}.status is invalid")
        locators = component.get("locators")
        if not isinstance(locators, list) or not all(
            isinstance(locator, str) for locator in locators
        ):
            errors.append(f"components.{name}.locators must be a string list")
    packets = payload.get("source_packets")
    if not isinstance(packets, list):
        return errors + ["source_packets must be an array"]
    for index, packet in enumerate(packets):
        if not isinstance(packet, dict):
            errors.append(f"source_packets[{index}] must be an object")
            continue
        if not isinstance(packet.get("packet_id"), str) or not packet["packet_id"]:
            errors.append(f"source_packets[{index}].packet_id must be non-empty")
        if packet.get("evidence_state") not in PACKET_STATES:
            errors.append(f"source_packets[{index}].evidence_state is invalid")
        locators = packet.get("locators")
        if not isinstance(locators, list) or not all(
            isinstance(locator, str) for locator in locators
        ):
            errors.append(f"source_packets[{index}].locators must be a string list")
    return errors


def missing_requirements(payload: dict) -> list[str]:
    components = payload.get("components", {})
    missing = []
    for name in REQUIRED_COMPONENTS:
        component = components.get(name, {})
        if component.get("status") != "inspected" or not component.get("locators"):
            missing.append(f"provide inspected, located component: {name}")
    packets = payload.get("source_packets", [])
    traceable_packets = [
        packet
        for packet in packets
        if packet.get("evidence_state") in TRACEABLE_PACKET_STATES
        and packet.get("packet_id")
        and packet.get("locators")
    ]
    if not traceable_packets:
        missing.append("provide at least one traceable inspected or queried source packet")
    return missing


def gate(payload: dict) -> dict:
    mode = payload.get("request_mode", "")
    requested = bool(payload.get("red_team_requested"))
    domain = payload.get("domain", "")

    if not requested:
        status = "not_requested"
        reason = "The selected OCEAN mode should continue without the package red-team contract."
        required_next = []
    elif mode not in {"Design", "Audit"}:
        status = "not_applicable"
        reason = "Research-package red-team is limited to Design and Audit requests."
        required_next = ["use the selected normal OCEAN mode"]
    elif domain not in SUPPORTED_DOMAINS:
        status = "not_applicable"
        reason = "The declared domain is outside the package red-team specialization."
        required_next = ["use the domain-specific normal OCEAN route"]
    else:
        required_next = missing_requirements(payload)
        if required_next:
            status = "cannot_decide"
            reason = "The declared package is incomplete or lacks traceable evidence required for a package-level decision."
        else:
            status = "ready_for_human_red_team"
            reason = "The declared package has the minimum traceable structure for human-and-model red-team review."

    components = payload.get("components", {})
    inspected_components = [
        name
        for name in REQUIRED_COMPONENTS
        if components.get(name, {}).get("status") == "inspected"
        and components.get(name, {}).get("locators")
    ]
    packet_ids = [
        packet.get("packet_id", "")
        for packet in payload.get("source_packets", [])
        if packet.get("packet_id")
    ]
    return {
        "schema_version": "ocean-research-package-gate-v1",
        "gate_id": stable_id("red-team-gate", payload),
        "request_mode": mode,
        "red_team_requested": requested,
        "domain": domain,
        "status": status,
        "reason": reason,
        "inspected_components": inspected_components,
        "source_packet_ids": packet_ids,
        "next_required": required_next,
        "evidence_boundary": evidence_boundary(
            inspected=[
                "declared request mode, domain, component states, source packet identifiers, and locators"
            ],
            not_inspected=[
                "scientific content of sources",
                "data, cohort, code, and validation correctness beyond declared locators",
                "publication, ethics, authorship, and clinical-decision context",
            ],
            cannot_conclude=[
                "scientific validity from package structure",
                "Go, Rework, Stop, publishability, clinical utility, or authorship",
            ],
            next_required=required_next or [
                "perform a bounded human red-team review against inspected material"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check a declared research package before human red-team review."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = read_json(args.input)
    errors = validate_required_contract(
        payload,
        schema_path(__file__, "research_package.schema.json"),
    )
    errors.extend(validate_structure(payload))
    if errors:
        raise SystemExit("ResearchPackage contract failed: " + "; ".join(errors))
    result = gate(payload)
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "next_required": len(result["next_required"]),
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
