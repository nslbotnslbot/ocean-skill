#!/usr/bin/env python3
"""Create a CSV template for scientific claim auditing."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

COLUMNS = [
    "id",
    "claim",
    "claim_type",
    "evidence_source",
    "evidence_type",
    "directness_1_to_5",
    "causality_1_to_5",
    "support_1_to_5",
    "novelty_status",
    "validation_status",
    "missing_validation",
    "risk",
    "suggested_rewrite",
]

EXAMPLE = {
    "id": "C1",
    "claim": "Model X discovers mechanism Y in disease Z.",
    "claim_type": "mechanism",
    "evidence_source": "Fig. 3 / Table S2",
    "evidence_type": "computational + literature",
    "directness_1_to_5": "3",
    "causality_1_to_5": "2",
    "support_1_to_5": "2",
    "novelty_status": "unclear",
    "validation_status": "not externally validated",
    "missing_validation": "external validation; perturbation experiment",
    "risk": "causal overstatement",
    "suggested_rewrite": "Model X prioritizes a hypothesis linking Y to disease Z.",
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="outputs/claim_table.csv", help="Output CSV path")
    parser.add_argument("--empty", action="store_true", help="Create only header without example row")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        if not args.empty:
            writer.writerow(EXAMPLE)
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
