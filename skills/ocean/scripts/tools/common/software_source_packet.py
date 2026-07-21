#!/usr/bin/env python3
"""Generic OCEAN software source-packet helper.

This helper is intentionally generic. It does not run bioinformatics software.
It turns inspected run metadata into a bounded OCEAN software source packet and
checks whether the required provenance fields are present.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


REQUIRED_FIELDS = [
    "tool_name",
    "tool_version",
    "task_intent",
    "command_line",
    "parameters",
    "reference_or_index",
    "input_files",
    "output_files",
    "logs_or_qc",
    "environment",
    "date",
]

DEFAULT_CANNOT_SUPPORT = [
    "biological mechanism",
    "causal conclusion",
    "clinical utility",
    "publication readiness",
    "reproducibility without rerun/log/environment checks",
]


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def today() -> str:
    return dt.date.today().isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def packet_id(tool_name: str, date: str, command_line: str) -> str:
    seed = f"{tool_name}|{date}|{command_line}".encode("utf-8")
    return "osp-software-" + hashlib.sha1(seed).hexdigest()[:12]


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]
    return [str(value)]


def audit_record(record: dict[str, Any]) -> tuple[list[str], list[str]]:
    missing = [field for field in REQUIRED_FIELDS if not record.get(field)]
    warnings = []
    boundary_status = record.get("boundary_status")
    if boundary_status in {"queried_evidence", "packet_evidence"} and missing:
        warnings.append("queried_evidence or packet_evidence requires complete provenance fields")
    elif boundary_status not in {None, "candidate_route", "queried_evidence", "packet_evidence"}:
        warnings.append("unknown software evidence boundary status")
    if record.get("supports_claims") and any("mechanism" in str(item).lower() for item in normalize_list(record.get("supports_claims"))):
        warnings.append("software output should not directly support mechanism claims")
    return missing, warnings


def make_packet(record: dict[str, Any]) -> dict[str, Any]:
    date = str(record.get("date") or today())
    tool_name = str(record.get("tool_name") or "unknown tool")
    command_line = str(record.get("command_line") or "")
    cannot_support = normalize_list(record.get("cannot_support")) or DEFAULT_CANNOT_SUPPORT
    missing, warnings = audit_record(record)
    inspected_fields = {
        "tool_name": "tool identity",
        "tool_version": "tool version",
        "task_intent": "task intent",
        "command_line": "command line",
        "parameters": "parameters",
        "reference_or_index": "reference/index",
        "input_files": "input file provenance",
        "output_files": "output file provenance",
        "logs_or_qc": "logs/QC",
        "environment": "environment boundary",
        "date": "execution date",
    }
    inspected_content = [label for field, label in inspected_fields.items() if record.get(field)]
    complete = not missing
    requested_boundary = record.get("boundary_status")
    if complete and requested_boundary in {"queried_evidence", "packet_evidence"}:
        boundary_status = requested_boundary
    elif complete and requested_boundary is None:
        boundary_status = "queried_evidence"
    else:
        boundary_status = "candidate_route"
    supports_claims = normalize_list(record.get("supports_claims")) if complete else []
    if complete and not supports_claims:
        supports_claims = ["software run identity and provenance"]
    return {
        "packet_id": record.get("packet_id") or packet_id(tool_name, date, command_line),
        "created_at": record.get("created_at") or now_iso(),
        "source_type": "bioinformatics_software_run",
        "resource": tool_name,
        "query": record.get("task_intent") or "software run provenance",
        "filters": {
            "adapter": "scripts/tools/common/software_source_packet.py",
            "tool_slug": record.get("tool_slug") or "",
        },
        "date_accessed": date,
        "identifiers": normalize_list(record.get("identifiers")),
        "inspected_content": inspected_content,
        "supports_claims": supports_claims,
        "cannot_support": cannot_support,
        "software_record": {field: record.get(field) for field in REQUIRED_FIELDS},
        "license_or_terms_note": record.get("license_or_terms_note") or "Check tool license, citation, and database/index terms before reuse.",
        "boundary_status": boundary_status,
        "handoff": record.get("handoff") or "Anchor",
        "provenance_audit": {
            "missing": missing,
            "warnings": warnings,
            "verdict": "pass" if complete else "needs_review",
        },
    }


def command_template(args: argparse.Namespace) -> int:
    template = {
        "tool_name": args.tool_name,
        "tool_slug": args.tool_slug or "",
        "tool_version": "",
        "task_intent": "",
        "command_line": "",
        "parameters": {},
        "reference_or_index": "",
        "input_files": [],
        "output_files": [],
        "logs_or_qc": [],
        "environment": "",
        "date": today(),
        "supports_claims": [],
        "cannot_support": DEFAULT_CANNOT_SUPPORT,
        "boundary_status": "candidate_route",
        "handoff": "Anchor",
    }
    write_json(args.output, template)
    print(f"Wrote {args.output}")
    return 0


def command_audit(args: argparse.Namespace) -> int:
    record = read_json(args.input)
    missing, warnings = audit_record(record)
    result = {
        "input": str(args.input),
        "missing": missing,
        "warnings": warnings,
        "verdict": "pass" if not missing else "needs_review",
    }
    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


def command_packet(args: argparse.Namespace) -> int:
    record = read_json(args.input)
    missing, _ = audit_record(record)
    packet = make_packet(record)
    write_json(args.output, packet)
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0 if not missing else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Create/audit generic OCEAN software source packets.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    template = sub.add_parser("template")
    template.add_argument("--tool-name", required=True)
    template.add_argument("--tool-slug", default="")
    template.add_argument("--output", type=Path, required=True)
    template.set_defaults(func=command_template)

    audit = sub.add_parser("audit")
    audit.add_argument("--input", type=Path, required=True)
    audit.add_argument("--output", type=Path, required=True)
    audit.set_defaults(func=command_audit)

    packet = sub.add_parser("packet")
    packet.add_argument("--input", type=Path, required=True)
    packet.add_argument("--output", type=Path, required=True)
    packet.set_defaults(func=command_packet)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
