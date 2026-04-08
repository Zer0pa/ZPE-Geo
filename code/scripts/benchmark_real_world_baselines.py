#!/usr/bin/env python3
"""Benchmark shipped real-world fixtures against gzip and Douglas-Peucker baselines."""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_benchmark import benchmark_fixture_path, load_fixture
from zpe_geo.comparator import encoded_size_dp_bytes, simplify_douglas_peucker
from zpe_geo.metrics import compression_ratio
from zpe_geo.utils import ensure_dir

REPO_ROOT = ROOT.parent
DEFAULT_FIXTURES = (
    REPO_ROOT / "code" / "fixtures" / "real_world" / "noaa_ais_day_extract.json",
    REPO_ROOT / "code" / "fixtures" / "real_world" / "geolife_extract.json",
    REPO_ROOT / "code" / "fixtures" / "real_world" / "osm_monaco_way_extract.json",
)
OUTPUT_ROOT = REPO_ROOT / "proofs" / "artifacts" / "baseline_benchmarks"
DP_EPSILON_M = 12.0
DATASET_LABELS = {
    "noaa_ais_day_extract": "NOAA AIS extract",
    "geolife_extract": "GeoLife extract",
    "osm_monaco_way_extract": "OSM Monaco extract",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture-path",
        action="append",
        dest="fixture_paths",
        help="Absolute or repo-relative path to a real-world fixture JSON. May be passed multiple times.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_ROOT),
        help="Directory for baseline benchmark artifacts.",
    )
    return parser.parse_args()


def _canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _gzip_bytes_total(trajectories: list[dict[str, Any]]) -> int:
    return sum(len(gzip.compress(_canonical_json_bytes(trajectory))) for trajectory in trajectories)


def _dp_bytes_total(trajectories: list[dict[str, Any]]) -> int:
    return sum(
        encoded_size_dp_bytes(simplify_douglas_peucker(trajectory, epsilon_m=DP_EPSILON_M))
        for trajectory in trajectories
    )


def _point_count_total(trajectories: list[dict[str, Any]]) -> int:
    return sum(len(trajectory.get("points") or []) for trajectory in trajectories)


def _dataset_label(fixture_path: Path) -> str:
    return DATASET_LABELS.get(fixture_path.stem, fixture_path.stem)


def build_record(fixture_path: Path) -> dict[str, Any]:
    benchmark = benchmark_fixture_path(fixture_path)
    metadata, trajectories = load_fixture(fixture_path)
    gzip_bytes_total = _gzip_bytes_total(trajectories)
    dp_bytes_total = _dp_bytes_total(trajectories)
    zpe_bytes_total = int(benchmark["encoded_bytes_total"])
    raw_json_bytes_total = int(benchmark["raw_json_bytes_total"])

    return {
        "dataset": _dataset_label(fixture_path),
        "fixture": fixture_path.name,
        "fixture_path": str(fixture_path.relative_to(REPO_ROOT)),
        "source_reference": metadata.get("reference", "unknown"),
        "source_url": metadata.get("source_url"),
        "trajectory_count": int(benchmark["trajectory_count"]),
        "point_count_total": _point_count_total(trajectories),
        "raw_json_bytes_total": raw_json_bytes_total,
        "zpe_bytes_total": zpe_bytes_total,
        "zpe_compression_ratio": float(benchmark["compression_ratio"]),
        "max_abs_coordinate_error": float(benchmark["roundtrip"]["max_abs_coordinate_error"]),
        "baselines": {
            "gzip": {
                "bytes_total": gzip_bytes_total,
                "compression_ratio": compression_ratio(raw_json_bytes_total, gzip_bytes_total),
                "improvement_vs_zpe": gzip_bytes_total / zpe_bytes_total,
            },
            "douglas_peucker": {
                "bytes_total": dp_bytes_total,
                "compression_ratio": compression_ratio(raw_json_bytes_total, dp_bytes_total),
                "epsilon_m": DP_EPSILON_M,
                "improvement_vs_zpe": dp_bytes_total / zpe_bytes_total,
            },
        },
    }


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(path: Path, records: list[dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    lines = [
        "# Real-World Baseline Benchmarks",
        "",
        "| Dataset | Trajectories | Points | Raw JSON Bytes | ZPE Bytes | ZPE Ratio | Max Error |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for record in records:
        lines.append(
            "| {dataset} | {trajectory_count} | {point_count_total} | {raw_json_bytes_total} | {zpe_bytes_total} | {zpe_compression_ratio:.2f}x | {max_abs_coordinate_error:.12f} |".format(
                **record
            )
        )
    lines.extend(
        [
            "",
            "| Dataset | Baseline | Baseline Bytes | ZPE Bytes | Improvement vs Baseline |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    for record in records:
        for baseline_name in ("gzip", "douglas_peucker"):
            baseline = record["baselines"][baseline_name]
            lines.append(
                "| {dataset} | {baseline_name} | {bytes_total} | {zpe_bytes_total} | {improvement_vs_zpe:.2f}x |".format(
                    dataset=record["dataset"],
                    baseline_name=baseline_name,
                    bytes_total=baseline["bytes_total"],
                    zpe_bytes_total=record["zpe_bytes_total"],
                    improvement_vs_zpe=baseline["improvement_vs_zpe"],
                )
            )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    fixture_paths = []
    for raw_path in args.fixture_paths or []:
        path = Path(raw_path)
        fixture_paths.append(path if path.is_absolute() else REPO_ROOT / path)
    if not fixture_paths:
        fixture_paths = list(DEFAULT_FIXTURES)

    records = [build_record(path.resolve()) for path in fixture_paths]
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "fixtures": [record["fixture"] for record in records],
        "records": records,
    }

    output_root = Path(args.output_dir).resolve()
    write_json(output_root / "real_world_baseline_summary.json", summary)
    write_markdown(output_root / "README.md", records)


if __name__ == "__main__":
    main()
