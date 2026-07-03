#!/usr/bin/env python3
"""Offline structural checks for OCEAN routing and artifact contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


REQUIRED_REFERENCES = [
    "domain-lens.md",
    "data-tool-router.md",
    "module-artifact-contract.md",
    "output-contract.md",
    "module-handoff.md",
    "sounding.md",
    "current.md",
    "reef.md",
    "reef-biological-data-sources.md",
    "reef-api-adapters.md",
    "iceberg.md",
    "anchor.md",
    "compass.md",
    "harbor.md",
]

MODULE_ARTIFACT_TERMS = {
    "Sounding": ["Source Packet", "Evidence Radar Map", "Negative Space", "Handoff Ticket"],
    "Current": ["Direction-Flow Map", "trend", "missing-search"],
    "Reef": ["Resource Provenance Map", "evidence hierarchy", "circularity"],
    "Iceberg": ["Claim-Evidence Matrix", "support verdict", "Safe rewrite"],
    "Anchor": ["Validation Plan", "leakage", "reproducibility"],
    "Compass": ["Research Route Card", "evidence driver", "decision"],
    "Harbor": ["Decision Memory", "contribution boundary", "reuse"],
}

DOMAIN_CASE_KEYWORDS = {
    "Medical AI / clinical prediction": ["medical ai", "clinical prediction", "leaderboard", "hospital", "auc", "imaging"],
    "Biological AI / AI-for-biology": ["protein language model", "foundation model", "biological ai", "splice-impact"],
    "Clinical research": ["clinicaltrials", "trial", "treatment", "clinvar"],
    "Molecular / cellular biology": ["mechanism", "pathway", "cell"],
    "Omics / single-cell / spatial": ["scrna", "single-cell", "spatial", "geo", "atlas", "expression"],
    "Drug / target / therapeutic hypothesis": ["open targets", "target", "drug", "inhibiting", "treats"],
    "Knowledge graph / database / resource": ["knowledge graph", "kg", "database", "edge", "predicts", "prediction"],
    "Manuscript / review / proposal": ["review", "manuscript", "journal", "proposal"],
    "Collaboration / authorship boundary": ["authorship", "contribution", "collaboration"],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def classify_domain(text: str) -> str:
    lowered = text.lower()
    scores: list[tuple[int, str]] = []
    for domain, keywords in DOMAIN_CASE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in lowered)
        scores.append((score, domain))
    scores.sort(reverse=True)
    return scores[0][1] if scores and scores[0][0] > 0 else "unknown"


def check_required_references(skill_dir: Path) -> list[dict]:
    rows = []
    refs_dir = skill_dir / "references"
    skill_text = read_text(skill_dir / "SKILL.md")
    output_contract = read_text(refs_dir / "output-contract.md")
    module_handoff = read_text(refs_dir / "module-handoff.md")
    for filename in REQUIRED_REFERENCES:
        path = refs_dir / filename
        mentioned = filename in skill_text or filename in output_contract or filename in module_handoff
        rows.append({
            "check": "required_reference",
            "target": filename,
            "status": "pass" if path.exists() and mentioned else "fail",
            "exists": path.exists(),
            "mentioned": mentioned,
        })
    return rows


def check_artifact_contract(skill_dir: Path) -> list[dict]:
    contract = read_text(skill_dir / "references" / "module-artifact-contract.md")
    rows = []
    for module, terms in MODULE_ARTIFACT_TERMS.items():
        missing = [term for term in terms if term.lower() not in contract.lower()]
        rows.append({
            "check": "module_artifact_contract",
            "target": module,
            "status": "pass" if not missing else "fail",
            "missing_terms": missing,
        })
    return rows


def check_case_routing(cases_path: Path) -> list[dict]:
    cases = json.loads(read_text(cases_path)).get("cases", [])
    rows = []
    for case in cases:
        predicted = classify_domain(case["input"] + " " + case["title"])
        rows.append({
            "check": "domain_router_case",
            "target": case["id"],
            "status": "pass" if predicted == case["expected_domain"] else "review",
            "expected_domain": case["expected_domain"],
            "predicted_domain": predicted,
            "expected_first_module": case["expected_first_module"],
            "expected_stop_condition": case["expected_stop_condition"],
        })
    return rows


def write_markdown(rows: list[dict], out: Path) -> None:
    passed = sum(1 for row in rows if row["status"] == "pass")
    review = sum(1 for row in rows if row["status"] == "review")
    failed = sum(1 for row in rows if row["status"] == "fail")
    lines = [
        "# OCEAN Contract Check",
        "",
        f"- Total checks: {len(rows)}",
        f"- Pass: {passed}",
        f"- Review: {review}",
        f"- Fail: {failed}",
        "",
        "| Check | Target | Status | Detail |",
        "|---|---|---|---|",
    ]
    for row in rows:
        detail_parts = []
        for key, value in row.items():
            if key in {"check", "target", "status"}:
                continue
            if value in (None, "", []):
                continue
            detail_parts.append(f"{key}={value}")
        detail = "<br>".join(str(part).replace("|", "\\|") for part in detail_parts)
        lines.append(f"| {row['check']} | {row['target']} | {row['status']} | {detail} |")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Check OCEAN structural routing contracts.")
    parser.add_argument("--skill-dir", type=Path, default=repo_root / "skills" / "ocean")
    parser.add_argument(
        "--cases",
        type=Path,
        default=repo_root / "skills" / "ocean" / "evals" / "domain-router-big-experiment-r1-cases.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=repo_root / "outputs" / "ocean-contract-check.md",
    )
    args = parser.parse_args()

    rows: list[dict] = []
    rows.extend(check_required_references(args.skill_dir))
    rows.extend(check_artifact_contract(args.skill_dir))
    rows.extend(check_case_routing(args.cases))

    write_markdown(rows, args.out)
    failed = [row for row in rows if row["status"] == "fail"]
    review = [row for row in rows if row["status"] == "review"]
    print(json.dumps({
        "total": len(rows),
        "pass": sum(1 for row in rows if row["status"] == "pass"),
        "review": len(review),
        "fail": len(failed),
        "out": str(args.out),
    }, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
