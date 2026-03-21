<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Consolidated Proof Report

Date: 2026-03-21<br>
Current operator pack anchor: [artifacts/2026-03-21_operator_status/](artifacts/2026-03-21_operator_status/)<br>
Historical bundle anchor: [artifacts/2026-02-20_zpe_geo_wave1/](artifacts/2026-02-20_zpe_geo_wave1/)

<p>
  <img src="../.github/assets/readme/section-bars/evidence.svg" alt="EVIDENCE" width="100%">
</p>

## Current Operator Evidence

The March 21 copied-back operator pack outranks the archived bundle for anything claimed as true now.

| Surface | Current result | Evidence |
| --- | --- | --- |
| Overall max-wave posture | `max_wave_overall_go=false` | [artifacts/2026-03-21_operator_status/phase0311_runpod/handoff_manifest.json](artifacts/2026-03-21_operator_status/phase0311_runpod/handoff_manifest.json) |
| Current red claims | `GEO-C001`, `GEO-C002`, `GEO-C004` -> `FAIL_RESOURCE_ATTEMPT` | [artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| Current green claims | `GEO-C003`, `GEO-C005`, `GEO-C006`, `GEO-C007`, `GEO-C008` -> `PASS` | [artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| AV2 durable continuation | `2425519440 / 50873856000` bytes completed with resume support | [artifacts/2026-03-21_operator_status/phase0311_runpod/max_av2_resume_state.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_av2_resume_state.json) |
| NOAA AIS durable continuation | `2 / 365` completed days, `14021403` rows, resume support enabled | [artifacts/2026-03-21_operator_status/phase0311_runpod/max_noaa_ais_resume_state.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_noaa_ais_resume_state.json) |
| Package alignment truth | standalone Python package candidate; `37 passed` on live and editable-install surfaces; wheel build succeeded; not a live public artifact yet | [artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md](artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md) |

<p>
  <img src="../.github/assets/readme/section-bars/summary.svg" alt="SUMMARY" width="100%">
</p>

## Historical Archived Metrics

The following rows are historical bundle facts only. They remain real archived results, but they are not current release authorization.

| Claim | Threshold | Historical archived result | Evidence |
| --- | --- | --- | --- |
| `GEO-C001` | AV compression ratio `>= 20x` | median `107.39x` | [artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json](artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json) |
| `GEO-C002` | AIS compression ratio `>= 25x` | median `475.32x` | [artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json](artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json) |
| `GEO-C003` | AV RMSE `<= 1 m` | mean `0.823 m` | [artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json](artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json) |
| `GEO-C004` | AIS DTW `<= 50 m` | mean `2.619 m` | [artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json](artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json) |
| `GEO-C005` | maneuver `P@10 >= 0.90` | mean `1.0` | [artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json](artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json) |
| `GEO-C006` | query latency `< 1 s` | p95 `0.064 ms` at simulated `10,000,200` corpus size | [artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json](artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json) |
| `GEO-C007` | AIS online encode `< 10 ms` | p95 `0.122 ms` | [artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json](artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json) |
| `GEO-C008` | H3 roundtrip consistency | `official_h3`, `0` failures | [artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json](artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json) |

## Historical Comparator Note

The archived AIS bundle includes an in-repo Douglas-Peucker comparison and beats that included baseline on compression ratio. This repo does not promote that historical result into a current parity or superiority claim.

<p>
  <img src="../.github/assets/readme/section-bars/evidence-dispute.svg" alt="EVIDENCE DISPUTE" width="100%">
</p>

## Contradictions Preserved

1. The February 20 handoff says all eight claims PASS and `max_wave_overall_go=true`, while the February 20 `max_claim_resource_map.json` still marks `GEO-C001`, `GEO-C002`, and `GEO-C004` as `FAIL_FULL_CORPUS_NOT_EXECUTED`.
2. The March 21 handoff is hybrid: it correctly preserves the current red-state outcome, but it also still embeds the February 20 `artifact_root` and historical `claim_statuses`.
3. The archived bundle contains a RunPod requirement disagreement between `net_new_gap_closure_matrix.json` and `runpod_readiness_manifest.json`.
4. Several archived files still carry stale absolute paths from the pre-extraction lane layout.

These contradictions remain visible because the repo preserves evidence rather than rewriting history.

<p>
  <img src="../.github/assets/readme/section-bars/open-risks-non-blocking.svg" alt="OPEN RISKS (NON-BLOCKING)" width="100%">
</p>

## Residual Risks Still Open

| Risk ID | Description | Status | Evidence |
| --- | --- | --- | --- |
| `R-01` | Schema-faithful fixtures used instead of full Argoverse2/NOAA corpora | OPEN | [artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md](artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md) |
| `R-02` | ACM supplementary dataset parity not proven directly in-lane | OPEN | [artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md](artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md) |
| `R-03` | Autoware plugin API stability not confirmed against roadmap | OPEN | [artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md](artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md) |
