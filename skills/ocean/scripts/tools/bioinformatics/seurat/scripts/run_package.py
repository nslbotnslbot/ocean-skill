#!/usr/bin/env python3
"""Per-tool OCEAN Python/R package runner.

Generated file. Keep tool-specific settings in ../wrapper_config.json.
"""

from __future__ import annotations

from pathlib import Path
import sys


def _find_tools_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        candidate = parent / "common" / "per_tool_package_runner.py"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find scripts/tools/common/per_tool_package_runner.py")


TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
sys.path.insert(0, str(TOOLS_ROOT / "common"))

from per_tool_package_runner import main_for_tool  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main_for_tool(Path(__file__).resolve().parents[1]))
