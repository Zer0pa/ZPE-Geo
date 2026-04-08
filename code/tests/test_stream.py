from __future__ import annotations

import unittest

from zpe_geo.stream import StreamState, encode_ais_update


class TestStream(unittest.TestCase):
    def test_encode_ais_update_requires_two_points_before_payload(self) -> None:
        state = StreamState()
        first_size, first_latency = encode_ais_update(
            state,
            {"mmsi": 111000111, "t": 0.0, "lat": 43.7384, "lon": 7.4246, "speed": 3.0, "cog": 90.0},
        )
        second_size, second_latency = encode_ais_update(
            state,
            {"mmsi": 111000111, "t": 10.0, "lat": 43.7386, "lon": 7.4250, "speed": 3.0, "cog": 90.0},
        )

        self.assertEqual(first_size, 0)
        self.assertGreaterEqual(first_latency, 0.0)
        self.assertGreater(second_size, 0)
        self.assertGreaterEqual(second_latency, 0.0)
        self.assertEqual(state.encoded_updates, 1)


if __name__ == "__main__":
    unittest.main()
