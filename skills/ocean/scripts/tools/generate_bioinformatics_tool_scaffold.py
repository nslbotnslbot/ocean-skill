#!/usr/bin/env python3
"""Generate OCEAN bioinformatics tool scaffold folders.

This script creates lightweight per-tool folders from OCEAN's bioinformatics
resource map. It is deterministic and does not install or run any external tool.
"""

from __future__ import annotations

import json
from pathlib import Path
import re


TOOLS = [
    ("qc_preprocessing", ["FastQC", "MultiQC", "cutadapt", "fastp", "Trimmomatic", "Trim Galore", "Picard", "Qualimap"]),
    ("sequence_alignment", ["BLAST", "LAST", "minimap2", "BWA", "Bowtie2"]),
    ("spliced_rna_alignment", ["STAR", "HISAT2"]),
    ("alignment_file_operations", ["SAMtools", "bcftools", "BEDTools", "HTSlib"]),
    ("variant_calling", ["GATK", "FreeBayes", "DeepVariant", "Strelka2", "Mutect2"]),
    ("rna_seq_quantification", ["Salmon", "kallisto", "RSEM", "featureCounts", "StringTie"]),
    ("differential_expression", ["DESeq2", "edgeR", "limma-voom", "sleuth"]),
    ("single_cell_analysis", ["Cell Ranger", "STARsolo", "Alevin-fry", "Seurat", "Scanpy", "scVI", "CellTypist", "Azimuth"]),
    ("spatial_transcriptomics", ["Space Ranger", "Squidpy", "Giotto", "cell2location", "Tangram", "Stereoscope", "stLearn"]),
    ("epigenomics_peak_calling", ["MACS2", "MACS3", "deepTools", "HOMER", "MEME", "FIMO"]),
    ("genome_assembly_annotation", ["Flye", "Canu", "Raven", "SPAdes", "MEGAHIT", "QUAST", "BUSCO", "CheckM", "Prokka", "Bakta", "eggNOG-mapper", "InterProScan"]),
    ("microbiome_metagenomics", ["QIIME2", "DADA2", "MetaPhlAn", "HUMAnN", "Kraken2", "Bracken"]),
    ("proteomics_metabolomics", ["MaxQuant", "FragPipe", "DIA-NN", "Skyline", "MS-DIAL", "XCMS", "MZmine"]),
    ("structure_modeling", ["AlphaFold", "AlphaFold DB", "ColabFold", "RoseTTAFold", "HH-suite", "HMMER", "MODELLER", "PyMOL", "ChimeraX"]),
    ("imaging_signal_ml", ["nnU-Net", "MONAI", "TorchIO", "SimpleITK", "ITK-SNAP", "3D Slicer"]),
    ("phylogenetics_comparative_genomics", ["MAFFT", "MUSCLE", "Clustal Omega", "IQ-TREE", "RAxML", "FastTree", "OrthoFinder"]),
    ("multi_omics_integration", ["WGCNA", "MOFA", "MOFA+", "mixOmics", "DIABLO"]),
    ("workflow_reproducibility", ["Snakemake", "Nextflow", "CWL", "WDL-Cromwell", "Galaxy", "Docker", "Singularity-Apptainer", "Conda", "nf-core"]),
]


