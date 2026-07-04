#!/usr/bin/env python3
"""ClinicalTrials.gov source-packet helper for OCEAN."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def command_fetch(args: argparse.Namespace) -> int:
    if args.nct_id:
        url = f"https://clinicaltrials.gov/api/v2/studies/{urllib.parse.quote(args.nct_id)}"
    else:
        params = urllib.parse.urlencode({"query.term": args.query, "pageSize": args.page_size})
        url = f"https://clinicaltrials.gov/api/v2/studies?{params}"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    args.output.write_bytes(data)
    print(json.dumps({"url": url, "path": str(args.output), "bytes": len(data)}, indent=2))
    return 0


def module(record: dict, name: str) -> dict:
    protocol = record.get("protocolSection", {})
    return protocol.get(name, {}) if isinstance(protocol, dict) else {}


def normalize_study(raw) -> dict:
    if isinstance(raw, dict) and "studies" in raw:
        studies = raw.get("studies", [])
        raw = studies[0] if studies else raw
    if not isinstance(raw, dict):
        return {"raw_type": type(raw).__name__}
    ident = module(raw, "identificationModule")
    status = module(raw, "statusModule")
    design = module(raw, "designModule")
    conditions = module(raw, "conditionsModule")
    arms = module(raw, "armsInterventionsModule")
    outcomes = module(raw, "outcomesModule")
    results = raw.get("resultsSection", {}) if isinstance(raw, dict) else {}
    return {
        "nct_id": ident.get("nctId") or raw.get("nctId") or "",
        "brief_title": ident.get("briefTitle") or raw.get("briefTitle") or "",
        "overall_status": status.get("overallStatus") or raw.get("overallStatus") or "",
        "phase": design.get("phases") or raw.get("phase") or [],
        "study_type": design.get("studyType") or "",
        "conditions": conditions.get("conditions") or [],
        "interventions": [item.get("name", "") for item in arms.get("interventions", []) if isinstance(item, dict)],
        "primary_outcomes": [item.get("measure", "") for item in outcomes.get("primaryOutcomes", []) if isinstance(item, dict)],
        "has_results_section": bool(results),
        "raw_top_keys": sorted(raw.keys()),
    }


def command_analyze(args: argparse.Namespace) -> int:
    raw = read_json(args.input)
    study = normalize_study(raw)
    inspected = ["registry identity/status/design fields"]
    if study.get("primary_outcomes"):
        inspected.append("primary outcome fields")
    if study.get("has_results_section"):
        inspected.append("results section presence")
    analysis = {
        "created_at": now_iso(),
        "resource": "ClinicalTrials.gov",
        "study": study,
        "inspected_content": inspected,
        "supports_claims": [
            "trial registration existence",
            "registry status/design/outcome metadata",
        ],
        "cannot_support": [
            "treatment efficacy",
            "safety superiority",
            "clinical guideline readiness",
            "causal treatment effect",
            "peer-reviewed trial interpretation",
        ],
    }
    write_json(args.output, analysis)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
    return 0


def command_packet(args: argparse.Namespace) -> int:
    analysis = read_json(args.analysis)
    study = analysis["study"]
    packet = {
        "packet_id": f"osp-clinicaltrials-{study.get('nct_id') or 'unknown'}-{dt.date.today().isoformat()}",
        "created_at": now_iso(),
        "source_type": "clinical_registry_record",
        "resource": "ClinicalTrials.gov",
        "query": f"ClinicalTrials.gov registry record for {study.get('nct_id') or 'unknown NCT'}",
        "filters": {"adapter": "scripts/tools/clinicaltrials/source_packet.py"},
        "date_accessed": dt.date.today().isoformat(),
        "identifiers": [study.get("nct_id")] if study.get("nct_id") else [],
        "inspected_content": analysis.get("inspected_content", []),
        "supports_claims": analysis.get("supports_claims", []),
        "cannot_support": analysis.get("cannot_support", []),
        "license_or_terms_note": "Check ClinicalTrials.gov terms before reuse.",
        "boundary_status": "queried_evidence",
        "handoff": args.handoff,
    }
    write_json(args.output, packet)
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ClinicalTrials.gov source-packet helper for OCEAN.")
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("--nct-id", default="")
    fetch.add_argument("--query", default="")
    fetch.add_argument("--page-size", default="5")
    fetch.add_argument("--output", type=Path, required=True)
    fetch.set_defaults(func=command_fetch)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("--input", type=Path, required=True)
    analyze.add_argument("--output", type=Path, required=True)
    analyze.set_defaults(func=command_analyze)
    packet = sub.add_parser("packet")
    packet.add_argument("--analysis", type=Path, required=True)
    packet.add_argument("--output", type=Path, required=True)
    packet.add_argument("--handoff", default="Iceberg", choices=["Reef", "Iceberg", "Anchor", "Compass", "Harbor", "stop"])
    packet.set_defaults(func=command_packet)
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
