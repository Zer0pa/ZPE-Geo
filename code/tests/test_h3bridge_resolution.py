from __future__ import annotations

import math
import unittest

from zpe_geo.h3bridge import H3Bridge


class TestH3BridgeResolution(unittest.TestCase):
    def test_centroid_recell_stable_across_resolutions(self) -> None:
        bridge = H3Bridge(resolution=9)
        for resolution in range(16):
            with self.subTest(resolution=resolution):
                cell = bridge.latlon_to_cell(37.7749, -122.4194, resolution=resolution)
                lat, lon = bridge.cell_to_latlon(cell)
                self.assertEqual(bridge.latlon_to_cell(lat, lon, resolution=resolution), cell)

    def test_encode_cell_path_deduplicates_repeated_cells(self) -> None:
        bridge = H3Bridge(resolution=9)
        trajectory = {
            "coord_system": "wgs84",
            "points": [
                {"lat": 37.7749, "lon": -122.4194},
                {"lat": 37.77491, "lon": -122.41939},
                {"lat": 37.7800, "lon": -122.4100},
            ],
        }
        path = bridge.encode_cell_path(trajectory, resolution=9)
        self.assertLessEqual(len(path), len(trajectory["points"]))
        self.assertGreaterEqual(len(path), 2)

    def test_boundary_coordinates_produce_finite_roundtrip(self) -> None:
        bridge = H3Bridge(resolution=12)
        for lat, lon in ((89.999, 0.0), (-89.999, 179.999), (0.0, -179.999)):
            with self.subTest(lat=lat, lon=lon):
                cell = bridge.latlon_to_cell(lat, lon)
                roundtrip_lat, roundtrip_lon = bridge.cell_to_latlon(cell)
                self.assertTrue(math.isfinite(roundtrip_lat) and math.isfinite(roundtrip_lon))

    def test_encode_cell_path_requires_wgs84(self) -> None:
        bridge = H3Bridge(resolution=9)
        with self.assertRaises(ValueError):
            bridge.encode_cell_path({"coord_system": "xy", "points": [{"x": 0.0, "y": 0.0}]})


if __name__ == "__main__":
    unittest.main()
