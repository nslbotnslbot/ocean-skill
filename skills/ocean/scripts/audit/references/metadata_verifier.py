#!/usr/bin/env python3
"""Verify DOI metadata offline or through the public Crossref REST API."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


def normalize(value: str) -> str:
    return " ".join(value.casefold().split())


def crossref_lookup(doi: str, mailto: str, timeout: int) -> dict:
    query = f"?{urlencode({'mailto': mailto})}" if mailto else ""
    url = f"https://api.crossref.org/works/{quote(doi, safe='')}{query}"
    request = Request(
        url,
        headers={"User-Agent": "OCEAN-evidence-audit/0.2 (https://github.com/nslbotnslbot/ocean-skill)"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        return {"lookup_status": "failed", "error": str(exc), "url": url}
    message = payload.get("message", {})
    published = message.get("published-print") or message.get("published-online") or {}
    date_parts = published.get("date-parts", [[]])
    year = date_parts[0][0] if date_parts and date_parts[0] else None
    authors = [
        " ".join(part for part in (author.get("given", ""), author.get("family", "")) if part)
        for author in message.get("author", [])
    ]
    return {
        "lookup_status": "retrieved",
        "url": url,
        "doi": message.get("DOI", ""),
        "title": (message.get("title") or [""])[0],
        "year": year,
        "authors": authors,
        "container_title": (message.get("container-title") or [""])[0],
        "volume": message.get("volume", ""),
        "issue": message.get("issue", ""),
        "page": message.get("page", ""),
        "type": message.get("type", ""),
    }


def compare(record: dict, observed: dict) -> dict:
    expected = record.get("expected", {})
    comparisons = {}
    for field in ("doi", "title", "container_title", "volume", "issue", "page"):
        if field in expected:
            comparisons[field] = normalize(str(expected[field])) == normalize(str(observed.get(field, "")))
    if "year" in expected:
        comparisons["year"] = str(expected["year"]) == str(observed.get("year", ""))
    if "first_author" in expected:
        observed_first = (observed.get("authors") or [""])[0]
        comparisons["first_author"] = normalize(expected["first_author"]) in normalize(observed_first)
    return {
        "citation_id": record.get("citation_id", ""),
        "doi": record.get("doi", ""),
        "lookup_status": observed.get("lookup_status", "not_checked"),
        "comparisons": comparisons,
        "all_checked_fields_match": bool(comparisons) and all(comparisons.values()),
        "observed": observed,
    }


def verify(payload: dict, live: bool, mailto: str, timeout: int) -> dict:
    rows = []
    for index, record in enumerate(payload.get("citations", [])):
        if live:
            observed = crossref_lookup(record.get("doi", ""), mailto, timeout)
            if index + 1 < len(payload.get("citations", [])):
                time.sleep(0.34)
        else:
            observed = record.get("observed", {"lookup_status": "not_checked"})
        rows.append(compare(record, observed))
    mismatches = [
        row["citation_id"]
        for row in rows
        if row["comparisons"] and not row["all_checked_fields_match"]
    ]
    return {
        "schema_version": "ocean-reference-metadata-audit-v1",
        "mode": "live_crossref" if live else "offline_comparison",
        "citations": rows,
        "summary": {
            "total": len(rows),
            "mismatches": len(mismatches),
            "lookup_failures": sum(row["lookup_status"] == "failed" for row in rows),
        },
        "evidence_boundary": evidence_boundary(
            inspected=["declared fields and retrieved/provided bibliographic metadata"],
            not_inspected=["full text", "citation entailment", "publisher corrections not present in metadata"],
            cannot_conclude=["that a bibliographically valid citation supports a manuscript claim"],
            next_required=(
                [f"resolve metadata mismatch: {citation_id}" for citation_id in mismatches]
                or ["link each citation to a claim and audit scope/entailment"]
            ),
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify citation metadata.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--mailto", default="")
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args(argv)
    result = verify(read_json(args.input), args.live, args.mailto, args.timeout)
    write_json(args.output, result)
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
