from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestExamples(unittest.TestCase):
    def test_ais_compress_example_runs(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "examples" / "ais_compress.py")],
            check=True,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["dataset"], "NOAA AIS extract")
        self.assertGreater(payload["compression_ratio"], 1.0)
        self.assertGreater(payload["trajectory_count"], 0)

    def test_gpx_bridge_example_writes_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "roundtrip.gpx"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "examples" / "gpx_bridge.py"),
                    "--output",
                    str(output_path),
                ],
                check=True,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["input_points"], payload["output_points"])
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