FAMILY_USAGE = {
    "qc_preprocessing": {
        "use": "when inspecting raw-sequence quality, trimming, adapter removal, or read-level QC before downstream analysis.",
        "avoid": "as evidence for biological effect size, mechanism, or clinical validity.",
        "handoff": "Anchor for QC thresholds and reproducibility; Harbor for run records.",
    },
    "sequence_alignment": {
        "use": "when comparing query sequences to references or homologs with explicit database/index provenance.",
        "avoid": "as standalone proof of function, orthology, mechanism, or pathogenicity.",
        "handoff": "Reef for reference/database provenance; Iceberg for claims based on similarity.",
    },
    "spliced_rna_alignment": {
        "use": "when mapping RNA-seq reads to a genome/transcriptome with splice-aware alignment settings.",
        "avoid": "as standalone proof of differential expression or causal regulation.",
        "handoff": "Anchor for alignment QC and leakage checks; Iceberg for expression claims.",
    },
    "alignment_file_operations": {
        "use": "when sorting, indexing, filtering, summarizing, or intersecting alignment/interval files.",
        "avoid": "as a source of biological interpretation without upstream and downstream context.",
        "handoff": "Harbor for provenance; Anchor for reproducible command/environment checks.",
    },
    "variant_calling": {
        "use": "when recording inspected variant-calling runs with reference genome, caller version, parameters, and QC.",
        "avoid": "as standalone clinical interpretation, pathogenicity assignment, or treatment guidance.",
        "handoff": "Reef for ClinVar/gnomAD/resource routing; Iceberg for pathogenicity or mechanism claims.",
    },
    "rna_seq_quantification": {
        "use": "when quantifying transcript/gene abundance from RNA-seq with explicit reference and sample metadata.",
        "avoid": "as standalone proof of differential expression, mechanism, or phenotype causality.",
        "handoff": "Anchor for QC/replicate checks; Iceberg for expression-supported claims.",
    },
    "differential_expression": {
        "use": "when inspected count/contrast/design metadata can support bounded differential-expression analysis.",
        "avoid": "when design matrix, batch handling, replicates, or multiple-testing control are missing.",
        "handoff": "Iceberg for claim downgrade; Anchor for design, batch, and validation checks.",
    },
    "single_cell_analysis": {
        "use": "when inspecting single-cell preprocessing, clustering, annotation, integration, or reference mapping.",
        "avoid": "as proof of new cell types, causal states, or clinical biomarkers without orthogonal validation.",
        "handoff": "Reef for atlas/reference routing; Anchor for batch, doublet, annotation, and validation checks.",
    },
    "spatial_transcriptomics": {
        "use": "when inspecting spatial transcriptomics preprocessing, cell-type mapping, deconvolution, or spatial pattern analysis.",
        "avoid": "as standalone proof of cell-cell mechanism or spatial causality.",
        "handoff": "Reef for atlas/database provenance; Iceberg for mechanism claims; Anchor for validation.",
    },
    "epigenomics_peak_calling": {
        "use": "when inspecting peak calling, motif search, coverage, or regulatory-region evidence.",
        "avoid": "as standalone proof of direct transcriptional regulation or causal enhancer function.",
        "handoff": "Iceberg for regulatory claims; Anchor for controls, replicates, and blacklist/QC checks.",
    },
    "genome_assembly_annotation": {
        "use": "when inspecting assembly, annotation, completeness, contamination, or functional annotation outputs.",
        "avoid": "as standalone proof of phenotype, function, or taxonomic novelty without validation.",
        "handoff": "Anchor for assembly/QC; Reef for database/resource provenance.",
    },
    "microbiome_metagenomics": {
        "use": "when inspecting microbiome taxonomic, functional, or amplicon/metagenomic analysis runs.",
        "avoid": "as standalone proof of causality, treatment effect, or host mechanism.",
        "handoff": "Iceberg for association-vs-causality checks; Anchor for contamination, compositionality, and validation.",
    },
    "proteomics_metabolomics": {
        "use": "when inspecting proteomics/metabolomics identification, quantification, or feature-level analysis.",
        "avoid": "as standalone mechanistic or clinical proof without identification confidence and validation.",
        "handoff": "Anchor for FDR, batch, standards, and QC; Iceberg for mechanism claims.",
    },
    "structure_modeling": {
        "use": "when inspecting predicted/experimental structures, structural confidence, alignments, or visualization outputs.",
        "avoid": "as standalone proof of binding, mechanism, druggability, or functional rescue.",
        "handoff": "Reef for structure database provenance; Iceberg for structure-supported claims; Anchor for validation.",
    },
    "imaging_signal_ml": {
        "use": "when inspecting biomedical imaging/signal preprocessing, segmentation, model outputs, or evaluation runs.",
        "avoid": "as standalone clinical deployment evidence without external validation, calibration, and leakage checks.",
        "handoff": "Anchor for leakage/benchmark/reproducibility; Iceberg for clinical claims.",
    },
    "phylogenetics_comparative_genomics": {
        "use": "when inspecting multiple alignment, phylogeny, orthology, or comparative-genomics runs.",
        "avoid": "as standalone proof of function, trait causality, or species-level conclusion without support.",
        "handoff": "Reef for reference/database provenance; Iceberg for evolutionary/function claims.",
    },
    "multi_omics_integration": {
        "use": "when inspecting multi-omics modules, factors, networks, or integrative association patterns.",
        "avoid": "as standalone proof of causal mechanism or clinical utility.",
        "handoff": "Iceberg for association/causality boundaries; Anchor for validation and robustness checks.",
    },
    "workflow_reproducibility": {
        "use": "when inspecting workflow orchestration, environment capture, containers, dependency pinning, or run provenance.",
        "avoid": "as biological evidence by itself.",
        "handoff": "Harbor for reproducibility records; Anchor for rerun and benchmark planning.",
    },
}


