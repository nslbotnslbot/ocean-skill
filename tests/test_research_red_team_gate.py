#!/usr/bin/env python3
"""Regression tests for the conditional research-package red-team gate."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import read_json, run_cli, write_json


def qualified_payload(*, mode: str = "Audit", requested: bool = True) -> dict:
    return {
        "schema_version": "ocean-research-package-v1",
        "request_mode": mode,
        "red_team_requested": requested,
        "domain": "clinical_prediction",
        "components": {
            "study_framing": {"status": "inspected", "locators": ["plan:aim"]},
            "claims_or_study_plan": {"status": "inspected", "locators": ["plan:claims"]},
            "data_or_cohort": {"status": "inspected", "locators": ["methods:cohort"]},
            "validation_design": {"status": "inspected", "locators": ["methods:validation"]},
        },
        "source_packets": [
            {
                "packet_id": "PACKET-1",
                "evidence_state": "inspected",
                "locators": ["methods:1"],
            }
        ],
    }


def review_payload() -> dict:
    located = {
        "evidence_state": "located",
        "evidence": [{"packet_id": "PACKET-1", "locator": "methods:1"}],
        "next_required": [],
    }
    return {
        "schema_version": "ocean-research-red-team-review-v1",
        "package_gate_id": "red-team-gate-example",
        "package_gate_status": "ready_for_human_red_team",
        "source_packet_ids": ["PACKET-1"],
        "conclusions": [
            {"conclusion_id": "C1", "kind": "bottleneck", "statement": "External validation is not described.", **located},
            {"conclusion_id": "C2", "kind": "validity_verdict", "statement": "The declared package supports only the stated limited claim.", **located},
            {"conclusion_id": "C3", "kind": "minimum_validation", "statement": "Add an independent external validation plan.", **located},
            {"conclusion_id": "C4", "kind": "decision", "statement": "Rework until the validation boundary is addressed.", "decision": "Rework", **located},
            {"conclusion_id": "C5", "kind": "reviewer_risk", "statement": "Reviewers may question generalization.", **located},
            {"conclusion_id": "C6", "kind": "collaboration_boundary", "statement": "A domain reviewer must inspect the source material.", **located},
        ],
    }


class ResearchRedTeamGateTests(unittest.TestCase):
    def run_gate(self, payload: dict) -> dict:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "package.json"
            output_path = root / "gate.json"
            write_json(input_path, payload)
            run_cli("red-team-gate", "--input", input_path, "--output", output_path)
            return read_json(output_path)

    def test_ordinary_audit_does_not_trigger_red_team(self) -> None:
        result = self.run_gate(qualified_payload(requested=False))
        self.assertEqual(result["status"], "not_requested")
        self.assertNotIn("decision", result)

    def test_explore_revise_and_track_do_not_trigger_red_team(self) -> None:
        for mode in ("Explore", "Revise", "Track"):
            with self.subTest(mode=mode):
                result = self.run_gate(qualified_payload(mode=mode))
                self.assertEqual(result["status"], "not_applicable")
                self.assertNotIn("decision", result)

    def test_incomplete_package_returns_cannot_decide(self) -> None:
        payload = qualified_payload()
        payload["components"]["validation_design"] = {
            "status": "missing",
            "locators": [],
        }
        payload["source_packets"] = []
        result = self.run_gate(payload)
        self.assertEqual(result["status"], "cannot_decide")
        self.assertGreaterEqual(len(result["next_required"]), 2)
        self.assertIn(
            "Go, Rework, Stop",
            result["evidence_boundary"]["cannot_conclude"][1],
        )

    def test_qualified_package_needs_human_red_team_review(self) -> None:
        result = self.run_gate(qualified_payload())
        self.assertEqual(result["status"], "ready_for_human_red_team")
        self.assertEqual(result["source_packet_ids"], ["PACKET-1"])
        self.assertNotIn("decision", result)

    def test_review_check_accepts_located_conclusions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "review.json"
            output_path = root / "review-check.json"
            write_json(input_path, review_payload())
            run_cli("red-team-review-check", "--input", input_path, "--output", output_path)
            result = read_json(output_path)
        self.assertEqual(result["status"], "valid")
        self.assertEqual(result["traceable_conclusion_count"], 6)
        self.assertEqual(result["explicit_unknown_conclusion_count"], 0)

    def test_review_check_requires_explicit_unknown_or_valid_locator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "review.json"
            output_path = root / "review-check.json"
            payload = review_payload()
            payload["conclusions"][0]["evidence"] = [
                {"packet_id": "UNDECLARED", "locator": "methods:1"}
            ]
            write_json(input_path, payload)
            run_cli(
                "red-team-review-check",
                "--input",
                input_path,
                "--output",
                output_path,
                expect_success=False,
            )

    def test_review_check_allows_explicit_unknown_with_next_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "review.json"
            output_path = root / "review-check.json"
            payload = review_payload()
            payload["conclusions"][4].update(
                {
                    "evidence_state": "explicit_unknown",
                    "evidence": [],
                    "next_required": ["provide the reviewer-risk source material"],
                }
            )
            write_json(input_path, payload)
            run_cli("red-team-review-check", "--input", input_path, "--output", output_path)
            result = read_json(output_path)
        self.assertEqual(result["traceable_conclusion_count"], 5)
        self.assertEqual(result["explicit_unknown_conclusion_count"], 1)


if __name__ == "__main__":
    unittest.main()
