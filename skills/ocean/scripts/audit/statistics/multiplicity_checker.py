#!/usr/bin/env python3
"""Check declared hypothesis families and multiple-comparison control."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


def check(payload: dict) -> dict:
    families = payload.get("hypothesis_families", [])
    method = payload.get("multiplicity_method", "")
    exploratory = bool(payload.get("exploratory"))
    total = sum(int(item.get("tests", 0)) for item in families)
    issues = []
    if total > 1 and not method and not exploratory:
        issues.append("multiple confirmatory tests are declared without a multiplicity method")
    if exploratory and not payload.get("exploratory_label_in_manuscript", False):
        issues.append("exploratory analyses are not explicitly labelled in the manuscript")
    return {
        "schema_version": "ocean-multiplicity-audit-v1",
        "tests_declared": total,
        "hypothesis_families": families,
        "multiplicity_method": method,
        "exploratory": exploratory,
        "issues": issues,
        "status": "needs_review" if issues else "declared_control_present",
        "evidence_boundary": evidence_boundary(
            inspected=["declared hypothesis counts, families, and correction method"],
            not_inspected=["actual p-values", "analysis code", "unreported analyses"],
            cannot_conclude=["valid multiplicity control from a method name alone"],
            next_required=issues or ["inspect implementation and prespecification"],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit multiple-comparison metadata.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = check(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps({"status": result["status"], "issues": result["issues"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
