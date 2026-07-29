#!/usr/bin/env python3
"""Map declared statistical evidence to a bounded claim verdict."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


def map_claim(payload: dict) -> dict:
    effect = payload.get("effect_estimate")
    uncertainty = payload.get("uncertainty")
    adjusted = payload.get("multiplicity_addressed")
    replicated = payload.get("independent_replication")
    claim_level = payload.get("claim_level", "association")
    issues = []
    if effect in (None, ""):
        issues.append("effect estimate missing")
    if uncertainty in (None, ""):
        issues.append("uncertainty missing")
    if adjusted is False:
        issues.append("multiplicity not addressed")
    if claim_level in {"causal", "mechanism", "clinical_utility"}:
        issues.append(f"statistical association alone cannot support {claim_level}")
    if not replicated:
        issues.append("independent replication not declared")
    verdict = "partially_supported" if not issues else "unsupported_at_requested_level"
    maximum = (
        payload.get("claim_text", "")
        if verdict == "partially_supported"
        else "association observed under the declared analysis, pending independent validation"
    )
    return {
        "schema_version": "ocean-statistical-claim-map-v1",
        "claim_id": payload.get("claim_id", ""),
        "requested_claim_level": claim_level,
        "verdict": verdict,
        "maximum_safe_claim": maximum,
        "issues": issues,
        "evidence_boundary": evidence_boundary(
            inspected=["declared effect, uncertainty, multiplicity, replication, and claim level"],
            not_inspected=["raw data and model implementation"],
            cannot_conclude=["causality, mechanism, or clinical utility from statistical significance"],
            next_required=issues or ["inspect raw analysis and substantive importance"],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Map statistical evidence to a claim ceiling.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = map_claim(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps({"verdict": result["verdict"], "issues": result["issues"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
