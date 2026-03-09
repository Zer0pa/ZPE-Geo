# RUNBOOK_ZPE_GEO_GATE_F

## Objective
Execute Appendix F closure: commercial-safe parity rerun on OpenStreetMap extract, quantify stratified outcomes, and close `F-G1`/`F-G2` with explicit `PASS`/`FAIL`/`PAUSED_EXTERNAL` status.

## Inputs
1. `proofs/artifacts/2026-02-20_zpe_geo_wave1/net_new_gap_closure_matrix.json`
2. `proofs/artifacts/2026-02-20_zpe_geo_wave1/impracticality_decisions.json`
3. `proofs/artifacts/2026-02-20_zpe_geo_wave1/max_claim_resource_map.json`
4. External gap-closure concept note if available in the outer operator workspace; otherwise treat as reference-missing and continue on bundle evidence.

## Deterministic Policy
- Seed: `20260221`
- Sorting: deterministic lexical ordering for way IDs and trajectory IDs.
- Hash: SHA256 for all downloaded source files and derived parity summary payload.

## Predeclared Commands
1. `python3 code/scripts/gate_f_parity_closure.py`
2. `python3 code/scripts/validate_artifacts.py --gate F`

## Expected Outputs
1. `proofs/artifacts/2026-02-20_zpe_geo_wave1/osm_parity_full_corpus_report.json`
2. `proofs/artifacts/2026-02-20_zpe_geo_wave1/commercialization_gate_report.json`
3. `proofs/artifacts/2026-02-20_zpe_geo_wave1/net_new_gap_closure_matrix.json` (updated with `F-G1`, `F-G2`)
4. `proofs/artifacts/2026-02-20_zpe_geo_wave1/max_gate_matrix.json` (updated with `F-G1`, `F-G2`)

## Falsification Intent (Popper-First)
1. Attempt to falsify parity by using curvy and dense-node OSM ways where simplification and quantization degrade fidelity.
2. Attempt to falsify search robustness with confusable turn/merge classes synthesized from OSM-derived trajectories.
3. Attempt to falsify commercialization safety by checking whether required parity depends on non-commercial/restricted datasets.

## Pass Criteria
1. `F-G1`: all previously `OPEN` parity entries are now `CLOSED`, `FAIL`, or `PAUSED_EXTERNAL` with evidence paths.
2. `F-G2`: OSM parity report exists with stratified metrics and deterministic lock/checksum metadata.
3. No residual `OPEN` or `INCONCLUSIVE` statuses remain in final gap matrix.

## Fail Signatures
1. OSM extract unavailable and no fallback evidence.
2. Stratified parity metrics missing required classes/bins.
3. Any unresolved `OPEN`/`INCONCLUSIVE` entries after adjudication.
4. `PAUSED_EXTERNAL` used without commercial-safety analysis evidence.

## Rollback
Restore previous `net_new_gap_closure_matrix.json` and `max_gate_matrix.json`, patch only gate-F logic, rerun Gate F then re-run E2 packaging.

## Fallback
If full OSM PBF fetch fails, fallback to OSM public API extraction with deterministic bounding box and explicit representativeness impact; if neither available, mark dependent parity `FAIL` with command evidence.
