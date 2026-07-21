#!/usr/bin/env python3
"""Validate concise public-safe OCEAN project progress pages."""

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
    "ocean_phase",
    "project_stage",
    "public_status",
    "last_verified",
    "evidence_basis",
}
REQUIRED_HEADINGS = {"## Status", "## Progress", "## Next", "## Public Boundary"}
MAX_RECORD_LINES = 60
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


def parse_record(path: Path) -> tuple[dict, str, str]:
    text = path.read_text(encoding="utf-8")
    metadata_match = re.match(r"\A<!-- ocean-project\n(.*?)\n-->\n", text, flags=re.DOTALL)
    if not metadata_match:
        raise ValueError("missing hidden ocean-project metadata")
    data = yaml.safe_load(metadata_match.group(1))
    if not isinstance(data, dict):
        raise ValueError("project metadata must be a mapping")
    title_match = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
    if not title_match:
        raise ValueError("missing project title")
    return data, text, title_match.group(1).strip()


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
            data, text, title = parse_record(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{rel}: {exc}")
            continue

        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            errors.append(f"{rel}: missing metadata fields {sorted(missing)}")

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

        headings = set(re.findall(r"^## .+$", text, flags=re.MULTILINE))
        for heading in sorted(REQUIRED_HEADINGS - headings):
            errors.append(f"{rel}: missing heading {heading!r}")
        for heading in sorted(headings - REQUIRED_HEADINGS):
            errors.append(f"{rel}: unexpected project-page heading {heading!r}")
        if len(text.splitlines()) > MAX_RECORD_LINES:
            errors.append(f"{rel}: exceeds {MAX_RECORD_LINES} lines")

        progress = text.split("## Progress", 1)[-1].split("\n## ", 1)[0]
        progress_items = [line for line in progress.splitlines() if line.startswith("- ")]
        if not progress_items:
            errors.append(f"{rel}: Progress must contain at least one bullet")
        if len(progress_items) > 5:
            errors.append(f"{rel}: Progress must contain at most five bullets")

        updated_line = f"**Updated:** {raw_date}"
        if updated_line not in text:
            errors.append(f"{rel}: visible Updated date does not match metadata")

        index_link = f"({path.parent.name}/README.md)"
        index_row = next((line for line in index_text.splitlines() if index_link in line), "")
        if not index_row:
            errors.append(f"{rel}: missing from projects/README.md index")
        else:
            if title not in index_row:
                errors.append(f"{rel}: index title does not match page title")
            if str(raw_date) not in index_row:
                errors.append(f"{rel}: index date does not match metadata")

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

    print(f"Project records valid: {len(records)} concise pages, {len(seen_ids)} unique IDs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
