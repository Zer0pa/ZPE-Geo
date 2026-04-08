from __future__ import annotations

import unittest

from zpe_geo.datasets import generate_av_suite
from zpe_geo.search import ManeuverSearchIndex


class TestSearchWithoutDecode(unittest.TestCase):
    def test_query_works_on_original_trajectory_surface(self) -> None:
        trajectories = generate_av_suite(seed=23, n_per_class=3).trajectories
        index = ManeuverSearchIndex(seed=29)
        index.build(trajectories)

        results, latency_s = index.query("left_turn", top_k=5)

        self.assertGreaterEqual(len(results), 1)
        self.assertGreaterEqual(latency_s, 0.0)
        self.assertTrue(all(result.trajectory_id for result in results))


if __name__ == "__main__":
    unittest.main()
