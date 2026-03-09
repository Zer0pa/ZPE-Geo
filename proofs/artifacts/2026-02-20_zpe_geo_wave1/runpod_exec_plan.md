# RunPod Exec Plan

## Image / Runtime
1. Base image: Ubuntu 22.04 + Python 3.11 + CUDA 12.x.
2. Install ROS2 Humble, colcon, vcs, and Autoware build deps.
3. Install pinned Python dependencies from `runpod_requirements_lock.txt`.

## Exact Command Chain
```bash
set -euo pipefail
set -a; [ -f .env ] && source .env; set +a
python3 scripts/gate_m1_max_resources.py
python3 scripts/gate_m2_autoware_attempt.py
python3 scripts/gate_m3_scale_search.py
python3 scripts/gate_m4_risk_closure.py
python3 scripts/gate_e_netnew_package.py
```

## Expected Artifact Manifest
- `max_resource_lock.json`
- `dataset_subset_coverage_report.json`
- `trajectory_stratified_error_report.json`
- `autoware_smoke_results.json`
- `max_scale_search_eval.json`
- `net_new_gap_closure_matrix.json`
- `max_claim_resource_map.json`
- `max_gate_matrix.json`
