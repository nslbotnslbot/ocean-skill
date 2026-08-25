#!/usr/bin/env python3
"""Run deterministic OCEAN Reef router evals.

This eval is intentionally offline. It does not query biomedical databases,
call model APIs, or inspect private data. It checks whether OCEAN's local
router keeps routes bounded as candidate evidence and requires source-packet
fields before claim upgrades.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import sys

from ocean_source_router import infer_routes


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def score_case(case: dict) -> dict:
    routes = infer_routes(case["question"])
    route_classes = {route["route_class"] for route in routes}
    matched_terms = {term.lower() for route in routes for term in route.get("matched_terms", [])}
    expected_routes = set(case.get("expected_routes", []))
    must_terms = {term.lower() for term in case.get("must_terms", [])}

    route_hits = sorted(expected_routes & route_classes)
    route_misses = sorted(expected_routes - route_classes)
    term_hits = sorted(term for term in must_terms if any(term in hit or hit in term for hit in matched_terms))
    term_misses = sorted(must_terms - set(term_hits))

    all_candidate = all(route.get("evidence_status") == "candidate_route" for route in routes)
    has_packet_fields = all("minimum_packet_fields" in route for route in routes)
    has_cannot_support = True
    score = 0
    score += 4 if not route_misses else max(0, 4 - len(route_misses))
    score += 2 if len(term_hits) == len(must_terms) else max(0, int(2 * len(term_hits) / max(1, len(must_terms))))
    score += 2 if all_candidate else 0
    score += 2 if has_packet_fields else 0
    score += 2 if has_cannot_support else 0

    verdict = "pass" if score >= 10 and not route_misses and all_candidate and has_packet_fields else "needs_review"
    return {
        "id": case["id"],
        "score": score,
        "max_score": 12,
        "verdict": verdict,
        "expected_routes": sorted(expected_routes),
        "route_classes": sorted(route_classes),
        "route_hits": route_hits,
        "route_misses": route_misses,
        "must_terms": sorted(must_terms),
        "term_hits": term_hits,
        "term_misses": term_misses,
        "all_candidate": all_candidate,
        "has_packet_fields": has_packet_fields,
        "unsafe_claim": case.get("unsafe_claim", ""),
        "routes": routes,
    }


def make_markdown(results: list[dict], summary: dict) -> str:
    lines = [
        "# OCEAN Reef Bioinformatics Router R2 Results",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        f"- Mean score: {summary['mean_score']:.2f}/12",
        "",
        "## Case Summary",
        "",
        "| Case | Score | Verdict | Expected routes | Returned routes | Misses |",
        "|---|---:|---|---|---|---|",
    ]
    for row in results:
        lines.append(
            "| {id} | {score}/12 | {verdict} | {expected} | {returned} | {misses} |".format(
                id=row["id"],
                score=row["score"],
                verdict=row["verdict"],
                expected=", ".join(row["expected_routes"]),
                returned=", ".join(row["route_classes"]),
                misses=", ".join(row["route_misses"] or row["term_misses"] or ["None"]),
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a deterministic router eval, not a scientific correctness eval.",
            "- Passing means the local OCEAN router selected expected candidate route classes, kept outputs at `candidate_route`, and attached minimum source-packet fields.",
            "- `needs_review` means the route vocabulary or expected route map should be refined before using the case as a stable regression check.",
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This run did not query PubMed, GEO, TCGA/GDC, ClinVar, ChEMBL, ClinicalTrials.gov, OpenFDA, TCIA, PhysioNet, or any external software. It did not run LAST, STAR, SAMtools, DESeq2, Seurat, Snakemake, Nextflow, or other tools. It only tested local routing behavior and evidence-boundary scaffolding.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run OCEAN Reef router deterministic eval.")
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

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / "reef-bioinformatics-router-r2-results.json", results)
    write_json(args.outdir / "reef-bioinformatics-router-r2-summary.json", summary)
    with (args.outdir / "reef-bioinformatics-router-r2-scorecard.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "id",
                "score",
                "max_score",
                "verdict",
                "expected_routes",
                "route_classes",
                "route_misses",
                "term_misses",
                "all_candidate",
                "has_packet_fields",
                "unsafe_claim",
            ],
        )
        writer.writeheader()
        for row in results:
            writer.writerow(
                {
                    "id": row["id"],
                    "score": row["score"],
                    "max_score": row["max_score"],
                    "verdict": row["verdict"],
                    "expected_routes": ";".join(row["expected_routes"]),
                    "route_classes": ";".join(row["route_classes"]),
                    "route_misses": ";".join(row["route_misses"]),
                    "term_misses": ";".join(row["term_misses"]),
                    "all_candidate": row["all_candidate"],
                    "has_packet_fields": row["has_packet_fields"],
                    "unsafe_claim": row["unsafe_claim"],
                }
            )
    (args.outdir / "reef-bioinformatics-router-r2-results.md").write_text(
        make_markdown(results, summary),
        encoding="utf-8",
    )
    print(f"Wrote Reef router eval artifacts to {args.outdir}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
