# RUNBOOK_ZPE_GEO_GATE_E

## Objective
Package full artifact contract, adjudicate claims with evidence-only policy, compute quality scorecard, and issue GO/NO-GO.

## Predeclared Commands
1. `python3 code/scripts/gate_e_package.py`
2. `python3 code/scripts/validate_artifacts.py --gate E`

## Expected Outputs
- All mandatory PRD artifacts and rubric artifacts under `proofs/artifacts/2026-02-20_zpe_geo_wave1/`

## Pass Criteria
- Every required artifact file exists and is non-empty.
- Claim matrix status is evidence-bound with explicit file paths.
- Beyond-brief innovations are quantified and reproducible.
- No non-negotiable rubric gate failure.

## Fail Signatures
- Missing required artifact.
- Claim promoted without evidence path.
- Rubric non-negotiable failure.

## Rollback
- Recompute package from Gate D outputs; do not alter prior validated benchmark artifacts unless a defect is found.

## Fallback
- If any artifact cannot be conclusively proven, mark dependent claim `UNTESTED` or `INCONCLUSIVE` and issue `NO-GO`.
