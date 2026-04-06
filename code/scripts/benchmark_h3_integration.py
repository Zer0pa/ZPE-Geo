#!/usr/bin/env python3
"""Benchmark the H3 integration surface against codec payloads."""

from __future__ import annotations

import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_benchmark import write_json
from zpe_geo.codec import encode_trajectory
from zpe_geo.h3bridge import H3Bridge
from zpe_geo.metrics import percentile
from zpe_geo.utils import ensure_dir

REPO_ROOT = ROOT.parent
FIXTURE_ROOT = ROOT / "fixtures" / "real_world"
ARTIFACT_ROOT = REPO_ROOT / "proofs" / "artifacts" / "h3_benchmarks"
FIXTURE_NAMES = (
    "noaa_ais_day_extract.json",
    "geolife_extract.json",
    "osm_monaco_way_extract.json",
)
RESOLUTIONS = (7, 9, 12)


def load_trajectories() -> list[dict[str, Any]]:
    trajectories: list[dict[str, Any]] = []
    for name in FIXTURE_NAMES:
        payload = json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))
        trajectories.extend(payload["trajectories"])
    return trajectories


def benchmark_resolution(resolution: int, trajectories: list[dict[str, Any]]) -> dict[str, Any]:
    bridge = H3Bridge(resolution=resolution)
    codec_sizes: list[int] = []
    h3_uint64_sizes: list[int] = []
    h3_string_sizes: list[int] = []
    h3_encode_us: list[float] = []
    query_us: list[float] = []
    cell_index: dict[str, set[str]] = {}
    per_trajectory: list[dict[str, Any]] = []

    for trajectory in trajectories:
        codec_payload = encode_trajectory(trajectory, quant_step_m=0.25).payload
        start = time.perf_counter_ns()
        cell_path = bridge.encode_cell_path(trajectory, resolution=resolution)
        stop = time.perf_counter_ns()

        codec_sizes.append(len(codec_payload))
        h3_uint64_sizes.append(len(cell_path) * 8)
        h3_string_sizes.append(sum(len(cell) for cell in cell_path))
        h3_encode_us.append((stop - start) / 1000.0)
        per_trajectory.append(
            {
                "trajectory_id": trajectory["trajectory_id"],
                "codec_payload_bytes": len(codec_payload),
                "h3_cell_count": len(cell_path),
                "raw_h3_uint64_bytes": len(cell_path) * 8,
                "raw_h3_string_bytes": sum(len(cell) for cell in cell_path),
            }
        )
        for cell in cell_path:
            cell_index.setdefault(cell, set()).add(trajectory["trajectory_id"])

    hit_cells = list(cell_index.keys())[: min(100, len(cell_index))]
    miss_cells: list[str] = []
    for trajectory in trajectories:
        point = trajectory["points"][-1]
        candidate = bridge.latlon_to_cell(point["lat"] + 0.3, point["lon"] + 0.3, resolution=resolution)
        if candidate not in cell_index:
            miss_cells.append(candidate)
        if len(miss_cells) >= len(hit_cells):
            break

    query_cells = hit_cells + miss_cells
    for cell in query_cells:
        start = time.perf_counter_ns()
        _ = cell_index.get(cell, set())
        stop = time.perf_counter_ns()
        query_us.append((stop - start) / 1000.0)

    codec_beats_h3 = sum(
        1 for codec_size, h3_size in zip(codec_sizes, h3_uint64_sizes, strict=True) if codec_size < h3_size
    )
    return {
        "resolution": resolution,
        "backend": bridge.backend,
        "trajectory_count": len(trajectories),
        "codec_payload_bytes_mean": statistics.mean(codec_sizes),
        "raw_h3_uint64_bytes_mean": statistics.mean(h3_uint64_sizes),
        "raw_h3_string_bytes_mean": statistics.mean(h3_string_sizes),
        "codec_smaller_than_raw_h3_uint64_count": codec_beats_h3,
        "h3_encode_time_us": {
            "mean": statistics.mean(h3_encode_us),
            "median": statistics.median(h3_encode_us),
            "p95": percentile(h3_encode_us, 95),
        },
        "hex_query_time_us": {
            "mean": statistics.mean(query_us) if query_us else 0.0,
            "median": statistics.median(query_us) if query_us else 0.0,
            "p95": percentile(query_us, 95) if query_us else 0.0,
        },
        "cell_index": {
            "distinct_cells": len(cell_index),
            "hit_queries": len(hit_cells),
            "miss_queries": len(miss_cells),
        },
        "per_trajectory": per_trajectory,
    }


def write_markdown(path: Path, results: list[dict[str, Any]]) -> None:
    lines = [
        "# H3 Integration Benchmarks",
        "",
        "| Resolution | Backend | Codec Bytes Mean | Raw H3 UInt64 Bytes Mean | H3 Encode Mean (us) | Hex Query Mean (us) |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        lines.append(
            "| {resolution} | {backend} | {codec:.1f} | {h3:.1f} | {encode:.1f} | {query:.3f} |".format(
                resolution=result["resolution"],
                backend=result["backend"],
                codec=result["codec_payload_bytes_mean"],
                h3=result["raw_h3_uint64_bytes_mean"],
                encode=result["h3_encode_time_us"]["mean"],
                query=result["hex_query_time_us"]["mean"],
            )
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dir(ARTIFACT_ROOT)
    trajectories = load_trajectories()
    results = [benchmark_resolution(resolution, trajectories) for resolution in RESOLUTIONS]
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "fixtures": list(FIXTURE_NAMES),
        "resolutions": results,
    }
    write_json(ARTIFACT_ROOT / "h3_integration_benchmark.json", payload)
    write_markdown(ARTIFACT_ROOT / "README.md", results)


if __name__ == "__main__":
    main()
