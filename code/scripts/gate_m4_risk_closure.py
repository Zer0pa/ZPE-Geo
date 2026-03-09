#!/usr/bin/env python3
"""Gate M4: residual risk closure and quantified gap matrix."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from common import ARTIFACT_ROOT, init_artifact_root, write_json
from max_common import append_validation_log, load_impracticality
from zpe_geo.utils import append_command_log, now_utc_iso


def _safe_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _upsert_gap(gaps: dict[str, dict[str, Any]], row: dict[str, Any]) -> None:
    gaps[row["gap_id"]] = row


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_m4_risk_closure.py", "Gate M4 start")

    impr = load_impracticality()
    impr_codes = [x.get("impracticality_code", "") for x in impr]
    max_lock = _safe_json(ARTIFACT_ROOT / "max_resource_lock.json", {})
    m3 = _safe_json(ARTIFACT_ROOT / "max_scale_search_eval.json", {})
    autoware = _safe_json(ARTIFACT_ROOT / "autoware_smoke_results.json", {})
    parity = _safe_json(ARTIFACT_ROOT / "osm_parity_full_corpus_report.json", {})
    commercialization = _safe_json(ARTIFACT_ROOT / "commercialization_gate_report.json", {})
    prior = _safe_json(ARTIFACT_ROOT / "net_new_gap_closure_matrix.json", {"gaps": []})

    has_imp_storage = any(c == "IMP-STORAGE" for c in impr_codes)
    has_imp_compute = any(c == "IMP-COMPUTE" for c in impr_codes)

    runpod_ready = (ARTIFACT_ROOT / "runpod_readiness_manifest.json").exists() and (
        ARTIFACT_ROOT / "runpod_exec_plan.md"
    ).exists()

    gaps: dict[str, dict[str, Any]] = {}
    for row in prior.get("gaps", []):
        if isinstance(row, dict) and row.get("gap_id"):
            gaps[str(row["gap_id"])] = row

    _upsert_gap(
        gaps,
        {
            "gap_id": "D2-GAP-01",
            "description": "Full Argoverse2 and NOAA AIS locked-corpus runs",
            "status": "ACCEPTED_WITH_IMPACT" if has_imp_storage else "CLOSED",
            "impact": "High evidence quality impact for max-wave full-corpus acceptance",
            "evidence": ["max_resource_lock.json", "impracticality_decisions.json"],
        },
    )
    _upsert_gap(
        gaps,
        {
            "gap_id": "D2-GAP-02",
            "description": "Autoware runtime pinned API integration",
            "status": "ACCEPTED_WITH_IMPACT"
            if not autoware.get("runtime_smoke_pass", False)
            else "CLOSED",
            "impact": "Integration-runtime confidence limited when local runtime cannot execute",
            "evidence": ["autoware_version_matrix.json", "autoware_smoke_results.json"],
        },
    )

    d2_gap03_status = "FAIL"
    d2_gap03_impact = "ACM supplementary parity unresolved."
    d2_gap03_evidence = ["innovation_delta_report.md", "concept_open_questions_resolution.md"]
    acm_gate = commercialization.get("acm_supplementary_parity", {})
    if acm_gate.get("status") == "PAUSED_EXTERNAL":
        d2_gap03_status = "PAUSED_EXTERNAL"
        d2_gap03_impact = str(acm_gate.get("reason", "Commercialization/licensing blocked with no open alternative."))
        d2_gap03_evidence.extend(["commercialization_gate_report.json"])
    elif parity.get("parity_pass") is True:
        d2_gap03_status = "CLOSED"
        d2_gap03_impact = "ACM framing parity closed via commercial-safe OSM full-extract benchmark evidence."
        d2_gap03_evidence.extend(["osm_parity_full_corpus_report.json", "commercialization_gate_report.json"])
    elif parity:
        d2_gap03_status = "FAIL"
        d2_gap03_impact = "OSM parity run executed but failed closure thresholds."
        d2_gap03_evidence.extend(["osm_parity_full_corpus_report.json", "commercialization_gate_report.json"])

    _upsert_gap(
        gaps,
        {
            "gap_id": "D2-GAP-03",
            "description": "ACM supplementary parity closure",
            "status": d2_gap03_status,
            "impact": d2_gap03_impact,
            "evidence": d2_gap03_evidence,
        },
    )

    _upsert_gap(
        gaps,
        {
            "gap_id": "E-G1",
            "description": "100% E3 resources attempted",
            "status": "CLOSED" if max_lock.get("resource_attempts") else "FAIL",
            "impact": "None",
            "evidence": ["max_resource_lock.json", "max_resource_validation_log.md"],
        },
    )
    _upsert_gap(
        gaps,
        {
            "gap_id": "E-G2",
            "description": "Core claims not closed on single-corpus evidence only",
            "status": "CLOSED" if max_lock.get("resource_attempts") else "FAIL",
            "impact": "Cross-resource evidence present but full-corpus constraints remain",
            "evidence": ["max_claim_resource_map.json", "max_resource_lock.json"],
        },
    )
    _upsert_gap(
        gaps,
        {
            "gap_id": "E-G3",
            "description": "Stratified error reporting",
            "status": "CLOSED" if (ARTIFACT_ROOT / "trajectory_stratified_error_report.json").exists() else "FAIL",
            "impact": "None",
            "evidence": ["trajectory_stratified_error_report.json"],
        },
    )
    _upsert_gap(
        gaps,
        {
            "gap_id": "E-G4",
            "description": "Skipped resource needs valid IMP record",
            "status": "CLOSED" if impr else "FAIL",
            "impact": "None",
            "evidence": ["impracticality_decisions.json"],
        },
    )
    _upsert_gap(
        gaps,
        {
            "gap_id": "E-G5",
            "description": "RunPod artifacts required when IMP-COMPUTE exists",
            "status": ("CLOSED" if runpod_ready else "FAIL") if has_imp_compute else "NOT_REQUIRED",
            "impact": "High if not provided",
            "evidence": ["runpod_readiness_manifest.json", "runpod_exec_plan.md"],
        },
    )

    fg2_closed = bool(
        parity
        and parity.get("stratified_metrics_present")
        and parity.get("extract_lock", {}).get("sha256")
    )
    _upsert_gap(
        gaps,
        {
            "gap_id": "F-G2",
            "description": "OSM full-extract parity evidence with stratified metrics",
            "status": "CLOSED" if fg2_closed else "FAIL",
            "impact": "Commercial-safe parity closure lacks hard evidence if FAIL.",
            "evidence": ["osm_parity_full_corpus_report.json", "commercialization_gate_report.json"],
        },
    )

    resolved_statuses = [
        str(gaps[g].get("status", "")).upper()
        for g in ("D2-GAP-01", "D2-GAP-02", "D2-GAP-03")
        if g in gaps
    ]
    fg1_closed = all(s not in {"OPEN", "INCONCLUSIVE"} for s in resolved_statuses)
    _upsert_gap(
        gaps,
        {
            "gap_id": "F-G1",
            "description": "All prior OPEN/INCONCLUSIVE parity entries resolved to explicit adjudication",
            "status": "CLOSED" if fg1_closed else "FAIL",
            "impact": "No unresolved OPEN/INCONCLUSIVE parity entries allowed at final phase; explicit FAIL is acceptable closure.",
            "evidence": ["net_new_gap_closure_matrix.json", "commercialization_gate_report.json"],
        },
    )

    ordered_ids = [
        "D2-GAP-01",
        "D2-GAP-02",
        "D2-GAP-03",
        "E-G1",
        "E-G2",
        "E-G3",
        "E-G4",
        "E-G5",
        "F-G1",
        "F-G2",
    ]
    ordered = [gaps[g] for g in ordered_ids if g in gaps]

    matrix = {
        "generated_at_utc": now_utc_iso(),
        "gaps": ordered,
        "m3_pass": bool(m3.get("pass", False)),
        "impracticality_count": len(impr),
        "has_open_or_inconclusive": any(
            str(g.get("status", "")).upper() in {"OPEN", "INCONCLUSIVE"} for g in ordered
        ),
    }
    write_json(ARTIFACT_ROOT / "net_new_gap_closure_matrix.json", matrix)
    append_validation_log(
        [
            "",
            f"## Gate M4 ({now_utc_iso()})",
            f"- Gap entries: {len(matrix['gaps'])}",
            f"- IMP entries: {len(impr)}",
            f"- M3 pass: {matrix['m3_pass']}",
            f"- has_open_or_inconclusive: {matrix['has_open_or_inconclusive']}",
        ]
    )
    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_M4" / "gate_M4_manifest.json",
        {"gate": "M4", "artifacts": ["net_new_gap_closure_matrix.json"]},
    )
    append_command_log("python3 code/scripts/gate_m4_risk_closure.py", "Gate M4 complete")


if __name__ == "__main__":
    main()
