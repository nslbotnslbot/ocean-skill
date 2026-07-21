#!/usr/bin/env python3
"""Create an OCEAN project-start record and GitHub sync ticket."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re


DEFAULT_MODULE_ROUTE = [
    "Sounding",
    "Current",
    "Reef",
    "Iceberg",
    "Anchor",
    "Compass",
    "Harbor",
]


def slugify(value: str) -> str:
    lowered = value.lower()
    replaced = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return replaced or "untitled-project"


def split_csv(value: str) -> list[str]:
    parts = [part.strip() for part in value.split(",")]
    return [part for part in parts if part]


def markdown_list(value: str) -> str:
    items = split_csv(value)
    if not items:
        return "- To be updated"
    return "\n".join(f"- {item}" for item in items)


def module_route_table(modules: list[str]) -> str:
    rows = ["| Step | Module | Planned artifact | Stop condition |", "|---:|---|---|---|"]
    artifact_map = {
        "Sounding": "Source Packet",
        "Current": "Direction-Flow Map",
        "Reef": "Resource Provenance Map",
        "Iceberg": "Claim-Evidence Matrix",
        "Anchor": "Validation Plan",
        "Compass": "Research Route Card",
        "Harbor": "Decision Memory / GitHub Sync Ticket",
    }
    for idx, module in enumerate(modules, start=1):
        artifact = artifact_map.get(module, "Module-specific artifact")
        rows.append(
            f"| {idx} | {module} | {artifact} | Stop if evidence boundary cannot be stated. |"
        )
    return "\n".join(rows)


def next_project_id(outdir: Path) -> str:
    numbers: list[int] = []
    for path in outdir.glob("*/README.md"):
        match = re.search(r"^project_id:\s*OCEAN-PROJ-(\d{3})\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            numbers.append(int(match.group(1)))
    return f"OCEAN-PROJ-{max(numbers, default=0) + 1:03d}"


def build_project_card(args: argparse.Namespace, project_id: str, slug: str, modules: list[str]) -> str:
    title_yaml = json.dumps(args.title, ensure_ascii=False)
    domain_yaml = json.dumps(args.domain, ensure_ascii=False)
    evidence_basis_yaml = json.dumps(args.evidence_basis, ensure_ascii=False)
    return f"""---
project_id: {project_id}
title: {title_yaml}
domain: {domain_yaml}
ocean_phase: {args.ocean_phase}
project_stage: {args.project_stage}
public_status: {args.public_status}
last_verified: {args.start_date}
evidence_basis: {evidence_basis_yaml}
---

# {args.title}

## Public Snapshot

| Field | Verified public-safe value |
|---|---|
| Project ID | {project_id} |
| Project title | {args.title} |
| Start date | {args.start_date} |
| Project class | {args.project_class} |
| Domain lane | {args.domain} |
| Starting module | {modules[0] if modules else "To be updated"} |
| Expected module route | {" -> ".join(modules) if modules else "To be updated"} |
| OCEAN phase | {args.ocean_phase} |
| Project stage | {args.project_stage} |
| Public status | {args.public_status} |
| Public-safe? | {args.public_safe} |
| Record slug | {slug} |

## Project Summary

{args.summary or "To be updated."}

## Evidence Basis

### Inspected

{markdown_list(args.inspected)}

### Not inspected

{markdown_list(args.not_inspected)}

### Cannot conclude

{markdown_list(args.cannot_conclude)}

### Next evidence needed

{markdown_list(args.next_evidence_needed)}

### Excluded from public record

{markdown_list(args.excluded_material)}

## OCEAN Module Record

The following route is planned at project start. A module must not be marked complete until its artifact is inspected.

{module_route_table(modules)}

## Progress Log

| Date | Verified change | Evidence boundary | Next gate |
|---|---|---|---|
| {args.start_date} | Public-safe OCEAN project record created. | Project registration does not establish scientific validity or submission status. | {args.next_evidence_needed or "Confirm the first inspected artifact and project-owner-approved public milestone."} |

## Next Public Gate

{args.next_evidence_needed or "Confirm the first inspected artifact and project-owner-approved public milestone."}

## Confidentiality Boundary

{markdown_list(args.excluded_material)}

## Harbor Seed

