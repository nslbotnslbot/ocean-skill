#!/usr/bin/env python3
"""Integrity tests for OCEAN routing, ledgers, and artifact envelopes."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import ROOT, read_json, run_cli, write_json


class ControlPlaneIntegrityTests(unittest.TestCase):
    def test_domain_lens_routes_materials_without_claiming_validity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "domain.json"
            output = root / "lens.json"
            write_json(
                input_path,
                {
                    "task_id": "TEST-MATERIALS-ROUTE",
                    "domain": "materials",
                    "research_object": "unspecified material",
                    "claim_type": "property",
                    "available_evidence": ["composition and material identity"],
                },
            )
            run_cli("domain-lens", "--input", input_path, "--output", output)
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
                "TEST-PROJECT",
                "--title",
                "Ledger integrity test",
                "--output",
                ledger,
            )
            boundary = json.dumps(
                {
                    "inspected": ["test event declaration"],
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
                "Test event, not scientific evidence.",
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
                "OCEAN test",
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


if __name__ == "__main__":
    unittest.main()
