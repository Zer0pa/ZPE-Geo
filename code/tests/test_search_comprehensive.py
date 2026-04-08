from __future__ import annotations

import unittest

from zpe_geo.search import ManeuverSearchIndex


def _xy_trajectory(trajectory_id: str, label: str, points: list[tuple[float, float]]) -> dict:
    return {
        "trajectory_id": trajectory_id,
        "coord_system": "xy",
        "label": label,
        "points": [
            {"t": float(index), "x": x, "y": y, "speed": 3.0, "cog": 90.0}
            for index, (x, y) in enumerate(points)
        ],
    }


def _wgs84_trajectory(trajectory_id: str, label: str, points: list[tuple[float, float]]) -> dict:
    return {
        "trajectory_id": trajectory_id,
        "coord_system": "wgs84",
        "label": label,
        "points": [
            {"t": float(index), "lat": lat, "lon": lon, "speed": 3.0, "cog": 45.0}
            for index, (lat, lon) in enumerate(points)
        ],
    }


class TestSearchComprehensive(unittest.TestCase):
    def setUp(self) -> None:
        self.xy_a = _xy_trajectory("xy_a", "straight", [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)])
        self.xy_b = _xy_trajectory("xy_b", "straight", [(2.0, 0.0), (2.5, 0.5), (3.0, 1.0)])
        self.xy_c = _xy_trajectory("xy_c", "straight", [(10.0, 10.0), (11.0, 11.0), (12.0, 12.0)])
        self.wgs_a = _wgs84_trajectory(
            "wgs_a",
            "straight",
            [(37.7749, -122.4194), (37.7750, -122.4190), (37.7751, -122.4185)],
        )
        self.wgs_b = _wgs84_trajectory(
            "wgs_b",
            "straight",
            [(37.7800, -122.4200), (37.7801, -122.4198), (37.7802, -122.4196)],
        )
        self.index = ManeuverSearchIndex(seed=7)
        self.index.build([self.xy_a, self.xy_b, self.xy_c, self.wgs_a, self.wgs_b])

    def test_bbox_query_returns_expected_xy_trajectories(self) -> None:
        matches = self.index.query_bbox(0.0, 0.0, 2.1, 2.1, coord_system="xy")
        self.assertEqual([match.trajectory_id for match in matches], ["xy_a", "xy_b"])

    def test_bbox_query_returns_expected_single_subset_match(self) -> None:
        matches = self.index.query_bbox(1.5, -0.1, 3.1, 1.1, coord_system="xy")
        self.assertEqual([match.trajectory_id for match in matches], ["xy_b"])

    def test_bbox_query_empty_result(self) -> None:
        matches = self.index.query_bbox(-5.0, -5.0, -1.0, -1.0, coord_system="xy")
        self.assertEqual(matches, [])

    def test_bbox_query_includes_edge_boundary(self) -> None:
        matches = self.index.query_bbox(2.0, 2.0, 2.0, 2.0, coord_system="xy")
        self.assertEqual([match.trajectory_id for match in matches], ["xy_a"])

    def test_radius_query_returns_expected_wgs84_match(self) -> None:
        matches = self.index.query_radius(37.7749, -122.4194, 60.0, coord_system="wgs84")
        self.assertEqual([match.trajectory_id for match in matches], ["wgs_a"])

    def test_radius_query_orders_by_distance(self) -> None:
        matches = self.index.query_radius(37.7765, -122.4195, 700.0, coord_system="wgs84")
        self.assertEqual([match.trajectory_id for match in matches], ["wgs_a", "wgs_b"])

    def test_bbox_query_ignores_empty_trajectories(self) -> None:
        self.index.build(
            [
                self.xy_a,
                {"trajectory_id": "empty_xy", "coord_system": "xy", "label": "straight", "points": []},
            ]
        )
        matches = self.index.query_bbox(0.0, 0.0, 2.1, 2.1, coord_system="xy")
        self.assertEqual([match.trajectory_id for match in matches], ["xy_a"])

    def test_radius_query_ignores_empty_trajectories(self) -> None:
        self.index.build(
            [
                self.wgs_a,
                {"trajectory_id": "empty_wgs", "coord_system": "wgs84", "label": "straight", "points": []},
            ]
        )
        matches = self.index.query_radius(37.7749, -122.4194, 60.0, coord_system="wgs84")
        self.assertEqual([match.trajectory_id for match in matches], ["wgs_a"])


if __name__ == "__main__":
    unittest.main()
