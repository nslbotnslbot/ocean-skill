#!/usr/bin/env python3
"""Check whether citation context matches claim species, tissue, disease, and evidence level."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


CONTEXT_FIELDS = ["species", "tissue", "disease", "cell_type", "intervention", "outcome"]
LEVEL_ORDER = {
    "metadata": 0,
    "abstract": 1,
    "full_text": 2,
    "primary_data": 3,
    "independent_replication": 4,
}
CLAIM_MINIMUM = {
    "descriptive": 1,
    "association": 2,
    "technical_performance": 3,
    "causal": 4,
    "mechanism": 4,
    "clinical_utility": 4,
}


def check_pair(item: dict) -> dict:
    claim = item.get("claim", {})
    citation = item.get("citation", {})
    mismatches = []
    unknown = []
    for field in CONTEXT_FIELDS:
        claim_value = claim.get(field)
        citation_value = citation.get(field)
        if claim_value and citation_value and str(claim_value).casefold() != str(citation_value).casefold():
            mismatches.append(field)
        elif claim_value and not citation_value:
            unknown.append(field)
    claim_type = claim.get("claim_type", "descriptive")
    source_level = LEVEL_ORDER.get(citation.get("evidence_level", "metadata"), 0)
    required_level = CLAIM_MINIMUM.get(claim_type, 2)
    level_sufficient = source_level >= required_level
    if mismatches:
        status = "scope_mismatch"
    elif unknown or not level_sufficient:
        status = "scope_incomplete"
    else:
        status = "scope_compatible"
    return {
        "claim_id": claim.get("claim_id", ""),
        "citation_id": citation.get("citation_id", ""),
        "status": status,
        "context_mismatches": mismatches,
        "unknown_context": unknown,
        "evidence_level": citation.get("evidence_level", "metadata"),
        "minimum_level_for_claim": required_level,
        "level_sufficient": level_sufficient,
    }


def audit(payload: dict) -> dict:
    rows = [check_pair(item) for item in payload.get("pairs", [])]
    return {
        "schema_version": "ocean-citation-scope-audit-v1",
        "pairs": rows,
        "summary": {
            "total": len(rows),
            "compatible": sum(row["status"] == "scope_compatible" for row in rows),
            "needs_review": sum(row["status"] != "scope_compatible" for row in rows),
        },
        "evidence_boundary": evidence_boundary(
            inspected=["declared context fields and evidence-level labels"],
            not_inspected=["full semantic entailment or source truth"],
            cannot_conclude=["claim support solely from compatible metadata"],
            next_required=["inspect the cited passage and primary evidence for every claim"],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit citation scope compatibility.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = audit(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
