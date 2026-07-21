#!/usr/bin/env python3
"""Deterministic structural regression check for OCEAN manuscript lifecycle routing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REVISION_TERMS = ("修改", "润色", "改写", "精简", "翻译", "措辞", "替换")
STRESS_TERMS = ("投稿前", "模拟审稿", "压力测试", "完整压力测试", "全模块审计")
DESIGN_TERMS = ("实验还没开始", "研究想法", "帮助设计", "早期草稿", "全面批判", "主要问题")
RESPONSE_TERMS = ("审稿意见", "逐条回复", "回复审稿", "response letter")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def classify_case(case: dict) -> str:
    request = case["user_request"].lower()
    shape = case["input_shape"]
    if any(term.lower() in request for term in RESPONSE_TERMS):
        return "Reviewer Response"
    if any(term.lower() in request for term in STRESS_TERMS):
        return "Pre-submission Stress Test"
    if any(term.lower() in request for term in DESIGN_TERMS) or shape in {"research_idea", "early_draft"}:
        return "Design / Audit"
    if shape == "finished_manuscript_text" and any(term.lower() in request for term in REVISION_TERMS):
        return "Manuscript Revision"
    return "Unclassified"


def contract_checks(skill_dir: Path) -> list[dict]:
    targets = {
        "revision_reference": (
            skill_dir / "references" / "manuscript-revision-mode.md",
            ["Manuscript Revision", "修订正文（可直接替换）", "修改说明（不进入正文）", "作者确认项（仅必要时）", "Channel Isolation"],
        ),
        "skill_entrypoint": (
            skill_dir / "SKILL.md",
            ["manuscript-revision-mode.md", "drafted passage", "clean replacement text"],
        ),
        "output_contract": (
            skill_dir / "references" / "output-contract.md",
            ["Manuscript Revision Mode", "修订正文（可直接替换）", "ordinary finished-text revision"],
        ),
        "routing_protocol": (
            skill_dir / "static" / "core" / "routing-protocol.md",
            ["Manuscript lifecycle gate", "silent bounded Iceberg check", "must not trigger the standard seven-module chain"],
        ),
        "iceberg_isolation": (
            skill_dir / "references" / "iceberg.md",
            ["keep the claim audit internal", "paste-ready paragraph"],
        ),
        "manifest_always_load": (
            skill_dir / "manifest.yaml",
            ["references/manuscript-revision-mode.md"],
        ),
    }
    rows = []
    for name, (path, terms) in targets.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [term for term in terms if term not in text]
        rows.append({
            "check": "contract",
            "target": name,
            "status": "pass" if exists and not missing else "fail",
            "detail": "all required terms present" if not missing else f"missing={missing}",
        })
    return rows


def case_checks(cases_path: Path) -> list[dict]:
    payload = json.loads(read_text(cases_path))
    forbidden = payload.get("forbidden_in_clean_revision", [])
    rows = []
    seen = set()
    for case in payload.get("cases", []):
        predicted = classify_case(case)
        unique = case["id"] not in seen
        seen.add(case["id"])
        required_channels = case.get("required_channels", [])
        clean_case = case["expected_mode"] == "Manuscript Revision"
        channel_ok = bool(required_channels) and (
            not clean_case or "修订正文（可直接替换）" in required_channels
        )
        visibility_ok = case.get("visible_audit_allowed") is (not clean_case)
        status = "pass" if predicted == case["expected_mode"] and unique and channel_ok and visibility_ok else "fail"
        rows.append({
            "check": "lifecycle_case",
            "target": case["id"],
            "status": status,
            "detail": f"expected={case['expected_mode']}; predicted={predicted}; channels={required_channels}",
        })
    rows.append({
        "check": "forbidden_clean_tokens",
        "target": "forbidden_token_registry",
        "status": "pass" if len(forbidden) >= 10 else "fail",
        "detail": f"registered={len(forbidden)}",
    })
    return rows


def write_markdown(rows: list[dict], out: Path) -> None:
    passed = sum(row["status"] == "pass" for row in rows)
    failed = sum(row["status"] == "fail" for row in rows)
    lines = [
        "# Manuscript Revision Mode R1 Results",
        "",
        "This is a deterministic structural and lifecycle-routing regression check. It does not evaluate scientific correctness or reproduce private manuscript text.",
        "",
        f"- Checks: {len(rows)}",
        f"- Pass: {passed}",
        f"- Fail: {failed}",
        "",
        "| Check | Target | Status | Detail |",
        "|---|---|---|---|",
    ]
    for row in rows:
        detail = str(row["detail"]).replace("|", "\\|")
        lines.append(f"| {row['check']} | {row['target']} | {row['status']} | {detail} |")
    lines.extend([
        "",
        "## Evidence Boundary",
        "",
        "Passing means the public skill files contain the lifecycle gate and the public-safe case router selects the expected mode. It does not prove that every model will obey the contract, that any manuscript claim is correct, or that private manuscript material was inspected in this regression run.",
    ])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description="Check OCEAN manuscript lifecycle routing contracts.")
    parser.add_argument("--skill-dir", type=Path, default=repo_root / "skills" / "ocean")
    parser.add_argument(
        "--cases",
        type=Path,
        default=repo_root / "validation" / "manuscript-revision-mode-r1-cases.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=repo_root / "validation" / "manuscript-revision-mode-r1-results.md",
    )
    args = parser.parse_args()

    rows = contract_checks(args.skill_dir) + case_checks(args.cases)
    write_markdown(rows, args.out)
    failed = [row for row in rows if row["status"] == "fail"]
    print(json.dumps({
        "total": len(rows),
        "pass": len(rows) - len(failed),
        "fail": len(failed),
        "out": str(args.out),
    }, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
