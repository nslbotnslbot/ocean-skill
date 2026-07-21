#!/usr/bin/env python3
"""Validate public-safe OCEAN project progress records."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "projects"
INDEX = PROJECTS / "README.md"
REQUIRED_FIELDS = {
    "project_id",
    "title",
    "domain",
    "ocean_phase",
    "project_stage",
    "public_status",
    "last_verified",
    "evidence_basis",
}
REQUIRED_HEADINGS = {
    "## Public Snapshot",
    "## Evidence Basis",
    "## OCEAN Module Record",
    "## Progress Log",
    "## Next Public Gate",
    "## Confidentiality Boundary",
}
ALLOWED_OCEAN_PHASES = {
    "planning",
    "evidence-audit",
    "validation-planning",
    "manuscript-support",
    "pre-submission-audit",
    "reviewer-response",
    "archived",
}
ALLOWED_PROJECT_STAGES = {
    "idea",
    "analysis",
    "manuscript-preparation",
    "repository-release-preparation",
    "submitted",
    "under-review",
    "revision",
    "accepted",
    "published",
    "paused",
    "to-be-confirmed",
}
ALLOWED_PUBLIC_STATUSES = {
    "active",
    "paused",
    "completed",
    "archived",
    "awaiting-owner-confirmation",
}
FORBIDDEN_PUBLIC_TEXT = {
    "/Users/": "local absolute path",
    "codex://": "private Codex thread link",
    "sk-ant-": "API credential prefix",
    "sk-proj-": "API credential prefix",
}


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data, text


def main() -> int:
    errors: list[str] = []
    records = sorted(PROJECTS.glob("*/README.md"))
    index_text = INDEX.read_text(encoding="utf-8")
    seen_ids: set[str] = set()

    if not records:
        errors.append("no project records found")

    for path in records:
        rel = path.relative_to(ROOT)
        try:
            data, text = parse_frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            errors.append(f"{rel}: missing fields {sorted(missing)}")

        project_id = str(data.get("project_id", ""))
        if not re.fullmatch(r"OCEAN-PROJ-\d{3}", project_id):
            errors.append(f"{rel}: invalid project_id {project_id!r}")
        elif project_id in seen_ids:
            errors.append(f"{rel}: duplicate project_id {project_id}")
        seen_ids.add(project_id)

        if data.get("ocean_phase") not in ALLOWED_OCEAN_PHASES:
            errors.append(f"{rel}: invalid ocean_phase {data.get('ocean_phase')!r}")
        if data.get("project_stage") not in ALLOWED_PROJECT_STAGES:
            errors.append(f"{rel}: invalid project_stage {data.get('project_stage')!r}")
        if data.get("public_status") not in ALLOWED_PUBLIC_STATUSES:
            errors.append(f"{rel}: invalid public_status {data.get('public_status')!r}")

        raw_date = data.get("last_verified")
        try:
            verified = raw_date if isinstance(raw_date, dt.date) else dt.date.fromisoformat(str(raw_date))
            if verified > dt.date.today():
                errors.append(f"{rel}: last_verified is in the future")
        except ValueError:
            errors.append(f"{rel}: last_verified must be ISO YYYY-MM-DD")

        for heading in sorted(REQUIRED_HEADINGS):
            if heading not in text:
                errors.append(f"{rel}: missing heading {heading!r}")

        for needle, label in FORBIDDEN_PUBLIC_TEXT.items():
            if needle in text:
                errors.append(f"{rel}: contains {label}: {needle!r}")

        index_link = f"({path.parent.name}/README.md)"
        if index_link not in index_text:
            errors.append(f"{rel}: missing from projects/README.md index")
        index_row = next(
            (line for line in index_text.splitlines() if line.startswith(f"| {project_id} |")),
            "",
        )
        if not index_row:
            errors.append(f"{rel}: project ID missing from projects/README.md index")
        else:
            if str(data.get("title", "")) not in index_row:
                errors.append(f"{rel}: index title does not match frontmatter")
            if str(raw_date) not in index_row:
                errors.append(f"{rel}: index last-verified date does not match frontmatter")
        if str(raw_date) not in text.split("## Progress Log", 1)[-1]:
            errors.append(f"{rel}: last_verified date missing from Progress Log")

    for path in sorted(PROJECTS.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for needle, label in FORBIDDEN_PUBLIC_TEXT.items():
            if needle in text:
                errors.append(f"{rel}: contains {label}: {needle!r}")

    if errors:
        print("Project record validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Project records valid: {len(records)} records, {len(seen_ids)} unique IDs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
