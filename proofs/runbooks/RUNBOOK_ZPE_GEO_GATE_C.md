# RUNBOOK_ZPE_GEO_GATE_C

## Objective
Produce comparator and performance matrix for AV/AIS compression, maneuver search, query latency, stream latency, and H3 roundtrip.

## Predeclared Commands
1. `python3 code/scripts/gate_c_benchmarks.py`
2. `python3 code/scripts/validate_artifacts.py --gate C`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/gate_snapshots/gate_C/`

## Falsification Intent
- Comparator: use difficult oscillatory traces to challenge compression ratio.
- Search: inject confusable maneuver negatives to reduce precision.
- Latency: stress 10M simulation under skew and hot/cold index cases.
- H3: perturb resolutions and boundary coordinates to induce mismatch.

## Pass Criteria
- AV CR >= 20x.
- AIS CR >= 25x.
- Maneuver P@10 >= 0.90.
- Query latency p95 < 1.0 s on 10M simulation.
- AIS online encode latency p95 < 10 ms.
- H3+ZPE roundtrip consistency = 100%.

## Fail Signatures
- Any threshold miss.
- Comparator output missing.
- Roundtrip mismatch count > 0.

## Rollback
- Restore Gate B snapshot, patch failing subsystem, rerun Gate C.

## Fallback
- If official H3 library unavailable, use deterministic H3-compatible adapter and classify equivalence confidence.
