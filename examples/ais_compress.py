#!/usr/bin/env python3
"""Compress a shipped real NOAA AIS extract and report savings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from zpe_geo.codec import encode_trajectory
from zpe_geo.metrics import compression_ratio


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = REPO_ROOT / "code" / "fixtures" / "real_world" / "noaa_ais_day_extract.json"


def _load_payload(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected dict payload in {path}")
    trajectories = payload.get("trajectories") or []
    if not trajectories:
        raise ValueError(f"fixture {path} contains no trajectories")
    metadata = payload.get("metadata") or {}
    return metadata, trajectories


def _raw_json_bytes(trajectory: dict[str, Any]) -> int:
    return len(json.dumps(trajectory, separators=(",", ":"), sort_keys=True).encode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-path", default=str(DEFAULT_FIXTURE), help="Path to a real-world AIS fixture JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    fixture_path = Path(args.fixture_path).resolve()
    metadata, trajectories = _load_payload(fixture_path)

    raw_bytes_total = 0
    encoded_bytes_total = 0
    for trajectory in trajectories:
        raw_bytes_total += _raw_json_bytes(trajectory)
        encoded_bytes_total += len(encode_trajectory(trajectory, quant_step_m=0.25).payload)

    summary = {
        "dataset": "NOAA AIS extract",
        "fixture_path": str(fixture_path),
        "trajectory_count": len(trajectories),
        "raw_json_bytes_total": raw_bytes_total,
        "encoded_bytes_total": encoded_bytes_total,
        "compression_ratio": compression_ratio(raw_bytes_total, encoded_bytes_total),
        "source_reference": metadata.get("reference", "unknown"),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
