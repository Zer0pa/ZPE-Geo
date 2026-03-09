#!/usr/bin/env python3
"""Validate required artifacts for each gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import ARTIFACT_ROOT, init_artifact_root
from zpe_geo.utils import append_command_log


REQUIRED_BY_GATE = {
    "A": ["dataset_lock.json", "schema_inventory.json"],
    "B": ["geo_av_fidelity.json", "geo_ais_fidelity.json"],
    "C": [
        "geo_av_benchmark.json",
        "geo_ais_benchmark.json",
        "geo_maneuver_search_eval.json",
        "geo_query_latency_benchmark.json",
        "geo_stream_latency.json",
        "geo_h3_roundtrip_results.json",
    ],
    "D": ["falsification_results.md", "determinism_replay_results.json", "regression_results.txt"],
    "E": [
        "handoff_manifest.json",
        "before_after_metrics.json",
        "claim_status_delta.md",
        "quality_gate_scorecard.json",
        "innovation_delta_report.md",
        "integration_readiness_contract.json",
        "residual_risk_register.md",
        "concept_open_questions_resolution.md",
        "concept_resource_traceability.json",
    ],
    "M1": [
        "max_resource_lock.json",
        "dataset_subset_coverage_report.json",
        "trajectory_stratified_error_report.json",
        "impracticality_decisions.json",
    ],
    "M2": [
        "autoware_version_matrix.json",
        "autoware_smoke_results.json",
    ],
    "M3": ["max_scale_search_eval.json"],
    "M4": ["net_new_gap_closure_matrix.json"],
    "E2": [
        "max_resource_validation_log.md",
        "max_claim_resource_map.json",
        "impracticality_decisions.json",
        "max_gate_matrix.json",
    ],
    "F": [
        "osm_parity_full_corpus_report.json",
        "commercialization_gate_report.json",
        "net_new_gap_closure_matrix.json",
        "max_gate_matrix.json",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", required=True, choices=sorted(REQUIRED_BY_GATE.keys()))
    args = parser.parse_args()

    init_artifact_root()
    append_command_log(
        f"python3 code/scripts/validate_artifacts.py --gate {args.gate}",
        f"Validate gate {args.gate}",
    )
    missing = []
    for rel in REQUIRED_BY_GATE[args.gate]:
        p = ARTIFACT_ROOT / rel
        if not p.exists() or p.stat().st_size == 0:
            missing.append(rel)
    if missing:
        print("MISSING")
        for m in missing:
            print(m)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
