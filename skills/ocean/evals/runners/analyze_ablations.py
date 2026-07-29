#!/usr/bin/env python3
"""Compute descriptive deltas between pre-specified OCEAN conditions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from ocean_core import evidence_boundary, read_json, write_json


METRICS = (
    "accuracy",
    "macro_f1",
    "unsupported_strong_claim_errors",
)


def compare(payload: dict) -> dict:
    reference_name = payload.get("reference_condition")
    reports = payload.get("reports", [])
    by_condition = {report.get("condition"): report for report in reports}
    if not reference_name or reference_name not in by_condition:
        raise SystemExit("reference_condition must identify one supplied report")
    reference = by_condition[reference_name]
    reference_cases = reference.get("case_ids_checksum")
    if not reference_cases:
        raise SystemExit("Reference report is missing case_ids_checksum")
    rows = []
    for condition, report in sorted(by_condition.items()):
        if condition == reference_name:
            continue
        if report.get("cases") != reference.get("cases"):
            raise SystemExit(
                f"Condition {condition} covers a different number of cases"
            )
        if report.get("case_ids_checksum") != reference_cases:
            raise SystemExit(
                f"Condition {condition} covers a different case set"
            )
        rows.append(
            {
                "condition": condition,
                "reference": reference_name,
                "cases": report.get("cases"),
                "deltas": {
                    metric: round(
                        float(report.get(metric, 0))
                        - float(reference.get(metric, 0)),
                        6,
                    )
                    for metric in METRICS
                },
            }
        )
    return {
        "schema_version": "ocean-ablation-summary-v1",
        "reference_condition": reference_name,
        "comparisons": rows,
        "evidence_boundary": evidence_boundary(
            inspected=["declared aggregate reports with equal case counts"],
            not_inspected=[
                "case-set identity beyond counts",
                "run pairing",
                "sampling uncertainty",
            ],
            cannot_conclude=[
                "causal contribution of a component",
                "statistical significance or generalization",
            ],
            next_required=[
                "use identical blinded cases, repeated runs, and a pre-specified analysis plan"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze OCEAN ablation reports.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = compare(read_json(args.input))
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "reference_condition": result["reference_condition"],
                "comparisons": len(result["comparisons"]),
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
