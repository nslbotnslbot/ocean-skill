#!/usr/bin/env python3
"""Gate a validated Harbor workflow before creating a reusable skill skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, stable_id, write_json


REQUIREMENTS = {
    "complete_execution_record": "workflow was executed end to end at least once",
    "stable_input_contract": "input contract is explicit and stable",
    "stable_output_contract": "output contract is explicit and stable",
    "input_contract": "the reusable input contract is included",
    "output_contract": "the reusable output contract is included",
    "provenance_complete": "critical steps preserve provenance",
    "positive_case": "at least one positive case exists",
    "negative_case": "at least one negative case exists",
    "failure_case": "at least one failure case exists",
    "stop_conditions": "stop conditions are explicit",
    "eval_case": "an executable evaluation case exists",
    "privacy_check": "privacy review passed",
    "license_check": "license review passed",
    "user_approval": "user explicitly approved distillation",
}


def evaluate(payload: dict) -> dict:
    checks = []
    for field, description in REQUIREMENTS.items():
        value = payload.get(field)
        passed = value is True or (
            field in {
                "input_contract",
                "output_contract",
                "stop_conditions",
                "positive_case",
                "negative_case",
                "failure_case",
                "eval_case",
            }
            and bool(value)
        )
        checks.append(
            {
                "requirement": field,
                "description": description,
                "passed": passed,
            }
        )
    eligible = all(item["passed"] for item in checks)
    return {
        "schema_version": "ocean-harbor-to-skill-gate-v1",
        "distillation_id": stable_id("distill", payload),
        "workflow_name": payload.get("workflow_name", ""),
        "eligible": eligible,
        "checks": checks,
        "missing_requirements": [
            item["requirement"] for item in checks if not item["passed"]
        ],
        "evidence_boundary": evidence_boundary(
            inspected=["declared workflow validation and approval fields"],
            not_inspected=["undeclared runs, private data, and external legal obligations"],
            cannot_conclude=["that a generated skill is scientifically correct or publication-ready"],
            next_required=(
                [item["description"] for item in checks if not item["passed"]]
                or ["review generated skeleton before adding it to a public repository"]
            ),
        ),
    }


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9-]+", "-", value.casefold().replace("_", "-")).strip("-")
    if not slug:
        raise SystemExit("workflow_name cannot be converted to a safe skill slug")
    return slug


def emit_skeleton(payload: dict, target_root: Path) -> Path:
    slug = safe_slug(payload["workflow_name"])
    skill_dir = target_root / slug
    if skill_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing directory: {skill_dir}")
    skill_dir.mkdir(parents=True)
    description = payload.get(
        "description",
        "Reusable workflow distilled from a provenance-complete OCEAN Harbor record.",
    )
    skill_text = (
        "---\n"
        f"name: {slug}\n"
        f"description: {description}\n"
        "---\n\n"
        f"# {payload['workflow_name']}\n\n"
        "## Input Contract\n\n"
        f"{json.dumps(payload.get('input_contract', {}), ensure_ascii=False, indent=2)}\n\n"
        "## Output Contract\n\n"
        f"{json.dumps(payload.get('output_contract', {}), ensure_ascii=False, indent=2)}\n\n"
        "## Stop Conditions\n\n"
        + "\n".join(f"- {item}" for item in payload.get("stop_conditions", []))
        + "\n"
    )
    (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
    return skill_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gate and optionally distill a Harbor workflow.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skeleton-root", type=Path)
    args = parser.parse_args(argv)
    payload = read_json(args.input)
    report = evaluate(payload)
    if args.skeleton_root:
        if not report["eligible"]:
            write_json(args.output, report)
            raise SystemExit(
                "Distillation blocked: " + ", ".join(report["missing_requirements"])
            )
        report["skeleton_path"] = str(emit_skeleton(payload, args.skeleton_root))
    write_json(args.output, report)
    print(json.dumps({"eligible": report["eligible"], "missing": report["missing_requirements"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
