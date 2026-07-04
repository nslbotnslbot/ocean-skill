#!/usr/bin/env python3
"""Run deterministic OCEAN end-to-end module routing evals.

This runner is offline and stdlib-only. It checks whether research scenarios
route to the expected OCEAN modules, candidate biomedical resources, required
artifacts, and stop conditions without treating routes as evidence.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import re
import sys

from ocean_source_router import infer_routes


MODULE_ARTIFACTS = {
    "Sounding": ["Source packet", "Evidence Radar Map", "Negative Space", "Handoff Ticket"],
    "Current": ["Trend Map", "Direction-flow Boundary", "Consensus-vs-Hype Notes"],
    "Reef": ["Resource Provenance Map", "Evidence Hierarchy", "API/Database Boundary", "Source Packet Audit"],
    "Iceberg": ["Surface Claim", "Support Level", "Hidden Risk", "Downgraded Safe Claim"],
    "Anchor": ["Validation Checklist", "Reproducibility Plan", "External-check Boundary"],
    "Compass": ["Evidence-based Idea Card", "Experiment Plan", "Strategy Route"],
    "Harbor": ["Decision Memo", "Evidence Boundary Ledger", "Contribution Boundary Record"],
}

MODULE_KEYWORDS = {
    "Sounding": ["paper", "manuscript", "proposal", "project", "study", "source", "literature", "preprint", "doi", "idea", "plan"],
    "Current": ["current", "trend", "recent", "literature", "field", "journal", "publication", "proposal", "project", "study", "idea", "plan"],
    "Reef": ["database", "resource", "kg", "cohort", "registry", "tool", "routing", "tcga", "geo", "mimic", "chembl", "clinvar"],
    "Iceberg": ["claim", "claims", "prove", "causal", "mechanism", "support", "ready", "readiness", "utility"],
    "Anchor": ["validation", "external validation", "benchmark", "calibration", "deployment", "reproducibility", "prospective"],
    "Compass": ["plan", "planning", "experiment", "strategy", "journal", "prioritization", "proposal"],
    "Harbor": ["record", "memory", "decision", "contribution", "collaboration", "submission", "report"],
}

STOP_CONDITIONS = {
    "Sounding": "Stop if no traceable source packet or only uninspected snippets exist.",
    "Current": "Stop before trend or consensus claims without a dated inspected source corpus.",
    "Reef": "Stop before treating candidate routes, APIs, databases, or tools as evidence.",
    "Iceberg": "Stop before causal, mechanistic, clinical, or publication-ready claims when support is only association, prediction, annotation, or route context.",
    "Anchor": "Stop before validation, reproducibility, benchmark fairness, or clinical readiness if required artifacts are named but not inspected.",
    "Compass": "Stop before journal strategy or polished research claims if evidence readiness is not established.",
    "Harbor": "Stop before recording authorship, submission, reviewer, or collaboration status without explicit traceable records.",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def word_hit(text: str, keyword: str) -> bool:
    keyword = keyword.lower()
    if " " in keyword or "-" in keyword or "/" in keyword:
        return keyword in text
    return re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", text) is not None


def infer_modules(text: str) -> list[str]:
    lowered = text.lower()
    hits = []
    for module, keywords in MODULE_KEYWORDS.items():
        if any(word_hit(lowered, keyword) for keyword in keywords):
            hits.append(module)
    if "Reef" not in hits and len(infer_routes(text)) > 1:
        hits.append("Reef")
    return [module for module in MODULE_ARTIFACTS if module in hits]


def artifact_plan(modules: list[str]) -> dict[str, dict[str, object]]:
    return {
        module: {
            "artifact": MODULE_ARTIFACTS[module],
            "stop_condition": STOP_CONDITIONS[module],
        }
        for module in modules
    }


def score_case(case: dict) -> dict:
    inferred_modules = infer_modules(case["scenario"])
    route_classes = sorted({route["route_class"] for route in infer_routes(case["scenario"])})
    expected_modules = case["expected_modules"]
    expected_routes = case["expected_routes"]

    module_misses = [module for module in expected_modules if module not in inferred_modules]
    route_misses = [route for route in expected_routes if route not in route_classes]
    plan = artifact_plan(inferred_modules)
    missing_artifacts = [module for module in expected_modules if module not in plan or not plan[module]["artifact"]]
    missing_stops = [module for module in expected_modules if module not in plan or not plan[module]["stop_condition"]]

    score = 0
    score += 4 if not module_misses else max(0, 4 - len(module_misses))
    score += 3 if not route_misses else max(0, 3 - len(route_misses))
    score += 3 if not missing_artifacts else max(0, 3 - len(missing_artifacts))
    score += 2 if not missing_stops else 0
    verdict = "pass" if score >= 11 and not module_misses and not route_misses and not missing_artifacts and not missing_stops else "needs_review"
    return {
        "id": case["id"],
        "score": score,
        "max_score": 12,
        "verdict": verdict,
        "expected_modules": expected_modules,
        "inferred_modules": inferred_modules,
        "module_misses": module_misses,
        "expected_routes": expected_routes,
        "route_classes": route_classes,
        "route_misses": route_misses,
        "missing_artifacts": missing_artifacts,
        "missing_stops": missing_stops,
        "unsafe_claim": case.get("unsafe_claim", ""),
        "artifact_plan": plan,
    }


def make_markdown(results: list[dict], summary: dict) -> str:
    lines = [
        "# OCEAN E2E Module Router R1 Results",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        f"- Mean score: {summary['mean_score']:.2f}/12",
        "",
        "| Case | Score | Verdict | Module misses | Route misses |",
        "|---|---:|---|---|---|",
    ]
    for row in results:
        lines.append(
            "| {id} | {score}/12 | {verdict} | {modules} | {routes} |".format(
                id=row["id"],
                score=row["score"],
                verdict=row["verdict"],
                modules=", ".join(row["module_misses"] or ["None"]),
                routes=", ".join(row["route_misses"] or ["None"]),
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This eval checks whether research scenarios produce the expected OCEAN module chain, route classes, artifacts, and stop conditions.",
            "- Passing does not mean the scientific claim is true. It means OCEAN kept the workflow evidence-bound and artifact-led.",
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This run is deterministic and offline. It did not inspect real papers, manuscripts, private data, patient records, public APIs, external databases, model outputs, or bioinformatics software runs.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run OCEAN E2E module routing eval.")
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
            fieldnames=["id", "score", "max_score", "verdict", "module_misses", "route_misses", "unsafe_claim"],
        )
        writer.writeheader()
        for row in results:
            writer.writerow(
                {
                    "id": row["id"],
                    "score": row["score"],
                    "max_score": row["max_score"],
                    "verdict": row["verdict"],
                    "module_misses": ";".join(row["module_misses"]),
                    "route_misses": ";".join(row["route_misses"]),
                    "unsafe_claim": row["unsafe_claim"],
                }
            )
    (args.outdir / f"{prefix}-results.md").write_text(make_markdown(results, summary), encoding="utf-8")
    print(f"Wrote OCEAN E2E eval artifacts to {args.outdir}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
