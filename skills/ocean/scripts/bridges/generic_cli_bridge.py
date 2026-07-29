#!/usr/bin/env python3
"""Convert an inspected OCEAN CLI software record into SourcePacket v2 and RunManifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ocean_core import read_json, write_json
from scientific_tool_bridge import convert


def adapt_cli(payload: dict) -> dict:
    record = payload.get("software_record", payload)
    return {
        "source": {
            "source_type": "bioinformatics_software_run",
            "source_id": record.get("tool_slug", ""),
            "title": record.get("tool_name", ""),
            "version": record.get("tool_version", ""),
            "access_mode": "local",
        },
        "result": {
            "execution_status": record.get("execution_status", ""),
            "returncode": record.get("returncode"),
            "stdout_excerpt": record.get("stdout_excerpt", ""),
            "stderr_excerpt": record.get("stderr_excerpt", ""),
        },
        "provenance": {
            "task_intent": record.get("task_intent", ""),
            "created_at": record.get("created_at", record.get("date", "")),
            "status": record.get("execution_status", "partial"),
            "command": shlex.split(record.get("command_line", "")),
            "software": record.get("tool_name", ""),
            "software_version": record.get("tool_version", ""),
            "parameters": record.get("parameters", {}),
            "inputs": [{"path": path, "exists": True} for path in record.get("input_files", [])],
            "outputs": [{"path": path, "exists": True} for path in record.get("output_files", [])],
            "environment": {
                "python": "unknown",
                "platform": record.get("environment", "unknown"),
            },
            "logs": record.get("logs_or_qc", []),
            "checksum": "",
        },
        "supports_claims": record.get("supports_claims", []),
        "cannot_support": record.get("cannot_support", []),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bridge an OCEAN CLI run record.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--packet-output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path, required=True)
    args = parser.parse_args(argv)
    packet, manifest = convert(adapt_cli(read_json(args.input)))
    write_json(args.packet_output, packet)
    write_json(args.manifest_output, manifest)
    print(json.dumps({"packet_id": packet["packet_id"], "run_id": manifest["run_id"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
