#!/usr/bin/env python3
"""Run a bounded AI Manuscript Reliability Audit from grounded inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))
WORKFLOW_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_ROOT))
INGEST_ROOT = SCRIPT_ROOT / "ingest"
DETECTOR_ROOT = SCRIPT_ROOT / "detectors"
sys.path.insert(0, str(INGEST_ROOT))
sys.path.insert(0, str(DETECTOR_ROOT))

from ocean_core import evidence_boundary, now_utc, read_json, stable_id
from audit_source_grounding import audit_claims
from build_source_map import build_source_map
from claim_to_validation import compile_claim
from leakage import audit_leakage
from workflow_common import write_workflow_artifacts


def run_audit(payload: dict) -> dict:
    bundle = read_json(Path(payload["paper_bundle"]))
    source_map = build_source_map(bundle)
    claims_payload = {"claims": payload.get("claims", [])}
    grounding = audit_claims(source_map, claims_payload)
    leakage = audit_leakage(payload.get("split_manifest", {}))
    validation_cards = [
        compile_claim(
            row.get("claim_text", ""),
            row.get("claim_type"),
            row.get("evidence_classes", []),
            row.get("source_locators", []),
        )
        for row in payload.get("claims", [])
    ]
    risks = []
    if grounding["summary"]["needs_review"]:
        risks.append("one or more claims lack a resolved source locator")
    if leakage["classification"] in {"detected", "unknown"}:
        risks.append(f"leakage status: {leakage['classification']}")
    if any(card["missing_evidence"] for card in validation_cards):
        risks.append("one or more claims exceed currently declared evidence")
    state = "needs_revision_or_evidence" if risks else "ready_for_human_review"
    return {
        "schema_version": "ocean-manuscript-reliability-workflow-v1",
        "workflow_run_id": stable_id(
            "workflow",
            {"paper_id": bundle["paper_id"], "created_at": now_utc()},
        ),
        "created_at": now_utc(),
        "paper_id": bundle["paper_id"],
        "locator_mode": bundle["locator_mode"],
        "state": state,
        "source_map_summary": {
            "locators": len(source_map["locators"]),
            "figures": len(source_map["figures"]),
            "tables": len(source_map["tables"]),
            "unresolved_regions": source_map["unresolved_regions"],
        },
        "grounding_audit": grounding,
        "leakage_audit": leakage,
        "validation_cards": validation_cards,
        "priority_risks": risks,
        "safe_rewrite_rule": (
            "Any manuscript rewrite must remain separate from audit notes and must not add "
            "data, methods, citations, or completed validations that were not supplied."
        ),
        "handoff": {
            "Iceberg": "review claim support and safe downgrades",
            "Anchor": "resolve leakage, external validation, statistics, and reproducibility gaps",
            "Harbor": "preserve the grounded audit and author decisions separately from clean manuscript text",
        },
        "evidence_boundary": evidence_boundary(
            inspected=[
                "PaperBundle locators",
                "declared claims and evidence classes",
                "declared split identifiers",
            ],
            not_inspected=[
                "semantic truth of each claim",
                "figure pixels and table values unless represented in the bundle",
                "undeclared preprocessing or model training sources",
            ],
            cannot_conclude=[
                "submission readiness, clinical utility, or scientific correctness from structural checks alone"
            ],
            next_required=risks or ["domain and statistical human review"],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run AI Manuscript Reliability Audit.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path)
    args = parser.parse_args(argv)
    input_payload = read_json(args.input)
    result = run_audit(input_payload)
    manifest_path = write_workflow_artifacts(
        result=result,
        input_path=args.input,
        output_path=args.output,
        manifest_path=args.manifest_output,
        parameters={"paper_bundle": input_payload.get("paper_bundle", "")},
        command=[
            sys.executable,
            str(Path(__file__).resolve()),
            "--input",
            str(args.input),
            "--output",
            str(args.output),
        ],
    )
    print(
        json.dumps(
            {
                "state": result["state"],
                "locator_mode": result["locator_mode"],
                "priority_risks": result["priority_risks"],
                "output": str(args.output),
                "run_manifest": str(manifest_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
