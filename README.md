<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

<h1 align="center">ZPE Geo</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v7.0-e5e7eb?labelColor=111111" alt="License: SAL v7.0"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-3.11%20%7C%203.12-e5e7eb?labelColor=111111" alt="Python 3.11 and 3.12"></a>
  <a href="proofs/artifacts/2026-03-21_operator_status/README.md"><img src="https://img.shields.io/badge/operator%20status-current%20pack-e5e7eb?labelColor=111111" alt="Operator status: current pack"></a>
</p>

ZPE-Geo ships a repo-local Python package for deterministic trajectory encoding, H3-backed indexing helpers, and maneuver-search utilities over shipped fixtures.

This README only keeps claims that are exercised by the repo CI test surface and anchored to proof files committed in this repository. Historical and operator-status material remains available through the proof routes below.

## CI-Exercised Surface

| Claim | CI coverage | Proof artifact |
| --- | --- | --- |
| `encode_trajectory` and `decode_trajectory` round-trip shipped XY and WGS84 fixtures without dropping point counts | `code/tests/test_codec.py`, `code/tests/test_roundtrip.py`, `code/tests/test_edge_cases.py` | [`proofs/artifacts/fixture_benchmarks/`](proofs/artifacts/fixture_benchmarks/) |
| `ManeuverSearchIndex` builds and answers deterministic label, bounding-box, and radius queries on repo-local fixtures | `code/tests/test_search.py`, `code/tests/test_search_comprehensive.py` | [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json) |
| `H3Bridge` roundtrip and cell-path behavior stays stable across tested resolutions and edge coordinates | `code/tests/test_h3bridge.py`, `code/tests/test_h3bridge_resolution.py` | [`proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json`](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json) |
| The repo-root package surface installs as an editable package and builds as a distribution | GitHub Actions `CI`, local `python -m build` | [`proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md`](proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md) |

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
