# RUNBOOK_ZPE_GEO_GATE_E_NETNEW

## Objective
Package Appendix E NET-NEW artifacts, claim-resource mapping, IMP logs, and RunPod readiness.

## Predeclared Commands
1. `python3 code/scripts/gate_e_netnew_package.py`
2. `python3 code/scripts/validate_artifacts.py --gate E2`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/max_resource_validation_log.md`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/max_claim_resource_map.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/impracticality_decisions.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/runpod_readiness_manifest.json` (if any IMP-COMPUTE)
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/runpod_exec_plan.md` (if any IMP-COMPUTE)

## Fail Signatures
- Missing command evidence for attempted resources.
- IMP record lacks code/error/fallback/claim-impact fields.
- RunPod artifacts absent when IMP-COMPUTE exists.

## Rollback
Regenerate packaging from latest gate outputs; do not alter prior benchmark artifacts unless defect is found.
