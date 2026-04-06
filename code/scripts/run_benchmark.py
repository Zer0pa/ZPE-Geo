#!/usr/bin/env python3
"""Run fixture benchmarks and write machine-readable results."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zpe_geo.codec import decode_trajectory, encode_trajectory
from zpe_geo.metrics import compression_ratio, percentile
from zpe_geo.utils import ensure_dir

REPO_ROOT = ROOT.parent
FIXTURE_ROOT = ROOT / "fixtures"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "proofs" / "artifacts" / "fixture_benchmarks"
DEFAULT_FIXTURES = ("ais_noaa_fixture_v1.json", "av_argoverse2_fixture_v1.json")
DEFAULT_QUANT_BY_COORD = {"wgs84": 0.25, "xy": 0.05}


@dataclass(frozen=True)
class RoundtripCheck:
    exact: bool
    max_abs_error: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        action="append",
        dest="fixtures",
        help="Fixture filename under code/fixtures. May be passed multiple times.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Directory for benchmark artifacts.",
    )
    return parser.parse_args()


def load_fixture(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        trajectories = payload.get("trajectories") or []
        metadata = payload.get("metadata") or {}
    elif isinstance(payload, list):
        trajectories = payload
        metadata = {}
    else:
        raise ValueError(f"unsupported fixture payload in {path}")
    if not trajectories:
        raise ValueError(f"fixture {path.name} contains no trajectories")
    return metadata, trajectories


def raw_json_bytes(trajectory: dict[str, Any]) -> int:
    return len(json.dumps(trajectory, separators=(",", ":"), sort_keys=True).encode("utf-8"))


def roundtrip_check(original: dict[str, Any], decoded: dict[str, Any]) -> RoundtripCheck:
    if len(original["points"]) != len(decoded["points"]):
        return RoundtripCheck(exact=False, max_abs_error=float("inf"))

    coord_system = original.get("coord_system", "xy")
    max_error = 0.0
    for source, recovered in zip(original["points"], decoded["points"], strict=True):
        if coord_system == "wgs84":
            errors = [
                abs(float(source["lat"]) - float(recovered["lat"])),
                abs(float(source["lon"]) - float(recovered["lon"])),
            ]
        else:
            errors = [
                abs(float(source["x"]) - float(recovered["x"])),
                abs(float(source["y"]) - float(recovered["y"])),
            ]
        max_error = max(max_error, *errors)
        if any(error != 0.0 for error in errors):
            return RoundtripCheck(exact=False, max_abs_error=max_error)
    return RoundtripCheck(exact=True, max_abs_error=max_error)


def quant_step_for(trajectory: dict[str, Any]) -> float:
    coord_system = trajectory.get("coord_system", "xy")
    return DEFAULT_QUANT_BY_COORD.get(coord_system, 0.05)


def benchmark_fixture(fixture_name: str) -> dict[str, Any]:
    fixture_path = FIXTURE_ROOT / fixture_name
    metadata, trajectories = load_fixture(fixture_path)
    encode_timings_us: list[float] = []
    decode_timings_us: list[float] = []
    encoded_sizes: list[int] = []
    raw_sizes: list[int] = []
    exact_matches = 0
    max_abs_error = 0.0

    for trajectory in trajectories:
        quant_step_m = quant_step_for(trajectory)
        encode_start = time.perf_counter_ns()
        encoded = encode_trajectory(trajectory, quant_step_m=quant_step_m)
        encode_end = time.perf_counter_ns()
        decoded = decode_trajectory(encoded.payload)
        decode_end = time.perf_counter_ns()

        raw_sizes.append(raw_json_bytes(trajectory))
        encoded_sizes.append(len(encoded.payload))
        encode_timings_us.append((encode_end - encode_start) / 1000.0)
        decode_timings_us.append((decode_end - encode_end) / 1000.0)

        check = roundtrip_check(trajectory, decoded)
        exact_matches += int(check.exact)
        max_abs_error = max(max_abs_error, check.max_abs_error)

    coord_system = trajectories[0].get("coord_system", "xy")
    return {
        "fixture": fixture_name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata,
        "coord_system": coord_system,
        "trajectory_count": len(trajectories),
        "fixture_file_bytes": fixture_path.stat().st_size,
        "raw_json_bytes_total": sum(raw_sizes),
        "encoded_bytes_total": sum(encoded_sizes),
        "compression_ratio": compression_ratio(sum(raw_sizes), sum(encoded_sizes)),
        "quant_step_m": quant_step_for(trajectories[0]),
        "encode_time_us": {
            "mean": statistics.mean(encode_timings_us),
            "median": statistics.median(encode_timings_us),
            "p95": percentile(encode_timings_us, 95),
        },
        "decode_time_us": {
            "mean": statistics.mean(decode_timings_us),
            "median": statistics.median(decode_timings_us),
            "p95": percentile(decode_timings_us, 95),
        },
        "roundtrip": {
            "coordinate_exact_match_count": exact_matches,
            "coordinate_exact_match_ratio": exact_matches / len(trajectories),
            "all_coordinates_exact": exact_matches == len(trajectories),
            "max_abs_coordinate_error": max_abs_error,
        },
    }


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_markdown(path: Path, results: list[dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    lines = [
        "# Fixture Benchmarks",
        "",
        "| Fixture | Compression Ratio | Encode Mean (us) | Decode Mean (us) | Exact Coordinate Matches | Max Abs Error |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        roundtrip = result["roundtrip"]
        lines.append(
            "| {fixture} | {ratio:.2f} | {encode:.1f} | {decode:.1f} | {matches}/{count} | {max_error:.12f} |".format(
                fixture=result["fixture"],
                ratio=result["compression_ratio"],
                encode=result["encode_time_us"]["mean"],
                decode=result["decode_time_us"]["mean"],
                matches=roundtrip["coordinate_exact_match_count"],
                count=result["trajectory_count"],
                max_error=roundtrip["max_abs_coordinate_error"],
            )
        )
    lines.extend(
        [
            "",
            "Exact coordinate equality is reported as observed.",
            "The current codec does not produce exact coordinate equality on the shipped fixtures, so this artifact preserves that result instead of suppressing it.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    fixture_names = args.fixtures or list(DEFAULT_FIXTURES)
    output_root = Path(args.output_dir).resolve()
    ensure_dir(output_root)

    results = [benchmark_fixture(name) for name in fixture_names]
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "fixtures": [result["fixture"] for result in results],
        "result_files": [f"{Path(result['fixture']).stem}_benchmark.json" for result in results],
    }

    for result in results:
        result_path = output_root / f"{Path(result['fixture']).stem}_benchmark.json"
        write_json(result_path, result)
    write_json(output_root / "benchmark_summary.json", summary)
    write_markdown(output_root / "README.md", results)


if __name__ == "__main__":
    main()
