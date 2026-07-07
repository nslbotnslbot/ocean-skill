#!/usr/bin/env python3
"""Generate per-tool launcher/workflow runner entrypoints."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


LAUNCHER_LAYERS = {"heavy_launcher_plan", "workflow_runtime", "source_packet_adapter"}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def runner_script() -> str:
    return '''#!/usr/bin/env python3
"""Per-tool OCEAN launcher/workflow runner.

Generated file. Keep tool-specific settings in ../wrapper_config.json.
"""

from __future__ import annotations

from pathlib import Path
import sys


def _find_tools_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        candidate = parent / "common" / "per_tool_launcher_runner.py"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find scripts/tools/common/per_tool_launcher_runner.py")


TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
sys.path.insert(0, str(TOOLS_ROOT / "common"))

from per_tool_launcher_runner import main_for_tool  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main_for_tool(Path(__file__).resolve().parents[1]))
'''


def ensure_api_commands(api_path: Path, slug: str, layer: str) -> None:
    api = read_json(api_path)
    commands = api.setdefault("commands", [])
    if not any(command.get("name") == "launcher-plan" for command in commands):
        commands.append(
            {
                "name": "launcher-plan",
                "description": "Create a bounded non-executing launcher/workflow/source-packet plan.",
                "argv": [
                    "python3",
                    "scripts/run_launcher.py",
                    "plan",
                    "--output",
                    f"outputs/{slug}-launcher-plan.json",
                ],
            }
        )
    if layer == "workflow_runtime":
        if not any(command.get("name") == "runtime-probe" for command in commands):
            commands.append(
                {
                    "name": "runtime-probe",
                    "description": "Run the bounded workflow-runtime availability/version probe.",
                    "argv": [
                        "python3",
                        "scripts/run_launcher.py",
                        "probe-runtime",
                        "--output",
                        f"outputs/{slug}-runtime-probe.json",
                        "--packet-output",
                        f"outputs/{slug}-runtime-probe-source-packet.json",
                    ],
                }
            )
        if not any(command.get("name") == "runtime-run-record" for command in commands):
            commands.append(
                {
                    "name": "runtime-run-record",
                    "description": "Run user-supplied workflow-runtime arguments and record bounded provenance. Replace placeholder args with an inspected command plan.",
                    "argv": [
                        "python3",
                        "scripts/run_launcher.py",
                        "run-runtime",
                        "--args-json",
                        "[\"<user-supplied arguments>\"]",
                        "--output",
                        f"outputs/{slug}-runtime-run-record.json",
                        "--packet-output",
                        f"outputs/{slug}-runtime-run-source-packet.json",
                    ],
                }
            )
    api["launcher_runner_wrapper"] = "scripts/run_launcher.py"
    write_json(api_path, api)


def ensure_readme_section(readme_path: Path, slug: str, layer: str) -> None:
    text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    marker = "## Launcher / Workflow Runner Wrapper"
    if marker in text:
        return
    workflow_block = ""
    if layer == "workflow_runtime":
        workflow_block = f"""

Probe workflow runtime availability:

```bash
python3 scripts/run_launcher.py probe-runtime \\
  --output /path/to/{slug}-runtime-probe.json
```

Run explicit workflow-runtime arguments:

```bash
python3 scripts/run_launcher.py run-runtime \\
  --args-json '[\"<user-supplied arguments>\"]' \\
  --output /path/to/{slug}-runtime-run-record.json \\
  --packet-output /path/to/{slug}-runtime-run-source-packet.json
```
"""
    addition = f"""

{marker}

Use `scripts/run_launcher.py` to create a bounded non-executing launch/source-packet plan:

```bash
python3 scripts/run_launcher.py plan \\
  --output /path/to/{slug}-launcher-plan.json
```
{workflow_block}
This runner does not install software, download references, choose private input files, launch GUI/GPU/HPC jobs, complete workflows, benchmark methods, or validate scientific claims.
"""
    readme_path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def generate(skill_dir: Path) -> list[str]:
    bio_root = skill_dir / "scripts" / "tools" / "bioinformatics"
    generated = []
    for config_path in sorted(bio_root.glob("*/wrapper_config.json")):
        folder = config_path.parent
        config = read_json(config_path)
        layer = config.get("execution_layer")
        if layer not in LAUNCHER_LAYERS:
            continue
        script_path = folder / "scripts" / "run_launcher.py"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(runner_script(), encoding="utf-8")
        script_path.chmod(0o755)
        config["launcher_runner_wrapper"] = "scripts/run_launcher.py"
        config["launcher_runner_boundary"] = "Creates non-executing launcher/source-packet plans; workflow runtimes may also run bounded availability probes."
        write_json(config_path, config)
        ensure_api_commands(folder / "api.json", config["tool_slug"], layer)
        ensure_readme_section(folder / "README.md", config["tool_slug"], layer)
        generated.append(config["tool_slug"])
    return generated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate launcher/workflow runner wrappers.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    generated = generate(args.skill_dir)
    print(json.dumps({"generated": len(generated), "tools": generated}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
