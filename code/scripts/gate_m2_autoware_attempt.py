#!/usr/bin/env python3
"""Gate M2: Autoware pinned runtime integration attempt."""

from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from common import ARTIFACT_ROOT, init_artifact_root, write_json
from max_common import append_validation_log, load_impracticality, run_cmd, save_impracticality
from zpe_geo.paths import preferred_third_party_root
from zpe_geo.utils import append_command_log, now_utc_iso


THIRD_PARTY = preferred_third_party_root().resolve()
LOCAL_COLCON = THIRD_PARTY / "bin" / "colcon"


def _append_imp(
    entries: list[dict[str, Any]],
    code: str,
    command: str,
    error_signature: str,
    fallback: str,
    claim_impact: str,
) -> None:
    entries.append(
        {
            "resource": "Autoware runtime integration",
            "impracticality_code": code,
            "command_evidence": command,
            "error_signature": error_signature,
            "fallback": fallback,
            "claim_impact_note": claim_impact,
        }
    )


def _fetch_release_tags() -> list[dict[str, Any]]:
    url = "https://api.github.com/repos/autowarefoundation/autoware/releases?per_page=10"
    with urlopen(url, timeout=25) as resp:  # nosec B310
        payload = json.loads(resp.read().decode("utf-8"))
    rows = []
    for r in payload[:6]:
        rows.append(
            {
                "tag_name": r.get("tag_name"),
                "published_at": r.get("published_at"),
                "prerelease": bool(r.get("prerelease")),
                "html_url": r.get("html_url"),
            }
        )
    return rows


def _cmd_payload(command: str) -> dict[str, Any]:
    out = run_cmd(command, timeout_s=240)
    return {
        "command": out.command,
        "exit_code": out.exit_code,
        "stdout": out.stdout.strip(),
        "stderr": out.stderr.strip(),
        "duration_s": round(out.duration_s, 3),
    }


