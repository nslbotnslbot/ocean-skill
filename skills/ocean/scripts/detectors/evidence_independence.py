#!/usr/bin/env python3
"""Classify independence between discovery and validation evidence sources."""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
import json
from pathlib import Path
import sys
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import evidence_boundary, read_json, write_json


DEPENDENCY_RELATIONS = {
    "derived_from",
    "contains",
    "trained_on",
    "validated_on",
    "same_source_family",
    "overlaps",
    "reuses",
}


def ancestor_map(nodes: dict[str, dict], edges: list[dict]) -> dict[str, set[str]]:
    parents: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge.get("relation") in DEPENDENCY_RELATIONS:
            source = edge.get("source")
            target = edge.get("target")
            if source in nodes and target in nodes:
                parents[source].add(target)
    result: dict[str, set[str]] = {}
    for node_id in nodes:
        seen: set[str] = set()
        queue = deque(parents.get(node_id, set()))
        while queue:
            current = queue.popleft()
            if current in seen:
                continue
            seen.add(current)
            queue.extend(parents.get(current, set()) - seen)
        result[node_id] = seen
    return result


def classify_pair(
    discovery: str,
    validation: str,
    nodes: dict[str, dict],
    ancestors: dict[str, set[str]],
) -> dict[str, Any]:
    discovery_node = nodes.get(discovery)
    validation_node = nodes.get(validation)
    if not discovery_node or not validation_node:
        return {
            "discovery": discovery,
            "validation": validation,
            "classification": "unknown",
            "reasons": ["one or both source nodes are missing"],
        }
    discovery_ancestors = ancestors.get(discovery, set())
    validation_ancestors = ancestors.get(validation, set())
    shared_upstream = sorted(discovery_ancestors & validation_ancestors)
    same_family = (
        bool(discovery_node.get("source_family"))
        and discovery_node.get("source_family") == validation_node.get("source_family")
    )
    reasons: list[str] = []
    if discovery == validation:
        classification = "circular"
        reasons.append("the same source is used for discovery and validation")
    elif discovery in validation_ancestors or validation in discovery_ancestors:
        classification = "circular"
        reasons.append("one source is upstream of the other")
    elif shared_upstream:
        classification = "partially_independent"
        reasons.append("sources share upstream dependencies: " + ", ".join(shared_upstream))
    elif same_family:
        classification = "partially_independent"
        reasons.append("sources share the same declared source family")
    elif not discovery_node.get("source_family") or not validation_node.get("source_family"):
        classification = "unknown"
        reasons.append("source-family provenance is incomplete")
    else:
        classification = "independent"
        reasons.append("no shared node, dependency path, upstream ancestor, or source family was declared")
    return {
        "discovery": discovery,
        "validation": validation,
        "classification": classification,
        "reasons": reasons,
        "shared_upstream": shared_upstream,
        "discovery_source_family": discovery_node.get("source_family", ""),
        "validation_source_family": validation_node.get("source_family", ""),
    }


def classify_graph(payload: dict) -> dict:
    nodes = {node["node_id"]: node for node in payload.get("nodes", [])}
    edges = payload.get("edges", [])
    discovery_sources = payload.get("discovery_sources", [])
    validation_sources = payload.get("validation_sources", [])
    ancestors = ancestor_map(nodes, edges)
    pairs = [
        classify_pair(discovery, validation, nodes, ancestors)
        for discovery in discovery_sources
        for validation in validation_sources
    ]
    labels = {pair["classification"] for pair in pairs}
    if not pairs:
        overall = "unknown"
    elif "circular" in labels:
        overall = "circular"
    elif "unknown" in labels:
        overall = "unknown"
    elif "partially_independent" in labels:
        overall = "partially_independent"
    else:
        overall = "independent"
    missing_nodes = sorted(
        set(discovery_sources + validation_sources) - set(nodes)
    )
    return {
        "schema_version": "ocean-evidence-independence-v1",
        "classification": overall,
        "discovery_sources": discovery_sources,
        "validation_sources": validation_sources,
        "pairs": pairs,
        "missing_nodes": missing_nodes,
        "graph_summary": {
            "nodes": len(nodes),
            "edges": len(edges),
            "dependency_relations_considered": sorted(DEPENDENCY_RELATIONS),
        },
        "evidence_boundary": evidence_boundary(
            inspected=[
                "declared nodes, source families, and dependency edges",
                "declared discovery and validation source sets",
            ],
            not_inspected=[
                "undeclared database aggregation",
                "patient/cohort overlap not represented in the graph",
                "training-corpus overlap not represented in the graph",
            ],
            cannot_conclude=[
                "real-world independence when provenance is incomplete",
                "scientific validity merely because sources appear independent",
            ],
            next_required=(
                [f"add missing node provenance: {node}" for node in missing_nodes]
                or ["confirm upstream datasets, cohorts, papers, and model training sources"]
            ),
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect circular or partially independent evidence.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    payload = classify_graph(read_json(args.input))
    write_json(args.output, payload)
    print(json.dumps({"classification": payload["classification"], "pairs": len(payload["pairs"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
