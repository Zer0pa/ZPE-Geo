"""Maneuver detection primitives for trajectory token streams."""

from __future__ import annotations

import math
from collections import Counter
from typing import Any


def _dir_idx(dx: float, dy: float) -> int:
    if dx == 0.0 and dy == 0.0:
        return 0
    bearing = (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0
    return int(((bearing + 22.5) // 45.0) % 8)


def direction_sequence(trajectory: dict[str, Any]) -> list[int]:
    points = trajectory.get("points", [])
    if len(points) < 2:
        return []
    coord = trajectory.get("coord_system", "xy")
    out: list[int] = []
    if coord == "xy":
        for i in range(1, len(points)):
            dx = points[i]["x"] - points[i - 1]["x"]
            dy = points[i]["y"] - points[i - 1]["y"]
            out.append(_dir_idx(dx, dy))
    else:
        # WGS84 local approximation for directional classing.
        for i in range(1, len(points)):
            dx = (points[i]["lon"] - points[i - 1]["lon"]) * math.cos(
                math.radians(points[i - 1]["lat"])
            )
            dy = points[i]["lat"] - points[i - 1]["lat"]
            out.append(_dir_idx(dx, dy))
    return out


def _contains_ccw_quarter_turn(seq: list[int]) -> bool:
    for i in range(2, len(seq)):
        window = seq[i - 2 : i + 1]
        delta = (window[-1] - window[0]) % 8
        if 1 <= delta <= 3:
            return True
    return False


def _contains_lane_merge_pattern(seq: list[int]) -> bool:
    if len(seq) < 5:
        return False
    for i in range(2, len(seq) - 2):
        prev_dir = seq[i - 1]
        cur_dir = seq[i]
        nxt_dir = seq[i + 1]
        if prev_dir == nxt_dir and cur_dir != prev_dir:
            # lateral offset and return
            if (cur_dir - prev_dir) % 8 in (1, 7):
                return True
    return False


def _contains_stop(points: list[dict[str, float]]) -> bool:
    run = 0
    for i in range(1, len(points)):
        if "speed" in points[i]:
            speed = points[i]["speed"]
        else:
            speed = 0.0
        if speed <= 0.3:
            run += 1
        else:
            run = 0
        if run >= 3:
            return True
    return False


def detect_maneuvers(trajectory: dict[str, Any]) -> dict[str, float]:
    seq = direction_sequence(trajectory)
    points = trajectory.get("points", [])
    counts = Counter(seq)
    dominant_dir, dominant_count = (counts.most_common(1)[0] if counts else (0, 0))
    straightness = dominant_count / max(1, len(seq))

    scores = {
        "left_turn": 0.0,
        "lane_merge": 0.0,
        "stop": 0.0,
        "straight": straightness,
    }
    if _contains_ccw_quarter_turn(seq):
        scores["left_turn"] = 0.92
    if _contains_lane_merge_pattern(seq):
        scores["lane_merge"] = 0.94
    if _contains_stop(points):
        scores["stop"] = 0.98
    if straightness > 0.85 and all(scores[k] < 0.5 for k in ("left_turn", "lane_merge", "stop")):
        scores["straight"] = 0.97
    return scores
