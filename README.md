<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

<h1 align="center">ZPE Geo</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Zer0pa%20SAL-e5e7eb?labelColor=111111" alt="License: Zer0pa SAL"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-3.11%2B-e5e7eb?labelColor=111111" alt="Python 3.11+"></a>
  <a href="proofs/FINAL_STATUS.md"><img src="https://img.shields.io/badge/release%20posture-not%20release--ready-e5e7eb?labelColor=111111" alt="Release posture: not release-ready"></a>
  <a href="proofs/artifacts/2026-03-21_operator_status/README.md"><img src="https://img.shields.io/badge/current%20operator%20state-red%20claims%20remain-e5e7eb?labelColor=111111" alt="Current operator state: red claims remain"></a>
  <a href="proofs/artifacts/2026-02-20_zpe_geo_wave1/claim_status_delta.md"><img src="https://img.shields.io/badge/historical%20bundle-archived%20only-e5e7eb?labelColor=111111" alt="Historical bundle: archived only"></a>
</p>
<p align="center">
  <a href="code/README.md"><img src="https://img.shields.io/badge/quick%20verify-package%20surface-e5e7eb?labelColor=111111" alt="Quick verify: package surface"></a>
  <a href="proofs/FINAL_STATUS.md"><img src="https://img.shields.io/badge/proof%20anchors-final%20status%20%2B%20operator%20pack-e5e7eb?labelColor=111111" alt="Proof anchors: final status and operator pack"></a>
  <a href="docs/ARCHITECTURE.md"><img src="https://img.shields.io/badge/architecture-repo%20map-e5e7eb?labelColor=111111" alt="Architecture: repo map"></a>
  <a href="PUBLIC_AUDIT_LIMITS.md"><img src="https://img.shields.io/badge/public%20limits-explicit%20boundary-e5e7eb?labelColor=111111" alt="Public limits: explicit boundary"></a>
  <a href="docs/README.md"><img src="https://img.shields.io/badge/docs-routing%20index-e5e7eb?labelColor=111111" alt="Docs routing index"></a>
</p>
<table align="center" width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td width="25%"><a href="#quick-start"><img src=".github/assets/readme/nav/quickstart-and-license.svg" alt="Quickstart And License" width="100%"></a></td>
    <td width="25%"><a href="#what-this-is"><img src=".github/assets/readme/nav/what-this-is.svg" alt="What This Is" width="100%"></a></td>
    <td width="25%"><a href="#current-authority"><img src=".github/assets/readme/nav/current-authority.svg" alt="Current Authority" width="100%"></a></td>
    <td width="25%"><a href="#go-next"><img src=".github/assets/readme/nav/go-next.svg" alt="Go Next" width="100%"></a></td>
  </tr>
</table>

---

## What This Is

Compress movement traces and keep them searchable. Fleet routes, vessel tracks, AV telemetry, logistics trajectories — indexed during encoding so downstream search never touches the raw stream.

ZPE-Geo is deterministic trajectory compression with H3 hexagonal spatial indexing, maneuver-aware search, and fidelity validation on the compressed representation. Built for mobility analytics platforms, fleet telematics teams, and maritime AIS infrastructure where trajectory archives grow without bound and query-after-decompress is operationally painful.

Zer0pa SAL is free below $100M annual revenue. See [LICENSE](LICENSE).

| Field | Value |
|-------|-------|
| Architecture | TRAJECTORY_MANIFOLD |
| Encoding | H3_HEX_PACK |

## Key Metrics

| Metric | Value | Baseline |
|--------|-------|----------|
| AIS_CR | 475× | vs Douglas-Peucker ~315× |
| AV_CR | 107× | — |
| SEARCH | p@10 1.0 | — |
| ENCODE_P95 | 0.12 | ms |

> Source: [`proofs/CONSOLIDATED_PROOF_REPORT.md`](proofs/CONSOLIDATED_PROOF_REPORT.md) | [`proofs/artifacts/2026-02-20_zpe_geo_wave1/`](proofs/artifacts/2026-02-20_zpe_geo_wave1/)
>
> Note: All metrics from Wave-1 archived proofs. Does not override current March 21 red-state operator posture.

## Competitive Benchmarks

> Wave-1 AIS corpus (190 trajectories). Source: [`proofs/artifacts/2026-02-20_zpe_geo_wave1/`](proofs/artifacts/2026-02-20_zpe_geo_wave1/)

| Tool | AIS Ratio (median) | Notes |
|------|-------------------|-------|
| **ZPE-Geo** | **475×** | H3-indexed; search preserved |
| Douglas-Peucker | ~315× | no spatial index; no search |

