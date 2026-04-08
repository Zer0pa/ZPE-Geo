# Benchmarks

## Methodology

Run all benchmark commands from the repo root after creating the local virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[test,h3]"
make benchmark
```

Real-world extracts reuse the committed public-source fixtures already shipped in this repo:

```bash
make benchmark-real-world
.venv/bin/python code/scripts/benchmark_h3_integration.py
.venv/bin/python code/scripts/benchmark_real_world_baselines.py
```

The current baseline comparison route uses:

- `gzip` on canonical per-trajectory JSON bytes
- `Douglas-Peucker` using the in-repo comparator at `epsilon_m = 12.0`
- current ZPE encoded payload size from `code/scripts/run_benchmark.py`

## Dataset Coverage

| Dataset | Status | Route |
| --- | --- | --- |
| NOAA AIS extract | completed | `proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json` |
| GeoLife extract | completed | `proofs/artifacts/real_world_benchmarks/geolife_extract_benchmark.json` |
| OSM Monaco extract | completed | `proofs/artifacts/real_world_benchmarks/osm_monaco_way_extract_benchmark.json` |
| OpenSky scientific datasets | blocked in this repo pass | Public dataset page exists at `https://opensky-network.org/data/scientific`, but unattended acquisition was not wired into this repo pass, so no OpenSky metric is claimed here |

## Artifact Routes

| Dataset | Script | Fixture | Artifact |
| --- | --- | --- | --- |
| NOAA AIS extract | `code/scripts/run_benchmark.py` | `code/fixtures/real_world/noaa_ais_day_extract.json` | `proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json` |
| GeoLife extract | `code/scripts/run_benchmark.py` | `code/fixtures/real_world/geolife_extract.json` | `proofs/artifacts/real_world_benchmarks/geolife_extract_benchmark.json` |
| OSM Monaco extract | `code/scripts/run_benchmark.py` | `code/fixtures/real_world/osm_monaco_way_extract.json` | `proofs/artifacts/real_world_benchmarks/osm_monaco_way_extract_benchmark.json` |
| gzip + Douglas-Peucker baselines | `code/scripts/benchmark_real_world_baselines.py` | `code/fixtures/real_world/*.json` | `proofs/artifacts/baseline_benchmarks/real_world_baseline_summary.json` |
| H3 integration | `code/scripts/benchmark_h3_integration.py` | `code/fixtures/real_world/*.json` | `proofs/artifacts/h3_benchmarks/h3_integration_benchmark.json` |

## Published Summary Tables

| Dataset | Trajectories | Points | Raw JSON Bytes | ZPE Bytes | ZPE Ratio | Max Error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NOAA AIS extract | 5 | 60 | 8545 | 406 | 21.05x | 0.014429029350 |
| GeoLife extract | 5 | 160 | 17935 | 657 | 27.30x | 0.000549743650 |
| OSM Monaco extract | 5 | 100 | 6107 | 480 | 12.72x | 0.000311479106 |

| Dataset | Baseline | Baseline Bytes | ZPE Bytes | Improvement vs Baseline |
| --- | --- | ---: | ---: | ---: |
| NOAA AIS extract | gzip | 2009 | 406 | 4.95x |
| NOAA AIS extract | douglas_peucker | 520 | 406 | 1.28x |
| GeoLife extract | gzip | 2820 | 657 | 4.29x |
| GeoLife extract | douglas_peucker | 440 | 657 | 0.67x |
| OSM Monaco extract | gzip | 1728 | 480 | 3.60x |
| OSM Monaco extract | douglas_peucker | 424 | 480 | 0.88x |

The latest rerun-backed summary tables live in:

- `proofs/artifacts/baseline_benchmarks/README.md`
- `proofs/artifacts/baseline_benchmarks/real_world_baseline_summary.json`
- `proofs/artifacts/h3_benchmarks/h3_integration_benchmark.json`
