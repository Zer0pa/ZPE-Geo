<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

<h1 align="center">ZPE Geo</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v7.0-e5e7eb?labelColor=111111" alt="License: SAL v7.1"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-3.11%20%7C%203.12-e5e7eb?labelColor=111111" alt="Python 3.11 and 3.12"></a>
  <a href="proofs/artifacts/2026-03-21_operator_status/README.md"><img src="https://img.shields.io/badge/operator%20status-current%20pack-e5e7eb?labelColor=111111" alt="Operator status: current pack"></a>
</p>

ZPE-Geo is a deterministic trajectory codec: encode, compress, and search GPS and XY trajectories with bit-exact round-trip guarantees. It ships a repo-local Python package covering trajectory encoding, H3-backed spatial indexing, and maneuver-search over committed fixtures.

**Above baseline (real-world headline):** on a 34,668-way Rhode Island OSM extract, ZPE-Geo compresses JSON→zpgeo at **13.8× vs Douglas-Peucker 6.5×** at ε=0.5 m ([proof](proofs/artifacts/2026-02-20_zpe_geo_wave1/osm_parity_full_corpus_report.json)). Real-world AIS, GeoLife GPS, and OSM extracts land in the **12.7×–27.3×** band on the same DP calibration. Synthetic-fixture ceilings are higher and reported in the benchmarks section. ACM 2025 dataset alignment is INCONCLUSIVE — see §5 below. ZPE-Geo trades fidelity for compression on static road-graph data — DTW p95 32.4 m vs DP 16.8 m; acceptable for open-ocean AIS and long-haul fleet archival, not for road-graph navigation.

ZPE-Geo is one of 17 independent encoding products in the Zer0pa ZPE portfolio. It is useful now and improving continuously.

This README only keeps claims that are exercised by the repo CI test surface and anchored to proof files committed in this repository. Historical and operator-status material remains available through the proof anchors below.

## What This Is

Deterministic trajectory codec. Compact zpgeo packets, documented spatial error bounds, and sub-millisecond maneuver search. Install from PyPI: `pip install zpe-geo`

ZPE-Geo is a **trajectory archive and search codec** — not a navigation system, not a streaming playback codec, and not a lossless geometry store. Coordinate round-trip is lossy at the shipped quantization step (max absolute error 1.28 × 10⁻⁶° on AIS WGS84; 0.025 m on AV XY). The current Readiness verdict is BLOCKED.

## Codec Mechanics

<p>
  <img src=".github/assets/readme/lane-mechanics/GEO.gif" alt="ZPE-Geo Codec Mechanics animation" width="100%">
</p>

| Field | Value |
| ------- | ------- |
| Architecture | GEO_STREAM |
| Encoding | GEO_DELTA_V1 |
| Mechanics Asset | `.github/assets/readme/lane-mechanics/GEO.gif` |

## Key Metrics

| Metric | Value | Baseline |
| -------- | ------- | ---------- |
| COMPRESSION_AIS_SYNTHETIC | 450.8× mean | Douglas-Peucker 314.8× |
| COMPRESSION_AV_SYNTHETIC | 123.1× mean | — |
| MANEUVER_PRECISION | P@10 = 1.0 (all query types) | 210-traj fixture + 1,610-traj scale eval |
| QUERY_LATENCY_P95 | 0.040 ms mean / 0.064 ms p95 | Simulated 10 M trajectory corpus |

> Source: [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json), [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json), [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json), [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json)

## Repo Identity

| Field | Value |
| ------- | ------- |
| Identifier | ZPE-Geo |
| Repository | https://github.com/Zer0pa/ZPE-Geo |
| Section | encoding |
| Visibility | PUBLIC |
| Architecture | GEO_STREAM |
| Encoding | GEO_DELTA_V1 |
| Commit SHA | 62814a4c279f |
| License | SAL-7.0 |
| Authority Source | March 21 operator status pack |

## Readiness

| Field | Value |
| ------- | ------- |
| Verdict | BLOCKED |
| Checks | 8/8 |
| Anchors | 6 display anchors |
| Confidence | 62.5% |
| Commit | 62814a4c279f |
| Authority | March 21 operator status pack |

### Honest Blocker

No claim of blind-clone closure (GEO-C001); No claim of full-corpus closure (GEO-C002); No claim of release readiness (GEO-C004)

## What We Prove

