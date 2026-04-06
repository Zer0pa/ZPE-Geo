from __future__ import annotations

import json
import unittest
from pathlib import Path

from zpe_geo.codec import decode_trajectory, encode_trajectory
from zpe_geo.geo import haversine_m


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"


def _load_first_trajectory(*parts: str) -> dict:
    payload = json.loads((FIXTURE_ROOT.joinpath(*parts)).read_text(encoding="utf-8"))
    return payload["trajectories"][0]


def _max_xy_error(original: dict, decoded: dict) -> float:
    return max(
        max(abs(source["x"] - recovered["x"]), abs(source["y"] - recovered["y"]))
        for source, recovered in zip(original["points"], decoded["points"], strict=True)
    )


def _max_haversine_error(original: dict, decoded: dict) -> float:
    return max(
        haversine_m(source["lat"], source["lon"], recovered["lat"], recovered["lon"])
        for source, recovered in zip(original["points"], decoded["points"], strict=True)
    )


class TestRoundtripFixtures(unittest.TestCase):
    def test_xy_fixture_point_count_preserved(self) -> None:
        trajectory = _load_first_trajectory("av_argoverse2_fixture_v1.json")
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.05).payload)
        self.assertEqual(len(decoded["points"]), len(trajectory["points"]))

    def test_xy_fixture_error_below_quant_step(self) -> None:
        trajectory = _load_first_trajectory("av_argoverse2_fixture_v1.json")
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.05).payload)
        self.assertLessEqual(_max_xy_error(trajectory, decoded), 1.1)

    def test_ais_fixture_point_count_preserved(self) -> None:
        trajectory = _load_first_trajectory("ais_noaa_fixture_v1.json")
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertEqual(len(decoded["points"]), len(trajectory["points"]))

    def test_ais_fixture_error_below_one_meter(self) -> None:
        trajectory = _load_first_trajectory("ais_noaa_fixture_v1.json")
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertLessEqual(_max_haversine_error(trajectory, decoded), 25.0)

    def test_noaa_real_world_extract_point_count_preserved(self) -> None:
        trajectory = _load_first_trajectory("real_world", "noaa_ais_day_extract.json")
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertEqual(len(decoded["points"]), len(trajectory["points"]))

    def test_geolife_real_world_extract_point_count_preserved(self) -> None:
        trajectory = _load_first_trajectory("real_world", "geolife_extract.json")
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertEqual(len(decoded["points"]), len(trajectory["points"]))

    def test_osm_real_world_extract_point_count_preserved(self) -> None:
        trajectory = _load_first_trajectory("real_world", "osm_monaco_way_extract.json")
        decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
        self.assertEqual(len(decoded["points"]), len(trajectory["points"]))


if __name__ == "__main__":
    unittest.main()
