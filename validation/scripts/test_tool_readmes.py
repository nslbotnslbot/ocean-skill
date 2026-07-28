#!/usr/bin/env python3
"""Keep the bilingual parent tool indexes synchronized with tool manifests."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "skills" / "ocean" / "scripts"
TOOLS_DIR = SCRIPTS_DIR / "tools"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ToolReadmeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.english_path = SCRIPTS_DIR / "README.md"
        self.chinese_path = SCRIPTS_DIR / "README.zh-CN.md"
        self.english = self.english_path.read_text(encoding="utf-8")
        self.chinese = self.chinese_path.read_text(encoding="utf-8")

    def test_bilingual_indexes_cover_every_registered_tool(self) -> None:
        registry = load_json(TOOLS_DIR / "bioinformatics" / "registry.json")
        database_tools = [
            load_json(path)
            for path in sorted((TOOLS_DIR / "databases").glob("*/tool.json"))
        ]

        self.assertEqual(115, len(registry))
        self.assertEqual(13, len(database_tools))

        for document in (self.english, self.chinese):
            for tool in registry:
                self.assertIn(tool["name"], document)
            for tool in database_tools:
                self.assertIn(tool["name"], document)

    def test_indexes_cover_tool_layers_and_boundaries(self) -> None:
        for document in (self.english, self.chinese):
            for required in (
                "tools/bioinformatics/",
                "tools/databases/",
                "tools/literature/",
                "tools/clinicaltrials/",
                "tools/common/",
                "Covered",
                "Available",
                "Executed",
            ):
                self.assertIn(required, document)

        self.assertIn("not automatically available or", self.english)
        self.assertIn("不代表当前机器一定已经安装或运行", self.chinese)

    def test_indexes_link_to_each_other(self) -> None:
        self.assertIn("[中文工具说明](README.zh-CN.md)", self.english)
        self.assertIn("[English version](README.md)", self.chinese)


if __name__ == "__main__":
    unittest.main()

