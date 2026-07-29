#!/usr/bin/env python3
"""Aggregate repeated benchmark runs without inventing missing cost data."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import statistics
import sys

SKILL_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from ocean_core import evidence_boundary, read_json, write_json


NUMERIC_METRICS = (
    "accuracy",
    "macro_f1",
    "unsupported_strong_claim_errors",
    "tokens",
    "elapsed_seconds",
    "cost_usd",
)
REQUIRED_FIELDS = (
    "run_id",
    "condition",
    "model",
    "model_version",
    "prompt_checksum",
    "repetition",
    "case_ids",
    "status",
    "failures",
)
RUN_STATUSES = {"executed", "partial", "failed", "timeout", "rate_limited"}


def summarize(values: list[float]) -> dict:
    return {
        "reported_runs": len(values),
        "mean": round(statistics.fmean(values), 6),
        "minimum": round(min(values), 6),
        "maximum": round(max(values), 6),
        "sample_standard_deviation": (
            round(statistics.stdev(values), 6) if len(values) > 1 else None
        ),
    }


def aggregate(payload: dict) -> dict:
    runs = payload.get("runs", [])
    for index, run in enumerate(runs, start=1):
        missing = [
            field
            for field in REQUIRED_FIELDS
            if field not in run or run[field] in (None, "")
        ]
        if missing:
            raise SystemExit(
                f"Run {index} is missing required fields: {', '.join(missing)}"
            )
        if run["status"] not in RUN_STATUSES:
            raise SystemExit(
                f"Run {run['run_id']} has unsupported status: {run['status']}"
            )
        if not isinstance(run["repetition"], int) or run["repetition"] < 1:
            raise SystemExit(
                f"Run {run['run_id']} requires a positive integer repetition"
            )
        if not isinstance(run["case_ids"], list) or not run["case_ids"]:
            raise SystemExit(f"Run {run['run_id']} requires non-empty case_ids")
        if not isinstance(run["failures"], list):
            raise SystemExit(f"Run {run['run_id']} failures must be an array")
    identifiers = [run.get("run_id") for run in runs]
    if any(not item for item in identifiers):
        raise SystemExit("Every run requires run_id")
    if len(set(identifiers)) != len(identifiers):
        raise SystemExit("run_id values must be unique")
    grouped: dict[str, list[dict]] = defaultdict(list)
    for run in runs:
        condition = str(run.get("condition", "")).strip()
        if not condition:
            raise SystemExit(f"Run {run['run_id']} is missing condition")
        grouped[condition].append(run)
    conditions = {}
    for condition, condition_runs in sorted(grouped.items()):
        metrics = {}
        for metric in NUMERIC_METRICS:
            values = [
                float(run[metric])
                for run in condition_runs
                if isinstance(run.get(metric), (int, float))
                and not isinstance(run.get(metric), bool)
            ]
            metrics[metric] = (
                {
                    **summarize(values),
                    "unreported_runs": len(condition_runs) - len(values),
                }
                if values
                else {
                    "reported_runs": 0,
                    "unreported_runs": len(condition_runs),
                    "status": "not_reported",
                }
            )
        conditions[condition] = {
            "runs": len(condition_runs),
            "models": sorted(
                {
                    f"{run['model']}@{run['model_version']}"
                    for run in condition_runs
                }
            ),
            "prompt_checksums": sorted(
                {str(run["prompt_checksum"]) for run in condition_runs}
            ),
            "case_sets": sorted(
                {
                    "|".join(sorted(str(case_id) for case_id in run["case_ids"]))
                    for run in condition_runs
                }
            ),
            "declared_failures": sum(
                len(run["failures"]) for run in condition_runs
            ),
            "statuses": {
                status: sum(run.get("status", "unknown") == status for run in condition_runs)
                for status in sorted(
                    {str(run.get("status", "unknown")) for run in condition_runs}
                )
            },
            "metrics": metrics,
        }
    return {
        "schema_version": "ocean-repeated-run-summary-v1",
        "benchmark_id": payload.get("benchmark_id", ""),
        "runs": len(runs),
        "conditions": conditions,
        "evidence_boundary": evidence_boundary(
            inspected=["declared run metrics and completion status"],
            not_inspected=[
                "provider billing records",
                "model outputs",
                "case-level human adjudication",
            ],
            cannot_conclude=[
                "statistical significance, model superiority, or scientific reliability from descriptive aggregates alone"
            ],
            next_required=[
                "report confidence intervals and blinded human adjudication before performance claims"
            ],
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aggregate repeated OCEAN benchmark runs.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    result = aggregate(read_json(args.input))
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "runs": result["runs"],
                "conditions": len(result["conditions"]),
                "output": str(args.output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
