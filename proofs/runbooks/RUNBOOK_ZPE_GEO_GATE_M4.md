# RUNBOOK_ZPE_GEO_GATE_M4

## Objective
Close or explicitly accept all prior open residual risks with quantified impact.

## Predeclared Commands
1. `python3 code/scripts/gate_m4_risk_closure.py`
2. `python3 code/scripts/validate_artifacts.py --gate M4`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/net_new_gap_closure_matrix.json`

## Fail Signatures
- Residual risks without closure status.
- Missing quantitative impact field.

## Rollback
Patch risk mapping only and rerun M4.

## Fallback
If closure cannot be proven, mark as `ACCEPTED_WITH_IMPACT` or `OPEN` and force GO/NO-GO downgrade.