- Current decision: {args.current_decision}
- Unresolved risks: {args.unresolved_risks}
- Next-action register: {args.next_actions}
- Reuse warning: Recheck evidence boundary, project status, and public-safe approval before reusing this record.
"""


def build_harbor_seed(args: argparse.Namespace, project_id: str, modules: list[str]) -> str:
    return f"""# Harbor Seed

## Decision Memo

- Project ID: {project_id}
- Current decision: {args.current_decision}
- OCEAN phase: {args.ocean_phase}
- Project stage: {args.project_stage}
- Public status: {args.public_status}
- What can be claimed now: The project has entered OCEAN tracking only if the evidence boundary above is preserved.
- What must remain hypothesis: Any scientific, clinical, mechanism, validation, authorship, or publication claim not directly supported by inspected evidence.

## Evidence Boundary Ledger

| Item | Status | Evidence basis | Reuse warning |
|---|---|---|---|
| Inspected material | checked | {args.inspected or "To be updated"} | Recheck before downstream claims. |
| Missing material | unchecked | {args.not_inspected or "To be updated"} | Do not infer missing results. |
| Cannot conclude | cannot judge | {args.cannot_conclude or "To be updated"} | Keep claims downgraded. |
| Next evidence | needed next | {args.next_evidence_needed or "To be updated"} | Required before stronger claims. |

## Module Route

{module_route_table(modules)}

## Next-Action Register

| Action | Why needed | Owner/role | Priority | Evidence required |
|---|---|---|---|---|
| {args.next_actions} | Preserve project traceability | Project owner / OCEAN user | Medium | Public-safe evidence boundary |

## Reuse Note

- This memo can be reused for: project orientation, OCEAN module routing, and public-safe update planning.
- Must be rechecked before reuse: source identities, project status, private/public boundary, and module outputs.
- Do not reuse as evidence for: scientific validity, clinical utility, validation success, authorship, submission, review outcome, acceptance, or publication.
"""


def build_sync_ticket(args: argparse.Namespace, project_id: str, slug: str, project_dir: Path) -> str:
    files = [
        project_dir / "README.md",
        project_dir / "harbor-seed.md",
        project_dir / "github-sync-ticket.md",
        project_dir / "project-state.json",
    ]
    file_list = "<br>".join(str(path) for path in files)
    push_state = "approved" if args.remote_push == "approved" else args.remote_push
    return f"""# GitHub Sync Ticket

| Field | Value |
|---|---|
| Project ID | {project_id} |
| Target repository | {args.target_repo} |
| Suggested branch | {args.branch or f"project/{slug}"} |
| Files to add/update | {file_list} |
| Commit message | {args.commit_message or f"Add OCEAN project start record for {slug}"} |
| Remote push | {push_state} |
| Public-safe summary | {args.summary or "To be updated."} |
| Excluded material | {args.excluded_material or "Private or unconfirmed project material must stay out of public GitHub records."} |

## Push Rule

