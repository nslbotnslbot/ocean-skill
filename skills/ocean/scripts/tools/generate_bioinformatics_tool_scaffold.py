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
"""


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
            registry.append(data)

    registry.sort(key=lambda item: item["slug"])
    (bio_root / "registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (bio_root / "README.md").write_text(
        "# Bioinformatics Tool Scaffolds\n\n"
        "This directory contains one folder per bioinformatics tool listed in OCEAN's bioinformatics resource map.\n\n"
        "These folders are scaffolds, not claims that the tools are installed or executable in OCEAN. "
        "Use `../common/software_source_packet.py` for generic source-packet creation until a tool has a dedicated wrapper.\n\n"
        f"Tool folders: {len(registry)}\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(registry)} tool scaffold folders to {bio_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
