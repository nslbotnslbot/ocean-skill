#!/usr/bin/env python3
"""Run local availability/version smoke checks for OCEAN bioinformatics tools.

This is a real local execution smoke eval, not an end-to-end scientific run.
For each tool scaffold, it tries safe local entry points:

- CLI command discovery and version/help execution;
- Python package import where that is the natural interface;
- R package version checks where applicable;
- OCEAN local adapter evals for tools that have local adapters.

It does not install software, download databases, build indices, run alignments,
process patient data, or claim biological validity.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any

COMMON_DIR = Path(__file__).resolve().parent / "common"
sys.path.insert(0, str(COMMON_DIR))

from probe_status import classify_probe_status  # noqa: E402


CLI_ALIASES = {
    "alevin_fry": ["alevin-fry"],
    "alphafold": ["run_alphafold.py", "alphafold"],
    "bakta": ["bakta"],
    "bcftools": ["bcftools"],
    "bedtools": ["bedtools"],
    "blast": ["blastp", "blastn", "blastx"],
    "bowtie2": ["bowtie2"],
    "bracken": ["bracken"],
    "busco": ["busco"],
    "bwa": ["bwa"],
    "canu": ["canu"],
    "cell_ranger": ["cellranger"],
    "checkm": ["checkm"],
    "chimerax": ["ChimeraX", "chimerax"],
    "clustal_omega": ["clustalo"],
    "colabfold": ["colabfold_batch"],
    "conda": ["conda"],
    "cutadapt": ["cutadapt"],
    "cwl": ["cwltool"],
    "deeptools": ["deeptools", "bamCoverage", "plotHeatmap"],
    "deepvariant": ["run_deepvariant"],
    "dia_nn": ["diann"],
    "docker": ["docker"],
    "eggnog_mapper": ["emapper.py", "emapper"],
    "fastp": ["fastp"],
    "fastqc": ["fastqc"],
    "fasttree": ["FastTree", "fasttree"],
    "featurecounts": ["featureCounts"],
    "fimo": ["fimo"],
    "flye": ["flye"],
    "fragpipe": ["fragpipe"],
    "freebayes": ["freebayes"],
    "galaxy": ["galaxy"],
    "gatk": ["gatk"],
    "hh_suite": ["hhsearch", "hhblits", "hhmake"],
    "hisat2": ["hisat2"],
    "hmmer": ["hmmscan", "hmmsearch", "hmmbuild"],
    "homer": ["findMotifsGenome.pl", "homer"],
    "htslib": ["bgzip", "tabix"],
    "humann": ["humann"],
    "interproscan": ["interproscan.sh", "interproscan"],
    "iq_tree": ["iqtree2", "iqtree"],
    "itk_snap": ["itksnap"],
    "kallisto": ["kallisto"],
    "kraken2": ["kraken2"],
    "last": ["lastal", "lastdb"],
    "macs2": ["macs2"],
    "macs3": ["macs3"],
    "mafft": ["mafft"],
    "maxquant": ["MaxQuantCmd", "maxquant"],
    "megahit": ["megahit"],
    "meme": ["meme"],
    "metaphlan": ["metaphlan"],
    "minimap2": ["minimap2"],
    "modeller": ["mod9.25", "mod10.4", "modeller"],
    "ms_dial": ["MSDIAL", "msdial"],
    "multiqc": ["multiqc"],
    "muscle": ["muscle"],
    "mutect2": ["gatk"],
    "mzmine": ["mzmine"],
    "nextflow": ["nextflow"],
    "nf_core": ["nf-core"],
    "nnu_net": ["nnUNetv2_train", "nnUNet_train"],
    "orthofinder": ["orthofinder"],
    "picard": ["picard"],
    "prokka": ["prokka"],
    "pymol": ["pymol"],
    "qiime2": ["qiime"],
    "qualimap": ["qualimap"],
    "quast": ["quast.py", "quast"],
    "raven": ["raven"],
    "raxml": ["raxmlHPC", "raxml-ng"],
    "rsem": ["rsem-calculate-expression"],
    "salmon": ["salmon"],
    "samtools": ["samtools"],
    "singularity_apptainer": ["apptainer", "singularity"],
    "skyline": ["SkylineCmd", "skyline"],
    "snakemake": ["snakemake"],
    "space_ranger": ["spaceranger"],
    "spades": ["spades.py", "spades"],
    "star": ["STAR"],
    "starsolo": ["STAR"],
    "strelka2": ["configureStrelkaGermlineWorkflow.py", "configureStrelkaSomaticWorkflow.py"],
    "stringtie": ["stringtie"],
    "three_d_slicer": ["Slicer"],
    "trim_galore": ["trim_galore"],
    "trimmomatic": ["trimmomatic"],
    "wdl_cromwell": ["cromwell"],
}

PYTHON_IMPORTS = {
    "cell2location": ["cell2location"],
    "celltypist": ["celltypist"],
    "deeptools": ["deeptools"],
    "diablo": ["mixomics"],
    "giotto": ["giotto"],
    "monai": ["monai"],
    "mofa": ["mofapy2"],
    "mofaplus": ["mofapy2"],
    "scanpy": ["scanpy"],
    "scvi": ["scvi"],
    "simpleitk": ["SimpleITK"],
    "squidpy": ["squidpy"],
    "stereoscope": ["stereoscope"],
    "stlearn": ["stlearn"],
    "tangram": ["tangram"],
    "torchio": ["torchio"],
}

R_PACKAGES = {
    "azimuth": ["Azimuth"],
    "dada2": ["dada2"],
    "deseq2": ["DESeq2"],
    "edger": ["edgeR"],
    "limma_voom": ["limma"],
    "mixomics": ["mixOmics"],
    "seurat": ["Seurat"],
    "sleuth": ["sleuth"],
    "wgcna": ["WGCNA"],
    "xcms": ["xcms"],
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_text(text: str, limit: int = 2000) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text[:limit]


def candidate_commands(tool: dict[str, Any]) -> list[str]:
    slug = tool["slug"]
    name = tool["name"]
    if slug in CLI_ALIASES:
        return CLI_ALIASES[slug]
    generated = {
        slug,
        slug.replace("_", "-"),
        slug.replace("_", ""),
        name.lower(),
        name.lower().replace(" ", "-"),
        name.lower().replace(" ", "_"),
    }
    return list(dict.fromkeys(CLI_ALIASES.get(slug, []) + sorted(generated)))


def run_command(command: list[str], timeout: int) -> tuple[int, str]:
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        return proc.returncode, safe_text(output)
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") + ("\n" + exc.stderr if exc.stderr else "")
        return 124, safe_text(str(output) + "\nTIMEOUT")
    except OSError as exc:
        return 127, safe_text(str(exc))


def try_cli(tool: dict[str, Any], timeout: int) -> dict[str, Any] | None:
    for candidate in candidate_commands(tool):
        resolved = shutil.which(candidate)
        if not resolved:
            continue
        nonzero_probe: dict[str, Any] | None = None
        probes = [
            [resolved, "--version"],
            [resolved, "-version"],
            [resolved, "version"],
            [resolved, "--help"],
            [resolved, "-h"],
        ]
        for probe in probes:
            code, output = run_command(probe, timeout)
            status = classify_probe_status(code, output)
            if status == "executed":
                return {
                    "interface": "cli",
                    "status": "executed",
                    "entrypoint": candidate,
                    "resolved_path": resolved,
                    "command": probe,
                    "returncode": code,
                    "output_excerpt": output,
                }
            if status == "found_but_probe_nonzero" and nonzero_probe is None:
                nonzero_probe = {
                    "interface": "cli",
                    "status": "found_but_probe_nonzero",
                    "entrypoint": candidate,
                    "resolved_path": resolved,
                    "command": probe,
                    "returncode": code,
                    "output_excerpt": output,
                }
        if nonzero_probe:
            return nonzero_probe
        return {
            "interface": "cli",
            "status": "found_but_probe_failed",
            "entrypoint": candidate,
            "resolved_path": resolved,
            "command": probes[0],
            "returncode": code,
            "output_excerpt": output,
        }
    return None


def try_python_import(tool: dict[str, Any]) -> dict[str, Any] | None:
    for module in PYTHON_IMPORTS.get(tool["slug"], []):
        try:
            imported = importlib.import_module(module)
            version = getattr(imported, "__version__", "version_not_exposed")
            return {
                "interface": "python_import",
                "status": "executed",
                "entrypoint": module,
                "version": str(version),
                "output_excerpt": f"import {module} succeeded; version={version}",
            }
        except Exception as exc:  # noqa: BLE001 - diagnostic smoke test
            last_error = str(exc)
    if PYTHON_IMPORTS.get(tool["slug"]):
        return {
            "interface": "python_import",
            "status": "not_available_current_environment",
            "entrypoint": ",".join(PYTHON_IMPORTS[tool["slug"]]),
            "output_excerpt": safe_text(last_error),
        }
    return None


def try_r_package(tool: dict[str, Any], timeout: int) -> dict[str, Any] | None:
    rscript = shutil.which("Rscript")
    packages = R_PACKAGES.get(tool["slug"], [])
    if not packages:
        return None
    if not rscript:
        return {
            "interface": "r_package",
            "status": "not_available_current_environment",
            "entrypoint": ",".join(packages),
            "output_excerpt": "Rscript is not available on PATH.",
        }
    package = packages[0]
    code, output = run_command(
        [rscript, "-e", f"cat(as.character(utils::packageVersion('{package}')))"],
        timeout,
    )
    return {
        "interface": "r_package",
        "status": "executed" if code == 0 else "not_available_current_environment",
        "entrypoint": package,
        "command": [rscript, "-e", f"packageVersion('{package}')"],
        "returncode": code,
        "output_excerpt": output,
    }


def try_local_adapter(tool: dict[str, Any], skill_dir: Path, outdir: Path) -> dict[str, Any] | None:
    if tool["slug"] != "alphafold_db":
        return None
    script = skill_dir / "scripts" / "tools" / "bioinformatics" / "alphafold_db" / "run_eval.py"
    if not script.exists():
        return None
    adapter_outdir = outdir / "bioinformatics-real-tool-smoke-r1-adapter-artifacts"
    command = [sys.executable, str(script), "--skill-dir", str(skill_dir), "--outdir", str(adapter_outdir)]
    code, output = run_command(command, 30)
    return {
        "interface": "ocean_local_adapter",
        "status": "executed" if code == 0 else "found_but_probe_failed",
        "entrypoint": str(script),
        "command": command,
        "returncode": code,
        "output_excerpt": output,
    }


def evaluate_tool(tool: dict[str, Any], skill_dir: Path, outdir: Path, timeout: int) -> dict[str, Any]:
    attempts = []
    for attempt in [
        try_local_adapter(tool, skill_dir, outdir),
        try_cli(tool, timeout),
        try_python_import(tool),
        try_r_package(tool, timeout),
    ]:
        if attempt:
            attempts.append(attempt)
            if attempt["status"] == "executed":
                break
    if not attempts:
        attempts.append(
            {
                "interface": "none_found",
                "status": "not_available_current_environment",
                "entrypoint": "",
                "output_excerpt": "No CLI command, Python module, R package, or OCEAN local adapter found in the current environment.",
            }
        )
    best = attempts[-1] if attempts[-1]["status"] == "executed" else attempts[0]
    return {
        "slug": tool["slug"],
        "name": tool["name"],
        "family": tool["family"],
        "maturity": tool.get("maturity", ""),
        "verdict": best["status"],
        "best_interface": best["interface"],
        "attempts": attempts,
        "evidence_boundary": "Real local availability/version smoke only; not an end-to-end biological analysis or scientific validation.",
    }


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN Bioinformatics Real-Tool Smoke Eval R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Tools checked: {summary['tools_checked']}",
        f"- Executed locally: {summary['executed']}",
        f"- Found but probe failed: {summary['found_but_probe_failed']}",
        f"- Not available in current environment: {summary['not_available_current_environment']}",
        "",
        "| Tool | Family | Verdict | Interface | Entrypoint |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        first = row["attempts"][0]
        lines.append(
            f"| {row['name']} | {row['family']} | {row['verdict']} | {row['best_interface']} | {first.get('entrypoint', '')} |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval attempts real local smoke execution only. It checks local CLI/version/help commands, Python imports, R package version calls, or OCEAN local adapters when available. It does not install missing tools, download reference databases, build indices, run omics workflows, process raw biological/clinical data, benchmark methods, or validate scientific claims.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run local smoke checks for OCEAN bioinformatics tool scaffolds.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=8)
    args = parser.parse_args(argv)

    registry_path = args.skill_dir / "scripts" / "tools" / "bioinformatics" / "registry.json"
    registry = read_json(registry_path)
    rows = [evaluate_tool(tool, args.skill_dir, args.outdir, args.timeout) for tool in registry]
    summary = {
        "run_date": dt.date.today().isoformat(),
        "tools_checked": len(rows),
        "executed": sum(1 for row in rows if row["verdict"] == "executed"),
        "found_but_probe_failed": sum(1 for row in rows if row["verdict"] == "found_but_probe_failed"),
        "not_available_current_environment": sum(1 for row in rows if row["verdict"] == "not_available_current_environment"),
        "boundary": "Local smoke execution only; not end-to-end analysis.",
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_json(args.outdir / "bioinformatics-real-tool-smoke-r1-results.json", rows)
    write_json(args.outdir / "bioinformatics-real-tool-smoke-r1-summary.json", summary)
    with (args.outdir / "bioinformatics-real-tool-smoke-r1-scorecard.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["slug", "name", "family", "verdict", "best_interface"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "slug": row["slug"],
                    "name": row["name"],
                    "family": row["family"],
                    "verdict": row["verdict"],
                    "best_interface": row["best_interface"],
                }
            )
    (args.outdir / "bioinformatics-real-tool-smoke-r1-results.md").write_text(make_markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
