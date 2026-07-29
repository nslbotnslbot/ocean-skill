#!/usr/bin/env python3
"""Validate explicit claim-to-citation links and source locators."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


def link(payload: dict) -> dict:
    claims = {item["claim_id"]: item for item in payload.get("claims", [])}
    citations = {item["citation_id"]: item for item in payload.get("citations", [])}
    rows = []
    for item in payload.get("links", []):
        claim_id = item.get("claim_id", "")
        citation_id = item.get("citation_id", "")
        locators = item.get("source_locators", [])
        issues = []
        if claim_id not in claims:
            issues.append("unknown claim_id")
        if citation_id not in citations:
            issues.append("unknown citation_id")
        if not locators:
            issues.append("no source locator")
        rows.append(
            {
                "claim_id": claim_id,
                "citation_id": citation_id,
                "source_locators": locators,
                "issues": issues,
                "status": "linked" if not issues else "needs_review",
            }
        )
    unlinked_claims = sorted(set(claims) - {row["claim_id"] for row in rows if row["status"] == "linked"})
    return {
        "schema_version": "ocean-citation-claim-links-v1",
        "links": rows,
        "unlinked_claims": unlinked_claims,
        "evidence_boundary": evidence_boundary(
            inspected=["identifier existence and locator presence"],
            not_inspected=["bibliographic accuracy and semantic support"],
            cannot_conclude=["that a linked citation entails the claim"],
            next_required=[
                *[f"link claim to inspected source: {item}" for item in unlinked_claims],
                "run citation scope and entailment audit",
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate claim-citation links.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = link(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps({"links": len(result["links"]), "unlinked_claims": result["unlinked_claims"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
