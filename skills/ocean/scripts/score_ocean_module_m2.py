#!/usr/bin/env python3
"""Score OCEAN M1 module outputs with the M2 rubric.

This script is intentionally conservative. It is a deterministic screening
layer for evidence-boundary and artifact-quality issues, not a scientific judge.
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


DIMENSIONS = [
    "evidence_boundary",
    "claim_downgrade",
    "no_invention",
    "artifact_quality",
    "handoff_correctness",
    "research_usefulness",
]

VALID_MODULES = ["Sounding", "Current", "Reef", "Iceberg", "Anchor", "Compass", "Harbor"]

BOUNDARY_LABELS = ["已检查", "未检查", "不能判断", "下一步需要"]

DOWNGRADE_TERMS = [
    "不支持",
    "不能证明",
    "无法证明",
    "不能直接",
    "不能得出",
    "不应",
    "不应该",
    "需要验证",
    "需要补充",
    "降级",
    "假设",
    "候选",
    "不能保证",
    "不足以",
]

UNSAFE_ACCEPT_TERMS = [
    "可以证明",
    "已经证明",
    "证明了",
    "无需验证",
    "不需要验证",
    "临床可用",
    "可直接用于",
    "直接指导",
    "保证",
    "确定可以",
]

NEGATION_TERMS = [
    "不",
    "不能",
    "无法",
    "未",
    "没有",
    "不可",
    "不足以",
    "不应",
    "不应该",
    "不构成",
    "不等于",
    "不自动",
    "拒绝",
    "严禁",
    "不得",
    "不承诺",
    "不背书",
    "不可支持",
    "不可主张",
    "被拒绝",
    "不接受",
]

DETAIL_RISK_TERMS = [
    "AUROC",
    "AUPRC",
    "accuracy",
    "sensitivity",
    "specificity",
    "sample size",
    "cohort size",
    "样本量",
    "队列大小",
    "准确率",
    "灵敏度",
    "特异性",
    "外部验证结果",
]

MODULE_KEYWORDS = {
    "Sounding": ["source packet", "Evidence Radar", "Negative Space", "Handoff Ticket", "来源包", "证据雷达", "负空间", "交接"],
    "Current": ["trend", "direction", "方向", "趋势", "流动", "field-wide", "领域"],
    "Reef": ["resource", "database", "benchmark", "provenance", "knowledge graph", "资源", "数据库", "基准", "谱系", "知识图谱"],
    "Iceberg": ["surface claim", "hidden risk", "downgrade", "support level", "表面", "隐藏风险", "降级", "证据支撑"],
    "Anchor": ["validation", "replication", "benchmark", "leakage", "external validation", "验证", "复现", "泄漏", "外部验证"],
    "Compass": ["idea", "plan", "experiment", "positioning", "hypothesis", "想法", "计划", "实验", "投稿", "假设"],
    "Harbor": ["report", "workspace", "memory", "collaboration", "authorship", "报告", "工作区", "记忆", "协作", "署名"],
}

USEFULNESS_TERMS = [
    "验证",
    "复现",
    "外部验证",
    "数据",
    "实验",
    "临床",
    "生物",
    "benchmark",
    "机制",
    "证据缺口",
    "下一步",
    "研究",
    "风险",
]

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
ARXIV_RE = re.compile(r"\b\d{4}\.\d{4,5}(?:v\d+)?\b")
URL_RE = re.compile(r"https?://[^\s)\]）>,，。；、]+")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def normalize_identifier(value: str) -> str:
    return value.strip().rstrip(".,;:)），。；、]").lower()


def extract_identifiers(text: str) -> set[str]:
    values = set()
    for regex in (DOI_RE, ARXIV_RE, URL_RE):
        values.update(normalize_identifier(match.group(0)) for match in regex.finditer(text))
    return values


def contains(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term.lower() in lowered]


def unnegated_phrase_hits(text: str, terms: list[str], window: int = 60) -> list[str]:
    hits = []
    lowered = text.lower()
    for term in terms:
        term_lower = term.lower()
        start = 0
        while True:
            idx = lowered.find(term_lower, start)
            if idx == -1:
                break
            context = text[max(0, idx - window):idx + len(term) + window]
            if not any(neg in context for neg in NEGATION_TERMS):
                hits.append(term)
                break
            start = idx + len(term_lower)
    return hits


def asserted_detail_hits(text: str) -> list[str]:
    hits = []
    lowered = text.lower()
    for term in DETAIL_RISK_TERMS:
        term_lower = term.lower()
        start = 0
        while True:
            idx = lowered.find(term_lower, start)
            if idx == -1:
                break
            context = text[max(0, idx - 18):idx + len(term) + 18]
            if not any(marker in context for marker in ["未提供", "未检查", "不能判断", "无法判断", "not provided", "not inspected"]):
                hits.append(term)
                break
            start = idx + len(term_lower)
    return hits


def score_evidence_boundary(text: str) -> tuple[int, list[str], list[str]]:
    present = [label for label in BOUNDARY_LABELS if label in text]
    flags = []
    if len(present) == 4:
        return 2, flags, present
    missing = [label for label in BOUNDARY_LABELS if label not in text]
    flags.append("missing_boundary_labels:" + ",".join(missing))
    if len(present) >= 2:
        return 1, flags, present
    return 0, ["critical_missing_evidence_boundary"], present


def score_claim_downgrade(text: str) -> tuple[int, list[str], list[str]]:
    unsafe_hits = unnegated_phrase_hits(text, UNSAFE_ACCEPT_TERMS)
    downgrade_hits = contains(text, DOWNGRADE_TERMS)
    flags = []
    if unsafe_hits and len(downgrade_hits) < 2:
        flags.append("critical_unsupported_claim_may_be_accepted:" + ",".join(unsafe_hits))
        return 0, flags, downgrade_hits
    if len(downgrade_hits) >= 2:
        return 2, flags, downgrade_hits
    if downgrade_hits:
        return 1, flags, downgrade_hits
    return 0, ["no_clear_unsupported_claim_downgrade"], downgrade_hits


def score_no_invention(text: str, allowed_context: str) -> tuple[int, list[str], list[str]]:
    allowed = extract_identifiers(allowed_context)
    observed = extract_identifiers(text)
    unexpected = sorted(observed - allowed)
    detail_risks = asserted_detail_hits(text)
    flags = []
    if unexpected:
        flags.append("critical_unexpected_identifier:" + ",".join(unexpected))
        return 0, flags, unexpected
    if detail_risks:
        flags.append("detail_risk_requires_manual_review:" + ",".join(detail_risks))
        return 1, flags, detail_risks
    return 2, flags, []


def score_artifact_quality(text: str, module: str) -> tuple[int, list[str], list[str]]:
    if module.lower() not in text.lower():
        return 0, ["active_module_not_mentioned"], []
    hits = contains(text, MODULE_KEYWORDS.get(module, []))
    if len(hits) >= 3:
        return 2, [], hits
    if hits:
        return 1, ["partial_module_artifact"], hits
    return 0, ["generic_or_missing_module_artifact"], hits


def score_handoff(text: str) -> tuple[int, list[str], list[str]]:
    valid_hits = contains(text, VALID_MODULES)
    stop_hits = contains(text, ["stop", "停止", "不交接", "无需交接", "stop condition"])
    invalid_hits = contains(text, ["Scrutiny", "Synthesis", "Navigator module", "Retriever"])
    flags = []
    if invalid_hits:
        flags.append("wrong_handoff_vocabulary:" + ",".join(invalid_hits))
        return 0, flags, valid_hits
    if valid_hits or stop_hits:
        return 2, flags, valid_hits + stop_hits
    if contains(text, ["下一步", "交接", "handoff"]):
        return 1, ["generic_handoff_without_ocean_module"], []
    return 0, ["missing_handoff_or_stop"], []


def score_usefulness(text: str) -> tuple[int, list[str], list[str]]:
    hits = contains(text, USEFULNESS_TERMS)
    if len(hits) >= 4:
        return 2, [], hits
    if len(hits) >= 2:
        return 1, ["limited_research_usefulness"], hits
    return 0, ["low_research_usefulness"], hits


def maturity_band(total: int, flags: list[str]) -> str:
    if any(flag.startswith("critical_") for flag in flags):
        return "needs_review"
    if total >= 10:
        return "strong"
    if total >= 8:
        return "developing"
    return "needs_review"


def score_output(text: str, case: dict) -> dict:
    flags: list[str] = []
    evidence, f, evidence_hits = score_evidence_boundary(text)
    flags.extend(f)
    downgrade, f, downgrade_hits = score_claim_downgrade(text)
    flags.extend(f)
    no_invention, f, invention_hits = score_no_invention(
        text,
        "\n".join([case.get("packet", ""), case.get("source_boundary", ""), case.get("title", "")]),
    )
    flags.extend(f)
    artifact, f, artifact_hits = score_artifact_quality(text, case["module"])
    flags.extend(f)
    handoff, f, handoff_hits = score_handoff(text)
    flags.extend(f)
    usefulness, f, usefulness_hits = score_usefulness(text)
    flags.extend(f)

    scores = {
        "evidence_boundary": evidence,
        "claim_downgrade": downgrade,
        "no_invention": no_invention,
        "artifact_quality": artifact,
        "handoff_correctness": handoff,
        "research_usefulness": usefulness,
    }
    total = sum(scores.values())
    return {
        **scores,
        "total_score": total,
        "max_score": 12,
        "maturity": maturity_band(total, flags),
        "flags": flags,
        "evidence_hits": evidence_hits,
        "downgrade_hits": downgrade_hits,
        "invention_hits": invention_hits,
        "artifact_hits": artifact_hits,
        "handoff_hits": handoff_hits,
        "usefulness_hits": usefulness_hits,
    }


def choose_output_path(artifact_roots: str, case_id: str, repo_root: Path) -> Path | None:
    roots = [root.strip() for root in artifact_roots.split(";") if root.strip()]
    for root in reversed(roots):
        output = repo_root / root / case_id / "output.md"
        if output.exists():
            return output
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


def build_results_markdown(rows: list[dict], module_summary: list[dict], model_summary: list[dict]) -> str:
    maturity_counts = {
        "strong": sum(1 for row in rows if row["maturity"] == "strong"),
        "developing": sum(1 for row in rows if row["maturity"] == "developing"),
        "needs_review": sum(1 for row in rows if row["maturity"] == "needs_review"),
    }
    critical_count = sum(1 for row in rows if any(flag.startswith("critical_") for flag in row["flags"].split("|") if flag))
    mean_score = round(statistics.mean([int(row["total_score"]) for row in rows]), 2) if rows else 0.0
    weak_rows = sorted(rows, key=lambda r: (int(r["total_score"]), r["module"], r["model_id"], r["case_id"]))[:12]

    return "\n\n".join([
        "# OCEAN Module Strict Eval M2 Results",
        f"Date: {dt.datetime.now().isoformat(timespec='seconds')}",
        "M2 applies the first content-quality scoring screen to the M1 all-module outputs. It scores evidence boundary correctness, unsupported-claim downgrade, absence of invented source details, module-specific artifact quality, handoff correctness, and biomedical/biological research usefulness.",
        "## Boundary\n\nThis is a deterministic heuristic screen over existing M1 outputs. It is not a final scientific correctness judgment, not a model leaderboard, and not a substitute for manual review against the source materials.",
        f"## Overall\n\n- Scored outputs: {len(rows)}\n- Mean score: {mean_score}/12\n- Strong: {maturity_counts['strong']}\n- Developing: {maturity_counts['developing']}\n- Needs review: {maturity_counts['needs_review']}\n- Critical-flag rows: {critical_count}",
        "## Module Summary\n\n" + markdown_table(module_summary, ["module", "n", "mean_score", "strong", "developing", "needs_review", "critical_flags"]),
        "## Model Summary\n\n" + markdown_table(model_summary, ["model_id", "n", "mean_score", "strong", "developing", "needs_review", "critical_flags"]),
        "## Lowest-scoring Rows For Manual Review\n\n" + markdown_table(weak_rows, ["model_id", "case_id", "module", "total_score", "maturity", "flags"]),
        "## Artifacts\n\n- Rubric: `validation/ocean-module-m2-rubric.md`\n- Scorecard CSV: `validation/ocean-module-m2-scorecard.csv`\n- Summary JSON: `validation/ocean-module-m2-summary.json`\n- Scoring script: `skills/ocean/scripts/score_ocean_module_m2.py`",
    ]) + "\n"


def run(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parents[3]
    cases_doc = load_json(args.cases)
    coverage = load_json(args.coverage)
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
                    "module": case.get("module", ""),
                    "status": "missing_output",
                    **{dimension: 0 for dimension in DIMENSIONS},
                    "total_score": 0,
                    "max_score": 12,
                    "maturity": "needs_review",
                    "flags": "critical_missing_output",
                    "output_path": "",
                })
                continue

            scored = score_output(read_text(output_path), case)
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
        "rubric": "validation/ocean-module-m2-rubric.md",
        "coverage_input": str(args.coverage.relative_to(repo_root) if args.coverage.is_relative_to(repo_root) else args.coverage),
        "scorecard": str(args.scorecard.relative_to(repo_root) if args.scorecard.is_relative_to(repo_root) else args.scorecard),
        "scored_outputs": len(rows),
        "mean_score": round(statistics.mean([int(row["total_score"]) for row in rows]), 2) if rows else 0.0,
        "module_summary": module_summary,
        "model_summary": model_summary,
        "boundary": "Deterministic heuristic screen only; manual source-grounded review remains required.",
    }
    write_text(args.summary, json.dumps(summary, ensure_ascii=False, indent=2))
    write_text(args.results, build_results_markdown(rows, module_summary, model_summary))
    print(args.results)
    print(args.scorecard)
    print(args.summary)
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Score OCEAN M1 outputs with the M2 rubric.")
    parser.add_argument("--cases", type=Path, default=repo_root / "validation/ocean-module-eval-cases.json")
    parser.add_argument("--coverage", type=Path, default=repo_root / "validation/ocean-module-m1-coverage.json")
    parser.add_argument("--scorecard", type=Path, default=repo_root / "validation/ocean-module-m2-scorecard.csv")
    parser.add_argument("--summary", type=Path, default=repo_root / "validation/ocean-module-m2-summary.json")
    parser.add_argument("--results", type=Path, default=repo_root / "validation/ocean-module-m2-results.md")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(run(parse_args(sys.argv[1:])))
