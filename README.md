<h1 align="center">ZPE Geo</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Zer0pa%20SAL-e5e7eb?labelColor=111111" alt="License: Zer0pa SAL"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-3.11%2B-e5e7eb?labelColor=111111" alt="Python 3.11+"></a>
  <img src="https://img.shields.io/badge/release%20posture-always--in--beta-e5e7eb?labelColor=111111" alt="Release posture: always in beta">
  <a href="proofs/artifacts/2026-03-21_operator_status/README.md"><img src="https://img.shields.io/badge/current%20operator%20state-red%20claims%20remain-e5e7eb?labelColor=111111" alt="Current operator state: red claims remain"></a>
  <a href="proofs/artifacts/2026-02-20_zpe_geo_wave1/claim_status_delta.md"><img src="https://img.shields.io/badge/historical%20bundle-archived%20only-e5e7eb?labelColor=111111" alt="Historical bundle: archived only"></a>
</p>
<p align="center">
  <a href="code/README.md"><img src="https://img.shields.io/badge/quick%20verify-package%20surface-e5e7eb?labelColor=111111" alt="Quick verify: package surface"></a>
  <a href="proofs/artifacts/2026-03-21_operator_status/README.md"><img src="https://img.shields.io/badge/proof%20anchors-operator%20pack%20%2B%20gates-e5e7eb?labelColor=111111" alt="Proof anchors: operator pack and gate map"></a>
  <a href="docs/ARCHITECTURE.md"><img src="https://img.shields.io/badge/architecture-repo%20map-e5e7eb?labelColor=111111" alt="Architecture: repo map"></a>
  <a href="docs/LEGAL_BOUNDARIES.md"><img src="https://img.shields.io/badge/public%20limits-explicit%20boundary-e5e7eb?labelColor=111111" alt="Public limits: explicit boundary"></a>
  <a href="docs/ARCHITECTURE.md"><img src="https://img.shields.io/badge/docs-architecture%20map-e5e7eb?labelColor=111111" alt="Docs: architecture map"></a>
</p>
<p align="center">
  <a href="#quick-start">Quick Start</a> |
  <a href="#what-this-is">What This Is</a> |
  <a href="#commercial-readiness">Commercial Readiness</a> |
  <a href="#go-next">Go Next</a>
</p>

---

## What This Is

Compress movement traces and keep them spatially searchable. Fleet routes, vessel tracks, AV telemetry, logistics trajectories — indexed during encoding so downstream lookup does not need the raw stream.

ZPE-Geo is deterministic trajectory compression with H3 hexagonal spatial indexing, a maneuver-search surface on the compressed representation, and fidelity validation. Trajectories are encoded as sequences of 8-compass direction tokens with magnitude quantisation and RLE compression. The strongest current wedge is storage plus spatial indexing: the committed AV maneuver benchmark now measures p@10 mean `0.33` (`left_turn` `0.0`, `lane_merge` `0.0`, `stop` `1.0`), so this repo should not currently be read as a strong maneuver-ranking result.

Zer0pa SAL is free below $100M annual revenue. See [LICENSE](LICENSE).

| Field | Value |
|-------|-------|
| Architecture | TRAJECTORY_MANIFOLD |
| Encoding | H3_HEX_PACK |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| AIS_CR | 475× (lossy; quant_step=0.25m) | vs Douglas-Peucker ~315× (also lossy) |
| AV_CR | 107× (lossy; quant_step=0.25m) | — |
| SEARCH | p@10 0.33 mean (`left_turn` 0.0, `lane_merge` 0.0, `stop` 1.0) | committed AV benchmark path |
| ENCODE_P95 | 0.12 | ms |

> Sources: `AIS_CR`, `AV_CR`, and `ENCODE_P95` remain historical-only Wave-1 metrics from [`proofs/artifacts/2026-02-20_zpe_geo_wave1/`](proofs/artifacts/2026-02-20_zpe_geo_wave1/).
>
> `SEARCH` was recomputed on `2026-04-15` on the committed benchmark path in `code/scripts/gate_c_benchmarks.py` against `code/fixtures/av_argoverse2_fixture_v1.json` after removing benchmark label injection from `ManeuverSearchIndex.build()`.
>
> The March 21 operator pack remains the governing release-readiness surface.