def slugify(name: str) -> str:
    slug = name.lower()
    slug = slug.replace("+", "plus")
    slug = slug.replace("3d", "three_d")
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug


def readme(tool: dict) -> str:
    return f"""# {tool['name']}

OCEAN tool scaffold for `{tool['name']}`.

## Scope

- Family: `{tool['family']}`
- Current maturity: `L0/L1 scaffold`
- Shared helper: `../../common/software_source_packet.py`
- API contract: `api.json`
- Python wrapper: `scripts/create_source_packet.py`
- Example run record: `examples/run-record.example.json`

## Evidence Boundary

This folder does not mean OCEAN can run `{tool['name']}` automatically. It defines where tool-specific wrapper code, examples, and source-packet tests should live.

Before `{tool['name']}` output can be used as evidence, provide:

- tool version;
- command line or workflow step;
- parameters;
- reference/index/database;
- input files;
- output files;
- logs/QC;
- environment;
- date;
- inspected result fields.

The output cannot by itself prove biological mechanism, causality, clinical utility, reproducibility, or publication readiness.

## Python Wrapper

Use `scripts/create_source_packet.py` only after you have inspected a real run record:

```bash
python3 scripts/create_source_packet.py \\
  --input examples/run-record.example.json \\
  --output /path/to/{tool['slug']}-source-packet.json
```

The wrapper creates an OCEAN software source packet from provenance fields. It does not install or execute `{tool['name']}`.
"""


def readme_python_section(tool: dict) -> str:
    return f"""

## API / Python Wrapper

- API contract: `api.json`
- Python wrapper: `scripts/create_source_packet.py`
- Example input: `examples/run-record.example.json`

Use the wrapper only after you have inspected a real `{tool['name']}` run record:

```bash
python3 scripts/create_source_packet.py \\
  --input examples/run-record.example.json \\
  --output /path/to/{tool['slug']}-source-packet.json
```

The wrapper converts provenance fields into an OCEAN software source packet. It does not install or execute `{tool['name']}`.
"""


def readme_usage_section(tool: dict) -> str:
    return f"""

## Science-skills-style usage guide

See `references/tool_usage.md` for the tool-specific use/avoid rules, required local execution evidence, stop conditions, and OCEAN handoff path.
"""


def usage_reference(tool: dict) -> str:
    family = FAMILY_USAGE.get(
        tool["family"],
        {
            "use": "when an inspected software run can be tied to concrete inputs, parameters, outputs, logs, and environment metadata.",
            "avoid": "as standalone support for biological mechanism, causality, clinical utility, or publication readiness.",
            "handoff": "Anchor for validation and Harbor for run records.",
        },
    )
    return f"""# {tool['name']} Usage Guide

This is an OCEAN tool-use guide inspired by science-skills-style wrappers. It is not a standalone Codex skill and it does not mean `{tool['name']}` is installed locally.

## Use When

Use `{tool['name']}` {family['use']}

## Do Not Use When

Do not use `{tool['name']}` {family['avoid']}

Do not infer uninspected sample sizes, databases, parameters, versions, benchmarks, effect sizes, or validation results.

## Before Running Or Trusting Output

Confirm and record:

- tool version and executable/package source;
- command line or workflow step;
- parameters and configuration files;
- reference/index/database and version;
- input files and sample metadata boundaries;
- output files and inspected result fields;
- logs, warnings, QC metrics, and failure messages;
- environment, container, OS, hardware if relevant, and run date;
- license/terms constraints when the tool or database requires them.

## OCEAN Packet Workflow

1. Run an availability smoke check before promising execution.
2. If the tool is unavailable, report `not_available_current_environment` and create an install/environment plan rather than inventing output.
3. If a real run exists, fill `examples/run-record.example.json` with inspected metadata.
4. Convert the inspected run record with `scripts/create_source_packet.py`.
5. Hand off the packet according to: {family['handoff']}

## Stop Conditions

Stop and ask for more evidence when:

- version, command, reference/index, inputs, outputs, or logs are missing;
- the run used private/clinical data without explicit access/privacy boundaries;
- the result is being used to claim mechanism, causality, clinical utility, or publication readiness without independent validation;
- the tool is unavailable in the current environment.

## Evidence Boundary

`{tool['name']}` output can support bounded software-run provenance only after the run record is inspected. It cannot by itself prove biological mechanism, causal conclusion, clinical utility, reproducibility, or publication readiness.
"""


