#!/usr/bin/env python3
"""Route a research task to domain-specific evidence standards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, stable_id, write_json


DOMAIN_STANDARDS = {
    "biomedical": {
        "required_evidence": [
            "research-object identity",
            "study design and experimental unit",
            "source provenance",
            "effect estimate and uncertainty",
            "independent validation appropriate to the claim",
        ],
        "claim_ceiling": "evidence-bounded biomedical hypothesis or finding",
        "stop_conditions": [
            "do not infer mechanism from association alone",
            "do not infer clinical utility from retrospective performance alone",
        ],
    },
    "biological": {
        "required_evidence": [
            "organism, tissue, cell type, and condition identity",
            "biological and technical replication hierarchy",
            "orthogonal or perturbational evidence for mechanism claims",
            "source and assay provenance",
        ],
        "claim_ceiling": "finding in the supplied biological context",
        "stop_conditions": [
            "do not generalize across species, tissue, cell type, or condition without evidence",
            "do not call a mechanism without decisive perturbation and controls",
        ],
    },
    "clinical": {
        "required_evidence": [
            "population and eligibility criteria",
            "site, time, and outcome definitions",
            "analysis unit and missing-data handling",
            "calibration and independent external validation",
            "prospective utility evidence for clinical-use claims",
        ],
        "claim_ceiling": "performance or association in the evaluated clinical setting",
        "stop_conditions": [
            "do not provide treatment guidance from registry, retrospective, or model evidence alone",
            "do not claim generalizability without independent site and time validation",
        ],
    },
    "biomedical_ai": {
        "required_evidence": [
            "dataset, cohort, site, and time provenance",
            "patient-level split and leakage audit",
            "comparator and benchmark fairness",
            "calibration, subgroup behavior, and external validation",
            "reproducible code, model, and environment record",
        ],
        "claim_ceiling": "bounded model performance in the evaluated datasets",
        "stop_conditions": [
            "do not equate benchmark performance with clinical utility",
            "do not call validation independent when training or upstream data overlap",
        ],
    },
    "omics": {
        "required_evidence": [
            "sample and assay identity",
            "batch, preprocessing, and quality-control provenance",
            "biological replicate and analysis-unit definition",
            "multiplicity control and effect uncertainty",
            "orthogonal validation for functional claims",
        ],
        "claim_ceiling": "omics association in the supplied sample and assay context",
        "stop_conditions": [
            "do not treat cells, reads, or features as independent biological replicates",
            "do not upgrade enrichment or differential abundance into mechanism",
        ],
    },
    "drug": {
        "required_evidence": [
            "compound identity, dose, formulation, and exposure",
            "target engagement and assay context",
            "selectivity and off-target controls",
            "replication across relevant models",
            "clinical registry or trial evidence for clinical claims",
        ],
        "claim_ceiling": "compound activity in the evaluated experimental context",
        "stop_conditions": [
            "do not infer efficacy from binding, docking, or pathway association alone",
            "do not provide clinical recommendations without appropriate trial evidence",
        ],
    },
    "materials": {
        "required_evidence": [
            "composition and material identity",
            "processing history and batch identity",
            "characterization method and instrument conditions",
            "property-test protocol and uncertainty",
            "independent batch or laboratory replication",
        ],
        "claim_ceiling": "measured property under the supplied preparation and test conditions",
        "stop_conditions": [
            "do not generalize beyond tested composition, processing, and conditions",
            "do not infer structure-property mechanism from correlation alone",
        ],
    },
    "chemistry": {
        "required_evidence": [
            "compound identity and purity",
            "reaction conditions and analytical characterization",
            "yield definition and replicate information",
            "controls supporting selectivity or mechanism",
            "source and instrument provenance",
        ],
        "claim_ceiling": "observed chemical result under the supplied conditions",
        "stop_conditions": [
            "do not claim identity from a single insufficient analytical signal",
            "do not claim mechanism from product formation alone",
        ],
    },
    "engineering": {
        "required_evidence": [
            "system requirements and operating envelope",
            "hardware, software, and calibration versions",
            "test protocol, load, and environmental conditions",
            "failure modes and uncertainty",
            "independent repeat or deployment evidence",
        ],
        "claim_ceiling": "system performance under the evaluated operating conditions",
        "stop_conditions": [
            "do not generalize reliability outside the tested operating envelope",
            "do not treat simulation-only results as deployed-system validation",
        ],
    },
}


def route(payload: dict) -> dict:
    requested = str(payload.get("domain", "")).strip().casefold()
    standards = DOMAIN_STANDARDS.get(requested)
    recognized = standards is not None
    if not recognized:
        standards = {
            "required_evidence": [
                "domain identity",
                "research-object identity",
                "source provenance",
                "claim-specific validation standard",
            ],
            "claim_ceiling": "unclassified hypothesis pending domain review",
            "stop_conditions": [
                "do not issue a domain-specific conclusion until the domain is classified"
            ],
        }
    supplied = set(payload.get("available_evidence", []))
    missing = [
        item for item in standards["required_evidence"] if item not in supplied
    ]
    return {
        "schema_version": "ocean-domain-lens-v1",
        "routing_id": stable_id("domain", payload),
        "task_id": payload.get("task_id", ""),
        "requested_domain": requested or "unspecified",
        "recognized": recognized,
        "supported_domains": sorted(DOMAIN_STANDARDS),
        "research_object": payload.get("research_object", ""),
        "claim_type": payload.get("claim_type", ""),
        "required_evidence": standards["required_evidence"],
        "available_evidence": sorted(supplied),
        "missing_evidence": missing,
        "maximum_safe_claim": standards["claim_ceiling"],
        "stop_conditions": standards["stop_conditions"],
        "evidence_boundary": evidence_boundary(
            inspected=[
                "declared domain, research object, claim type, and evidence labels"
            ],
            not_inspected=[
                "source content",
                "scientific correctness of supplied evidence labels",
                "domain-expert judgment",
            ],
            cannot_conclude=[
                "scientific validity from routing alone",
                "that missing evidence is absent rather than undeclared",
            ],
            next_required=(
                [f"provide or inspect: {item}" for item in missing]
                if recognized
                else ["classify the domain with a qualified reviewer"]
            ),
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply an OCEAN domain evidence lens.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = route(read_json(args.input))
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "requested_domain": result["requested_domain"],
                "recognized": result["recognized"],
                "missing_evidence": len(result["missing_evidence"]),
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
