#!/usr/bin/env python3
"""Unified command router for OCEAN evidence-control utilities."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


SCRIPT_ROOT = Path(__file__).resolve().parent

DIRECT = {
    "doctor": SCRIPT_ROOT / "runtime/ocean_doctor.py",
    "credentials": SCRIPT_ROOT / "runtime/safe_credentials.py",
    "licenses": SCRIPT_ROOT / "runtime/license_registry.py",
    "source-packet": SCRIPT_ROOT / "runtime/source_packet.py",
    "manifest": SCRIPT_ROOT / "runtime/run_manifest.py",
    "ledger": SCRIPT_ROOT / "runtime/harbor_ledger.py",
    "domain-lens": SCRIPT_ROOT / "runtime/domain_lens.py",
}

GROUPED = {
    "paper": {
        "prepare": SCRIPT_ROOT / "ingest/prepare_paper.py",
        "source-map": SCRIPT_ROOT / "ingest/build_source_map.py",
        "artifacts": SCRIPT_ROOT / "ingest/extract_figures_tables.py",
        "grounding": SCRIPT_ROOT / "ingest/audit_source_grounding.py",
    },
    "workflow": {
        "variant": SCRIPT_ROOT / "workflows/variant_evidence/run_workflow.py",
        "target-disease": SCRIPT_ROOT / "workflows/target_disease/run_workflow.py",
        "manuscript": SCRIPT_ROOT / "workflows/manuscript_reliability/run_workflow.py",
    },
    "detect": {
        "independence": SCRIPT_ROOT / "detectors/evidence_independence.py",
        "circularity": SCRIPT_ROOT / "detectors/circularity.py",
        "leakage": SCRIPT_ROOT / "detectors/leakage.py",
        "claim-validation": SCRIPT_ROOT / "detectors/claim_to_validation.py",
        "diff": SCRIPT_ROOT / "detectors/evidence_diff.py",
    },
    "audit": {
        "statistics-design": SCRIPT_ROOT / "audit/statistics/design_parser.py",
        "statistics-unit": SCRIPT_ROOT / "audit/statistics/unit_of_analysis_checker.py",
        "statistics-multiplicity": SCRIPT_ROOT / "audit/statistics/multiplicity_checker.py",
        "statistics-figure": SCRIPT_ROOT / "audit/statistics/figure_statistics_checker.py",
        "statistics-claim": SCRIPT_ROOT / "audit/statistics/statistical_claim_mapper.py",
        "data-availability": SCRIPT_ROOT / "audit/data_availability.py",
        "citation-link": SCRIPT_ROOT / "audit/references/citation_claim_linker.py",
        "citation-scope": SCRIPT_ROOT / "audit/references/citation_scope_checker.py",
        "citation-entailment": SCRIPT_ROOT / "audit/references/entailment_auditor.py",
        "citation-metadata": SCRIPT_ROOT / "audit/references/metadata_verifier.py",
    },
    "bridge": {
        "grounded-reader": SCRIPT_ROOT / "bridges/grounded_reader_bridge.py",
        "scientific-tool": SCRIPT_ROOT / "bridges/scientific_tool_bridge.py",
        "generic-cli": SCRIPT_ROOT / "bridges/generic_cli_bridge.py",
        "mcp": SCRIPT_ROOT / "bridges/mcp_output_bridge.py",
        "envelope": SCRIPT_ROOT / "bridges/artifact_envelope.py",
        "distill": SCRIPT_ROOT / "bridges/harbor_to_skill_distiller.py",
    },
}


def usage() -> str:
    lines = [
        "OCEAN evidence-control CLI",
        "",
        "Usage:",
        "  ocean.py <command> [arguments]",
        "  ocean.py <group> <command> [arguments]",
        "",
        "Direct commands: " + ", ".join(sorted(DIRECT)),
    ]
    for group, commands in GROUPED.items():
        lines.append(f"{group}: " + ", ".join(sorted(commands)))
    lines.extend(
        [
            "",
            "Examples:",
            "  ocean.py doctor --output outputs/doctor.json",
            "  ocean.py source-packet create --help",
            "  ocean.py paper prepare --help",
            "  ocean.py workflow variant --help",
        ]
    )
    return "\n".join(lines)


def resolve(argv: list[str]) -> tuple[Path, list[str]]:
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(usage())
        raise SystemExit(0)
    first = argv[0]
    if first in DIRECT:
        return DIRECT[first], argv[1:]
    if first in GROUPED:
        if len(argv) < 2 or argv[1] not in GROUPED[first]:
            choices = ", ".join(sorted(GROUPED[first]))
            raise SystemExit(f"{first} requires one of: {choices}")
        return GROUPED[first][argv[1]], argv[2:]
    raise SystemExit(f"Unknown command: {first}\n\n{usage()}")


def main(argv: list[str] | None = None) -> int:
    script, forwarded = resolve(list(argv if argv is not None else sys.argv[1:]))
    completed = subprocess.run(
        [sys.executable, str(script), *forwarded],
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
