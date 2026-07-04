#!/usr/bin/env python3
"""AlphaFold DB source-packet helper for OCEAN.

This helper is intentionally stdlib-only. It can fetch public AlphaFold DB
files when explicitly requested, but all evals use local mock files.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import statistics
import sys
import time
import urllib.error
import urllib.request


AFDB_BASE = "https://alphafold.ebi.ac.uk/files"


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_uniprot(accession: str) -> str:
    value = accession.strip()
    if not value or not value.replace("-", "").isalnum():
        raise SystemExit("Provide a UniProt accession-like identifier, not a protein/gene name.")
    return value


def fetch_url(url: str, output: Path, delay_seconds: float = 0.4) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    time.sleep(delay_seconds)
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
            output.write_bytes(data)
            return {
                "url": url,
                "path": str(output),
                "status": response.status,
                "bytes": len(data),
                "content_type": response.headers.get("content-type", ""),
            }
    except urllib.error.HTTPError as exc:
        return {"url": url, "path": str(output), "status": exc.code, "error": str(exc)}
    except urllib.error.URLError as exc:
        return {"url": url, "path": str(output), "status": "url_error", "error": str(exc)}


def command_fetch(args: argparse.Namespace) -> int:
    accession = validate_uniprot(args.uniprot)
    version = args.version
    stem = f"AF-{accession}-F1"
    targets = {
        "metadata": f"{AFDB_BASE}/{stem}-metadata_v{version}.json",
        "pae": f"{AFDB_BASE}/{stem}-predicted_aligned_error_v{version}.json",
        "cif": f"{AFDB_BASE}/{stem}-model_v{version}.cif",
    }
    outputs = {}
    for label, url in targets.items():
        suffix = url.rsplit("/", 1)[-1]
        outputs[label] = fetch_url(url, args.outdir / suffix, args.delay_seconds)
    manifest = {
        "created_at": now_iso(),
        "resource": "AlphaFold DB",
        "uniprot": accession,
        "version": version,
        "files": outputs,
        "license_terms_note": "User must check AlphaFold DB/EMBL-EBI terms before reuse.",
    }
    write_json(args.outdir / f"{stem}-ocean-fetch-manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def extract_plddt_values(metadata) -> list[float]:
    candidates = []
    if isinstance(metadata, dict):
        for key in ["confidenceScore", "plddt", "pLDDT", "perResidueConfidenceScore"]:
            value = metadata.get(key)
            if isinstance(value, list):
                candidates.extend(float(item) for item in value if isinstance(item, (int, float)))
        if "structures" in metadata and isinstance(metadata["structures"], list):
            for item in metadata["structures"]:
                if isinstance(item, dict):
                    candidates.extend(extract_plddt_values(item))
    elif isinstance(metadata, list):
        for item in metadata:
            if isinstance(item, dict):
                candidates.extend(extract_plddt_values(item))
            elif isinstance(item, (int, float)):
                candidates.append(float(item))
    return candidates


def parse_cif_bfactor_plddt(path: Path) -> list[float]:
    values = []
    if not path:
        return values
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        parts = line.split()
        numeric = []
        for part in parts:
            try:
                numeric.append(float(part))
            except ValueError:
                pass
        if numeric:
            candidate = numeric[-1]
            if 0 <= candidate <= 100:
                values.append(candidate)
    return values


def summarize_plddt(values: list[float]) -> dict:
    if not values:
        return {
            "available": False,
            "conclusion": "No pLDDT values inspected.",
            "mean_plddt": None,
            "fraction_below_50": None,
            "fraction_above_90": None,
        }
    mean_value = statistics.mean(values)
    below_50 = sum(1 for value in values if value < 50) / len(values)
    above_90 = sum(1 for value in values if value >= 90) / len(values)
    if below_50 >= 0.4:
        conclusion = "High low-confidence/disorder signal; whole-protein structural interpretation is unsafe."
    elif mean_value >= 80 and above_90 >= 0.3:
        conclusion = "Mostly confident predicted structure, subject to PAE/domain checks."
    else:
        conclusion = "Mixed confidence; restrict claims to confident regions."
    return {
        "available": True,
        "residue_count": len(values),
        "mean_plddt": round(mean_value, 2),
        "min_plddt": round(min(values), 2),
        "max_plddt": round(max(values), 2),
        "fraction_below_50": round(below_50, 3),
        "fraction_above_90": round(above_90, 3),
        "conclusion": conclusion,
    }


def normalize_pae_matrix(raw) -> list[list[float]]:
    if isinstance(raw, dict):
        for key in ["predicted_aligned_error", "pae", "distance"]:
            value = raw.get(key)
            if isinstance(value, list):
                return [[float(item) for item in row] for row in value]
        if "pae" in raw and isinstance(raw["pae"], dict):
            return normalize_pae_matrix(raw["pae"])
    if isinstance(raw, list):
        if raw and isinstance(raw[0], dict):
            for item in raw:
                matrix = normalize_pae_matrix(item)
                if matrix:
                    return matrix
        if raw and isinstance(raw[0], list):
            return [[float(item) for item in row] for row in raw]
    return []


def summarize_pae(matrix: list[list[float]]) -> dict:
    if not matrix:
        return {
            "available": False,
            "conclusion": "No PAE matrix inspected.",
            "mean_pae": None,
        }
    flattened = [value for row in matrix for value in row]
    n = len(matrix)
    mean_pae = statistics.mean(flattened)
    high_pairs = sum(1 for value in flattened if value >= 15) / max(1, len(flattened))
    conclusion = "High inter-residue uncertainty; avoid rigid whole-protein conclusions." if high_pairs >= 0.35 else "PAE does not show a dominant high-uncertainty signal at this coarse level."
    return {
        "available": True,
        "matrix_size": n,
        "mean_pae": round(mean_pae, 2),
        "fraction_pairs_above_15": round(high_pairs, 3),
        "conclusion": conclusion,
    }


def command_analyze(args: argparse.Namespace) -> int:
    plddt_values = []
    inspected = []
    if args.metadata:
        metadata = read_json(args.metadata)
        plddt_values.extend(extract_plddt_values(metadata))
        inspected.append(str(args.metadata))
    if args.cif:
        plddt_values.extend(parse_cif_bfactor_plddt(args.cif))
        inspected.append(str(args.cif))
    pae_summary = {"available": False, "conclusion": "No PAE matrix inspected.", "mean_pae": None}
    if args.pae:
        pae_summary = summarize_pae(normalize_pae_matrix(read_json(args.pae)))
        inspected.append(str(args.pae))
    analysis = {
        "created_at": now_iso(),
        "resource": "AlphaFold DB",
        "uniprot": args.uniprot or "",
        "inspected_files": inspected,
        "plddt_summary": summarize_plddt(plddt_values),
        "pae_summary": pae_summary,
        "cannot_support": [
            "binding proof",
            "experimental function",
            "disease mechanism",
            "drug efficacy",
            "clinical relevance",
        ],
    }
    write_json(args.output, analysis)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
    return 0


def command_packet(args: argparse.Namespace) -> int:
    analysis = read_json(args.analysis)
    inspected = analysis.get("inspected_files", [])
    plddt = analysis.get("plddt_summary", {})
    pae = analysis.get("pae_summary", {})
    packet = {
        "packet_id": f"osp-afdb-{analysis.get('uniprot') or 'unknown'}-{dt.date.today().isoformat()}",
        "created_at": now_iso(),
        "source_type": "predicted_structure_database",
        "resource": "AlphaFold DB",
        "query": f"AlphaFold DB predicted structure analysis for {analysis.get('uniprot') or 'unknown UniProt'}",
        "filters": {"adapter": "afdb_source_packet.py"},
        "date_accessed": dt.date.today().isoformat(),
        "identifiers": [analysis.get("uniprot")] if analysis.get("uniprot") else [],
        "inspected_content": inspected + ["pLDDT summary", "PAE summary"],
        "supports_claims": [
            plddt.get("conclusion", "bounded pLDDT confidence assessment"),
            pae.get("conclusion", "bounded PAE assessment"),
        ],
        "cannot_support": analysis.get("cannot_support", []),
        "license_or_terms_note": "Check AlphaFold DB/EMBL-EBI terms before reuse.",
        "boundary_status": "packet_evidence" if inspected else "retrieved_external_context",
        "handoff": args.handoff,
    }
    write_json(args.output, packet)
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AlphaFold DB helper for OCEAN source packets.")
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="Fetch AlphaFold DB files for a UniProt accession.")
    fetch.add_argument("--uniprot", required=True)
    fetch.add_argument("--outdir", type=Path, required=True)
    fetch.add_argument("--version", default="6")
    fetch.add_argument("--delay-seconds", type=float, default=0.4)
    fetch.set_defaults(func=command_fetch)

    analyze = sub.add_parser("analyze", help="Analyze local AFDB metadata/PAE/mmCIF files.")
    analyze.add_argument("--metadata", type=Path)
    analyze.add_argument("--pae", type=Path)
    analyze.add_argument("--cif", type=Path)
    analyze.add_argument("--uniprot", default="")
    analyze.add_argument("--output", type=Path, required=True)
    analyze.set_defaults(func=command_analyze)

    packet = sub.add_parser("packet", help="Convert an AFDB analysis JSON into an OCEAN source packet.")
    packet.add_argument("--analysis", type=Path, required=True)
    packet.add_argument("--output", type=Path, required=True)
    packet.add_argument("--handoff", default="Iceberg", choices=["Reef", "Iceberg", "Anchor", "Compass", "Harbor", "stop"])
    packet.set_defaults(func=command_packet)

    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
