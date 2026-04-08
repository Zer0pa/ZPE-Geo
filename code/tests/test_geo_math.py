from __future__ import annotations

import unittest

from zpe_geo.geo import dtw_distance_m, haversine_m, latlon_to_local_xy_m, local_xy_to_latlon_m


class TestGeoMath(unittest.TestCase):
    def test_local_xy_roundtrip_stays_close(self) -> None:
        east, north = latlon_to_local_xy_m(43.7390, 7.4258, 43.7384, 7.4246)
        lat, lon = local_xy_to_latlon_m(east, north, 43.7384, 7.4246)
        self.assertAlmostEqual(lat, 43.7390, places=6)
        self.assertAlmostEqual(lon, 7.4258, places=6)

    def test_haversine_zero_distance(self) -> None:
        self.assertEqual(haversine_m(43.0, 7.0, 43.0, 7.0), 0.0)

    def test_dtw_empty_sequence_returns_inf(self) -> None:
        self.assertEqual(dtw_distance_m([], [(43.0, 7.0)]), float("inf"))

    def test_dtw_identical_sequences_small(self) -> None:
        seq = [(43.7384, 7.4246), (43.7386, 7.4250), (43.7388, 7.4254)]
        self.assertLessEqual(dtw_distance_m(seq, seq), 1e-9)


if __name__ == "__main__":
    unittest.main()
