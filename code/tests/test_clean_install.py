from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = REPO_ROOT / "code"


class TestCleanInstall(unittest.TestCase):
    def test_clean_install_imports_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            venv_dir = Path(temp_dir) / "clean-venv"
            dist_dir = Path(temp_dir) / "dist"
            python_bin = venv_dir / "bin" / "python"
            sdist_path = None

            subprocess.run(
                [sys.executable, "-m", "build", "--sdist", "--outdir", str(dist_dir), str(PACKAGE_ROOT)],
                check=True,
                cwd=REPO_ROOT,
            )
            for candidate in dist_dir.glob("zpe_geo-*.tar.gz"):
                sdist_path = candidate
                break
            if sdist_path is None:
                self.fail("sdist build did not produce a .tar.gz artifact")

            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True, cwd=REPO_ROOT)
            subprocess.run(
                [str(python_bin), "-m", "pip", "install", "--disable-pip-version-check", str(sdist_path)],
                check=True,
                cwd=REPO_ROOT,
            )
            proc = subprocess.run(
                [str(python_bin), "-c", "import zpe_geo; print(zpe_geo.__all__)"],
                check=True,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )

        self.assertIn("encode_trajectory", proc.stdout)


if __name__ == "__main__":
    unittest.main()
