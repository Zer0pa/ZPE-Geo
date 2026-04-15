from __future__ import annotations

import json
import unittest
from pathlib import Path

from zpe_geo.search import ManeuverSearchIndex, precision_at_k


class TestSearch(unittest.TestCase):
    def test_labels_do_not_affect_ranking(self) -> None:
        lane_merge = {
            "trajectory_id": "lane_merge",
            "coord_system": "xy",
            "label": "stop",
            "points": [
                {"t": 0.0, "x": 0.0, "y": 0.0, "speed": 4.0, "cog": 0.0},
                {"t": 1.0, "x": 0.0, "y": 1.0, "speed": 4.0, "cog": 0.0},
                {"t": 2.0, "x": 0.0, "y": 2.0, "speed": 4.0, "cog": 0.0},
                {"t": 3.0, "x": 1.0, "y": 3.0, "speed": 4.0, "cog": 45.0},
                {"t": 4.0, "x": 1.0, "y": 4.0, "speed": 4.0, "cog": 0.0},
                {"t": 5.0, "x": 1.0, "y": 5.0, "speed": 4.0, "cog": 0.0},
            ],
        }
        stop = {
            "trajectory_id": "stop",
            "coord_system": "xy",
            "label": "lane_merge",
            "points": [
                {"t": 0.0, "x": 0.0, "y": 0.0, "speed": 3.0, "cog": 0.0},
                {"t": 1.0, "x": 0.0, "y": 1.0, "speed": 3.0, "cog": 0.0},
                {"t": 2.0, "x": 0.0, "y": 2.0, "speed": 0.0, "cog": 511.0},
                {"t": 3.0, "x": 0.0, "y": 2.0, "speed": 0.0, "cog": 511.0},
                {"t": 4.0, "x": 0.0, "y": 2.0, "speed": 0.0, "cog": 511.0},
                {"t": 5.0, "x": 0.0, "y": 3.0, "speed": 3.0, "cog": 0.0},
            ],
        }
        idx = ManeuverSearchIndex(seed=44)
        idx.build([lane_merge, stop])

        lane_merge_results, _latency = idx.query("lane_merge", top_k=10)
        stop_results, _latency = idx.query("stop", top_k=10)

        self.assertEqual([result.trajectory_id for result in lane_merge_results], ["lane_merge"])
        self.assertEqual([result.trajectory_id for result in stop_results], ["stop"])
        self.assertEqual(lane_merge_results[0].label, "stop")
        self.assertEqual(stop_results[0].label, "lane_merge")

    def test_existing_benchmark_path_reports_honest_precision(self) -> None:
        fixture_path = (
            Path(__file__).resolve().parents[1] / "fixtures" / "av_argoverse2_fixture_v1.json"
        )
        av = json.loads(fixture_path.read_text(encoding="utf-8"))["trajectories"]
        idx = ManeuverSearchIndex(seed=20260224)
        idx.build(av)

        observed = {}
        for maneuver in ("left_turn", "lane_merge", "stop"):
            results, _latency = idx.query(maneuver, top_k=10)
            observed[maneuver] = precision_at_k(results, expected_label=maneuver, k=10)

        self.assertEqual(observed["left_turn"], 0.0)
        self.assertEqual(observed["lane_merge"], 0.0)
        self.assertEqual(observed["stop"], 1.0)
        self.assertAlmostEqual(sum(observed.values()) / 3.0, 1.0 / 3.0)


if __name__ == "__main__":
    unittest.main()
