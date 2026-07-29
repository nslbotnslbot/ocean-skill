#!/usr/bin/env python3
"""Report circular evidence paths using the OCEAN independence engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))
DETECTOR_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(DETECTOR_ROOT))

from ocean_core import read_json, write_json
from evidence_independence import classify_graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect circular evidence paths.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = classify_graph(read_json(args.input))
    circular_pairs = [
        pair for pair in result["pairs"] if pair["classification"] == "circular"
    ]
    payload = {
        "schema_version": "ocean-circularity-report-v1",
        "circularity": "detected" if circular_pairs else (
            "unknown" if result["classification"] == "unknown" else "not_detected"
        ),
        "independence_classification": result["classification"],
        "circular_pairs": circular_pairs,
        "all_pairs": result["pairs"],
        "evidence_boundary": result["evidence_boundary"],
    }
    write_json(args.output, payload)
    print(json.dumps({"circularity": payload["circularity"], "pairs": len(circular_pairs)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
