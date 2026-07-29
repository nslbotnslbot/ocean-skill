#!/usr/bin/env python3
"""Run deterministic OCEAN-Bench contract cases or score external predictions."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
SCRIPT_ROOT = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))
sys.path.insert(0, str(SCRIPT_ROOT / "detectors"))
sys.path.insert(0, str(SCRIPT_ROOT / "audit" / "references"))

from ocean_core import now_utc, read_json, sha256_json, write_json
from claim_to_validation import compile_claim
from citation_scope_checker import check_pair
from entailment_auditor import audit_pair
from evidence_diff import compare as evidence_diff
from evidence_independence import classify_graph
from leakage import audit_leakage


SAFE_LABELS = {
    "supported",
    "unchanged",
    "supported_candidate",
    "independent",
    "not_detected_in_declared_identifiers",
    "complete",
    "preserved",
    "consistent",
    "unchanged_snapshot",
}


def run_ocean_case(case: dict) -> str:
    category = case["category"]
    payload = case["input"]
    if category == "claim_support":
        card = compile_claim(
            payload["claim_text"],
            payload.get("claim_type"),
            payload.get("evidence_classes", []),
            payload.get("source_locators", []),
        )
        return "supported" if not card["missing_evidence"] else "unsupported"
    if category == "claim_downgrade":
        card = compile_claim(
            payload["claim_text"],
            payload.get("claim_type"),
            payload.get("evidence_classes", []),
            payload.get("source_locators", []),
        )
        return "unchanged" if card["maximum_safe_claim"] == payload["claim_text"] else "downgraded"
    if category == "citation_entailment":
        return audit_pair(payload)["verdict"]
    if category == "evidence_independence":
        return classify_graph(payload)["classification"]
    if category == "leakage_detection":
        return audit_leakage(payload)["classification"]
    if category == "validation_planning":
        card = compile_claim(
            payload["claim_text"],
            payload.get("claim_type"),
            payload.get("evidence_classes", []),
            payload.get("source_locators", []),
        )
        if card["claim_type"] == "unknown":
            return "needs_claim_type"
        return (
            "complete"
            if card["required_evidence_classes"]
            and card["decisive_controls"]
            and card["pass_criteria"]
            and card["stop_conditions"]
            else "incomplete"
        )
    if category == "reproducibility":
        required = [
            "command",
            "software",
            "parameters",
            "inputs",
            "outputs",
            "environment",
            "evidence_boundary",
        ]
        if payload.get("status") == "failed":
            return "failed"
        return "complete" if all(payload.get(field) not in (None, "", []) for field in required) else "incomplete"
    if category == "negative_evidence":
        state = payload.get("result_state")
        preserved = payload.get("recorded_state") == state
        return "preserved" if preserved and state in {"no_hit", "failed", "conflicting"} else "lost"
    if category == "long_horizon_consistency":
        prior = set(payload.get("prior_cannot_conclude", []))
        current = set(payload.get("current_cannot_conclude", []))
        return "consistent" if prior <= current else "boundary_lost"
    if category == "evidence_diff":
        result = evidence_diff(payload["old"], payload["new"])
        if result["new_evidence"] or result["removed_evidence"] or result["changed_packets"]:
            return "changed_snapshot"
        return "unchanged_snapshot"
    raise ValueError(f"Unknown benchmark category: {category}")


def macro_f1(rows: list[dict]) -> float:
    labels = sorted({row["expected"] for row in rows} | {row["predicted"] for row in rows})
    scores = []
    for label in labels:
        tp = sum(row["expected"] == label and row["predicted"] == label for row in rows)
        fp = sum(row["expected"] != label and row["predicted"] == label for row in rows)
        fn = sum(row["expected"] == label and row["predicted"] != label for row in rows)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return sum(scores) / len(scores) if scores else 0.0


def score(cases: list[dict], predictions: dict[str, str], condition: str) -> dict:
    rows = []
    by_category: dict[str, list[bool]] = defaultdict(list)
    for case in cases:
        expected = case["expected"]["label"]
        predicted = predictions.get(case["case_id"], "missing_prediction")
        correct = predicted == expected
        rows.append(
            {
                "case_id": case["case_id"],
                "category": case["category"],
                "expected": expected,
                "predicted": predicted,
                "correct": correct,
            }
        )
        by_category[case["category"]].append(correct)
    strong_claim_errors = sum(
        row["predicted"] in SAFE_LABELS
        and row["expected"] not in SAFE_LABELS
        for row in rows
    )
    return {
        "schema_version": "ocean-benchmark-report-v1",
        "condition": condition,
        "created_at": now_utc(),
        "cases": len(rows),
        "case_ids_checksum": sha256_json(
            sorted(row["case_id"] for row in rows)
        ),
        "correct": sum(row["correct"] for row in rows),
        "accuracy": round(sum(row["correct"] for row in rows) / len(rows), 6) if rows else 0.0,
        "macro_f1": round(macro_f1(rows), 6),
        "unsupported_strong_claim_errors": strong_claim_errors,
        "by_category": {
            category: {
                "cases": len(values),
                "accuracy": round(sum(values) / len(values), 6),
            }
            for category, values in sorted(by_category.items())
        },
        "rows": rows,
        "interpretation_boundary": (
            "Included formal cases test deterministic contract behavior. They are not a "
            "scientific-performance benchmark, model leaderboard, or substitute for blinded expert cases."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run or score OCEAN-Bench cases.")
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--predictions", type=Path)
    parser.add_argument("--condition", default="ocean-deterministic-contracts")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    cases_payload = read_json(args.cases)
    cases = cases_payload.get("cases", [])
    if args.predictions:
        prediction_payload = read_json(args.predictions)
        predictions = prediction_payload.get("predictions", {})
    else:
        predictions = {case["case_id"]: run_ocean_case(case) for case in cases}
    report = score(cases, predictions, args.condition)
    write_json(args.output, report)
    print(
        json.dumps(
            {
                "condition": report["condition"],
                "cases": report["cases"],
                "accuracy": report["accuracy"],
                "macro_f1": report["macro_f1"],
                "unsupported_strong_claim_errors": report["unsupported_strong_claim_errors"],
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
