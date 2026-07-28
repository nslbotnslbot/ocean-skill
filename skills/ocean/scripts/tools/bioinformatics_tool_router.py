#!/usr/bin/env python3
"""Route bioinformatics tools to OCEAN execution layers and workflow plans."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any


DEFAULT_SKILL_DIR = Path(__file__).resolve().parents[2]

WORKFLOWS = {
    "fastq-qc": {
        "intent": "raw FASTQ quality control and preprocessing evidence plan",
        "tools": ["fastqc", "fastp", "cutadapt", "multiqc"],
        "handoff": "Anchor",
    },
    "rna-seq-differential-expression": {
        "intent": "bulk RNA-seq QC, alignment/quantification, and differential-expression evidence plan",
        "tools": ["fastqc", "multiqc", "star", "salmon", "featurecounts", "deseq2", "limma_voom", "edger"],
        "handoff": "Iceberg",
    },
    "variant-calling-qc": {
        "intent": "variant calling, file-operation, and QC provenance plan",
        "tools": ["bwa", "samtools", "bcftools", "gatk", "freebayes", "strelka2", "deepvariant", "picard"],
        "handoff": "Anchor",
    },
    "single-cell-rna-seq": {
        "intent": "single-cell RNA-seq preprocessing, annotation, and latent-model provenance plan",
        "tools": ["cell_ranger", "alevin_fry", "starsolo", "scanpy", "seurat", "scvi", "celltypist", "azimuth"],
        "handoff": "Iceberg",
    },
    "spatial-transcriptomics": {
        "intent": "spatial transcriptomics alignment, annotation, deconvolution, and mapping plan",
        "tools": [
            "space_ranger",
            "squidpy",
            "stlearn",
            "cell2location",
            "tangram",
            "stereoscope",
            "giotto",
        ],
        "handoff": "Iceberg",
    },
    "metagenomics-microbiome": {
        "intent": "microbiome/metagenomics QC, profiling, and compositional-analysis evidence plan",
        "tools": ["fastqc", "multiqc", "kraken2", "bracken", "metaphlan", "humann", "qiime2", "dada2"],
        "handoff": "Iceberg",
    },
    "genome-assembly-annotation": {
        "intent": "genome assembly, assembly QC, and annotation provenance plan",
        "tools": [
            "flye",
            "canu",
            "raven",
            "spades",
            "megahit",
            "quast",
            "busco",
            "bakta",
            "prokka",
            "eggnog_mapper",
            "interproscan",
        ],
        "handoff": "Anchor",
    },
    "protein-structure": {
        "intent": "protein structure prediction, structure search, and confidence-boundary plan",
        "tools": ["alphafold_db", "alphafold", "colabfold", "rosettafold", "hh_suite", "hmmer", "modeller", "pymol", "chimerax"],
        "handoff": "Iceberg",
    },
    "epigenomics-peak-calling": {
        "intent": "epigenomic alignment, peak-calling, motif, and signal-track provenance plan",
        "tools": ["fastqc", "multiqc", "bowtie2", "samtools", "bedtools", "macs2", "macs3", "homer", "deeptools", "fimo", "meme"],
        "handoff": "Iceberg",
    },
    "proteomics-metabolomics": {
        "intent": "proteomics/metabolomics search, quantification, and feature-detection provenance plan",
        "tools": ["maxquant", "fragpipe", "dia_nn", "skyline", "ms_dial", "mzmine", "xcms"],
        "handoff": "Anchor",
    },
    "workflow-reproducibility": {
        "intent": "workflow, environment, and container reproducibility plan",
        "tools": ["conda", "docker", "singularity_apptainer", "snakemake", "nextflow", "nf_core", "cwl", "wdl_cromwell", "galaxy"],
        "handoff": "Harbor",
    },
    "imaging-ai": {
        "intent": "medical/biological imaging annotation, segmentation, and ML workflow provenance plan",
        "tools": ["three_d_slicer", "itk_snap", "simpleitk", "torchio", "monai", "nnu_net"],
        "handoff": "Anchor",
    },
}


def today() -> str:
    return dt.date.today().isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def registry_path(skill_dir: Path) -> Path:
    return skill_dir / "scripts" / "tools" / "bioinformatics" / "registry.json"


def tool_dir(skill_dir: Path, slug: str) -> Path:
    return skill_dir / "scripts" / "tools" / "bioinformatics" / slug


def load_wrapper_config(skill_dir: Path, slug: str) -> dict[str, Any]:
    path = tool_dir(skill_dir, slug) / "wrapper_config.json"
    if not path.exists():
        raise SystemExit(f"Missing wrapper config for '{slug}': {path}")
    return read_json(path)


def load_registry(skill_dir: Path) -> list[dict[str, Any]]:
    return read_json(registry_path(skill_dir))


def tool_index(skill_dir: Path) -> dict[str, dict[str, Any]]:
    return {item["slug"]: item for item in load_registry(skill_dir)}


def family_tags(family: str) -> list[str]:
    return [part for part in family.replace("-", "_").split("_") if part]


def wrapper_for_layer(layer: str) -> str:
    return {
        "source_packet_adapter": "tool-specific source_packet.py",
        "lightweight_cli": "tool-specific scripts/run_cli.py",
        "r_bioconductor": "tool-specific scripts/run_package.py",
        "python_package": "tool-specific scripts/run_package.py",
        "workflow_runtime": "tool-specific scripts/run_launcher.py",
        "heavy_launcher_plan": "tool-specific scripts/run_launcher.py",
        "run_record_only": "tool-specific scripts/probe_or_plan.py",
    }[layer]


def required_evidence(layer: str) -> list[str]:
    base = [
        "tool name and version",
        "task intent",
        "exact command or script path",
        "parameters",
        "input/output manifest",
        "logs or QC artifacts",
        "environment",
        "date",
    ]
    if layer == "source_packet_adapter":
        return ["adapter input identifiers/files", "adapter output packet", "source-specific confidence/metadata fields"]
    if layer == "lightweight_cli":
        return base + ["PATH-resolved executable", "stdout/stderr excerpts", "return code"]
    if layer == "r_bioconductor":
        return base + ["Rscript path", "R package version", "R session/environment notes"]
    if layer == "python_package":
        return base + ["Python package version or import check", "Python environment export"]
    if layer == "workflow_runtime":
        return base + ["workflow definition", "container/environment lock", "resume/cache state", "executor/backend"]
    if layer == "heavy_launcher_plan":
        return base + ["license/terms status", "reference database/index", "compute requirements", "launcher plan"]
    return base


def stop_conditions(layer: str) -> list[str]:
    common = [
        "missing tool version",
        "missing input manifest",
        "missing parameters",
        "missing logs/QC",
    ]
    if layer == "lightweight_cli":
        return ["command not installed on PATH", "probe/run returns no usable output", *common]
    if layer == "r_bioconductor":
        return ["Rscript not installed", "R package unavailable", *common]
    if layer == "python_package":
        return ["Python package unavailable", "no script/notebook/run record supplied", *common]
    if layer == "heavy_launcher_plan":
        return [
            "license/terms not confirmed",
            "reference database/index missing",
            "GPU/HPC/container runtime missing",
            "GUI workflow has no exported log",
            *common,
        ]
    if layer == "workflow_runtime":
        return ["workflow engine unavailable", "container/environment lock missing", "no run manifest", *common]
    if layer == "source_packet_adapter":
        return ["adapter input missing", "source file/API response missing", "source-specific confidence fields missing"]
    return common


def wrapper_command(
    slug: str,
    layer: str,
    skill_dir: Path,
) -> list[str]:
    directory = tool_dir(skill_dir, slug)
    if layer == "source_packet_adapter":
        return ["python3", str(directory / "source_packet.py"), "--help"]
    if layer == "lightweight_cli":
        return [
            "python3",
            str(directory / "scripts" / "run_cli.py"),
            "probe",
            "--output",
            f"outputs/{slug}-probe.json",
        ]
    if layer in {"r_bioconductor", "python_package"}:
        return [
            "python3",
            str(directory / "scripts" / "run_package.py"),
            "probe",
            "--output",
            f"outputs/{slug}-package-probe.json",
        ]
    if layer == "workflow_runtime":
        return [
            "python3",
            str(directory / "scripts" / "run_launcher.py"),
            "probe-runtime",
            "--output",
            f"outputs/{slug}-runtime-probe.json",
        ]
    if layer == "heavy_launcher_plan":
        return [
            "python3",
            str(directory / "scripts" / "run_launcher.py"),
            "plan",
            "--output",
            f"outputs/{slug}-launcher-plan.json",
        ]
    return [
        "python3",
        str(directory / "scripts" / "probe_or_plan.py"),
        "--output",
        f"outputs/{slug}-check.json",
    ]


def shell_join(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def build_profile(tool: dict[str, Any], skill_dir: Path) -> dict[str, Any]:
    slug = tool["slug"]
    config = load_wrapper_config(skill_dir, slug)
    layer = config.get("execution_layer")
    if not layer:
        raise SystemExit(f"Missing execution_layer in wrapper config for '{slug}'")
    command = wrapper_command(slug, layer, skill_dir)
    entrypoint = config.get("entrypoint") or slug.replace("_", "-")
    return {
        "tool_name": tool["name"],
        "tool_slug": slug,
        "family": tool["family"],
        "task_tags": family_tags(tool["family"]),
        "execution_layer": layer,
        "primary_entrypoint": entrypoint,
        "wrapper": wrapper_for_layer(layer),
        "wrapper_command": command,
        "wrapper_command_shell": shell_join(command),
        "required_evidence": config.get("required_run_evidence") or required_evidence(layer),
        "stop_conditions": config.get("stop_conditions") or stop_conditions(layer),
        "handoff": config.get("handoff", "Anchor"),
        "availability": "unknown_until_checked",
        "source_packet_rule": "Only create a source packet after inspecting run metadata or source-specific adapter outputs.",
        "cannot_support_alone": tool.get("cannot_support_alone", []),
        "evidence_boundary": "Execution profile only; not proof that the tool is installed, executed, valid, benchmarked, or biologically correct.",
    }


def export_catalog(skill_dir: Path) -> dict[str, Any]:
    registry = load_registry(skill_dir)
    profiles = [build_profile(tool, skill_dir) for tool in registry]
    by_layer: dict[str, int] = {}
    by_family: dict[str, int] = {}
    for profile in profiles:
        by_layer[profile["execution_layer"]] = by_layer.get(profile["execution_layer"], 0) + 1
        by_family[profile["family"]] = by_family.get(profile["family"], 0) + 1
    return {
        "schema_version": "ocean-bioinformatics-tool-router-r1",
        "date": today(),
        "tools": len(profiles),
        "by_execution_layer": dict(sorted(by_layer.items())),
        "by_family": dict(sorted(by_family.items())),
        "profiles": profiles,
        "evidence_boundary": "Catalog profiles route tools to execution layers; they do not execute tools or validate claims.",
    }


def build_workflow(skill_dir: Path, workflow: str) -> dict[str, Any]:
    if workflow not in WORKFLOWS:
        raise SystemExit(f"Unknown workflow '{workflow}'. Use list-workflows.")
    index = tool_index(skill_dir)
    spec = WORKFLOWS[workflow]
    steps = []
    missing = []
    for number, slug in enumerate(spec["tools"], start=1):
        tool = index.get(slug)
        if not tool:
            missing.append(slug)
            continue
        profile = build_profile(tool, skill_dir)
        steps.append(
            {
                "step": number,
                "tool_slug": slug,
                "tool_name": profile["tool_name"],
                "execution_layer": profile["execution_layer"],
                "wrapper": profile["wrapper"],
                "wrapper_command_shell": profile["wrapper_command_shell"],
                "required_evidence": profile["required_evidence"],
                "stop_conditions": profile["stop_conditions"],
                "handoff": profile["handoff"],
            }
        )
    return {
        "schema_version": "ocean-bioinformatics-workflow-plan-r1",
        "date": today(),
        "workflow": workflow,
        "intent": spec["intent"],
        "steps": steps,
        "missing_tool_slugs": missing,
        "final_handoff": spec["handoff"],
        "negative_space": [
            "No tool execution has happened from this plan alone.",
            "No reference database/index has been inspected unless a run record says so.",
            "No biological mechanism, diagnosis, treatment effect, or benchmark superiority is supported by the plan alone.",
        ],
        "evidence_boundary": "Workflow plan only; execute tools locally and inspect run records before making scientific claims.",
    }


def make_workflow_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# OCEAN Bioinformatics Workflow Plan: {plan['workflow']}",
        "",
        f"- Date: {plan['date']}",
        f"- Intent: {plan['intent']}",
        f"- Final handoff: {plan['final_handoff']}",
        "",
        "| Step | Tool | Layer | Wrapper |",
        "|---:|---|---|---|",
    ]
    for step in plan["steps"]:
        lines.append(
            f"| {step['step']} | {step['tool_name']} | {step['execution_layer']} | {step['wrapper']} |"
        )
    lines.extend(["", "## Wrapper Commands", ""])
    for step in plan["steps"]:
        lines.append(f"{step['step']}. `{step['wrapper_command_shell']}`")
    lines.extend(
        [
            "",
            "## Negative Space",
            "",
            *[f"- {item}" for item in plan["negative_space"]],
            "",
            "## Evidence Boundary",
            "",
            plan["evidence_boundary"],
        ]
    )
    return "\n".join(lines) + "\n"


def command_profile(args: argparse.Namespace) -> int:
    index = tool_index(args.skill_dir)
    tool = index.get(args.tool)
    if not tool:
        raise SystemExit(f"Unknown tool slug: {args.tool}")
    profile = build_profile(tool, args.skill_dir)
    if args.output:
        write_json(args.output, profile)
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


def command_catalog(args: argparse.Namespace) -> int:
    catalog = export_catalog(args.skill_dir)
    if args.output:
        write_json(args.output, catalog)
    print(json.dumps({"tools": catalog["tools"], "by_execution_layer": catalog["by_execution_layer"]}, ensure_ascii=False, indent=2))
    return 0


def command_workflow(args: argparse.Namespace) -> int:
    plan = build_workflow(args.skill_dir, args.workflow)
    if args.output:
        write_json(args.output, plan)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(make_workflow_markdown(plan), encoding="utf-8")
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0 if not plan["missing_tool_slugs"] else 1


def command_list_workflows(args: argparse.Namespace) -> int:
    data = {
        name: {
            "intent": spec["intent"],
            "tools": spec["tools"],
            "handoff": spec["handoff"],
        }
        for name, spec in WORKFLOWS.items()
    }
    if args.output:
        write_json(args.output, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def command_list_tools(args: argparse.Namespace) -> int:
    profiles = [
        build_profile(tool, args.skill_dir)
        for tool in load_registry(args.skill_dir)
    ]
    if args.family:
        profiles = [item for item in profiles if item["family"] == args.family]
    if args.layer:
        profiles = [item for item in profiles if item["execution_layer"] == args.layer]
    if args.search:
        needle = args.search.casefold()
        profiles = [
            item
            for item in profiles
            if needle in item["tool_name"].casefold()
            or needle in item["tool_slug"].casefold()
            or needle in item["family"].casefold()
        ]
    payload = {
        "count": len(profiles),
        "tools": [
            {
                "slug": item["tool_slug"],
                "name": item["tool_name"],
                "family": item["family"],
                "execution_layer": item["execution_layer"],
                "availability": item["availability"],
            }
            for item in profiles
        ],
    }
    if args.output:
        write_json(args.output, payload)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("slug\tname\tfamily\texecution_layer\tavailability")
        for item in payload["tools"]:
            print(
                "\t".join(
                    [
                        item["slug"],
                        item["name"],
                        item["family"],
                        item["execution_layer"],
                        item["availability"],
                    ]
                )
            )
    return 0


def command_check(args: argparse.Namespace) -> int:
    index = tool_index(args.skill_dir)
    if args.tool not in index:
        raise SystemExit(f"Unknown tool slug: {args.tool}")
    script = tool_dir(args.skill_dir, args.tool) / "scripts" / "probe_or_plan.py"
    if not script.exists():
        raise SystemExit(f"Missing check entrypoint for '{args.tool}': {script}")
    output = args.output or Path("outputs") / f"{args.tool}-check.json"
    command = [
        sys.executable,
        str(script),
        "--output",
        str(output),
        "--timeout",
        str(args.timeout),
    ]
    if args.packet_output:
        command.extend(["--packet-output", str(args.packet_output)])
    print(f"Running: {shell_join(command)}", flush=True)
    return subprocess.run(command, check=False).returncode


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Route OCEAN bioinformatics tools to execution layers and workflow plans.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    list_tools = sub.add_parser("list-tools", help="List covered tools without claiming local availability.")
    list_tools.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    list_tools.add_argument("--family")
    list_tools.add_argument("--layer")
    list_tools.add_argument("--search")
    list_tools.add_argument("--format", choices=["text", "json"], default="text")
    list_tools.add_argument("--output", type=Path)
    list_tools.set_defaults(func=command_list_tools)

    profile = sub.add_parser("profile", help="Show one tool's execution layer and evidence contract.")
    profile.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    profile.add_argument("--tool", required=True)
    profile.add_argument("--output", type=Path)
    profile.set_defaults(func=command_profile)

    catalog = sub.add_parser("catalog", help="Export the complete tool catalog.")
    catalog.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    catalog.add_argument("--output", type=Path)
    catalog.set_defaults(func=command_catalog)

    workflow = sub.add_parser("workflow", help="Build a bounded workflow plan.")
    workflow.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    workflow.add_argument("--workflow", choices=sorted(WORKFLOWS), required=True)
    workflow.add_argument("--output", type=Path)
    workflow.add_argument("--markdown-output", type=Path)
    workflow.set_defaults(func=command_workflow)

    list_workflows = sub.add_parser("list-workflows", help="List available workflow templates.")
    list_workflows.add_argument("--output", type=Path)
    list_workflows.set_defaults(func=command_list_workflows)

    check = sub.add_parser("check", help="Run a bounded availability probe or create a non-executing plan.")
    check.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    check.add_argument("--tool", required=True)
    check.add_argument("--output", type=Path)
    check.add_argument("--packet-output", type=Path)
    check.add_argument("--timeout", type=int, default=20)
    check.set_defaults(func=command_check)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
