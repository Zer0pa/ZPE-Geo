"""Geospatial math helpers (stdlib only)."""

from __future__ import annotations

import math

EARTH_RADIUS_M = 6371008.8


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in meters."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    )
    return 2.0 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def latlon_to_local_xy_m(
    lat: float, lon: float, origin_lat: float, origin_lon: float
) -> tuple[float, float]:
    """Project WGS84 lat/lon to local tangent plane (east, north) in meters."""
    d_lat = math.radians(lat - origin_lat)
    d_lon = math.radians(lon - origin_lon)
    origin_lat_rad = math.radians(origin_lat)
    north = d_lat * EARTH_RADIUS_M
    east = d_lon * EARTH_RADIUS_M * math.cos(origin_lat_rad)
    return east, north


def local_xy_to_latlon_m(
    east: float, north: float, origin_lat: float, origin_lon: float
) -> tuple[float, float]:
    """Inverse tangent-plane projection."""
    d_lat = north / EARTH_RADIUS_M
    origin_lat_rad = math.radians(origin_lat)
    cos_lat = max(1e-12, math.cos(origin_lat_rad))
    d_lon = east / (EARTH_RADIUS_M * cos_lat)
    lat = origin_lat + math.degrees(d_lat)
    lon = origin_lon + math.degrees(d_lon)
    return lat, lon


def dtw_distance_m(
    seq_a: list[tuple[float, float]], seq_b: list[tuple[float, float]]
) -> float:
    """DTW distance using haversine over two lat/lon sequences."""
    if not seq_a or not seq_b:
        return float("inf")
    n = len(seq_a)
    m = len(seq_b)
    prev = [float("inf")] * (m + 1)
    curr = [float("inf")] * (m + 1)
    prev[0] = 0.0
    for i in range(1, n + 1):
        curr[0] = float("inf")
        a_lat, a_lon = seq_a[i - 1]
        for j in range(1, m + 1):
            b_lat, b_lon = seq_b[j - 1]
            cost = haversine_m(a_lat, a_lon, b_lat, b_lon)
            curr[j] = cost + min(curr[j - 1], prev[j], prev[j - 1])
        prev, curr = curr, prev
    path_len = n + m
    return prev[m] / max(1, path_len)
