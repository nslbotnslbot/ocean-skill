#!/usr/bin/env python3
"""Build an OCEAN bioinformatics tool capability matrix.

The matrix joins three bounded evidence layers:

- the static bioinformatics registry;
- per-tool API/source-packet contracts;
- optional local real-tool smoke-eval results.

It does not install tools, run biological analyses, download databases, or
validate scientific claims.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import datetime as dt
import json
from pathlib import Path
import sys
from typing import Any


DEFAULT_SMOKE_RESULTS = "bioinformatics-real-tool-smoke-r1-results.json"

PRIORITY_SLUGS = [
    "fastqc",
    "multiqc",
    "cutadapt",
    "fastp",
    "samtools",
    "bcftools",
    "bedtools",
    "blast",
    "mafft",
    "hmmer",
    "minimap2",
    "deseq2",
    "edger",
    "limma_voom",
    "seurat",
    "dada2",
    "snakemake",
    "nextflow",
    "docker",
    "singularity_apptainer",
]


def read_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_smoke_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows = read_json(path, default=[])
    return {row["slug"]: row for row in rows}


def capability_tier(tool: dict[str, Any], api: dict[str, Any]) -> str:
    maturity = str(tool.get("maturity", api.get("maturity", ""))).lower()
    if "l2" in maturity or "l3" in maturity or "adapter" in maturity:
        return "source_packet_adapter"
    interface_type = api.get("interface_type")
    if interface_type == "provenance_to_source_packet":
        return "source_packet_scaffold"
    return "metadata_scaffold"


def local_status(smoke: dict[str, Any] | None) -> tuple[str, str, str]:
    if not smoke:
        return ("not_smoke_checked", "unknown", "")
    attempts = smoke.get("attempts") or []
    entrypoint = ""
    if attempts:
        entrypoint = str(attempts[0].get("entrypoint", ""))
    return (
        str(smoke.get("verdict", "unknown")),
        str(smoke.get("best_interface", "unknown")),
        entrypoint,
    )


def recommended_action(
    tool: dict[str, Any],
    api: dict[str, Any],
    smoke: dict[str, Any] | None,
    tier: str,
    status: str,
) -> str:
    slug = tool["slug"]
    if status == "executed":
        if tier == "source_packet_adapter":
            return "Promote with real inspected files next; keep adapter outputs bounded by source-packet limitations."
        return "Create a real run record from inspected files, then convert it into an OCEAN software source packet."
    if tier == "source_packet_adapter":
        return "Run the dedicated adapter with real inspected source files when available; do not infer missing biological claims."
    if slug in PRIORITY_SLUGS:
        return "High-priority practical wrapper candidate: add install/container notes and a focused smoke fixture before promising execution."
    interface = str((smoke or {}).get("best_interface", ""))
    if interface in {"cli", "python_import", "r_package"}:
        return "Environment-dependent tool: document installation/container requirements, then rerun real-tool smoke eval."
    return "Keep as scaffold until a real local tool, container, workflow record, or inspected output is available."


def build_rows(skill_dir: Path, smoke_results: Path) -> list[dict[str, Any]]:
    bio_root = skill_dir / "scripts" / "tools" / "bioinformatics"
    registry = read_json(bio_root / "registry.json", default=[])
    smoke_by_slug = load_smoke_rows(smoke_results)
    rows = []
    for tool in registry:
        folder = bio_root / tool["slug"]
        api = read_json(folder / "api.json", default={})
        smoke = smoke_by_slug.get(tool["slug"])
        tier = capability_tier(tool, api)
        status, best_interface, entrypoint = local_status(smoke)
        output_contract = api.get("output_contract") if isinstance(api.get("output_contract"), dict) else {}
        execution_contract = api.get("execution_contract") if isinstance(api.get("execution_contract"), dict) else {}
        rows.append(
            {
                "slug": tool["slug"],
                "name": tool["name"],
                "family": tool["family"],
                "maturity": tool.get("maturity", api.get("maturity", "")),
                "capability_tier": tier,
                "local_smoke_status": status,
                "best_interface": best_interface,
                "entrypoint": entrypoint,
                "api_contract": bool(api),
                "python_wrapper": api.get("python_wrapper", "scripts/create_source_packet.py"),
                "handoff": output_contract.get("handoff", "Anchor"),
                "requires_availability_smoke": bool(
                    execution_contract.get("availability_smoke_required_before_execution_claim", True)
                ),
                "real_run_required": bool(execution_contract.get("real_run_record_required_before_evidence_packet", True)),
                "next_action": recommended_action(tool, api, smoke, tier, status),
                "evidence_boundary": "Capability matrix only; not installation, end-to-end analysis, benchmark, or biological validation.",
            }
        )
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_status = Counter(row["local_smoke_status"] for row in rows)
    by_tier = Counter(row["capability_tier"] for row in rows)
    by_family: dict[str, dict[str, int]] = defaultdict(lambda: {"tools": 0, "executed": 0, "adapters": 0, "scaffolds": 0})
    for row in rows:
        fam = by_family[row["family"]]
        fam["tools"] += 1
        if row["local_smoke_status"] == "executed":
            fam["executed"] += 1
        if row["capability_tier"] == "source_packet_adapter":
            fam["adapters"] += 1
        if row["capability_tier"].endswith("scaffold"):
            fam["scaffolds"] += 1
    return {
        "run_date": dt.date.today().isoformat(),
        "tools": len(rows),
        "local_smoke_status": dict(sorted(by_status.items())),
        "capability_tier": dict(sorted(by_tier.items())),
        "families": dict(sorted(by_family.items())),
        "evidence_boundary": "Capability matrix joins registry/API/smoke metadata only; it does not prove tool execution capability beyond recorded smoke results.",
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "slug",
        "name",
        "family",
        "maturity",
        "capability_tier",
        "local_smoke_status",
        "best_interface",
        "entrypoint",
        "handoff",
        "requires_availability_smoke",
        "real_run_required",
        "next_action",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    family_lines = [
        "| Family | Tools | Executed locally | Source-packet adapters | Scaffolds |",
        "|---|---:|---:|---:|---:|",
    ]
    for family, data in summary["families"].items():
        family_lines.append(
            f"| {family} | {data['tools']} | {data['executed']} | {data['adapters']} | {data['scaffolds']} |"
        )

    priority_rows = [row for row in rows if row["slug"] in PRIORITY_SLUGS]
    priority_lines = [
        "| Tool | Family | Local status | Interface | Next action |",
        "|---|---|---|---|---|",
    ]
    for row in priority_rows:
        priority_lines.append(
            f"| {row['name']} | {row['family']} | {row['local_smoke_status']} | {row['best_interface']} | {row['next_action']} |"
        )

    matrix_lines = [
        "| Tool | Family | Tier | Local status | Interface | Handoff |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        matrix_lines.append(
            f"| {row['name']} | {row['family']} | {row['capability_tier']} | {row['local_smoke_status']} | {row['best_interface']} | {row['handoff']} |"
        )

    return "\n".join(
        [
            "# OCEAN Bioinformatics Capability Matrix R1",
            "",
            f"- Run date: {summary['run_date']}",
            f"- Tools indexed: {summary['tools']}",
            f"- Capability tiers: `{json.dumps(summary['capability_tier'], sort_keys=True)}`",
            f"- Local smoke status: `{json.dumps(summary['local_smoke_status'], sort_keys=True)}`",
            "",
            "## What This Matrix Means",
            "",
            "This matrix joins OCEAN's static tool registry, per-tool API/source-packet contracts, and the latest local real-tool smoke results. It is a planning artifact for tool coverage and implementation priority.",
            "",
            "It does not install software, run omics analyses, download databases, benchmark tools, or validate biological conclusions.",
            "",
            "## Family Summary",
            "",
            *family_lines,
            "",
            "## Practical Wrapper Priorities",
            "",
            "These are high-utility tools where OCEAN should next add stronger install/container notes, focused smoke fixtures, or dedicated wrappers before claiming execution support.",
            "",
            *priority_lines,
            "",
            "## Full Matrix",
            "",
            *matrix_lines,
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "- `executed` means the current local environment produced a bounded smoke result only.",
            "- `not_available_current_environment` means the scaffold may be useful, but local execution is not available until the tool/package/container is installed.",
            "- `source_packet_scaffold` means OCEAN can packetize inspected run metadata, not run the underlying scientific tool.",
            "- `source_packet_adapter` means a narrower adapter exists, but its outputs still need source-specific evidence boundaries.",
            "- This matrix must not be used as evidence of mechanism, causality, clinical utility, reproducibility, or publication readiness.",
        ]
    ) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build OCEAN bioinformatics capability matrix.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--smoke-results", type=Path)
    args = parser.parse_args(argv)

    smoke_results = args.smoke_results or args.outdir / DEFAULT_SMOKE_RESULTS
    rows = build_rows(args.skill_dir, smoke_results)
    summary = summarize(rows)
    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / "bioinformatics-capability-matrix-r1-results.json", rows)
    write_json(args.outdir / "bioinformatics-capability-matrix-r1-summary.json", summary)
    write_csv(args.outdir / "bioinformatics-capability-matrix-r1-scorecard.csv", rows)
    (args.outdir / "bioinformatics-capability-matrix-r1-results.md").write_text(
        make_markdown(rows, summary),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
