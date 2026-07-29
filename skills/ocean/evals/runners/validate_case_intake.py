#!/usr/bin/env python3
"""Validate benchmark case intake and research-readiness gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT_ROOT = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    evidence_boundary,
    read_json,
    schema_path,
    validate_required_contract,
    write_json,
)


def validate(payload: dict, required_count: int, base_dir: Path) -> dict:
    cases = payload.get("cases", [])
    schema = schema_path(
        str(SCRIPT_ROOT / "ocean.py"),
        "benchmark_case.schema.json",
    )
    errors = []
    seen = set()
    for index, case in enumerate(cases):
        case_id = case.get("case_id", "")
        if case_id in seen:
            errors.append(f"case {index + 1}: duplicate case_id {case_id}")
        seen.add(case_id)
        errors.extend(
            f"case {index + 1}: {error}"
            for error in validate_required_contract(case, schema)
        )
    scientific_cases = sum(
        case.get("scientific_evidence") is True for case in cases
    )
    expert_ready = 0
    permitted_sources = 0
    adjudication_schema = schema_path(
        str(SCRIPT_ROOT / "ocean.py"),
        "adjudication_record.schema.json",
    )
    for index, case in enumerate(cases, start=1):
        provenance = case.get("provenance", {})
        if (
            provenance.get("source_identifier")
            and provenance.get("redistribution_status") == "permitted"
        ):
            permitted_sources += 1
        record_value = case.get("adjudication_record")
        if not record_value:
            continue
        record_path = Path(record_value)
        if not record_path.is_absolute():
            record_path = base_dir / record_path
        if not record_path.is_file():
            errors.append(
                f"case {index}: adjudication record unavailable: {record_path}"
            )
            continue
        record = read_json(record_path)
        record_errors = validate_required_contract(
            record,
            adjudication_schema,
        )
        if record_errors:
            errors.extend(
                f"case {index} adjudication: {error}"
                for error in record_errors
            )
            continue
        if record.get("case_id") != case.get("case_id"):
            errors.append(f"case {index}: adjudication case_id mismatch")
            continue
        if (
            record.get("blinding_state") == "blinded"
            and len(record.get("reviewers", [])) >= 2
            and case.get("blinding_state") == "blinded"
        ):
            expert_ready += 1
    gates = {
        "minimum_case_count": len(cases) >= required_count,
        "all_cases_contract_valid": not errors,
        "all_case_ids_unique": len(seen) == len(cases),
        "all_cases_are_scientific_evidence": (
            bool(cases) and scientific_cases == len(cases)
        ),
        "all_sources_traceable_and_permitted": (
            bool(cases) and permitted_sources == len(cases)
        ),
        "all_cases_blinded_and_adjudicated": (
            bool(cases) and expert_ready == len(cases)
        ),
    }
    return {
        "schema_version": "ocean-case-intake-report-v1",
        "required_count": required_count,
        "case_count": len(cases),
        "scientific_evidence_cases": scientific_cases,
        "traceable_permitted_sources": permitted_sources,
        "blinded_adjudicated_cases": expert_ready,
        "gates": gates,
        "research_ready": all(gates.values()),
        "errors": errors,
        "evidence_boundary": evidence_boundary(
            inspected=["case contracts and declared adjudication references"],
            not_inspected=[
                "source truth",
                "expert identity",
                "adjudication record contents",
                "case leakage",
            ],
            cannot_conclude=[
                "benchmark validity from case count or schema validity alone"
            ],
            next_required=[
                "independently verify sources, blinding, expert adjudication, and leakage"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OCEAN benchmark case intake.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--required-count", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    if args.required_count < 1:
        raise SystemExit("--required-count must be positive")
    result = validate(
        read_json(args.input),
        args.required_count,
        args.input.resolve().parent,
    )
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "case_count": result["case_count"],
                "required_count": result["required_count"],
                "research_ready": result["research_ready"],
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0 if result["research_ready"] or not args.strict else 1


if __name__ == "__main__":
    raise SystemExit(main())
