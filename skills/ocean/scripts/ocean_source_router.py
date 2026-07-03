#!/usr/bin/env python3
"""OCEAN source-packet router and audit helper.

This script is intentionally stdlib-only. It does not call live APIs. It creates
route plans, records query metadata, packetizes existing JSON/text evidence, and
audits whether a packet is complete enough for OCEAN to use as evidence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROUTE_CLASSES = {
    "literature": {
        "keywords": ["paper", "literature", "pubmed", "doi", "preprint", "abstract", "review", "trial publication"],
        "resources": ["PubMed", "EuropePMC", "OpenAlex", "CrossRef", "arXiv", "bioRxiv", "medRxiv"],
    },
    "omics": {
        "keywords": ["rna", "single-cell", "scrna", "snrna", "transcriptomics", "expression", "spatial", "proteogenomic", "multi-omics", "multiomics", "gtex", "geo", "sra", "encode", "cellxgene", "hubmap"],
        "resources": ["GEO", "SRA", "ENA", "ArrayExpress", "Expression Atlas", "GTEx", "ENCODE", "Human Cell Atlas", "Single Cell Portal", "CELLxGENE", "HuBMAP", "CZ CELLxGENE"],
    },
    "epigenomics_regulatory": {
        "keywords": ["chip-seq", "chipseq", "atac", "atac-seq", "cut&run", "cuttag", "cut&tag", "methylation", "motif", "motifs", "peak", "enhancer", "tf binding", "regulatory", "jaspar"],
        "resources": ["ENCODE", "Cistrome DB", "ReMap", "JASPAR", "UCSC Genome Browser", "Roadmap Epigenomics"],
    },
    "cancer_genomics": {
        "keywords": ["cancer", "tumor", "tumour", "tcga", "gdc", "cbioportal", "icgc", "cosmic", "survival", "copy number"],
        "resources": ["TCGA/GDC", "cBioPortal", "ICGC", "COSMIC"],
    },
    "pathway_gene_set": {
        "keywords": ["pathway", "enrichment", "gene set", "go term", "reactome", "kegg", "msigdb", "gsea", "wikipathways"],
        "resources": ["Gene Ontology", "Reactome", "KEGG", "WikiPathways", "MSigDB", "GSEA resources"],
    },
    "proteomics_metabolomics": {
        "keywords": ["proteomics", "protein abundance", "peptide", "metabolomics", "metabolite", "lipidomics", "pride", "metabolights", "hmdb", "massive"],
        "resources": ["PRIDE", "ProteomeXchange", "PeptideAtlas", "MetaboLights", "HMDB", "MassIVE"],
    },
    "microbiome": {
        "keywords": ["microbiome", "metagenomics", "16s", "shotgun", "taxonomic", "mgnify", "qiita", "hmp"],
        "resources": ["MGnify", "Qiita", "Human Microbiome Project", "SRA", "ENA"],
    },
    "protein_structure": {
        "keywords": ["protein", "structure", "alphafold", "pdb", "domain", "binding", "msa", "uniprot"],
        "resources": ["UniProt", "PDB", "AlphaFold DB", "InterPro", "STRING"],
    },
    "variant_genetics": {
        "keywords": ["variant", "snp", "mutation", "clinvar", "dbsnp", "gnomad", "vep", "genome build"],
        "resources": ["ClinVar", "dbSNP", "gnomAD", "Ensembl/VEP"],
    },
    "drug_target": {
        "keywords": ["drug", "drugs", "compound", "compounds", "target", "targets", "inhibitor", "agonist", "antagonist", "chembl", "pubchem", "opentargets", "bindingdb", "drugbank", "dgidb", "pharmgkb", "ic50", "ki"],
        "resources": ["ChEMBL", "OpenTargets", "PubChem", "BindingDB", "DrugBank", "DGIdb", "PharmGKB", "OpenFDA", "UniProt"],
    },
    "clinical": {
        "keywords": ["clinical", "clinically", "trial", "trials", "clinicaltrials.gov", "registry", "patient", "cohort", "mimic", "eicu", "endpoint", "calibration", "diagnostic", "deployment", "clinical utility", "actionable", "therapy", "treatment"],
        "resources": ["ClinicalTrials.gov", "WHO ICTRP", "EU Clinical Trials Register", "OpenFDA", "clinical registries", "MIMIC/eICU when lawfully provided"],
    },
    "clinical_imaging_signal": {
        "keywords": ["image", "images", "imaging", "radiology", "ct", "mri", "x-ray", "xray", "pathology slide", "whole-slide", "wsi", "ecg", "eeg", "physionet", "tcia"],
        "resources": ["TCIA", "PhysioNet", "MIMIC-CXR when lawfully provided", "OpenNeuro", "UK Biobank when authorized"],
    },
    "regulatory_safety": {
        "keywords": ["adverse event", "adverse events", "faers", "label", "labels", "dailymed", "fda", "ema", "safety", "contraindication", "postmarket", "pharmacovigilance"],
        "resources": ["OpenFDA", "DailyMed", "FDA labels", "EMA public assessment reports", "FAERS with caveats"],
    },
    "model_organism": {
        "keywords": ["mouse", "murine", "drosophila", "fly", "worm", "yeast", "zebrafish", "arabidopsis", "mgi", "flybase", "wormbase", "sgd", "zfin", "tair"],
        "resources": ["MGI", "FlyBase", "WormBase", "SGD", "ZFIN", "TAIR"],
    },
    "benchmark": {
        "keywords": ["benchmark", "leaderboard", "challenge", "dream challenge", "baseline", "split", "test set", "external validation", "mlperf", "openml", "kaggle", "biomarker benchmark"],
        "resources": ["DREAM Challenges", "task-specific benchmark repositories", "OpenML where relevant", "Kaggle only with caution", "MLPerf where relevant"],
    },
    "bioinformatics_software": {
        "keywords": [
            "blast", "last", "lastal", "bwa", "bowtie", "bowtie2", "hisat2", "star", "minimap2",
            "samtools", "bedtools", "gatk", "bcftools", "freebayes", "deepvariant", "strelka", "mutect2",
            "salmon", "kallisto", "rsem", "stringtie", "featurecounts", "deseq2", "edger", "limma", "sleuth",
            "seurat", "scanpy", "scvi", "celltypist", "azimuth", "cell ranger", "starsolo", "alevin",
            "macs2", "macs3", "deeptools", "homer", "meme", "fimo",
            "qiime2", "dada2", "metaphlan", "humann", "kraken2", "bracken", "megahit", "spades",
            "maxquant", "fragpipe", "dia-nn", "skyline", "ms-dial", "xcms", "mzmine",
            "alphafold", "colabfold", "rosettafold", "hh-suite", "hmmer", "modeller", "pymol", "chimerax",
            "mafft", "muscle", "clustal omega", "iq-tree", "raxml", "fasttree", "orthofinder",
            "snakemake", "nextflow", "cwl", "cromwell", "wdl", "galaxy", "docker", "singularity", "apptainer", "conda", "nf-core"
        ],
        "resources": [
            "BLAST", "LAST", "BWA", "Bowtie2", "HISAT2", "STAR", "minimap2", "SAMtools",
            "BEDTools", "GATK", "bcftools", "FreeBayes", "DeepVariant", "Strelka2", "Mutect2",
            "Salmon", "kallisto", "RSEM", "StringTie", "featureCounts", "DESeq2", "edgeR", "limma-voom", "sleuth",
            "Cell Ranger", "STARsolo", "Alevin-fry", "Seurat", "Scanpy", "scVI", "CellTypist", "Azimuth",
            "MACS2/MACS3", "deepTools", "HOMER", "MEME/FIMO",
            "QIIME2", "DADA2", "MetaPhlAn", "HUMAnN", "Kraken2", "Bracken", "MEGAHIT", "SPAdes",
            "MaxQuant", "FragPipe", "DIA-NN", "Skyline", "MS-DIAL", "XCMS", "MZmine",
            "AlphaFold", "ColabFold", "RoseTTAFold", "HH-suite", "HMMER", "MODELLER", "PyMOL", "ChimeraX",
            "MAFFT", "MUSCLE", "Clustal Omega", "IQ-TREE", "RAxML", "FastTree", "OrthoFinder",
            "Snakemake", "Nextflow", "CWL", "WDL/Cromwell", "Galaxy", "Docker", "Singularity/Apptainer", "Conda", "nf-core"
        ],
    },
    "artifact": {
        "keywords": ["notebook", "code", "figure", "table", "slurm", "log", "dataset", "csv", "supplement"],
        "resources": ["local files", "notebooks", "scripts", "figures", "tables", "logs"],
    },
}

ROUTE_PACKET_FIELDS = {
    "literature": ["query", "date", "source", "PMID/DOI/preprint ID", "inspected title/abstract/full-text boundary"],
    "omics": ["accession", "organism", "assay/platform", "sample table", "condition labels", "inspected metadata fields"],
    "epigenomics_regulatory": ["assay type", "genome build", "peak/region set", "control/input", "motif database/version", "inspected fields"],
    "cancer_genomics": ["cohort", "data type", "endpoint definition", "filters", "version/access date", "analysis boundary"],
    "variant_genetics": ["variant ID", "genome build/transcript", "phenotype context", "submitter/evidence status", "date"],
    "drug_target": ["compound/target ID", "assay type", "endpoint", "organism/cell line", "concentration/unit", "date"],
    "clinical": ["registry/cohort ID", "status/date", "endpoint", "population", "access/ethics boundary"],
    "clinical_imaging_signal": ["dataset ID", "modality", "label definition", "split/provenance", "privacy/access boundary", "inspection date"],
    "regulatory_safety": ["resource", "drug/product ID", "label/adverse-event field", "date", "reporting-bias caveat"],
    "bioinformatics_software": ["tool name", "version", "command line", "parameters", "reference/index", "input files", "output files", "logs", "environment", "date"],
}

BIOINFORMATICS_SOFTWARE_NAMES = {
    name.lower()
    for name in ROUTE_CLASSES["bioinformatics_software"]["resources"]
}
BIOINFORMATICS_SOFTWARE_REQUIRED_FIELDS = [
    "tool_version",
    "command_line",
    "parameters",
    "reference_or_index",
    "input_files",
    "output_files",
    "logs_or_qc",
    "environment",
]

VALID_BOUNDARY = {"candidate_route", "retrieved_external_context", "queried_evidence", "packet_evidence"}
VALID_HANDOFF = {"Sounding", "Current", "Reef", "Iceberg", "Anchor", "Compass", "Harbor", "stop"}


def today() -> str:
    return dt.date.today().isoformat()


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def packet_id_seed(*parts: str) -> str:
    raw = "|".join(parts).encode("utf-8")
    return "osp-" + hashlib.sha1(raw).hexdigest()[:12]


def split_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def keyword_matches(text: str, keyword: str) -> bool:
    keyword = keyword.lower()
    if len(keyword) <= 3 and keyword.replace("-", "").isalnum():
        return re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", text) is not None
    if " " in keyword or "-" in keyword or "/" in keyword or "&" in keyword:
        return keyword in text
    return re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", text) is not None


def infer_routes(question: str) -> list[dict[str, Any]]:
    text = question.lower()
    routes = []
    for route_class, spec in ROUTE_CLASSES.items():
        hits = [kw for kw in spec["keywords"] if keyword_matches(text, kw)]
        if hits:
            routes.append(
                {
                    "route_class": route_class,
                    "candidate_resources": spec["resources"],
                    "matched_terms": hits,
                    "evidence_status": "candidate_route",
                    "minimum_packet_fields": ROUTE_PACKET_FIELDS.get(route_class, []),
                    "limit": "Route suggestion only; no query has been executed.",
                }
            )
    if not routes:
        routes.append(
            {
                "route_class": "literature",
                "candidate_resources": ROUTE_CLASSES["literature"]["resources"],
                "matched_terms": [],
                "evidence_status": "candidate_route",
                "minimum_packet_fields": ROUTE_PACKET_FIELDS.get("literature", []),
                "limit": "Default route; no domain-specific terms were detected.",
            }
        )
    return routes


def command_route(args: argparse.Namespace) -> int:
    data = {
        "created_at": now_iso(),
        "question": args.question,
        "claim": args.claim,
        "routes": infer_routes(" ".join(filter(None, [args.question, args.claim]))),
        "boundary_status": "candidate_route",
        "handoff": "Reef",
        "cannot_support": [
            "This route plan does not prove source existence, identifiers, mechanisms, clinical readiness, or validation."
        ],
    }
    write_json(args.output, data)
    print(f"Wrote {args.output}")
    return 0


def command_record_query(args: argparse.Namespace) -> int:
    filters = {}
    for item in args.filter or []:
        if "=" not in item:
            raise SystemExit(f"Invalid --filter value {item!r}; expected key=value")
        key, value = item.split("=", 1)
        filters[key.strip()] = value.strip()
    identifiers = split_list(args.identifiers)
    inspected = split_list(args.inspected_content)
    status = "queried_evidence" if (args.query or identifiers) and inspected else "retrieved_external_context"
    data = {
        "created_at": now_iso(),
        "resource": args.resource,
        "query": args.query,
        "filters": filters,
        "date_accessed": args.date_accessed or today(),
        "identifiers": identifiers,
        "inspected_content": inspected,
        "boundary_status": status,
        "license_or_terms_note": args.license_or_terms_note or "",
        "cannot_support": split_list(args.cannot_support),
    }
    write_json(args.output, data)
    print(f"Wrote {args.output}")
    return 0


def normalize_packet(raw: Any, args: argparse.Namespace) -> dict[str, Any]:
    if isinstance(raw, dict) and {"packet_id", "boundary_status"}.intersection(raw):
        packet = dict(raw)
    else:
        packet = {
            "raw_input_type": type(raw).__name__,
            "raw_input_preview": raw if isinstance(raw, (str, int, float)) else "",
        }
        if isinstance(raw, dict):
            for key in ["resource", "query", "filters", "date_accessed", "identifiers", "inspected_content", "boundary_status", "license_or_terms_note", "cannot_support"]:
                if key in raw:
                    packet[key] = raw[key]
        elif isinstance(raw, list):
            packet["inspected_content"] = [f"Imported list with {len(raw)} records"]

    resource = args.resource or packet.get("resource") or "unknown"
    source_type = args.source_type or packet.get("source_type") or "other"
    query = args.query if args.query is not None else packet.get("query")
    identifiers = split_list(args.identifiers) or list(packet.get("identifiers") or [])
    inspected_content = split_list(args.inspected_content) or list(packet.get("inspected_content") or [])
    cannot_support = split_list(args.cannot_support) or list(packet.get("cannot_support") or [])
    boundary_status = args.boundary_status or packet.get("boundary_status") or "retrieved_external_context"
    handoff = args.handoff or packet.get("handoff") or "Reef"

    if boundary_status not in VALID_BOUNDARY:
        raise SystemExit(f"Invalid boundary_status {boundary_status!r}; expected one of {sorted(VALID_BOUNDARY)}")
    if handoff not in VALID_HANDOFF:
        raise SystemExit(f"Invalid handoff {handoff!r}; expected one of {sorted(VALID_HANDOFF)}")

    packet.update(
        {
            "packet_id": packet.get("packet_id") or packet_id_seed(resource, str(query), ",".join(identifiers), now_iso()),
            "created_at": packet.get("created_at") or now_iso(),
            "source_type": source_type,
            "resource": resource,
            "query": query,
            "filters": packet.get("filters") or {},
            "date_accessed": packet.get("date_accessed") or today(),
            "identifiers": identifiers,
            "inspected_content": inspected_content,
            "supports_claims": split_list(args.supports_claims) or list(packet.get("supports_claims") or []),
            "cannot_support": cannot_support,
            "license_or_terms_note": args.license_or_terms_note or packet.get("license_or_terms_note") or "",
            "boundary_status": boundary_status,
            "handoff": handoff,
        }
    )
    return packet


def command_packetize(args: argparse.Namespace) -> int:
    raw_text = args.input.read_text(encoding="utf-8")
    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError:
        raw = raw_text[:5000]
    packet = normalize_packet(raw, args)
    write_json(args.output, packet)
    print(f"Wrote {args.output}")
    return 0


def audit_packet(packet: dict[str, Any]) -> tuple[list[str], list[str]]:
    missing = []
    warnings = []
    for field in ["packet_id", "source_type", "resource", "date_accessed", "boundary_status", "handoff"]:
        if not packet.get(field):
            missing.append(field)
    boundary = packet.get("boundary_status")
    if boundary not in VALID_BOUNDARY:
        missing.append("valid boundary_status")
    if packet.get("handoff") not in VALID_HANDOFF:
        missing.append("valid handoff")
    if boundary in {"queried_evidence", "packet_evidence"} and not packet.get("inspected_content"):
        missing.append("inspected_content for evidence-level packet")
    if boundary == "queried_evidence" and not (packet.get("query") or packet.get("identifiers")):
        missing.append("query or identifiers for queried_evidence")
    if boundary == "packet_evidence" and not packet.get("cannot_support"):
        warnings.append("packet_evidence should record cannot_support limitations")
    source_type = str(packet.get("source_type") or "").lower()
    resource = str(packet.get("resource") or "").lower()
    is_software_packet = (
        source_type in {"bioinformatics_software", "software", "workflow"}
        or resource in BIOINFORMATICS_SOFTWARE_NAMES
    )
    if is_software_packet and boundary in {"queried_evidence", "packet_evidence"}:
        for field in BIOINFORMATICS_SOFTWARE_REQUIRED_FIELDS:
            if not packet.get(field):
                missing.append(f"software field: {field}")
    if boundary == "candidate_route":
        warnings.append("candidate_route cannot support claims until a query/source is inspected")
        if packet.get("supports_claims"):
            missing.append("candidate_route must not include supports_claims")
    if boundary == "retrieved_external_context":
        warnings.append("retrieved_external_context is context only, not packet evidence")
    return missing, warnings


def markdown_audit(packet: dict[str, Any], missing: list[str], warnings: list[str]) -> str:
    status = "Pass" if not missing else "Incomplete"
    rows = [
        ("Packet ID", packet.get("packet_id", "")),
        ("Resource", packet.get("resource", "")),
        ("Source type", packet.get("source_type", "")),
        ("Boundary status", packet.get("boundary_status", "")),
        ("Query", packet.get("query", "")),
        ("Identifiers", ", ".join(packet.get("identifiers") or [])),
        ("Inspected content", "; ".join(packet.get("inspected_content") or [])),
        ("Can support", "; ".join(packet.get("supports_claims") or [])),
        ("Cannot support", "; ".join(packet.get("cannot_support") or [])),
        ("Handoff", packet.get("handoff", "")),
    ]
    lines = [
        "# OCEAN Source Packet Audit",
        "",
        f"- Status: {status}",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in rows)
    lines.extend(["", "## Missing fields", ""])
    lines.extend([f"- {item}" for item in missing] or ["- None"])
    lines.extend(["", "## Boundary warnings", ""])
    lines.extend([f"- {item}" for item in warnings] or ["- None"])
    lines.extend(["", "## OCEAN use", ""])
    if missing:
        lines.append("- Do not use this packet as evidence until missing fields are fixed.")
    elif packet.get("boundary_status") in {"candidate_route", "retrieved_external_context"}:
        lines.append("- Use this only as routing/context. Do not upgrade claims.")
    else:
        lines.append("- Use this as bounded packet evidence and hand off to the selected OCEAN module.")
    return "\n".join(lines) + "\n"


def command_audit_packet(args: argparse.Namespace) -> int:
    packet = read_json(args.input)
    missing, warnings = audit_packet(packet)
    text = markdown_audit(packet, missing, warnings)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 1 if missing and args.fail_on_incomplete else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OCEAN source-packet router and audit helper.")
    sub = parser.add_subparsers(dest="command", required=True)

    route = sub.add_parser("route", help="Classify a question/claim into candidate source routes.")
    route.add_argument("--question", required=True)
    route.add_argument("--claim", default="")
    route.add_argument("--output", type=Path, required=True)
    route.set_defaults(func=command_route)

    record = sub.add_parser("record-query", help="Record query metadata without claiming proof.")
    record.add_argument("--resource", required=True)
    record.add_argument("--query", default="")
    record.add_argument("--filter", action="append")
    record.add_argument("--date-accessed")
    record.add_argument("--identifiers", default="")
    record.add_argument("--inspected-content", default="")
    record.add_argument("--cannot-support", default="")
    record.add_argument("--license-or-terms-note", default="")
    record.add_argument("--output", type=Path, required=True)
    record.set_defaults(func=command_record_query)

    packetize = sub.add_parser("packetize", help="Convert an existing JSON/text file into an OCEAN source packet.")
    packetize.add_argument("--input", type=Path, required=True)
    packetize.add_argument("--output", type=Path, required=True)
    packetize.add_argument("--source-type")
    packetize.add_argument("--resource")
    packetize.add_argument("--query")
    packetize.add_argument("--identifiers", default="")
    packetize.add_argument("--inspected-content", default="")
    packetize.add_argument("--supports-claims", default="")
    packetize.add_argument("--cannot-support", default="")
    packetize.add_argument("--license-or-terms-note", default="")
    packetize.add_argument("--boundary-status", choices=sorted(VALID_BOUNDARY))
    packetize.add_argument("--handoff", choices=sorted(VALID_HANDOFF))
    packetize.set_defaults(func=command_packetize)

    audit = sub.add_parser("audit-packet", help="Audit source-packet completeness.")
    audit.add_argument("--input", type=Path, required=True)
    audit.add_argument("--output", type=Path, required=True)
    audit.add_argument("--fail-on-incomplete", action="store_true")
    audit.set_defaults(func=command_audit_packet)

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
