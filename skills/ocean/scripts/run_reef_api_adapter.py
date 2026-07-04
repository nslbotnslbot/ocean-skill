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
    "alphafold-db": {
        "label": "AlphaFold DB",
        "resource_role": "Predicted protein structure metadata and confidence files by UniProt accession",
        "official_doc": "https://alphafold.ebi.ac.uk/api-docs",
        "endpoint_family": "https://alphafold.ebi.ac.uk/api/prediction/",
        "supports": "Traceable predicted-structure metadata lookup by UniProt accession.",
        "does_not_support": "Experimental structure proof, binding proof, mechanism, druggability, or functional rescue.",
    },
    "chembl": {
        "label": "ChEMBL",
        "resource_role": "Bioactive molecules, targets, assays, and drug-like compound metadata",
        "official_doc": "https://chembl.gitbook.io/chembl-interface-documentation/web-services",
        "endpoint_family": "https://www.ebi.ac.uk/chembl/api/data/",
        "supports": "Traceable molecule/target/assay metadata discovery.",
        "does_not_support": "Efficacy, safety, clinical utility, or mechanism from database presence alone.",
    },
    "clinvar": {
        "label": "ClinVar via NCBI E-utilities",
        "resource_role": "Public variant clinical-significance records and ClinVar metadata",
        "official_doc": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
        "endpoint_family": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
        "supports": "Traceable ClinVar record discovery and public metadata retrieval planning.",
        "does_not_support": "Clinical diagnosis, treatment guidance, or variant pathogenicity without inspected record details and expert interpretation.",
    },
    "europepmc": {
        "label": "Europe PMC",
        "resource_role": "Literature metadata, abstracts, preprints, and publication identifiers",
        "official_doc": "https://europepmc.org/RestfulWebService",
        "endpoint_family": "https://www.ebi.ac.uk/europepmc/webservices/rest/",
        "supports": "Traceable literature metadata and abstract-level source discovery.",
        "does_not_support": "Full-paper methods/results quality, peer-review status, mechanism, or clinical efficacy unless source text is inspected.",
    },
    "gnomad": {
        "label": "gnomAD",
        "resource_role": "Population variant frequency and constraint metadata",
        "official_doc": "https://gnomad.broadinstitute.org/help/api",
        "endpoint_family": "https://gnomad.broadinstitute.org/api",
        "supports": "Population-frequency or constraint-resource provenance for specified variants/genes.",
        "does_not_support": "Pathogenicity, diagnosis, treatment, or clinical actionability from frequency alone.",
    },
    "ncbi-eutils": {
        "label": "NCBI E-utilities",
        "resource_role": "PubMed, Gene, GEO, SRA, Protein, PMC, and other Entrez metadata",
        "official_doc": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
        "endpoint_family": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
        "supports": "Traceable Entrez record search and public metadata retrieval planning.",
        "does_not_support": "Full-paper evidence, mechanism, causality, clinical efficacy, or absence-of-evidence claims.",
    },
    "pubmed": {
        "label": "PubMed via NCBI E-utilities",
        "resource_role": "PubMed literature metadata",
        "official_doc": "https://www.ncbi.nlm.nih.gov/books/NBK25501/",
        "endpoint_family": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
        "supports": "Traceable PubMed record discovery and public metadata retrieval planning.",
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
    "quickgo": {
        "label": "QuickGO",
        "resource_role": "Gene Ontology term and annotation metadata",
        "official_doc": "https://www.ebi.ac.uk/QuickGO/api/index.html",
        "endpoint_family": "https://www.ebi.ac.uk/QuickGO/services/",
        "supports": "Traceable GO term or annotation metadata discovery.",
        "does_not_support": "Direct molecular mechanism, causality, or phenotype proof from annotation presence alone.",
    },
    "reactome": {
        "label": "Reactome",
        "resource_role": "Curated pathway and reaction metadata",
        "official_doc": "https://reactome.org/dev/content-service",
        "endpoint_family": "https://reactome.org/ContentService/",
        "supports": "Traceable pathway/resource discovery and pathway-context provenance.",
        "does_not_support": "Pathway activity, causality, disease mechanism, or treatment effect without experimental support.",
    },
    "string": {
        "label": "STRING",
        "resource_role": "Protein identifier mapping and protein-protein association metadata",
        "official_doc": "https://string-db.org/help/api/",
        "endpoint_family": "https://string-db.org/api/",
        "supports": "Traceable STRING identifier mapping or association-resource provenance.",
        "does_not_support": "Physical binding, direct mechanism, causality, or disease relevance from association scores alone.",
    },
    "uniprot": {
        "label": "UniProt",
        "resource_role": "Protein metadata, function, taxonomy, sequence, and cross-references",
        "official_doc": "https://www.uniprot.org/help/api",
        "endpoint_family": "https://rest.uniprot.org/",
        "supports": "Traceable protein accession, reviewed/unreviewed status, sequence, and annotation metadata.",
        "does_not_support": "New functional proof, mechanism, causality, or clinical utility without primary evidence.",
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


def bounded_items(value: Any, limit: int) -> list[Any]:
    if isinstance(value, list):
        return value[:limit]
    return []


def compact_dict(item: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: item.get(key) for key in keys if key in item and item.get(key) not in [None, "", []]}


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
    adapter = "clinvar" if args.adapter == "clinvar" else "pubmed" if args.adapter == "pubmed" else "ncbi-eutils"
    database = "clinvar" if adapter == "clinvar" else "pubmed" if adapter == "pubmed" else args.database
    params = {
        "db": database,
        "term": args.query,
        "retmode": "json",
        "retmax": str(args.retmax),
    }
    url = ADAPTERS[args.adapter]["endpoint_family"] + "esearch.fcgi?" + urllib.parse.urlencode(params)
    packet["query"] = {
        "database": database,
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


def build_uniprot_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    if args.accession:
        url = f"https://rest.uniprot.org/uniprotkb/{urllib.parse.quote(args.accession)}.json"
        packet["query"] = {"accession": args.accession}
    else:
        params = {
            "query": args.query,
            "format": "json",
            "size": str(args.retmax),
            "fields": "accession,id,protein_name,gene_names,organism_name,reviewed",
        }
        url = "https://rest.uniprot.org/uniprotkb/search?" + urllib.parse.urlencode(params)
        packet["query"] = {"query": args.query, "retmax": args.retmax}
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    if args.accession:
        records = [data]
    else:
        records = bounded_items(data.get("results"), args.retmax)
    compact = []
    for record in records:
        genes = record.get("genes") or []
        compact.append(
            {
                "primaryAccession": record.get("primaryAccession"),
                "uniProtkbId": record.get("uniProtkbId"),
                "reviewed": record.get("entryType"),
                "proteinDescription": record.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value"),
                "genes": [gene.get("geneName", {}).get("value") for gene in genes if isinstance(gene, dict) and gene.get("geneName")],
                "organism": record.get("organism", {}).get("scientificName"),
            }
        )
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(compact),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "records": compact,
        "inspected_fields": ["primaryAccession", "uniProtkbId", "entryType", "proteinDescription", "genes", "organism"],
    }
    return packet


def build_europepmc_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    params = {"query": args.query, "format": "json", "pageSize": str(args.retmax)}
    url = ADAPTERS["europepmc"]["endpoint_family"] + "search?" + urllib.parse.urlencode(params)
    packet["query"] = {"query": args.query, "pageSize": args.retmax}
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    records = bounded_items(data.get("resultList", {}).get("result"), args.retmax)
    compact = [
        compact_dict(record, ["id", "source", "pmid", "pmcid", "doi", "title", "journalTitle", "pubYear", "authorString"])
        for record in records
        if isinstance(record, dict)
    ]
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(compact),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "hit_count": data.get("hitCount"),
        "records": compact,
        "inspected_fields": ["id", "source", "pmid", "pmcid", "doi", "title", "journalTitle", "pubYear", "authorString"],
    }
    return packet


def build_chembl_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    params = {"pref_name__icontains": args.query, "limit": str(args.retmax), "format": "json"}
    url = ADAPTERS["chembl"]["endpoint_family"] + "molecule.json?" + urllib.parse.urlencode(params)
    packet["query"] = {"pref_name__icontains": args.query, "limit": args.retmax}
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    molecules = bounded_items(data.get("molecules"), args.retmax)
    compact = [
        compact_dict(molecule, ["molecule_chembl_id", "pref_name", "max_phase", "molecule_type", "first_approval"])
        for molecule in molecules
        if isinstance(molecule, dict)
    ]
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(compact),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "records": compact,
        "inspected_fields": ["molecule_chembl_id", "pref_name", "max_phase", "molecule_type", "first_approval"],
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


def build_string_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    params = {
        "identifiers": args.identifier or args.query,
        "species": str(args.species),
        "limit": str(args.retmax),
    }
    url = ADAPTERS["string"]["endpoint_family"] + "json/get_string_ids?" + urllib.parse.urlencode(params)
    packet["query"] = params
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    records = bounded_items(data, args.retmax)
    compact = [
        compact_dict(record, ["queryItem", "stringId", "preferredName", "ncbiTaxonId", "annotation"])
        for record in records
        if isinstance(record, dict)
    ]
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(compact),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "records": compact,
        "inspected_fields": ["queryItem", "stringId", "preferredName", "ncbiTaxonId", "annotation"],
    }
    return packet