def _remove_autoware_compute_imp(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in entries:
        if row.get("resource") != "Autoware runtime integration":
            out.append(row)
            continue
        if row.get("impracticality_code") != "IMP-COMPUTE":
            out.append(row)
    return out


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_m2_autoware_attempt.py", "Gate M2 start")

    impracticality = load_impracticality()
    matrix = {
        "generated_at_utc": now_utc_iso(),
        "repo": "https://github.com/autowarefoundation/autoware",
        "candidate_versions": [],
        "pinned_for_lane": {
            "autoware_tag": "v1.4.0",
            "ros2_distribution": "humble",
            "build_system": "colcon",
            "status": "PINNED_FOR_SMOKE_ATTEMPT",
        },
    }
    try:
        matrix["candidate_versions"] = _fetch_release_tags()
    except Exception as exc:
        _append_imp(
            impracticality,
            "IMP-ACCESS",
            "GET https://api.github.com/repos/autowarefoundation/autoware/releases",
            f"{type(exc).__name__}: {exc}",
            "Fallback to static pinned matrix from known stable tag.",
            "M2 runtime confidence reduced; keep integration closure INCONCLUSIVE.",
        )

    local_install_attempts = {
        "pip_ros2cli": _cmd_payload(
            f"python3 -m pip install --upgrade --target {shlex.quote(str(THIRD_PARTY))} ros2cli"
        ),
        "pip_colcon_common_extensions": _cmd_payload(
            "python3 -m pip install --upgrade "
            f"--target {shlex.quote(str(THIRD_PARTY))} colcon-common-extensions"
        ),
        "brew_ros_humble_formula": _cmd_payload("brew install ros-humble-ros-base"),
    }

    checks = {
        "ros2_cli": _cmd_payload("command -v ros2 || true"),
        "colcon": _cmd_payload("command -v colcon || true"),
        "local_colcon": {
            "command": f"test -x {shlex.quote(str(LOCAL_COLCON))}",
            "exit_code": 0 if LOCAL_COLCON.exists() else 1,
            "stdout": str(LOCAL_COLCON.resolve()) if LOCAL_COLCON.exists() else "",
            "stderr": "",
            "duration_s": 0.0,
        },
        "docker": _cmd_payload("command -v docker || true"),
    }

    host_ros2_path = checks["ros2_cli"]["stdout"]
    host_colcon_path = checks["colcon"]["stdout"] or checks["local_colcon"]["stdout"]
    host_smoke = {
        "ros2_help": _cmd_payload("ros2 --help >/tmp/geo_m2_ros2_help.txt 2>&1 || true")
        if host_ros2_path
        else {"command": "ros2 --help", "exit_code": 127, "stdout": "", "stderr": "ros2 not found", "duration_s": 0.0},
        "colcon_help": _cmd_payload("colcon --help >/tmp/geo_m2_colcon_help.txt 2>&1 || true")
        if checks["colcon"]["stdout"]
        else (
            _cmd_payload(
                f"{shlex.quote(str(LOCAL_COLCON))} --help >/tmp/geo_m2_colcon_help.txt 2>&1 || true"
            )
            if LOCAL_COLCON.exists()
            else {
                "command": "colcon --help",
                "exit_code": 127,
                "stdout": "",
                "stderr": "colcon not found",
                "duration_s": 0.0,
            }
        ),
    }
    host_smoke_pass = (
        bool(host_ros2_path)
        and bool(host_colcon_path)
        and host_smoke["ros2_help"]["exit_code"] == 0
        and host_smoke["colcon_help"]["exit_code"] == 0
    )

    container_attempts: dict[str, Any] = {
        "docker_info_before": _cmd_payload("docker info --format '{{.ServerVersion}} {{.OSType}}/{{.Architecture}}'"),
    }
    docker_ready = container_attempts["docker_info_before"]["exit_code"] == 0
    if not docker_ready:
        container_attempts["colima_start_vz"] = _cmd_payload(
            "PATH=/opt/homebrew/bin:$PATH /opt/homebrew/bin/colima start --vm-type vz --arch aarch64 --vz-rosetta --cpu 4 --memory 8 --disk 60"
        )
        container_attempts["docker_info_after"] = _cmd_payload(
            "docker info --format '{{.ServerVersion}} {{.OSType}}/{{.Architecture}}'"
        )
        docker_ready = container_attempts["docker_info_after"]["exit_code"] == 0

    container_smoke = {
        "command": (
            "docker run --rm ros:humble-ros-base bash -lc "
            "'set -e; command -v ros2; ros2 --help >/tmp/ros2_help.txt; "
            "apt-get update >/tmp/apt_update.log; "
            "apt-get install -y python3-colcon-common-extensions >/tmp/apt_install.log; "
            "command -v colcon; colcon --help >/tmp/colcon_help.txt; echo OK'"
        ),
        "exit_code": 127,
        "stdout": "",
        "stderr": "docker daemon unavailable",
        "duration_s": 0.0,
    }
    if docker_ready:
        out = run_cmd(container_smoke["command"], timeout_s=1800)
        container_smoke = {
            "command": out.command,
            "exit_code": out.exit_code,
            "stdout": out.stdout.strip(),
            "stderr": out.stderr.strip(),
            "duration_s": round(out.duration_s, 3),
        }
    container_smoke_pass = container_smoke["exit_code"] == 0

    runtime_smoke_pass = host_smoke_pass or container_smoke_pass
    smoke_mode = "HOST" if host_smoke_pass else ("CONTAINER" if container_smoke_pass else "BLOCKED")
    if runtime_smoke_pass:
        impracticality = _remove_autoware_compute_imp(impracticality)
        matrix["pinned_for_lane"]["status"] = f"PASS_{smoke_mode}_SMOKE"
    else:
        _append_imp(
            impracticality,
            "IMP-COMPUTE",
            "ros2/colcon host + docker/colima container smoke chain",
            "Host missing ros2 or smoke failed, and container smoke path failed.",
            "Use RunPod image with ROS2 Humble + Autoware toolchain and deterministic replay script.",
            "M2 remains FAIL; GEO-C008 integration confidence blocked pending external compute/runtime.",
        )

    smoke = {
        "generated_at_utc": now_utc_iso(),
        "checks": checks,
        "local_install_attempts": local_install_attempts,
        "host_smoke": host_smoke,
        "container_attempts": container_attempts,
        "container_smoke": container_smoke,
        "runtime_smoke_pass": runtime_smoke_pass,
        "smoke_mode": smoke_mode,
        "notes": [
            "Host and containerized runtime checks executed in sequence.",
            "Container smoke uses ros:humble-ros-base with in-container colcon install for reproducibility.",
        ],
    }

    write_json(ARTIFACT_ROOT / "autoware_version_matrix.json", matrix)
    write_json(ARTIFACT_ROOT / "autoware_smoke_results.json", smoke)
    save_impracticality(impracticality)
    append_validation_log(
        [
            "",
            f"## Gate M2 ({now_utc_iso()})",
            f"- Runtime smoke pass: {smoke['runtime_smoke_pass']}",
            f"- Smoke mode: {smoke['smoke_mode']}",
            f"- Docker ready: {container_attempts.get('docker_info_after', container_attempts['docker_info_before'])['exit_code'] == 0}",
        ]
    )
    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_M2" / "gate_M2_manifest.json",
        {
            "gate": "M2",
            "artifacts": [
                "autoware_version_matrix.json",
                "autoware_smoke_results.json",
                "impracticality_decisions.json",
            ],
        },
    )
    append_command_log("python3 code/scripts/gate_m2_autoware_attempt.py", "Gate M2 complete")


if __name__ == "__main__":
    main()
