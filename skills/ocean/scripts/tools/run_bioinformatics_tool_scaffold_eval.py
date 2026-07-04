#!/usr/bin/env python3
"""Validate OCEAN bioinformatics tool scaffold folders."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_FIELDS = {
    "name",
    "slug",
    "family",
    "maturity",
    "shared_helper",
    "evidence_level",
    "required_packet_fields",
    "cannot_support_alone",
}

REQUIRED_EXAMPLE_FIELDS = {
    "example_note",
    "tool_name",
    "tool_slug",
    "tool_family",
    "tool_version",
    "task_intent",
    "command_line",
    "parameters",
    "reference_or_index",
    "input_files",
    "output_files",
    "logs_or_qc",
    "environment",
    "date",
    "supports_claims",
    "cannot_support",
    "boundary_status",
    "handoff",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run bioinformatics tool scaffold eval.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args(argv)

    bio_root = args.skill_dir / "scripts" / "tools" / "bioinformatics"
    registry_path = bio_root / "registry.json"
    registry = read_json(registry_path)
    rows = []
    for item in registry:
        folder = bio_root / item["slug"]
        tool_json = folder / "tool.json"
        readme = folder / "README.md"
        example = folder / "examples" / "run-record.example.json"
        data = read_json(tool_json) if tool_json.exists() else {}
        example_data = read_json(example) if example.exists() else {}
        missing_fields = sorted(REQUIRED_FIELDS - set(data))
        missing_example_fields = sorted(REQUIRED_EXAMPLE_FIELDS - set(example_data))
        verdict = (
            "pass"
            if folder.exists()
            and tool_json.exists()
            and readme.exists()
            and example.exists()
            and not missing_fields
            and not missing_example_fields
            else "needs_review"
        )
        rows.append(
            {
                "slug": item["slug"],
                "name": item["name"],
                "folder_exists": folder.exists(),
                "tool_json_exists": tool_json.exists(),
                "readme_exists": readme.exists(),
                "example_exists": example.exists(),
                "missing_fields": missing_fields,
                "missing_example_fields": missing_example_fields,
                "shared_helper": data.get("shared_helper"),
                "verdict": verdict,
            }
        )

    summary = {
        "cases": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / "bioinformatics-tool-scaffold-r1-results.json", rows)
    write_json(args.outdir / "bioinformatics-tool-scaffold-r1-summary.json", summary)
    (args.outdir / "bioinformatics-tool-scaffold-r1-results.md").write_text(
        "\n".join(
            [
                "# OCEAN Bioinformatics Tool Scaffold R1 Results",
                "",
                f"- Cases: {summary['cases']}",
                f"- Pass: {summary['pass']}",
                f"- Needs review: {summary['needs_review']}",
                "",
                "| Tool | Folder | tool.json | README | Example | Verdict |",
                "|---|---|---|---|---|---|",
                *[
                    f"| {row['name']} | {row['folder_exists']} | {row['tool_json_exists']} | {row['readme_exists']} | {row['example_exists']} | {row['verdict']} |"
                    for row in rows
                ],
                "",
                "## Evidence Boundary / 证据边界",
                "",
                "This eval checks scaffold and example-record completeness only. It does not install, run, benchmark, or validate any bioinformatics software.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
