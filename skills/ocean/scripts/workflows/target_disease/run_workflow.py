#!/usr/bin/env python3
"""Run OCEAN Target-Disease Evidence Audit on supplied source packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))
WORKFLOW_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKFLOW_ROOT))

from ocean_core import read_json
from workflow_common import workflow_result, write_workflow_artifacts


REQUIRED_SOURCE_CLASSES = [
    "target_disease_association",
    "compound_or_perturbation",
    "pathway_or_interaction",
    "primary_literature",
    "clinical_registry",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Target-Disease Evidence Audit.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path)
    args = parser.parse_args(argv)
    payload = read_json(args.input)
    result = workflow_result(
        workflow="target_disease_evidence_audit",
        task_id=payload.get("task_id", "target-disease-unspecified"),
        payload=payload,
        required_source_classes=REQUIRED_SOURCE_CLASSES,
        extra_checks={
            "identity": {
                "target_id": payload.get("target_id", ""),
                "disease_id": payload.get("disease_id", ""),
            },
            "claim_ceiling": (
                "triangulated target-disease hypothesis; not validated mechanism, efficacy, or treatment recommendation"
            ),
        },
    )
    manifest_path = write_workflow_artifacts(
        result=result,
        input_path=args.input,
        output_path=args.output,
        manifest_path=args.manifest_output,
        parameters={"required_source_classes": REQUIRED_SOURCE_CLASSES},
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
                "workflow": result["workflow"],
                "state": result["state"],
                "missing_source_classes": result["missing_source_classes"],
                "independence": result["evidence_independence"]["classification"],
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
