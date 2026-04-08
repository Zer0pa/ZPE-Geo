from __future__ import annotations

import math
import unittest

from zpe_geo.metrics import compression_ratio, mean, path_length_haversine_m, percentile, rmse_xy_m


class TestMetrics(unittest.TestCase):
    def test_compression_ratio_handles_zero_encoded_bytes(self) -> None:
        self.assertEqual(compression_ratio(100, 0), float("inf"))
        self.assertEqual(compression_ratio(100, 25), 4.0)

    def test_rmse_xy_empty_points_returns_inf(self) -> None:
        self.assertEqual(rmse_xy_m([], []), float("inf"))

    def test_rmse_xy_matches_expected(self) -> None:
        original = [{"x": 0.0, "y": 0.0}, {"x": 2.0, "y": 0.0}]
        decoded = [{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 0.0}]
        self.assertAlmostEqual(rmse_xy_m(original, decoded), 1.0)

    def test_mean_handles_empty_values(self) -> None:
        self.assertTrue(math.isnan(mean([])))
        self.assertEqual(mean([1.0, 2.0, 3.0]), 2.0)

    def test_percentile_boundaries_and_interpolation(self) -> None:
        values = [1.0, 2.0, 3.0, 4.0]
        self.assertTrue(math.isnan(percentile([], 50)))
        self.assertEqual(percentile(values, 0), 1.0)
        self.assertEqual(percentile(values, 100), 4.0)
        self.assertEqual(percentile(values, 50), 2.5)

    def test_path_length_haversine_positive(self) -> None:
        points = [
            {"lat": 43.7384, "lon": 7.4246},
            {"lat": 43.7386, "lon": 7.4250},
            {"lat": 43.7388, "lon": 7.4254},
        ]
        self.assertGreater(path_length_haversine_m(points), 0.0)


if __name__ == "__main__":
    unittest.main()
