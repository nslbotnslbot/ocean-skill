#!/usr/bin/env python3
"""Check whether supplied claims resolve to locators in an OCEAN source map."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


NUMBER_RE = re.compile(r"(?<![A-Za-z])(?:\d+(?:\.\d+)?%?|\bp\s*[<=>]\s*0?\.\d+)", re.IGNORECASE)


def audit_claims(source_map: dict, claims_payload: dict) -> dict:
    known = set(source_map.get("locators", {}))
    rows = []
    for claim in claims_payload.get("claims", []):
        claim_id = claim.get("claim_id", "")
        text = claim.get("claim_text", "")
        locators = claim.get("source_locators", [])
        resolved = [locator for locator in locators if locator in known]
        unresolved = [locator for locator in locators if locator not in known]
        has_number = bool(NUMBER_RE.search(text))
        if unresolved:
            status = "unresolved_locator"
        elif not locators:
            status = "missing_locator"
        elif has_number and not resolved:
            status = "numeric_claim_ungrounded"
        else:
            status = "locator_resolved"
        rows.append(
            {
                "claim_id": claim_id,
                "status": status,
                "resolved_locators": resolved,
                "unresolved_locators": unresolved,
                "numeric_or_statistical_text_detected": has_number,
            }
        )
    failed = [row for row in rows if row["status"] != "locator_resolved"]
    return {
        "schema_version": "ocean-grounding-audit-v1",
        "paper_id": source_map["paper_id"],
        "locator_mode": source_map["locator_mode"],
        "claims": rows,
        "summary": {
            "total": len(rows),
            "resolved": len(rows) - len(failed),
            "needs_review": len(failed),
        },
        "evidence_boundary": evidence_boundary(
            inspected=["locator existence and numeric/statistical text markers"],
            not_inspected=["semantic entailment between claim and source text"],
            cannot_conclude=["that a resolved locator proves the claim"],
            next_required=[
                "inspect source excerpt and context for every claim",
                "run citation/scope or claim-evidence audit before publication",
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit claim-to-source locator grounding.")
    parser.add_argument("--source-map", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = audit_claims(read_json(args.source_map), read_json(args.claims))
    write_json(args.output, payload)
    print(json.dumps(payload["summary"], indent=2))
    return 0 if payload["summary"]["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
