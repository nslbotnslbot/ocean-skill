#!/usr/bin/env python3
"""Build a compact locator index from an OCEAN PaperBundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, now_utc, read_json, write_json


def build_source_map(bundle: dict) -> dict:
    locators: dict[str, dict] = {}
    for block in bundle.get("blocks", []):
        for locator in block.get("locators", []):
            locators[locator] = {
                "block_id": block["block_id"],
                "text_checksum": block["text_checksum"],
                "excerpt": block["text"][:240],
            }
    for artifact_type in ("figures", "tables", "supplements"):
        for artifact in bundle.get(artifact_type, []):
            for locator in artifact.get("locators", []):
                locators.setdefault(locator, {}).setdefault("artifacts", []).append(
                    {
                        "artifact_type": artifact_type[:-1],
                        "source_block_id": artifact.get("source_block_id", ""),
                    }
                )
    return {
        "schema_version": "ocean-source-map-v1",
        "paper_id": bundle["paper_id"],
        "file_checksum": bundle["file_checksum"],
        "locator_mode": bundle["locator_mode"],
        "created_at": now_utc(),
        "locators": locators,
        "sections": bundle.get("sections", []),
        "figures": bundle.get("figures", []),
        "tables": bundle.get("tables", []),
        "supplements": bundle.get("supplements", []),
        "unresolved_regions": bundle.get("unresolved_regions", []),
        "evidence_boundary": evidence_boundary(
            inspected=["PaperBundle locator identifiers and excerpt checksums"],
            not_inspected=["claim truth or semantic entailment"],
            cannot_conclude=["that a locator supports a claim merely because it exists"],
            next_required=["link each claim to a locator and run the grounding auditor"],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an OCEAN source map.")
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = build_source_map(read_json(args.bundle))
    write_json(args.output, payload)
    print(json.dumps({"locators": len(payload["locators"]), "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
