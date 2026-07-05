#!/usr/bin/env python3
"""Evaluate OCEAN's bioinformatics tool router."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


EXPECTED_WORKFLOWS = [
    "fastq-qc",
    "rna-seq-differential-expression",
    "variant-calling-qc",
    "single-cell-rna-seq",
    "spatial-transcriptomics",
    "metagenomics-microbiome",
    "genome-assembly-annotation",
    "protein-structure",
    "epigenomics-peak-calling",
    "proteomics-metabolomics",
    "workflow-reproducibility",
    "imaging-ai",
]


def load_router(router_path: Path):
    spec = importlib.util.spec_from_file_location("bioinformatics_tool_router", router_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load router: {router_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_command(command: list[str], timeout: int = 30) -> tuple[int, str]:
    proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    return proc.returncode, (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")


def check_profile(profile: dict[str, Any]) -> list[str]:
    missing = []
    for field in [
        "tool_name",
        "tool_slug",
        "family",
        "execution_layer",
        "wrapper",
        "wrapper_command",
        "required_evidence",
        "stop_conditions",
        "evidence_boundary",
    ]:
        if not profile.get(field):
            missing.append(field)
    if "subprocess_wrapper.py" in str(profile.get("wrapper")) and "--command" not in profile.get("wrapper_command", []):
        missing.append("cli_wrapper_command_shape")
    if profile.get("execution_layer") == "heavy_launcher_plan" and "launcher" not in profile.get("wrapper", ""):
        missing.append("heavy_wrapper_shape")
    return missing


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run OCEAN bioinformatics tool-router eval.")
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args(argv)

    router_path = args.skill_dir / "scripts" / "tools" / "bioinformatics_tool_router.py"
    router = load_router(router_path)
    catalog = router.export_catalog(args.skill_dir)
    args.outdir.mkdir(parents=True, exist_ok=True)
    artifact_dir = args.outdir / "bioinformatics-tool-router-r1-artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    write_json(artifact_dir / "catalog.json", catalog)

    rows: list[dict[str, Any]] = []
    for profile in catalog["profiles"]:
        missing = check_profile(profile)
        rows.append(
            {
                "case_type": "profile",
                "name": profile["tool_slug"],
                "execution_layer": profile["execution_layer"],
                "verdict": "pass" if not missing else "needs_review",
                "notes": ",".join(missing),
            }
        )

    workflow_rows = []
    for workflow in EXPECTED_WORKFLOWS:
        json_out = artifact_dir / f"{workflow}.json"
        md_out = artifact_dir / f"{workflow}.md"
        code, output = run_command(
            [
                sys.executable,
                str(router_path),
                "workflow",
                "--skill-dir",
                str(args.skill_dir),
                "--workflow",
                workflow,
                "--output",
                str(json_out),
                "--markdown-output",
                str(md_out),
            ]
        )
        plan = read_json(json_out) if json_out.exists() else {}
        notes = []
        if code != 0:
            notes.append("workflow_command_failed")
        if plan.get("missing_tool_slugs"):
            notes.append("missing_tool_slugs")
        if len(plan.get("steps", [])) < 4:
            notes.append("too_few_steps")
        if not plan.get("negative_space"):
            notes.append("missing_negative_space")
        if workflow == "fastq-qc":
            slugs = {step["tool_slug"] for step in plan.get("steps", [])}
            if not {"fastqc", "multiqc"}.issubset(slugs):
                notes.append("missing_fastq_qc_core")
        if workflow == "protein-structure":
            layers = {step["execution_layer"] for step in plan.get("steps", [])}
            if "source_packet_adapter" not in layers or "heavy_launcher_plan" not in layers:
                notes.append("missing_structure_layer_mix")
        if workflow == "workflow-reproducibility":
            layers = {step["execution_layer"] for step in plan.get("steps", [])}
            if "workflow_runtime" not in layers:
                notes.append("missing_workflow_runtime")
        row = {
            "case_type": "workflow",
            "name": workflow,
            "execution_layer": "mixed",
            "verdict": "pass" if not notes else "needs_review",
            "notes": ",".join(notes) or output[:500],
        }
        rows.append(row)
        workflow_rows.append(row)

    layers = catalog["by_execution_layer"]
    layer_checks = {
        "has_lightweight_cli": layers.get("lightweight_cli", 0) > 0,
        "has_r_bioconductor": layers.get("r_bioconductor", 0) > 0,
        "has_heavy_launcher_plan": layers.get("heavy_launcher_plan", 0) > 0,
        "has_python_package": layers.get("python_package", 0) > 0,
        "has_workflow_runtime": layers.get("workflow_runtime", 0) > 0,
        "has_source_packet_adapter": layers.get("source_packet_adapter", 0) > 0,
    }
    for name, passed in layer_checks.items():
        rows.append(
            {
                "case_type": "layer_coverage",
                "name": name,
                "execution_layer": "catalog",
                "verdict": "pass" if passed else "needs_review",
                "notes": "",
            }
        )

    summary = {
        "run_date": dt.date.today().isoformat(),
        "cases": len(rows),
        "pass": sum(1 for row in rows if row["verdict"] == "pass"),
        "needs_review": sum(1 for row in rows if row["verdict"] != "pass"),
        "tools_profiled": catalog["tools"],
        "workflows_planned": len(workflow_rows),
        "by_execution_layer": layers,
        "boundary": "Router/profile/workflow-plan eval only; no external tool execution or scientific validation.",
    }

    write_json(args.outdir / "bioinformatics-tool-router-r1-results.json", rows)
    write_json(args.outdir / "bioinformatics-tool-router-r1-summary.json", summary)
    with (args.outdir / "bioinformatics-tool-router-r1-scorecard.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=["case_type", "name", "execution_layer", "verdict", "notes"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    lines = [
        "# OCEAN Bioinformatics Tool Router Eval R1",
        "",
        f"- Run date: {summary['run_date']}",
        f"- Cases: {summary['cases']}",
        f"- Pass: {summary['pass']}",
        f"- Needs review: {summary['needs_review']}",
        f"- Tools profiled: {summary['tools_profiled']}",
        f"- Workflows planned: {summary['workflows_planned']}",
        "",
        "## Execution Layer Coverage",
        "",
        "| Layer | Count |",
        "|---|---:|",
        *[f"| {key} | {value} |" for key, value in sorted(layers.items())],
        "",
        "## Workflow Cases",
        "",
        "| Workflow | Verdict | Notes |",
        "|---|---|---|",
        *[f"| {row['name']} | {row['verdict']} | {row['notes']} |" for row in workflow_rows],
        "",
        "## Evidence Boundary / 证据边界",
        "",
        "This eval checks routing/profile/workflow-plan behavior only. It does not install or run external bioinformatics tools, download references, process biological/clinical data, benchmark methods, or validate scientific claims.",
    ]
    (args.outdir / "bioinformatics-tool-router-r1-results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["needs_review"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
