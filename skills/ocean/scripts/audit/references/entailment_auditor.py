#!/usr/bin/env python3
"""Triage citation entailment from explicit source-review annotations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ocean_core import evidence_boundary, read_json, write_json
from citation_scope_checker import check_pair


def audit_pair(item: dict) -> dict:
    scope = check_pair(item)
    claim = item.get("claim", {})
    citation = item.get("citation", {})
    reviewed_support = citation.get("reviewed_support", "unknown")
    source_locator = citation.get("source_locator", "")
    if reviewed_support == "contradicts":
        verdict = "contradicted"
    elif reviewed_support == "does_not_support":
        verdict = "not_supported"
    elif reviewed_support == "supports" and scope["status"] == "scope_compatible" and source_locator:
        verdict = "supported_candidate"
    elif reviewed_support == "supports":
        verdict = "partially_supported"
    else:
        verdict = "unknown"
    return {
        "claim_id": claim.get("claim_id", ""),
        "citation_id": citation.get("citation_id", ""),
        "verdict": verdict,
        "reviewed_support": reviewed_support,
        "source_locator": source_locator,
        "scope": scope,
    }


def audit(payload: dict) -> dict:
    rows = [audit_pair(item) for item in payload.get("pairs", [])]
    return {
        "schema_version": "ocean-citation-entailment-audit-v1",
        "pairs": rows,
        "summary": {
            "total": len(rows),
            "supported_candidates": sum(row["verdict"] == "supported_candidate" for row in rows),
            "unknown_or_problematic": sum(row["verdict"] != "supported_candidate" for row in rows),
        },
        "evidence_boundary": evidence_boundary(
            inspected=[
                "explicit human/tool review annotation",
                "source locator presence",
                "declared context compatibility",
            ],
            not_inspected=[
                "source passage semantics unless reviewed_support was produced by a documented review",
                "unprovided full text",
            ],
            cannot_conclude=[
                "automated semantic entailment from metadata alone",
                "causality or clinical utility from citation presence",
            ],
            next_required=[
                "retain the inspected passage and reviewer identity/method for each support annotation"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Triage citation entailment from reviewed annotations.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = audit(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
