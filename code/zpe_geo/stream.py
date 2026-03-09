"""Streaming encode utilities for AIS-like updates."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .codec import encode_trajectory


@dataclass
class StreamState:
    points_by_vessel: dict[int, list[dict[str, Any]]] = field(default_factory=dict)
    encoded_updates: int = 0


def encode_ais_update(state: StreamState, update: dict[str, Any]) -> tuple[int, float]:
    """Encode one AIS update in an online fashion; returns payload size and latency ms."""
    t0 = time.perf_counter()
    mmsi = int(update["mmsi"])
    points = state.points_by_vessel.setdefault(mmsi, [])
    points.append(
        {
            "t": float(update["t"]),
            "lat": float(update["lat"]),
            "lon": float(update["lon"]),
            "speed": float(update.get("speed", 0.0)),
            "cog": float(update.get("cog", 511.0)),
        }
    )
    if len(points) < 2:
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return 0, latency_ms
    traj = {
        "trajectory_id": f"stream_{mmsi}",
        "coord_system": "wgs84",
        "points": points[-32:],
    }
    encoded = encode_trajectory(traj)
    state.encoded_updates += 1
    latency_ms = (time.perf_counter() - t0) * 1000.0
    return len(encoded.payload), latency_ms
