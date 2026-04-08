from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from zpe_geo.utils import (
    append_command_log,
    canonical_json_bytes,
    ensure_dir,
    now_utc_iso,
    read_json,
    sha256_hex,
    snapshot_gate,
    write_json,
    write_text,
)


class TestUtils(unittest.TestCase):
    def test_json_and_text_helpers_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            json_path = temp_root / "nested" / "payload.json"
            text_path = temp_root / "nested" / "note.txt"

            ensure_dir(json_path.parent)
            write_json(json_path, {"b": 2, "a": 1})
            write_text(text_path, "hello")

            self.assertEqual(read_json(json_path), {"a": 1, "b": 2})
            self.assertEqual(text_path.read_text(encoding="utf-8"), "hello")
            self.assertEqual(canonical_json_bytes({"b": 2, "a": 1}), b'{"a":1,"b":2}')

    def test_hash_and_time_helpers(self) -> None:
        self.assertEqual(sha256_hex({"a": 1}), sha256_hex({"a": 1}))
        self.assertEqual(len(sha256_hex(b"abc")), 64)
        self.assertIn("+00:00", now_utc_iso())

    def test_command_log_and_snapshot_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            artifact_root = Path(temp_dir)
            source_file = artifact_root / "report.json"
            source_file.write_text('{"ok": true}', encoding="utf-8")

            with patch("zpe_geo.utils.ARTIFACT_ROOT", artifact_root):
                append_command_log("python -m pytest", "phase2")
                snapshot_gate("gate_P2", ["report.json"])

            command_log = (artifact_root / "command_log.txt").read_text(encoding="utf-8")
            snapshot_path = artifact_root / "gate_snapshots" / "gate_P2" / "report.json"
            self.assertIn("python -m pytest", command_log)
            self.assertEqual(snapshot_path.read_text(encoding="utf-8"), '{"ok": true}')


if __name__ == "__main__":
    unittest.main()
