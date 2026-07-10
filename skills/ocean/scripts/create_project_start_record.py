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


def build_project_card(args: argparse.Namespace, project_id: str, slug: str, modules: list[str]) -> str:
    return f"""# OCEAN Project Start Card

| Field | Value |
|---|---|
| Project ID | {project_id} |
| Project title | {args.title} |
| Start date | {args.start_date} |
| Project class | {args.project_class} |
| Domain lane | {args.domain} |
| Starting module | {modules[0] if modules else "To be updated"} |
| Expected module route | {" -> ".join(modules) if modules else "To be updated"} |
| Status | {args.status} |
| Public-safe? | {args.public_safe} |
| Record slug | {slug} |

## Project Summary

{args.summary or "To be updated."}

## Evidence Boundary Snapshot

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

## Module Route

{module_route_table(modules)}

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
- Current status: {args.status}
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
        project_dir / "project-card.md",
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
        "status": args.status,
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


def update_index(index_path: Path, project_id: str, title: str, slug: str, status: str) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    row = f"| {project_id} | [{title}]({slug}/project-card.md) | {status} | To be updated | |\n"
    if not index_path.exists():
        index_path.write_text(
            "# OCEAN Project Records\n\n"
            "Public-safe or local project-start records created by the Harbor Project Start Gate.\n\n"
            "| Project ID | Project | Status | Last update | Notes |\n"
            "|---|---|---|---|---|\n"
            + row,
            encoding="utf-8",
        )
        return

    current = index_path.read_text(encoding="utf-8")
    if project_id in current or f"]({slug}/project-card.md)" in current:
        return
    index_path.write_text(current.rstrip() + "\n" + row, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create OCEAN project-start record files.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--project-id", default="")
    parser.add_argument("--domain", default="To be classified")
    parser.add_argument("--project-class", default="New tracked project")
    parser.add_argument("--status", default="OCEAN planning")
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
    parser.add_argument("--outdir", type=Path, default=Path("docs/project-records"))
    parser.add_argument("--no-index", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    slug = slugify(args.title)
    project_id = args.project_id or f"OCEAN-PROJ-{args.start_date.replace('-', '')}-{slug}"
    modules = split_csv(args.modules)
    project_dir = args.outdir / slug
    state = build_state(args, project_id, slug, modules)

    outputs = {
        "project-card.md": build_project_card(args, project_id, slug, modules),
        "harbor-seed.md": build_harbor_seed(args, project_id, modules),
        "github-sync-ticket.md": build_sync_ticket(args, project_id, slug, project_dir),
        "project-state.json": json.dumps(state, ensure_ascii=False, indent=2) + "\n",
    }

    if not args.dry_run:
        project_dir.mkdir(parents=True, exist_ok=True)
        for filename, text in outputs.items():
            (project_dir / filename).write_text(text, encoding="utf-8")
        if not args.no_index:
            update_index(args.outdir / "index.md", project_id, args.title, slug, args.status)

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
