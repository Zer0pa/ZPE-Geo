#!/usr/bin/env python3
"""Gate M3: scale search + maneuver robustness on multi-resource cohorts."""

from __future__ import annotations

import math
import sys
from typing import Any

from common import ARTIFACT_ROOT, DATA_ROOT, init_artifact_root, load_json, write_json
from max_common import append_validation_log, load_impracticality, save_impracticality
from zpe_geo.paths import EXTERNAL_SAMPLES_ROOT, preferred_third_party_root
from zpe_geo.search import ManeuverSearchIndex, precision_at_k
from zpe_geo.utils import append_command_log, now_utc_iso

THIRD_PARTY = preferred_third_party_root().resolve()
if str(THIRD_PARTY) not in sys.path:
    sys.path.insert(0, str(THIRD_PARTY))

try:
    import pyarrow.parquet as pq  # type: ignore
except Exception:  # pragma: no cover
    pq = None


def _label_xy(points: list[dict[str, float]]) -> str:
    if len(points) < 6:
        return "straight"
    headings = []
    for i in range(1, len(points)):
        dx = points[i]["x"] - points[i - 1]["x"]
        dy = points[i]["y"] - points[i - 1]["y"]
        if dx == 0.0 and dy == 0.0:
            continue
        headings.append(math.degrees(math.atan2(dy, dx)))
    if len(headings) < 2:
        return "straight"
    sweep = headings[-1] - headings[0]
    if sweep > 30:
        return "left_turn"
    if abs(sweep) < 10:
        return "straight"
    return "lane_merge"


def _load_av2_subset(max_n: int = 1200) -> list[dict[str, Any]]:
    path = EXTERNAL_SAMPLES_ROOT / "av2_mf_focal_test_annotations.parquet"
    if pq is None or not path.exists():
        return []
    table = pq.read_table(str(path), columns=["scenario_id", "track_id", "gt_trajectory_x", "gt_trajectory_y"])
    rows = table.to_pylist()
    out = []
    for r in rows[:max_n]:
        xs = r["gt_trajectory_x"] or []
        ys = r["gt_trajectory_y"] or []
        n = min(len(xs), len(ys))
        if n < 20:
            continue
        pts = []
        for i in range(n):
            pts.append({"t": i * 0.1, "x": float(xs[i]), "y": float(ys[i]), "speed": 0.0, "cog": 511.0})
        out.append(
            {
                "trajectory_id": f"av2_{r['scenario_id']}_{r['track_id']}",
                "coord_system": "xy",
                "points": pts,
                "label": _label_xy(pts),
            }
        )
    return out


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_m3_scale_search.py", "Gate M3 start")
    impracticality = load_impracticality()

    av_fixture = load_json(DATA_ROOT / "av_argoverse2_fixture_v1.json")["trajectories"]
    av2_subset = _load_av2_subset(max_n=1400)
    trajectories = av_fixture + av2_subset

    index = ManeuverSearchIndex(seed=20260226)
    index.build(trajectories)

    eval_rows = {}
    p10s = []
    latencies_ms = []
    for maneuver in ("left_turn", "lane_merge", "stop"):
        results, lat_s = index.query(maneuver, top_k=10, simulated_corpus_size=10_000_000)
        p10 = precision_at_k(results, expected_label=maneuver, k=10)
        eval_rows[maneuver] = {"p_at_10": p10, "latency_ms": lat_s * 1000.0}
        p10s.append(p10)
        latencies_ms.append(lat_s * 1000.0)

    # Scale stress loop.
    for _ in range(150):
        for maneuver in ("left_turn", "lane_merge", "stop"):
            _res, lat_s = index.query(maneuver, top_k=10, simulated_corpus_size=10_000_000)
            latencies_ms.append(lat_s * 1000.0)

    lat_sorted = sorted(latencies_ms)
    p95_idx = int(round(0.95 * (len(lat_sorted) - 1)))
    latency_p95 = lat_sorted[p95_idx]

    payload = {
        "generated_at_utc": now_utc_iso(),
        "cohorts": {
            "av_fixture_count": len(av_fixture),
            "av2_subset_count": len(av2_subset),
            "total_indexed": len(trajectories),
        },
        "queries": eval_rows,
        "p_at_10_mean": sum(p10s) / max(1, len(p10s)),
        "latency_ms_p95": latency_p95,
        "thresholds": {"p_at_10_min": 0.90, "latency_ms_p95_max": 1000.0},
        "pass": (sum(p10s) / max(1, len(p10s))) >= 0.90 and latency_p95 < 1000.0,
    }
    write_json(ARTIFACT_ROOT / "max_scale_search_eval.json", payload)
    save_impracticality(impracticality)
    append_validation_log(
        [
            "",
            f"## Gate M3 ({now_utc_iso()})",
            f"- Cohort total indexed: {len(trajectories)}",
            f"- p@10 mean: {payload['p_at_10_mean']:.4f}",
            f"- latency p95 ms: {latency_p95:.4f}",
            f"- pass: {payload['pass']}",
        ]
    )
    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_M3" / "gate_M3_manifest.json",
        {"gate": "M3", "artifacts": ["max_scale_search_eval.json"]},
    )
    append_command_log("python3 code/scripts/gate_m3_scale_search.py", "Gate M3 complete")


if __name__ == "__main__":
    main()
