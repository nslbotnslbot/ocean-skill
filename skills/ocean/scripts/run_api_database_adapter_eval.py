#!/usr/bin/env python3
"""Evaluate OCEAN Reef API/database adapters.

Default mode is dry-run and does not make network requests. Use
`--execute-live` to run bounded live API calls and record any API/network
failures without inventing unavailable evidence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


CASES = [
    {
        "case_id": "API-R1-UNIPROT",
        "adapter": "uniprot",
        "args": ["--accession", "P04637"],
        "expected_query_key": "accession",
    },
    {
        "case_id": "API-R1-PUBMED",
        "adapter": "pubmed",
        "args": ["--query", "TP53"],
        "expected_query_key": "term",
    },
    {
        "case_id": "API-R1-EUROPEPMC",
        "adapter": "europepmc",
        "args": ["--query", "TP53"],
        "expected_query_key": "query",
    },
    {
        "case_id": "API-R1-CHEMBL",
        "adapter": "chembl",
        "args": ["--query", "aspirin"],
        "expected_query_key": "pref_name__icontains",
    },
    {
        "case_id": "API-R1-OPENTARGETS",
        "adapter": "opentargets",
        "args": ["--ensembl-id", "ENSG00000141510"],
        "expected_query_key": "ensembl_id",
    },
    {
        "case_id": "API-R1-STRING",
        "adapter": "string",
        "args": ["--identifier", "TP53"],
        "expected_query_key": "identifiers",
    },
    {
        "case_id": "API-R1-REACTOME",
        "adapter": "reactome",
        "args": ["--query", "TP53"],
        "expected_query_key": "query",
    },
    {
        "case_id": "API-R1-QUICKGO",
        "adapter": "quickgo",
        "args": ["--query", "apoptosis"],
        "expected_query_key": "query",
    },
    {
        "case_id": "API-R1-CLINVAR",
        "adapter": "clinvar",
        "args": ["--query", "BRCA1"],
        "expected_query_key": "term",
    },
    {
        "case_id": "API-R1-GNOMAD",
        "adapter": "gnomad",
        "args": ["--variant-id", "11-5227002-T-A"],
        "expected_query_key": "variant_id",
    },
    {
        "case_id": "API-R1-ALPHAFOLDDB",
        "adapter": "alphafold-db",
        "args": ["--accession", "P04637"],
        "expected_query_key": "uniprot_accession",
    },
    {
        "case_id": "API-R1-CLINICALTRIALS",
        "adapter": "clinicaltrials",
        "args": ["--query", "melanoma"],
        "expected_query_key": "query.term",
    },
    {
        "case_id": "API-R1-NCBI-EUTILS",
        "adapter": "ncbi-eutils",
        "args": ["--database", "gene", "--query", "TP53"],
        "expected_query_key": "term",
    },
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# OCEAN API/Database Adapter Eval R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Mode: {summary['mode']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        "",
        "| Case | Adapter | Status | Records | Verdict | Notes |",
        "|---|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['case_id']} | {row['adapter']} | {row['query_status']} | {row['records_inspected']} | {row['verdict']} | {row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Evidence Boundary / 证据边界",
            "",
            "This eval checks that OCEAN can construct bounded Reef packets for API/database resources. Dry-run mode validates query construction and packet contracts without network calls. Live mode performs bounded public API requests, records failures as failures or needs-review, and still does not claim biological mechanism, clinical utility, or scientific validity.",
        ]
    )
    return "\n".join(lines) + "\n"


def evaluate_case(case: dict[str, Any], args: argparse.Namespace, runner: Path, case_dir: Path) -> dict[str, Any]:
    out = case_dir / f"{case['adapter']}.json"
    command = [
        sys.executable,
        str(runner),
        "--adapter",
        case["adapter"],
        "--retmax",
        str(args.retmax),
        "--timeout",
        str(args.timeout),
        "--out",
        str(out),
        *case["args"],
    ]
    if args.execute_live:
        command.append("--execute")
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    packet = read_json(out) if out.exists() else {}
    query = packet.get("query", {})
    query_log = packet.get("query_log", {})
    boundary = packet.get("evidence_boundary", {})
    expected_query_ok = case["expected_query_key"] in query
    boundary_ok = all(key in boundary for key in ["can_support", "cannot_support", "privacy_or_access", "handoff"])
    status = query_log.get("status", "")
    records = query_log.get("records_inspected", 0)
    if args.execute_live:
        status_ok = status in {"executed", "error"}
        no_subprocess_error = proc.returncode == 0
        live_failure = status == "error" or (isinstance(records, int) and records == 0)
        verdict = "pass" if no_subprocess_error and status_ok and expected_query_ok and boundary_ok and not live_failure else "needs_review"
    else:
        verdict = "pass" if proc.returncode == 0 and status == "dry-run" and expected_query_ok and boundary_ok else "needs_review"
    notes = ""
    if proc.returncode != 0:
        notes = (proc.stderr or proc.stdout).strip().replace("\n", " ")[:180]
    elif query_log.get("failure_or_limit"):
        notes = str(query_log.get("failure_or_limit"))[:180]
    return {
        "case_id": case["case_id"],
        "adapter": case["adapter"],
        "mode": "live" if args.execute_live else "dry-run",
        "command": command,
        "packet_path": str(out),
        "returncode": proc.returncode,
        "query_status": status,
        "records_inspected": records,
        "expected_query_ok": expected_query_ok,
        "boundary_ok": boundary_ok,
        "verdict": verdict,
        "notes": notes,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Reef API/database adapters.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--execute-live", action="store_true", help="Run bounded live API calls.")
    parser.add_argument("--retmax", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args(argv)

    runner = args.skill_dir / "scripts" / "run_reef_api_adapter.py"
    mode = "live" if args.execute_live else "dry-run"
    case_dir = args.outdir / f"api-database-adapter-r1-{mode}-packets"
    rows = [evaluate_case(case, args, runner, case_dir) for case in CASES]
    summary = {
        "run_date": dt.date.today().isoformat(),
        "mode": mode,
        "cases": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "adapters": [case["adapter"] for case in CASES],
        "boundary": "API/database packet construction only; not scientific validation.",
    }
    prefix = f"api-database-adapter-r1-{mode}"
    write_json(args.outdir / f"{prefix}-results.json", rows)
    write_json(args.outdir / f"{prefix}-summary.json", summary)
    (args.outdir / f"{prefix}-results.md").write_text(make_markdown(rows, summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
