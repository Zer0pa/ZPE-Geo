from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestRealWorldBaselineBenchmarks(unittest.TestCase):
    def test_script_writes_summary_for_single_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "artifacts"
            subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "code" / "scripts" / "benchmark_real_world_baselines.py"),
                    "--fixture-path",
                    "code/fixtures/real_world/noaa_ais_day_extract.json",
                    "--output-dir",
                    str(output_root),
                ],
                check=True,
                cwd=REPO_ROOT,
            )
            summary = json.loads((output_root / "real_world_baseline_summary.json").read_text(encoding="utf-8"))

        self.assertEqual(summary["fixtures"], ["noaa_ais_day_extract.json"])
        self.assertEqual(summary["records"][0]["dataset"], "NOAA AIS extract")


if __name__ == "__main__":
    unittest.main()
