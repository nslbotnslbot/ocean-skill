#!/usr/bin/env python3
"""Run OCEAN Variant Evidence Triangulation on supplied source packets."""

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
    "variant_assertion",
    "population_frequency",
    "functional_annotation",
    "tissue_or_regulatory_evidence",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Variant Evidence Triangulation.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path)
    args = parser.parse_args(argv)
    payload = read_json(args.input)
    task_id = payload.get("task_id", "variant-evidence-unspecified")
    result = workflow_result(
        workflow="variant_evidence_triangulation",
        task_id=task_id,
        payload=payload,
        required_source_classes=REQUIRED_SOURCE_CLASSES,
        extra_checks={
            "identity": {
                "variant_id": payload.get("variant_id", ""),
                "assembly": payload.get("assembly", ""),
                "transcript": payload.get("transcript", ""),
            },
            "claim_ceiling": (
                "variant-level evidence synthesis; not patient-level diagnosis or treatment guidance"
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
