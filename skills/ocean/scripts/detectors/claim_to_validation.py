#!/usr/bin/env python3
"""Compile a scientific claim into an evidence-bound validation contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    evidence_boundary,
    schema_path,
    stable_id,
    validate_required_contract,
    write_json,
)


RULES = {
    "mechanism": {
        "keywords": ["mechanism", "mechanistic", "机制", "mediates", "drives"],
        "required": [
            "independent observational evidence",
            "perturbation evidence",
            "orthogonal assay",
            "dose or time response",
            "rescue or reversal experiment",
            "context-specific validation",
        ],
        "controls": [
            "negative and positive perturbation controls",
            "orthogonal measurement of the proposed mediator",
            "rescue or reversal of the phenotype",
        ],
        "pass": [
            "perturbation changes the proposed mediator and outcome in the predicted direction",
            "orthogonal assay confirms the effect",
            "rescue or reversal reduces a plausible alternative explanation",
        ],
        "safe": "prioritized mechanistic hypothesis",
        "stop": "Do not use 'demonstrates a mechanism' before independent perturbation and orthogonal evidence.",
    },
    "causal": {
        "keywords": ["causes", "causal", "leads to", "导致", "因果"],
        "required": [
            "temporality",
            "controlled intervention or credible causal identification",
            "confounder assessment",
            "independent replication",
        ],
        "controls": ["negative control exposure/outcome", "sensitivity analysis", "intervention or natural experiment"],
        "pass": ["effect persists under prespecified causal assumptions and sensitivity checks"],
        "safe": "association consistent with a causal hypothesis",
        "stop": "Do not state causality from association, prediction, or database co-occurrence alone.",
    },
    "clinical_utility": {
        "keywords": ["clinical utility", "clinical benefit", "treatment guidance", "临床应用", "指导治疗"],
        "required": [
            "independent external validation",
            "calibration",
            "decision-curve or utility analysis",
            "prospective workflow evaluation",
            "safety and subgroup assessment",
        ],
        "controls": ["current standard-of-care comparator", "prospective or temporal holdout", "failure-mode analysis"],
        "pass": ["prespecified clinical action improves a patient-relevant or workflow outcome without unacceptable harm"],
        "safe": "candidate for clinical evaluation",
        "stop": "Do not claim clinical utility from retrospective discrimination metrics alone.",
    },
    "diagnostic": {
        "keywords": ["diagnostic", "diagnosis", "detects disease", "诊断"],
        "required": [
            "blinded reference-standard comparison",
            "representative spectrum",
            "external validation",
            "sensitivity, specificity, calibration, and uncertainty",
        ],
        "controls": ["reference standard", "clinically relevant comparator", "spectrum-bias assessment"],
        "pass": ["prespecified diagnostic performance holds in an independent target population"],
        "safe": "diagnostic candidate requiring external validation",
        "stop": "Do not claim diagnostic readiness from case-control or internal validation alone.",
    },
    "prognostic": {
        "keywords": ["prognostic", "predicts outcome", "risk prediction", "预后", "风险预测"],
        "required": [
            "patient-level split",
            "temporal or external validation",
            "calibration",
            "clinically relevant comparator",
        ],
        "controls": ["leakage audit", "baseline model", "subgroup and missingness analysis"],
        "pass": ["performance and calibration persist under an external or temporal evaluation"],
        "safe": "prognostic association or internally validated prediction",
        "stop": "Do not claim transportability or utility without external evidence.",
    },
    "technical_performance": {
        "keywords": ["outperforms", "state-of-the-art", "sota", "better than", "性能优于"],
        "required": [
            "frozen evaluation protocol",
            "fair comparator tuning",
            "independent test set",
            "uncertainty and repeated runs",
        ],
        "controls": ["matched input information", "same split and metric", "ablation study"],
        "pass": ["prespecified advantage persists across repeated runs and a fair independent benchmark"],
        "safe": "higher observed performance under the evaluated setting",
        "stop": "Do not claim general superiority from one split or unmatched comparators.",
    },
    "association": {
        "keywords": ["associated", "correlated", "association", "相关", "关联"],
        "required": ["defined population", "effect estimate", "uncertainty", "multiplicity and confounder assessment"],
        "controls": ["negative controls where feasible", "replication cohort"],
        "pass": ["direction and effect estimate replicate with controlled multiplicity"],
        "safe": "observed association in the evaluated data",
        "stop": "Do not upgrade association to mechanism or causality.",
    },
    "database_relation": {
        "keywords": ["database", "knowledge graph", "co-occurrence", "数据库", "知识图谱"],
        "required": ["source provenance", "evidence-type separation", "independent non-overlapping validation"],
        "controls": ["source-overlap audit", "manual primary-source check"],
        "pass": ["relation is confirmed by evidence independent of database construction"],
        "safe": "database-supported candidate relation",
        "stop": "Do not treat database co-occurrence or KG edges as validated mechanism.",
    },
    "reproducibility": {
        "keywords": ["reproducible", "reproduced", "复现", "可复现"],
        "required": ["run manifest", "environment lock", "input checksums", "independent rerun"],
        "controls": ["fresh environment rerun", "output checksum or tolerance comparison"],
        "pass": ["independent rerun recreates prespecified outputs within tolerance"],
        "safe": "documented workflow prepared for reproducibility testing",
        "stop": "Do not claim reproducibility from code availability or one successful run alone.",
    },
    "novelty": {
        "keywords": ["novel", "first", "unprecedented", "新颖", "首次"],
        "required": ["dated search strategy", "scope definition", "closest-prior-work comparison"],
        "controls": ["independent literature search", "preprint and registry coverage"],
        "pass": ["no materially equivalent prior work is found under a documented search scope"],
        "safe": "potentially novel within the searched scope",
        "stop": "Do not claim 'first' without a documented and current search boundary.",
    },
}


def infer_claim_type(text: str) -> str:
    lowered = text.casefold()
    for claim_type, rule in RULES.items():
        if any(keyword.casefold() in lowered for keyword in rule["keywords"]):
            return claim_type
    return "unknown"


def compile_claim(
    claim_text: str,
    claim_type: str | None,
    evidence_classes: list[str],
    source_locators: list[str],
) -> dict:
    resolved_type = claim_type or infer_claim_type(claim_text)
    if resolved_type not in RULES:
        required = ["claim-type clarification", "source locators", "appropriate independent evidence"]
        controls = ["domain-expert review"]
        pass_criteria = ["claim type and evidence requirement are explicitly resolved"]
        safe_claim = "unclassified hypothesis"
        stop = "Do not strengthen an unclassified claim."
    else:
        rule = RULES[resolved_type]
        required = rule["required"]
        controls = rule["controls"]
        pass_criteria = rule["pass"]
        safe_claim = rule["safe"]
        stop = rule["stop"]
    normalized_current = {item.casefold() for item in evidence_classes}
    missing = [
        item
        for item in required
        if not any(token in item.casefold() for token in normalized_current)
    ]
    claim_id = stable_id("claim", {"text": claim_text, "type": resolved_type})
    payload = {
        "schema_version": "ocean-validation-card-v1",
        "validation_id": stable_id("validation", {"claim_id": claim_id, "required": required}),
        "claim_id": claim_id,
        "claim_text": claim_text,
        "claim_type": resolved_type,
        "current_evidence_classes": evidence_classes,
        "source_locators": source_locators,
        "required_evidence_classes": required,
        "independence_requirement": "At least one decisive validation source must not derive from the discovery source family.",
        "decisive_controls": controls,
        "pass_criteria": pass_criteria,
        "missing_evidence": missing,
        "maximum_safe_claim": claim_text if not missing else safe_claim,
        "stop_conditions": [stop],
        "evidence_boundary": evidence_boundary(
            inspected=["claim text", "declared evidence-class labels", "declared source locators"],
            not_inspected=["underlying data, methods, figures, or full source context"],
            cannot_conclude=["that declared evidence exists or satisfies the required class"],
            next_required=missing or ["inspect source-level evidence against pass criteria"],
        ),
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile a claim into a validation contract.")
    parser.add_argument("--claim", required=True)
    parser.add_argument("--claim-type", choices=sorted(RULES))
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--source-locator", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = compile_claim(args.claim, args.claim_type, args.evidence, args.source_locator)
    errors = validate_required_contract(
        payload,
        schema_path(__file__, "validation_card.schema.json"),
    )
    if errors:
        raise SystemExit("ValidationCard contract failed: " + "; ".join(errors))
    write_json(args.output, payload)
    print(
        json.dumps(
            {
                "claim_type": payload["claim_type"],
                "maximum_safe_claim": payload["maximum_safe_claim"],
                "missing_evidence": len(payload["missing_evidence"]),
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
