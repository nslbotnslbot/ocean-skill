#!/usr/bin/env python3
"""Validate OCEAN JSON Schemas and their explicitly mapped fixtures.

This is a development/CI check. It deliberately validates only the eleven
published schemas and the instances mapped below; it does not imply that every
JSON file in the repository conforms to one of these schemas.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "skills" / "ocean" / "schemas"
DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


def evidence_boundary() -> Dict[str, List[str]]:
    return {
        "inspected": [],
        "not_inspected": [],
        "cannot_conclude": [],
        "next_required": [],
    }


def availability_dimension(dimension_id: str) -> Dict[str, Any]:
    return {
        "dimension_id": dimension_id,
        "status": "not_explicitly_located",
        "signal_count": 0,
        "retained_evidence_count": 0,
        "evidence": [],
        "cannot_conclude": "No explicit signal was located in this fixture.",
        "author_input_needed": "Human review is required before any conclusion.",
        "human_review_required": True,
    }


DIMENSION_IDS = (
    "data_availability_statement",
    "code_availability_statement",
    "data_repository",
    "persistent_identifier_or_accession",
    "controlled_access",
    "request_based_access",
    "third_party_restriction",
    "metadata_or_data_dictionary",
    "license_terms",
    "source_data",
    "model_weights",
    "prompt_or_configuration",
    "reproducibility_environment",
    "version_or_commit",
)


# Every published schema must appear exactly once in this explicit map. Inline
# entries are deterministic test fixtures; file entries are checked-in runtime
# examples. The coverage guard in main() fails if a schema is added or removed
# without updating this mapping.
INLINE_FIXTURES: Dict[str, Dict[str, Any]] = {
    "artifact_envelope.schema.json": {
        "schema_version": "ocean-artifact-envelope-v1",
        "envelope_id": "envelope-fixture",
        "artifact_type": "external_artifact",
        "artifact_schema_version": "fixture-v1",
        "artifact_id": "artifact-fixture",
        "producer": {"name": "fixture", "version": "1"},
        "created_at": "2026-01-01T00:00:00Z",
        "content_checksum": "fixture-checksum",
        "artifact": {},
        "source_refs": [],
        "run_ref": "run-fixture",
        "access": "local",
        "license": "unknown",
        "evidence_boundary": evidence_boundary(),
    },
    "availability_evidence_card.schema.json": {
        "schema_version": "ocean-availability-evidence-card-v1",
        "run_id": "run-fixture",
        "case_id": "case-fixture",
        "paper_id": "paper-fixture",
        "paper_bundle": {
            "path": "paper-bundle.json",
            "sha256": "0" * 64,
            "source_xml_path": "paper.xml",
            "source_xml_sha256": "1" * 64,
            "locator_mode": "structure-grounded",
            "license": None,
        },
        "inspection": {
            "inspected_section_count": 0,
            "inspected_paragraph_count": 0,
            "unique_text_count": 0,
            "duplicate_locator_count": 0,
            "availability_section_ids": [],
            "availability_section_titles": [],
            "excluded_reference_section_count": 0,
            "unresolved_regions": [],
        },
        "dimensions": {
            dimension_id: availability_dimension(dimension_id)
            for dimension_id in DIMENSION_IDS
        },
        "resource_candidates": [],
        "resource_candidate_count": 0,
        "retained_resource_candidate_count": 0,
        "placeholder_candidates": [],
        "placeholder_candidate_count": 0,
        "retained_placeholder_candidate_count": 0,
        "not_explicitly_located_dimension_count": 14,
        "author_input_needed": ["Human review of availability evidence."],
        "stop_conditions": ["Do not infer availability from absent text."],
        "overall_state": "availability_signals_only",
        "availability_verified": False,
        "fair_compliance_verified": False,
        "repository_identity_verified": False,
        "license_compatibility_verified": False,
        "expert_review_required": True,
        "scientific_evidence": False,
        "evidence_boundary": "Fixture exercises structure, not scientific truth.",
        "deterministic_payload_sha256": "2" * 64,
    },
    "claim_card.schema.json": {
        "schema_version": "ocean-claim-card-v1",
        "claim_id": "claim-fixture",
        "claim_text": "Fixture claim with no scientific assertion.",
        "claim_type": "unknown",
        "support_level": "unknown",
        "current_evidence": [],
        "source_locators": [],
        "maximum_safe_claim": "Cannot decide from this fixture.",
        "missing_evidence": ["Inspected evidence"],
        "stop_conditions": ["No evidence supplied"],
        "evidence_boundary": evidence_boundary(),
    },
    "evidence_node.schema.json": {
        "schema_version": "ocean-evidence-node-v1",
        "node_id": "node-fixture",
        "node_type": "paper",
        "label": "Fixture node",
        "source_family": "fixture",
        "metadata": {},
    },
    "paper_bundle.schema.json": {
        "schema_version": "ocean-paper-bundle-v1",
        "paper_id": "paper-fixture",
        "source": {
            "path": "paper.txt",
            "title": "Fixture paper",
            "media_type": "text/plain",
        },
        "file_checksum": "fixture-checksum",
        "locator_mode": "source-limited",
        "sections": [],
        "blocks": [],
        "figures": [],
        "tables": [],
        "supplements": [],
        "unresolved_regions": [],
        "extraction": {
            "method": "fixture",
            "created_at": "2026-01-01T00:00:00Z",
            "page_count": 0,
        },
        "evidence_boundary": evidence_boundary(),
    },
    "research_package.schema.json": {
        "schema_version": "ocean-research-package-v1",
        "request_mode": "Audit",
        "red_team_requested": True,
        "domain": "biomedical_ai",
        "components": {
            component: {"status": "missing", "locators": []}
            for component in (
                "study_framing",
                "claims_or_study_plan",
                "data_or_cohort",
                "validation_design",
            )
        },
        "source_packets": [
            {
                "packet_id": "packet-fixture",
                "evidence_state": "candidate",
                "locators": [],
            }
        ],
    },
    "research_red_team_review.schema.json": {
        "schema_version": "ocean-research-red-team-review-v1",
        "package_gate_id": "gate-fixture",
        "package_gate_status": "ready_for_human_red_team",
        "source_packet_ids": ["packet-fixture"],
        "conclusions": [
            {
                "conclusion_id": "conclusion-fixture",
                "kind": "decision",
                "statement": "Human review is still required.",
                "decision": "Cannot decide",
                "evidence_state": "located",
                "evidence": [
                    {"packet_id": "packet-fixture", "locator": "fixture:1"}
                ],
                "next_required": ["Human red-team review"],
            }
        ],
    },
    "run_manifest.schema.json": {
        "schema_version": "ocean-run-manifest-v1",
        "run_id": "run-fixture",
        "task_intent": "Exercise schema validation only",
        "created_at": "2026-01-01T00:00:00Z",
        "status": "planned",
        "command": [],
        "software": {"name": "fixture", "version": "1"},
        "parameters": {},
        "inputs": [],
        "outputs": [],
        "environment": {"python": "3", "platform": "fixture"},
        "evidence_boundary": evidence_boundary(),
    },
    "source_packet_v2.schema.json": {
        "schema_version": "ocean-source-packet-v2",
        "packet_id": "packet-fixture",
        "source": {
            "source_type": "fixture",
            "source_id": "source-fixture",
            "retrieved_at": "2026-01-01T00:00:00Z",
            "checksum": "fixture-checksum",
        },
        "evidence_state": "candidate",
        "locator_mode": "source-limited",
        "locators": [],
        "supports_claims": [],
        "cannot_support": ["Scientific conclusions"],
        "upstream_dependencies": [],
        "conflict_state": "unknown",
        "recheck_policy": {
            "stale_after": "unknown",
            "recheck_trigger": ["Source changes"],
        },
        "evidence_boundary": evidence_boundary(),
    },
    "validation_card.schema.json": {
        "schema_version": "ocean-validation-card-v1",
        "validation_id": "validation-fixture",
        "claim_id": "claim-fixture",
        "claim_type": "unknown",
        "current_evidence_classes": [],
        "required_evidence_classes": [],
        "independence_requirement": "Human review required",
        "decisive_controls": [],
        "pass_criteria": [],
        "missing_evidence": ["Inspected evidence"],
        "maximum_safe_claim": "Cannot decide from this fixture.",
        "stop_conditions": ["No evidence supplied"],
        "evidence_boundary": evidence_boundary(),
    },
}

FILE_FIXTURES: Dict[str, Tuple[Path, ...]] = {
    "visual_style_memory.schema.json": (
        ROOT / "skills" / "ocean" / "references" / "visual-style-memory.json",
        ROOT / "skills" / ".ocean" / "visual_style_memory.json",
    )
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def json_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        elif isinstance(part, str) and part.isidentifier():
            rendered += f".{part}"
        else:
            rendered += f"[{json.dumps(part)}]"
    return rendered


def diagnostic(error: ValidationError) -> str:
    schema_path = "/".join(str(part) for part in error.absolute_schema_path)
    return (
        f"validator={error.validator!r} instance_path={json_path(error.absolute_path)} "
        f"schema_path=/{schema_path}: {error.message}"
    )


def ordered_errors(
    validator: Draft202012Validator, instance: Any
) -> List[ValidationError]:
    return sorted(
        validator.iter_errors(instance),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            tuple(str(part) for part in error.absolute_schema_path),
            error.message,
        ),
    )


def mapped_fixtures(schema_name: str) -> Sequence[Tuple[str, Any]]:
    if schema_name in INLINE_FIXTURES:
        return (("inline:minimal-valid", INLINE_FIXTURES[schema_name]),)
    return tuple(
        (str(path.relative_to(ROOT)), load_json(path))
        for path in FILE_FIXTURES[schema_name]
    )


def negative_cases() -> Sequence[Tuple[str, str, Any, str, Tuple[Any, ...]]]:
    research_package = INLINE_FIXTURES["research_package.schema.json"]
    availability = INLINE_FIXTURES["availability_evidence_card.schema.json"]

    missing_ref_required = copy.deepcopy(research_package)
    del missing_ref_required["components"]["study_framing"]["locators"]

    extra_property = copy.deepcopy(research_package)
    extra_property["undeclared"] = True

    invalid_pattern = copy.deepcopy(availability)
    invalid_pattern["deterministic_payload_sha256"] = "not-a-sha256"

    too_few_items = copy.deepcopy(availability)
    too_few_items["stop_conditions"] = []

    duplicate_items = copy.deepcopy(availability)
    duplicate_items["author_input_needed"] = ["review", "review"]

    return (
        (
            "nested-$ref-required",
            "research_package.schema.json",
            missing_ref_required,
            "required",
            ("components", "study_framing"),
        ),
        (
            "additional-properties",
            "research_package.schema.json",
            extra_property,
            "additionalProperties",
            (),
        ),
        (
            "sha256-pattern",
            "availability_evidence_card.schema.json",
            invalid_pattern,
            "pattern",
            ("deterministic_payload_sha256",),
        ),
        (
            "nonempty-stop-conditions",
            "availability_evidence_card.schema.json",
            too_few_items,
            "minItems",
            ("stop_conditions",),
        ),
        (
            "unique-author-input",
            "availability_evidence_card.schema.json",
            duplicate_items,
            "uniqueItems",
            ("author_input_needed",),
        ),
    )


def main() -> int:
    failures: List[str] = []
    schema_paths = sorted(SCHEMA_DIR.glob("*.schema.json"))
    discovered = {path.name for path in schema_paths}
    mapped = set(INLINE_FIXTURES) | set(FILE_FIXTURES)
    duplicate_mappings = set(INLINE_FIXTURES) & set(FILE_FIXTURES)

    if duplicate_mappings:
        failures.append(
            "schemas mapped as both inline and file fixtures: "
            f"{sorted(duplicate_mappings)}"
        )

    if discovered != mapped:
        missing = sorted(discovered - mapped)
        stale = sorted(mapped - discovered)
        if missing:
            failures.append(f"schemas without explicit fixtures: {missing}")
        if stale:
            failures.append(f"fixture mappings without schemas: {stale}")

    schemas: Dict[str, Dict[str, Any]] = {}
    validators: Dict[str, Draft202012Validator] = {}
    positive_count = 0

    for schema_path in schema_paths:
        schema_name = schema_path.name
        schema = load_json(schema_path)
        schemas[schema_name] = schema

        if schema.get("$schema") != DRAFT_2020_12:
            failures.append(
                f"{schema_name}: $schema must be {DRAFT_2020_12!r}, "
                f"got {schema.get('$schema')!r}"
            )
            continue

        try:
            # check_schema validates the schema itself against the Draft 2020-12
            # meta-schema before we use that same dialect for its instances.
            Draft202012Validator.check_schema(schema)
        except SchemaError as error:
            failures.append(f"{schema_name}: invalid Draft 2020-12 schema: {error}")
            continue

        validator = Draft202012Validator(schema)
        validators[schema_name] = validator
        print(f"[PASS] meta-schema: {schema_name}")

        if schema_name not in mapped:
            continue
        for fixture_name, instance in mapped_fixtures(schema_name):
            positive_count += 1
            errors = ordered_errors(validator, instance)
            if errors:
                details = "\n    ".join(diagnostic(error) for error in errors)
                failures.append(
                    f"{schema_name} <- {fixture_name} failed:\n    {details}"
                )
            else:
                print(f"[PASS] instance: {schema_name} <- {fixture_name}")

    # This assertion makes the $ref part of the first negative case explicit;
    # the expected `required` error must be emitted after resolving this ref.
    component_ref = (
        schemas.get("research_package.schema.json", {})
        .get("properties", {})
        .get("components", {})
        .get("properties", {})
        .get("study_framing", {})
        .get("$ref")
    )
    if component_ref != "#/$defs/component":
        failures.append(
            "nested-$ref-required setup: expected study_framing to reference "
            f"#/$defs/component, got {component_ref!r}"
        )

    negative_count = 0
    for case_name, schema_name, instance, expected_validator, expected_path in negative_cases():
        validator = validators.get(schema_name)
        if validator is None:
            failures.append(f"{case_name}: validator unavailable for {schema_name}")
            continue
        negative_count += 1
        errors = ordered_errors(validator, instance)
        matching = [
            error
            for error in errors
            if error.validator == expected_validator
            and tuple(error.absolute_path) == expected_path
        ]
        if not matching:
            observed = "\n    ".join(diagnostic(error) for error in errors) or "no error"
            failures.append(
                f"negative fixture {case_name}: expected validator="
                f"{expected_validator!r} at {json_path(expected_path)}; observed:\n"
                f"    {observed}"
            )
        else:
            print(
                f"[PASS] negative: {case_name} -> validator={expected_validator!r} "
                f"instance_path={json_path(expected_path)}"
            )

    if failures:
        print("\nJSON Schema validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        "\nValidated "
        f"{len(schema_paths)} Draft 2020-12 schemas, "
        f"{positive_count} explicitly mapped valid instances, and "
        f"{negative_count} deterministic negative fixtures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
