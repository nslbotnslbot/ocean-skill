#!/usr/bin/env python3
"""Export figure, table, and supplement caption records from a PaperBundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export caption records from a PaperBundle.")
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    bundle = read_json(args.bundle)
    payload = {
        "schema_version": "ocean-paper-artifact-index-v1",
        "paper_id": bundle["paper_id"],
        "locator_mode": bundle["locator_mode"],
        "figures": bundle.get("figures", []),
        "tables": bundle.get("tables", []),
        "supplements": bundle.get("supplements", []),
        "evidence_boundary": evidence_boundary(
            inspected=["caption-like text detected in extracted blocks"],
            not_inspected=["figure pixels", "table cell values", "supplement file contents"],
            cannot_conclude=["that a caption or referenced artifact supports a scientific claim"],
            next_required=["visually inspect each claim-relevant artifact and preserve its locator"],
        ),
    }
    write_json(args.output, payload)
    print(
        json.dumps(
            {
                "figures": len(payload["figures"]),
                "tables": len(payload["tables"]),
                "supplements": len(payload["supplements"]),
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
