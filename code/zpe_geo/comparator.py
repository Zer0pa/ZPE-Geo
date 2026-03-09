"""Comparator baselines (Douglas-Peucker)."""

from __future__ import annotations

import math
from typing import Any

from .geo import latlon_to_local_xy_m, local_xy_to_latlon_m


def _perp_distance(p: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
    if a == b:
        dx = p[0] - a[0]
        dy = p[1] - a[1]
        return math.sqrt(dx * dx + dy * dy)
    num = abs((b[1] - a[1]) * p[0] - (b[0] - a[0]) * p[1] + b[0] * a[1] - b[1] * a[0])
    den = math.sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)
    return num / den


def _rdp(points: list[tuple[float, float]], epsilon: float) -> list[tuple[float, float]]:
    if len(points) < 3:
        return points[:]
    start = points[0]
    end = points[-1]
    max_dist = -1.0
    max_idx = -1
    for i in range(1, len(points) - 1):
        d = _perp_distance(points[i], start, end)
        if d > max_dist:
            max_dist = d
            max_idx = i
    if max_dist > epsilon:
        left = _rdp(points[: max_idx + 1], epsilon)
        right = _rdp(points[max_idx:], epsilon)
        return left[:-1] + right
    return [start, end]


def simplify_douglas_peucker(
    trajectory: dict[str, Any], epsilon_m: float = 12.0
) -> dict[str, Any]:
    points = trajectory["points"]
    coord = trajectory.get("coord_system", "xy")
    if coord == "xy":
        xy_points = [(p["x"], p["y"]) for p in points]
        simplified = _rdp(xy_points, epsilon_m)
        return {
            "trajectory_id": trajectory["trajectory_id"],
            "coord_system": "xy",
            "points": [{"x": x, "y": y} for x, y in simplified],
        }
    origin_lat = points[0]["lat"]
    origin_lon = points[0]["lon"]
    xy_points = [
        latlon_to_local_xy_m(p["lat"], p["lon"], origin_lat, origin_lon) for p in points
    ]
    simplified = _rdp(xy_points, epsilon_m)
    return {
        "trajectory_id": trajectory["trajectory_id"],
        "coord_system": "wgs84",
        "points": [
            {
                "lat": local_xy_to_latlon_m(x, y, origin_lat, origin_lon)[0],
                "lon": local_xy_to_latlon_m(x, y, origin_lat, origin_lon)[1],
            }
            for x, y in simplified
        ],
    }


def encoded_size_dp_bytes(simplified_trajectory: dict[str, Any]) -> int:
    # Assume standard float64 coordinate tuple representation.
    coord = simplified_trajectory.get("coord_system", "xy")
    if coord == "xy":
        per_point = 16
    else:
        per_point = 16
    return len(simplified_trajectory["points"]) * per_point + 24
