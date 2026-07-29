#!/usr/bin/env python3
"""Contract tests for external bridges and Harbor-to-Skill distillation."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import read_json, run_cli, write_json


class ControlPlaneBridgeTests(unittest.TestCase):
    def test_reader_bridge_emits_paper_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "reader.json"
            output = root / "paper-bundle.json"
            write_json(
                input_path,
                {
                    "paper_id": "FORMAL-PAPER",
                    "source": {
                        "title": "Formal reader artifact",
                        "media_type": "application/json",
                        "checksum": "formal-checksum",
                    },
                    "locator_mode": "structure-grounded",
                    "locators": [
                        {
                            "block_id": "block-00001",
                            "text": "Formal text, not scientific evidence.",
                            "locators": ["section:formal"],
                        }
                    ],
                },
            )
            run_cli(
                "bridge",
                "grounded-reader",
                "--input",
                input_path,
                "--output",
                output,
            )
            bundle = read_json(output)
            self.assertEqual(bundle["schema_version"], "ocean-paper-bundle-v1")
            self.assertEqual(bundle["blocks"][0]["locators"], ["section:formal"])

    def test_science_bridge_preserves_source_and_run_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "tool-result.json"
            packet_output = root / "packet.json"
            manifest_output = root / "manifest.json"
            write_json(
                input_path,
                {
                    "source": {
                        "source_type": "formal_database",
                        "source_id": "FORMAL-RECORD",
                        "title": "Formal record",
                        "access_mode": "public",
                    },
                    "result": {"status": "no_hit"},
                    "locators": [
                        {
                            "locator_id": "record-1",
                            "locator_type": "record",
                            "value": "FORMAL-RECORD",
                        }
                    ],
                    "provenance": {
                        "task_intent": "formal bridge test",
                        "software": "formal-client",
                        "software_version": "0",
                        "command": ["formal-client", "query"],
                        "status": "executed",
                    },
                },
            )
            run_cli(
                "bridge",
                "scientific-tool",
                "--input",
                input_path,
                "--packet-output",
                packet_output,
                "--manifest-output",
                manifest_output,
            )
            packet = read_json(packet_output)
            manifest = read_json(manifest_output)
            self.assertEqual(packet["evidence_state"], "queried_evidence")
            self.assertEqual(packet["result_summary"]["status"], "no_hit")
            self.assertEqual(manifest["status"], "executed")
            self.assertEqual(manifest["software"]["name"], "formal-client")

    def test_science_bridge_does_not_claim_unlocated_result_was_queried(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "tool-result.json"
            packet_output = root / "packet.json"
            manifest_output = root / "manifest.json"
            write_json(
                input_path,
                {
                    "source": {
                        "source_type": "formal_database",
                        "source_id": "FORMAL-UNLOCATED",
                    },
                    "result": {"value": "unlocated"},
                    "provenance": {"status": "partial"},
                },
            )
            run_cli(
                "bridge",
                "scientific-tool",
                "--input",
                input_path,
                "--packet-output",
                packet_output,
                "--manifest-output",
                manifest_output,
            )
            packet = read_json(packet_output)
            self.assertEqual(packet["evidence_state"], "candidate")
            self.assertFalse(packet["locators"])

    def test_distiller_requires_actual_contracts_and_all_gates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "distill.json"
            output = root / "gate.json"
            skeleton_root = root / "skills"
            incomplete = {
                "workflow_name": "formal_workflow",
                "complete_execution_record": True,
                "stable_input_contract": True,
                "stable_output_contract": True,
            }
            write_json(input_path, incomplete)
            completed = run_cli(
                "bridge",
                "distill",
                "--input",
                input_path,
                "--output",
                output,
                "--skeleton-root",
                skeleton_root,
                expect_success=False,
            )
            self.assertIn("Distillation blocked", completed.stderr)
            report = read_json(output)
            self.assertIn("input_contract", report["missing_requirements"])
            self.assertFalse(skeleton_root.exists())

            complete = {
                "workflow_name": "formal_workflow",
                "description": "Formal reusable workflow skeleton.",
                "complete_execution_record": True,
                "stable_input_contract": True,
                "stable_output_contract": True,
                "input_contract": {"source": "path"},
                "output_contract": {"report": "path"},
                "provenance_complete": True,
                "positive_case": "formal positive fixture",
                "negative_case": "formal negative fixture",
                "failure_case": "formal failure fixture",
                "stop_conditions": ["stop when source provenance is missing"],
                "eval_case": "formal executable fixture",
                "privacy_check": True,
                "license_check": True,
                "user_approval": True,
            }
            write_json(input_path, complete)
            run_cli(
                "bridge",
                "distill",
                "--input",
                input_path,
                "--output",
                output,
                "--skeleton-root",
                skeleton_root,
            )
            report = read_json(output)
            self.assertTrue(report["eligible"])
            skill = skeleton_root / "formal-workflow/SKILL.md"
            self.assertTrue(skill.is_file())
            self.assertIn("Input Contract", skill.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