def build_reactome_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    params = {"query": args.query, "pageSize": str(args.retmax), "page": "1"}
    if args.species_name:
        params["species"] = args.species_name
    url = ADAPTERS["reactome"]["endpoint_family"] + "search/query?" + urllib.parse.urlencode(params)
    packet["query"] = params
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    results = bounded_items(data.get("results"), args.retmax)
    compact = []
    for result in results:
        if isinstance(result, dict):
            compact.append(compact_dict(result, ["stId", "dbId", "name", "schemaClass", "speciesName"]))
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(compact),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "records": compact,
        "inspected_fields": ["stId", "dbId", "name", "schemaClass", "speciesName"],
    }
    return packet


def build_quickgo_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    params = {"query": args.query, "limit": str(args.retmax), "page": "1"}
    url = ADAPTERS["quickgo"]["endpoint_family"] + "ontology/go/search?" + urllib.parse.urlencode(params)
    packet["query"] = params
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    results = bounded_items(data.get("results"), args.retmax)
    compact = [
        compact_dict(record, ["id", "name", "definition", "aspect", "isObsolete"])
        for record in results
        if isinstance(record, dict)
    ]
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(compact),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "records": compact,
        "inspected_fields": ["id", "name", "definition", "aspect", "isObsolete"],
    }
    return packet


