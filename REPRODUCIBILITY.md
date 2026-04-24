# Reproducibility

ZPE-Geo is an always-in-beta geospatial trajectory codec. This file records the repo-local inputs and verification route that can be exercised from a fresh clone without raw external corpora.

## Canonical Inputs

- `code/fixtures/ais_noaa_fixture_v1.json`
- `code/fixtures/av_argoverse2_fixture_v1.json`
- `code/fixtures/real_world/geolife_extract.json`
- `code/fixtures/real_world/noaa_ais_day_extract.json`
- `code/fixtures/real_world/osm_monaco_way_extract.json`
- `proofs/artifacts/fixture_benchmarks/benchmark_summary.json`
- `proofs/artifacts/h3_benchmarks/h3_integration_benchmark.json`
- `proofs/artifacts/real_world_benchmarks/acquisition_report.json`

Raw external corpora, full RunPod execution state, and heavy validation payloads are outside the Git-backed repo unless explicitly copied back as compact proof artifacts.

## Golden-Bundle Hash

Placeholder: will be populated by the `receipt-bundle.yml` workflow in Wave 3.

## Verification Command

```bash
git clone https://github.com/Zer0pa/ZPE-Geo.git zpe-geo
cd zpe-geo
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,h3]"
python -m pytest code/tests -q
python - <<'PY'
from zpe_geo import H3Bridge, ManeuverSearchIndex, decode_trajectory, encode_trajectory
print("zpe-geo import OK")
print("h3 backend:", H3Bridge().backend)
print("search surface:", ManeuverSearchIndex.__name__)
PY
```

This command verifies the repo-local package and lightweight fixture-backed checks. It does not claim blind-clone closure, full-corpus closure, or release readiness.

## Supported Runtimes

- Python 3.11 or newer.
- Optional H3 backend via the `h3` extra (`python -m pip install -e ".[h3]"`).
- The fallback package surface remains importable without raw external corpora.
