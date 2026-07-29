#!/usr/bin/env python3
"""Compare two OCEAN-Bench reports without overstating significance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from ocean_core import read_json, write_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare benchmark reports.")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    baseline = read_json(args.baseline)
    candidate = read_json(args.candidate)
    if baseline["cases"] != candidate["cases"]:
        raise SystemExit("Reports cover different numbers of cases")
    payload = {
        "schema_version": "ocean-benchmark-comparison-v1",
        "baseline": baseline["condition"],
        "candidate": candidate["condition"],
        "cases": candidate["cases"],
        "accuracy_delta": round(candidate["accuracy"] - baseline["accuracy"], 6),
        "macro_f1_delta": round(candidate["macro_f1"] - baseline["macro_f1"], 6),
        "unsupported_strong_claim_error_delta": (
            candidate["unsupported_strong_claim_errors"]
            - baseline["unsupported_strong_claim_errors"]
        ),
        "boundary": (
            "Descriptive difference only. No confidence interval, significance, model "
            "generalization, or scientific-performance claim is implied."
        ),
    }
    write_json(args.output, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
