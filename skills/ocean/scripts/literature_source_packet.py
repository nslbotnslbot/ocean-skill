#!/usr/bin/env python3
"""Literature source-packet helper for OCEAN.

Supports PubMed/EuropePMC live fetch, local JSON analysis, and OCEAN packet
creation. Evals use local mock records only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_json(url: str, output: Path) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    output.write_bytes(data)
    try:
        parsed = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        parsed = {"raw_preview": data.decode("utf-8", errors="ignore")[:2000]}
    return {"url": url, "path": str(output), "bytes": len(data), "parsed": parsed}


def command_fetch_pubmed(args: argparse.Namespace) -> int:
    params = urllib.parse.urlencode({"db": "pubmed", "term": args.query, "retmode": "json", "retmax": args.retmax})
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"
    result = fetch_json(url, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_fetch_europepmc(args: argparse.Namespace) -> int:
    params = urllib.parse.urlencode({"query": args.query, "format": "json", "pageSize": args.retmax})
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}"
    result = fetch_json(url, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def first_value(record: dict, keys: list[str], default=""):
    for key in keys:
        value = record.get(key)
        if value:
            return value
    return default


def normalize_record(raw) -> dict:
    if isinstance(raw, dict) and "resultList" in raw:
        records = raw.get("resultList", {}).get("result", [])
        raw = records[0] if records else raw
    if isinstance(raw, dict) and "records" in raw:
        records = raw.get("records", [])
        raw = records[0] if records else raw
    if not isinstance(raw, dict):
        return {"raw_type": type(raw).__name__}
    title = first_value(raw, ["title", "articleTitle", "name"])
    abstract = first_value(raw, ["abstractText", "abstract", "abstractTextList"])
    identifiers = []
    for key in ["pmid", "PMID", "doi", "DOI", "pmcid", "PMCID", "id"]:
        value = raw.get(key)
        if value:
            identifiers.append(f"{key}:{value}")
    return {
        "title": title,
        "abstract": abstract if isinstance(abstract, str) else json.dumps(abstract, ensure_ascii=False)[:2000],
        "journal": first_value(raw, ["journalTitle", "journal", "source"]),
        "year": first_value(raw, ["pubYear", "year", "publicationYear"]),
        "authors": raw.get("authorString") or raw.get("authors") or "",
        "identifiers": identifiers,
        "raw_keys": sorted(raw.keys()),
    }


def command_analyze(args: argparse.Namespace) -> int:
    raw = read_json(args.input)
    record = normalize_record(raw)
    inspected = ["title/metadata"]
    if record.get("abstract"):
        inspected.append("abstract")
    analysis = {
        "created_at": now_iso(),
        "resource": args.resource,
        "query": args.query or "",
        "record": record,
        "inspected_content": inspected,
        "supports_claims": ["source identity", "title/abstract-level framing"],
        "cannot_support": [
            "full methods quality",
            "full results quality",
            "figure/table evidence",
            "causal mechanism",
            "clinical efficacy",
            "publication readiness",
        ],
    }
    write_json(args.output, analysis)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
    return 0


def command_packet(args: argparse.Namespace) -> int:
    analysis = read_json(args.analysis)
    record = analysis["record"]
    packet = {
        "packet_id": f"osp-literature-{dt.date.today().isoformat()}",
        "created_at": now_iso(),
        "source_type": "literature_record",
        "resource": analysis.get("resource", "literature"),
        "query": analysis.get("query", ""),
        "filters": {"adapter": "literature_source_packet.py"},
        "date_accessed": dt.date.today().isoformat(),
        "identifiers": record.get("identifiers", []),
        "inspected_content": analysis.get("inspected_content", []),
        "supports_claims": analysis.get("supports_claims", []),
        "cannot_support": analysis.get("cannot_support", []),
        "license_or_terms_note": "Check PubMed/EuropePMC/source terms before reuse.",
        "boundary_status": "queried_evidence",
        "handoff": args.handoff,
    }
    write_json(args.output, packet)
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Literature source-packet helper for OCEAN.")
    sub = parser.add_subparsers(dest="command", required=True)
    fetch_pubmed = sub.add_parser("fetch-pubmed")
    fetch_pubmed.add_argument("--query", required=True)
    fetch_pubmed.add_argument("--retmax", default="5")
    fetch_pubmed.add_argument("--output", type=Path, required=True)
    fetch_pubmed.set_defaults(func=command_fetch_pubmed)
    fetch_epmc = sub.add_parser("fetch-europepmc")
    fetch_epmc.add_argument("--query", required=True)
    fetch_epmc.add_argument("--retmax", default="5")
    fetch_epmc.add_argument("--output", type=Path, required=True)
    fetch_epmc.set_defaults(func=command_fetch_europepmc)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("--input", type=Path, required=True)
    analyze.add_argument("--resource", default="local literature record")
    analyze.add_argument("--query", default="")
    analyze.add_argument("--output", type=Path, required=True)
    analyze.set_defaults(func=command_analyze)
    packet = sub.add_parser("packet")
    packet.add_argument("--analysis", type=Path, required=True)
    packet.add_argument("--output", type=Path, required=True)
    packet.add_argument("--handoff", default="Sounding", choices=["Sounding", "Current", "Iceberg", "Harbor", "stop"])
    packet.set_defaults(func=command_packet)
    return parser


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
