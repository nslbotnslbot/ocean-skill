#!/usr/bin/env python3
"""End-to-end contract tests for OCEAN's three reference workflows."""

from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest

from control_plane_test_utils import EVALS, ROOT, read_json, run_cli, write_json


class ControlPlaneWorkflowTests(unittest.TestCase):
    def assert_manifest_valid(self, manifest: Path) -> None:
        payload = read_json(manifest)
        self.assertEqual(payload["schema_version"], "ocean-run-manifest-v1")
        self.assertEqual(payload["status"], "executed")
        self.assertTrue(payload["command"])
        self.assertEqual(payload["software"]["version"], "0.2.0")
        self.assertEqual(len(payload["inputs"][0]["sha256"]), 64)
        self.assertEqual(len(payload["outputs"][0]["sha256"]), 64)
        run_cli("manifest", "validate", "--input", manifest)

    def test_variant_workflow_blocks_formal_overclaim(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "variant.json"
            run_cli(
                "workflow",
                "variant",
                "--input",
                EVALS / "fixtures/variant_workflow.formal.json",
                "--output",
                output,
            )
            result = read_json(output)
            self.assertEqual(result["state"], "blocked_by_missing_evidence")
            self.assertIn("functional_annotation", result["missing_source_classes"])
            self.assertIn(
                result["evidence_independence"]["classification"],
                {"partially_independent", "dependent"},
            )
            self.assert_manifest_valid(Path(str(output) + ".run-manifest.json"))

    def test_target_disease_workflow_detects_circularity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "target-disease.json"
            run_cli(
                "workflow",
                "target-disease",
                "--input",
                EVALS / "fixtures/target_disease_workflow.formal.json",
                "--output",
                output,
            )
            result = read_json(output)
            self.assertEqual(result["state"], "blocked_by_missing_evidence")
            self.assertEqual(
                result["evidence_independence"]["classification"],
                "circular",
            )
            self.assertIn("clinical_registry", result["missing_source_classes"])
            self.assert_manifest_valid(Path(str(output) + ".run-manifest.json"))

    def test_manuscript_workflow_keeps_audit_notes_out_of_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / "paper-bundle.json"
            input_path = root / "manuscript-input.json"
            output = root / "manuscript-audit.json"
            run_cli(
                "paper",
                "prepare",
                "--input",
                ROOT / "README.md",
                "--output",
                bundle,
            )
            payload = copy.deepcopy(
                read_json(EVALS / "fixtures/manuscript_claims.formal.json")
            )
            payload["paper_bundle"] = str(bundle)
            write_json(input_path, payload)
            run_cli(
                "workflow",
                "manuscript",
                "--input",
                input_path,
                "--output",
                output,
            )
            result = read_json(output)
            self.assertEqual(result["state"], "needs_revision_or_evidence")
            self.assertTrue(result["priority_risks"])
            self.assertIn("separate", result["safe_rewrite_rule"])
            self.assertNotIn("rewritten_manuscript", result)
            self.assert_manifest_valid(Path(str(output) + ".run-manifest.json"))


if __name__ == "__main__":
    unittest.main()
