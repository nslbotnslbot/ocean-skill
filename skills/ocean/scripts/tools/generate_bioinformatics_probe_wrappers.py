#!/usr/bin/env python3
"""Generate per-tool OCEAN probe/plan wrappers for bioinformatics tools.

This fills each `scripts/tools/bioinformatics/<tool>/` folder with:

- `wrapper_config.json`
- `scripts/probe_or_plan.py`
- an API command entry for the generated wrapper

The generated wrappers are bounded availability/plan entrypoints. They do not
install software, download references, execute analyses, or validate claims.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from bioinformatics_tool_router import (
    PYTHON_PACKAGES,
    R_PACKAGES,
    build_profile,
    cli_probe_args,
    load_registry,
    primary_entrypoint,
)


READINESS_PREFIX = "bioinformatics-wrapper-readiness-all-r1"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def probe_script() -> str:
    return '''#!/usr/bin/env python3
"""Per-tool OCEAN probe/plan entrypoint.

Generated file. Keep tool-specific settings in ../wrapper_config.json.
"""

from __future__ import annotations

from pathlib import Path
import sys


def _find_tools_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        candidate = parent / "common" / "per_tool_probe_or_plan.py"
        if candidate.exists():
            return parent
    raise RuntimeError("Could not find scripts/tools/common/per_tool_probe_or_plan.py")


TOOLS_ROOT = _find_tools_root(Path(__file__).resolve())
sys.path.insert(0, str(TOOLS_ROOT / "common"))

from per_tool_probe_or_plan import main_for_tool  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main_for_tool(Path(__file__).resolve().parents[1]))
'''


def load_readiness(skill_dir: Path) -> dict[str, dict[str, Any]]:
    artifacts_dir = skill_dir / "evals" / f"{READINESS_PREFIX}-artifacts"
    rows = {}
    if not artifacts_dir.exists():
        return rows
    for path in artifacts_dir.glob("*-readiness-plan.json"):
        data = read_json(path)
        rows[data["tool"]["slug"]] = data
    return rows


def wrapper_mode(profile: dict[str, Any]) -> str:
    layer = profile["execution_layer"]
    if layer == "lightweight_cli":
        return "cli_probe"
    if layer == "workflow_runtime":
        return "cli_probe"
    if layer == "r_bioconductor":
        return "r_package_check"
    if layer == "python_package":
        return "python_import_check"
    if layer == "heavy_launcher_plan":
        return "heavy_launcher_plan"
    if layer == "source_packet_adapter":
        return "source_packet_adapter_plan"
    return "run_record_template"


def command_and_probe_args(profile: dict[str, Any]) -> tuple[list[str], list[str]]:
    slug = profile["tool_slug"]
    entrypoint = primary_entrypoint(slug)
    if profile["execution_layer"] == "workflow_runtime":
        return [entrypoint], [cli_probe_args(slug)]
    if profile["execution_layer"] == "lightweight_cli":
        return [entrypoint], [cli_probe_args(slug)]
    return [], []


def make_config(tool: dict[str, Any], profile: dict[str, Any], readiness: dict[str, Any] | None) -> dict[str, Any]:
    slug = tool["slug"]
    mode = wrapper_mode(profile)
    command, probe_args = command_and_probe_args(profile)
    readiness = readiness or {}
    state = readiness.get("current_ocean_state", {})
    smoke_command = readiness.get("smoke_command", [])
    entrypoint = primary_entrypoint(slug)
    config = {
        "schema_version": "ocean-bioinformatics-per-tool-wrapper-v1",
        "tool_name": tool["name"],
        "tool_slug": slug,
        "tool_family": tool["family"],
        "execution_layer": profile["execution_layer"],
        "wrapper_mode": mode,
        "entrypoint": entrypoint,
        "command": command,
        "probe_args": probe_args,
        "smoke_command": smoke_command,
        "readiness_stage": readiness.get("readiness_stage", ""),
        "local_smoke_status": state.get("local_smoke_status", ""),
        "candidate_install_routes": readiness.get("candidate_install_routes", []),
        "minimal_fixture": readiness.get("minimal_fixture", ""),
        "expected_outputs": readiness.get("expected_outputs", []),
        "required_run_evidence": readiness.get("required_run_evidence", profile.get("required_evidence", [])),
        "stop_conditions": readiness.get("stop_conditions", profile.get("stop_conditions", [])),
        "source_packet_wrapper": "scripts/create_source_packet.py",
        "probe_or_plan_wrapper": "scripts/probe_or_plan.py",
        "task_intent": f"{tool['name']} bounded availability probe or launcher/source-packet plan",
        "command_template": f"{entrypoint} <user-supplied arguments>",
        "handoff": readiness.get("handoff") or profile.get("handoff", "Anchor"),
        "environment_note": "current local PATH/Python/R environment unless a verified container or workflow runtime is supplied",
        "evidence_boundary": "Per-tool wrapper config only; not installation, execution, benchmark, or biological validation.",
    }
    if slug in R_PACKAGES:
        config["r_package"] = R_PACKAGES[slug][0]
    if slug in PYTHON_PACKAGES:
        config["python_module"] = PYTHON_PACKAGES[slug][0]
    return config


def ensure_api_command(api_path: Path, slug: str) -> None:
    api = read_json(api_path)
    commands = api.setdefault("commands", [])
    if not any(command.get("name") == "probe-or-plan" for command in commands):
        commands.append(
            {
                "name": "probe-or-plan",
                "description": "Run a bounded availability probe or create a launcher/source-packet plan for this tool.",
                "argv": [
                    "python3",
                    "scripts/probe_or_plan.py",
                    "--output",
                    f"outputs/{slug}-probe-or-plan.json",
                ],
            }
        )
    api["probe_or_plan_wrapper"] = "scripts/probe_or_plan.py"
    api["wrapper_config"] = "wrapper_config.json"
    write_json(api_path, api)


def ensure_readme_section(readme_path: Path, slug: str) -> None:
    text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    marker = "## Probe / Plan Wrapper"
    if marker in text:
        return
    addition = f"""

{marker}

Use `scripts/probe_or_plan.py` to run the bounded per-tool availability probe or to create a launcher/source-packet plan:

```bash
python3 scripts/probe_or_plan.py \\
  --output /path/to/{slug}-probe-or-plan.json
```

This wrapper records availability or planning evidence only. It does not install the tool, download databases, run biological analyses, benchmark methods, or validate scientific claims.
"""
    readme_path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate per-tool OCEAN bioinformatics probe/plan wrappers.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    args = parser.parse_args(argv)

    bio_root = args.skill_dir / "scripts" / "tools" / "bioinformatics"
    readiness_by_slug = load_readiness(args.skill_dir)
    registry = load_registry(args.skill_dir)
    generated = []
    for tool in registry:
        slug = tool["slug"]
        folder = bio_root / slug
        profile = build_profile(tool, args.skill_dir)
        config = make_config(tool, profile, readiness_by_slug.get(slug))
        write_json(folder / "wrapper_config.json", config)
        script_path = folder / "scripts" / "probe_or_plan.py"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(probe_script(), encoding="utf-8")
        ensure_api_command(folder / "api.json", slug)
        ensure_readme_section(folder / "README.md", slug)
        generated.append(slug)
    print(json.dumps({"generated": len(generated), "tools": generated}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
