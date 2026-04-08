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
```

## Artifact Routes

| Dataset | Script | Fixture | Artifact |
| --- | --- | --- | --- |
| NOAA AIS extract | `code/scripts/run_benchmark.py` | `code/fixtures/real_world/noaa_ais_day_extract.json` | `proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json` |
| GeoLife extract | `code/scripts/run_benchmark.py` | `code/fixtures/real_world/geolife_extract.json` | `proofs/artifacts/real_world_benchmarks/geolife_extract_benchmark.json` |
| OSM Monaco extract | `code/scripts/run_benchmark.py` | `code/fixtures/real_world/osm_monaco_way_extract.json` | `proofs/artifacts/real_world_benchmarks/osm_monaco_way_extract_benchmark.json` |
| H3 integration | `code/scripts/benchmark_h3_integration.py` | `code/fixtures/real_world/*.json` | `proofs/artifacts/h3_benchmarks/h3_integration_benchmark.json` |

## Notes

- This document currently publishes the reproducible method and artifact routes.
- Current numeric benchmark claims remain in the linked machine-readable artifacts until a consolidated summary table is regenerated.
