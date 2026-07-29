#!/usr/bin/env python3
"""Generate an intentionally permissive baseline for OCEAN-Bench comparison."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from ocean_core import read_json, write_json


DEFAULTS = {
    "claim_support": "supported",
    "claim_downgrade": "unchanged",
    "citation_entailment": "supported_candidate",
    "evidence_independence": "independent",
    "leakage_detection": "not_detected_in_declared_identifiers",
    "validation_planning": "complete",
    "reproducibility": "complete",
    "negative_evidence": "lost",
    "long_horizon_consistency": "consistent",
    "evidence_diff": "unchanged_snapshot",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create optimistic baseline predictions.")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    cases = read_json(args.cases).get("cases", [])
    payload = {
        "condition": "optimistic-baseline",
        "predictions": {
            case["case_id"]: DEFAULTS[case["category"]]
            for case in cases
        },
        "boundary": "A deliberately permissive control, not a model result.",
    }
    write_json(args.output, payload)
    print(json.dumps({"predictions": len(payload["predictions"]), "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
