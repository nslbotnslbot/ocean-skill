#!/usr/bin/env python3
"""Run deterministic OCEAN source-packet boundary evals."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import sys

from ocean_source_router import audit_packet, markdown_audit


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_case(case: dict) -> dict:
    missing, warnings = audit_packet(case["packet"])
    actual = "pass" if not missing else "fail"
    return {
        "id": case["id"],
        "expected": case["expect"],
        "actual": actual,
        "verdict": "pass" if actual == case["expect"] else "needs_review",
        "missing": missing,
        "warnings": warnings,
        "audit_markdown": markdown_audit(case["packet"], missing, warnings),
    }


def make_markdown(results: list[dict], summary: dict) -> str:
    lines = [
        "# OCEAN Source Packet Boundary R2 Results",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        "",
        "| Case | Expected | Actual | Verdict | Missing fields | Warnings |",
        "|---|---|---|---|---|---|",
    ]
    for row in results:
        lines.append(
            "| {id} | {expected} | {actual} | {verdict} | {missing} | {warnings} |".format(
                id=row["id"],
                expected=row["expected"],
                actual=row["actual"],
                verdict=row["verdict"],
                missing="; ".join(row["missing"] or ["None"]),
                warnings="; ".join(row["warnings"] or ["None"]),
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Complete software evidence packets must include software-specific provenance fields.",
            "- Candidate routes, missing inspected content, and software outputs without command/version/parameter provenance cannot be used as evidence.",
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval uses synthetic public-safe packets only. It does not inspect real software logs, private data, patient records, manuscripts, or live database/API responses.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run OCEAN source-packet boundary eval.")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args(argv)

    cases = read_json(args.cases)
    results = [run_case(case) for case in cases]
    summary = {
        "run_date": dt.date.today().isoformat(),
        "cases": len(results),
        "pass": sum(1 for row in results if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in results if row["verdict"] != "pass"),
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / "source-packet-boundary-r2-results.json", results)
    write_json(args.outdir / "source-packet-boundary-r2-summary.json", summary)
    (args.outdir / "source-packet-boundary-r2-results.md").write_text(
        make_markdown(results, summary),
        encoding="utf-8",
    )
    print(f"Wrote source-packet boundary eval artifacts to {args.outdir}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
