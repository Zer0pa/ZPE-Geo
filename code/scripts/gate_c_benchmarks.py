#!/usr/bin/env python3
"""Gate C: comparator and performance matrix."""

from __future__ import annotations

import statistics
import time
from pathlib import Path

from common import ARTIFACT_ROOT, DATA_ROOT, init_artifact_root, load_json, write_json
from zpe_geo.codec import decode_trajectory, encode_trajectory
from zpe_geo.comparator import encoded_size_dp_bytes, simplify_douglas_peucker
from zpe_geo.datasets import (
    estimate_raw_ais_nmea_bytes,
    estimate_raw_av_bytes,
    simulate_trajectory_corpus_size,
)
from zpe_geo.h3bridge import H3Bridge
from zpe_geo.metrics import compression_ratio, path_length_haversine_m, percentile
from zpe_geo.search import ManeuverSearchIndex, precision_at_k
from zpe_geo.stream import StreamState, encode_ais_update
from zpe_geo.utils import append_command_log


def _load_fixture(name: str) -> list[dict]:
    payload = load_json(DATA_ROOT / name)
    return payload["trajectories"]


def benchmark_av(av_trajs: list[dict]) -> dict:
    ratios = []
    encoded_sizes = []
    for traj in av_trajs:
        enc = encode_trajectory(traj, quant_step_m=0.05)
        raw_b = estimate_raw_av_bytes(traj)
        ratios.append(compression_ratio(raw_b, len(enc.payload)))
        encoded_sizes.append(len(enc.payload))
    return {
        "trajectory_count": len(av_trajs),
        "compression_ratio_mean": statistics.mean(ratios),
        "compression_ratio_median": statistics.median(ratios),
        "compression_ratio_p95": percentile(ratios, 95),
        "encoded_size_mean_bytes": statistics.mean(encoded_sizes),
        "threshold": 20.0,
        "pass": statistics.mean(ratios) >= 20.0,
    }


def benchmark_ais(ais_trajs: list[dict]) -> dict:
    zpe_ratios = []
    dp_ratios = []
    zpe_lens = []
    dp_lens = []
    length_loss_dp = []
    for traj in ais_trajs:
        raw_b = estimate_raw_ais_nmea_bytes(traj)
        enc = encode_trajectory(traj, quant_step_m=0.25)
        zpe_b = len(enc.payload)
        zpe_ratios.append(compression_ratio(raw_b, zpe_b))
        zpe_lens.append(zpe_b)

        dp = simplify_douglas_peucker(traj, epsilon_m=15.0)
        dp_b = encoded_size_dp_bytes(dp)
        dp_ratios.append(compression_ratio(raw_b, dp_b))
        dp_lens.append(dp_b)

        raw_len = path_length_haversine_m(traj["points"])
        dp_len = path_length_haversine_m(dp["points"])
        if raw_len > 0.0:
            length_loss_dp.append(max(0.0, (raw_len - dp_len) / raw_len))

    zpe_mean = statistics.mean(zpe_ratios)
    dp_mean = statistics.mean(dp_ratios)
    return {
        "trajectory_count": len(ais_trajs),
        "compression_ratio_mean": zpe_mean,
        "compression_ratio_median": statistics.median(zpe_ratios),
        "compression_ratio_p95": percentile(zpe_ratios, 95),
        "encoded_size_mean_bytes": statistics.mean(zpe_lens),
        "threshold": 25.0,
        "pass": zpe_mean >= 25.0,
        "comparators": {
            "douglas_peucker": {
                "compression_ratio_mean": dp_mean,
                "encoded_size_mean_bytes": statistics.mean(dp_lens),
                "avg_length_loss_ratio": statistics.mean(length_loss_dp) if length_loss_dp else 0.0,
            },
            "acm_2025_framing": {
                "paper_reference": "https://dl.acm.org/doi/10.1145/3764920.3770598",
                "positioning": (
                    "In-lane benchmark includes incumbent DP baseline; direct paper dataset parity "
                    "remains INCONCLUSIVE without supplementary dataset alignment."
                ),
            },
        },
        "beat_dp": zpe_mean > dp_mean,
    }


def benchmark_search(av_trajs: list[dict]) -> dict:
    idx = ManeuverSearchIndex(seed=20260224)
    idx.build(av_trajs)
    queries = ["left_turn", "lane_merge", "stop"]
    per_class = {}
    p10s = []
    for q in queries:
        results, latency_s = idx.query(q, top_k=10)
        p10 = precision_at_k(results, expected_label=q, k=10)
        per_class[q] = {"p_at_10": p10, "latency_ms": latency_s * 1000.0}
        p10s.append(p10)
    return {
        "trajectory_count": len(av_trajs),
        "queries": per_class,
        "p_at_10_mean": statistics.mean(p10s) if p10s else 0.0,
        "threshold": 0.90,
        "pass": (statistics.mean(p10s) if p10s else 0.0) >= 0.90,
    }


