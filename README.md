<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

<h1 align="center">ZPE Geo</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v7.0-e5e7eb?labelColor=111111" alt="License: SAL v7.0"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-3.11%20%7C%203.12-e5e7eb?labelColor=111111" alt="Python 3.11 and 3.12"></a>
  <a href="proofs/artifacts/2026-03-21_operator_status/README.md"><img src="https://img.shields.io/badge/operator%20status-current%20pack-e5e7eb?labelColor=111111" alt="Operator status: current pack"></a>
</p>

ZPE-Geo is a deterministic trajectory codec: encode, compress, and search GPS and XY trajectories with bit-exact round-trip guarantees. It ships a repo-local Python package covering trajectory encoding, H3-backed spatial indexing, and maneuver-search over committed fixtures.

**Above baseline:** on NOAA AIS synthetic trajectories (190-traj. fixture), ZPE-Geo compresses JSON→zpgeo at **450.8× mean** versus **Douglas-Peucker 314.8×** on the same fixture ([proof](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json)). On a 34,668-way Rhode Island OSM extract, **13.8× vs DP 6.5×** at ε=0.5 m ([proof](proofs/artifacts/2026-02-20_zpe_geo_wave1/osm_parity_full_corpus_report.json)). Both comparisons use in-lane DP calibration runs on the same data; ACM 2025 dataset alignment is INCONCLUSIVE — see caveats below.

ZPE-Geo is one of 17 independent encoding products in the Zer0pa ZPE portfolio. It is useful now and improving continuously.

This README only keeps claims that are exercised by the repo CI test surface and anchored to proof files committed in this repository. Historical and operator-status material remains available through the proof routes below.

## What This Is

ZPE-Geo encodes trajectories to a compact binary format (`zpgeo`), preserving spatial fidelity within documented error bounds, and indexes them for sub-millisecond maneuver search. The codec is deterministic: the same input always produces the same output, byte for byte.

## CI-Exercised Surface

| Claim | CI coverage | Proof artifact |
| --- | --- | --- |
| `encode_trajectory` and `decode_trajectory` round-trip shipped XY and WGS84 fixtures without dropping point counts | `code/tests/test_codec.py`, `code/tests/test_roundtrip.py`, `code/tests/test_edge_cases.py` | [`proofs/artifacts/fixture_benchmarks/`](proofs/artifacts/fixture_benchmarks/) |
| `ManeuverSearchIndex` builds and answers deterministic label, bounding-box, and radius queries on repo-local fixtures | `code/tests/test_search.py`, `code/tests/test_search_comprehensive.py` | [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json) |
| `H3Bridge` roundtrip and cell-path behavior stays stable across tested resolutions and edge coordinates | `code/tests/test_h3bridge.py`, `code/tests/test_h3bridge_resolution.py` | [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json) |
| The repo-root package surface installs as an editable package and builds as a distribution | GitHub Actions `CI`, local `python -m build` | [`proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md`](proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md) |

## Performance Metrics

All numbers below are generated from committed proof artifacts. Fixture-level benchmarks use synthetic schema-faithful data. Real-world extracts use public-domain or open-license sources.

### Compression

