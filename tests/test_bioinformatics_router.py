#!/usr/bin/env python3
"""Regression tests for the public bioinformatics tool entry point."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills/ocean"
ROUTER_PATH = SKILL_DIR / "scripts/tools/bioinformatics_tool_router.py"
BIOINFORMATICS_DIR = SKILL_DIR / "scripts/tools/bioinformatics"

SPEC = importlib.util.spec_from_file_location("ocean_bioinformatics_router", ROUTER_PATH)
assert SPEC and SPEC.loader
ROUTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROUTER)


class BioinformaticsRouterTests(unittest.TestCase):
    def test_registry_and_tool_configs_are_portable(self) -> None:
        registry = ROUTER.load_registry(SKILL_DIR)
        self.assertEqual(len(registry), 115)
        self.assertEqual(len({item["slug"] for item in registry}), 115)

        for item in registry:
            tool_dir = BIOINFORMATICS_DIR / item["slug"]
            config = json.loads(
                (tool_dir / "wrapper_config.json").read_text(encoding="utf-8")
            )
            self.assertNotIn("readiness_stage", config)
            self.assertNotIn("local_smoke_status", config)
            self.assertTrue(config.get("execution_layer"))
            self.assertTrue((tool_dir / "scripts/probe_or_plan.py").exists())

            tool_metadata = json.loads(
                (tool_dir / "tool.json").read_text(encoding="utf-8")
            )
            api_metadata = json.loads(
                (tool_dir / "api.json").read_text(encoding="utf-8")
            )
            self.assertNotIn("maturity", tool_metadata)
            self.assertNotIn("maturity", api_metadata)
            boundary = api_metadata.get("evidence_boundary", {})
            self.assertNotIn("does_not_run_external_tool", boundary)
            self.assertTrue(boundary.get("source_packet_wrapper_does_not_run_external_tool"))
            self.assertTrue(boundary.get("external_execution_requires_explicit_run_command"))
            self.assertEqual(tool_metadata["slug"], item["slug"])
            self.assertEqual(tool_metadata["name"], item["name"])
            self.assertEqual(tool_metadata["family"], item["family"])
            self.assertEqual(config["tool_slug"], item["slug"])
            self.assertEqual(config["tool_name"], item["name"])
            self.assertEqual(config["tool_family"], item["family"])

            runner_by_layer = {
                "lightweight_cli": "run_cli.py",
                "python_package": "run_package.py",
                "r_bioconductor": "run_package.py",
                "heavy_launcher_plan": "run_launcher.py",
                "workflow_runtime": "run_launcher.py",
                "source_packet_adapter": "run_launcher.py",
            }
            runner = runner_by_layer[config["execution_layer"]]
            self.assertTrue((tool_dir / "scripts" / runner).exists())

            for command in api_metadata.get("commands", []):
                argv = command.get("argv", [])
                if len(argv) >= 2 and argv[0].startswith("python"):
                    self.assertTrue(
                        (tool_dir / argv[1]).exists(),
                        f"{item['slug']} has a missing API entrypoint: {argv[1]}",
                    )

    def test_profile_uses_the_tool_specific_runner(self) -> None:
        profile = ROUTER.build_profile(
            ROUTER.tool_index(SKILL_DIR)["last"],
            SKILL_DIR,
        )
        self.assertEqual(profile["execution_layer"], "lightweight_cli")
        self.assertEqual(profile["availability"], "unknown_until_checked")
        self.assertTrue(profile["wrapper_command"][1].endswith("last/scripts/run_cli.py"))
        self.assertIn("outputs/last-probe.json", profile["wrapper_command"])

    def test_every_workflow_resolves_to_registered_tools(self) -> None:
        for workflow in ROUTER.WORKFLOWS:
            plan = ROUTER.build_workflow(SKILL_DIR, workflow)
            self.assertFalse(plan["missing_tool_slugs"], workflow)
            self.assertTrue(plan["steps"], workflow)

    def test_list_tools_search_is_user_facing(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROUTER_PATH),
                "list-tools",
                "--search",
                "deseq2",
                "--format",
                "json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["tools"][0]["slug"], "deseq2")
        self.assertEqual(
            payload["tools"][0]["availability"],
            "unknown_until_checked",
        )

    def test_heavy_tool_check_creates_plan_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "alphafold-check.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROUTER_PATH),
                    "check",
                    "--tool",
                    "alphafold",
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["execution_status"], "planned_not_executed")
            self.assertIn("evidence_boundary", payload)


if __name__ == "__main__":
    unittest.main()
