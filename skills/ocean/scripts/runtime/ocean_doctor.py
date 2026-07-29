#!/usr/bin/env python3
"""Run a non-secret, non-destructive OCEAN environment readiness check."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
from urllib.parse import urlparse

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import now_utc, read_json, write_json
from runtime.environment_manager import build_environment_report


DEFAULT_CREDENTIALS = Path(__file__).with_name("credentials.example.json")
DEFAULT_LICENSES = SCRIPT_ROOT.parent / "licenses" / "registry.yaml"


def safe_credential_status(config: Path) -> list[dict]:
    names = read_json(config).get("credential_names", [])
    return [{"name": name, "present": bool(os.environ.get(name))} for name in names]


def tool_status() -> list[dict]:
    commands = ["pdftotext", "git", "Rscript", "docker", "snakemake", "nextflow"]
    return [
        {"command": command, "available": bool(shutil.which(command)), "path": shutil.which(command) or ""}
        for command in commands
    ]


def license_status(path: Path) -> dict:
    registry = read_json(path)
    resources = registry.get("resources", [])
    return {
        "registry_readable": True,
        "resource_notices": len(resources),
        "acknowledgement_required": sum(
            bool(item.get("acknowledgement_required")) for item in resources
        ),
    }


def endpoint_inventory() -> list[dict]:
    endpoints = [
        "https://eutils.ncbi.nlm.nih.gov",
        "https://clinicaltrials.gov",
        "https://www.ebi.ac.uk",
    ]
    return [
        {
            "host": urlparse(endpoint).hostname,
            "network_checked": False,
            "status": "not_checked",
        }
        for endpoint in endpoints
    ]


def build_report(args: argparse.Namespace) -> dict:
    environment = build_environment_report()
    credentials = safe_credential_status(args.credentials)
    tools = tool_status()
    warnings = list(environment["warnings"])
    if not environment["runtime"]["uv"]["available"]:
        warnings.append("uv is not available; use python3 fallback or install uv explicitly.")
    if not any(item["available"] for item in tools if item["command"] == "pdftotext"):
        warnings.append("pdftotext is unavailable; PDF ingest will try the optional pypdf package.")
    return {
        "schema_version": "ocean-doctor-report-v1",
        "checked_at": now_utc(),
        "runtime": environment["runtime"],
        "credentials": credentials,
        "tools": tools,
        "api_endpoints": endpoint_inventory(),
        "licenses": license_status(args.licenses),
        "network": {
            "checked": False,
            "reason": "Doctor is offline by default; live API access requires an explicit workflow command.",
        },
        "warnings": warnings,
        "ready_for_contract_workflows": bool(environment["runtime"]["python"]["available"]),
        "ready_for_all_external_workflows": False,
        "evidence_boundary": (
            "Environment discovery only. No secret value, API response, external tool analysis, "
            "license compliance, or scientific result was inspected."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OCEAN runtime readiness without exposing secrets.")
    parser.add_argument("--credentials", type=Path, default=DEFAULT_CREDENTIALS)
    parser.add_argument("--licenses", type=Path, default=DEFAULT_LICENSES)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    payload = build_report(args)
    if args.output:
        write_json(args.output, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
