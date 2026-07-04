#!/usr/bin/env python3
"""Run offline source-adapter evals for OCEAN."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run offline OCEAN source adapter evals.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args(argv)

    args.outdir.mkdir(parents=True, exist_ok=True)
    lit_script = args.skill_dir / "scripts" / "tools" / "literature" / "source_packet.py"
    ct_script = args.skill_dir / "scripts" / "tools" / "clinicaltrials" / "source_packet.py"

    lit_analysis = args.outdir / "literature-adapter-r1-analysis.json"
    lit_packet = args.outdir / "literature-adapter-r1-packet.json"
    ct_analysis = args.outdir / "clinicaltrials-adapter-r1-analysis.json"
    ct_packet = args.outdir / "clinicaltrials-adapter-r1-packet.json"

    run([
        sys.executable,
        str(lit_script),
        "analyze",
        "--input",
        str(args.skill_dir / "evals" / "literature-adapter-r1-mock-record.json"),
        "--resource",
        "mock literature record",
        "--query",
        "mock biomarker association",
        "--output",
        str(lit_analysis),
    ])
    run([sys.executable, str(lit_script), "packet", "--analysis", str(lit_analysis), "--output", str(lit_packet), "--handoff", "Sounding"])

    run([
        sys.executable,
        str(ct_script),
        "analyze",
        "--input",
        str(args.skill_dir / "evals" / "clinicaltrials-adapter-r1-mock-study.json"),
        "--output",
        str(ct_analysis),
    ])
    run([sys.executable, str(ct_script), "packet", "--analysis", str(ct_analysis), "--output", str(ct_packet), "--handoff", "Iceberg"])

    lit_packet_data = read_json(lit_packet)
    ct_packet_data = read_json(ct_packet)
    checks = {
        "literature_packet_exists": lit_packet.exists(),
        "literature_boundary_queried": lit_packet_data["boundary_status"] == "queried_evidence",
        "literature_refuses_full_methods": "full methods quality" in lit_packet_data["cannot_support"],
        "literature_handoff_sounding": lit_packet_data["handoff"] == "Sounding",
        "clinicaltrials_packet_exists": ct_packet.exists(),
        "clinicaltrials_boundary_queried": ct_packet_data["boundary_status"] == "queried_evidence",
        "clinicaltrials_refuses_efficacy": "treatment efficacy" in ct_packet_data["cannot_support"],
        "clinicaltrials_handoff_iceberg": ct_packet_data["handoff"] == "Iceberg",
    }
    passed = all(checks.values())
    summary = {
        "cases": 2,
        "pass": 2 if passed else sum(1 for value in checks.values() if value),
        "needs_review": 0 if passed else 1,
        "checks": checks,
    }
    (args.outdir / "source-adapters-r1-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.outdir / "source-adapters-r1-results.md").write_text(
        "\n".join(
            [
                "# OCEAN Source Adapters R1 Results",
                "",
                f"- Cases: {summary['cases']}",
                f"- Pass: {summary['pass']}",
                f"- Needs review: {summary['needs_review']}",
                "",
                "| Check | Result |",
                "|---|---|",
                *[f"| {key} | {value} |" for key, value in checks.items()],
                "",
                "## Evidence Boundary / 证据边界",
                "",
                "This eval uses local mock literature and ClinicalTrials.gov-style JSON only. It does not query PubMed, EuropePMC, ClinicalTrials.gov, or any external API. Passing means the adapters create bounded source packets; it does not mean abstracts prove full-paper claims or registry records prove efficacy.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
