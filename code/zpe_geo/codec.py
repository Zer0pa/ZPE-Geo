"""Wave-1 trajectory encoder/decoder for .zpgeo payloads."""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass
from typing import Any

from .constants import DEFAULT_QUANT_STEP_M, DEFAULT_SAMPLE_DT_MS, DIR_VECTORS, MAGIC, VERSION
from .geo import latlon_to_local_xy_m, local_xy_to_latlon_m


@dataclass(frozen=True)
class EncodedTrajectory:
    payload: bytes
    metadata: dict[str, Any]


def _encode_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("varint must be non-negative")
    out = bytearray()
    while True:
        part = value & 0x7F
        value >>= 7
        if value:
            out.append(part | 0x80)
        else:
            out.append(part)
            break
    return bytes(out)


def _decode_varint(buf: bytes, offset: int) -> tuple[int, int]:
    shift = 0
    value = 0
    while True:
        if offset >= len(buf):
            raise ValueError("truncated varint")
        byte = buf[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return value, offset
        shift += 7
        if shift > 35:
            raise ValueError("varint overflow")


def _is_valid_cog(cog: Any) -> bool:
    if cog is None:
        return False
    try:
        v = float(cog)
    except (TypeError, ValueError):
        return False
    return 0.0 <= v < 360.0


def _direction_from_dxdy(dx: float, dy: float) -> int:
    if dx == 0.0 and dy == 0.0:
        return 0
    bearing = (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0
    return int(((bearing + 22.5) // 45.0) % 8)


def _direction_from_cog(cog: float) -> int:
    return int(((cog + 22.5) // 45.0) % 8)


def _normalize_points(trajectory: dict[str, Any]) -> tuple[list[dict[str, float]], dict[str, float]]:
    points = trajectory.get("points") or []
    if len(points) < 2:
        raise ValueError("trajectory requires at least two points")
    coord_system = trajectory.get("coord_system", "xy")
    norm: list[dict[str, float]] = []
    origin_meta: dict[str, float] = {}

    if coord_system == "wgs84":
        origin_lat = float(points[0]["lat"])
        origin_lon = float(points[0]["lon"])
        origin_meta = {"origin_lat": origin_lat, "origin_lon": origin_lon}
        for p in points:
            lat = float(p["lat"])
            lon = float(p["lon"])
            east, north = latlon_to_local_xy_m(lat, lon, origin_lat, origin_lon)
            norm.append(
                {
                    "t": float(p.get("t", len(norm))),
                    "x": east,
                    "y": north,
                    "speed": float(p.get("speed", 0.0)),
                    "cog": float(p["cog"]) if _is_valid_cog(p.get("cog")) else float("nan"),
                }
            )
    else:
        origin_x = float(points[0]["x"])
        origin_y = float(points[0]["y"])
        origin_meta = {"origin_x": origin_x, "origin_y": origin_y}
        for p in points:
            norm.append(
                {
                    "t": float(p.get("t", len(norm))),
                    "x": float(p["x"]) - origin_x,
                    "y": float(p["y"]) - origin_y,
                    "speed": float(p.get("speed", 0.0)),
                    "cog": float(p["cog"]) if _is_valid_cog(p.get("cog")) else float("nan"),
                }
            )
    return norm, origin_meta


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    mid = len(s) // 2
    if len(s) % 2 == 1:
        return s[mid]
    return 0.5 * (s[mid - 1] + s[mid])


def encode_trajectory(
    trajectory: dict[str, Any],
    quant_step_m: float = DEFAULT_QUANT_STEP_M,
    mag_tolerance_q: int = 1,
) -> EncodedTrajectory:
    """Encode trajectory to .zpgeo payload."""
    if quant_step_m <= 0.0:
        raise ValueError("quant_step_m must be > 0")
    points, origin_meta = _normalize_points(trajectory)
    coord_system = trajectory.get("coord_system", "xy")

    dts_ms: list[float] = []
    steps: list[tuple[int, int, int]] = []  # dir_idx, mag_q, speed_bin
    for i in range(1, len(points)):
        a = points[i - 1]
        b = points[i]
        dx = b["x"] - a["x"]
        dy = b["y"] - a["y"]
        dt = b["t"] - a["t"]
        if dt > 0:
            dts_ms.append(dt * 1000.0)
        dist = math.sqrt(dx * dx + dy * dy)
        if _is_valid_cog(b.get("cog")):
            dir_idx = _direction_from_cog(float(b["cog"]))
        else:
            dir_idx = _direction_from_dxdy(dx, dy)
        mag_q = max(0, int(round(dist / quant_step_m)))
        speed = b["speed"] if b["speed"] > 0.0 else (dist / dt if dt > 0 else 0.0)
        speed_bin = max(0, min(15, int(round(speed / 2.0))))
        steps.append((dir_idx, mag_q, speed_bin))

    sample_dt_ms = int(round(_median(dts_ms))) if dts_ms else DEFAULT_SAMPLE_DT_MS
    sample_dt_ms = max(1, min(65535, sample_dt_ms))

    # Run-length groups: keep runs only when direction and speed_bin are stable and
    # magnitude quantization stays near the running average.
    runs: list[tuple[int, int, int, int]] = []  # dir, count, avg_mag_q, speed_bin
    cur_dir, cur_mag_q, cur_speed = steps[0]
    cur_count = 1
    cur_sum_mag = cur_mag_q
    for dir_idx, mag_q, speed_bin in steps[1:]:
        cur_avg = int(round(cur_sum_mag / cur_count))
        if (
            dir_idx == cur_dir
            and speed_bin == cur_speed
            and abs(mag_q - cur_avg) <= mag_tolerance_q
        ):
            cur_count += 1
            cur_sum_mag += mag_q
        else:
            runs.append((cur_dir, cur_count, int(round(cur_sum_mag / cur_count)), cur_speed))
            cur_dir = dir_idx
            cur_count = 1
            cur_sum_mag = mag_q
            cur_speed = speed_bin
    runs.append((cur_dir, cur_count, int(round(cur_sum_mag / cur_count)), cur_speed))

    payload = bytearray()
    payload.extend(MAGIC)
    payload.extend(struct.pack("<B", VERSION))
    coord_flag = 1 if coord_system == "wgs84" else 0
    payload.extend(struct.pack("<B", coord_flag))
    quant_cm = max(1, int(round(quant_step_m * 100.0)))
    payload.extend(struct.pack("<H", quant_cm))
    payload.extend(struct.pack("<d", points[0]["t"]))
    payload.extend(struct.pack("<H", sample_dt_ms))
    payload.extend(struct.pack("<I", len(steps)))
    payload.extend(struct.pack("<I", len(runs)))
    if coord_flag:
        payload.extend(struct.pack("<dd", origin_meta["origin_lat"], origin_meta["origin_lon"]))
    else:
        payload.extend(struct.pack("<dd", origin_meta["origin_x"], origin_meta["origin_y"]))
    for dir_idx, count, mag_q, speed_bin in runs:
        packed = (speed_bin << 3) | dir_idx
        payload.extend(struct.pack("<B", packed))
        payload.extend(_encode_varint(count))
        payload.extend(_encode_varint(mag_q))

    metadata = {
        "trajectory_id": trajectory.get("trajectory_id", ""),
        "coord_system": coord_system,
        "point_count": len(points),
        "step_count": len(steps),
        "run_count": len(runs),
        "quant_step_m": quant_step_m,
        "sample_dt_ms": sample_dt_ms,
    }
    return EncodedTrajectory(payload=bytes(payload), metadata=metadata)


def decode_trajectory(payload: bytes) -> dict[str, Any]:
    """Decode .zpgeo payload to trajectory dictionary."""
    offset = 0
    if len(payload) < len(MAGIC) + 1:
        raise ValueError("payload too short")
    if payload[: len(MAGIC)] != MAGIC:
        raise ValueError("invalid magic")
    offset += len(MAGIC)

    version = payload[offset]
    offset += 1
    if version != VERSION:
        raise ValueError(f"unsupported version {version}")
    coord_flag = payload[offset]
    offset += 1
    quant_cm = struct.unpack_from("<H", payload, offset)[0]
    offset += 2
    quant_step_m = quant_cm / 100.0
    start_t = struct.unpack_from("<d", payload, offset)[0]
    offset += 8
    sample_dt_ms = struct.unpack_from("<H", payload, offset)[0]
    offset += 2
    step_count = struct.unpack_from("<I", payload, offset)[0]
    offset += 4
    run_count = struct.unpack_from("<I", payload, offset)[0]
    offset += 4
    origin_a, origin_b = struct.unpack_from("<dd", payload, offset)
    offset += 16

    points_xy = [{"t": start_t, "x": 0.0, "y": 0.0, "speed": 0.0}]
    for _ in range(run_count):
        if offset >= len(payload):
            raise ValueError("truncated run payload")
        packed = payload[offset]
        offset += 1
        dir_idx = packed & 0x07
        speed_bin = (packed >> 3) & 0x0F
        count, offset = _decode_varint(payload, offset)
        mag_q, offset = _decode_varint(payload, offset)
        mag_m = mag_q * quant_step_m
        vx, vy = DIR_VECTORS[dir_idx]
        for _step in range(count):
            prev = points_xy[-1]
            points_xy.append(
                {
                    "t": prev["t"] + (sample_dt_ms / 1000.0),
                    "x": prev["x"] + vx * mag_m,
                    "y": prev["y"] + vy * mag_m,
                    "speed": speed_bin * 2.0,
                }
            )
    if len(points_xy) != step_count + 1:
        raise ValueError("decoded step count mismatch")

    coord_system = "wgs84" if coord_flag else "xy"
    if coord_system == "wgs84":
        out_points: list[dict[str, float]] = []
        for p in points_xy:
            lat, lon = local_xy_to_latlon_m(p["x"], p["y"], origin_a, origin_b)
            out_points.append({"t": p["t"], "lat": lat, "lon": lon, "speed": p["speed"]})
    else:
        out_points = []
        for p in points_xy:
            out_points.append(
                {
                    "t": p["t"],
                    "x": p["x"] + origin_a,
                    "y": p["y"] + origin_b,
                    "speed": p["speed"],
                }
            )
    return {
        "coord_system": coord_system,
        "points": out_points,
        "sample_dt_ms": sample_dt_ms,
        "quant_step_m": quant_step_m,
    }


def encoded_size_bytes(trajectory: dict[str, Any], quant_step_m: float = DEFAULT_QUANT_STEP_M) -> int:
    return len(encode_trajectory(trajectory, quant_step_m=quant_step_m).payload)
