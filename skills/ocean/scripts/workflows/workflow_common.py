#!/usr/bin/env python3
"""Shared helpers for OCEAN task-level evidence workflows."""

from __future__ import annotations

from pathlib import Path
import platform
import sys
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))
DETECTOR_ROOT = SCRIPT_ROOT / "detectors"
sys.path.insert(0, str(DETECTOR_ROOT))

from ocean_core import (
    OCEAN_VERSION,
    evidence_boundary,
    file_record,
    now_utc,
    schema_path,
    stable_id,
    validate_required_contract,
    write_json,
)
from claim_to_validation import compile_claim
from evidence_independence import classify_graph


def compile_claims(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        compile_claim(
            row.get("claim_text", ""),
            row.get("claim_type"),
            row.get("evidence_classes", []),
            row.get("source_locators", []),
        )
        for row in rows
    ]


def source_inventory(payload: dict[str, Any]) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}
    for packet in payload.get("source_packets", []):
        source = packet.get("source", {})
        source_type = source.get("source_type", "unknown")
        inventory.setdefault(source_type, []).append(
            packet.get("packet_id") or source.get("source_id", "unknown")
        )
    return inventory


def workflow_result(
    *,
    workflow: str,
    task_id: str,
    payload: dict[str, Any],
    required_source_classes: list[str],
    extra_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    inventory = source_inventory(payload)
    missing_sources = [
        source_class
        for source_class in required_source_classes
        if source_class not in inventory
    ]
    independence = classify_graph(payload.get("evidence_graph", {}))
    validation_cards = compile_claims(payload.get("claims", []))
    unresolved_claims = [
        card["claim_id"] for card in validation_cards if card["missing_evidence"]
    ]
    state = (
        "blocked_by_missing_evidence"
        if missing_sources or unresolved_claims or independence["classification"] in {"circular", "unknown"}
        else "ready_for_human_review"
    )
    return {
        "schema_version": "ocean-task-workflow-v1",
        "workflow": workflow,
        "workflow_run_id": stable_id(
            "workflow",
            {"workflow": workflow, "task_id": task_id, "created_at": now_utc()},
        ),
        "task_id": task_id,
        "created_at": now_utc(),
        "state": state,
        "source_inventory": inventory,
        "required_source_classes": required_source_classes,
        "missing_source_classes": missing_sources,
        "evidence_independence": independence,
        "validation_cards": validation_cards,
        "extra_checks": extra_checks or {},
        "handoff": {
            "Reef": "source inventory and independence classification",
            "Iceberg": "claim ceiling and unsupported-claim downgrade",
            "Anchor": "missing evidence, decisive controls, pass criteria, and stop conditions",
            "Harbor": "preserve this result with its source packets and run manifest",
        },
        "evidence_boundary": evidence_boundary(
            inspected=[
                "provided source-packet metadata",
                "provided evidence graph",
                "provided claim and evidence-class declarations",
            ],
            not_inspected=[
                "undeclared sources",
                "raw source records unless embedded in the supplied packets",
                "scientific correctness of user-provided metadata",
            ],
            cannot_conclude=[
                "scientific validity or clinical readiness from workflow completion",
                "independence when upstream provenance is omitted",
            ],
            next_required=(
                [f"add source class: {item}" for item in missing_sources]
                + [f"resolve validation card: {claim_id}" for claim_id in unresolved_claims]
                or ["domain-expert review of source content and pass criteria"]
            ),
        ),
    }


def write_workflow_artifacts(
    *,
    result: dict[str, Any],
    input_path: Path,
    output_path: Path,
    manifest_path: Path | None,
    parameters: dict[str, Any] | None = None,
    command: list[str] | None = None,
) -> Path:
    """Write a workflow result and a reproducibility sidecar manifest."""

    write_json(output_path, result)
    resolved_manifest = manifest_path or Path(
        str(output_path) + ".run-manifest.json"
    )
    manifest = {
        "schema_version": "ocean-run-manifest-v1",
        "run_id": stable_id(
            "run",
            {
                "workflow_run_id": result["workflow_run_id"],
                "input": file_record(input_path),
                "output": file_record(output_path),
            },
        ),
        "task_intent": result.get("workflow", "manuscript_reliability_audit"),
        "created_at": result["created_at"],
        "status": "executed",
        "command": command or [],
        "software": {
            "name": "OCEAN evidence-control workflow",
            "version": OCEAN_VERSION,
        },
        "parameters": parameters or {},
        "inputs": [file_record(input_path)],
        "outputs": [file_record(output_path)],
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "logs": [],
        "evidence_boundary": evidence_boundary(
            inspected=[
                "workflow input and output file identity/checksum",
                "workflow software version and declared parameters",
            ],
            not_inspected=[
                "undeclared dependencies",
                "scientific correctness of workflow inputs or outputs",
            ],
            cannot_conclude=[
                "biological, clinical, or statistical validity from successful execution"
            ],
            next_required=["inspect source-level evidence and human review decisions"],
        ),
    }
    errors = validate_required_contract(
        manifest,
        schema_path(__file__, "run_manifest.schema.json"),
    )
    if errors:
        raise SystemExit("Workflow RunManifest validation failed: " + "; ".join(errors))
    write_json(resolved_manifest, manifest)
    return resolved_manifest
