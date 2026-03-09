# RUNBOOK_ZPE_GEO_MASTER

## 1. Scope and Lane Lock
- Lane root: repo root `zpe-geo/`
- Operator-only sibling resources may still exist one level above the repo root under the outer workspace.
- Forbidden paths: other sector folders and any material outside the outer Geo workspace.
- All tracked implementation, docs, and proofs remain inside the repo root.

## 2. Read Order Completion
1. `README.md`
2. `proofs/FINAL_STATUS.md`
3. External operator references remain outside the repo and are reference-only.
4. Do not treat missing external reference docs as justification to widen the repo boundary.

## 3. Execution Order (Hard Gates)
1. Gate A: runbook + dataset lock + schema/inventory freeze.
2. Gate B: core encode/decode + baseline fidelity checks.
3. Gate C: AV/AIS comparator and performance matrix.
4. Gate D: adversarial + malformed + determinism campaigns.
5. Gate E: packaging + claim adjudication.
6. Gate M1: full-corpus/subset-locked maximalization metrics (AV2 + NOAA AIS + H3 sweep + CARLA stress path).
7. Gate M2: Autoware pinned runtime integration attempt and compatibility smoke evidence.
8. Gate M3: scale search + maneuver robustness on multi-resource ingestion.
9. Gate M4: residual-risk closure/acceptance with quantified impact.
10. Gate E2 / E-G1..E-G5: NET-NEW ingestion and RunPod readiness gates.
11. Gate F: Appendix F parity/commercialization closure (`F-G1`, `F-G2`).

No gate skipping. If a gate fails, patch minimally and rerun failed gate and all downstream gates.

## 4. Deterministic Seed Policy
- Master seed: `20260220`
- Additional deterministic seeds:
  - AV suite seed: `20260221`
  - AIS suite seed: `20260222`
  - Adversarial seed: `20260223`
  - Determinism replay seeds: `[91001, 91002, 91003, 91004, 91005]`
- RNG source: Python `random.Random(seed)` only.
- Hash algorithm for determinism checks: SHA256 over canonical JSON with sorted keys.

## 5. Command Ledger (Predeclared)
| ID | Command | Purpose | Expected Output | Fail Signature | Rollback/Fallback |
|---|---|---|---|---|---|
| CMD-A1 | `python3 code/scripts/gate_a_lock.py` | Freeze dataset snapshots and schema inventory | `proofs/artifacts/2026-02-20_zpe_geo_wave1/dataset_lock.json`, `schema_inventory.json` | Missing source/snapshot not written | Use synthetic schema-faithful fixtures; record substitution and impact |
| CMD-B1 | `python3 code/scripts/gate_b_core_checks.py` | Validate encode/decode and baseline fidelity | `geo_av_fidelity.json`, `geo_ais_fidelity.json` | RMSE/DTW threshold miss or crash | Patch codec and rerun Gate B |
| CMD-C1 | `python3 code/scripts/gate_c_benchmarks.py` | Compression, comparator, search, latency, stream, H3 checks | `geo_av_benchmark.json`, `geo_ais_benchmark.json`, `geo_maneuver_search_eval.json`, `geo_query_latency_benchmark.json`, `geo_stream_latency.json`, `geo_h3_roundtrip_results.json` | Threshold miss, missing comparator outputs | Patch metric-specific component, rerun Gate C |
| CMD-D1 | `python3 code/scripts/gate_d_falsification.py` | Run DT-GEO-1..DT-GEO-5 and determinism replay | `falsification_results.md`, `determinism_replay_results.json` | uncaught crash >0, deterministic mismatch | Patch robust handling, rerun Gate D + downstream |
| CMD-D2 | `python3 -m unittest discover -s code/tests -p 'test_*.py'` | Regression suite | `regression_results.txt` | Any test fail | Patch minimally then rerun tests and downstream |
| CMD-E1 | `python3 code/scripts/gate_e_package.py` | Build handoff contract, scorecard, claims, innovation delta | `handoff_manifest.json`, `before_after_metrics.json`, `claim_status_delta.md`, rubric outputs | Missing mandatory artifact or invalid manifest | Recompute packaging with strict artifact verification |
| CMD-M1 | `python3 code/scripts/gate_m1_max_resources.py` | Execute maximalization resource attempts and corpus lock | `max_resource_lock.json`, `dataset_subset_coverage_report.json`, `trajectory_stratified_error_report.json` | Resource attempt missing, lock absent, no stratified report | Record IMP-* with command evidence and rerun |
| CMD-M2 | `python3 code/scripts/gate_m2_autoware_attempt.py` | Attempt Autoware runtime integration with pinned matrix/smoke | `autoware_version_matrix.json`, `autoware_smoke_results.json` | No pinned matrix, no runtime attempt evidence | Record IMP-COMPUTE/IMP-ACCESS and produce RunPod handoff |
| CMD-M3 | `python3 code/scripts/gate_m3_scale_search.py` | Multi-resource latency/P@10 stress at scale | `max_scale_search_eval.json` | Threshold miss or no cross-resource evidence | Patch search/index and rerun M3+downstream |
| CMD-M4 | `python3 code/scripts/gate_m4_risk_closure.py` | Risk closure/acceptance quantification | `net_new_gap_closure_matrix.json` | Prior open risk neither closed nor accepted | Update mitigation and rerun M4 |
| CMD-E2 | `python3 code/scripts/gate_e_netnew_package.py` | Build NET-NEW ingestion artifacts and RunPod readiness | `max_resource_validation_log.md`, `max_claim_resource_map.json`, `impracticality_decisions.json`, `runpod_readiness_manifest.json`, `runpod_exec_plan.md` | Missing E5 artifacts or IMP record incomplete | Fill evidence block and rerun E2 |
| CMD-F1 | `python3 code/scripts/gate_f_parity_closure.py` | Execute Appendix F OSM parity + commercialization adjudication | `osm_parity_full_corpus_report.json`, `commercialization_gate_report.json`, `net_new_gap_closure_matrix.json` | `F-G1`/`F-G2` unresolved, missing OSM lock/checksum, unresolved status class | Patch parity/commercialization mapping and rerun F + downstream packaging |

