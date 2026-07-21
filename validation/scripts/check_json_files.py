#!/usr/bin/env python3
"""Validate every tracked-style JSON file in the repository tree."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()

    failures: list[str] = []
    checked = 0
    for path in sorted(args.root.rglob("*.json")):
        if ".git" in path.parts or "outputs" in path.parts:
            continue
        checked += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            failures.append(f"{path.relative_to(args.root)}: {exc}")

    if failures:
        print("\n".join(failures))
        return 1
    print(f"JSON validation passed: {checked} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
