#!/usr/bin/env python3
"""Per-database OCEAN Reef query-packet entrypoint.

Generated file. Keep adapter-specific settings in ../adapter_config.json.
"""

from __future__ import annotations

from pathlib import Path
import sys


def _find_tools_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        candidate = parent / "common" / "database_adapter_entrypoint.py"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find scripts/tools/common/database_adapter_entrypoint.py")


TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
sys.path.insert(0, str(TOOLS_ROOT / "common"))

from database_adapter_entrypoint import main_for_adapter  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main_for_adapter(Path(__file__).resolve().parents[1]))
