#!/usr/bin/env python3
"""Score OCEAN module outputs with the M3 OCEAN-10 rubric.

This script is a deterministic screening layer. It prefers output.clean.md
when available, keeps the old M2 scorer untouched, and reports both numeric
scores and flags for manual review.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
import re
import statistics
import sys

import score_ocean_module_m2 as m2


DIMENSIONS = [
    "task_framing",
    "evidence_boundary",
    "source_traceability",
    "claim_calibration",
    "no_invention",
    "negative_space",
    "artifact_quality",
    "handoff_correctness",
    "research_usefulness",
    "output_consistency",
]

REQUIRED_HEADINGS = [
    "Module任务定义",
    "Evidence Boundary",
    "Module-specific output",
    "Negative Space",
    "Handoff or Stop Condition",
    "OCEAN behavior verdict",
]

TRACEABILITY_TERMS = [
    "doi",
    "arxiv",
    "url",
    "pmid",
    "来源",
    "source",
    "identifier",
    "标识符",
    "未提供",
    "未检查",
    "不可追踪",
    "source packet",
]

NEGATIVE_SPACE_TERMS = [
    "negative space",
    "未检查",
    "未找到",
    "不可推出",
    "不能推出",
    "证据缺口",
    "缺失",
    "反例",
    "替代解释",
    "矛盾",
    "过度外推",
    "不能判断",
]

MODULE_ARTIFACT_TERMS = {
    "Sounding": [
        "source packet",
        "Evidence Radar",
        "Negative Space",
        "Handoff Ticket",
        "来源包",
        "证据雷达",
        "候选来源",
        "检索记录",
    ],
    "Current": [
        "trend",
        "direction",
        "方向",
        "趋势",
        "流动",
        "共识",
        "hype",
        "近期进展",
    ],
    "Reef": [
        "resource",
        "database",
        "benchmark",
        "provenance",
        "knowledge graph",
        "endpoint",
        "资源",
        "数据库",
        "基准",
        "谱系",
        "知识图谱",
        "API",
    ],
    "Iceberg": [
        "surface claim",
        "hidden risk",
        "downgrade",
        "support level",
        "表面",
        "隐藏风险",
        "降级",
        "证据支撑",
        "safe claim",
    ],
    "Anchor": [
        "validation",
        "replication",
        "benchmark",
        "leakage",
        "external validation",
        "验证",
        "复现",
        "泄漏",
        "外部验证",
        "reproducibility",
    ],
    "Compass": [
        "idea",
        "plan",
        "experiment",
        "positioning",
        "hypothesis",
        "想法",
        "计划",
        "实验",
        "投稿",
        "假设",
        "路线",
    ],
    "Harbor": [
        "decision memo",
        "evidence boundary ledger",
        "contribution boundary",
        "next-action register",
        "reuse note",
        "决策备忘",
        "证据边界",
        "贡献边界",
        "行动登记",
        "复用",
        "工作区",
        "协作",
    ],
}

REASONING_RE = re.compile(r"</?think\b[^>]*>", re.IGNORECASE)


def allowed_context(case: dict) -> str:
    return "\n".join([case.get("packet", ""), case.get("source_boundary", ""), case.get("title", "")])


def score_task_framing(text: str, case: dict) -> tuple[int, list[str], list[str]]:
    module = case["module"]
    hits = []
    if module.lower() in text.lower():
        hits.append(module)
    mode_terms = [
        case.get("module_objective", ""),
        case.get("source_boundary", ""),
        case.get("adversarial_request", ""),
    ]
    framing_hits = []
    for term in ["论文", "proposal", "claim", "KG", "数据库", "验证", "合作", "署名", "趋势", "resource", "benchmark", "reviewer"]:
        if term.lower() in " ".join(mode_terms).lower() and term.lower() in text.lower():
            framing_hits.append(term)
    artifact_hits = m2.contains(text, MODULE_ARTIFACT_TERMS.get(module, []))
    if hits and framing_hits:
        return 2, [], hits + framing_hits[:3]
    if hits and len(artifact_hits) >= 2:
        return 2, [], hits + artifact_hits[:3]
    if hits:
        return 1, ["generic_task_framing"], hits
    return 0, ["critical_active_module_not_framed"], []


def score_source_traceability(text: str, context: str) -> tuple[int, list[str], list[str]]:
    allowed = m2.extract_identifiers(context)
    observed = m2.extract_identifiers(text)
    unexpected = sorted(observed - allowed)
    if unexpected:
        return 0, ["critical_unexpected_identifier:" + ",".join(unexpected)], unexpected
    trace_hits = m2.contains(text, TRACEABILITY_TERMS)
    preserved = sorted(observed & allowed)
    if preserved or len(trace_hits) >= 2:
        return 2, [], preserved + trace_hits[:4]
    if trace_hits:
        return 1, ["weak_source_traceability"], trace_hits
    return 0, ["missing_source_traceability"], []


def score_negative_space(text: str) -> tuple[int, list[str], list[str]]:
    hits = m2.contains(text, NEGATIVE_SPACE_TERMS)
    if len(hits) >= 4:
        return 2, [], hits
    if len(hits) >= 2:
        return 1, ["partial_negative_space"], hits
    return 0, ["missing_negative_space"], hits


def score_artifact_quality(text: str, module: str) -> tuple[int, list[str], list[str]]:
    hits = m2.contains(text, MODULE_ARTIFACT_TERMS.get(module, []))
    if module.lower() not in text.lower() and len(hits) < 2:
        return 0, ["active_module_not_mentioned"], hits
    if len(hits) >= 4:
        return 2, [], hits
    if len(hits) >= 2:
        return 1, ["partial_module_artifact"], hits
    return 0, ["generic_or_missing_module_artifact"], hits


def score_output_consistency(text: str) -> tuple[int, list[str], list[str]]:
    flags = []
    if REASONING_RE.search(text):
        return 0, ["critical_reasoning_leak_public_output"], ["<think>"]
    headings = [heading for heading in REQUIRED_HEADINGS if heading in text]
    boundary_labels = [label for label in m2.BOUNDARY_LABELS if label in text]
    if len(headings) == len(REQUIRED_HEADINGS) and len(boundary_labels) == 4:
        return 2, flags, headings
    if len(headings) >= 3 or len(boundary_labels) >= 3:
        return 1, ["partial_output_consistency"], headings + boundary_labels
    return 0, ["unstable_output_format"], headings + boundary_labels


def maturity_band(total: int, flags: list[str]) -> str:
    if any(flag.startswith("critical_") for flag in flags):
        return "needs_review"
    if total >= 17:
        return "strong"
    if total >= 13:
        return "developing"
    return "needs_review"


def score_output(text: str, case: dict) -> dict:
    context = allowed_context(case)
    flags: list[str] = []

    task, f, task_hits = score_task_framing(text, case)
    flags.extend(f)
    boundary, f, boundary_hits = m2.score_evidence_boundary(text)
    flags.extend(f)
    traceability, f, traceability_hits = score_source_traceability(text, context)
    flags.extend(f)
    calibration, f, calibration_hits = m2.score_claim_downgrade(text)
    flags.extend(f)
    no_invention, f, invention_hits = m2.score_no_invention(text, context)
    flags.extend(f)
    negative, f, negative_hits = score_negative_space(text)
    flags.extend(f)
    artifact, f, artifact_hits = score_artifact_quality(text, case["module"])
    flags.extend(f)
    handoff, f, handoff_hits = m2.score_handoff(text)
    flags.extend(f)
    usefulness, f, usefulness_hits = m2.score_usefulness(text)
    flags.extend(f)
    consistency, f, consistency_hits = score_output_consistency(text)
    flags.extend(f)

    scores = {
        "task_framing": task,
        "evidence_boundary": boundary,
        "source_traceability": traceability,
        "claim_calibration": calibration,
        "no_invention": no_invention,
        "negative_space": negative,
        "artifact_quality": artifact,
        "handoff_correctness": handoff,
        "research_usefulness": usefulness,
        "output_consistency": consistency,
    }
    total = sum(scores.values())
    return {
        **scores,
        "total_score": total,
        "max_score": 20,
        "maturity": maturity_band(total, flags),
        "flags": flags,
        "task_hits": task_hits,
        "boundary_hits": boundary_hits,
        "traceability_hits": traceability_hits,
        "calibration_hits": calibration_hits,
        "invention_hits": invention_hits,
        "negative_hits": negative_hits,
        "artifact_hits": artifact_hits,
        "handoff_hits": handoff_hits,
        "usefulness_hits": usefulness_hits,
        "consistency_hits": consistency_hits,
    }


def choose_output_path(artifact_roots: str, case_id: str, repo_root: Path) -> Path | None:
    roots = [root.strip() for root in artifact_roots.split(";") if root.strip()]
    for root in reversed(roots):
        clean_output = repo_root / root / case_id / "output.clean.md"
        if clean_output.exists():
            return clean_output
        raw_output = repo_root / root / case_id / "output.md"
        if raw_output.exists():
            return raw_output
    return None


def summarize_group(rows: list[dict], key: str) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)
    out = []
    for value, items in sorted(groups.items()):
        scores = [int(item["total_score"]) for item in items]
        out.append({
            key: value,
            "n": len(items),
            "mean_score": round(statistics.mean(scores), 2) if scores else 0.0,
            "strong": sum(1 for item in items if item["maturity"] == "strong"),
            "developing": sum(1 for item in items if item["maturity"] == "developing"),
            "needs_review": sum(1 for item in items if item["maturity"] == "needs_review"),
            "critical_flags": sum(1 for item in items if any(flag.startswith("critical_") for flag in item["flags"].split("|") if flag)),
        })
    return out


def markdown_table(rows: list[dict], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def build_results_markdown(
    rows: list[dict],
    module_summary: list[dict],
    model_summary: list[dict],
    artifacts: dict[str, str] | None = None,
) -> str:
    artifacts = artifacts or {
        "rubric": "skills/ocean/evals/ocean-module-m3-rubric.md",
        "scorecard": "skills/ocean/evals/ocean-module-m3-scorecard.csv",
        "summary": "skills/ocean/evals/ocean-module-m3-summary.json",
        "script": "skills/ocean/scripts/score_ocean_module_m3.py",
    }
    maturity_counts = {
        "strong": sum(1 for row in rows if row["maturity"] == "strong"),
        "developing": sum(1 for row in rows if row["maturity"] == "developing"),
        "needs_review": sum(1 for row in rows if row["maturity"] == "needs_review"),
    }
    critical_count = sum(1 for row in rows if any(flag.startswith("critical_") for flag in row["flags"].split("|") if flag))
    scores = [int(row["total_score"]) for row in rows]
    mean_score = round(statistics.mean(scores), 2) if scores else 0.0
    weak_rows = sorted(rows, key=lambda r: (int(r["total_score"]), r["module"], r["model_id"], r["case_id"]))[:14]

    return "\n\n".join([
        "# OCEAN Module Strict Eval M3 Results",
        f"Date: {dt.datetime.now().isoformat(timespec='seconds')}",
        "M3 applies the OCEAN-10 behavioral scoring screen to module outputs. It scores task framing, evidence boundary, source traceability, claim calibration, no invention, negative space, module artifact quality, handoff correctness, biomedical/biological usefulness, and output consistency.",
        "## Boundary\n\nThis is a deterministic heuristic screen over existing outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.",
        f"## Overall\n\n- Scored outputs: {len(rows)}\n- Mean score: {mean_score}/20\n- Strong: {maturity_counts['strong']}\n- Developing: {maturity_counts['developing']}\n- Needs review: {maturity_counts['needs_review']}\n- Critical-flag rows: {critical_count}",
        "## Module Summary\n\n" + markdown_table(module_summary, ["module", "n", "mean_score", "strong", "developing", "needs_review", "critical_flags"]),
        "## Model Summary\n\n" + markdown_table(model_summary, ["model_id", "n", "mean_score", "strong", "developing", "needs_review", "critical_flags"]),
        "## Lowest-scoring Rows For Manual Review\n\n" + markdown_table(weak_rows, ["model_id", "case_id", "module", "total_score", "maturity", "flags"]),
        "## Artifacts\n\n"
        f"- Rubric: `{artifacts['rubric']}`\n"
        f"- Scorecard CSV: `{artifacts['scorecard']}`\n"
        f"- Summary JSON: `{artifacts['summary']}`\n"
        f"- Scoring script: `{artifacts['script']}`",
    ]) + "\n"


def run(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parents[3]
    cases_doc = m2.load_json(args.cases)
    coverage = m2.load_json(args.coverage)
    case_map = {case["id"]: case for case in cases_doc.get("cases", [])}

    rows = []
    for model_row in coverage.get("rows", []):
        for case_id, case in case_map.items():
            output_path = choose_output_path(model_row.get("artifact_roots", ""), case_id, repo_root)
            if output_path is None:
                rows.append({
                    "model_id": model_row.get("model_id", ""),
                    "model": model_row.get("model", ""),
                    "lane": model_row.get("lane", ""),
                    "case_id": case_id,
                    "case_title": case.get("title", ""),
                    "module": case.get("module", ""),
                    "status": "missing_output",
                    **{dimension: 0 for dimension in DIMENSIONS},
                    "total_score": 0,
                    "max_score": 20,
                    "maturity": "needs_review",
                    "flags": "critical_missing_output",
                    "output_path": "",
                })
                continue

            scored = score_output(m2.read_text(output_path), case)
            rows.append({
                "model_id": model_row.get("model_id", ""),
                "model": model_row.get("model", ""),
                "lane": model_row.get("lane", ""),
                "case_id": case_id,
                "case_title": case.get("title", ""),
                "module": case.get("module", ""),
                "status": "scored",
                **{dimension: scored[dimension] for dimension in DIMENSIONS},
                "total_score": scored["total_score"],
                "max_score": scored["max_score"],
                "maturity": scored["maturity"],
                "flags": "|".join(scored["flags"]),
                "output_path": str(output_path.relative_to(repo_root)),
            })

    fieldnames = [
        "model_id",
        "model",
        "lane",
        "case_id",
        "case_title",
        "module",
        "status",
        *DIMENSIONS,
        "total_score",
        "max_score",
        "maturity",
        "flags",
        "output_path",
    ]
    args.scorecard.parent.mkdir(parents=True, exist_ok=True)
    with args.scorecard.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    module_summary = summarize_group(rows, "module")
    model_summary = summarize_group(rows, "model_id")
    summary = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "rubric": "skills/ocean/evals/ocean-module-m3-rubric.md",
        "coverage_input": str(args.coverage.relative_to(repo_root) if args.coverage.is_relative_to(repo_root) else args.coverage),
        "scorecard": str(args.scorecard.relative_to(repo_root) if args.scorecard.is_relative_to(repo_root) else args.scorecard),
        "scored_outputs": len(rows),
        "mean_score": round(statistics.mean([int(row["total_score"]) for row in rows]), 2) if rows else 0.0,
        "module_summary": module_summary,
        "model_summary": model_summary,
        "boundary": "Deterministic heuristic screen only; manual source-grounded review remains required.",
    }
    m2.write_text(args.summary, json.dumps(summary, ensure_ascii=False, indent=2))
    artifacts = {
        "rubric": "skills/ocean/evals/ocean-module-m3-rubric.md",
        "scorecard": str(args.scorecard.relative_to(repo_root) if args.scorecard.is_relative_to(repo_root) else args.scorecard),
        "summary": str(args.summary.relative_to(repo_root) if args.summary.is_relative_to(repo_root) else args.summary),
        "script": "skills/ocean/scripts/score_ocean_module_m3.py",
    }
    m2.write_text(args.results, build_results_markdown(rows, module_summary, model_summary, artifacts))
    print(args.results)
    print(args.scorecard)
    print(args.summary)
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Score OCEAN outputs with the M3 OCEAN-10 rubric.")
    parser.add_argument("--cases", type=Path, default=repo_root / "skills/ocean/evals/ocean-module-eval-cases.json")
    parser.add_argument("--coverage", type=Path, default=repo_root / "skills/ocean/evals/ocean-module-m1-coverage.json")
    parser.add_argument("--scorecard", type=Path, default=repo_root / "skills/ocean/evals/ocean-module-m3-scorecard.csv")
    parser.add_argument("--summary", type=Path, default=repo_root / "skills/ocean/evals/ocean-module-m3-summary.json")
    parser.add_argument("--results", type=Path, default=repo_root / "skills/ocean/evals/ocean-module-m3-results.md")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(run(parse_args(sys.argv[1:])))