ACM 2025: [doi:10.1145/3764920.3770598](https://dl.acm.org/doi/10.1145/3764920.3770598). Direct dataset parity with paper corpus INCONCLUSIVE.

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3.4.gif" alt="ZPE Geo Upper Insert" width="100%">
</p>

## What We Prove

> Auditable guarantees backed by committed proof artifacts. Start at `AUDITOR_PLAYBOOK.md`.

- Trajectory compression with preserved query capability
- H3 hexagonal spatial indexing during encoding
- Maneuver-aware search on compressed representation
- Lightweight test suite passes

## What We Don't Claim

- No claim of blind-clone closure (GEO-C001)
- No claim of full-corpus closure (GEO-C002)
- No claim of release readiness (GEO-C004)
- No claim of superiority over incumbent geospatial compression
- Real-corpus equivalence for simulated query benchmarks — the 10M-corpus query-latency figure in historical proofs uses replicated synthetic trajectories, not a real-world corpus

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3.5.gif" alt="ZPE Geo Lower Insert" width="100%">
</p>

## Commercial Readiness

| Field | Value |
|-------|-------|
| Verdict | NOT_RELEASE_READY |
| Commit SHA | bb9b5e39fc2e |
| Confidence | 62.5% |
| Source | proofs/FINAL_STATUS.md |

> **Evaluators:** Proof surface available for inspection. See Open Risks for remaining gaps. Contact hello@zer0pa.com.

- Supporting operator pack: [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md)
- Open gates: `GEO-C001`, `GEO-C002`, `GEO-C004`
- Confidence basis: `5 / 8` tracked claims green on [proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json)

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3-2.gif" alt="ZPE Geo Mid Masthead" width="100%">
</p>

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
| proofs/FINAL_STATUS.md | VERIFIED |
| proofs/CONSOLIDATED_PROOF_REPORT.md | VERIFIED |
| proofs/artifacts/2026-03-21_operator_status/README.md | VERIFIED |
| proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json | VERIFIED |
| proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md | VERIFIED |

Quickest outsider orientation:

| Route | Why |
| --- | --- |
| [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) | Governing current repo verdict |
| [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) | Explicit public claim boundary |
| [AUDITOR_PLAYBOOK.md](AUDITOR_PLAYBOOK.md) | Audit route and reading order |
| [code/README.md](code/README.md) | Install-facing package surface |

## Repo Shape

| Field | Value |
|-------|-------|
| Proof Anchors | 5 |
| Modality Lanes | 4 |
| Authority Source | proofs/FINAL_STATUS.md |

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3-3.gif" alt="ZPE Geo Lower Masthead" width="100%">
</p>

## Quick Start

### Quick Verify

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

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3.6.gif" alt="ZPE Geo Authority Insert" width="100%">
</p>

## Ecosystem

| Workstream | Route | Notes |
| --- | --- | --- |
| ZPE Geo | [github.com/Zer0pa/ZPE-Geo](https://github.com/Zer0pa/ZPE-Geo) | This geospatial codec, search, and H3 workstream. |
| ZPE-IMC | [github.com/Zer0pa/ZPE-IMC](https://github.com/Zer0pa/ZPE-IMC) | Current documentation-structure reference surface reused by sibling repos. |
| ZPE-FT | [github.com/Zer0pa/ZPE-FT](https://github.com/Zer0pa/ZPE-FT) | Parallel ZPE family workstream. |
| ZPE-Bio | [github.com/Zer0pa/ZPE-Bio](https://github.com/Zer0pa/ZPE-Bio) | Parallel ZPE family workstream. |
| ZPE-IoT | [github.com/Zer0pa/ZPE-IoT](https://github.com/Zer0pa/ZPE-IoT) | Parallel ZPE family workstream. |

**Observability:** [Comet dashboard](https://www.comet.com/zer0pa/zpe-geospatial/view/new/panels) (public)

## Who This Is For

| | |
|---|---|
| **Ideal first buyer** | Mobility analytics platform or fleet telematics team |
| **Pain statement** | Large movement-trace archives are expensive to store and operationally painful to search — conventional compression destroys spatial query capability |
| **Deployment model** | Python SDK with H3 spatial backend, private-stage |
| **Family position** | Product candidate — the trajectory compression problem has clear enterprise buyers |

## Historical Context Only

The archived bundle under [proofs/artifacts/2026-02-20_zpe_geo_wave1/](proofs/artifacts/2026-02-20_zpe_geo_wave1/) remains part of the repo because it contains real historical evidence:

- archived performance metrics across all eight promoted claims
- archived comparator notes, including an in-repo AIS baseline comparison
- preserved contradictions that explain why archived success does not equal current release authorization

Read those facts as historical-only context through [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md), not as current release status.

## Go Next

| Need | Route |
| --- | --- |
| Current verdict and release posture | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| Detailed current evidence and historical bundle interpretation | [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md) |
| Audit path | [AUDITOR_PLAYBOOK.md](AUDITOR_PLAYBOOK.md) |
| Audit limits and exclusions | [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) |
| Architecture and evidence map | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Docs ownership map | [docs/CANONICAL_DOC_REGISTRY.md](docs/CANONICAL_DOC_REGISTRY.md) |
| FAQ and support | [docs/FAQ.md](docs/FAQ.md), [docs/SUPPORT.md](docs/SUPPORT.md) |
| Community conduct | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Install surface | [code/README.md](code/README.md) |

## Contributing, Security, Support

| Need | Route |
| --- | --- |
| Contribution rules and docs hygiene | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Community conduct and evidence norms | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Vulnerability reporting and secret-exposure handling | [SECURITY.md](SECURITY.md) |
| Reader routing and response expectations | [docs/SUPPORT.md](docs/SUPPORT.md) |
