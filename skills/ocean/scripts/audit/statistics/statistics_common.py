#!/usr/bin/env python3
"""Shared builders for OCEAN Statistical Evidence Cards."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, stable_id


FIELDS = [
    "experimental_unit",
    "observation_unit",
    "replication_hierarchy",
    "model_or_test",
    "assumptions",
    "effect_estimate",
    "uncertainty",
    "multiplicity",
    "claim_supported",
    "claim_not_supported",
]


def make_card(payload: dict[str, Any], issues: list[str], author_input: list[str]) -> dict:
    data = {field: payload.get(field) for field in FIELDS}
    return {
        "schema_version": "ocean-statistical-evidence-card-v1",
        "card_id": stable_id("stats", payload),
        **data,
        "issues": issues,
        "AUTHOR_INPUT_NEEDED": author_input,
        "status": "needs_author_input" if author_input else "needs_review" if issues else "structurally_complete",
        "evidence_boundary": evidence_boundary(
            inspected=["declared statistical design fields"],
            not_inspected=["raw data", "model fit", "test implementation", "figure pixels"],
            cannot_conclude=["statistical validity or biological importance from metadata alone"],
            next_required=author_input or issues or ["inspect raw analysis and assumptions"],
        ),
    }


def missing_fields(payload: dict[str, Any]) -> list[str]:
    return [field for field in FIELDS if payload.get(field) in (None, "", [], {})]