## Competitive Benchmarks

> Wave-1 AIS corpus (190 trajectories). Source: [`proofs/artifacts/2026-02-20_zpe_geo_wave1/`](proofs/artifacts/2026-02-20_zpe_geo_wave1/)

> **Framing disclosure:** ZPE-Geo is a lossy trajectory codec (lossy at quant_step=0.25m; max coordinate error 0.0018° ≈ 200m at equator on real NOAA AIS data). Douglas-Peucker is also lossy, so the comparison below is lossy-vs-lossy. Neither codec preserves lossless coordinates. On real-world NOAA AIS extracts, coordinate_exact_match_count = 0/5. See [`proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json).

| Tool | AIS Ratio (median) | Notes |
|------|-------------------|-------|
| **ZPE-Geo** | **475×** | Lossy; H3-indexed; maneuver search surface exists, but the current committed AV benchmark is p@10 0.33 mean |
| Douglas-Peucker | ~315× | Lossy; no spatial index; no search |

ACM 2025: [doi:10.1145/3764920.3770598](https://dl.acm.org/doi/10.1145/3764920.3770598). Direct dataset parity with paper corpus INCONCLUSIVE.

## What We Prove

> Auditable guarantees backed by committed proof artifacts. Start at `proofs/artifacts/2026-03-21_operator_status/README.md`.

- Trajectory compression with preserved spatial query capability
- H3 hexagonal spatial indexing during encoding
- Maneuver search surface on compressed representation; current committed AV benchmark is p@10 mean `0.33`
- Lightweight test suite passes

## What We Don't Claim

- No claim of blind-clone closure (GEO-C001)
- No claim of full-corpus closure (GEO-C002)
- No claim of release readiness (GEO-C004)
- No claim of strong maneuver-retrieval quality — the committed AV benchmark path currently measures p@10 mean `0.33`, with `left_turn` and `lane_merge` at `0.0`
- No claim of superiority over incumbent geospatial compression
- Lossless coordinate preservation — compression at default settings (quant_step=0.25m) introduces up to 0.0018° (~200m at equator) coordinate error. On real NOAA AIS data, coordinate_exact_match_count = 0/5. See [`proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json`](proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json)
- Real-corpus equivalence for simulated query benchmarks — the 10M-corpus query-latency figure in historical proofs uses replicated synthetic trajectories, not a real-world corpus

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | BLOCKED |
| Commit SHA | 30bc0b69f5d6 |
| Confidence | 62.5% |
| Source | proofs/artifacts/2026-03-21_operator_status/README.md |

> Always in beta: useful now, improving continuously while release gates remain open.

> **Evaluators:** Proof surface available for inspection. See Open Risks for remaining gaps. Contact architects@zer0pa.ai.

- Supporting operator pack: [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md)
- Open gates: `GEO-C001`, `GEO-C002`, `GEO-C004`
- Confidence basis: `5 / 8` tracked claims green on [proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json)

## Tests and Verification

| Code | Check | Verdict |
|------|-------|---------|
| V_01 | Repo-local package surface | PASS |
| V_02 | Lightweight code tests | PASS |
| V_03 | GEO-C001 blind-clone closure | FAIL |
| V_04 | GEO-C002 full-corpus closure | FAIL |
| V_05 | GEO-C004 release readiness | FAIL |
| V_06 | H3 roundtrip consistency | PASS |

## Proof Anchors

| Path | State |
|------|-------|
| proofs/artifacts/2026-03-21_operator_status/README.md | VERIFIED |
| proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json | VERIFIED |
| proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md | VERIFIED |
| proofs/artifacts/2026-02-20_zpe_geo_wave1/ | ARCHIVED_ONLY |

Quickest outsider orientation:

| Route | Why |
| --- | --- |
| [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) | Governing current operator-status narrative |
| [proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) | Current claim split and open-gate map |
| [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) | Explicit public claim boundary |
| [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) | Audit route and reading order |
| [code/README.md](code/README.md) | Install-facing package surface |

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 4 |
| Modality Lanes | 4 |
| Authority Source | March 21 operator status pack |

## Quick Start

### Install from PyPI

```bash
pip install zpe-geo
```

### Quick Verify (from source)

The steps below verify the current repo-local package surface. They do not prove blind-clone closure, full-corpus closure, or release readiness.

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

After a successful repo-local verification you should have:

- an editable install of the repo-root package surface
- passing lightweight repo-local tests under `code/tests`
- an importable `zpe_geo` surface without relying on outer-workspace material

### License Boundary

- Repo-root package metadata uses `LicenseRef-Zer0pa-SAL-6.2`.
- `LICENSE` remains the in-repo legal text shipped with this checkout.
- Commercial or hosted use above the SAL threshold requires contact at `architects@zer0pa.ai`.
- `LICENSE` is the legal source of truth. Repo docs summarize it; they do not override it.

## Ecosystem

| Workstream | Route | Notes |
| --- | --- | --- |
| ZPE Geo | [github.com/Zer0pa/ZPE-Geo](https://github.com/Zer0pa/ZPE-Geo) | This geospatial codec, search, and H3 workstream. |
| ZPE-IMC | [github.com/Zer0pa/ZPE-IMC](https://github.com/Zer0pa/ZPE-IMC) | Sibling integration product in the Zer0pa portfolio. |
| ZPE-FT | [github.com/Zer0pa/ZPE-FT](https://github.com/Zer0pa/ZPE-FT) | Parallel ZPE family workstream. |
| ZPE-Bio | [github.com/Zer0pa/ZPE-Bio](https://github.com/Zer0pa/ZPE-Bio) | Parallel ZPE family workstream. |
| ZPE-IoT | [github.com/Zer0pa/ZPE-IoT](https://github.com/Zer0pa/ZPE-IoT) | Parallel ZPE family workstream. |

**Observability:** [Comet dashboard](https://www.comet.com/zer0pa/zpe-geospatial/view/new/panels) (public)

## Who This Is For

| | |
|---|---|
| **Ideal first buyer** | Mobility analytics platform or fleet telematics team |
| **Pain statement** | Large movement-trace archives are expensive to store and operationally painful to search — conventional compression destroys spatial query capability |
| **Deployment model** | Python SDK with H3 spatial backend, always in beta |
| **Family position** | Independent geospatial encoding product in the Zer0pa portfolio |

## Historical Context Only

The archived bundle under [proofs/artifacts/2026-02-20_zpe_geo_wave1/](proofs/artifacts/2026-02-20_zpe_geo_wave1/) remains part of the repo because it contains real historical evidence:

- archived performance metrics across all eight promoted claims
- archived comparator notes, including an in-repo AIS baseline comparison
- preserved contradictions that explain why archived success does not equal current release authorization

Read those facts as historical-only context through the archived wave-1 bundle, not as current release status.

## Go Next

| Need | Route |
| --- | --- |
| Current verdict and release posture | [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) |
| Current claim split and open gates | [proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json) |
| Historical Wave-1 metrics and contradictions | [proofs/artifacts/2026-02-20_zpe_geo_wave1/](proofs/artifacts/2026-02-20_zpe_geo_wave1/) |
| Audit path | [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) |
| Audit limits and exclusions | [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) |
| Architecture and evidence map | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Repo map and doc ownership | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Evidence boundary and reader routing | [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) |
| Install surface | [code/README.md](code/README.md) |

## Contributing, Security, Support

| Need | Route |
| --- | --- |
| Contribution and package surface | [code/README.md](code/README.md) |
| Evidence boundary and claim limits | [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) |
| Reader routing and contact path | [docs/LEGAL_BOUNDARIES.md](docs/LEGAL_BOUNDARIES.md) |
