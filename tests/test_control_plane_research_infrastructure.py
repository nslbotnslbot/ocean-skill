#!/usr/bin/env python3
"""Tests for long-horizon, multi-run, and publication-gate infrastructure."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import EVALS, ROOT, read_json, run_cli, write_json


class ControlPlaneResearchInfrastructureTests(unittest.TestCase):
    def test_domain_lens_routes_materials_without_claiming_validity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "domain.json"
            output = root / "lens.json"
            write_json(
                input_path,
                {
                    "task_id": "FORMAL-MATERIALS-ROUTE",
                    "domain": "materials",
                    "research_object": "unspecified material",
                    "claim_type": "property",
                    "available_evidence": ["composition and material identity"],
                },
            )
            run_cli(
                "domain-lens",
                "--input",
                input_path,
                "--output",
                output,
            )
            result = read_json(output)
            self.assertTrue(result["recognized"])
            self.assertIn(
                "processing history and batch identity",
                result["missing_evidence"],
            )
            self.assertIn(
                "under the supplied preparation and test conditions",
                result["maximum_safe_claim"],
            )
            self.assertIn(
                "scientific validity from routing alone",
                result["evidence_boundary"]["cannot_conclude"],
            )

    def test_harbor_ledger_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            ledger = Path(temporary) / "ledger.json"
            run_cli(
                "ledger",
                "init",
                "--project-id",
                "FORMAL-PROJECT",
                "--title",
                "Formal long-horizon contract test",
                "--output",
                ledger,
            )
            boundary = json.dumps(
                {
                    "inspected": ["formal event declaration"],
                    "not_inspected": ["scientific source content"],
                    "cannot_conclude": ["that the declared event occurred"],
                    "next_required": ["attach source and run records"],
                }
            )
            run_cli(
                "ledger",
                "append",
                "--ledger",
                ledger,
                "--event-type",
                "project_started",
                "--summary",
                "Formal event, not scientific evidence.",
                "--evidence-boundary-json",
                boundary,
            )
            run_cli("ledger", "validate", "--ledger", ledger)
            payload = read_json(ledger)
            payload["entries"][0]["summary"] = "tampered"
            write_json(ledger, payload)
            completed = run_cli(
                "ledger",
                "validate",
                "--ledger",
                ledger,
                expect_success=False,
            )
            self.assertIn("entry checksum mismatch", completed.stdout)

    def test_artifact_envelope_preserves_embedded_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packet = root / "packet.json"
            envelope = root / "envelope.json"
            run_cli(
                "source-packet",
                "create",
                "--source-type",
                "repository_document",
                "--source-id",
                "README",
                "--source-file",
                ROOT / "README.md",
                "--evidence-state",
                "inspected",
                "--locators-json",
                '[{"locator_id":"line-1","locator_type":"line","value":"README.md:1"}]',
                "--output",
                packet,
            )
            run_cli(
                "bridge",
                "envelope",
                "--input",
                packet,
                "--producer",
                "OCEAN formal test",
                "--producer-version",
                "r1",
                "--access",
                "public",
                "--license",
                "MIT",
                "--output",
                envelope,
            )
            result = read_json(envelope)
            self.assertEqual(result["artifact_type"], "source_packet")
            self.assertEqual(
                result["artifact_id"],
                read_json(packet)["packet_id"],
            )
            self.assertEqual(len(result["content_checksum"]), 64)

    def test_repeated_run_aggregation_does_not_invent_missing_cost(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "runs.json"
            output = root / "summary.json"
            write_json(
                input_path,
                {
                    "benchmark_id": "FORMAL-REPEATED-RUNS",
                    "runs": [
                        {
                            "run_id": "run-1",
                            "condition": "ocean",
                            "model": "formal-model",
                            "model_version": "0",
                            "prompt_checksum": "formal-prompt-checksum",
                            "repetition": 1,
                            "case_ids": ["FORMAL-CASE"],
                            "status": "executed",
                            "failures": [],
                            "accuracy": 0.8,
                            "tokens": 100,
                            "elapsed_seconds": 2.0,
                            "cost_usd": 0.01,
                        },
                        {
                            "run_id": "run-2",
                            "condition": "ocean",
                            "model": "formal-model",
                            "model_version": "0",
                            "prompt_checksum": "formal-prompt-checksum",
                            "repetition": 2,
                            "case_ids": ["FORMAL-CASE"],
                            "status": "timeout",
                            "failures": ["timeout"],
                            "accuracy": 0.6,
                            "tokens": 120,
                            "elapsed_seconds": 4.0,
                        },
                    ],
                },
            )
            run_cli(
                "benchmark",
                "aggregate",
                "--input",
                input_path,
                "--output",
                output,
            )
            result = read_json(output)
            condition = result["conditions"]["ocean"]
            self.assertEqual(condition["runs"], 2)
            self.assertEqual(condition["metrics"]["accuracy"]["mean"], 0.7)
            self.assertEqual(condition["metrics"]["cost_usd"]["reported_runs"], 1)
            self.assertEqual(condition["metrics"]["cost_usd"]["unreported_runs"], 1)

    def test_case_intake_keeps_formal_suite_below_research_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "intake.json"
            run_cli(
                "benchmark",
                "case-intake",
                "--input",
                EVALS / "cases/golden_contract_cases.json",
                "--required-count",
                "100",
                "--output",
                output,
            )
            result = read_json(output)
            self.assertFalse(result["research_ready"])
            self.assertFalse(result["gates"]["minimum_case_count"])
            self.assertEqual(result["scientific_evidence_cases"], 0)

    def test_leaderboard_rejects_unadjudicated_internal_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            report = root / "report.json"
            submission = root / "submission.json"
            output = root / "leaderboard.json"
            run_cli(
                "benchmark",
                "run",
                "--cases",
                EVALS / "cases/golden_contract_cases.json",
                "--output",
                report,
            )
            write_json(
                submission,
                {
                    "benchmark_version": "formal-r1",
                    "submissions": [
                        {
                            "submission_id": "FORMAL-INTERNAL",
                            "system_name": "Formal internal runner",
                            "report_path": str(report),
                            "report_checksum": "",
                            "adjudication_records": [],
                            "external_origin": False,
                            "permission_to_publish": False,
                        }
                    ],
                },
            )
            run_cli(
                "benchmark",
                "leaderboard",
                "--input",
                submission,
                "--minimum-cases",
                "100",
                "--output",
                output,
            )
            result = read_json(output)
            self.assertFalse(result["entries"])
            self.assertEqual(len(result["rejected_submissions"]), 1)
            reasons = result["rejected_submissions"][0]["reasons"]
            self.assertTrue(any("fewer than 100 cases" in item for item in reasons))
            self.assertTrue(any("not declared external" in item for item in reasons))

    def test_ablation_report_is_descriptive_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "ablation.json"
            output = root / "ablation-summary.json"
            write_json(
                input_path,
                {
                    "reference_condition": "base",
                    "reports": [
                        {
                            "condition": "base",
                            "cases": 30,
                            "case_ids_checksum": "formal-case-set",
                            "accuracy": 0.4,
                            "macro_f1": 0.2,
                            "unsupported_strong_claim_errors": 16,
                        },
                        {
                            "condition": "ocean",
                            "cases": 30,
                            "case_ids_checksum": "formal-case-set",
                            "accuracy": 1.0,
                            "macro_f1": 1.0,
                            "unsupported_strong_claim_errors": 0,
                        },
                    ],
                },
            )
            run_cli(
                "benchmark",
                "ablation",
                "--input",
                input_path,
                "--output",
                output,
            )
            result = read_json(output)
            self.assertEqual(
                result["comparisons"][0]["deltas"]["accuracy"],
                0.6,
            )
            self.assertIn(
                "statistical significance or generalization",
                result["evidence_boundary"]["cannot_conclude"],
            )

    def test_long_horizon_runner_detects_silent_boundary_loss(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "traces.json"
            output = root / "trace-report.json"
            write_json(
                input_path,
                {
                    "traces": [
                        {
                            "trace_id": "FORMAL-TRACE",
                            "sessions": [
                                {
                                    "session_id": "session-1",
                                    "ledger_head_checksum": "head-1",
                                    "cannot_conclude": [
                                        "clinical utility is not established"
                                    ],
                                    "open_risks": ["external validation missing"],
                                    "resolved_items": [],
                                },
                                {
                                    "session_id": "session-2",
                                    "ledger_head_checksum": "head-2",
                                    "cannot_conclude": [],
                                    "open_risks": [],
                                    "resolved_items": [],
                                },
                            ],
                        }
                    ]
                },
            )
            run_cli(
                "benchmark",
                "long-horizon",
                "--input",
                input_path,
                "--output",
                output,
            )
            result = read_json(output)
            self.assertEqual(result["summary"]["boundary_lost"], 1)
            self.assertTrue(
                any(
                    "dropped without resolution evidence" in issue
                    for issue in result["traces"][0]["issues"]
                )
            )


if __name__ == "__main__":
    unittest.main()