## 6. Claim Falsification Matrix (Popper-First)
| Claim | Falsification attempt before promotion | Promotion condition | Evidence artifact |
|---|---|---|---|
| GEO-C001 (AV CR >=20x) | Force high-curvature/noisy AV path where RLE is weak | Median AV CR >=20x under locked suite | `geo_av_benchmark.json` |
| GEO-C002 (AIS CR >=25x) | Force oscillatory harbour AIS pattern and sparse straight-line mix | Median AIS CR >=25x and comparator included | `geo_ais_benchmark.json` |
| GEO-C003 (AV RMSE <=1m) | Stress high-speed heading changes | RMSE <=1m at 10Hz equivalent sampling | `geo_av_fidelity.json` |
| GEO-C004 (AIS DTW <=50m) | Missing/invalid COG with inferred heading conflicts | DTW <=50m under mixed COG validity | `geo_ais_fidelity.json` |
| GEO-C005 (P@10 >=0.90) | Hard negatives with confusable manoeuvres | P@10 >=0.90 for left-turn/lane-merge/stop | `geo_maneuver_search_eval.json` |
| GEO-C006 (<1s query latency) | 10M-corpus simulation with skewed class distribution | P95 latency <1s | `geo_query_latency_benchmark.json` |
| GEO-C007 (<10ms online encode) | Bursty vessel update stream with malformed rows | P95 encode latency <10ms/update | `geo_stream_latency.json` |
| GEO-C008 (H3 roundtrip) | Resolution perturbation stress and coordinate edge cases | 100% roundtrip consistency | `geo_h3_roundtrip_results.json` |

## 7. Failure Signatures and Stop Conditions
- Stop condition S1: Any uncaught exception in malformed/adversarial campaigns.
- Stop condition S2: Determinism replay mismatch for any of 5 seeds.
- Stop condition S3: Mandatory threshold miss after patch attempts.
- Stop condition S4: Missing evidence path for promoted claim.

## 8. Rollback Strategy
- Gate snapshots are stored under `proofs/artifacts/2026-02-20_zpe_geo_wave1/gate_snapshots/`.
- On failure:
  1. Restore from last green snapshot (`cp` from snapshot files).
  2. Apply minimal patch in source.
  3. Rerun failed gate and all downstream gates.
  4. Update `command_log.txt` with retry trace.

