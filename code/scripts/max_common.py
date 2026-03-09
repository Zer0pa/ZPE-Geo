"""Shared helpers for maximalization and NET-NEW gates."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from common import ARTIFACT_ROOT, write_json
from zpe_geo.utils import ensure_dir, now_utc_iso


@dataclass
class CmdResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float


def run_cmd(command: str, timeout_s: int = 90) -> CmdResult:
    t0 = time.perf_counter()
    proc = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True,
        timeout=timeout_s,
        executable="/bin/zsh",
    )
    dt = time.perf_counter() - t0
    return CmdResult(
        command=command,
        exit_code=proc.returncode,
        stdout=(proc.stdout or "")[-6000:],
        stderr=(proc.stderr or "")[-6000:],
        duration_s=dt,
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def probe_url(url: str, timeout_s: float = 25.0) -> dict[str, Any]:
    req = Request(url, method="HEAD")
    try:
        with urlopen(req, timeout=timeout_s) as resp:  # nosec B310
            return {
                "status": f"reachable:{getattr(resp, 'status', 200)}",
                "headers": dict(resp.headers.items()),
            }
    except HTTPError as exc:
        return {"status": f"http_error:{exc.code}", "error": str(exc)}
    except URLError as exc:
        return {"status": "url_error", "error": str(exc)}
    except Exception as exc:  # broad by design for evidence capture
        return {"status": type(exc).__name__, "error": str(exc)}


def append_validation_log(lines: list[str]) -> None:
    ensure_dir(ARTIFACT_ROOT)
    path = ARTIFACT_ROOT / "max_resource_validation_log.md"
    if not path.exists():
        path.write_text("# Max Resource Validation Log\n\n", encoding="utf-8")
    with open(path, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")


def load_impracticality() -> list[dict[str, Any]]:
    path = ARTIFACT_ROOT / "impracticality_decisions.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("decisions", [])


def save_impracticality(entries: list[dict[str, Any]]) -> None:
    # Deduplicate on stable signature to keep reruns reproducible and compact.
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for row in entries:
        key = (
            str(row.get("resource", "")),
            str(row.get("impracticality_code", "")),
            str(row.get("command_evidence", "")),
            str(row.get("error_signature", "")),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    payload = {
        "generated_at_utc": now_utc_iso(),
        "allowed_codes": ["IMP-LICENSE", "IMP-ACCESS", "IMP-COMPUTE", "IMP-STORAGE", "IMP-NOCODE"],
        "decisions": deduped,
    }
    write_json(ARTIFACT_ROOT / "impracticality_decisions.json", payload)
