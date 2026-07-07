#!/usr/bin/env python3
"""Generate per-tool CLI runner entrypoints for lightweight bioinformatics CLIs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def runner_script() -> str:
    return '''#!/usr/bin/env python3
"""Per-tool OCEAN lightweight CLI runner.

Generated file. Keep tool-specific settings in ../wrapper_config.json.
"""

from __future__ import annotations

from pathlib import Path
import sys


def _find_tools_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        candidate = parent / "common" / "per_tool_cli_runner.py"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find scripts/tools/common/per_tool_cli_runner.py")


TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
sys.path.insert(0, str(TOOLS_ROOT / "common"))

from per_tool_cli_runner import main_for_tool  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main_for_tool(Path(__file__).resolve().parents[1]))
'''


def ensure_api_commands(api_path: Path, slug: str) -> None:
    api = read_json(api_path)
    commands = api.setdefault("commands", [])
    if not any(command.get("name") == "cli-probe" for command in commands):
        commands.append(
            {
                "name": "cli-probe",
                "description": "Run the bounded per-tool CLI availability/version/help probe.",
                "argv": [
                    "python3",
                    "scripts/run_cli.py",
                    "probe",
                    "--output",
                    f"outputs/{slug}-cli-probe.json",
                    "--packet-output",
                    f"outputs/{slug}-cli-probe-source-packet.json",
                ],
            }
        )
    if not any(command.get("name") == "cli-run-record" for command in commands):
        commands.append(
            {
                "name": "cli-run-record",
                "description": "Run user-supplied local CLI arguments and record bounded provenance. Replace the placeholder args with a real inspected command plan.",
                "argv": [
                    "python3",
                    "scripts/run_cli.py",
                    "run",
                    "--args-json",
                    "[\"<user-supplied arguments>\"]",
                    "--output",
                    f"outputs/{slug}-cli-run-record.json",
                    "--packet-output",
                    f"outputs/{slug}-cli-run-source-packet.json",
                ],
            }
        )
    api["cli_runner_wrapper"] = "scripts/run_cli.py"
    write_json(api_path, api)


def ensure_readme_section(readme_path: Path, slug: str) -> None:
    text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    marker = "## CLI Runner Wrapper"
    if marker in text:
        return
    addition = f"""

{marker}

For lightweight CLI tools, use `scripts/run_cli.py` to record bounded local CLI provenance.

Probe only:

```bash
python3 scripts/run_cli.py probe \\
  --output /path/to/{slug}-cli-probe.json
```

Run with explicit user-supplied arguments:

```bash
python3 scripts/run_cli.py run \\
  --args-json '[\"<user-supplied arguments>\"]' \\
  --output /path/to/{slug}-cli-run-record.json \\
  --packet-output /path/to/{slug}-cli-run-source-packet.json
```

This runner does not install software, choose private input files, download references, or validate scientific claims. It records command provenance for downstream OCEAN review.
"""
    readme_path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def generate(skill_dir: Path) -> list[str]:
    bio_root = skill_dir / "scripts" / "tools" / "bioinformatics"
    generated = []
    for config_path in sorted(bio_root.glob("*/wrapper_config.json")):
        folder = config_path.parent
        config = read_json(config_path)
        if config.get("execution_layer") != "lightweight_cli":
            continue
        script_path = folder / "scripts" / "run_cli.py"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(runner_script(), encoding="utf-8")
        script_path.chmod(0o755)
        config["cli_runner_wrapper"] = "scripts/run_cli.py"
        config["cli_runner_boundary"] = "Runs local command only when executable exists and user supplies explicit arguments; records provenance only."
        write_json(config_path, config)
        ensure_api_commands(folder / "api.json", config["tool_slug"])
        ensure_readme_section(folder / "README.md", config["tool_slug"])
        generated.append(config["tool_slug"])
    return generated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate lightweight CLI runner wrappers.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    generated = generate(args.skill_dir)
    print(json.dumps({"generated": len(generated), "tools": generated}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