def build_gnomad_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    query = """
    query variant($variantId: String!, $dataset: DatasetId!) {
      variant(variantId: $variantId, dataset: $dataset) {
        variant_id
        reference_genome
        chrom
        pos
        ref
        alt
        exome { ac an af }
        genome { ac an af }
      }
    }
    """
    body = {
        "query": query,
        "variables": {"variantId": args.variant_id, "dataset": args.gnomad_dataset},
    }
    packet["query"] = {"variant_id": args.variant_id, "dataset": args.gnomad_dataset}
    packet["query_url_or_endpoint"] = ADAPTERS["gnomad"]["endpoint_family"]
    packet["request_body"] = body
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(ADAPTERS["gnomad"]["endpoint_family"], method="POST", body=body, timeout=args.timeout)
    variant = data.get("data", {}).get("variant")
    compact = compact_dict(variant or {}, ["variant_id", "reference_genome", "chrom", "pos", "ref", "alt", "exome", "genome"])
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": 1 if compact else 0,
        "failure_or_limit": "" if compact else "No variant returned for supplied variant ID/dataset.",
        "response": metadata,
    }
    packet["result_summary"] = {
        "variant": compact,
        "inspected_fields": ["variant_id", "reference_genome", "chrom", "pos", "ref", "alt", "exome.ac/an/af", "genome.ac/an/af"],
    }
    return packet


