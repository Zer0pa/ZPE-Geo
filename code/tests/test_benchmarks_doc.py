from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestBenchmarksDoc(unittest.TestCase):
    def test_benchmarks_doc_has_methodology_and_table(self) -> None:
        content = (REPO_ROOT / "BENCHMARKS.md").read_text(encoding="utf-8")
        self.assertIn("## Methodology", content)
        self.assertIn("| Dataset | Script | Fixture | Artifact |", content)


if __name__ == "__main__":
    unittest.main()
