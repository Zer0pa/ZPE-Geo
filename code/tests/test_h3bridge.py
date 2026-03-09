from __future__ import annotations

import unittest

from zpe_geo.datasets import generate_ais_suite
from zpe_geo.h3bridge import H3Bridge


class TestH3Bridge(unittest.TestCase):
    def test_roundtrip_consistency(self) -> None:
        traj = generate_ais_suite(seed=55, n_per_class=1).trajectories[0]
        bridge = H3Bridge(resolution=9)
        result = bridge.roundtrip_consistent(traj, resolutions=[9, 10], drift_threshold_m=500.0)
        self.assertTrue(result["all_consistent"])


if __name__ == "__main__":
    unittest.main()
