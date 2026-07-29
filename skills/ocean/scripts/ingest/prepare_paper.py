#!/usr/bin/env python3
"""Create an OCEAN PaperBundle from a local PDF, Markdown, or text file."""

from __future__ import annotations

import argparse
import json
import mimetypes
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import (
    OCEAN_VERSION,
    evidence_boundary,
    now_utc,
    schema_path,
    sha256_file,
    sha256_json,
    stable_id,
    validate_required_contract,
    write_json,
)


HEADING_RE = re.compile(
    r"^(abstract|introduction|background|methods?|materials and methods|results?|"
    r"discussion|conclusions?|references|acknowledg(?:e)?ments?|supplementary.*)$",
    re.IGNORECASE,
)
FIGURE_RE = re.compile(r"^(?:figure|fig\.)\s*([A-Za-z0-9.-]+)", re.IGNORECASE)
TABLE_RE = re.compile(r"^table\s*([A-Za-z0-9.-]+)", re.IGNORECASE)
SUPPLEMENT_RE = re.compile(
    r"^(?:supplementary|supplemental)\s+(?:figure|table|data|note)?\s*([A-Za-z0-9.-]*)",
    re.IGNORECASE,
)


def extract_pdf_with_pypdf(path: Path, max_pages: int) -> tuple[list[str], str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return [], ""
    reader = PdfReader(str(path))
    pages = [
        (page.extract_text() or "")
        for page in reader.pages[:max_pages]
    ]
    return pages, "pypdf"


def extract_pdf_with_pdftotext(path: Path, max_pages: int) -> tuple[list[str], str]:
    executable = shutil.which("pdftotext")
    if not executable:
        return [], ""
    proc = subprocess.run(
        [executable, "-f", "1", "-l", str(max_pages), "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if proc.returncode != 0:
        return [], ""
    pages = proc.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages, "pdftotext"


def extract_text(path: Path, max_pages: int) -> tuple[list[str], str, str, list[str]]:
    suffix = path.suffix.lower()
    unresolved: list[str] = []
    if suffix == ".pdf":
        pages, method = extract_pdf_with_pypdf(path, max_pages)
        if not pages:
            pages, method = extract_pdf_with_pdftotext(path, max_pages)
        if not pages:
            unresolved.append(
                "PDF text was not extracted because neither pypdf nor pdftotext was available or successful."
            )
            return [], "application/pdf", "unavailable", unresolved
        return pages, "application/pdf", method, unresolved
    if suffix in {".txt", ".md", ".markdown"}:
        text = path.read_text(encoding="utf-8")
        pages = text.split("\f")
        media_type = "text/markdown" if suffix in {".md", ".markdown"} else "text/plain"
        return pages[:max_pages], media_type, "plain-text", unresolved
    guessed = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    unresolved.append(f"Unsupported media type: {guessed}")
    return [], guessed, "unavailable", unresolved


def paragraph_blocks(pages: list[str], page_grounded: bool) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for page_number, page in enumerate(pages, start=1):
        paragraphs = [
            re.sub(r"\s+", " ", paragraph).strip()
            for paragraph in re.split(r"\n\s*\n", page)
            if paragraph.strip()
        ]
        if not paragraphs and page.strip():
            paragraphs = [
                re.sub(r"\s+", " ", line).strip()
                for line in page.splitlines()
                if line.strip()
            ]
        for paragraph_number, text in enumerate(paragraphs, start=1):
            locator = (
                [f"page:{page_number}", f"paragraph:{page_number}.{paragraph_number}"]
                if page_grounded
                else [f"block:{len(blocks) + 1}"]
            )
            blocks.append(
                {
                    "block_id": f"block-{len(blocks) + 1:05d}",
                    "text": text,
                    "locators": locator,
                    "text_checksum": sha256_json(text),
                }
            )
    return blocks


def detect_artifacts(blocks: list[dict[str, Any]]) -> tuple[list[dict], list[dict], list[dict]]:
    figures: list[dict] = []
    tables: list[dict] = []
    supplements: list[dict] = []
    for block in blocks:
        text = block["text"]
        figure_match = FIGURE_RE.match(text)
        table_match = TABLE_RE.match(text)
        supplement_match = SUPPLEMENT_RE.match(text)
        record = {
            "caption": text,
            "source_block_id": block["block_id"],
            "locators": block["locators"],
        }
        if figure_match:
            figures.append({"figure_id": figure_match.group(1), **record})
        if table_match:
            tables.append({"table_id": table_match.group(1), **record})
        if supplement_match:
            supplements.append(
                {"supplement_id": supplement_match.group(1) or str(len(supplements) + 1), **record}
            )
    return figures, tables, supplements


def detect_sections(blocks: list[dict[str, Any]]) -> list[dict]:
    sections: list[dict] = []
    for block in blocks:
        text = block["text"].strip().strip("#").strip()
        if len(text) <= 120 and HEADING_RE.fullmatch(text):
            sections.append(
                {
                    "section_id": f"section-{len(sections) + 1:03d}",
                    "title": text,
                    "start_block_id": block["block_id"],
                    "locators": block["locators"],
                }
            )
    return sections


def build_bundle(args: argparse.Namespace) -> dict:
    path = args.input.resolve()
    if not path.exists() or not path.is_file():
        raise SystemExit(f"Input file does not exist: {path}")
    pages, media_type, method, unresolved = extract_text(path, args.max_pages)
    page_grounded = media_type == "application/pdf" and bool(pages)
    locator_mode = (
        "page-grounded"
        if page_grounded
        else "structure-grounded"
        if pages
        else "source-limited"
    )
    blocks = paragraph_blocks(pages, page_grounded)
    figures, tables, supplements = detect_artifacts(blocks)
    sections = detect_sections(blocks)
    title = args.title or path.stem
    paper_id = args.paper_id or stable_id(
        "paper",
        {"checksum": sha256_file(path), "title": title},
    )
    inspected = ["local file identity and SHA-256 checksum"]
    if blocks:
        inspected.append(f"{len(blocks)} extracted text blocks")
    if page_grounded:
        inspected.append(f"{len(pages)} PDF pages with page locators")
    cannot_conclude = [
        "scientific validity, causal mechanism, clinical utility, or reproducibility from extraction alone",
        "content of image-only figures, equations, or tables unless separately inspected",
    ]
    return {
        "schema_version": "ocean-paper-bundle-v1",
        "paper_id": paper_id,
        "producer": {"name": "OCEAN PaperBundle builder", "version": OCEAN_VERSION},
        "source": {
            "path": str(path),
            "title": title,
            "media_type": media_type,
        },
        "file_checksum": sha256_file(path),
        "locator_mode": locator_mode,
        "sections": sections,
        "blocks": blocks,
        "figures": figures,
        "tables": tables,
        "supplements": supplements,
        "unresolved_regions": unresolved,
        "extraction": {
            "method": method,
            "created_at": now_utc(),
            "page_count": len(pages),
            "max_pages": args.max_pages,
        },
        "evidence_boundary": evidence_boundary(
            inspected=inspected,
            not_inspected=[
                "semantic correctness of extracted text",
                "figure pixels and table cell structure",
                "supplement files not supplied as input",
            ],
            cannot_conclude=cannot_conclude,
            next_required=(
                ["install pypdf or pdftotext and rerun extraction"]
                if not pages and media_type == "application/pdf"
                else ["audit claim locators and inspect relevant figures/tables before claim review"]
            ),
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prepare a grounded OCEAN PaperBundle.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--title")
    parser.add_argument("--paper-id")
    parser.add_argument("--max-pages", type=int, default=500)
    args = parser.parse_args(argv)
    if args.max_pages < 1:
        raise SystemExit("--max-pages must be positive")
    bundle = build_bundle(args)
    errors = validate_required_contract(
        bundle,
        schema_path(__file__, "paper_bundle.schema.json"),
    )
    if errors:
        raise SystemExit("PaperBundle validation failed: " + "; ".join(errors))
    write_json(args.output, bundle)
    print(
        json.dumps(
            {
                "paper_id": bundle["paper_id"],
                "locator_mode": bundle["locator_mode"],
                "blocks": len(bundle["blocks"]),
                "figures": len(bundle["figures"]),
                "tables": len(bundle["tables"]),
                "unresolved_regions": len(bundle["unresolved_regions"]),
                "output": str(args.output),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
