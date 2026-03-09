# RUNBOOK_ZPE_GEO_GATE_B

## Objective
Implement and validate core encode/decode path and baseline fidelity checks.

## Predeclared Commands
1. `python3 code/scripts/gate_b_core_checks.py`
2. `python3 code/scripts/validate_artifacts.py --gate B`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/gate_snapshots/gate_B/`

## Falsification Intent
- Stress high-curvature trajectories to attempt RMSE failure.
- Inject missing COG and heading conflicts to attempt AIS DTW failure.

## Pass Criteria
- AV RMSE <= 1.0 meter.
- AIS DTW <= 50.0 meters.
- No uncaught exceptions on malformed records.

## Fail Signatures
- RMSE > 1.0.
- DTW > 50.0.
- Any unhandled exception.

## Rollback
- Restore codec module from Gate A snapshot, patch minimal sections, rerun Gate B.

## Fallback
- If external geometry libs are unavailable, use stdlib haversine + dynamic programming DTW implementation.
