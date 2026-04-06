from __future__ import annotations

import math
import unittest

from zpe_geo.codec import decode_trajectory, encode_trajectory


def _xy_trajectory(points: list[tuple[float, float]]) -> dict:
    return {
        "trajectory_id": "xy_edge",
        "coord_system": "xy",
        "points": [
            {"t": float(index), "x": x, "y": y, "speed": 1.0, "cog": 0.0}
            for index, (x, y) in enumerate(points)
        ],
    }


def _wgs84_trajectory(points: list[tuple[float, float]]) -> dict:
    return {
        "trajectory_id": "wgs_edge",
        "coord_system": "wgs84",
        "points": [
            {"t": float(index), "lat": lat, "lon": lon, "speed": 1.0, "cog": 45.0}
            for index, (lat, lon) in enumerate(points)
        ],
    }


class TestEdgeCases(unittest.TestCase):
    def test_empty_points_rejected(self) -> None:
        with self.assertRaises(ValueError):
            encode_trajectory({"trajectory_id": "empty", "coord_system": "xy", "points": []})

    def test_single_point_rejected(self) -> None:
        with self.assertRaises(ValueError):
            encode_trajectory(
                {
                    "trajectory_id": "single",
                    "coord_system": "xy",
                    "points": [{"t": 0.0, "x": 0.0, "y": 0.0, "speed": 0.0, "cog": 0.0}],
                }
            )

    def test_zero_zero_wgs84_roundtrip_keeps_length(self) -> None:
        trajectory = _wgs84_trajectory([(0.0, 0.0), (0.0002, 0.0002), (0.0004, 0.0004)])
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertEqual(len(decoded["points"]), 3)

    def test_max_precision_xy_roundtrip_keeps_length(self) -> None:
        trajectory = _xy_trajectory(
            [
                (0.123456789, -0.987654321),
                (1.123456789, -0.487654321),
                (2.123456789, 0.012345679),
            ]
        )
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.05).payload)
        self.assertEqual(len(decoded["points"]), 3)

    def test_antimeridian_roundtrip_keeps_finite_coordinates(self) -> None:
        trajectory = _wgs84_trajectory([(10.0, 179.9), (10.05, 179.95), (10.1, 179.99)])
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertTrue(all(math.isfinite(point["lat"]) and math.isfinite(point["lon"]) for point in decoded["points"]))

    def test_polar_roundtrip_keeps_finite_coordinates(self) -> None:
        trajectory = _wgs84_trajectory([(89.8, 0.0), (89.81, 0.1), (89.82, 0.2)])
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertTrue(all(math.isfinite(point["lat"]) and math.isfinite(point["lon"]) for point in decoded["points"]))


if __name__ == "__main__":
    unittest.main()
