#!/usr/bin/env python3
"""Normalize a structured study description into a Statistical Evidence Card."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ocean_core import read_json, write_json
from statistics_common import make_card, missing_fields


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an OCEAN Statistical Evidence Card.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = read_json(args.input)
    missing = missing_fields(payload)
    card = make_card(
        payload,
        issues=[],
        author_input=[f"provide {field}" for field in missing],
    )
    write_json(args.output, card)
    print(json.dumps({"status": card["status"], "missing": missing}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
