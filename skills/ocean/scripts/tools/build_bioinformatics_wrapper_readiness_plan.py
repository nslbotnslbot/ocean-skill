#!/usr/bin/env python3
"""Build readiness plans for priority OCEAN bioinformatics wrappers.

This script turns the capability matrix into implementation plans for the
highest-priority bioinformatics tools. It does not install software, execute
tools, download references, or validate biological claims.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import sys
from typing import Any


DEFAULT_MATRIX = "bioinformatics-capability-matrix-r1-results.json"
DEFAULT_OUT_PREFIX = "bioinformatics-wrapper-readiness-r1"

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

COMMON_RUN_EVIDENCE = [
    "tool version and executable/package source",
    "exact command line or workflow step",
    "parameters and configuration files",
    "reference/index/database name and version when applicable",
    "input file manifest and sample metadata boundary",
    "output file manifest",
    "logs, warnings, QC metrics, and failure messages",
    "environment/container/OS/hardware notes when relevant",
    "run date",
]

COMMON_STOP_CONDITIONS = [
    "tool is unavailable in the current environment and no container/install plan is provided",
    "version, command, reference/index, inputs, outputs, or logs are missing",
    "private clinical data or unpublished data lack explicit local handling boundaries",
    "the result is being used to claim mechanism, causality, clinical utility, or publication readiness without independent validation",
]


def profile(
    interface_layer: str,
    smoke_command: list[str],
    candidate_install_routes: list[str],
    minimal_fixture: str,
    expected_outputs: list[str],
    handoff: str = "Anchor",
    container_note: str = "Use a pinned container only after verifying source, license, and version tags.",
    extra_stop_conditions: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "interface_layer": interface_layer,
        "smoke_command": smoke_command,
        "candidate_install_routes": candidate_install_routes,
        "container_note": container_note,
        "minimal_fixture": minimal_fixture,
        "expected_outputs": expected_outputs,
        "handoff": handoff,
        "stop_conditions": COMMON_STOP_CONDITIONS + (extra_stop_conditions or []),
    }


PROFILES: dict[str, dict[str, Any]] = {
    "fastqc": profile(
        "lightweight_cli_subprocess",
        ["fastqc", "--version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "One tiny FASTQ or inspected existing FASTQ manifest; never publish private read data.",
        ["FastQC HTML report", "FastQC zip output", "stderr/stdout log"],
    ),
    "multiqc": profile(
        "lightweight_cli_subprocess",
        ["multiqc", "--version"],
        [
            "Candidate Python/conda route; verify current package and version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Directory containing one or more inspected QC report folders.",
        ["MultiQC HTML report", "multiqc_data directory", "execution log"],
    ),
    "cutadapt": profile(
        "lightweight_cli_subprocess",
        ["cutadapt", "--version"],
        [
            "Candidate Python/conda route; verify current package and version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Small FASTQ plus explicit adapter sequence or inspected trimming config.",
        ["trimmed FASTQ", "cutadapt report/log"],
    ),
    "fastp": profile(
        "lightweight_cli_subprocess",
        ["fastp", "--version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Small paired or single-end FASTQ fixture with explicit read privacy boundary.",
        ["trimmed FASTQ", "JSON report", "HTML report", "stderr/stdout log"],
    ),
    "samtools": profile(
        "lightweight_cli_subprocess",
        ["samtools", "--version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Small public/test BAM or inspected local BAM manifest with no private sequence release.",
        ["indexed/sorted BAM or stats output", "command log"],
    ),
    "bcftools": profile(
        "lightweight_cli_subprocess",
        ["bcftools", "--version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Small public/test VCF or inspected local VCF manifest.",
        ["filtered/query VCF or stats output", "command log"],
    ),
    "bedtools": profile(
        "lightweight_cli_subprocess",
        ["bedtools", "--version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Tiny public/test BED intervals with explicit genome-build boundary.",
        ["intersect/coverage output", "command log"],
    ),
    "blast": profile(
        "lightweight_cli_subprocess",
        ["blastp", "-version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate local database route; verify database provenance, date, and license before query.",
        ],
        "Short public/test sequence and tiny local database or explicitly inspected database metadata.",
        ["tabular BLAST output", "database provenance note", "command log"],
        extra_stop_conditions=["database provenance is missing or remote database terms are unclear"],
    ),
    "mafft": profile(
        "lightweight_cli_subprocess",
        ["mafft", "--version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Small public/test FASTA alignment fixture.",
        ["aligned FASTA", "command log"],
    ),
    "hmmer": profile(
        "lightweight_cli_subprocess",
        ["hmmsearch", "-h"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate profile/database route; verify HMM library provenance and date before use.",
        ],
        "Small public/test HMM profile plus FASTA target, or inspected HMM database metadata.",
        ["hmmsearch/hmmscan tabular output", "profile/database provenance note", "command log"],
        extra_stop_conditions=["HMM profile/database provenance is missing"],
    ),
    "minimap2": profile(
        "lightweight_cli_subprocess",
        ["minimap2", "--version"],
        [
            "Candidate conda/bioconda route; verify package/channel/version before use.",
            "Candidate container route; verify image source, tag, and license before use.",
        ],
        "Small public/test FASTA/FASTQ plus reference sequence with explicit reference boundary.",
        ["PAF/SAM output", "command log"],
    ),
    "deseq2": profile(
        "r_bioconductor_rscript",
        ["Rscript", "-e", "cat(as.character(utils::packageVersion('DESeq2')))"],
        [
            "Candidate Bioconductor route through BiocManager; verify R/Bioconductor compatibility before use.",
            "Candidate container route; verify image source, tag, and package versions before use.",
        ],
        "Small count matrix plus explicit design metadata and contrast definition.",
        ["DE result table", "sessionInfo output", "design/contrast log"],
        extra_stop_conditions=["replicates, design matrix, batch handling, or multiple-testing control are missing"],
    ),
    "edger": profile(
        "r_bioconductor_rscript",
        ["Rscript", "-e", "cat(as.character(utils::packageVersion('edgeR')))"],
        [
            "Candidate Bioconductor route through BiocManager; verify R/Bioconductor compatibility before use.",
            "Candidate container route; verify image source, tag, and package versions before use.",
        ],
        "Small count matrix plus explicit design metadata and contrast definition.",
        ["DE result table", "sessionInfo output", "design/contrast log"],
        extra_stop_conditions=["normalization, dispersion model, design matrix, or FDR handling are missing"],
    ),
    "limma_voom": profile(
        "r_bioconductor_rscript",
        ["Rscript", "-e", "cat(as.character(utils::packageVersion('limma')))"],
        [
            "Candidate Bioconductor route through BiocManager; verify R/Bioconductor compatibility before use.",
            "Candidate container route; verify image source, tag, and package versions before use.",
        ],
        "Small count/expression matrix plus explicit design metadata and contrast definition.",
        ["DE result table", "sessionInfo output", "voom/design/contrast log"],
        extra_stop_conditions=["voom/limma assumptions, design matrix, or FDR handling are missing"],
    ),
    "seurat": profile(
        "r_bioconductor_rscript",
        ["Rscript", "-e", "cat(as.character(utils::packageVersion('Seurat')))"],
        [
            "Candidate R package route; verify R/package compatibility before use.",
            "Candidate container route; verify image source, tag, and package versions before use.",
        ],
        "Tiny public/test object or inspected object manifest; never expose private cell-level data.",
        ["processed object metadata", "QC summary", "sessionInfo output", "analysis log"],
        extra_stop_conditions=["batch, doublet, annotation, or cell filtering boundary is missing"],
    ),
    "dada2": profile(
        "r_bioconductor_rscript",
        ["Rscript", "-e", "cat(as.character(utils::packageVersion('dada2')))"],
        [
            "Candidate Bioconductor route through BiocManager; verify R/Bioconductor compatibility before use.",
            "Candidate container route; verify image source, tag, and package versions before use.",
        ],
        "Small public/test amplicon FASTQ fixture or inspected local read manifest.",
        ["ASV table", "taxonomy table if classifier/reference is supplied", "filtering/error logs", "sessionInfo output"],
        extra_stop_conditions=["primer/read orientation, filtering parameters, reference classifier, or contamination boundary is missing"],
    ),
    "snakemake": profile(
        "workflow_reproducibility",
        ["snakemake", "--version"],
        [
            "Candidate Python/conda route; verify current package and workflow compatibility before use.",
            "Candidate containerized workflow route; verify images and profiles before use.",
        ],
        "Tiny dry-run workflow with explicit Snakefile, config, and input manifest.",
        ["dry-run DAG/log", "workflow config", "environment/container manifest"],
        handoff="Harbor",
        extra_stop_conditions=["workflow lacks pinned environment, input manifest, or dry-run evidence"],
    ),
    "nextflow": profile(
        "workflow_reproducibility",
        ["nextflow", "-version"],
        [
            "Candidate runtime route through official installer or package manager; verify Java/runtime compatibility.",
            "Candidate nf-core/container route; verify workflow version, profiles, and image tags.",
        ],
        "Tiny dry-run or test-profile workflow with explicit config and input manifest.",
        ["dry-run/test log", "workflow config", "container/environment manifest"],
        handoff="Harbor",
        extra_stop_conditions=["workflow version, profile, container image, or input manifest is missing"],
    ),
    "docker": profile(
        "workflow_reproducibility",
        ["docker", "--version"],
        [
            "System/container-runtime installation route; verify platform permissions and security policy before use.",
        ],
        "Version probe plus image manifest only; do not run unknown images.",
        ["runtime version output", "image digest/tag manifest", "container command log when executed"],
        handoff="Harbor",
        container_note="Docker is the container runtime; verify image digest, permissions, and data mounts before execution.",
        extra_stop_conditions=["image source, digest/tag, volume mounts, or data egress boundaries are unclear"],
    ),
    "singularity_apptainer": profile(
        "workflow_reproducibility",
        ["apptainer", "--version"],
        [
            "System/HPC runtime installation route; verify institutional module/container policy before use.",
            "Fallback command may be `singularity --version` when Apptainer is not present; verify runtime identity and version before use.",
        ],
        "Version probe plus SIF/image manifest only; do not run unknown images.",
        ["runtime version output", "SIF/image digest/tag manifest", "container command log when executed"],
        handoff="Harbor",
        container_note="Apptainer/Singularity is the container runtime; verify image provenance and HPC policy before execution.",
        extra_stop_conditions=["image provenance, bind mounts, HPC policy, or data egress boundaries are unclear"],
    ),
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_matrix(path: Path) -> dict[str, dict[str, Any]]:
    rows = read_json(path)
    return {row["slug"]: row for row in rows}


def readiness_score(row: dict[str, Any], plan: dict[str, Any]) -> int:
    score = 0
    if row.get("capability_tier") in {"source_packet_scaffold", "source_packet_adapter"}:
        score += 2
    if row.get("local_smoke_status") == "executed":
        score += 2
    if plan.get("smoke_command"):
        score += 1
    if plan.get("candidate_install_routes"):
        score += 1
    if plan.get("minimal_fixture"):
        score += 1
    if plan.get("required_run_evidence"):
        score += 1
    if plan.get("stop_conditions"):
        score += 1
    if plan.get("handoff"):
        score += 1
    return score


def readiness_stage(row: dict[str, Any]) -> str:
    if row.get("local_smoke_status") == "executed":
        return "stage_2_local_smoke_executed"
    if row.get("best_interface") in {"r_package", "python_import", "cli", "none_found"}:
        return "stage_1_plan_ready_environment_missing"
    return "stage_0_profile_needed"


def make_plan(row: dict[str, Any]) -> dict[str, Any]:
    slug = row["slug"]
    base = PROFILES.get(slug)
    if base is None:
        base = profile(
            "unknown",
            [],
            ["No priority profile exists yet; inspect official tool documentation before adding install or execution claims."],
            "No fixture specified yet.",
            [],
        )
    plan = {
        "schema_version": "ocean-bioinformatics-wrapper-readiness-r1",
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "tool": {
            "slug": slug,
            "name": row["name"],
            "family": row["family"],
            "maturity": row.get("maturity", ""),
        },
        "current_ocean_state": {
            "capability_tier": row.get("capability_tier", ""),
            "local_smoke_status": row.get("local_smoke_status", ""),
            "best_interface": row.get("best_interface", ""),
            "entrypoint": row.get("entrypoint", ""),
            "python_wrapper": row.get("python_wrapper", ""),
            "real_run_required": row.get("real_run_required", True),
        },
        "readiness_stage": readiness_stage(row),
        "interface_layer": base["interface_layer"],
        "smoke_command": base["smoke_command"],
        "candidate_install_routes": base["candidate_install_routes"],
        "container_note": base["container_note"],
        "minimal_fixture": base["minimal_fixture"],
        "required_run_evidence": COMMON_RUN_EVIDENCE,
        "expected_outputs": base["expected_outputs"],
        "stop_conditions": base["stop_conditions"],
        "source_packet_step": {
            "wrapper": row.get("python_wrapper", "scripts/create_source_packet.py"),
            "required_before_packet": "Fill a real run-record JSON from inspected files/logs before creating an OCEAN software source packet.",
        },
        "handoff": base["handoff"],
        "evidence_boundary": "Readiness plan only; not installation, execution, benchmark, or biological validation.",
    }
    plan["readiness_score_0_10"] = readiness_score(row, plan)
    return plan


def make_markdown(plans: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Wrapper Readiness Plan R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Priority tools planned: {summary['priority_tools']}",
        f"- Mean readiness score: {summary['mean_readiness_score']:.2f} / 10",
        f"- Local smoke already executed: {summary['stage_counts'].get('stage_2_local_smoke_executed', 0)}",
        f"- Environment-missing but plan-ready: {summary['stage_counts'].get('stage_1_plan_ready_environment_missing', 0)}",
        "",
        "## What This Adds",
        "",
        "This R1 artifact turns the capability matrix into implementation plans for high-priority tools. Each plan records the intended interface layer, a bounded smoke probe, candidate install/container routes, the minimal fixture needed, required run evidence, stop conditions, and OCEAN handoff.",
        "",
        "It does not install or run the tools. Candidate install routes must be verified against current official documentation before use.",
        "",
        "## Priority Plan Table",
        "",
        "| Tool | Family | Stage | Score | Interface | Smoke command | Handoff |",
        "|---|---|---|---:|---|---|---|",
    ]
    for plan in plans:
        command = " ".join(plan["smoke_command"]) if plan["smoke_command"] else "profile needed"
        lines.append(
            f"| {plan['tool']['name']} | {plan['tool']['family']} | {plan['readiness_stage']} | {plan['readiness_score_0_10']} | {plan['interface_layer']} | `{command}` | {plan['handoff']} |"
        )
    lines.extend(
        [
            "",
            "## Next Implementation Order",
            "",
        ]
    )
    sorted_plans = sorted(
        plans,
        key=lambda item: (
            item["readiness_stage"] != "stage_2_local_smoke_executed",
            -item["readiness_score_0_10"],
            item["tool"]["slug"],
        ),
    )
    for index, plan in enumerate(sorted_plans, start=1):
        lines.append(
            f"{index}. **{plan['tool']['name']}**: {plan['readiness_stage']}; next step is to collect a real run record or verify/install the environment, then create a source packet."
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "- `stage_2_local_smoke_executed` means a bounded local version/package probe existed in the capability matrix, not a biological analysis.",
            "- `stage_1_plan_ready_environment_missing` means OCEAN has a plan, but local execution is unavailable until the environment/tool/container is supplied.",
            "- Candidate install routes are planning notes and must be verified against official/current documentation before use.",
            "- These plans cannot support mechanism, causality, clinical utility, reproducibility, or publication readiness without inspected run records and downstream OCEAN audit.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_csv(path: Path, plans: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "slug",
        "name",
        "family",
        "stage",
        "score",
        "interface_layer",
        "local_smoke_status",
        "best_interface",
        "smoke_command",
        "handoff",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for plan in plans:
            writer.writerow(
                {
                    "slug": plan["tool"]["slug"],
                    "name": plan["tool"]["name"],
                    "family": plan["tool"]["family"],
                    "stage": plan["readiness_stage"],
                    "score": plan["readiness_score_0_10"],
                    "interface_layer": plan["interface_layer"],
                    "local_smoke_status": plan["current_ocean_state"]["local_smoke_status"],
                    "best_interface": plan["current_ocean_state"]["best_interface"],
                    "smoke_command": " ".join(plan["smoke_command"]),
                    "handoff": plan["handoff"],
                }
            )


def summarize(plans: list[dict[str, Any]]) -> dict[str, Any]:
    stage_counts: dict[str, int] = {}
    interface_counts: dict[str, int] = {}
    for plan in plans:
        stage_counts[plan["readiness_stage"]] = stage_counts.get(plan["readiness_stage"], 0) + 1
        interface_counts[plan["interface_layer"]] = interface_counts.get(plan["interface_layer"], 0) + 1
    mean_score = sum(plan["readiness_score_0_10"] for plan in plans) / len(plans) if plans else 0.0
    return {
        "run_date": dt.date.today().isoformat(),
        "priority_tools": len(plans),
        "mean_readiness_score": round(mean_score, 2),
        "stage_counts": dict(sorted(stage_counts.items())),
        "interface_counts": dict(sorted(interface_counts.items())),
        "evidence_boundary": "Wrapper readiness plans only; no installation, execution, benchmark, or biological validation.",
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build OCEAN bioinformatics wrapper readiness plans.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--matrix", type=Path)
    parser.add_argument("--prefix", default=DEFAULT_OUT_PREFIX)
    args = parser.parse_args(argv)

    matrix_path = args.matrix or args.outdir / DEFAULT_MATRIX
    matrix_by_slug = load_matrix(matrix_path)
    missing = [slug for slug in PRIORITY_SLUGS if slug not in matrix_by_slug]
    if missing:
        raise SystemExit("Missing priority slugs from matrix: " + ", ".join(missing))

    plans = [make_plan(matrix_by_slug[slug]) for slug in PRIORITY_SLUGS]
    summary = summarize(plans)
    artifacts_dir = args.outdir / f"{args.prefix}-artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    for plan in plans:
        write_json(artifacts_dir / f"{plan['tool']['slug']}-readiness-plan.json", plan)

    write_json(args.outdir / f"{args.prefix}-results.json", plans)
    write_json(args.outdir / f"{args.prefix}-summary.json", summary)
    write_csv(args.outdir / f"{args.prefix}-scorecard.csv", plans)
    (args.outdir / f"{args.prefix}-results.md").write_text(make_markdown(plans, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
