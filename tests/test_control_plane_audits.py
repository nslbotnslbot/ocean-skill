#!/usr/bin/env python3
"""Boundary tests for statistics, availability, and citation audits."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import read_json, run_cli, write_json


class ControlPlaneAuditTests(unittest.TestCase):
    def test_unit_checker_flags_unmodeled_nested_observations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "design.json"
            output = root / "unit-audit.json"
            write_json(
                input_path,
                {
                    "analysis_id": "FORMAL-UNIT-AUDIT",
                    "experimental_unit": "patient",
                    "observation_unit": "cell",
                    "replication_hierarchy": {
                        "technical_replicates": 3,
                        "biological_replicates": 0,
                    },
                    "model_or_test": "ordinary least squares",
                },
            )
            run_cli(
                "audit",
                "statistics-unit",
                "--input",
                input_path,
                "--output",
                output,
            )
            result = read_json(output)
            self.assertEqual(result["status"], "needs_review")
            self.assertTrue(
                any("clustering or nesting" in issue for issue in result["issues"])
            )
            self.assertTrue(
                any("technical replicates" in issue for issue in result["issues"])
            )

    def test_data_availability_never_fills_placeholder_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "availability.json"
            output = root / "availability-audit.json"
            write_json(
                input_path,
                {
                    "assets": [
                        {
                            "asset_id": "DATA-1",
                            "asset_type": "data",
                            "access": "public",
                            "license": "TBD",
                            "repository": "TBD",
                            "identifier": "ACCESSION_HERE",
                        }
                    ]
                },
            )
            run_cli(
                "audit",
                "data-availability",
                "--input",
                input_path,
                "--output",
                output,
            )
            result = read_json(output)
            self.assertTrue(result["issues"])
            self.assertTrue(
                result["draft_statement"].startswith("AUTHOR_INPUT_NEEDED")
            )
            self.assertIn(
                "Do not insert repository identifiers",
                result["draft_statement"],
            )

    def test_citation_scope_and_entailment_preserve_uncertainty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_path = root / "citations.json"
            scope_output = root / "scope.json"
            entailment_output = root / "entailment.json"
            write_json(
                input_path,
                {
                    "pairs": [
                        {
                            "claim": {
                                "claim_id": "FORMAL-CLAIM",
                                "claim_type": "mechanism",
                                "species": "human",
                                "tissue": "liver",
                            },
                            "citation": {
                                "citation_id": "FORMAL-CITATION",
                                "species": "mouse",
                                "evidence_level": "abstract",
                                "reviewed_support": "supports",
                                "source_locator": "",
                            },
                        }
                    ]
                },
            )
            run_cli(
                "audit",
                "citation-scope",
                "--input",
                input_path,
                "--output",
                scope_output,
            )
            run_cli(
                "audit",
                "citation-entailment",
                "--input",
                input_path,
                "--output",
                entailment_output,
            )
            scope = read_json(scope_output)
            entailment = read_json(entailment_output)
            self.assertEqual(scope["pairs"][0]["status"], "scope_mismatch")
            self.assertEqual(
                entailment["pairs"][0]["verdict"],
                "partially_supported",
            )


if __name__ == "__main__":
    unittest.main()
