#!/usr/bin/env python3
"""Audit data/code/model availability metadata without inventing identifiers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


PLACEHOLDER_RE = re.compile(r"(todo|tbd|placeholder|xxx|accession_here|doi_here)", re.IGNORECASE)


def audit_asset(asset: dict) -> dict:
    access = asset.get("access", "unknown")
    required = ["asset_id", "asset_type", "access", "license"]
    if access == "public":
        required.extend(["repository", "identifier"])
    if access == "controlled":
        required.extend(["repository", "access_procedure", "restriction_reason"])
    if access == "third_party":
        required.extend(["source", "terms_url"])
    missing = [field for field in required if not asset.get(field)]
    placeholders = [
        field
        for field, value in asset.items()
        if isinstance(value, str) and PLACEHOLDER_RE.search(value)
    ]
    return {
        "asset_id": asset.get("asset_id", ""),
        "asset_type": asset.get("asset_type", ""),
        "access": access,
        "missing_fields": missing,
        "placeholder_fields": placeholders,
        "status": "needs_input" if missing or placeholders else "metadata_complete",
    }


def build_statement(assets: list[dict], rows: list[dict]) -> str:
    if any(row["status"] != "metadata_complete" for row in rows):
        return (
            "AUTHOR_INPUT_NEEDED: availability metadata is incomplete. "
            "Do not insert repository identifiers, accessions, DOIs, licenses, "
            "or access procedures until they are confirmed."
        )
    sentences = []
    for asset in assets:
        if asset["access"] == "public":
            sentences.append(
                f"{asset['asset_type']} {asset['asset_id']} is available from "
                f"{asset['repository']} under identifier {asset['identifier']}."
            )
        elif asset["access"] == "controlled":
            sentences.append(
                f"{asset['asset_type']} {asset['asset_id']} is available through "
                f"{asset['repository']} under controlled access; {asset['access_procedure']}."
            )
        elif asset["access"] == "included":
            sentences.append(f"{asset['asset_type']} {asset['asset_id']} is included with the article or supplement.")
        else:
            sentences.append(
                f"{asset['asset_type']} {asset['asset_id']} follows the declared {asset['access']} access route."
            )
    return " ".join(sentences)


def audit(payload: dict) -> dict:
    assets = payload.get("assets", [])
    rows = [audit_asset(asset) for asset in assets]
    missing_categories = [
        category
        for category in ("data", "code", "model", "prompt", "environment")
        if not any(asset.get("asset_type") == category for asset in assets)
    ]
    issues = [
        f"{row['asset_id'] or '<unnamed>'}: missing {', '.join(row['missing_fields'])}"
        for row in rows
        if row["missing_fields"]
    ]
    issues.extend(
        f"{row['asset_id'] or '<unnamed>'}: unresolved placeholders in {', '.join(row['placeholder_fields'])}"
        for row in rows
        if row["placeholder_fields"]
    )
    return {
        "schema_version": "ocean-availability-audit-v1",
        "assets": rows,
        "missing_categories": missing_categories,
        "issues": issues,
        "draft_statement": build_statement(assets, rows),
        "reproducibility_capsule": {
            "data_dictionary_declared": bool(payload.get("data_dictionary")),
            "source_data_declared": bool(payload.get("source_data")),
            "environment_lock_declared": any(
                asset.get("asset_type") == "environment" and asset.get("identifier")
                for asset in assets
            ),
            "random_seed_policy": payload.get("random_seed_policy", ""),
        },
        "evidence_boundary": evidence_boundary(
            inspected=["declared asset metadata and placeholder patterns"],
            not_inspected=["repository existence", "file contents", "license compatibility", "access approval"],
            cannot_conclude=["FAIR compliance or reproducibility from statements alone"],
            next_required=issues
            + [f"declare availability for {category}" for category in missing_categories],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit data, code, model, and prompt availability metadata.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = audit(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps({"issues": len(result["issues"]), "missing_categories": result["missing_categories"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
