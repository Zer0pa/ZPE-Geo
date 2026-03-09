"""Shared helpers for gate scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zpe_geo.paths import ARTIFACT_ROOT as GEO_ARTIFACT_ROOT
from zpe_geo.paths import FIXTURES_ROOT
from zpe_geo.utils import ensure_dir, now_utc_iso

ARTIFACT_ROOT = GEO_ARTIFACT_ROOT
DATA_ROOT = FIXTURES_ROOT
GATE_SNAPSHOT_ROOT = ARTIFACT_ROOT / "gate_snapshots"


def init_artifact_root() -> None:
    ensure_dir(ARTIFACT_ROOT)
    ensure_dir(DATA_ROOT)
    ensure_dir(GATE_SNAPSHOT_ROOT)


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


def gate_snapshot_dir(gate_name: str) -> Path:
    p = GATE_SNAPSHOT_ROOT / gate_name
    ensure_dir(p)
    return p


def write_resource_failure(line: str) -> None:
    ensure_dir(ARTIFACT_ROOT)
    with open(ARTIFACT_ROOT / "resource_failures.log", "a", encoding="utf-8") as f:
        f.write(f"[{now_utc_iso()}] {line}\n")
