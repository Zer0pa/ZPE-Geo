"""Utility helpers for deterministic IO and logging."""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from .paths import ARTIFACT_ROOT


def ensure_dir(path: str | os.PathLike[str]) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def write_json(path: str | os.PathLike[str], payload: Any) -> None:
    ensure_dir(Path(path).parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


def read_json(path: str | os.PathLike[str]) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(payload: Any) -> str:
    if isinstance(payload, (dict, list, tuple)):
        raw = canonical_json_bytes(payload)
    elif isinstance(payload, bytes):
        raw = payload
    else:
        raw = str(payload).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def now_utc_iso() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).replace(microsecond=0).isoformat()


def append_command_log(command: str, note: str = "") -> None:
    ensure_dir(ARTIFACT_ROOT)
    stamp = now_utc_iso()
    line = f"[{stamp}] {command}"
    if note:
        line += f" :: {note}"
    with open(ARTIFACT_ROOT / "command_log.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def write_text(path: str | os.PathLike[str], text: str) -> None:
    ensure_dir(Path(path).parent)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def snapshot_gate(gate_name: str, files: list[str]) -> None:
    """Copy files into gate snapshot directory for rollback points."""
    base = ARTIFACT_ROOT / "gate_snapshots" / gate_name
    ensure_dir(base)
    for rel in files:
        src = ARTIFACT_ROOT / rel
        if src.exists():
            dst = base / rel
            ensure_dir(dst.parent)
            dst.write_bytes(src.read_bytes())
