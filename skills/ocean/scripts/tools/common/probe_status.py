"""Shared classification for bounded command availability probes."""

from __future__ import annotations


def classify_probe_status(returncode: int, *outputs: str) -> str:
    """Return an evidence-safe status for a version/help probe."""
    has_output = any(output.strip() for output in outputs)
    if returncode == 0 and has_output:
        return "executed"
    if returncode in {1, 2} and has_output:
        return "found_but_probe_nonzero"
    return "found_but_probe_failed"
