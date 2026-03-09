#!/usr/bin/env python3
"""Gate A: runbook + dataset lock + schema inventory freeze."""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path

from common import ARTIFACT_ROOT, DATA_ROOT, init_artifact_root, write_json, write_resource_failure
from zpe_geo.datasets import generate_ais_suite, generate_av_suite
from zpe_geo.utils import append_command_log, now_utc_iso

AV_SEED = 20260221
AIS_SEED = 20260222


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def probe_url(url: str, timeout_s: float = 8.0) -> dict[str, str]:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # nosec B310
            status = getattr(resp, "status", 200)
            return {"status": f"reachable:{status}"}
    except urllib.error.HTTPError as exc:
        return {"status": f"http_error:{exc.code}"}
    except Exception as exc:  # broad by design for protocol capture
        return {"status": f"unreachable:{type(exc).__name__}", "detail": str(exc)}


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_a_lock.py", "Gate A start")

    av_bundle = generate_av_suite(seed=AV_SEED, n_per_class=42)
    ais_bundle = generate_ais_suite(seed=AIS_SEED, n_per_class=38)

    av_path = DATA_ROOT / "av_argoverse2_fixture_v1.json"
    ais_path = DATA_ROOT / "ais_noaa_fixture_v1.json"
    write_json(av_path, {"metadata": av_bundle.metadata, "trajectories": av_bundle.trajectories})
    write_json(ais_path, {"metadata": ais_bundle.metadata, "trajectories": ais_bundle.trajectories})

    source_checks = {
        "argoverse_av2": {
            "url": "https://argoverse.org/av2.html",
            "probe": probe_url("https://argoverse.org/av2.html"),
        },
        "noaa_ais": {
            "url": "https://marinecadastre.gov/ais/",
            "probe": probe_url("https://marinecadastre.gov/ais/"),
        },
        "acm_2025_benchmark": {
            "url": "https://dl.acm.org/doi/10.1145/3764920.3770598",
            "probe": probe_url("https://dl.acm.org/doi/10.1145/3764920.3770598"),
        },
    }

    substitution_notes = []
    for key, check in source_checks.items():
        status = check["probe"]["status"]
        if not status.startswith("reachable:"):
            msg = f"{key} source probe failed ({status}); using schema-faithful deterministic fixture."
            write_resource_failure(msg)
            substitution_notes.append(
                {
                    "resource": key,
                    "substitution": "schema-faithful deterministic local fixture",
                    "comparability_impact": "MEDIUM",
                    "status": "INCONCLUSIVE_UNTIL_EQUIVALENCE_PROVEN",
                }
            )

    # Even when reachable, fixtures are locked for deterministic replay and offline execution.
    substitution_notes.append(
        {
            "resource": "argoverse_av2/noaa_ais runtime datasets",
            "substitution": "seed-locked schema-faithful fixtures for deterministic reproducibility",
            "comparability_impact": "LOW_TO_MEDIUM",
            "status": "EQUIVALENCE_PARTIAL_SCHEMA_LEVEL",
        }
    )

    dataset_lock = {
        "created_at_utc": now_utc_iso(),
        "seeds": {
            "master": 20260220,
            "av_suite": AV_SEED,
            "ais_suite": AIS_SEED,
            "adversarial": 20260223,
            "determinism_replay": [91001, 91002, 91003, 91004, 91005],
        },
        "sources": source_checks,
        "fixtures": [
            {
                "name": "argoverse2_schema_faithful_fixture_v1",
                "path": str(av_path),
                "sha256": sha256_file(av_path),
                "trajectory_count": len(av_bundle.trajectories),
                "snapshot_version": "2026-02-20",
            },
            {
                "name": "noaa_ais_schema_faithful_fixture_v1",
                "path": str(ais_path),
                "sha256": sha256_file(ais_path),
                "trajectory_count": len(ais_bundle.trajectories),
                "snapshot_version": "2026-02-20",
            },
        ],
        "substitution_notes": substitution_notes,
    }
    write_json(ARTIFACT_ROOT / "dataset_lock.json", dataset_lock)

    schema_inventory = {
        "created_at_utc": now_utc_iso(),
        "schemas": {
            "av_trajectory": {
                "required_fields": ["trajectory_id", "domain", "coord_system", "label", "points"],
                "point_fields": ["t", "x", "y", "speed", "cog"],
            },
            "ais_trajectory": {
                "required_fields": ["trajectory_id", "domain", "coord_system", "label", "points"],
                "point_fields": [
                    "t",
                    "lat",
                    "lon",
                    "speed",
                    "cog",
                    "timestamp_iso",
                    "mmsi",
                ],
            },
            "zpgeo_payload": {
                "magic": "ZPGEO1",
                "version": 1,
                "fields": [
                    "coord_flag",
                    "quant_step_cm",
                    "start_t",
                    "sample_dt_ms",
                    "step_count",
                    "run_count",
                    "origin",
                    "runs",
                ],
            },
            "search_index_row": {"fields": ["trajectory_id", "ground_truth", "scores"]},
            "integration_contract": {
                "fields": ["movingpandas_adapter", "autoware_plugin_stub", "schema_version", "status"]
            },
        },
    }
    write_json(ARTIFACT_ROOT / "schema_inventory.json", schema_inventory)
    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_A" / "gate_A_manifest.json",
        {
            "gate": "A",
            "artifacts": ["dataset_lock.json", "schema_inventory.json", "resource_failures.log"],
        },
    )
    append_command_log("python3 code/scripts/gate_a_lock.py", "Gate A complete")


if __name__ == "__main__":
    main()
