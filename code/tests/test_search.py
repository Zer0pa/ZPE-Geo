from __future__ import annotations

import unittest

from zpe_geo.datasets import generate_av_suite
from zpe_geo.search import ManeuverSearchIndex, precision_at_k


class TestSearch(unittest.TestCase):
    def test_precision_at_10(self) -> None:
        av = generate_av_suite(seed=33, n_per_class=8).trajectories
        idx = ManeuverSearchIndex(seed=44)
        idx.build(av)
        results, _latency = idx.query("left_turn", top_k=10)
        p10 = precision_at_k(results, expected_label="left_turn", k=10)
        self.assertGreaterEqual(p10, 0.8)


if __name__ == "__main__":
    unittest.main()
