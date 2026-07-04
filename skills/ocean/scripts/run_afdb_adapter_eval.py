#!/usr/bin/env python3
"""Run offline AlphaFold DB adapter eval for OCEAN."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run offline AFDB adapter eval.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args(argv)

    script = args.skill_dir / "scripts" / "afdb_source_packet.py"
    metadata = args.skill_dir / "evals" / "afdb-adapter-r1-mock-metadata.json"
    pae = args.skill_dir / "evals" / "afdb-adapter-r1-mock-pae.json"
    analysis = args.outdir / "afdb-adapter-r1-analysis.json"
    packet = args.outdir / "afdb-adapter-r1-packet.json"
    args.outdir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            sys.executable,
            str(script),
            "analyze",
            "--metadata",
            str(metadata),
            "--pae",
            str(pae),
            "--uniprot",
            "PTEST1",
            "--output",
            str(analysis),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(script),
            "packet",
            "--analysis",
            str(analysis),
            "--output",
            str(packet),
            "--handoff",
            "Iceberg",
        ],
        check=True,
    )
    analysis_data = read_json(analysis)
    packet_data = read_json(packet)
    checks = {
        "analysis_exists": analysis.exists(),
        "packet_exists": packet.exists(),
        "plddt_available": analysis_data["plddt_summary"]["available"] is True,
        "pae_available": analysis_data["pae_summary"]["available"] is True,
        "boundary_status_packet_evidence": packet_data["boundary_status"] == "packet_evidence",
        "cannot_support_mechanism": "disease mechanism" in packet_data["cannot_support"],
        "handoff_iceberg": packet_data["handoff"] == "Iceberg",
    }
    passed = all(checks.values())
    summary = {
        "cases": 1,
        "pass": 1 if passed else 0,
        "needs_review": 0 if passed else 1,
        "checks": checks,
        "mean_plddt": analysis_data["plddt_summary"]["mean_plddt"],
        "mean_pae": analysis_data["pae_summary"]["mean_pae"],
    }
    (args.outdir / "afdb-adapter-r1-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.outdir / "afdb-adapter-r1-results.md").write_text(
        "\n".join(
            [
                "# OCEAN AlphaFold DB Adapter R1 Results",
                "",
                f"- Cases: {summary['cases']}",
                f"- Pass: {summary['pass']}",
                f"- Needs review: {summary['needs_review']}",
                f"- Mean pLDDT: {summary['mean_plddt']}",
                f"- Mean PAE: {summary['mean_pae']}",
                "",
                "## Checks",
                "",
                "| Check | Result |",
                "|---|---|",
                *[f"| {key} | {value} |" for key, value in checks.items()],
                "",
                "## Evidence Boundary / 证据边界",
                "",
                "This eval uses local mock AFDB-style metadata and PAE files only. It does not query AlphaFold DB and does not prove protein function, binding, mechanism, druggability, or clinical relevance.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
