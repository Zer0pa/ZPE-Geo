# RUNBOOK_ZPE_GEO_GATE_M2

## Objective
Attempt Autoware runtime integration with pinned versions and compatibility smoke evidence.

## Predeclared Commands
1. `python3 code/scripts/gate_m2_autoware_attempt.py`
2. `python3 code/scripts/validate_artifacts.py --gate M2`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/autoware_version_matrix.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/autoware_smoke_results.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/impracticality_decisions.json` (if needed)

## Fail Signatures
- No pinned version matrix.
- No runtime attempt evidence.
- No IMP block when runtime cannot execute locally.

## Rollback
Keep integration contract stable, patch only failing smoke scripts, rerun M2.

## Fallback
If ROS2/Autoware runtime cannot be provisioned locally within lane constraints, emit RunPod-ready smoke plan and mark M2 dependent claims `INCONCLUSIVE`.
