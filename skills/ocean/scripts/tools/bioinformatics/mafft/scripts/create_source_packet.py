#!/usr/bin/env python3
"""Create an OCEAN source packet for an inspected MAFFT run.

This wrapper does not install, call, or validate MAFFT. It converts a
completed run-record JSON into a bounded OCEAN software source packet.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def _find_tools_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        candidate = parent / "common" / "software_source_packet.py"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find scripts/tools/common/software_source_packet.py")


TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
sys.path.insert(0, str(TOOLS_ROOT / "common"))

from software_source_packet import audit_record, make_packet, read_json, write_json  # noqa: E402


TOOL_NAME = 'MAFFT'
TOOL_SLUG = 'mafft'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Create an OCEAN source packet for {TOOL_NAME}.")
    parser.add_argument("--input", type=Path, required=True, help="Inspected run-record JSON.")
    parser.add_argument("--output", type=Path, required=True, help="Output source-packet JSON.")
    args = parser.parse_args(argv)

    record = read_json(args.input)
    record.setdefault("tool_name", TOOL_NAME)
    record.setdefault("tool_slug", TOOL_SLUG)
    missing, warnings = audit_record(record)
    packet = make_packet(record)
    packet["filters"]["adapter"] = f"scripts/tools/bioinformatics/{TOOL_SLUG}/scripts/create_source_packet.py"
    packet["provenance_audit"] = {
        "missing": missing,
        "warnings": warnings,
        "verdict": "pass" if not missing else "needs_review",
    }
    write_json(args.output, packet)
    print(f"Wrote {args.output}")
    if missing:
        print("Missing required run-record fields: " + ", ".join(missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