def benchmark_query_latency(av_trajs: list[dict]) -> dict:
    idx = ManeuverSearchIndex(seed=20260225)
    idx.build(av_trajs)
    corpus = simulate_trajectory_corpus_size(indexed_count=len(av_trajs), target_count=10_000_000)
    latencies = []
    for _ in range(120):
        for maneuver in ("left_turn", "lane_merge", "stop"):
            _results, elapsed = idx.query(
                maneuver, top_k=10, simulated_corpus_size=corpus["simulated_total"]
            )
            latencies.append(elapsed)
    p95 = percentile([x * 1000.0 for x in latencies], 95)
    return {
        "indexed_trajectories": len(av_trajs),
        "simulated_corpus": corpus,
        "query_latency_ms_mean": statistics.mean(latencies) * 1000.0,
        "query_latency_ms_p95": p95,
        "threshold_s": 1.0,
        "pass": p95 < 1000.0,
    }


def benchmark_stream_latency(ais_trajs: list[dict]) -> dict:
    state = StreamState()
    latencies = []
    encoded_sizes = []
    max_updates = 40_000
    updates = 0
    for traj in ais_trajs:
        for p in traj["points"]:
            sz, lat_ms = encode_ais_update(state, p)
            if sz:
                encoded_sizes.append(sz)
                latencies.append(lat_ms)
            updates += 1
            if updates >= max_updates:
                break
        if updates >= max_updates:
            break
    p95 = percentile(latencies, 95)
    return {
        "updates_processed": updates,
        "encoded_updates": state.encoded_updates,
        "encode_latency_ms_mean": statistics.mean(latencies) if latencies else float("inf"),
        "encode_latency_ms_p95": p95,
        "encoded_size_mean_bytes": statistics.mean(encoded_sizes) if encoded_sizes else 0.0,
        "threshold_ms": 10.0,
        "pass": p95 < 10.0,
    }


def benchmark_h3_roundtrip(ais_trajs: list[dict]) -> dict:
    bridge = H3Bridge(resolution=9)
    sample = ais_trajs[:30]
    checks = []
    failures = 0
    for traj in sample:
        result = bridge.roundtrip_consistent(traj, resolutions=[9, 10, 11], drift_threshold_m=250.0)
        checks.append(
            {
                "trajectory_id": traj["trajectory_id"],
                "all_consistent": result["all_consistent"],
                "failures": result["failures"],
            }
        )
        failures += result["failures"]
    pass_all = failures == 0 and all(c["all_consistent"] for c in checks)
    return {
        "backend": bridge.backend,
        "trajectory_count": len(sample),
        "failures": failures,
        "all_consistent": pass_all,
        "threshold": "zero failures",
        "pass": pass_all,
    }


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_c_benchmarks.py", "Gate C start")
    av_trajs = _load_fixture("av_argoverse2_fixture_v1.json")
    ais_trajs = _load_fixture("ais_noaa_fixture_v1.json")

    av_b = benchmark_av(av_trajs)
    ais_b = benchmark_ais(ais_trajs)
    search_b = benchmark_search(av_trajs)
    query_b = benchmark_query_latency(av_trajs)
    stream_b = benchmark_stream_latency(ais_trajs)
    h3_b = benchmark_h3_roundtrip(ais_trajs)

    write_json(ARTIFACT_ROOT / "geo_av_benchmark.json", av_b)
    write_json(ARTIFACT_ROOT / "geo_ais_benchmark.json", ais_b)
    write_json(ARTIFACT_ROOT / "geo_maneuver_search_eval.json", search_b)
    write_json(ARTIFACT_ROOT / "geo_query_latency_benchmark.json", query_b)
    write_json(ARTIFACT_ROOT / "geo_stream_latency.json", stream_b)
    write_json(ARTIFACT_ROOT / "geo_h3_roundtrip_results.json", h3_b)

    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_C" / "gate_C_manifest.json",
        {
            "gate": "C",
            "artifacts": [
                "geo_av_benchmark.json",
                "geo_ais_benchmark.json",
                "geo_maneuver_search_eval.json",
                "geo_query_latency_benchmark.json",
                "geo_stream_latency.json",
                "geo_h3_roundtrip_results.json",
            ],
        },
    )
    append_command_log("python3 code/scripts/gate_c_benchmarks.py", "Gate C complete")


if __name__ == "__main__":
    main()
