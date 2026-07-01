#!/usr/bin/env python3
"""Check OCEAN public docs and M1 outputs for adjacent-framework drift."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys


HIGH_RISK_PHRASES = [
    "execution-drafted",
    "guidance-reviewed",
    "evidence ledger",
    "human-supervised release",
    "release gate",
    "release-gated",
    "manuscript-facing release",
    "endpoint calibration",
    "endpoint status",
    "outcome spectrum",
    "source-proof card",
    "proof object",
    "claim-after",
    "paired non-claim",
    "decision node",
    "artifact route",
    "execution package",
]

GUARDRAIL_MARKERS = [
    "avoid",
    "do not",
    "not ",
    "not a",
    "not an",
    "rather than",
    "instead of",
    "should avoid",
    "should not",
    "不要",
    "不是",
    "不做",
    "避免",
    "而不是",
    "avoided framing",
    "preferred vocabulary",
    "differentiation guardrail",
    "| avoid | prefer |",
]

PUBLIC_TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml"}
PUBLIC_JSON_SUFFIXES = {".json"}
GENERATED_SELF_FILES = {
    "skills/ocean/evals/ocean-differentiation-m3-results.md",
    "skills/ocean/evals/ocean-differentiation-m3-summary.json",
}
SKIP_PUBLIC_FILE_NAMES = {
    "sounding-article-error-matrix-r2.json",
    "sounding-article-error-matrix-r3.json",
    "sounding-multimodel-cases.json",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def line_context(line: str) -> str:
    return line.strip()[:240]


def is_guardrail_context(context: str) -> bool:
    lowered = context.lower()
    return any(marker in lowered for marker in GUARDRAIL_MARKERS)


def scan_text(path: Path, text: str, repo_root: Path, source: str) -> list[dict]:
    rows = []
    rel = str(path.relative_to(repo_root)) if path.is_relative_to(repo_root) else str(path)
    lines = text.splitlines()
    for line_no, line in enumerate(lines, 1):
        lowered = line.lower()
        for phrase in HIGH_RISK_PHRASES:
            if phrase.lower() in lowered:
                window = "\n".join(lines[max(0, line_no - 15):line_no])
                rows.append({
                    "source": source,
                    "path": rel,
                    "line": line_no,
                    "phrase": phrase,
                    "guardrail_context": is_guardrail_context(window),
                    "context": line_context(line),
                })
    return rows


def iter_public_files(repo_root: Path) -> list[Path]:
    roots = [
        repo_root / "README.md",
        repo_root / "README.zh-CN.md",
        repo_root / "CHANGELOG.md",
        repo_root / "docs",
        repo_root / "skills/ocean/SKILL.md",
        repo_root / "skills/ocean/agents",
        repo_root / "skills/ocean/references",
        repo_root / "skills/ocean/evals",
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            rel = str(root.relative_to(repo_root)) if root.is_relative_to(repo_root) else str(root)
            if rel not in GENERATED_SELF_FILES:
                files.append(root)
        elif root.exists():
            for path in root.rglob("*"):
                if path.name in SKIP_PUBLIC_FILE_NAMES:
                    continue
                if path.is_file() and (path.suffix in PUBLIC_TEXT_SUFFIXES or path.suffix in PUBLIC_JSON_SUFFIXES or path.suffix == ".csv"):
                    rel = str(path.relative_to(repo_root)) if path.is_relative_to(repo_root) else str(path)
                    if rel not in GENERATED_SELF_FILES:
                        files.append(path)
    return sorted(set(files))


def output_paths_from_coverage(repo_root: Path, coverage_path: Path) -> list[Path]:
    coverage = load_json(coverage_path)
    cases = load_json(repo_root / "skills/ocean/evals/ocean-module-eval-cases.json").get("cases", [])
    case_ids = [case["id"] for case in cases]
    outputs: list[Path] = []
    for row in coverage.get("rows", []):
        roots = [part.strip() for part in row.get("artifact_roots", "").split(";") if part.strip()]
        for case_id in case_ids:
            for root in reversed(roots):
                output = repo_root / root / case_id / "output.md"
                if output.exists():
                    outputs.append(output)
                    break
    return outputs


def markdown_table(rows: list[dict], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parents[3]
    public_rows: list[dict] = []
    for path in iter_public_files(repo_root):
        try:
            public_rows.extend(scan_text(path, read_text(path), repo_root, "public_repo"))
        except UnicodeDecodeError:
            continue

    output_rows: list[dict] = []
    for path in output_paths_from_coverage(repo_root, args.coverage):
        output_rows.extend(scan_text(path, read_text(path), repo_root, "m1_output"))

    all_rows = public_rows + output_rows
    unqualified = [row for row in all_rows if not row["guardrail_context"]]
    guardrail_rows = [row for row in all_rows if row["guardrail_context"]]
    by_source = {
        "public_repo": sum(1 for row in unqualified if row["source"] == "public_repo"),
        "m1_output": sum(1 for row in unqualified if row["source"] == "m1_output"),
    }
    summary = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "protocol": "skills/ocean/evals/ocean-differentiation-m3-protocol.md",
        "coverage_input": str(args.coverage.relative_to(repo_root) if args.coverage.is_relative_to(repo_root) else args.coverage),
        "public_files_scanned": len(iter_public_files(repo_root)),
        "m1_outputs_scanned": len(output_paths_from_coverage(repo_root, args.coverage)),
        "guardrail_mentions": len(guardrail_rows),
        "unqualified_high_risk_mentions": len(unqualified),
        "unqualified_by_source": by_source,
        "status": "pass" if not unqualified else "needs_review",
        "boundary": "Positioning/similarity guardrail only; not legal or scientific originality review.",
    }
    write_text(args.summary, json.dumps(summary, ensure_ascii=False, indent=2))

    review_rows = [
        {
            "source": row["source"],
            "path": row["path"],
            "line": row["line"],
            "phrase": row["phrase"],
            "context": row["context"].replace("|", "/"),
        }
        for row in unqualified[:30]
    ]
    guardrail_preview = [
        {
            "path": row["path"],
            "line": row["line"],
            "phrase": row["phrase"],
            "context": row["context"].replace("|", "/"),
        }
        for row in guardrail_rows[:12]
    ]

    body = [
        "# OCEAN Differentiation Eval M3 Results",
        f"Date: {summary['generated_at']}",
        "M3 checks whether OCEAN public docs and saved M1 outputs drift toward adjacent execution-ledger / release-gate / endpoint-calibration framing.",
        "## Boundary\n\nThis is a positioning and similarity-avoidance scan. It is not legal clearance, trademark clearance, scientific superiority, or originality proof.",
        "## Summary",
        markdown_table([
            {"metric": "Public files scanned", "value": summary["public_files_scanned"]},
            {"metric": "M1 outputs scanned", "value": summary["m1_outputs_scanned"]},
            {"metric": "Guardrail mentions", "value": summary["guardrail_mentions"]},
            {"metric": "Unqualified high-risk mentions", "value": summary["unqualified_high_risk_mentions"]},
            {"metric": "Status", "value": summary["status"]},
        ], ["metric", "value"]),
        "## Unqualified Mentions Requiring Review",
        markdown_table(review_rows, ["source", "path", "line", "phrase", "context"]) if review_rows else "None.",
        "## Guardrail Mentions",
        markdown_table(guardrail_preview, ["path", "line", "phrase", "context"]) if guardrail_preview else "None.",
        "## Artifacts\n\n- Protocol: `skills/ocean/evals/ocean-differentiation-m3-protocol.md`\n- Summary JSON: `skills/ocean/evals/ocean-differentiation-m3-summary.json`\n- Script: `skills/ocean/scripts/check_ocean_differentiation.py`",
    ]
    write_text(args.results, "\n\n".join(body) + "\n")
    print(args.results)
    print(args.summary)
    print(summary["status"])
    return 0 if summary["status"] == "pass" else 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Check OCEAN differentiation guardrails.")
    parser.add_argument("--coverage", type=Path, default=repo_root / "skills/ocean/evals/ocean-module-m1-coverage.json")
    parser.add_argument("--summary", type=Path, default=repo_root / "skills/ocean/evals/ocean-differentiation-m3-summary.json")
    parser.add_argument("--results", type=Path, default=repo_root / "skills/ocean/evals/ocean-differentiation-m3-results.md")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(run(parse_args(sys.argv[1:])))
