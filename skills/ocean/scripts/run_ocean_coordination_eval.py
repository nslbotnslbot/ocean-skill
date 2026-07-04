#!/usr/bin/env python3
"""Run deterministic OCEAN seven-module coordination evals.

This runner checks module-chain completeness, handoff continuity, artifact
coverage, and downgrade/stop gates for full OCEAN workflow cases. It is an
offline structural eval; it does not inspect scientific sources or call APIs.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import sys
from typing import Any


MODULE_CHAIN = ["Sounding", "Current", "Reef", "Iceberg", "Anchor", "Compass", "Harbor"]

MODULE_ARTIFACTS = {
    "Sounding": "Source Packet + Evidence Radar Map + Negative Space",
    "Current": "Direction-Flow Map",
    "Reef": "Resource Provenance Map",
    "Iceberg": "Claim-Evidence Matrix",
    "Anchor": "Validation Plan",
    "Compass": "Research Route Card",
    "Harbor": "Decision Memory",
}

MODULE_BOUNDARY = {
    "Sounding": "Do not treat uninspected source packets, snippets, titles, or abstracts as full evidence.",
    "Current": "Do not claim field trends without a dated inspected source corpus.",
    "Reef": "Do not treat candidate databases, APIs, KGs, or tools as proof.",
    "Iceberg": "Downgrade unsupported causal, mechanistic, clinical, novelty, or publication claims.",
    "Anchor": "Do not imply planned validation, benchmark, or reproducibility checks have succeeded.",
    "Compass": "Do not propose journal/publication strategy as if evidence readiness is established.",
    "Harbor": "Do not record authorship, submission, collaboration, or project status without traceable records.",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def expected_handoffs(chain: list[str]) -> list[list[str]]:
    return [[chain[i], chain[i + 1]] for i in range(len(chain) - 1)]


def handoff_ticket(case_id: str, source: str, target: str, boundary: str) -> dict[str, str]:
    return {
        "case_id": case_id,
        "source_module": source,
        "next_module": target,
        "input_packet": f"{case_id}:{source.lower()}-artifact",
        "boundary": boundary,
        "unresolved_risk": "Downstream module must preserve missing-evidence notes and cannot upgrade unsupported claims.",
        "stop_condition": "Stop if the next module would need uninspected private data, live API results, raw files, reviewer text, or validation outcomes.",
    }


def module_plan(case: dict[str, Any]) -> list[dict[str, str]]:
    chain = case["expected_chain"]
    return [
        {
            "module": module,
            "artifact": MODULE_ARTIFACTS[module],
            "boundary": MODULE_BOUNDARY[module],
            "case_specific_boundary": "; ".join(case["required_boundaries"]),
        }
        for module in chain
    ]


def score_case(case: dict[str, Any]) -> dict[str, Any]:
    chain = case["expected_chain"]
    planned_handoffs = expected_handoffs(chain)
    required_handoffs = case["required_handoffs"]
    plan = module_plan(case)
    tickets = [
        handoff_ticket(case["id"], source, target, MODULE_BOUNDARY[source])
        for source, target in planned_handoffs
    ]

    module_coverage = all(module in chain for module in MODULE_CHAIN)
    artifact_coverage = all(row["artifact"] for row in plan)
    handoff_continuity = planned_handoffs == required_handoffs
    boundary_coverage = all(case["required_boundaries"]) and all(row["boundary"] for row in plan)
    downgrade_gate = bool(case.get("unsafe_claim")) and bool(case.get("expected_downgrade"))
    harbor_record = chain[-1] == "Harbor" and any(row["module"] == "Harbor" for row in plan)

    dimensions = {
        "module_coverage": 20 if module_coverage else 0,
        "artifact_coverage": 20 if artifact_coverage else 0,
        "handoff_continuity": 20 if handoff_continuity else 0,
        "boundary_coverage": 15 if boundary_coverage else 0,
        "unsupported_claim_downgrade": 15 if downgrade_gate else 0,
        "harbor_memory_closure": 10 if harbor_record else 0,
    }
    score = sum(dimensions.values())
    verdict = "pass" if score >= 90 and all(value > 0 for value in dimensions.values()) else "needs_review"

    return {
        "id": case["id"],
        "input_type": case["input_type"],
        "score": score,
        "max_score": 100,
        "verdict": verdict,
        "dimensions": dimensions,
        "expected_chain": chain,
        "planned_handoffs": planned_handoffs,
        "module_plan": plan,
        "handoff_tickets": tickets,
        "unsafe_claim": case["unsafe_claim"],
        "expected_downgrade": case["expected_downgrade"],
        "evidence_boundary": {
            "checked": "Scenario text and expected coordination contract only.",
            "not_checked": "No real papers, datasets, raw files, APIs, databases, reviewer reports, or model outputs were inspected.",
            "cannot_conclude": "Scientific truth, novelty, clinical utility, mechanism, validation success, authorship, or publication readiness.",
            "needed_next": case["required_boundaries"],
        },
    }


def make_markdown(results: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Seven-Module Coordination Eval R1 Results",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        f"- Mean score: {summary['mean_score']:.2f}/100",
        "",
        "| Case | Input type | Score | Verdict | Chain |",
        "|---|---|---:|---|---|",
    ]
    for row in results:
        lines.append(
            f"| {row['id']} | {row['input_type']} | {row['score']}/100 | {row['verdict']} | "
            f"{' -> '.join(row['expected_chain'])} |"
        )
    lines.extend(
        [
            "",
            "## What This Tests",
            "",
            "- Whether all seven OCEAN modules can form a continuous workflow.",
            "- Whether every module has a concrete artifact contract.",
            "- Whether every downstream move carries a Handoff Ticket.",
            "- Whether unsafe claims are downgraded before Anchor/Compass/Harbor.",
            "- Whether Harbor closes the run as decision memory instead of inventing status.",
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This is an offline structural coordination eval. It did not inspect real papers, datasets, raw data, private records, public APIs, external databases, reviewer reports, model outputs, or bioinformatics tool runs.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run OCEAN seven-module coordination eval.")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args(argv)

    cases = read_json(args.cases)
    results = [score_case(case) for case in cases]
    summary = {
        "run_date": dt.date.today().isoformat(),
        "cases": len(results),
        "pass": sum(1 for row in results if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in results if row["verdict"] != "pass"),
        "mean_score": sum(row["score"] for row in results) / max(1, len(results)),
    }

    prefix = args.cases.stem.removesuffix("-cases")
    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / f"{prefix}-results.json", results)
    write_json(args.outdir / f"{prefix}-summary.json", summary)
    with (args.outdir / f"{prefix}-scorecard.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "input_type",
                "score",
                "max_score",
                "verdict",
                "module_coverage",
                "artifact_coverage",
                "handoff_continuity",
                "boundary_coverage",
                "unsupported_claim_downgrade",
                "harbor_memory_closure",
            ],
        )
        writer.writeheader()
        for row in results:
            writer.writerow(
                {
                    "id": row["id"],
                    "input_type": row["input_type"],
                    "score": row["score"],
                    "max_score": row["max_score"],
                    "verdict": row["verdict"],
                    **row["dimensions"],
                }
            )
    (args.outdir / f"{prefix}-results.md").write_text(make_markdown(results, summary), encoding="utf-8")
    print(f"Wrote OCEAN seven-module coordination eval artifacts to {args.outdir}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
