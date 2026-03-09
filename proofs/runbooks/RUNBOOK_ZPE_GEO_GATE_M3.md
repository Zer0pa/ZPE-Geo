# RUNBOOK_ZPE_GEO_GATE_M3

## Objective
Validate search latency and maneuver P@10 at scale under multi-resource ingestion context.

## Predeclared Commands
1. `python3 code/scripts/gate_m3_scale_search.py`
2. `python3 code/scripts/validate_artifacts.py --gate M3`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/max_scale_search_eval.json`

## Fail Signatures
- P@10 < 0.90.
- p95 latency >= 1 s.
- Missing cross-resource cohort analysis.

## Rollback
Patch index/search scoring only, rerun M3 and downstream packaging.

## Fallback
If one resource remains inaccessible, continue with available ingested sets and mark affected comparisons `INCONCLUSIVE` with IMP evidence.
