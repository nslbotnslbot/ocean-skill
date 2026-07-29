#!/usr/bin/env python3
"""Convert a user-supplied reader/source map into an OCEAN PaperBundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    evidence_boundary,
    now_utc,
    read_json,
    schema_path,
    sha256_json,
    stable_id,
    validate_required_contract,
    write_json,
)


def convert(payload: dict) -> dict:
    source = payload.get("source", {})
    locators = payload.get("locators", [])
    unresolved = list(payload.get("unresolved_regions", []))
    blocks = []
    for index, item in enumerate(locators, start=1):
        text = item.get("text") or item.get("excerpt") or ""
        locator_values = item.get("locators") or [item.get("locator", f"block:{index}")]
        blocks.append(
            {
                "block_id": item.get("block_id", f"block-{index:05d}"),
                "text": text,
                "locators": locator_values,
                "text_checksum": sha256_json(text),
            }
        )
    mode = payload.get("locator_mode", "source-limited")
    checksum = source.get("checksum", "")
    if mode in {"page-grounded", "structure-grounded"} and not checksum:
        mode = "source-limited"
        unresolved.append(
            "External reader artifact lacked an original-source checksum; "
            "grounding was downgraded to source-limited."
        )
    return {
        "schema_version": "ocean-paper-bundle-v1",
        "paper_id": payload.get("paper_id") or stable_id("paper", source),
        "source": {
            "path": source.get("path", ""),
            "title": source.get("title", ""),
            "media_type": source.get("media_type", "application/json"),
        },
        "file_checksum": checksum,
        "locator_mode": mode,
        "sections": payload.get("sections", []),
        "blocks": blocks,
        "figures": payload.get("figures", []),
        "tables": payload.get("tables", []),
        "supplements": payload.get("supplements", []),
        "unresolved_regions": unresolved,
        "extraction": {
            "method": "external-reader-bridge",
            "created_at": now_utc(),
            "page_count": int(payload.get("page_count", 0)),
        },
        "evidence_boundary": evidence_boundary(
            inspected=["supplied reader artifact structure and locators"],
            not_inspected=["external reader implementation", "original file unless separately supplied"],
            cannot_conclude=["that transformed locators support claims"],
            next_required=["validate against the original source checksum and run grounding audit"],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bridge an external reader artifact to PaperBundle.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = convert(read_json(args.input))
    errors = validate_required_contract(
        result,
        schema_path(__file__, "paper_bundle.schema.json"),
    )
    if errors:
        raise SystemExit("PaperBundle validation failed: " + "; ".join(errors))
    write_json(args.output, result)
    print(json.dumps({"paper_id": result["paper_id"], "blocks": len(result["blocks"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
