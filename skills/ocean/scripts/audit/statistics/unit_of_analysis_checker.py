#!/usr/bin/env python3
"""Check experimental-unit, observation-unit, and pseudoreplication risks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ocean_core import read_json, write_json
from statistics_common import make_card, missing_fields


def check(payload: dict) -> dict:
    issues = []
    experimental = payload.get("experimental_unit")
    observation = payload.get("observation_unit")
    hierarchy = payload.get("replication_hierarchy", {})
    model = str(payload.get("model_or_test", "")).casefold()
    if experimental and observation and experimental != observation:
        clustering_terms = ("mixed", "cluster", "random effect", "gee", "nested", "repeated")
        if not any(term in model for term in clustering_terms):
            issues.append(
                "observation unit differs from experimental unit but the declared model does not describe clustering or nesting"
            )
    if hierarchy and not isinstance(hierarchy, (dict, list)):
        issues.append("replication_hierarchy should be a structured object or list")
    if isinstance(hierarchy, dict):
        if hierarchy.get("technical_replicates") and not hierarchy.get("biological_replicates"):
            issues.append("technical replicates are declared without biological-replicate information")
    missing = [
        field
        for field in ("experimental_unit", "observation_unit", "replication_hierarchy")
        if not payload.get(field)
    ]
    return make_card(
        payload,
        issues=issues,
        author_input=[f"provide {field}" for field in missing],
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check unit-of-analysis metadata.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    card = check(read_json(args.input))
    write_json(args.output, card)
    print(json.dumps({"status": card["status"], "issues": card["issues"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
