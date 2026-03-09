# ZPE Geo

Private staged repo for the ZPE Geo sector as of 2026-03-09.

This repo contains the extracted code, proofs, and front-door documentation for the deterministic geospatial trajectory lane. It is hardened through Phase 3 plus Phase 4 only. Phase 4.5 performance augmentation and Phase 5 blind-clone verification are explicitly deferred.

## What This Is

ZPE Geo is a deterministic geospatial trajectory package and proof surface for:

- AV-style XY trajectories
- AIS-style WGS84 vessel trajectories
- maneuver search and query latency checks
- H3 roundtrip consistency checks
- adjudicated gate artifacts for the 2026-02-20 wave bundle

The package surface lives under `code/`. The proof surface lives under `proofs/`. Operator-only material remains outside this repo boundary.

## Current Status Snapshot

The adjudicated bundle in `proofs/artifacts/2026-02-20_zpe_geo_wave1/` still resolves the eight core claims to `PASS`, with known max-wave contradictions and open residual risks preserved rather than hidden.

| Surface | Current staged fact | Evidence |
| --- | --- | --- |
| Core claim count | `8 PASS / 0 FAIL / 0 INCONCLUSIVE / 0 PAUSED_EXTERNAL` | `proofs/artifacts/2026-02-20_zpe_geo_wave1/claim_status_delta.md` |
| AV compression | median `107.39x` over `210` trajectories | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json` |
| AIS compression | median `475.32x` over `190` trajectories | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json` |
| AV fidelity | mean RMSE `0.823 m` | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json` |
| AIS fidelity | mean DTW `2.619 m` | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json` |
| Search quality | mean `P@10 = 1.0` | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_maneuver_search_eval.json` |
| Query latency | `0.064 ms` p95 at simulated `10,000,200` corpus size | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json` |
| Streaming latency | `0.122 ms` p95 over `40,000` updates | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json` |
| H3 consistency | backend `official_h3`, `0` failures | `proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json` |

## What Is In This Repo

- `code/zpe_geo/`: Python package
- `code/scripts/`: gate and packaging scripts
- `code/tests/`: lightweight unit tests copied from the sector lane
- `code/fixtures/`: small deterministic fixtures only
- `docs/`: legal, support, and navigation surfaces
- `proofs/`: staged proof bundle, runbooks, and summary reports

## What Stays Outside This Repo

- `.env`
- `data/external_samples/`
- raw `third_party/`
- outer-shell orchestration outputs and meta reports
- Phase 5 verification outputs

The copied code is path-hardened to look for operator-only `third_party/` and `data/external_samples/` one level above the repo root when those resources are needed.

## Minimal Sanity

This is the only sanctioned quick check in the current phase:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[dev]"
python - <<'PY'
from zpe_geo import H3Bridge, decode_trajectory, encode_trajectory
print("zpe-geo import OK")
print("h3 backend:", H3Bridge().backend)
PY
```

This is import and layout sanity only. It is not a substitute for Phase 5 verification.

## Audit Entry Points

- `docs/README.md`
- `AUDITOR_PLAYBOOK.md`
- `PUBLIC_AUDIT_LIMITS.md`
- `proofs/FINAL_STATUS.md`
- `proofs/CONSOLIDATED_PROOF_REPORT.md`
