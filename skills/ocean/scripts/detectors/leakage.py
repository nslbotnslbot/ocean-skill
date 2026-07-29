#!/usr/bin/env python3
"""Detect declared entity, site, time, and benchmark overlap across splits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


DIMENSIONS = [
    "patient_ids",
    "subject_ids",
    "sample_ids",
    "site_ids",
    "time_windows",
    "benchmark_ids",
    "source_record_ids",
]


def overlap(left: list, right: list) -> list:
    return sorted(set(left) & set(right), key=str)


def audit_leakage(payload: dict) -> dict:
    splits = payload.get("splits", {})
    pairs = []
    names = sorted(splits)
    for index, left_name in enumerate(names):
        for right_name in names[index + 1 :]:
            left = splits[left_name]
            right = splits[right_name]
            overlaps = {
                dimension: overlap(left.get(dimension, []), right.get(dimension, []))
                for dimension in DIMENSIONS
            }
            overlaps = {key: value for key, value in overlaps.items() if value}
            pairs.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "overlaps": overlaps,
                    "leakage_detected": bool(overlaps),
                }
            )
    missing_dimensions = [
        dimension
        for dimension in DIMENSIONS
        if not any(dimension in split for split in splits.values())
    ]
    detected = any(pair["leakage_detected"] for pair in pairs)
    classification = (
        "detected"
        if detected
        else "unknown"
        if not splits or len(missing_dimensions) == len(DIMENSIONS)
        else "not_detected_in_declared_identifiers"
    )
    return {
        "schema_version": "ocean-leakage-audit-v1",
        "classification": classification,
        "split_pairs": pairs,
        "missing_dimensions": missing_dimensions,
        "evidence_boundary": evidence_boundary(
            inspected=["explicit identifiers declared in each split"],
            not_inspected=[
                "latent duplicates",
                "pretraining overlap",
                "feature engineering performed before splitting",
                "unreported temporal or site relationships",
            ],
            cannot_conclude=[
                "absence of leakage when identifiers or preprocessing provenance are incomplete"
            ],
            next_required=(
                [f"provide split-level {dimension}" for dimension in missing_dimensions]
                or ["inspect preprocessing order and hidden duplicate relationships"]
            ),
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit declared split leakage.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = audit_leakage(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps({"classification": result["classification"], "pairs": len(result["split_pairs"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
