#!/usr/bin/env python3
"""Generate per-tool Python/R package runner entrypoints."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PACKAGE_LAYERS = {"python_package", "r_bioconductor"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def runner_script() -> str:
    return '''#!/usr/bin/env python3
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
'''


def script_placeholder(layer: str) -> str:
    return "/path/to/inspected_script.R" if layer == "r_bioconductor" else "/path/to/inspected_script.py"


def ensure_api_commands(api_path: Path, slug: str, layer: str) -> None:
    api = read_json(api_path)
    commands = api.setdefault("commands", [])
    if not any(command.get("name") == "package-probe" for command in commands):
        commands.append(
            {
                "name": "package-probe",
                "description": "Run the bounded per-tool Python/R package availability/version probe.",
                "argv": [
                    "python3",
                    "scripts/run_package.py",
                    "probe",
                    "--output",
                    f"outputs/{slug}-package-probe.json",
                    "--packet-output",
                    f"outputs/{slug}-package-probe-source-packet.json",
                ],
            }
        )
    if not any(command.get("name") == "package-run-record" for command in commands):
        commands.append(
            {
                "name": "package-run-record",
                "description": "Run an explicit user-supplied Python/R script and record bounded provenance.",
                "argv": [
                    "python3",
                    "scripts/run_package.py",
                    "run-script",
                    "--script",
                    script_placeholder(layer),
                    "--args-json",
                    "[\"<user-supplied arguments>\"]",
                    "--output",
                    f"outputs/{slug}-package-run-record.json",
                    "--packet-output",
                    f"outputs/{slug}-package-run-source-packet.json",
                ],
            }
        )
    api["package_runner_wrapper"] = "scripts/run_package.py"
    write_json(api_path, api)


def ensure_readme_section(readme_path: Path, slug: str, layer: str) -> None:
    text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    marker = "## Package Runner Wrapper"
    if marker in text:
        return
    script_path = script_placeholder(layer)
    addition = f"""

{marker}

For Python/R package tools, use `scripts/run_package.py` to record bounded package availability and explicit script provenance.

Probe only:

```bash
python3 scripts/run_package.py probe \\
  --output /path/to/{slug}-package-probe.json
```

Run an inspected local script:

```bash
python3 scripts/run_package.py run-script \\
  --script {script_path} \\
  --args-json '[\"<user-supplied arguments>\"]' \\
  --output /path/to/{slug}-package-run-record.json \\
  --packet-output /path/to/{slug}-package-run-source-packet.json
```

This runner does not install packages, choose private input files, design the analysis, validate the script, or support biological claims without downstream OCEAN audit.
"""
    readme_path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def generate(skill_dir: Path) -> list[str]:
    bio_root = skill_dir / "scripts" / "tools" / "bioinformatics"
    generated = []
    for config_path in sorted(bio_root.glob("*/wrapper_config.json")):
        folder = config_path.parent
        config = read_json(config_path)
        layer = config.get("execution_layer")
        if layer not in PACKAGE_LAYERS:
            continue
        script_path = folder / "scripts" / "run_package.py"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(runner_script(), encoding="utf-8")
        script_path.chmod(0o755)
        config["package_runner_wrapper"] = "scripts/run_package.py"
        config["package_runner_boundary"] = "Runs only bounded package probes or explicit user-supplied scripts; records provenance only."
        write_json(config_path, config)
        ensure_api_commands(folder / "api.json", config["tool_slug"], layer)
        ensure_readme_section(folder / "README.md", config["tool_slug"], layer)
        generated.append(config["tool_slug"])
    return generated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Python/R package runner wrappers.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    generated = generate(args.skill_dir)
    print(json.dumps({"generated": len(generated), "tools": generated}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
