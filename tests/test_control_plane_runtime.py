#!/usr/bin/env python3
"""Regression tests for SourcePacket, RunManifest, and safe doctor behavior."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import ROOT, read_json, run_cli


class ControlPlaneRuntimeTests(unittest.TestCase):
    def test_source_packet_records_checksum_and_validates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "packet.json"
            locators = json.dumps(
                [
                    {
                        "locator_id": "readme-title",
                        "locator_type": "line",
                        "value": "README.md:1",
                    }
                ]
            )
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
                "--locator-mode",
                "structure-grounded",
                "--locators-json",
                locators,
                "--output",
                output,
            )
            packet = read_json(output)
            self.assertEqual(packet["schema_version"], "ocean-source-packet-v2")
            self.assertEqual(len(packet["source"]["checksum"]), 64)
            self.assertFalse(packet["source"]["checksum"].startswith("unverified:"))
            run_cli("source-packet", "validate", "--input", output)

    def test_queried_evidence_without_locator_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "invalid-packet.json"
            completed = run_cli(
                "source-packet",
                "create",
                "--source-type",
                "database",
                "--source-id",
                "FORMAL-QUERY",
                "--source-file",
                ROOT / "README.md",
                "--evidence-state",
                "queried_evidence",
                "--output",
                output,
                expect_success=False,
            )
            self.assertIn("queried evidence requires", completed.stderr)
            self.assertFalse(output.exists())

    def test_doctor_reports_presence_without_exposing_secret(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "doctor.json"
            sentinel = "OCEAN_TEST_SECRET_MUST_NOT_APPEAR"
            env = os.environ.copy()
            env["OPENAI_API_KEY"] = sentinel
            completed = run_cli("doctor", "--output", output, env=env)
            report = read_json(output)
            credential = next(
                item
                for item in report["credentials"]
                if item["name"] == "OPENAI_API_KEY"
            )
            self.assertTrue(credential["present"])
            self.assertNotIn(sentinel, completed.stdout)
            self.assertNotIn(sentinel, output.read_text(encoding="utf-8"))

    def test_run_manifest_preserves_input_checksum(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "manifest.json"
            run_cli(
                "manifest",
                "create",
                "--task",
                "formal manifest contract test",
                "--command-json",
                '["python", "formal.py"]',
                "--input",
                ROOT / "README.md",
                "--status",
                "planned",
                "--output",
                output,
            )
            manifest = read_json(output)
            self.assertEqual(manifest["schema_version"], "ocean-run-manifest-v1")
            self.assertEqual(len(manifest["inputs"][0]["sha256"]), 64)
            self.assertFalse(manifest["outputs"])
            run_cli("manifest", "validate", "--input", output)


if __name__ == "__main__":
    unittest.main()
