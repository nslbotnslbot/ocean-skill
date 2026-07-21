#!/usr/bin/env python3
"""Regression tests for OCEAN software evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
COMMON = REPO_ROOT / "skills" / "ocean" / "scripts" / "tools" / "common"


class SoftwareBoundaryTests(unittest.TestCase):
    def test_nonzero_probe_is_not_execution_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "probe.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(COMMON / "cli_subprocess_wrapper.py"),
                    "probe",
                    "--tool-name",
                    "Python diagnostic",
                    "--tool-slug",
                    "python-diagnostic",
                    "--command",
                    sys.executable,
                    "--probe-args=--definitely-invalid-ocean-probe",
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(payload["execution_status"], "found_but_probe_nonzero")
            self.assertEqual(payload["software_record"]["boundary_status"], "candidate_route")
            self.assertEqual(payload["software_record"]["supports_claims"], [])

    def test_incomplete_record_cannot_be_queried_evidence(self) -> None:
        record = {
            "tool_name": "BLAST",
            "tool_version": "",
            "task_intent": "",
            "command_line": "",
            "parameters": {},
            "reference_or_index": "",
            "input_files": [],
            "output_files": [],
            "logs_or_qc": [],
            "environment": "",
            "date": "",
            "supports_claims": [],
            "boundary_status": "queried_evidence",
        }
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "record.json"
            output = Path(tmp) / "packet.json"
            source.write_text(json.dumps(record), encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(COMMON / "software_source_packet.py"),
                    "packet",
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            packet = json.loads(output.read_text(encoding="utf-8"))
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(packet["boundary_status"], "candidate_route")
            self.assertEqual(packet["supports_claims"], [])
            self.assertEqual(packet["provenance_audit"]["verdict"], "needs_review")
            self.assertEqual(packet["inspected_content"], ["tool identity"])

    def test_complete_record_preserves_packet_evidence(self) -> None:
        record = {
            "tool_name": "Example tool",
            "tool_version": "1.0",
            "task_intent": "bounded fixture validation",
            "command_line": "example-tool --version",
            "parameters": {"mode": "fixture"},
            "reference_or_index": "fixture-index-v1",
            "input_files": ["input.fixture"],
            "output_files": ["output.fixture"],
            "logs_or_qc": ["run.log"],
            "environment": "test environment",
            "date": "2026-07-21",
            "supports_claims": ["recorded software provenance"],
            "boundary_status": "packet_evidence",
        }
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "record.json"
            output = Path(tmp) / "packet.json"
            source.write_text(json.dumps(record), encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(COMMON / "software_source_packet.py"),
                    "packet",
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            packet = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(packet["boundary_status"], "packet_evidence")
            self.assertEqual(packet["supports_claims"], ["recorded software provenance"])
            self.assertEqual(packet["provenance_audit"]["verdict"], "pass")


if __name__ == "__main__":
    unittest.main()
