#!/usr/bin/env python3
"""Appendix E packaging: NET-NEW artifacts and RunPod readiness."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from common import ARTIFACT_ROOT, init_artifact_root, write_json
from max_common import append_validation_log, load_impracticality, run_cmd
from zpe_geo.utils import append_command_log, now_utc_iso, write_text


def _safe_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resource_status(lock: dict[str, Any], key: str) -> str:
    res = lock.get(key, {})
    if not res:
        return "MISSING"
    if res.get("status") in {"FAILED", "PARSE_FAILED"}:
        return "FAILED"
    return "ATTEMPTED"


def _has_impr_code(impr: list[dict[str, Any]], resource_hint: str, code: str) -> bool:
    needle = resource_hint.lower()
    for row in impr:
        if str(row.get("impracticality_code", "")) != code:
            continue
        hay = f"{row.get('resource', '')} {row.get('claim_impact_note', '')}".lower()
        if needle in hay:
            return True
    return False


def _max_claim_status(
    claim_resources: list[str],
    resource_status: dict[str, str],
    impr: list[dict[str, Any]],
    paused_external_resources: set[str],
) -> str:
    if any(r in paused_external_resources for r in claim_resources):
        return "PAUSED_EXTERNAL"
    if any(resource_status.get(r) in {"FAILED", "MISSING"} for r in claim_resources):
        return "FAIL_RESOURCE_ATTEMPT"
    if any(resource_status.get(r) == "BLOCKED_LOCAL" for r in claim_resources):
        return "FAIL_RUNTIME_BLOCKED"
    if any(_has_impr_code(impr, r, "IMP-STORAGE") for r in claim_resources):
        return "FAIL_FULL_CORPUS_NOT_EXECUTED"
    if any(_has_impr_code(impr, r, "IMP-COMPUTE") for r in claim_resources):
        return "FAIL_RUNTIME_BLOCKED"
    return "PASS"


def _write_runpod_lockfile() -> str:
    out = run_cmd("python3 -m pip freeze | LC_ALL=C sort", timeout_s=120)
    content = out.stdout.strip()
    if not content:
        content = "# pip freeze unavailable in current runtime\n"
    if not content.endswith("\n"):
        content += "\n"
    rel = "runpod_requirements_lock.txt"
    write_text(ARTIFACT_ROOT / rel, content)
    return rel


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_e_netnew_package.py", "Gate E2 start")

    lock = _safe_json(ARTIFACT_ROOT / "max_resource_lock.json", {})
    impr = load_impracticality()
    impr_codes = [x.get("impracticality_code", "") for x in impr]
    gaps = _safe_json(ARTIFACT_ROOT / "net_new_gap_closure_matrix.json", {"gaps": []})
    m3 = _safe_json(ARTIFACT_ROOT / "max_scale_search_eval.json", {})
    autoware = _safe_json(ARTIFACT_ROOT / "autoware_smoke_results.json", {})
    handoff = _safe_json(ARTIFACT_ROOT / "handoff_manifest.json", {})
    commercial = _safe_json(ARTIFACT_ROOT / "commercialization_gate_report.json", {})

    paused_external_resources = set(commercial.get("paused_external_resources", []))
    resource_status = {
        "argoverse2": _resource_status(lock, "argoverse2"),
        "noaa_ais": _resource_status(lock, "noaa_ais"),
        "noaa_gfs_aws": _resource_status(lock, "noaa_gfs_aws"),
        "desi_dr1": _resource_status(lock, "desi_dr1"),
        "autoware_runtime": "PASS" if autoware.get("runtime_smoke_pass") else "BLOCKED_LOCAL",
    }
    claim_links: dict[str, list[str]] = {
        "GEO-C001": ["argoverse2"],
        "GEO-C002": ["argoverse2", "noaa_ais"],
        "GEO-C003": ["desi_dr1"],
        "GEO-C004": ["argoverse2", "noaa_ais"],
        "GEO-C005": ["noaa_gfs_aws"],
        "GEO-C006": ["noaa_gfs_aws"],
        "GEO-C007": ["desi_dr1"],
        "GEO-C008": ["desi_dr1", "autoware_runtime"],
    }
    claim_map = {
        "generated_at_utc": now_utc_iso(),
        "policy_note": "Appendix D7 requires full-corpus evidence; subset-only evidence cannot produce max-wave PASS for linked claims.",
        "resource_status": resource_status,
        "claim_links": {},
    }
    for cid, linked in claim_links.items():
        core_status = str(handoff.get("claim_statuses", {}).get(cid, {}).get("status", "UNKNOWN"))
        claim_map["claim_links"][cid] = {
            "resources": linked,
            "core_wave_status": core_status,
            "max_wave_status": _max_claim_status(linked, resource_status, impr, paused_external_resources),
        }
    write_json(ARTIFACT_ROOT / "max_claim_resource_map.json", claim_map)

    gap_status = {str(g.get("gap_id")): str(g.get("status")) for g in gaps.get("gaps", []) if g.get("gap_id")}

    gate_matrix = {
        "generated_at_utc": now_utc_iso(),
        "M1": bool((ARTIFACT_ROOT / "max_resource_lock.json").exists()),
        "M2": bool(autoware.get("runtime_smoke_pass", False)),
        "M3": bool(m3.get("pass", False)),
        "M4": all(
            str(g.get("status")) in {"CLOSED", "ACCEPTED_WITH_IMPACT", "NOT_REQUIRED", "PAUSED_EXTERNAL", "FAIL"}
            for g in gaps.get("gaps", [])
            if str(g.get("gap_id", "")).startswith(("D2-", "E-G", "F-G"))
        ),
        "E-G1": gap_status.get("E-G1") == "CLOSED",
        "E-G2": gap_status.get("E-G2") == "CLOSED",
        "E-G3": gap_status.get("E-G3") == "CLOSED",
        "E-G4": gap_status.get("E-G4") == "CLOSED",
        "E-G5": gap_status.get("E-G5") in {"CLOSED", "NOT_REQUIRED"},
        "F-G1": gap_status.get("F-G1") == "CLOSED",
        "F-G2": gap_status.get("F-G2") == "CLOSED",
    }

    requires_runpod = "IMP-COMPUTE" in impr_codes
    extra_files = [
        "max_resource_lock.json",
        "max_resource_validation_log.md",
        "max_claim_resource_map.json",
        "impracticality_decisions.json",
        "dataset_subset_coverage_report.json",
        "trajectory_stratified_error_report.json",
        "net_new_gap_closure_matrix.json",
        "max_gate_matrix.json",
    ]
    if requires_runpod:
        lockfile_rel = _write_runpod_lockfile()
        runpod_manifest = {
            "generated_at_utc": now_utc_iso(),
            "required": True,
            "trigger_code": "IMP-COMPUTE",
            "deferred_tasks": [
                "Autoware runtime smoke with ROS2 Humble + colcon",
                "Full-corpus AV2 + NOAA AIS replay batches",
                "Large-scale NOAA GFS archive replay",
            ],
            "hardware_profile": {"gpu": "NVIDIA A100/B200 class", "ram_gb_min": 64, "storage_gb_min": 300},
            "lockfile": lockfile_rel,
            "command_chain": [
                "set -euo pipefail",
                "python3 -m pip install -r runpod_requirements_lock.txt",
                "python3 code/scripts/gate_m1_max_resources.py",
                "python3 code/scripts/gate_m2_autoware_attempt.py",
                "python3 code/scripts/gate_m3_scale_search.py",
                "python3 code/scripts/gate_m4_risk_closure.py",
                "python3 code/scripts/gate_e_netnew_package.py",
            ],
            "expected_artifacts": [
                "max_resource_lock.json",
                "dataset_subset_coverage_report.json",
                "trajectory_stratified_error_report.json",
                "autoware_smoke_results.json",
                "max_scale_search_eval.json",
                "net_new_gap_closure_matrix.json",
                "max_claim_resource_map.json",
                "max_gate_matrix.json",
            ],
            "seed_policy": {
                "master_seed": 20260220,
                "av_seed": 20260221,
                "ais_seed": 20260222,
                "adversarial_seed": 20260223,
            },
        }
        write_json(ARTIFACT_ROOT / "runpod_readiness_manifest.json", runpod_manifest)
        plan_md = "\n".join(
            [
                "# RunPod Exec Plan",
                "",
                "## Image / Runtime",
                "1. Base image: Ubuntu 22.04 + Python 3.11 + CUDA 12.x.",
                "2. Install ROS2 Humble, colcon, vcs, and Autoware build deps.",
                "3. Install pinned Python dependencies from `runpod_requirements_lock.txt`.",
                "",
                "## Exact Command Chain",
                "```bash",
                "set -euo pipefail",
                "set -a; [ -f .env ] && source .env; set +a",
                "python3 code/scripts/gate_m1_max_resources.py",
                "python3 code/scripts/gate_m2_autoware_attempt.py",
                "python3 code/scripts/gate_m3_scale_search.py",
                "python3 code/scripts/gate_m4_risk_closure.py",
                "python3 code/scripts/gate_e_netnew_package.py",
                "```",
                "",
                "## Expected Artifact Manifest",
                "- `max_resource_lock.json`",
                "- `dataset_subset_coverage_report.json`",
                "- `trajectory_stratified_error_report.json`",
                "- `autoware_smoke_results.json`",
                "- `max_scale_search_eval.json`",
                "- `net_new_gap_closure_matrix.json`",
                "- `max_claim_resource_map.json`",
                "- `max_gate_matrix.json`",
            ]
        )
        write_text(ARTIFACT_ROOT / "runpod_exec_plan.md", plan_md + "\n")
        gate_matrix["E-G5"] = bool((ARTIFACT_ROOT / "runpod_readiness_manifest.json").exists())
        extra_files.extend(["runpod_readiness_manifest.json", "runpod_exec_plan.md", lockfile_rel])
    else:
        gate_matrix["E-G5"] = True

    write_json(ARTIFACT_ROOT / "max_gate_matrix.json", gate_matrix)

    handoff["max_wave_files"] = sorted(set(handoff.get("max_wave_files", []) + extra_files))
    handoff["max_wave_gate_matrix"] = gate_matrix
    handoff["max_wave_overall_go"] = all(
        gate_matrix[g]
        for g in ("M1", "M2", "M3", "M4", "E-G1", "E-G2", "E-G3", "E-G4", "E-G5", "F-G1", "F-G2")
    )
    write_json(ARTIFACT_ROOT / "handoff_manifest.json", handoff)

    append_validation_log(
        [
            "",
            f"## Gate E2 ({now_utc_iso()})",
            f"- RunPod required: {requires_runpod}",
            f"- Max-wave overall go: {handoff['max_wave_overall_go']}",
            f"- Gates: {gate_matrix}",
        ]
    )
    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_E2" / "gate_E2_manifest.json",
        {
            "gate": "E2",
            "artifacts": extra_files,
        },
    )
    append_command_log("python3 code/scripts/gate_e_netnew_package.py", "Gate E2 complete")


if __name__ == "__main__":
    main()