def api_contract(tool: dict) -> dict:
    return {
        "schema_version": "ocean-tool-api-v1",
        "tool_name": tool["name"],
        "tool_slug": tool["slug"],
        "tool_family": tool["family"],
        "maturity": tool.get("maturity", "L0/L1 scaffold"),
        "interface_type": "provenance_to_source_packet",
        "python_wrapper": "scripts/create_source_packet.py",
        "example_input": "examples/run-record.example.json",
        "default_output": f"outputs/{tool['slug']}-source-packet.json",
        "commands": [
            {
                "name": "create-source-packet",
                "description": "Convert an inspected tool run record into a bounded OCEAN software source packet.",
                "argv": [
                    "python3",
                    "scripts/create_source_packet.py",
                    "--input",
                    "examples/run-record.example.json",
                    "--output",
                    f"outputs/{tool['slug']}-source-packet.json",
                ],
            }
        ],
        "required_input_fields": [
            "tool_name",
            "tool_slug",
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
        ],
        "output_contract": {
            "source_type": "bioinformatics_software_run",
            "boundary_status": "queried_evidence",
            "handoff": "Anchor",
        },
        "usage_reference": "references/tool_usage.md",
        "execution_contract": {
            "availability_smoke_required_before_execution_claim": True,
            "real_run_record_required_before_evidence_packet": True,
            "install_or_container_plan_required_if_unavailable": True,
            "license_or_terms_check_required_when_applicable": True,
        },
        "evidence_boundary": {
            "does_not_run_external_tool": True,
            "cannot_support_alone": tool.get(
                "cannot_support_alone",
                [
                    "biological mechanism",
                    "causal conclusion",
                    "clinical utility",
                    "publication readiness",
                    "reproducibility without rerun/log/environment checks",
                ],
            ),
        },
    }


