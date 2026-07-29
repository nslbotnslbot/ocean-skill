#!/usr/bin/env python3
"""Shared standard-library helpers for OCEAN evidence-control scripts."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "ocean-control-plane-r1"
OCEAN_VERSION = "0.2.0"


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def today_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_json(payload: Any) -> str:
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def stable_id(prefix: str, payload: Any, length: int = 16) -> str:
    return f"{prefix}-{sha256_json(payload)[:length]}"


def parse_json_argument(value: str, expected_type: type, label: str) -> Any:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{label} must be valid JSON: {exc}") from exc
    if not isinstance(parsed, expected_type):
        raise SystemExit(f"{label} must decode to {expected_type.__name__}")
    return parsed


def require_fields(payload: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [
        field
        for field in fields
        if field not in payload or payload[field] in (None, "", [])
    ]
    if missing:
        raise SystemExit(f"{label} is missing required fields: {', '.join(missing)}")


def evidence_boundary(
    *,
    inspected: list[str],
    not_inspected: list[str],
    cannot_conclude: list[str],
    next_required: list[str],
) -> dict[str, list[str]]:
    return {
        "inspected": inspected,
        "not_inspected": not_inspected,
        "cannot_conclude": cannot_conclude,
        "next_required": next_required,
    }


def file_record(path: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
    }
    if path.exists() and path.is_file():
        record.update(
            {
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return record


def schema_path(script_file: str, schema_name: str) -> Path:
    scripts_dir = Path(script_file).resolve().parent
    while scripts_dir.name != "scripts" and scripts_dir.parent != scripts_dir:
        scripts_dir = scripts_dir.parent
    return scripts_dir.parent / "schemas" / schema_name


def validate_required_contract(
    payload: dict[str, Any],
    schema_file: Path,
) -> list[str]:
    """Validate the required/type/enum subset used by OCEAN schemas.

    Full JSON Schema validation remains available to downstream applications.
    Runtime scripts keep this dependency-free validator so an installed skill
    can enforce its core contract without downloading packages.
    """

    schema = read_json(schema_file)
    errors: list[str] = []

    def walk(value: Any, contract: dict[str, Any], location: str) -> None:
        expected = contract.get("type")
        type_map = {
            "object": dict,
            "array": list,
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
        }
        if expected in type_map and not isinstance(value, type_map[expected]):
            errors.append(f"{location}: expected {expected}")
            return
        if "const" in contract and value != contract["const"]:
            errors.append(f"{location}: expected constant {contract['const']!r}")
        if "enum" in contract and value not in contract["enum"]:
            errors.append(f"{location}: value is outside allowed enum")
        if isinstance(value, dict):
            for field in contract.get("required", []):
                if field not in value:
                    errors.append(f"{location}.{field}: required field missing")
            properties = contract.get("properties", {})
            for field, child in value.items():
                if field in properties:
                    walk(child, properties[field], f"{location}.{field}")
        if isinstance(value, list) and isinstance(contract.get("items"), dict):
            for index, child in enumerate(value):
                walk(child, contract["items"], f"{location}[{index}]")

    walk(payload, schema, "$")
    return errors
