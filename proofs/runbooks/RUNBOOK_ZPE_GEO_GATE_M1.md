# RUNBOOK_ZPE_GEO_GATE_M1

## Objective
Execute maximalization resource ingestion for AV2/NOAA AIS/NOAA GFS/DESI and generate subset lock + stratified error evidence.

## Predeclared Commands
1. `set -a; source .env; set +a`
2. `python3 code/scripts/gate_m1_max_resources.py`
3. `python3 code/scripts/validate_artifacts.py --gate M1`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/max_resource_lock.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/dataset_subset_coverage_report.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/trajectory_stratified_error_report.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/max_resource_validation_log.md`

## Popper/Kill Tests
1. Falsify heading quantization under jittery stop-go maritime tracks from attempted real AIS/GFS extracts.
2. Falsify long-haul fidelity under sparse-sampling subsets.
3. Falsify H3 sweep stability across r8-r12.

## Fail Signatures
- Any E3 resource not attempted.
- Subset lock missing checksums.
- Stratified report missing class-level error bins.

## Rollback
Restore prior green snapshot and re-run ingestion with minimal patch to failing parser/connector.

## Fallback
If full corpus is impractical, run locked subset + representativeness analysis and record IMP-* evidence.
