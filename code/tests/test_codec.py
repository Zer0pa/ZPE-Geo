from __future__ import annotations

import unittest

from zpe_geo.codec import decode_trajectory, encode_trajectory
from zpe_geo.datasets import generate_ais_suite, generate_av_suite
from zpe_geo.metrics import rmse_xy_m


class TestCodec(unittest.TestCase):
    def test_xy_roundtrip_rmse(self) -> None:
        traj = generate_av_suite(seed=11, n_per_class=1).trajectories[0]
        encoded = encode_trajectory(traj, quant_step_m=0.05)
        decoded = decode_trajectory(encoded.payload)
        rmse = rmse_xy_m(traj["points"], decoded["points"])
        self.assertLessEqual(rmse, 1.0)

    def test_wgs84_roundtrip(self) -> None:
        traj = generate_ais_suite(seed=21, n_per_class=1).trajectories[0]
        encoded = encode_trajectory(traj, quant_step_m=0.25)
        decoded = decode_trajectory(encoded.payload)
        self.assertEqual(decoded["coord_system"], "wgs84")
        self.assertEqual(len(decoded["points"]), len(traj["points"]))

    def test_invalid_payload(self) -> None:
        with self.assertRaises(ValueError):
            decode_trajectory(b"BAD")


if __name__ == "__main__":
    unittest.main()
