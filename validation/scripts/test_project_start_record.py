#!/usr/bin/env python3
"""Regression tests for the Harbor project-record generator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/ocean/scripts/create_project_start_record.py"


class ProjectStartRecordTests(unittest.TestCase):
    def test_generator_emits_canonical_public_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "projects"
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--title",
                    "Example Clinical Project",
                    "--project-id",
                    "OCEAN-PROJ-999",
                    "--domain",
                    "medical-ai",
                    "--ocean-phase",
                    "evidence-audit",
                    "--project-stage",
                    "analysis",
                    "--public-status",
                    "active",
                    "--public-safe",
                    "yes",
                    "--inspected",
                    "public protocol",
                    "--not-inspected",
                    "patient-level data",
                    "--next-evidence-needed",
                    "owner-approved milestone",
                    "--excluded-material",
                    "patient-level data,credentials",
                    "--outdir",
                    str(outdir),
                    "--no-index",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            record = outdir / "example-clinical-project" / "README.md"
            self.assertTrue(record.exists())
            text = record.read_text(encoding="utf-8")
            metadata = text.split("<!-- ocean-project\n", 1)[1].split("\n-->", 1)[0]
            data = yaml.safe_load(metadata)
            self.assertEqual(data["project_id"], "OCEAN-PROJ-999")
            self.assertEqual(data["ocean_phase"], "evidence-audit")
            self.assertEqual(data["project_stage"], "analysis")
            self.assertIn("## Progress", text)
            self.assertIn("## Public Boundary", text)
            self.assertLessEqual(len(text.splitlines()), 60)
            self.assertNotIn("/Users/", text)

    def test_unconfirmed_record_cannot_target_public_projects(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--title",
                "Unconfirmed Project",
                "--public-safe",
                "unclear",
                "--outdir",
                str(ROOT / "projects"),
            ],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing to write an unconfirmed record", result.stderr)

    def test_generator_creates_index_and_allocates_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "records"
            for title in ("First Public Project", "Second Public Project"):
                subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "--title",
                        title,
                        "--public-safe",
                        "yes",
                        "--outdir",
                        str(outdir),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            index = (outdir / "README.md").read_text(encoding="utf-8")
            self.assertIn("first-public-project/README.md", index)
            self.assertIn("second-public-project/README.md", index)
            first = (outdir / "first-public-project" / "README.md").read_text(encoding="utf-8")
            second = (outdir / "second-public-project" / "README.md").read_text(encoding="utf-8")
            self.assertIn("project_id: OCEAN-PROJ-001", first)
            self.assertIn("project_id: OCEAN-PROJ-002", second)


if __name__ == "__main__":
    unittest.main()
