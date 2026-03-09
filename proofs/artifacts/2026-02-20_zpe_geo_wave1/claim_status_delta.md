# Claim Status Delta

| Claim ID | Claim | Pre-status | Post-status | Evidence |
|---|---|---|---|---|
| GEO-C001 | AV CR >= 20x | UNTESTED | PASS | `geo_av_benchmark.json` |
| GEO-C002 | AIS CR >= 25x | UNTESTED | PASS | `geo_ais_benchmark.json` |
| GEO-C003 | AV RMSE <= 1 m | UNTESTED | PASS | `geo_av_fidelity.json` |
| GEO-C004 | AIS DTW <= 50 m | UNTESTED | PASS | `geo_ais_fidelity.json` |
| GEO-C005 | Maneuver P@10 >= 0.90 | UNTESTED | PASS | `geo_maneuver_search_eval.json` |
| GEO-C006 | Search latency < 1 s | UNTESTED | PASS | `geo_query_latency_benchmark.json` |
| GEO-C007 | AIS online encode < 10 ms | UNTESTED | PASS | `geo_stream_latency.json` |
| GEO-C008 | H3 roundtrip consistent | UNTESTED | PASS | `geo_h3_roundtrip_results.json` |

## Max-Wave Cycle Delta (2026-02-21 Closure Loop)

| Item | Before | After | Evidence |
|---|---|---|---|
| M2 gate | FAIL | PASS | `autoware_smoke_results.json` |
| M4 gate | FAIL | PASS | `max_gate_matrix.json` |
| D2-GAP-02 (Autoware runtime pinned API integration) | ACCEPTED_WITH_IMPACT | CLOSED | `net_new_gap_closure_matrix.json` |
| D2-GAP-03 (ACM supplementary parity closure) | FAIL | CLOSED | `osm_parity_full_corpus_report.json`, `net_new_gap_closure_matrix.json` |
| GEO-C008 max-wave | FAIL_RUNTIME_BLOCKED | PASS | `max_claim_resource_map.json` |
