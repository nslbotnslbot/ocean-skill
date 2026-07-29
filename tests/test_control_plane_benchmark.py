#!/usr/bin/env python3
"""Tests for the formal-only OCEAN-Bench contract suite."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import EVALS, read_json, run_cli


CASES = EVALS / "cases/golden_contract_cases.json"


class ControlPlaneBenchmarkTests(unittest.TestCase):
    def test_golden_suite_is_balanced_and_explicitly_formal(self) -> None:
        payload = read_json(CASES)
        cases = payload["cases"]
        self.assertEqual(len(cases), 30)
        self.assertFalse(payload["scientific_evidence"])
        counts = Counter(case["category"] for case in cases)
        self.assertEqual(len(counts), 10)
        self.assertTrue(all(count == 3 for count in counts.values()))
        self.assertTrue(all(not case["scientific_evidence"] for case in cases))

    def test_contract_runner_and_permissive_control_are_distinguishable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            candidate = root / "candidate.json"
            predictions = root / "baseline-predictions.json"
            baseline = root / "baseline.json"
            comparison = root / "comparison.json"
            run_cli(
                "benchmark",
                "run",
                "--cases",
                CASES,
                "--output",
                candidate,
            )
            run_cli(
                "benchmark",
                "baseline",
                "--cases",
                CASES,
                "--output",
                predictions,
            )
            run_cli(
                "benchmark",
                "run",
                "--cases",
                CASES,
                "--predictions",
                predictions,
                "--condition",
                "optimistic-control",
                "--output",
                baseline,
            )
            run_cli(
                "benchmark",
                "compare",
                "--baseline",
                baseline,
                "--candidate",
                candidate,
                "--output",
                comparison,
            )
            candidate_report = read_json(candidate)
            baseline_report = read_json(baseline)
            delta = read_json(comparison)
            self.assertEqual(candidate_report["cases"], 30)
            self.assertEqual(candidate_report["accuracy"], 1.0)
            self.assertIn("not a scientific-performance benchmark", candidate_report["interpretation_boundary"])
            self.assertGreater(
                baseline_report["unsupported_strong_claim_errors"],
                0,
            )
            self.assertGreater(delta["accuracy_delta"], 0)
            self.assertLess(
                delta["unsupported_strong_claim_error_delta"],
                0,
            )


if __name__ == "__main__":
    unittest.main()
