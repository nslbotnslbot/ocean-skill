#!/usr/bin/env python3
"""Route bioinformatics tools to OCEAN execution layers and workflow plans."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import shlex
import sys
from typing import Any


CLI_ENTRYPOINTS = {
    "alevin_fry": ["alevin-fry"],
    "bakta": ["bakta"],
    "bcftools": ["bcftools"],
    "bedtools": ["bedtools"],
    "blast": ["blastp", "blastn", "blastx"],
    "bowtie2": ["bowtie2"],
    "bracken": ["bracken"],
    "busco": ["busco"],
    "bwa": ["bwa"],
    "canu": ["canu"],
    "checkm": ["checkm"],
    "clustal_omega": ["clustalo"],
    "cutadapt": ["cutadapt"],
    "deeptools": ["bamCoverage", "plotHeatmap"],
    "dia_nn": ["diann"],
    "eggnog_mapper": ["emapper.py", "emapper"],
    "fastp": ["fastp"],
    "fastqc": ["fastqc"],
    "fasttree": ["FastTree", "fasttree"],
    "featurecounts": ["featureCounts"],
    "fimo": ["fimo"],
    "flye": ["flye"],
    "freebayes": ["freebayes"],
    "hh_suite": ["hhsearch", "hhblits", "hhmake"],
    "hisat2": ["hisat2"],
    "hmmer": ["hmmsearch", "hmmscan", "hmmbuild"],
    "homer": ["findMotifsGenome.pl", "homer"],
    "htslib": ["bgzip", "tabix"],
    "humann": ["humann"],
    "interproscan": ["interproscan.sh", "interproscan"],
    "iq_tree": ["iqtree2", "iqtree"],
    "kallisto": ["kallisto"],
    "kraken2": ["kraken2"],
    "last": ["lastal", "lastdb"],
    "macs2": ["macs2"],
    "macs3": ["macs3"],
    "mafft": ["mafft"],
    "megahit": ["megahit"],
    "meme": ["meme"],
    "metaphlan": ["metaphlan"],
    "minimap2": ["minimap2"],
    "multiqc": ["multiqc"],
    "muscle": ["muscle"],
    "orthofinder": ["orthofinder"],
    "picard": ["picard"],
    "prokka": ["prokka"],
    "qiime2": ["qiime"],
    "qualimap": ["qualimap"],
    "quast": ["quast.py", "quast"],
    "raven": ["raven"],
    "raxml": ["raxml-ng", "raxmlHPC"],
    "rsem": ["rsem-calculate-expression"],
    "salmon": ["salmon"],
    "samtools": ["samtools"],
    "spades": ["spades.py", "spades"],
    "star": ["STAR"],
    "starsolo": ["STAR"],
    "strelka2": ["configureStrelkaGermlineWorkflow.py", "configureStrelkaSomaticWorkflow.py"],
    "stringtie": ["stringtie"],
    "trim_galore": ["trim_galore"],
    "trimmomatic": ["trimmomatic"],
}

CLI_PROBE_ARGS = {
    "blast": "-version",
    "hmmmer": "-h",
    "hmmer": "-h",
    "last": "-h",
    "quast": "--version",
    "spades": "--version",
    "strelka2": "--help",
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

PYTHON_PACKAGES = {
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

HEAVY_TOOLS = {
    "alphafold",
    "cell_ranger",
    "chimerax",
    "colabfold",
    "deepvariant",
    "fragpipe",
    "galaxy",
    "gatk",
    "itk_snap",
    "maxquant",
    "modeller",
    "ms_dial",
    "mutect2",
    "mzmine",
    "nnu_net",
    "pymol",
    "rosettafold",
    "skyline",
    "space_ranger",
    "three_d_slicer",
}

WORKFLOW_TOOLS = {
    "conda": ["conda"],
    "cwl": ["cwltool"],
    "docker": ["docker"],
    "nextflow": ["nextflow"],
    "nf_core": ["nf-core"],
    "singularity_apptainer": ["apptainer", "singularity"],
    "snakemake": ["snakemake"],
    "wdl_cromwell": ["cromwell"],
}

SOURCE_PACKET_ADAPTERS = {
    "alphafold_db": "scripts/tools/bioinformatics/alphafold_db/source_packet.py",
}

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


def load_registry(skill_dir: Path) -> list[dict[str, Any]]:
    return read_json(registry_path(skill_dir))


def tool_index(skill_dir: Path) -> dict[str, dict[str, Any]]:
    return {item["slug"]: item for item in load_registry(skill_dir)}


def family_tags(family: str) -> list[str]:
    return [part for part in family.replace("-", "_").split("_") if part]


def primary_entrypoint(slug: str) -> str:
    for table in (CLI_ENTRYPOINTS, R_PACKAGES, PYTHON_PACKAGES, WORKFLOW_TOOLS):
        values = table.get(slug)
        if values:
            return values[0]
    return slug.replace("_", "-")


def cli_probe_args(slug: str) -> str:
    return CLI_PROBE_ARGS.get(slug, "--version")


def classify_tool(slug: str, family: str) -> str:
    if slug in SOURCE_PACKET_ADAPTERS:
        return "source_packet_adapter"
    if slug in HEAVY_TOOLS:
        return "heavy_launcher_plan"
    if slug in WORKFLOW_TOOLS:
        return "workflow_runtime"
    if slug in R_PACKAGES:
        return "r_bioconductor"
    if slug in PYTHON_PACKAGES:
        return "python_package"
    if slug in CLI_ENTRYPOINTS:
        return "lightweight_cli"
    if family == "workflow_reproducibility":
        return "workflow_runtime"
    return "run_record_only"


def wrapper_for_layer(layer: str) -> str:
    return {
        "source_packet_adapter": "tool-specific source_packet.py",
        "lightweight_cli": "scripts/tools/common/cli_subprocess_wrapper.py",
        "r_bioconductor": "scripts/tools/common/rscript_wrapper.py",
        "python_package": "scripts/tools/common/software_source_packet.py plus Python import/run record",
        "workflow_runtime": "scripts/tools/common/heavy_tool_launcher.py or workflow run record",
        "heavy_launcher_plan": "scripts/tools/common/heavy_tool_launcher.py",
        "run_record_only": "scripts/tools/common/software_source_packet.py",
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


def wrapper_command(slug: str, tool: dict[str, Any], layer: str, skill_dir: Path) -> list[str]:
    name = tool["name"]
    if layer == "source_packet_adapter":
        adapter = SOURCE_PACKET_ADAPTERS[slug]
        return ["python3", str(skill_dir / adapter), "--help"]
    if layer == "lightweight_cli":
        entry = primary_entrypoint(slug)
        return [
            "python3",
            str(skill_dir / "scripts/tools/common/cli_subprocess_wrapper.py"),
            "probe",
            "--tool-name",
            name,
            "--tool-slug",
            slug,
            "--command",
            entry,
            f"--probe-args={cli_probe_args(slug)}",
            "--output",
            f"{slug}-probe.json",
        ]
    if layer == "r_bioconductor":
        package = primary_entrypoint(slug)
        return [
            "python3",
            str(skill_dir / "scripts/tools/common/rscript_wrapper.py"),
            "check-package",
            "--tool-name",
            name,
            "--tool-slug",
            slug,
            "--package",
            package,
            "--output",
            f"{slug}-rscript-check.json",
        ]
    if layer in {"heavy_launcher_plan", "workflow_runtime"}:
        return [
            "python3",
            str(skill_dir / "scripts/tools/common/heavy_tool_launcher.py"),
            "plan",
            "--tool-name",
            name,
            "--tool-slug",
            slug,
            "--command-template",
            f"{primary_entrypoint(slug)} <user-supplied arguments>",
            "--output",
            f"{slug}-launch-plan.json",
        ]
    return [
        "python3",
        str(skill_dir / "scripts/tools/common/software_source_packet.py"),
        "template",
        "--tool-name",
        name,
        "--tool-slug",
        slug,
        "--output",
        f"{slug}-run-record.template.json",
    ]


def shell_join(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def build_profile(tool: dict[str, Any], skill_dir: Path) -> dict[str, Any]:
    slug = tool["slug"]
    layer = classify_tool(slug, tool["family"])
    command = wrapper_command(slug, tool, layer, skill_dir)
    return {
        "tool_name": tool["name"],
        "tool_slug": slug,
        "family": tool["family"],
        "task_tags": family_tags(tool["family"]),
        "execution_layer": layer,
        "primary_entrypoint": primary_entrypoint(slug),
        "wrapper": wrapper_for_layer(layer),
        "wrapper_command": command,
        "wrapper_command_shell": shell_join(command),
        "required_evidence": required_evidence(layer),
        "stop_conditions": stop_conditions(layer),
        "handoff": "Anchor" if layer in {"lightweight_cli", "r_bioconductor", "python_package", "workflow_runtime"} else "Compass",
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
    write_json(args.output, profile)
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


def command_catalog(args: argparse.Namespace) -> int:
    catalog = export_catalog(args.skill_dir)
    write_json(args.output, catalog)
    print(json.dumps({"tools": catalog["tools"], "by_execution_layer": catalog["by_execution_layer"]}, ensure_ascii=False, indent=2))
    return 0


def command_workflow(args: argparse.Namespace) -> int:
    plan = build_workflow(args.skill_dir, args.workflow)
    write_json(args.output, plan)
    if args.markdown_output:
        args.markdown_output.write_text(make_workflow_markdown(plan), encoding="utf-8")
    print(json.dumps({"workflow": args.workflow, "steps": len(plan["steps"]), "missing": plan["missing_tool_slugs"]}, ensure_ascii=False, indent=2))
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
    write_json(args.output, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Route OCEAN bioinformatics tools to execution layers and workflow plans.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    profile = sub.add_parser("profile")
    profile.add_argument("--skill-dir", type=Path, required=True)
    profile.add_argument("--tool", required=True)
    profile.add_argument("--output", type=Path, required=True)
    profile.set_defaults(func=command_profile)

    catalog = sub.add_parser("catalog")
    catalog.add_argument("--skill-dir", type=Path, required=True)
    catalog.add_argument("--output", type=Path, required=True)
    catalog.set_defaults(func=command_catalog)

    workflow = sub.add_parser("workflow")
    workflow.add_argument("--skill-dir", type=Path, required=True)
    workflow.add_argument("--workflow", required=True)
    workflow.add_argument("--output", type=Path, required=True)
    workflow.add_argument("--markdown-output", type=Path)
    workflow.set_defaults(func=command_workflow)

    list_workflows = sub.add_parser("list-workflows")
    list_workflows.add_argument("--output", type=Path, required=True)
    list_workflows.set_defaults(func=command_list_workflows)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
