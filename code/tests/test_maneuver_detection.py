from __future__ import annotations

import unittest

from zpe_geo.maneuver import detect_maneuvers


def _left_turn_trajectory() -> dict:
    return {
        "trajectory_id": "left_turn_demo",
        "coord_system": "xy",
        "points": [
            {"x": 0.0, "y": 0.0, "speed": 4.0},
            {"x": 0.0, "y": 1.0, "speed": 4.0},
            {"x": 1.0, "y": 2.0, "speed": 4.0},
            {"x": 2.0, "y": 2.0, "speed": 4.0},
        ],
    }


def _stop_trajectory() -> dict:
    return {
        "trajectory_id": "stop_demo",
        "coord_system": "xy",
        "points": [
            {"x": 0.0, "y": 0.0, "speed": 4.0},
            {"x": 1.0, "y": 0.0, "speed": 0.2},
            {"x": 1.0, "y": 0.0, "speed": 0.1},
            {"x": 1.0, "y": 0.0, "speed": 0.0},
            {"x": 2.0, "y": 0.0, "speed": 4.0},
        ],
    }


class TestManeuverDetection(unittest.TestCase):
    def test_left_turn_scores_high(self) -> None:
        scores = detect_maneuvers(_left_turn_trajectory())
        self.assertGreaterEqual(scores["left_turn"], 0.9)

    def test_stop_scores_high(self) -> None:
        scores = detect_maneuvers(_stop_trajectory())
        self.assertGreaterEqual(scores["stop"], 0.9)


if __name__ == "__main__":
    unittest.main()