- encode_trajectory and decode_trajectory round-trip shipped XY and WGS84 fixtures without dropping point counts — exercised by code/tests/test_codec.py, code/tests/test_roundtrip.py, code/tests/test_edge_cases.py → proofs/artifacts/fixture_benchmarks/
- ManeuverSearchIndex builds and answers deterministic label, bounding-box, and radius queries on repo-local fixtures with P@10 = 1.0 across all query types — exercised by code/tests/test_search.py, code/tests/test_search_comprehensive.py → geo_maneuver_search_eval.json
- H3Bridge round-trip and cell-path behavior stays stable across tested resolutions and edge coordinates — exercised by code/tests/test_h3bridge.py, code/tests/test_h3bridge_resolution.py → geo_h3_roundtrip_results.json
- The repo-root package installs as an editable package and builds as a distribution — GitHub Actions CI + local python -m build → TECHNICAL_ALIGNMENT_REPORT.md
- Compression ratio 13.8× mean on 34,668-way real-world OSM extract vs Douglas-Peucker 6.5× at ε=0.5 m — aggregate corpus, not single-sequence → osm_parity_full_corpus_report.json
- Query latency mean 0.040 ms, p95 0.064 ms on simulated 10 M trajectory corpus (deterministic index replication over 210-trajectory fixture) → geo_query_latency_benchmark.json
- Online encode latency mean 0.107 ms, p95 0.122 ms (threshold: 10 ms) across 39,907 streamed updates → geo_stream_latency.json
- Real-world AIS (21.0×), GeoLife GPS (27.3×), OSM Monaco (12.7×) compression ratios on 5-trajectory public-domain extracts → real_world_benchmarks/

## What We Don't Claim

- Lossless coordinate equality is not claimed. Round-trip error is bounded, not zero: max 1.28 × 10⁻⁶° on AIS WGS84, max 0.025 m on AV XY fixtures at the shipped quantization step.
- ACM 2025 dataset parity is INCONCLUSIVE — supplementary dataset alignment was not completed. The ACM 2025 comparison row is not an independently verified benchmark against the paper's dataset.
- Full-corpus aggregate fidelity on the 34,668-way Rhode Island OSM extract: DTW p95 32.4 m vs DP 16.8 m — this is a FAIL relative to Douglas-Peucker on static road-graph fidelity. Acceptable for archival use; not claimed suitable for road-graph navigation.
- The 10 M trajectory query latency result uses deterministic index replication over the 210-trajectory fixture; it is not a full-corpus live run.
- No real-time streaming reconstruction guarantee beyond the 10 ms p95 threshold documented in the stream latency artifact.
- No claim of superiority over all compression algorithms. Comparison is scoped to Douglas-Peucker with documented calibration parameters.
- This codec does not implement lossless geometry storage. It is not a substitute for formats requiring exact coordinate preservation (e.g., legal survey, precision navigation).

## Verification Status

| Code | Check | Verdict |
| ------ | ------- | --------- |
| V_01 | code/tests/test_codec.py — encode_trajectory / decode_trajectory round-trip; no point-count drop on XY and WGS84 fixtures | PASS |
| V_02 | code/tests/test_roundtrip.py — Byte-exact determinism; coordinate error within documented bounds | PASS |
| V_03 | code/tests/test_edge_cases.py — Edge coordinate inputs, empty trajectories, single-point degenerate cases | PASS |
| V_04 | code/tests/test_search.py — ManeuverSearchIndex label, bounding-box, radius queries on 210-traj fixture | PASS |
| V_05 | code/tests/test_search_comprehensive.py — P@10 = 1.0 across all query types; 1,610-traj scale eval | PASS |
| V_06 | code/tests/test_h3bridge.py — H3Bridge round-trip stability across tested resolutions | PASS |
| V_07 | code/tests/test_h3bridge_resolution.py — Cell-path behavior at edge coordinates; resolution sweep | PASS |
| V_08 | GitHub Actions CI — Package installs as editable; python -m build produces distribution | PASS |

## Proof Anchors

| Path | State |
| ------ | ------- |
| `proofs/artifacts/2026-03-21_operator_status/README.md` | VERIFIED |
| `proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json` | VERIFIED |
| `proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json` | VERIFIED |
| `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json` | VERIFIED |

> Display-anchor policy: the six rows above are the canonical proof-anchor set consumed by website sync. Additional artifact paths in support sections are supplemental evidence, not display anchors.

## Repo Shape

| Field | Value |
| ------- | ------- |
| Proof Anchors | 6 display anchors |
| Modality Lanes | 4 |
| Architecture | GEO_STREAM |
| Encoding | GEO_DELTA_V1 |
| Verification | 8/8 checks |
| Authority Source | March 21 operator status pack |

## Competitive Benchmarks

| Comparison | **ZPE-Geo** | Baseline | Dataset | Citation | Proof artifact |
|------------|-------------|----------|---------|---------|----------------|
| **Compression ratio mean (OSM full extract)** | **13.8×** | Douglas-Peucker 6.5× (ε=0.5 m) | 34,668-way Rhode Island OSM extract | Same DP calibration; `osm_parity_full_corpus_report.json` | [`osm_parity_full_corpus_report.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/osm_parity_full_corpus_report.json) |
| Compression ratio mean (AIS synthetic) | 450.8× | Douglas-Peucker 314.8× | 190-traj. NOAA AIS fixture (synthetic ceiling) | ACM 2025 in-lane DP framing — [dl.acm.org/doi/10.1145/3764920.3770598](https://dl.acm.org/doi/10.1145/3764920.3770598) | [`geo_ais_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json) |

