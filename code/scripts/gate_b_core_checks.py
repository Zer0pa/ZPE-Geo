#!/usr/bin/env python3
"""Gate B: core encode/decode + baseline fidelity checks."""

from __future__ import annotations

import statistics
from pathlib import Path

from common import ARTIFACT_ROOT, DATA_ROOT, init_artifact_root, load_json, write_json
from zpe_geo.codec import decode_trajectory, encode_trajectory
from zpe_geo.geo import dtw_distance_m
from zpe_geo.metrics import percentile, rmse_xy_m
from zpe_geo.utils import append_command_log


def _load_fixture(name: str) -> list[dict]:
    payload = load_json(DATA_ROOT / name)
    return payload["trajectories"]


def _av_fidelity(av_trajs: list[dict]) -> dict:
    rmses = []
    failures = 0
    for traj in av_trajs:
        try:
            encoded = encode_trajectory(traj, quant_step_m=0.05)
            decoded = decode_trajectory(encoded.payload)
            rmses.append(rmse_xy_m(traj["points"], decoded["points"]))
        except Exception:
            failures += 1
    return {
        "trajectory_count": len(av_trajs),
        "failures": failures,
        "rmse_m_mean": statistics.mean(rmses) if rmses else float("inf"),
        "rmse_m_p95": percentile(rmses, 95),
        "rmse_m_max": max(rmses) if rmses else float("inf"),
        "threshold_m": 1.0,
        "pass": failures == 0 and (statistics.mean(rmses) if rmses else float("inf")) <= 1.0,
    }


def _ais_fidelity(ais_trajs: list[dict]) -> dict:
    dtws = []
    failures = 0
    for traj in ais_trajs:
        try:
            encoded = encode_trajectory(traj, quant_step_m=0.25)
            decoded = decode_trajectory(encoded.payload)
            original_seq = [(p["lat"], p["lon"]) for p in traj["points"]]
            decoded_seq = [(p["lat"], p["lon"]) for p in decoded["points"]]
            dtws.append(dtw_distance_m(original_seq, decoded_seq))
        except Exception:
            failures += 1
    mean_dtw = statistics.mean(dtws) if dtws else float("inf")
    return {
        "trajectory_count": len(ais_trajs),
        "failures": failures,
        "dtw_m_mean": mean_dtw,
        "dtw_m_p95": percentile(dtws, 95),
        "dtw_m_max": max(dtws) if dtws else float("inf"),
        "threshold_m": 50.0,
        "pass": failures == 0 and mean_dtw <= 50.0,
    }


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_b_core_checks.py", "Gate B start")
    av_trajs = _load_fixture("av_argoverse2_fixture_v1.json")
    ais_trajs = _load_fixture("ais_noaa_fixture_v1.json")

    av = _av_fidelity(av_trajs)
    ais = _ais_fidelity(ais_trajs)

    write_json(ARTIFACT_ROOT / "geo_av_fidelity.json", av)
    write_json(ARTIFACT_ROOT / "geo_ais_fidelity.json", ais)
    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_B" / "gate_B_manifest.json",
        {"gate": "B", "artifacts": ["geo_av_fidelity.json", "geo_ais_fidelity.json"]},
    )
    append_command_log("python3 code/scripts/gate_b_core_checks.py", "Gate B complete")


if __name__ == "__main__":
    main()
