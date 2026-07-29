#!/usr/bin/env python3
"""Check structured figure-statistics metadata for common reporting gaps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


def check_figure(figure: dict) -> dict:
    required = ["figure_id", "experimental_unit", "n_definition", "summary_statistic"]
    missing = [field for field in required if not figure.get(field)]
    issues = [f"missing {field}" for field in missing]
    if figure.get("error_bars") and not figure.get("error_bar_definition"):
        issues.append("error bars are shown without a definition")
    if figure.get("p_values") and not figure.get("statistical_test"):
        issues.append("p-values are reported without a named test")
    if figure.get("statistical_test") and not figure.get("assumptions_checked"):
        issues.append("a statistical test is named but assumption checking is not declared")
    return {
        "figure_id": figure.get("figure_id", ""),
        "issues": issues,
        "status": "needs_review" if issues else "metadata_complete",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit structured figure-statistics metadata.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = read_json(args.input)
    rows = [check_figure(item) for item in payload.get("figures", [])]
    needs_review = sum(row["status"] == "needs_review" for row in rows)
    result = {
        "schema_version": "ocean-figure-statistics-audit-v1",
        "figures": rows,
        "summary": {"total": len(rows), "needs_review": needs_review},
        "evidence_boundary": evidence_boundary(
            inspected=["declared figure-statistics metadata"],
            not_inspected=["figure pixels", "raw plotted values", "analysis code"],
            cannot_conclude=["that a figure is statistically valid from metadata alone"],
            next_required=["inspect raw data and analysis for each claim-relevant figure"],
        ),
    }
    write_json(args.output, result)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