Remote push is allowed only when this ticket says `approved` and the repository state does not mix unrelated changes. If approval is missing, keep these files local and ask for a GitHub update decision.
"""


def build_state(args: argparse.Namespace, project_id: str, slug: str, modules: list[str]) -> dict:
    return {
        "schema_version": "ocean-project-start-r1",
        "project_id": project_id,
        "slug": slug,
        "title": args.title,
        "start_date": args.start_date,
        "project_class": args.project_class,
        "domain": args.domain,
        "ocean_phase": args.ocean_phase,
        "project_stage": args.project_stage,
        "public_status": args.public_status,
        "public_safe": args.public_safe,
        "modules": modules,
        "remote_push": args.remote_push,
        "target_repo": args.target_repo,
        "evidence_boundary": {
            "inspected": split_csv(args.inspected),
            "not_inspected": split_csv(args.not_inspected),
            "cannot_conclude": split_csv(args.cannot_conclude),
            "next_evidence_needed": split_csv(args.next_evidence_needed),
            "excluded_material": split_csv(args.excluded_material),
        },
    }


def update_index(
    index_path: Path,
    project_id: str,
    title: str,
    slug: str,
    domain: str,
    ocean_phase: str,
    project_stage: str,
    verified_date: str,
) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    row = (
        f"| {project_id} | {title} | {domain} | {ocean_phase} | {project_stage} | "
        f"{verified_date} | [Project record]({slug}/README.md) |\n"
    )
    if not index_path.exists():
        index_path.write_text(
            "# OCEAN Project Progress Hub\n\n"
            "Public-safe project records created by the Harbor Project Start Gate.\n\n"
            "| Project ID | Project | Domain | OCEAN phase | Project stage | Last verified | Record |\n"
            "|---|---|---|---|---|---|---|\n"
            + row,
            encoding="utf-8",
        )
        return

    current = index_path.read_text(encoding="utf-8")
    if project_id in current or f"]({slug}/README.md)" in current:
        return
    marker = "\n## Two Independent Statuses"
    if marker in current:
        current = current.replace(marker, "\n" + row + marker, 1)
    else:
        current = current.rstrip() + "\n" + row
    index_path.write_text(current, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create OCEAN project-start record files.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--project-id", default="")
    parser.add_argument("--domain", default="To be classified")
    parser.add_argument("--project-class", default="New tracked project")
    parser.add_argument(
        "--ocean-phase",
        choices=["planning", "evidence-audit", "validation-planning", "manuscript-support", "pre-submission-audit", "reviewer-response", "archived"],
        default="planning",
    )
    parser.add_argument(
        "--project-stage",
        choices=["idea", "analysis", "manuscript-preparation", "repository-release-preparation", "submitted", "under-review", "revision", "accepted", "published", "paused", "to-be-confirmed"],
        default="idea",
    )
    parser.add_argument(
        "--public-status",
        choices=["active", "paused", "completed", "archived", "awaiting-owner-confirmation"],
        default="awaiting-owner-confirmation",
    )
    parser.add_argument("--evidence-basis", default="owner-confirmation-needed")
    parser.add_argument("--public-safe", choices=["yes", "no", "unclear"], default="unclear")
    parser.add_argument("--modules", default=",".join(DEFAULT_MODULE_ROUTE))
    parser.add_argument("--summary", default="")
    parser.add_argument("--inspected", default="")
    parser.add_argument("--not-inspected", default="")
    parser.add_argument("--cannot-conclude", default="")
    parser.add_argument("--next-evidence-needed", default="")
    parser.add_argument("--excluded-material", default="")
    parser.add_argument("--current-decision", default="Create initial OCEAN project record.")
    parser.add_argument("--unresolved-risks", default="Evidence boundary and public-safe scope require review.")
    parser.add_argument("--next-actions", default="Confirm inspected materials and first OCEAN module route.")
    parser.add_argument("--target-repo", default="nslbotnslbot/ocean-skill")
    parser.add_argument("--branch", default="")
    parser.add_argument("--commit-message", default="")
    parser.add_argument(
        "--remote-push",
        choices=["approved", "needs approval", "not allowed"],
        default="needs approval",
    )
    parser.add_argument("--start-date", default=date.today().isoformat())
    parser.add_argument("--outdir", type=Path, default=Path("outputs/project-records"))
    parser.add_argument("--no-index", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    canonical_public_dir = (repo_root / "projects").resolve()
    if args.outdir.resolve() == canonical_public_dir and args.public_safe != "yes":
        raise SystemExit(
            "Refusing to write an unconfirmed record into projects/: "
            "set --public-safe yes after owner approval, or use outputs/project-records/."
        )
    if args.remote_push == "approved" and args.public_safe != "yes":
        raise SystemExit("Remote push requires --public-safe yes.")
    slug = slugify(args.title)
    project_id = args.project_id or next_project_id(args.outdir)
    modules = split_csv(args.modules)
    project_dir = args.outdir / slug
    state = build_state(args, project_id, slug, modules)

    outputs = {
        "README.md": build_project_card(args, project_id, slug, modules),
        "harbor-seed.md": build_harbor_seed(args, project_id, modules),
        "github-sync-ticket.md": build_sync_ticket(args, project_id, slug, project_dir),
        "project-state.json": json.dumps(state, ensure_ascii=False, indent=2) + "\n",
    }

    if not args.dry_run:
        project_dir.mkdir(parents=True, exist_ok=True)
        for filename, text in outputs.items():
            (project_dir / filename).write_text(text, encoding="utf-8")
        if not args.no_index:
            update_index(
                args.outdir / "README.md",
                project_id,
                args.title,
                slug,
                args.domain,
                args.ocean_phase,
                args.project_stage,
                args.start_date,
            )

    print(json.dumps({
        "project_id": project_id,
        "slug": slug,
        "project_dir": str(project_dir),
        "files": sorted(outputs),
        "dry_run": args.dry_run,
        "remote_push": args.remote_push,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
