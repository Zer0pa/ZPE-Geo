"""Deterministic dataset fixtures and corpus simulators."""

from __future__ import annotations

import csv
import datetime as dt
import io
import math
import random
from dataclasses import dataclass
from typing import Any

from .geo import local_xy_to_latlon_m


@dataclass(frozen=True)
class DatasetBundle:
    name: str
    seed: int
    trajectories: list[dict[str, Any]]
    metadata: dict[str, Any]


def _bearing_from_dir(dx: float, dy: float) -> float:
    if dx == 0.0 and dy == 0.0:
        return 0.0
    return (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0


def _build_xy_points(
    start_x: float,
    start_y: float,
    dt_s: float,
    segments: list[tuple[float, float, int]],
    speed_mps: float,
    include_stops: bool = False,
) -> list[dict[str, float]]:
    points: list[dict[str, float]] = [{"t": 0.0, "x": start_x, "y": start_y, "speed": speed_mps, "cog": 0.0}]
    t = 0.0
    x = start_x
    y = start_y
    for dx_step, dy_step, n_steps in segments:
        for _ in range(n_steps):
            t += dt_s
            x += dx_step
            y += dy_step
            cog = _bearing_from_dir(dx_step, dy_step)
            speed = speed_mps
            if include_stops and dx_step == 0.0 and dy_step == 0.0:
                speed = 0.0
                cog = 511.0
            points.append({"t": t, "x": x, "y": y, "speed": speed, "cog": cog})
    return points


def _av_template(label: str, rng: random.Random) -> list[tuple[float, float, int]]:
    # Keep long straight runs to reflect highway/arterial structure and challenge
    # codec on selected bursty segments.
    base = 1.8 + 0.2 * rng.random()
    diag = base / math.sqrt(2.0)
    if label == "left_turn":
        return [(base, 0.0, 80), (diag, diag, 18), (0.0, base, 70)]
    if label == "lane_merge":
        return [(0.0, base, 40), (diag, diag, 8), (0.0, base, 35), (-diag, diag, 8), (0.0, base, 40)]
    if label == "stop":
        return [(0.0, base, 50), (0.0, 0.0, 12), (0.0, base, 50)]
    if label == "zigzag":
        return [(base, 0.0, 10), (-base, 0.0, 10)] * 8 + [(0.0, base, 40)]
    return [(0.0, base, 150)]


def generate_av_suite(seed: int, n_per_class: int = 40) -> DatasetBundle:
    rng = random.Random(seed)
    labels = ["left_turn", "lane_merge", "stop", "straight", "zigzag"]
    trajectories: list[dict[str, Any]] = []
    traj_id = 0
    for label in labels:
        for _ in range(n_per_class):
            traj_id += 1
            start_x = rng.uniform(-20.0, 20.0)
            start_y = rng.uniform(-20.0, 20.0)
            speed = rng.uniform(8.0, 17.0)
            points = _build_xy_points(
                start_x=start_x,
                start_y=start_y,
                dt_s=0.1,
                segments=_av_template(label, rng),
                speed_mps=speed,
                include_stops=(label == "stop"),
            )
            trajectories.append(
                {
                    "trajectory_id": f"av_{traj_id:05d}",
                    "domain": "av",
                    "coord_system": "xy",
                    "label": label,
                    "sample_rate_hz": 10,
                    "points": points,
                }
            )
    return DatasetBundle(
        name="argoverse2_schema_faithful_fixture_v1",
        seed=seed,
        trajectories=trajectories,
        metadata={
            "reference": "Argoverse2 schema-faithful synthetic (local fixture)",
            "sample_rate_hz": 10,
            "classes": labels,
            "count": len(trajectories),
        },
    )


def _ais_segments(label: str, rng: random.Random) -> list[tuple[float, float, int]]:
    base = 16.0 + 2.0 * rng.random()
    diag = base / math.sqrt(2.0)
    if label == "left_turn":
        return [(base, 0.0, 240), (diag, diag, 30), (0.0, base, 220)]
    if label == "lane_merge":
        return [(0.0, base, 150), (diag, diag, 22), (0.0, base, 130), (-diag, diag, 22), (0.0, base, 140)]
    if label == "stop":
        return [(base, 0.0, 100), (0.0, 0.0, 25), (base, 0.0, 100)]
    if label == "harbour":
        return [(base, 0.0, 55), (diag, diag, 12), (0.0, base, 55), (-diag, diag, 12), (-base, 0.0, 55)]
    return [(base, 0.0, 520)]


def generate_ais_suite(seed: int, n_per_class: int = 35) -> DatasetBundle:
    rng = random.Random(seed)
    labels = ["left_turn", "lane_merge", "stop", "straight", "harbour"]
    trajectories: list[dict[str, Any]] = []
    traj_id = 0
    for label in labels:
        for _ in range(n_per_class):
            traj_id += 1
            mmsi = 300_000_000 + traj_id
            # Gulf-like origin for realistic lat/lon ranges.
            origin_lat = 29.0 + rng.uniform(-1.2, 1.2)
            origin_lon = -94.0 + rng.uniform(-1.5, 1.5)
            points_xy = _build_xy_points(
                start_x=0.0,
                start_y=0.0,
                dt_s=10.0,
                segments=_ais_segments(label, rng),
                speed_mps=rng.uniform(3.0, 12.0),
                include_stops=(label == "stop"),
            )
            start = dt.datetime(2025, 7, 1, 0, 0, 0)
            points: list[dict[str, Any]] = []
            for idx, p in enumerate(points_xy):
                ts = start + dt.timedelta(seconds=10 * idx)
                lat, lon = local_xy_to_latlon_m(p["x"], p["y"], origin_lat, origin_lon)
                cog = float(p["cog"])
                if label in {"stop", "harbour"} and rng.random() < 0.08:
                    cog = 511.0  # NOAA invalid COG sentinel
                points.append(
                    {
                        "t": ts.timestamp(),
                        "lat": lat,
                        "lon": lon,
                        "speed": p["speed"],
                        "cog": cog,
                        "timestamp_iso": ts.isoformat(),
                        "mmsi": mmsi,
                    }
                )
            trajectories.append(
                {
                    "trajectory_id": f"ais_{traj_id:05d}",
                    "domain": "ais",
                    "coord_system": "wgs84",
                    "label": label,
                    "sample_rate_hz": 0.1,
                    "points": points,
                }
            )
    return DatasetBundle(
        name="noaa_ais_schema_faithful_fixture_v1",
        seed=seed,
        trajectories=trajectories,
        metadata={
            "reference": "NOAA AIS schema-faithful synthetic (local fixture)",
            "sample_interval_s": 10,
            "classes": labels,
            "count": len(trajectories),
        },
    )


def estimate_raw_av_bytes(trajectory: dict[str, Any]) -> int:
    # float64 x/y + heading + vx + vy + timestamp
    point_bytes = 8 * 6
    return len(trajectory["points"]) * point_bytes


def estimate_raw_ais_nmea_bytes(trajectory: dict[str, Any]) -> int:
    # Approximate raw NMEA/CSV payload by serializing NOAA-like rows.
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["MMSI", "BaseDateTime", "LAT", "LON", "SOG", "COG", "Heading"])
    for p in trajectory["points"]:
        writer.writerow(
            [
                p["mmsi"],
                p["timestamp_iso"],
                f"{p['lat']:.6f}",
                f"{p['lon']:.6f}",
                f"{p['speed']:.2f}",
                f"{p['cog']:.1f}",
                int(round(p["cog"])) if p["cog"] != 511.0 else 511,
            ]
        )
    return len(out.getvalue().encode("utf-8"))


def simulate_trajectory_corpus_size(indexed_count: int, target_count: int = 10_000_000) -> dict[str, int]:
    """Map a built index to a large simulated corpus for latency scaling checks."""
    if indexed_count <= 0:
        raise ValueError("indexed_count must be positive")
    replication_factor = (target_count + indexed_count - 1) // indexed_count
    return {
        "indexed_count": indexed_count,
        "target_count": target_count,
        "replication_factor": replication_factor,
        "simulated_total": indexed_count * replication_factor,
    }
