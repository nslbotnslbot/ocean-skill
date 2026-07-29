#!/usr/bin/env python3
"""Report reproducibility runtime options without installing software."""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
import shutil
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import now_utc, write_json


def build_environment_report() -> dict:
    uv = shutil.which("uv")
    python = shutil.which("python3") or sys.executable
    return {
        "schema_version": "ocean-environment-report-v1",
        "checked_at": now_utc(),
        "runtime": {
            "uv": {"available": bool(uv), "path": uv or ""},
            "python": {
                "available": bool(python),
                "path": python or "",
                "version": platform.python_version(),
            },
            "git": {"available": bool(shutil.which("git")), "path": shutil.which("git") or ""},
        },
        "recommended_command": (
            "uv run skills/ocean/scripts/ocean.py doctor"
            if uv
            else "python3 skills/ocean/scripts/ocean.py doctor"
        ),
        "warnings": [
            "No dependency installation was attempted.",
            "A runtime check is not proof that a scientific workflow is reproducible.",
        ],
        "evidence_boundary": "Runtime discovery only; packages, APIs, reference data, and analyses were not executed.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect OCEAN runtime options.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    payload = build_environment_report()
    if args.output:
        write_json(args.output, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