## 9. Resource Failure Protocol and Substitution
If external resource unavailable:
1. Capture failure in `resource_failures.log` (URL/path, timestamp, error).
2. Select nearest viable open substitute (schema-equivalent fixture or public mirror).
3. Record substitution in `concept_resource_traceability.json` with comparability impact.
4. Keep dependent outcomes `INCONCLUSIVE` unless equivalence is explicitly demonstrated.

## 10. Appendix B Traceability Plan (Predeclared)
| Appendix B item | Planned source | Planned evidence artifact | Fallback and impact policy |
|---|---|---|---|
| Argoverse 2 in AV benchmark | AV2 schema snapshot + AV-like fixture locked in Gate A | `dataset_lock.json`, `geo_av_benchmark.json` | If AV2 sample inaccessible, use schema-faithful fixture; mark comparability impact |
| NOAA AIS in maritime benchmark | NOAA AIS CSV schema snapshot + AIS-like fixture | `dataset_lock.json`, `geo_ais_benchmark.json` | If NOAA fetch unavailable, use NOAA-schema fixture; impact logged |
| Douglas-Peucker baseline | Local DP comparator implementation | `geo_ais_benchmark.json` | None (implemented in-lane) |
| H3 integration path | H3-compatible index bridge implemented in-lane | `geo_h3_roundtrip_results.json`, `schema_inventory.json` | If official lib unavailable, use deterministic compatible adapter and log |
| MovingPandas interoperability | Geo trajectory object adapter contract | `integration_readiness_contract.json` | If MovingPandas unavailable, provide API-compatible adapter contract |
| CARLA validation run | CARLA-kinematic fixture scenario | `falsification_results.md`, `geo_av_fidelity.json` | If CARLA runtime unavailable, run deterministic CARLA-profile synthetic scenario |
| Autoware integration contract | Stub plugin interface contract | `integration_readiness_contract.json` | Provide versioned stub contract with explicit limits |
| ACM 2025 framing | Competitive positioning table | `innovation_delta_report.md` | If paper dataset unavailable, keep benchmark framing INCONCLUSIVE |

## 11. Expected Final Artifact Root
`proofs/artifacts/2026-02-20_zpe_geo_wave1/`

Mandatory files from PRD and rubric are generated in Gate E.

## 12. Environment Bootstrap and Provenance Locks
1. Mandatory bootstrap command: `set -a; [ -f .env ] && source .env; set +a`.
2. Secret policy: never write token values to logs/artifacts; log only key presence.
3. `.env` parse errors are fail signatures and must be patched before gate execution.
4. NET-NEW resource inputs are locked with checksums:
   - `ZPE 10-Lane NET-NEW Resource Maximization Pack.md`
   - `ZPE 10-Lane NET-NEW Resource Maximization Pack.pdf`

## 13. Impracticality Policy (Appendix E)
- Allowed codes only: `IMP-LICENSE`, `IMP-ACCESS`, `IMP-COMPUTE`, `IMP-STORAGE`, `IMP-NOCODE`.
- Every IMP record must include:
  1. Command evidence.
  2. Error signature.
  3. Fallback action.
  4. Claim-impact note.
- Missing any IMP evidence block forces dependent claim status to `UNTESTED` or `INCONCLUSIVE`.

## 14. Appendix F Final-Phase Closure Policy
1. Execute OSM full-extract parity rerun on CPU-first path and produce stratified metrics (`F-G2` evidence).
2. Enforce commercialization gate:
   - Prefer commercial-safe ODbL/open-government resources.
   - If parity cannot be closed without non-commercial/restricted assets and no open commercial-safe substitute exists, mark `PAUSED_EXTERNAL`.
3. Status vocabulary for final-phase unresolved items:
   - `PASS`: threshold and parity closure evidenced.
   - `FAIL`: test executed but threshold/gate not met.
   - `PAUSED_EXTERNAL`: blocked by external commercial/licensing constraints with evidence.
4. Any residual `OPEN`/`INCONCLUSIVE` in final matrix is non-compliant and must be reclassified to `PASS`, `FAIL`, or `PAUSED_EXTERNAL` with artifact references.
