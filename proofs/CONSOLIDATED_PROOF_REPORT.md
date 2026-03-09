# Consolidated Proof Report

Date: 2026-03-09
Bundle anchor: `proofs/artifacts/2026-02-20_zpe_geo_wave1/`

## Core Claim Table

| Claim | Threshold | Current bundled result | Evidence |
| --- | --- | --- | --- |
| `GEO-C001` | AV compression ratio `>= 20x` | median `107.39x` | `geo_av_benchmark.json` |
| `GEO-C002` | AIS compression ratio `>= 25x` | median `475.32x` | `geo_ais_benchmark.json` |
| `GEO-C003` | AV RMSE `<= 1 m` | mean `0.823 m` | `geo_av_fidelity.json` |
| `GEO-C004` | AIS DTW `<= 50 m` | mean `2.619 m` | `geo_ais_fidelity.json` |
| `GEO-C005` | maneuver `P@10 >= 0.90` | mean `1.0` | `geo_maneuver_search_eval.json` |
| `GEO-C006` | query latency `< 1 s` | p95 `0.064 ms` at simulated `10,000,200` corpus size | `geo_query_latency_benchmark.json` |
| `GEO-C007` | AIS online encode `< 10 ms` | p95 `0.122 ms` | `geo_stream_latency.json` |
| `GEO-C008` | H3 roundtrip consistency | `official_h3`, `0` failures | `geo_h3_roundtrip_results.json` |

## Core Bundle Reality

- `quality_gate_scorecard.json` reports `overall_pass=true`
- `claim_status_delta.md` records all eight claims as `PASS`
- `residual_risk_register.md` still keeps `R-01`, `R-02`, and `R-03` open

## Contradictions Preserved In The Bundle

1. `max_gate_matrix.json` reports max-gate success while `max_claim_resource_map.json` still contains `FAIL_FULL_CORPUS_NOT_EXECUTED` rows.
2. `net_new_gap_closure_matrix.json` conflicts with `runpod_readiness_manifest.json` on whether RunPod is required.
3. Several archived files still refer to stale `/Users/prinivenpillay/...` absolute paths.

These are not patched out of the archived bundle. They remain visible because the repo is preserving evidence, not rewriting history.

## Archived Bundle Limits

The proof bundle was produced before clean repo extraction. As a result:

- some artifact paths still reference the old lane layout
- some files refer to `data/fixtures/` and `data/external_samples/` instead of the staged repo layout
- some max-wave outputs disagree with one another

Use the staged docs to understand those limits. Use the archived bundle to inspect the raw evidence that created them.
