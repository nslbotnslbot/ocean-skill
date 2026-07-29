#!/usr/bin/env python3
"""Score whether evidence boundaries survive a declared multi-session trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from ocean_core import evidence_boundary, read_json, write_json


def score_trace(trace: dict) -> dict:
    sessions = trace.get("sessions", [])
    issues = []
    seen = set()
    prior_boundary: set[str] = set()
    prior_risks: set[str] = set()
    for index, session in enumerate(sessions, start=1):
        session_id = session.get("session_id", "")
        if not session_id:
            issues.append(f"session {index}: missing session_id")
        elif session_id in seen:
            issues.append(f"session {index}: duplicate session_id {session_id}")
        seen.add(session_id)
        current_boundary = set(session.get("cannot_conclude", []))
        current_risks = set(session.get("open_risks", []))
        resolutions = {
            item.get("item"): item
            for item in session.get("resolved_items", [])
            if item.get("item")
        }
        for item in sorted(prior_boundary - current_boundary):
            resolution = resolutions.get(item)
            if not resolution or not resolution.get("evidence_refs"):
                issues.append(
                    f"session {index}: evidence boundary was dropped without "
                    f"resolution evidence: {item}"
                )
        for item in sorted(prior_risks - current_risks):
            resolution = resolutions.get(item)
            if not resolution or not resolution.get("evidence_refs"):
                issues.append(
                    f"session {index}: open risk was dropped without "
                    f"resolution evidence: {item}"
                )
        if not session.get("ledger_head_checksum"):
            issues.append(f"session {index}: missing ledger_head_checksum")
        prior_boundary = current_boundary
        prior_risks = current_risks
    if len(sessions) < 2:
        issues.append("trace requires at least two sessions")
    return {
        "trace_id": trace.get("trace_id", ""),
        "sessions": len(sessions),
        "classification": "consistent" if not issues else "boundary_lost",
        "issues": issues,
    }


def score(payload: dict) -> dict:
    traces = [score_trace(trace) for trace in payload.get("traces", [])]
    return {
        "schema_version": "ocean-long-horizon-report-v1",
        "traces": traces,
        "summary": {
            "total": len(traces),
            "consistent": sum(
                trace["classification"] == "consistent" for trace in traces
            ),
            "boundary_lost": sum(
                trace["classification"] == "boundary_lost" for trace in traces
            ),
        },
        "evidence_boundary": evidence_boundary(
            inspected=[
                "declared session sequence, ledger checksums, unresolved boundaries, risks, and resolution references"
            ],
            not_inspected=[
                "referenced evidence content",
                "whether sessions were independent or actually executed",
            ],
            cannot_conclude=[
                "scientific correctness or real-world continuity from trace structure alone"
            ],
            next_required=[
                "verify ledger files, SourcePackets, RunManifests, and human resolutions"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score OCEAN multi-session traces.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = score(read_json(args.input))
    write_json(args.output, result)
    print(json.dumps({**result["summary"], "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
