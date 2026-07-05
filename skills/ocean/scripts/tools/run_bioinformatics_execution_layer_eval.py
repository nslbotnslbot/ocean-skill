#!/usr/bin/env python3
"""Evaluate OCEAN bioinformatics execution layers.

This eval covers three tool classes:

- lightweight CLI tools that can be probed through subprocess;
- R/Bioconductor tools that can be checked through Rscript;
- heavy/license/GUI/database/GPU tools that should produce launch plans only.

It does not install tools, download databases, run omics workflows, or validate
scientific claims.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


LIGHTWEIGHT_CLI_CASES = [
    ("FastQC", "fastqc", "fastqc", "--version"),
    ("MultiQC", "multiqc", "multiqc", "--version"),
    ("cutadapt", "cutadapt", "cutadapt", "--version"),
    ("fastp", "fastp", "fastp", "--version"),
    ("samtools", "samtools", "samtools", "--version"),
    ("bcftools", "bcftools", "bcftools", "--version"),
    ("BEDTools", "bedtools", "bedtools", "--version"),
    ("BLAST", "blast", "blastp", "-version"),
    ("MAFFT", "mafft", "mafft", "--version"),
    ("HMMER", "hmmer", "hmmsearch", "-h"),
    ("minimap2", "minimap2", "minimap2", "--version"),
]

RSCRIPT_CASES = [
    ("DESeq2", "deseq2", "DESeq2"),
    ("limma", "limma_voom", "limma"),
    ("edgeR", "edger", "edgeR"),
    ("Seurat", "seurat", "Seurat"),
    ("WGCNA", "wgcna", "WGCNA"),
    ("DADA2", "dada2", "dada2"),
]

HEAVY_TOOL_CASES = [
    (
        "Cell Ranger",
        "cell_ranger",
        "cellranger count --id <run_id> --transcriptome <refdata> --fastqs <fastq_dir> --sample <sample>",
        ["10x reference transcriptome", "FASTQ directory", "sample sheet", "Cell Ranger license/terms"],
    ),
    (
        "GATK",
        "gatk",
        "gatk HaplotypeCaller -R <reference.fa> -I <input.bam> -O <output.g.vcf.gz>",
        ["reference FASTA", "FASTA index", "sequence dictionary", "coordinate-sorted BAM", "BAM index"],
    ),
    (
        "AlphaFold",
        "alphafold",
        "run_alphafold.py --fasta_paths <input.fasta> --data_dir <database_dir> --output_dir <outdir>",
        ["AlphaFold genetic databases", "model parameters", "FASTA input", "GPU/container environment"],
    ),
    (
        "MaxQuant",
        "maxquant",
        "MaxQuantCmd.exe <mqpar.xml>",
        ["mqpar.xml", "raw mass spectrometry files", "FASTA database", "license/platform notes"],
    ),
    (
        "Galaxy",
        "galaxy",
        "plan Galaxy workflow export/import with workflow ID, history ID, datasets, and tool versions",
        ["workflow export", "history export", "dataset manifest", "tool shed versions"],
    ),
    (
        "3D Slicer",
        "three_d_slicer",
        "Slicer --no-main-window --python-script <script.py>",
        ["input image/segmentation manifest", "extension list", "script", "exported logs"],
    ),
    (
        "ChimeraX",
        "chimerax",
        "ChimeraX --nogui <script.cxc>",
        ["structure files", "session/script file", "render/export plan", "command log"],
    ),
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_command(command: list[str], timeout: int) -> tuple[int, str]:
    proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    return proc.returncode, (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")


def run_cli_case(common_dir: Path, outdir: Path, case: tuple[str, str, str, str], timeout: int) -> dict[str, Any]:
    name, slug, command_name, probe_args = case
    output = outdir / "bioinformatics-execution-layer-r1-artifacts" / f"{slug}-cli.json"
    command = [
        sys.executable,
        str(common_dir / "cli_subprocess_wrapper.py"),
        "probe",
        "--tool-name",
        name,
        "--tool-slug",
        slug,
        "--command",
        command_name,
        f"--probe-args={probe_args}",
        "--timeout",
        str(timeout),
        "--output",
        str(output),
    ]
    code, text = run_command(command, timeout + 5)
    if not output.exists():
        return {
            "layer": "lightweight_cli_subprocess",
            "tool": name,
            "slug": slug,
            "status": "wrapper_failed",
            "verdict": "needs_review",
            "artifact": str(output),
            "returncode": code,
            "output_excerpt": text[:1000],
        }
    payload = read_json(output)
    status = payload["execution_status"]
    verdict = "pass" if status in {"executed", "not_available_current_environment"} else "needs_review"
    return {
        "layer": "lightweight_cli_subprocess",
        "tool": name,
        "slug": slug,
        "status": status,
        "verdict": verdict,
        "artifact": str(output),
        "returncode": code,
        "output_excerpt": text[:1000],
    }


def run_r_case(common_dir: Path, outdir: Path, case: tuple[str, str, str], timeout: int) -> dict[str, Any]:
    name, slug, package = case
    output = outdir / "bioinformatics-execution-layer-r1-artifacts" / f"{slug}-rscript.json"
    command = [
        sys.executable,
        str(common_dir / "rscript_wrapper.py"),
        "check-package",
        "--tool-name",
        name,
        "--tool-slug",
        slug,
        "--package",
        package,
        "--timeout",
        str(timeout),
        "--output",
        str(output),
    ]
    code, text = run_command(command, timeout + 5)
    if not output.exists():
        return {
            "layer": "r_bioconductor_rscript",
            "tool": name,
            "slug": slug,
            "status": "wrapper_failed",
            "verdict": "needs_review",
            "artifact": str(output),
            "returncode": code,
            "output_excerpt": text[:1000],
        }
    payload = read_json(output)
    status = payload["execution_status"]
    verdict = "pass" if status in {"executed", "not_available_current_environment"} else "needs_review"
    return {
        "layer": "r_bioconductor_rscript",
        "tool": name,
        "slug": slug,
        "status": status,
        "verdict": verdict,
        "artifact": str(output),
        "returncode": code,
        "output_excerpt": text[:1000],
    }


def run_heavy_case(common_dir: Path, outdir: Path, case: tuple[str, str, str, list[str]], timeout: int) -> dict[str, Any]:
    name, slug, template, required_assets = case
    output = outdir / "bioinformatics-execution-layer-r1-artifacts" / f"{slug}-launcher-plan.json"
    command = [
        sys.executable,
        str(common_dir / "heavy_tool_launcher.py"),
        "plan",
        "--tool-name",
        name,
        "--tool-slug",
        slug,
        "--command-template",
        template,
        "--required-assets-json",
        json.dumps(required_assets),
        "--output",
        str(output),
    ]
    code, text = run_command(command, timeout + 5)
    if not output.exists():
        return {
            "layer": "heavy_tool_launcher_plan",
            "tool": name,
            "slug": slug,
            "status": "wrapper_failed",
            "verdict": "needs_review",
            "artifact": str(output),
            "returncode": code,
            "output_excerpt": text[:1000],
        }
    payload = read_json(output)
    status = payload["execution_status"]
    verdict = "pass" if status == "planned_not_executed" else "needs_review"
    return {
        "layer": "heavy_tool_launcher_plan",
        "tool": name,
        "slug": slug,
        "status": status,
        "verdict": verdict,
        "artifact": str(output),
        "returncode": code,
        "output_excerpt": text[:1000],
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Execution Layer Eval R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        f"- Executed local probes/packages: {summary['executed']}",
        f"- Unavailable in current environment: {summary['not_available_current_environment']}",
        f"- Launcher plans created without execution: {summary['planned_not_executed']}",
        "",
        "| Layer | Tool | Status | Verdict |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['layer']} | {row['tool']} | {row['status']} | {row['verdict']} |")
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval checks execution-layer behavior only. It does not install missing tools, download references, run full omics pipelines, process biological or clinical datasets, benchmark software, or validate scientific claims. Unavailable CLI/R tools are environment gaps, not failures of those tools. Heavy-tool cases must remain `planned_not_executed` until the user supplies installation, license, reference/database, compute, and run-record evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run OCEAN bioinformatics execution-layer eval.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args(argv)

    common_dir = args.skill_dir / "scripts" / "tools" / "common"
    rows: list[dict[str, Any]] = []
    for case in LIGHTWEIGHT_CLI_CASES:
        rows.append(run_cli_case(common_dir, args.outdir, case, args.timeout))
    for case in RSCRIPT_CASES:
        rows.append(run_r_case(common_dir, args.outdir, case, args.timeout))
    for case in HEAVY_TOOL_CASES:
        rows.append(run_heavy_case(common_dir, args.outdir, case, args.timeout))

    summary = {
        "run_date": dt.date.today().isoformat(),
        "cases": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "executed": sum(1 for row in rows if row["status"] == "executed"),
        "not_available_current_environment": sum(
            1 for row in rows if row["status"] == "not_available_current_environment"
        ),
        "planned_not_executed": sum(1 for row in rows if row["status"] == "planned_not_executed"),
        "boundary": "Execution-layer smoke only; not scientific validation.",
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / "bioinformatics-execution-layer-r1-results.json", rows)
    write_json(args.outdir / "bioinformatics-execution-layer-r1-summary.json", summary)
    with (args.outdir / "bioinformatics-execution-layer-r1-scorecard.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=["layer", "slug", "tool", "status", "verdict", "artifact"])
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in ["layer", "slug", "tool", "status", "verdict", "artifact"]})
    (args.outdir / "bioinformatics-execution-layer-r1-results.md").write_text(
        make_markdown(rows, summary), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
