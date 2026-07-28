#!/usr/bin/env python3
"""Guard the boundary between the public package and local working records."""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATHS = (
    "validation",
    "docs/evaluation",
    "docs/case-studies",
    "docs/application-submission-tracker.md",
    "docs/project-boundary.md",
    "skills/ocean/static",
)

FORBIDDEN_REFERENCES = (
    "`validation/",
    "](validation/",
    "docs/evaluation/",
    "docs/case-studies/",
    "docs/application-submission-tracker.md",
    "docs/project-boundary.md",
    "/Users/",
    "codex://threads/",
)

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def public_contract_files() -> list[Path]:
    files = [
        ROOT / "README.md",
        ROOT / "README.zh-CN.md",
        ROOT / "CHANGELOG.md",
        ROOT / "AGENTS.md",
        ROOT / "skills/ocean/SKILL.md",
        ROOT / "skills/ocean/manifest.yaml",
    ]
    for directory in (
        ROOT / "docs",
        ROOT / "projects",
        ROOT / "skills/ocean/references",
    ):
        files.extend(directory.rglob("*.md"))
    return files


class PublicRepositoryBoundaryTests(unittest.TestCase):
    def test_internal_archive_paths_are_absent(self) -> None:
        for relative_path in FORBIDDEN_PATHS:
            self.assertFalse(
                (ROOT / relative_path).exists(),
                f"Internal archive path must not be public: {relative_path}",
            )

    def test_public_contract_does_not_link_to_internal_archives(self) -> None:
        for path in public_contract_files():
            text = path.read_text(encoding="utf-8")
            for reference in FORBIDDEN_REFERENCES:
                self.assertNotIn(
                    reference,
                    text,
                    f"{path.relative_to(ROOT)} links to removed internal material",
                )

    def test_local_markdown_links_resolve(self) -> None:
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for match in MARKDOWN_LINK.finditer(text):
                target = match.group(1).strip().strip("<>")
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = unquote(target.split("#", 1)[0])
                if not target:
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    (
                        f"{path.relative_to(ROOT)} has a broken local link: "
                        f"{match.group(1)}"
                    ),
                )

    def test_installable_skill_excludes_development_runners(self) -> None:
        tools_dir = ROOT / "skills/ocean/scripts/tools"
        forbidden_globs = ("run_*_eval.py", "build_*.py", "generate_*.py")
        for pattern in forbidden_globs:
            self.assertFalse(
                list(tools_dir.glob(pattern)),
                f"Development runner leaked into installable skill: {pattern}",
            )

    def test_generated_output_directories_are_ignored(self) -> None:
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/outputs/*", gitignore)
        self.assertIn("**/outputs/", gitignore)

    def test_public_docs_use_ocean_language(self) -> None:
        borrowed_labels = (
            "science-skills-style",
            "inspired by science-skills",
            "alphascience",
            "claude science",
        )
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8").casefold()
            for label in borrowed_labels:
                self.assertNotIn(
                    label,
                    text,
                    f"{path.relative_to(ROOT)} contains development comparison language",
                )


if __name__ == "__main__":
    unittest.main()
