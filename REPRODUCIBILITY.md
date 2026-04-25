# Reproducibility

## Canonical Inputs

The committed fixture and corpus files that anchor repo-local verification are:

- `code/fixtures/av_argoverse2_fixture_v1.json`
- `code/fixtures/ais_noaa_fixture_v1.json`
- `code/fixtures/real_world/geolife_extract.json`
- `code/fixtures/real_world/noaa_ais_day_extract.json`
- `code/fixtures/real_world/osm_monaco_way_extract.json`

## Golden-Bundle Hash

This field will be populated by the `receipt-bundle.yml` workflow in Wave 3.

## Verification Command

The steps below are copied from the README Quick Start verification flow.

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

## Supported Runtimes

- Python 3.11+
- Repo-root editable install with the optional `h3` extra enabled
- macOS and Linux environments capable of installing the package surface and running `code/tests`
