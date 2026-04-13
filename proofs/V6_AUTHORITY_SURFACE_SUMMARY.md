# V6 Authority Surface Summary

Date: 2026-04-14

This file consolidates the V6 README Key Metrics from retained proof artifacts already present in the repo. It does not change the governing current verdict: `NOT_RELEASE_READY` with `max_wave_overall_go=false`.

## Current-State Metrics

| Metric | Value | Derivation | Source |
|--------|-------|------------|--------|
| CONFIDENCE | 62.5% (5/8 green) | `5` current PASS claims out of `8` tracked claims in the March 21 claim map | [FINAL_STATUS.md](FINAL_STATUS.md), [artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| OPEN_GATES | 3 | `GEO-C001`, `GEO-C002`, and `GEO-C004` remain unresolved | [FINAL_STATUS.md](FINAL_STATUS.md), [artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| VERIFICATION | 3/6 pass | Six retained checks below: `3` PASS and `3` FAIL | Six-check matrix below |

## Six-Check Verification Surface

| Check | Verdict | Source |
|-------|---------|--------|
| REPO-LOCAL_PACKAGE_SURFACE | PASS | [artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md](artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md) |
| LIGHTWEIGHT_CODE_TESTS | PASS | [artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md](artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md) |
| GEO-C001 | FAIL_RESOURCE_ATTEMPT | [artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| GEO-C002 | FAIL_RESOURCE_ATTEMPT | [artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| GEO-C004 | FAIL_RESOURCE_ATTEMPT | [artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| H3_ROUNDTRIP_CONSISTENCY | PASS | [artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json](artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json) |

## Historical Comparator Surface

| Metric | Value | Comparator | Source |
|--------|-------|------------|--------|
| AIS_CR | 475× median | vs Douglas-Peucker ~315× | [CONSOLIDATED_PROOF_REPORT.md](CONSOLIDATED_PROOF_REPORT.md), [artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json](artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json) |

The AIS comparator row above is retained historical benchmark evidence only. It does not override the current March 21 red-state operator posture or release block.
