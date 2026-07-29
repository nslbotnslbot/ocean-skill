#!/usr/bin/env python3
"""Small dependency-free rate limiter and retry policy for OCEAN adapters."""

from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import dataclass, field
from pathlib import Path
import sys

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ocean_core import write_json


@dataclass
class RateLimiter:
    requests_per_second: float = 3.0
    _last_request: float = field(default=0.0, init=False)

    def wait(self) -> None:
        if self.requests_per_second <= 0:
            raise ValueError("requests_per_second must be positive")
        interval = 1.0 / self.requests_per_second
        delay = interval - (time.monotonic() - self._last_request)
        if delay > 0:
            time.sleep(delay)
        self._last_request = time.monotonic()


def backoff_schedule(
    attempts: int,
    base_seconds: float,
    maximum_seconds: float,
    jitter_fraction: float,
    seed: int | None = None,
) -> list[float]:
    generator = random.Random(seed)
    schedule = []
    for attempt in range(attempts):
        delay = min(maximum_seconds, base_seconds * (2**attempt))
        jitter = delay * jitter_fraction * generator.random()
        schedule.append(round(delay + jitter, 3))
    return schedule


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a bounded API retry schedule.")
    parser.add_argument("--attempts", type=int, default=4)
    parser.add_argument("--base-seconds", type=float, default=1.0)
    parser.add_argument("--maximum-seconds", type=float, default=30.0)
    parser.add_argument("--jitter-fraction", type=float, default=0.2)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.attempts < 1 or args.attempts > 10:
        raise SystemExit("--attempts must be between 1 and 10")
    payload = {
        "schema_version": "ocean-retry-policy-v1",
        "attempts": args.attempts,
        "schedule_seconds": backoff_schedule(
            args.attempts,
            args.base_seconds,
            args.maximum_seconds,
            args.jitter_fraction,
            args.seed,
        ),
        "evidence_boundary": "Retry planning only; no network request was made.",
    }
    if args.output:
        write_json(args.output, payload)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
