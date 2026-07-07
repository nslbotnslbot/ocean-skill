#!/usr/bin/env python3
"""Validate OCEAN bioinformatics wrapper readiness plans.

This eval checks whether readiness plans are structurally complete and retain
their evidence boundaries. It does not install tools or execute analyses.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


DEFAULT_PREFIX = "bioinformatics-wrapper-readiness-r1"

REQUIRED_FIELDS = {
    "schema_version",
    "tool",
    "current_ocean_state",
    "readiness_stage",
    "interface_layer",
    "smoke_command",
    "candidate_install_routes",
    "container_note",
    "minimal_fixture",
    "required_run_evidence",
    "expected_outputs",
    "stop_conditions",
    "source_packet_step",
    "handoff",
    "evidence_boundary",
    "readiness_score_0_10",
}

REQUIRED_RUN_EVIDENCE_MARKERS = {
    "tool version",
    "exact command",
    "parameters",
    "input file",
    "output file",
    "logs",
    "run date",
}

VALID_STAGES = {
    "stage_0_profile_needed",
    "stage_1_plan_ready_environment_missing",
    "stage_2_local_smoke_executed",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_plan(plan: dict[str, Any], artifacts_dir: Path) -> dict[str, Any]:
    slug = plan.get("tool", {}).get("slug", "")
    expected_artifact = artifacts_dir / f"{slug}-readiness-plan.json"
    missing_fields = sorted(REQUIRED_FIELDS - set(plan))
    evidence_text = " ".join(str(item) for item in plan.get("required_run_evidence", []))
    missing_evidence_markers = sorted(
        marker for marker in REQUIRED_RUN_EVIDENCE_MARKERS if marker.lower() not in evidence_text.lower()
    )
    routes = plan.get("candidate_install_routes", [])
    route_boundary_ok = bool(routes) and all("verify" in str(route).lower() for route in routes)
    boundary_text = str(plan.get("evidence_boundary", "")).lower()
    boundary_ok = "not installation" in boundary_text and "biological validation" in boundary_text
    smoke_ok = isinstance(plan.get("smoke_command"), list) and bool(plan.get("smoke_command"))
    stop_ok = isinstance(plan.get("stop_conditions"), list) and len(plan.get("stop_conditions")) >= 4
    stage_ok = plan.get("readiness_stage") in VALID_STAGES
    score = plan.get("readiness_score_0_10")
    score_ok = isinstance(score, int) and 0 <= score <= 10
    artifact_ok = expected_artifact.exists()
    issues = []
    if missing_fields:
        issues.append("missing_required_fields")
    if missing_evidence_markers:
        issues.append("missing_required_run_evidence_markers")
    if not route_boundary_ok:
        issues.append("candidate_install_routes_lack_verify_boundary")
    if not boundary_ok:
        issues.append("weak_evidence_boundary")
    if not smoke_ok:
        issues.append("missing_smoke_command")
    if not stop_ok:
        issues.append("weak_stop_conditions")
    if not stage_ok:
        issues.append("invalid_stage")
    if not score_ok:
        issues.append("invalid_score")
    if not artifact_ok:
        issues.append("missing_artifact")
    return {
        "slug": slug,
        "name": plan.get("tool", {}).get("name", ""),
        "stage": plan.get("readiness_stage", ""),
        "score": plan.get("readiness_score_0_10", ""),
        "artifact": str(expected_artifact),
        "missing_fields": missing_fields,
        "missing_evidence_markers": missing_evidence_markers,
        "route_boundary_ok": route_boundary_ok,
        "boundary_ok": boundary_ok,
        "smoke_ok": smoke_ok,
        "stop_ok": stop_ok,
        "stage_ok": stage_ok,
        "score_ok": score_ok,
        "artifact_ok": artifact_ok,
        "issues": issues,
        "verdict": "pass" if not issues else "needs_review",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Wrapper Readiness Eval R1",
        "",
        f"- Plans checked: {summary['plans_checked']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        "",
        "| Tool | Stage | Score | Verdict | Issues |",
        "|---|---|---:|---|---|",
    ]
    for row in rows:
        issues = ", ".join(row["issues"]) if row["issues"] else ""
        lines.append(f"| {row['name']} | {row['stage']} | {row['score']} | {row['verdict']} | {issues} |")
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval validates wrapper-readiness planning artifacts only. It does not install software, run tools, process data, benchmark methods, or validate biological conclusions.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate OCEAN bioinformatics wrapper readiness plans.")
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    args = parser.parse_args(argv)

    results_path = args.outdir / f"{args.prefix}-results.json"
    artifacts_dir = args.outdir / f"{args.prefix}-artifacts"
    plans = read_json(results_path)
    rows = [check_plan(plan, artifacts_dir) for plan in plans]
    summary = {
        "plans_checked": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "evidence_boundary": "Structural readiness-plan eval only; no software execution or scientific validation.",
    }
    write_json(args.outdir / f"{args.prefix}-eval-results.json", rows)
    write_json(args.outdir / f"{args.prefix}-eval-summary.json", summary)
    (args.outdir / f"{args.prefix}-eval-results.md").write_text(make_markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
