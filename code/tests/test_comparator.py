from __future__ import annotations

import unittest

from zpe_geo.comparator import encoded_size_dp_bytes, simplify_douglas_peucker


class TestComparator(unittest.TestCase):
    def test_simplify_xy_reduces_points(self) -> None:
        trajectory = {
            "trajectory_id": "xy_demo",
            "coord_system": "xy",
            "points": [
                {"x": 0.0, "y": 0.0},
                {"x": 1.0, "y": 0.1},
                {"x": 2.0, "y": 0.0},
                {"x": 3.0, "y": 0.1},
                {"x": 4.0, "y": 0.0},
            ],
        }
        simplified = simplify_douglas_peucker(trajectory, epsilon_m=0.5)
        self.assertEqual(simplified["coord_system"], "xy")
        self.assertLess(len(simplified["points"]), len(trajectory["points"]))
        self.assertGreater(encoded_size_dp_bytes(simplified), 0)

    def test_simplify_wgs84_preserves_endpoints(self) -> None:
        trajectory = {
            "trajectory_id": "wgs_demo",
            "coord_system": "wgs84",
            "points": [
                {"lat": 43.7384, "lon": 7.4246},
                {"lat": 43.7386, "lon": 7.4250},
                {"lat": 43.7388, "lon": 7.4254},
                {"lat": 43.7390, "lon": 7.4258},
            ],
        }
        simplified = simplify_douglas_peucker(trajectory, epsilon_m=5.0)
        self.assertEqual(simplified["coord_system"], "wgs84")
        self.assertEqual(simplified["points"][0]["lat"], trajectory["points"][0]["lat"])
        self.assertEqual(simplified["points"][-1]["lon"], trajectory["points"][-1]["lon"])


if __name__ == "__main__":
    unittest.main()
