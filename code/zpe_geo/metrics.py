"""Metric utilities for benchmarks and claims."""

from __future__ import annotations

import math
from typing import Iterable

from .geo import haversine_m


def compression_ratio(raw_bytes: int, encoded_bytes: int) -> float:
    if encoded_bytes <= 0:
        return float("inf")
    return raw_bytes / encoded_bytes


def rmse_xy_m(
    original_points: list[dict[str, float]], decoded_points: list[dict[str, float]]
) -> float:
    n = min(len(original_points), len(decoded_points))
    if n == 0:
        return float("inf")
    err_sum = 0.0
    for i in range(n):
        dx = original_points[i]["x"] - decoded_points[i]["x"]
        dy = original_points[i]["y"] - decoded_points[i]["y"]
        err_sum += dx * dx + dy * dy
    return math.sqrt(err_sum / n)


def mean(values: Iterable[float]) -> float:
    vals = list(values)
    if not vals:
        return float("nan")
    return sum(vals) / len(vals)


def percentile(values: list[float], p: float) -> float:
    if not values:
        return float("nan")
    if p <= 0:
        return min(values)
    if p >= 100:
        return max(values)
    vals = sorted(values)
    idx = (len(vals) - 1) * p / 100.0
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return vals[lo]
    frac = idx - lo
    return vals[lo] * (1.0 - frac) + vals[hi] * frac


def path_length_haversine_m(points: list[dict[str, float]]) -> float:
    total = 0.0
    for i in range(1, len(points)):
        a = points[i - 1]
        b = points[i]
        total += haversine_m(a["lat"], a["lon"], b["lat"], b["lon"])
    return total