| Dataset | Corpus | Compression (JSON→zpgeo) | Proof artifact |
| --- | --- | ---: | --- |
| NOAA AIS synthetic fixture | 190 trajectories | 450.8× mean, 475.3× median | [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json) |
| Argoverse2 schema-faithful synthetic | 210 trajectories | 123.1× mean, 107.4× median | [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json) |
| NOAA AIS (real NOAA MarineCadastre extract) | 5 trajectories | 21.0× | [`proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json) |
| Microsoft GeoLife GPS (real extract) | 5 trajectories | 27.3× | [`proofs/artifacts/real_world_benchmarks/geolife_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/geolife_extract_benchmark.json) |
| OSM Monaco highways (real Geofabrik extract) | 5 trajectories | 12.7× | [`proofs/artifacts/real_world_benchmarks/osm_monaco_way_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/osm_monaco_way_extract_benchmark.json) |

Compression ratios compare uncompressed raw JSON payload bytes to encoded zpgeo payload bytes. Coordinate roundtrip is lossy: max absolute error is 1.28 × 10⁻⁶° on AIS WGS84 fixtures ([`proofs/artifacts/fixture_benchmarks/ais_noaa_fixture_v1_benchmark.json`](proofs/artifacts/fixture_benchmarks/ais_noaa_fixture_v1_benchmark.json) → `roundtrip.max_abs_coordinate_error`) and 0.025 m on AV XY fixtures ([`proofs/artifacts/fixture_benchmarks/av_argoverse2_fixture_v1_benchmark.json`](proofs/artifacts/fixture_benchmarks/av_argoverse2_fixture_v1_benchmark.json) → `roundtrip.max_abs_coordinate_error`) at the shipped quantization step.

### Fidelity

| Dataset | Metric | Result | Threshold | Proof artifact |
| --- | --- | ---: | ---: | --- |
| NOAA AIS synthetic (190 traj.) | DTW mean | 2.6 m | — | [`geo_ais_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json) |
| NOAA AIS synthetic (190 traj.) | DTW p95 | 7.8 m | 50 m | [`geo_ais_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json) |
| Argoverse2 synthetic (210 traj.) | RMSE mean | 0.82 m | — | [`geo_av_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json) |
| Argoverse2 synthetic (210 traj.) | RMSE p95 | 1.86 m | — | [`geo_av_fidelity.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json) |

### Search

| Metric | Result | Corpus | Proof artifact |
| --- | ---: | --- | --- |
| Maneuver label P@10 | 1.0 (all query types) | 210-trajectory fixture | [`geo_maneuver_search_eval.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json) |
| Maneuver label P@10 | 1.0 (all query types) | 1,610-trajectory scale eval | [`max_scale_search_eval.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/max_scale_search_eval.json) |
| Query latency mean | 0.040 ms | Simulated 10 M trajectory corpus | [`geo_query_latency_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json) |
| Query latency p95 | 0.064 ms | Simulated 10 M trajectory corpus | [`geo_query_latency_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json) |
| Online encode latency mean | 0.107 ms | 39,907 streamed updates | [`geo_stream_latency.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json) |
| Online encode latency p95 | 0.122 ms (threshold: 10 ms) | 39,907 streamed updates | [`geo_stream_latency.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json) |

The simulated 10 M corpus result uses deterministic index replication over the 210-trajectory fixture; it is not a full-corpus run.

### Comp Benchmarks vs Prior Art

| Comparison | ZPE-Geo | Baseline | Dataset | Citation | Proof artifact |
| --- | ---: | ---: | --- | --- | --- |
| Compression ratio mean (AIS synthetic) | 450.8× | Douglas-Peucker 314.8× | 190-traj. NOAA AIS fixture | ACM 2025 in-lane DP framing — [dl.acm.org/doi/10.1145/3764920.3770598](https://dl.acm.org/doi/10.1145/3764920.3770598) | [`geo_ais_benchmark.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json) |
| Compression ratio mean (OSM full extract) | 13.8× | Douglas-Peucker 6.5× (ε=0.5 m) | 34,668-way Rhode Island OSM extract | Same DP calibration; `osm_parity_full_corpus_report.json` | [`osm_parity_full_corpus_report.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/osm_parity_full_corpus_report.json) |

Caveats: The ACM 2025 paper dataset parity is labeled INCONCLUSIVE in the proof record (`geo_ais_benchmark.json` → `comparators.acm_2025_framing`) because supplementary dataset alignment was not completed. The DP compression numbers are generated from the repo's own DP calibration runs on the same fixtures; they are not taken from the ACM paper directly. DTW fidelity parity on the OSM full extract: ZPE p95 32.4 m vs DP p95 16.8 m at ε=0.5 m — ZPE trades some fidelity for higher compression on static road-graph data.

## Quick Verify

```bash
git clone https://github.com/Zer0pa/ZPE-Geo.git zpe-geo
cd zpe-geo
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,h3]"
python -m pytest code/tests -q
python -m build
```

## Proof Routes

| Route | Purpose |
| --- | --- |
| [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) | Current copied-back operator-status pack |
| [proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) | Current claim/resource split |
| [proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md](proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md) | Package-alignment evidence |
| [proofs/artifacts/2026-02-20_zpe_geo_wave1/](proofs/artifacts/2026-02-20_zpe_geo_wave1/) | Historical archived bundle |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Repo structure and evidence map |
| [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) | Public evidence boundary |
| [code/README.md](code/README.md) | Install-facing package details |

## Package Surface

The public repo-local import surface is:

- `zpe_geo.encode_trajectory`
- `zpe_geo.decode_trajectory`
- `zpe_geo.H3Bridge`
- `zpe_geo.ManeuverSearchIndex`

See [LICENSE](LICENSE) for the governing license text.