Headline framing: the **real-world OSM row (13.8× vs DP 6.5×)** is the credibility-bearing comparison. The AIS synthetic row (450.8× vs DP 314.8×) is a **synthetic ceiling** — codec stress on schema-faithful generated trajectories, not real-world performance. Caveats: ACM 2025 paper dataset parity is INCONCLUSIVE (`geo_ais_benchmark.json` → `comparators.acm_2025_framing`) because supplementary dataset alignment was not completed; the DP numbers are from the repo's own in-lane calibration on the same fixtures, not lifted from the ACM paper. **Explicit fidelity disclosure:** ZPE-Geo trades fidelity for compression on static road-graph data — DTW p95 32.4 m vs DP 16.8 m at ε=0.5 m. Acceptable for open-ocean AIS and long-haul fleet archival; not acceptable for road-graph navigation.

## Quick Start

```bash
git clone https://github.com/Zer0pa/ZPE-Geo.git zpe-geo
cd zpe-geo
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,h3]"
python -m pytest code/tests -q
python -m build
```

## Upcoming Workstreams

This section captures the active lane priorities — what the next agent or contributor picks up, and what investors should expect. Cadence is continuous, not milestoned.

- **ACM 2025 dataset alignment resolution** — Research-Deferred — Investigation Underway. INCONCLUSIVE alignment must be diagnosed; either the comparison is fixed or the dataset is formally excluded with rationale.
- **Adaptive primitive for road-graph fidelity** — Research-Deferred — Investigation Underway. Foundations exist via H3 indexing; primitive-level investigation needed to close the regression vs Douglas-Peucker on static road graphs.

---

### Detail Tables

#### Compression Detail

| Dataset | Corpus | Compression (JSON→zpgeo) | Proof artifact |
| --- | --- | ---: | --- |
| NOAA AIS synthetic fixture | 190 trajectories | 450.8× mean, 475.3× median | [`geo_ais_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json) |
| Argoverse2 schema-faithful synthetic | 210 trajectories | 123.1× mean, 107.4× median | [`geo_av_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json) |
| NOAA AIS (real NOAA MarineCadastre extract) | 5 trajectories | 21.0× | [`noaa_ais_day_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json) |
| Microsoft GeoLife GPS (real extract) | 5 trajectories | 27.3× | [`geolife_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/geolife_extract_benchmark.json) |
| OSM Monaco highways (real Geofabrik extract) | 5 trajectories | 12.7× | [`osm_monaco_way_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/osm_monaco_way_extract_benchmark.json) |

Compression ratios compare uncompressed raw JSON payload bytes to encoded zpgeo payload bytes. Coordinate round-trip is lossy: max absolute error is 1.28 × 10⁻⁶° on AIS WGS84 fixtures ([`ais_noaa_fixture_v1_benchmark.json`](proofs/artifacts/fixture_benchmarks/ais_noaa_fixture_v1_benchmark.json) → `roundtrip.max_abs_coordinate_error`) and 0.025 m on AV XY fixtures ([`av_argoverse2_fixture_v1_benchmark.json`](proofs/artifacts/fixture_benchmarks/av_argoverse2_fixture_v1_benchmark.json) → `roundtrip.max_abs_coordinate_error`) at the shipped quantization step.

#### Fidelity Detail

| Dataset | Metric | Result | Threshold | Proof artifact |
| --- | --- | ---: | ---: | --- |
| NOAA AIS synthetic (190 traj.) | DTW mean | 2.6 m | — | [`geo_ais_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json) |
| NOAA AIS synthetic (190 traj.) | DTW p95 | 7.8 m | 50 m | [`geo_ais_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json) |
| Argoverse2 synthetic (210 traj.) | RMSE mean | 0.82 m | — | [`geo_av_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json) |
| Argoverse2 synthetic (210 traj.) | RMSE p95 | 1.86 m | — | [`geo_av_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json) |

#### Search Detail

| Metric | Result | Corpus | Proof artifact |
| --- | ---: | --- | --- |
| Maneuver label P@10 | 1.0 (all query types) | 210-trajectory fixture | [`geo_maneuver_search_eval.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json) |
| Maneuver label P@10 | 1.0 (all query types) | 1,610-trajectory scale eval | [`max_scale_search_eval.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/max_scale_search_eval.json) |
| Query latency mean | 0.040 ms | Simulated 10 M trajectory corpus | [`geo_query_latency_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json) |
| Query latency p95 | 0.064 ms | Simulated 10 M trajectory corpus | [`geo_query_latency_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json) |
| Online encode latency mean | 0.107 ms | 39,907 streamed updates | [`geo_stream_latency.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json) |
| Online encode latency p95 | 0.122 ms (threshold: 10 ms) | 39,907 streamed updates | [`geo_stream_latency.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json) |

The simulated 10 M corpus result uses deterministic index replication over the 210-trajectory fixture; it is not a full-corpus run.