def python_wrapper(tool: dict) -> str:
    return f'''#!/usr/bin/env python3
"""Create an OCEAN source packet for an inspected {tool["name"]} run.

This wrapper does not install, call, or validate {tool["name"]}. It converts a
completed run-record JSON into a bounded OCEAN software source packet.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def _find_tools_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        candidate = parent / "common" / "software_source_packet.py"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find scripts/tools/common/software_source_packet.py")


TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
sys.path.insert(0, str(TOOLS_ROOT / "common"))

from software_source_packet import audit_record, make_packet, read_json, write_json  # noqa: E402


TOOL_NAME = {tool["name"]!r}
TOOL_SLUG = {tool["slug"]!r}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Create an OCEAN source packet for {{TOOL_NAME}}.")
    parser.add_argument("--input", type=Path, required=True, help="Inspected run-record JSON.")
    parser.add_argument("--output", type=Path, required=True, help="Output source-packet JSON.")
    args = parser.parse_args(argv)

    record = read_json(args.input)
    record.setdefault("tool_name", TOOL_NAME)
    record.setdefault("tool_slug", TOOL_SLUG)
    missing, warnings = audit_record(record)
    packet = make_packet(record)
    packet["filters"]["adapter"] = f"scripts/tools/bioinformatics/{{TOOL_SLUG}}/scripts/create_source_packet.py"
    packet["provenance_audit"] = {{
        "missing": missing,
        "warnings": warnings,
        "verdict": "pass" if not missing else "needs_review",
    }}
    write_json(args.output, packet)
    print(f"Wrote {{args.output}}")
    if missing:
        print("Missing required run-record fields: " + ", ".join(missing), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def example_run_record(tool: dict) -> dict:
    return {
        "example_note": "Template only. Replace placeholders with inspected run metadata before using as OCEAN evidence.",
        "tool_name": tool["name"],
        "tool_slug": tool["slug"],
        "tool_family": tool["family"],
        "tool_version": "",
        "task_intent": "",
        "command_line": "",
        "parameters": {},
        "reference_or_index": "",
        "input_files": [],
        "output_files": [],
        "logs_or_qc": [],
        "environment": "",
        "date": "",
        "supports_claims": [],
        "cannot_support": [
            "biological mechanism",
            "causal conclusion",
            "clinical utility",
            "publication readiness",
            "reproducibility without rerun/log/environment checks",
        ],
        "boundary_status": "queried_evidence",
        "handoff": "Anchor",
    }


def main() -> int:
    root = Path(__file__).resolve().parent
    bio_root = root / "bioinformatics"
    bio_root.mkdir(parents=True, exist_ok=True)

    registry = []
    seen = set()
    for family, names in TOOLS:
        for name in names:
            slug = slugify(name)
            if slug in seen:
                continue
            seen.add(slug)
            folder = bio_root / slug
            folder.mkdir(parents=True, exist_ok=True)
            data = {
                "name": name,
                "slug": slug,
                "family": family,
                "maturity": "L0/L1 scaffold",
                "shared_helper": "../../common/software_source_packet.py",
                "evidence_level": "candidate software route until run metadata is inspected",
                "required_packet_fields": [
                    "tool_name",
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
                ],
                "cannot_support_alone": [
                    "biological mechanism",
                    "causal conclusion",
                    "clinical utility",
                    "publication readiness",
                    "reproducibility without rerun/log/environment checks",
                ],
            }
            tool_json = folder / "tool.json"
            readme_path = folder / "README.md"
            if tool_json.exists():
                data = json.loads(tool_json.read_text(encoding="utf-8"))
            else:
                tool_json.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            if not readme_path.exists():
                readme_path.write_text(readme(data), encoding="utf-8")
            else:
                current_readme = readme_path.read_text(encoding="utf-8")
                if "## API / Python Wrapper" not in current_readme:
                    current_readme = current_readme.rstrip() + readme_python_section(data) + "\n"
                if "## Science-skills-style usage guide" not in current_readme:
                    current_readme = current_readme.rstrip() + readme_usage_section(data) + "\n"
                readme_path.write_text(current_readme, encoding="utf-8")
            references = folder / "references"
            references.mkdir(parents=True, exist_ok=True)
            usage_path = references / "tool_usage.md"
            if not usage_path.exists():
                usage_path.write_text(usage_reference(data), encoding="utf-8")
            examples = folder / "examples"
            examples.mkdir(parents=True, exist_ok=True)
            example_path = examples / "run-record.example.json"
            if not example_path.exists():
                example_path.write_text(
                    json.dumps(example_run_record(data), ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            api_path = folder / "api.json"
            if not api_path.exists():
                api_path.write_text(json.dumps(api_contract(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            else:
                api_data = json.loads(api_path.read_text(encoding="utf-8"))
                desired_api = api_contract(data)
                changed = False
                for key in ["usage_reference", "execution_contract"]:
                    if key not in api_data:
                        api_data[key] = desired_api[key]
                        changed = True
                if changed:
                    api_path.write_text(json.dumps(api_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            scripts = folder / "scripts"
            scripts.mkdir(parents=True, exist_ok=True)
            wrapper_path = scripts / "create_source_packet.py"
            if not wrapper_path.exists():
                wrapper_path.write_text(python_wrapper(data), encoding="utf-8")
            registry.append(data)

    registry.sort(key=lambda item: item["slug"])
    (bio_root / "registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (bio_root / "README.md").write_text(
        "# Bioinformatics Tool Scaffolds\n\n"
        "This directory contains one folder per bioinformatics tool listed in OCEAN's bioinformatics resource map.\n\n"
        "These folders are scaffolds, not claims that the tools are installed or executable in OCEAN. "
        "Use `../common/software_source_packet.py` for generic source-packet creation until a tool has a dedicated wrapper.\n\n"
        "Each tool folder includes `examples/run-record.example.json`, a template for recording inspected tool runs before "
        "they are converted into OCEAN evidence packets.\n\n"
        "Each tool folder also includes `api.json` and `scripts/create_source_packet.py`. These define a stable local "
        "wrapper contract for turning inspected run metadata into source packets; they do not install or execute external tools.\n\n"
        "Each tool folder includes `references/tool_usage.md`, a science-skills-style operation guide with use/avoid rules, "
        "required local execution evidence, stop conditions, and OCEAN handoff guidance.\n\n"
        f"Tool folders: {len(registry)}\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(registry)} tool scaffold folders to {bio_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
