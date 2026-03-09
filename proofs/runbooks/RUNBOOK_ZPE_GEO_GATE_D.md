# RUNBOOK_ZPE_GEO_GATE_D

## Objective
Run adversarial/malformed campaigns, determinism replay, and regression verification.

## Predeclared Commands
1. `python3 code/scripts/gate_d_falsification.py`
2. `python3 -m unittest discover -s code/tests -p 'test_*.py' > proofs/artifacts/2026-02-20_zpe_geo_wave1/regression_results.txt 2>&1`
3. `python3 code/scripts/validate_artifacts.py --gate D`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/falsification_results.md`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/determinism_replay_results.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/regression_results.txt`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/gate_snapshots/gate_D/`

## Falsification Campaigns
- DT-GEO-1 malformed coordinate/timestamp and CRS contamination.
- DT-GEO-2 extreme maneuver bursts (zig-zag, stop-go oscillation).
- DT-GEO-3 missing/invalid COG and inferred-heading conflicts.
- DT-GEO-4 deterministic replay on mixed AV+AIS corpus.
- DT-GEO-5 H3 resolution perturbation and drift stress.

## Pass Criteria
- 0 uncaught crashes across all campaigns.
- Determinism replay hash consistency 5/5.
- Regression suite all pass.

## Fail Signatures
- Any uncaught crash.
- Determinism mismatch.
- Regression test failure.

## Rollback
- Restore Gate C snapshot, patch minimal fault source, rerun Gate D and downstream.

## Fallback
- If a dependency fails during stress run, route to nearest local deterministic implementation and mark comparability impact as `INCONCLUSIVE` until proven.
