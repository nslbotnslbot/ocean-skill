#!/usr/bin/env python3
"""Build a public leaderboard only from fully adjudicated submissions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT_ROOT = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    evidence_boundary,
    read_json,
    schema_path,
    sha256_file,
    validate_required_contract,
    write_json,
)


def evaluate_submission(submission: dict, minimum_cases: int) -> tuple[dict, list[str]]:
    reasons = []
    report_path = Path(submission.get("report_path", ""))
    if not report_path.is_file():
        return {}, ["benchmark report is unavailable"]
    report = read_json(report_path)
    declared_checksum = submission.get("report_checksum", "")
    if not declared_checksum or declared_checksum != sha256_file(report_path):
        reasons.append("benchmark report checksum is missing or mismatched")
    case_ids = {
        row.get("case_id")
        for row in report.get("rows", [])
        if row.get("case_id")
    }
    if len(case_ids) != report.get("cases", 0):
        reasons.append("report rows do not cover the declared case count")
    for metric in (
        "accuracy",
        "macro_f1",
        "unsupported_strong_claim_errors",
    ):
        if not isinstance(report.get(metric), (int, float)):
            reasons.append(f"report metric is missing or non-numeric: {metric}")
    if report.get("cases", 0) < minimum_cases:
        reasons.append(f"fewer than {minimum_cases} cases")
    adjudication_paths = [
        Path(path) for path in submission.get("adjudication_records", [])
    ]
    records = []
    adjudication_schema = schema_path(
        str(SCRIPT_ROOT / "ocean.py"),
        "adjudication_record.schema.json",
    )
    for path in adjudication_paths:
        if not path.is_file():
            reasons.append(f"adjudication record unavailable: {path}")
            continue
        record = read_json(path)
        record_errors = validate_required_contract(
            record,
            adjudication_schema,
        )
        if record_errors:
            reasons.append(
                f"invalid adjudication record {path}: "
                + "; ".join(record_errors)
            )
            continue
        records.append(record)
    adjudicated_ids = {record.get("case_id") for record in records}
    if len(adjudicated_ids) != len(records):
        reasons.append("adjudication records contain duplicate case IDs")
    if case_ids - adjudicated_ids:
        reasons.append("one or more report cases lack adjudication records")
    if any(record.get("blinding_state") != "blinded" for record in records):
        reasons.append("one or more adjudication records were not blinded")
    if any(len(record.get("reviewers", [])) < 2 for record in records):
        reasons.append("one or more cases have fewer than two reviewers")
    if not submission.get("external_origin"):
        reasons.append("submission is not declared external")
    if not submission.get("permission_to_publish"):
        reasons.append("permission to publish is absent")
    if reasons:
        return {}, reasons
    return {
        "submission_id": submission.get("submission_id", ""),
        "system_name": submission.get("system_name", ""),
        "system_version": submission.get("system_version", ""),
        "condition": report.get("condition", ""),
        "cases": report.get("cases", 0),
        "accuracy": report.get("accuracy"),
        "macro_f1": report.get("macro_f1"),
        "unsupported_strong_claim_errors": report.get(
            "unsupported_strong_claim_errors"
        ),
        "report_checksum": declared_checksum,
    }, []


def build(payload: dict, minimum_cases: int) -> dict:
    accepted = []
    rejected = []
    for submission in payload.get("submissions", []):
        row, reasons = evaluate_submission(submission, minimum_cases)
        if reasons:
            rejected.append(
                {
                    "submission_id": submission.get("submission_id", ""),
                    "reasons": reasons,
                }
            )
        else:
            accepted.append(row)
    accepted.sort(
        key=lambda row: (
            -(row["macro_f1"] if isinstance(row["macro_f1"], (int, float)) else -1),
            row["unsupported_strong_claim_errors"],
            row["system_name"],
        )
    )
    for rank, row in enumerate(accepted, start=1):
        row["rank"] = rank
    return {
        "schema_version": "ocean-public-leaderboard-v1",
        "benchmark_version": payload.get("benchmark_version", ""),
        "minimum_cases": minimum_cases,
        "entries": accepted,
        "rejected_submissions": rejected,
        "evidence_boundary": evidence_boundary(
            inspected=[
                "report checksum, case count, adjudication coverage, blinding declarations, and publication permission"
            ],
            not_inspected=[
                "expert identity",
                "system execution environment",
                "source truth beyond submitted adjudication records",
            ],
            cannot_conclude=[
                "general scientific superiority from leaderboard rank"
            ],
            next_required=[
                "independent audit of accepted submissions and periodic re-evaluation"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a gated OCEAN leaderboard.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--minimum-cases", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = build(read_json(args.input), args.minimum_cases)
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "accepted": len(result["entries"]),
                "rejected": len(result["rejected_submissions"]),
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
