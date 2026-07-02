#!/usr/bin/env python3
"""Create bounded Reef API packets from selected public biomedical APIs.

Default mode is dry-run: the script records the query plan without making a
network request. Use --execute only after the Reef evidence boundary is clear.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request
from typing import Any


ADAPTERS = {
    "ncbi-eutils": {
        "label": "NCBI E-utilities",
        "resource_role": "PubMed, Gene, GEO, SRA, Protein, PMC, and other Entrez metadata",
        "official_doc": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
        "endpoint_family": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
        "supports": "Traceable Entrez record search and public metadata retrieval planning.",
        "does_not_support": "Full-paper evidence, mechanism, causality, clinical efficacy, or absence-of-evidence claims.",
    },
    "clinicaltrials": {
        "label": "ClinicalTrials.gov",
        "resource_role": "Clinical trial registry metadata",
        "official_doc": "https://clinicaltrials.gov/data-api/api",
        "endpoint_family": "https://clinicaltrials.gov/api/v2/",
        "supports": "Study existence, registration status, design metadata, and posted registry fields.",
        "does_not_support": "Treatment efficacy or clinical guidance unless results and publications are inspected.",
    },
    "opentargets": {
        "label": "Open Targets Platform",
        "resource_role": "Target, disease, drug, variant, and target-disease association context",
        "official_doc": "https://platform-docs.opentargets.org/data-access/graphql-api",
        "endpoint_family": "https://api.platform.opentargets.org/api/v4/graphql",
        "supports": "Target annotation and association-resource provenance.",
        "does_not_support": "Mechanism, therapeutic efficacy, or clinical readiness from association scores alone.",
    },
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def request_json(url: str, *, method: str = "GET", body: dict[str, Any] | None = None, timeout: int = 30) -> tuple[dict[str, Any], dict[str, Any]]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "OCEAN-Reef-Adapter/0.1",
    }
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()
        response_text = raw.decode("utf-8", errors="replace")
        parsed = json.loads(response_text)
        metadata = {
            "status_code": getattr(response, "status", None),
            "content_type": response.headers.get("content-type", ""),
            "bytes": len(raw),
        }
        return parsed, metadata


def base_packet(args: argparse.Namespace) -> dict[str, Any]:
    adapter = ADAPTERS[args.adapter]
    return {
        "ocean_module": "Reef",
        "adapter": args.adapter,
        "adapter_label": adapter["label"],
        "created_utc": utc_now(),
        "executed": bool(args.execute),
        "official_doc": adapter["official_doc"],
        "endpoint_family": adapter["endpoint_family"],
        "resource_role": adapter["resource_role"],
        "query": {},
        "query_url_or_endpoint": "",
        "request_body": None,
        "query_log": {
            "status": "planned",
            "records_inspected": 0,
            "failure_or_limit": "",
        },
        "result_summary": {},
        "evidence_boundary": {
            "can_support": adapter["supports"],
            "cannot_support": adapter["does_not_support"],
            "privacy_or_access": "Public metadata request only. Do not submit private manuscript text, patient data, PHI, or unpublished data.",
            "handoff": "Use this packet as Reef resource evidence for Iceberg, Anchor, or Compass. Do not treat it as primary experimental validation.",
        },
    }


def build_ncbi_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    params = {
        "db": args.database,
        "term": args.query,
        "retmode": "json",
        "retmax": str(args.retmax),
    }
    url = ADAPTERS["ncbi-eutils"]["endpoint_family"] + "esearch.fcgi?" + urllib.parse.urlencode(params)
    packet["query"] = {
        "database": args.database,
        "term": args.query,
        "retmax": args.retmax,
    }
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    result = data.get("esearchresult", {})
    ids = result.get("idlist", [])
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(ids),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "reported_count": result.get("count"),
        "returned_ids": ids,
        "query_translation": result.get("querytranslation"),
        "inspected_fields": ["esearchresult.count", "esearchresult.idlist", "esearchresult.querytranslation"],
    }
    return packet


def build_clinicaltrials_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    params = {
        "query.term": args.query,
        "pageSize": str(args.retmax),
        "format": "json",
    }
    url = ADAPTERS["clinicaltrials"]["endpoint_family"] + "studies?" + urllib.parse.urlencode(params)
    packet["query"] = {
        "query.term": args.query,
        "pageSize": args.retmax,
    }
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    studies = data.get("studies", [])
    nct_ids = []
    statuses = []
    for study in studies[: args.retmax]:
        protocol = study.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        if ident.get("nctId"):
            nct_ids.append(ident["nctId"])
        if status.get("overallStatus"):
            statuses.append(status["overallStatus"])
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(studies),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "returned_nct_ids": nct_ids,
        "overall_status_values_seen": sorted(set(statuses)),
        "inspected_fields": [
            "protocolSection.identificationModule.nctId",
            "protocolSection.statusModule.overallStatus",
        ],
    }
    return packet


def build_opentargets_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    query = """
    query target($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        id
        approvedSymbol
        approvedName
        biotype
      }
    }
    """
    body = {
        "query": query,
        "variables": {"ensemblId": args.ensembl_id},
    }
    packet["query"] = {"ensembl_id": args.ensembl_id}
    packet["query_url_or_endpoint"] = ADAPTERS["opentargets"]["endpoint_family"]
    packet["request_body"] = body
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(
        ADAPTERS["opentargets"]["endpoint_family"],
        method="POST",
        body=body,
        timeout=args.timeout,
    )
    target = data.get("data", {}).get("target")
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": 1 if target else 0,
        "failure_or_limit": "" if target else "No target returned for supplied Ensembl ID.",
        "response": metadata,
    }
    packet["result_summary"] = {
        "target": target,
        "inspected_fields": ["target.id", "target.approvedSymbol", "target.approvedName", "target.biotype"],
    }
    return packet


def packet_to_markdown(packet: dict[str, Any]) -> str:
    boundary = packet["evidence_boundary"]
    query_log = packet["query_log"]
    result_summary = packet.get("result_summary") or {}
    result_preview = json.dumps(result_summary, ensure_ascii=False, indent=2)
    return "\n".join([
        "# Reef API Resource Packet",
        "",
        "## 一、Query Plan",
        "",
        f"- Adapter: {packet['adapter_label']} (`{packet['adapter']}`)",
        f"- Official documentation: {packet['official_doc']}",
        f"- Endpoint family: {packet['endpoint_family']}",
        f"- Executed: {packet['executed']}",
        f"- Query date UTC: {packet['created_utc']}",
        f"- Query target: `{json.dumps(packet['query'], ensure_ascii=False)}`",
        "",
        "## 二、Query Log",
        "",
        f"- Status: {query_log.get('status')}",
        f"- Records inspected: {query_log.get('records_inspected')}",
        f"- Failure/limit: {query_log.get('failure_or_limit') or 'None'}",
        "",
        "## 三、Resource Provenance",
        "",
        f"- Resource role: {packet['resource_role']}",
        f"- Query URL or endpoint: `{packet['query_url_or_endpoint']}`",
        "",
        "## 四、Evidence Boundary",
        "",
        f"- Can support: {boundary['can_support']}",
        f"- Cannot support: {boundary['cannot_support']}",
        f"- Privacy/access: {boundary['privacy_or_access']}",
        f"- Handoff: {boundary['handoff']}",
        "",
        "## 五、Result Summary",
        "",
        "```json",
        result_preview,
        "```",
        "",
    ])


def write_packet(packet: dict[str, Any], out: Path, markdown_out: Path | None) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if markdown_out is None:
        markdown_out = out.with_suffix(".md")
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.write_text(packet_to_markdown(packet), encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create bounded Reef API packets.")
    parser.add_argument("--adapter", choices=sorted(ADAPTERS), required=True)
    parser.add_argument("--query", help="Search term for NCBI E-utilities or ClinicalTrials.gov.")
    parser.add_argument("--database", default="pubmed", help="NCBI Entrez database, e.g. pubmed, gene, geo, sra.")
    parser.add_argument("--ensembl-id", help="Ensembl gene ID for Open Targets target lookup.")
    parser.add_argument("--retmax", type=int, default=5, help="Maximum records to inspect for search-style adapters.")
    parser.add_argument("--execute", action="store_true", help="Actually call the public API. Default is dry-run.")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--out", type=Path, default=Path("outputs/reef_api_packet.json"))
    parser.add_argument("--markdown-out", type=Path)
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    if args.retmax < 1 or args.retmax > 25:
        raise SystemExit("--retmax must be between 1 and 25 for bounded Reef queries.")
    if args.adapter in {"ncbi-eutils", "clinicaltrials"} and not args.query:
        raise SystemExit(f"--query is required for {args.adapter}.")
    if args.adapter == "opentargets" and not args.ensembl_id:
        raise SystemExit("--ensembl-id is required for opentargets.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    validate_args(args)
    builders = {
        "ncbi-eutils": build_ncbi_packet,
        "clinicaltrials": build_clinicaltrials_packet,
        "opentargets": build_opentargets_packet,
    }
    try:
        packet = builders[args.adapter](args)
    except Exception as exc:
        packet = base_packet(args)
        packet["query_log"] = {
            "status": "error",
            "records_inspected": 0,
            "failure_or_limit": f"{type(exc).__name__}: {exc}",
        }
    write_packet(packet, args.out, args.markdown_out)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
