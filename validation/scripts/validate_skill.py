#!/usr/bin/env python3
"""Validate the minimal Codex skill frontmatter and required files."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=Path(__file__).resolve().parents[2] / "skills" / "ocean")
    args = parser.parse_args()

    skill_file = args.skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise SystemExit("SKILL.md is missing YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict):
        raise SystemExit("SKILL.md frontmatter must be a mapping")
    if frontmatter.get("name") != "ocean":
        raise SystemExit("SKILL.md name must be 'ocean'")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        raise SystemExit("SKILL.md description must be a non-empty string")
    if len(description) > 1600:
        raise SystemExit("SKILL.md description is unexpectedly long")

    openai_config = args.skill_dir / "agents" / "openai.yaml"
    manifest = args.skill_dir / "manifest.yaml"
    required = [
        openai_config,
        manifest,
        args.skill_dir / "references" / "output-contract.md",
        args.skill_dir / "references" / "module-artifact-contract.md",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("Missing required skill files: " + ", ".join(missing))
    for path in (openai_config, manifest):
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            raise SystemExit(f"{path.name} must contain a YAML mapping")
    print("Skill validation passed: ocean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