def build_alphafold_db_packet(args: argparse.Namespace) -> dict[str, Any]:
    packet = base_packet(args)
    accession = args.accession or args.query
    url = ADAPTERS["alphafold-db"]["endpoint_family"] + urllib.parse.quote(accession)
    packet["query"] = {"uniprot_accession": accession}
    packet["query_url_or_endpoint"] = url
    packet["query_log"]["status"] = "dry-run"
    if not args.execute:
        return packet

    data, metadata = request_json(url, timeout=args.timeout)
    records = bounded_items(data, args.retmax)
    compact = [
        compact_dict(record, ["entryId", "gene", "uniprotAccession", "uniprotId", "organismScientificName", "modelCreatedDate", "latestVersion"])
        for record in records
        if isinstance(record, dict)
    ]
    packet["query_log"] = {
        "status": "executed",
        "records_inspected": len(compact),
        "failure_or_limit": "",
        "response": metadata,
    }
    packet["result_summary"] = {
        "records": compact,
        "inspected_fields": ["entryId", "gene", "uniprotAccession", "uniprotId", "organismScientificName", "modelCreatedDate", "latestVersion"],
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
    parser.add_argument("--accession", help="Protein accession for UniProt or AlphaFold DB.")
    parser.add_argument("--identifier", help="Gene/protein identifier for identifier-mapping APIs such as STRING.")
    parser.add_argument("--ensembl-id", help="Ensembl gene ID for Open Targets target lookup.")
    parser.add_argument("--variant-id", help="gnomAD variant ID such as 1-55516888-G-A.")
    parser.add_argument("--gnomad-dataset", default="gnomad_r4", help="gnomAD dataset id for GraphQL variant lookup.")
    parser.add_argument("--species", type=int, default=9606, help="NCBI taxonomy ID for species-aware adapters.")
    parser.add_argument("--species-name", default="Homo sapiens", help="Species name for Reactome search.")
    parser.add_argument("--retmax", type=int, default=5, help="Maximum records to inspect for search-style adapters.")
    parser.add_argument("--execute", action="store_true", help="Actually call the public API. Default is dry-run.")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--out", type=Path, default=Path("outputs/reef_api_packet.json"))
    parser.add_argument("--markdown-out", type=Path)
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    if args.retmax < 1 or args.retmax > 25:
        raise SystemExit("--retmax must be between 1 and 25 for bounded Reef queries.")
    if args.adapter in {"ncbi-eutils", "pubmed", "clinvar", "clinicaltrials", "europepmc", "chembl", "quickgo", "reactome"} and not args.query:
        raise SystemExit(f"--query is required for {args.adapter}.")
    if args.adapter == "uniprot" and not (args.query or args.accession):
        raise SystemExit("--query or --accession is required for uniprot.")
    if args.adapter == "alphafold-db" and not (args.query or args.accession):
        raise SystemExit("--accession or --query is required for alphafold-db.")
    if args.adapter == "opentargets" and not args.ensembl_id:
        raise SystemExit("--ensembl-id is required for opentargets.")
    if args.adapter == "string" and not (args.identifier or args.query):
        raise SystemExit("--identifier or --query is required for string.")
    if args.adapter == "gnomad" and not args.variant_id:
        raise SystemExit("--variant-id is required for gnomad.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    validate_args(args)
    builders = {
        "alphafold-db": build_alphafold_db_packet,
        "chembl": build_chembl_packet,
        "clinvar": build_ncbi_packet,
        "ncbi-eutils": build_ncbi_packet,
        "pubmed": build_ncbi_packet,
        "clinicaltrials": build_clinicaltrials_packet,
        "europepmc": build_europepmc_packet,
        "gnomad": build_gnomad_packet,
        "opentargets": build_opentargets_packet,
        "quickgo": build_quickgo_packet,
        "reactome": build_reactome_packet,
        "string": build_string_packet,
        "uniprot": build_uniprot_packet,
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
